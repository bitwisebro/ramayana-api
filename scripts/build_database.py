import os
import re
import json
import sqlite3
from pathlib import Path
from transliterator import to_iast

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_SOURCE = BASE_DIR / "data-source"
SAN_DIR = DATA_SOURCE / "san"
TRANS_DIR = DATA_SOURCE / "translations"
OUTPUT_DATA_DIR = BASE_DIR / "data"
PUBLIC_API_DIR = BASE_DIR / "public" / "api" / "v1"

KANDAS_META = [
    {
        "id": 1,
        "name": "Bala Kanda",
        "name_sanskrit": "बालकाण्डम्",
        "slug": "bala-kanda",
        "file": "balakanda_all.json",
        "trans_dir": "bala_kanda",
        "description": "The Book of Youth: Depicts the divine birth of Rama, his early life, slaying of demons, and marriage to Sita."
    },
    {
        "id": 2,
        "name": "Ayodhya Kanda",
        "name_sanskrit": "अयोध्याकाण्डम्",
        "slug": "ayodhya-kanda",
        "file": "ayodhyakanda_all.json",
        "trans_dir": "ayodhya_kanda",
        "description": "The Book of Ayodhya: Preparations for Rama's coronation, Kaikeyi's boons, and Rama's exile to the forest with Sita and Lakshmana."
    },
    {
        "id": 3,
        "name": "Aranya Kanda",
        "name_sanskrit": "अरण्यकाण्डम्",
        "slug": "aranya-kanda",
        "file": "aranyakanda_all.json",
        "trans_dir": "aranya_kanda",
        "description": "The Book of the Forest: Forest life of Rama, encounters with sages and demons, Surpanakha's episode, and Sita's abduction by Ravana."
    },
    {
        "id": 4,
        "name": "Kishkindha Kanda",
        "name_sanskrit": "किष्किन्धाकाण्डम्",
        "slug": "kishkindha-kanda",
        "file": "kishkindhakanda_all.json",
        "trans_dir": "kishkindha_kanda",
        "description": "The Book of Kishkindha: Rama's alliance with Sugriva and Hanuman, the slaying of Vali, and the search for Sita across all directions."
    },
    {
        "id": 5,
        "name": "Sundara Kanda",
        "name_sanskrit": "सुन्दरकाण्डम्",
        "slug": "sundara-kanda",
        "file": "sundarakanda_all.json",
        "trans_dir": "sundara_kanda",
        "description": "The Book of Beauty: Hanuman's heroic leap across the ocean to Lanka, locating Sita in the Ashoka Vatika, and burning Lanka."
    },
    {
        "id": 6,
        "name": "Yuddha Kanda",
        "name_sanskrit": "युद्धकाण्डम्",
        "slug": "yuddha-kanda",
        "file": "yudhhakanda_all.json",
        "trans_dir": "yuddha_kanda",
        "description": "The Book of War: Building the bridge to Lanka, the epic battle between Rama's army and Ravana's forces, victory, and coronation in Ayodhya."
    },
    {
        "id": 7,
        "name": "Uttara Kanda",
        "name_sanskrit": "उत्तरकाण्डम्",
        "slug": "uttara-kanda",
        "file": "uttarakanda_all.json",
        "trans_dir": "uttara_kanda",
        "description": "The Epilogue: Rama's righteous reign (Rama Rajya), the birth of Lava and Kusha, Sita's trial, and Rama's final departure."
    }
]

def load_json_safe(path):
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f, strict=False)
    except Exception as e:
        print(f"Warning: Failed reading {path}: {e}")
        return None

def extract_verse_number(sloka_str, fallback_num):
    # Pattern matching ॥1-1-1॥ or ॥१-१-१॥ or ॥1॥
    m = re.search(r'[॥\|](\d+)[-–—](\d+)[-–—](\d+)[॥\|]', sloka_str)
    if m:
        return int(m.group(3))
    
    # Devanagari numerals
    dev_num_map = str.maketrans('०१२३४५६७८९', '0123456789')
    m_dev = re.search(r'[॥\|]([०-९]+)[-–—]([०-९]+)[-–—]([०-९]+)[॥\|]', sloka_str)
    if m_dev:
        num_str = m_dev.group(3).translate(dev_num_map)
        return int(num_str)
    
    m_single = re.search(r'[॥\|](\d+)[॥\|]', sloka_str)
    if m_single:
        return int(m_single.group(1))

    m_dev_single = re.search(r'[॥\|]([०-९]+)[॥\|]', sloka_str)
    if m_dev_single:
        return int(m_dev_single.group(1).translate(dev_num_map))

    return fallback_num

