import os
import json
import sqlite3
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ramayana.db"
DOCS_DIR = BASE_DIR / "docs"

def main():
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        return

    print("Generating GitHub Pages Static API in 'docs/'...")
    if DOCS_DIR.exists():
        # Keep index.html or 404.html if they exist, or recreate clean
        for item in DOCS_DIR.iterdir():
            if item.name not in ["index.html", "404.html", "CNAME", "style.css", "app.js"]:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    else:
        DOCS_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Generate /kandas.json & /kandas/index.json
    cur.execute("SELECT id, name, name_sanskrit, slug, description, chapters_count, verses_count FROM kandas ORDER BY id")
    kandas = []
    for row in cur.fetchall():
        kandas.append({
            "id": row[0],
            "name": row[1],
            "name_sanskrit": row[2],
            "slug": row[3],
            "description": row[4],
            "chapters_count": row[5],
            "verses_count": row[6]
        })

    def save_json(file_path, data):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Save kandas
    save_json(DOCS_DIR / "kandas.json", kandas)
    save_json(DOCS_DIR / "kandas" / "index.json", kandas)
    print("✓ Created /kandas.json")

    # 2. Generate per-Kanda and per-Sarga endpoints
    for k in kandas:
        kid = k["id"]
        # Save individual kanda detail
        save_json(DOCS_DIR / "kanda" / f"{kid}.json", k)
        save_json(DOCS_DIR / "kanda" / str(kid) / "index.json", k)

        # Sargas in this kanda
        cur.execute("SELECT sarga_number, verses_count FROM sargas WHERE kanda_id = ? ORDER BY sarga_number", (kid,))
        sargas_list = []
        for srow in cur.fetchall():
            sargas_list.append({
                "kanda_id": kid,
                "kanda_name": k["name"],
                "sarga_number": srow[0],
                "verses_count": srow[1]
            })

        save_json(DOCS_DIR / "kanda" / str(kid) / "sargas.json", sargas_list)
        save_json(DOCS_DIR / "kanda" / str(kid) / "sargas" / "index.json", sargas_list)

        # Per sarga details with all verses inside it
        for s in sargas_list:
            snum = s["sarga_number"]
            cur.execute("""
            SELECT verse_number, sloka, transliteration, translation_en, translation_hi, translation_te
            FROM verses WHERE kanda_id = ? AND sarga_number = ? ORDER BY verse_number
            """, (kid, snum))
            
            verses = []
            for vrow in cur.fetchall():
                v_obj = {
                    "kanda": kid,
                    "kanda_name": k["name"],
                    "kanda_name_sanskrit": k["name_sanskrit"],
                    "sarga": snum,
                    "verse": vrow[0],
                    "sloka": vrow[1],
                    "transliteration": vrow[2],
                    "translations": {
                        "english": vrow[3],
                        "hindi": vrow[4],
                        "telugu": vrow[5]
                    }
                }
                verses.append(v_obj)

                # Individual verse endpoint: /slok/:kanda/:sarga/:verse.json
                slok_path_json = DOCS_DIR / "slok" / str(kid) / str(snum) / f"{vrow[0]}.json"
                slok_path_dir = DOCS_DIR / "slok" / str(kid) / str(snum) / str(vrow[0]) / "index.json"
                save_json(slok_path_json, v_obj)
                save_json(slok_path_dir, v_obj)

            sarga_payload = {
                "kanda": kid,
                "kanda_name": k["name"],
                "kanda_name_sanskrit": k["name_sanskrit"],
                "sarga": snum,
                "verses_count": len(verses),
                "verses": verses
            }
            save_json(DOCS_DIR / "kanda" / str(kid) / "sarga" / f"{snum}.json", sarga_payload)
            save_json(DOCS_DIR / "kanda" / str(kid) / "sarga" / str(snum) / "index.json", sarga_payload)

        print(f"✓ Kanda {kid} ({k['name']}) static API generated ({len(sargas_list)} sargas)")

    conn.close()
    print("\n" + "=" * 50)
    print("STATIC API GENERATION FOR GITHUB PAGES COMPLETE!")
    print(f"Output files stored in: {DOCS_DIR}")

if __name__ == "__main__":
    main()