def setup_database(db_path):
    if db_path.exists():
        db_path.unlink()
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE kandas (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        name_sanskrit TEXT NOT NULL,
        slug TEXT NOT NULL,
        description TEXT,
        chapters_count INTEGER DEFAULT 0,
        verses_count INTEGER DEFAULT 0
    );
    """)
    
    cur.execute("""
    CREATE TABLE sargas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanda_id INTEGER NOT NULL,
        sarga_number INTEGER NOT NULL,
        verses_count INTEGER DEFAULT 0,
        FOREIGN KEY (kanda_id) REFERENCES kandas(id)
    );
    """)
    
    cur.execute("""
    CREATE TABLE verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanda_id INTEGER NOT NULL,
        sarga_number INTEGER NOT NULL,
        verse_number INTEGER NOT NULL,
        sloka TEXT NOT NULL,
        transliteration TEXT,
        translation_en TEXT,
        translation_hi TEXT,
        translation_te TEXT,
        FOREIGN KEY (kanda_id) REFERENCES kandas(id)
    );
    """)
    
    # Create indexes for high-speed queries
    cur.execute("CREATE INDEX idx_verses_lookup ON verses(kanda_id, sarga_number, verse_number);")
    cur.execute("CREATE INDEX idx_sargas_lookup ON sargas(kanda_id, sarga_number);")
    
    # Create FTS5 virtual table for lightning-fast search
    cur.execute("""
    CREATE VIRTUAL TABLE verses_fts USING fts5(
        verse_id UNINDEXED,
        kanda_id UNINDEXED,
        sarga_number UNINDEXED,
        verse_number UNINDEXED,
        sloka,
        transliteration,
        translation_en,
        translation_hi
    );
    """)
    
    conn.commit()
    return conn

def main():
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = OUTPUT_DATA_DIR / "ramayana.db"
    print(f"Initializing SQLite database at: {db_path}")
    conn = setup_database(db_path)
    cur = conn.cursor()

    all_kandas_summary = []
    total_all_verses = 0

    for kanda in KANDAS_META:
        kanda_id = kanda["id"]
        kanda_name = kanda["name"]
        san_file = SAN_DIR / kanda["file"]
        
        print(f"\nProcessing Kanda {kanda_id}: {kanda_name}...")
        san_data = load_json_safe(san_file)
        if not san_data:
            print(f"Error: Missing {san_file}")
            continue
            
        k_key = list(san_data.keys())[0]
        chapters = san_data[k_key].get("chapters", [])
        
        kanda_verse_count = 0
        sargas_summary = []

        for ch in chapters:
            sarga_num = ch.get("chapter_number")
            raw_slokas = ch.get("slokas", [])
            
            # Load translations for this sarga
            en_trans_file = TRANS_DIR / "en" / kanda["trans_dir"] / f"chapter{sarga_num}.json"
            hi_trans_file = TRANS_DIR / "hi" / kanda["trans_dir"] / f"chapter{sarga_num}.json"
            te_trans_file = TRANS_DIR / "te" / kanda["trans_dir"] / f"chapter{sarga_num}.json"
            
            en_data = load_json_safe(en_trans_file)
            hi_data = load_json_safe(hi_trans_file)
            te_data = load_json_safe(te_trans_file)
            
            en_verses = en_data.get("verses", {}) if en_data else {}
            hi_verses = hi_data.get("verses", {}) if hi_data else {}
            te_verses = te_data.get("verses", {}) if te_data else {}
            
            # Insert Sarga record
            cur.execute(
                "INSERT INTO sargas (kanda_id, sarga_number, verses_count) VALUES (?, ?, ?)",
                (kanda_id, sarga_num, len(raw_slokas))
            )
            sarga_db_id = cur.lastrowid
            
            sarga_verse_count = 0
            
            for idx, sloka in enumerate(raw_slokas, start=1):
                verse_num = extract_verse_number(sloka, idx)
                verse_str_key = str(verse_num)
                
                # Fetch translations
                tr_en = en_verses.get(verse_str_key) or en_verses.get(str(idx)) or ""
                tr_hi = hi_verses.get(verse_str_key) or hi_verses.get(str(idx)) or ""
                tr_te = te_verses.get(verse_str_key) or te_verses.get(str(idx)) or ""
                
                iast_text = to_iast(sloka)
                
                cur.execute("""
                INSERT INTO verses (kanda_id, sarga_number, verse_number, sloka, transliteration, translation_en, translation_hi, translation_te)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (kanda_id, sarga_num, verse_num, sloka, iast_text, tr_en, tr_hi, tr_te))
                
                verse_row_id = cur.lastrowid
                
                # Insert into FTS5 index
                cur.execute("""
                INSERT INTO verses_fts (verse_id, kanda_id, sarga_number, verse_number, sloka, transliteration, translation_en, translation_hi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (verse_row_id, kanda_id, sarga_num, verse_num, sloka, iast_text, tr_en, tr_hi))
                
                sarga_verse_count += 1
                
            kanda_verse_count += sarga_verse_count
            sargas_summary.append({
                "sarga_number": sarga_num,
                "verses_count": sarga_verse_count
            })
            
        cur.execute("""
        INSERT INTO kandas (id, name, name_sanskrit, slug, description, chapters_count, verses_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (kanda_id, kanda["name"], kanda["name_sanskrit"], kanda["slug"], kanda["description"], len(chapters), kanda_verse_count))
        
        all_kandas_summary.append({
            "id": kanda_id,
            "name": kanda["name"],
            "name_sanskrit": kanda["name_sanskrit"],
            "slug": kanda["slug"],
            "description": kanda["description"],
            "chapters_count": len(chapters),
            "verses_count": kanda_verse_count
        })
        
        total_all_verses += kanda_verse_count
        print(f"✓ Kanda {kanda_id} complete: {len(chapters)} Sargas, {kanda_verse_count} Verses")

    conn.commit()
    conn.close()

    print("\n" + "=" * 50)
    print(f"DATABASE BUILD COMPLETE: {len(all_kandas_summary)} Kandas, {total_all_verses} Verses indexed!")
    print(f"Saved SQLite DB to: {db_path}")

if __name__ == "__main__":
    main()
