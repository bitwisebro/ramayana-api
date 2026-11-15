# Ramayana API (रामायणम् API)

[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-blue?style=flat-square&logo=github)](https://bitwisebro.github.io/ramayana-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Verses](https://img.shields.io/badge/Verses-23%2C334%20(Dataset)-orange?style=flat-square)](#)
[![Chapters](https://img.shields.io/badge/Sargas-645-yellow?style=flat-square)](#)
[![Books](https://img.shields.io/badge/Kandas-7-red?style=flat-square)](#)

> **A keyless, open-source, serverless RESTful JSON API for Sage Valmiki's Ramayana, inspired by and built following the model of [vedicscriptures.github.io](https://vedicscriptures.github.io).**

> [!NOTE]
> **On Verse Counts:** While tradition classically refers to the Valmiki Ramayana as having 24,000 verses (*Chaturvimshati Sahasri*), the exact verse count varies across recensions (Northern, Southern, Eastern) and critical editions. The **23,334 verses** advertised here represent the specific count digitized and aligned in this dataset (sourced from Sanskrit Wikisource with IIT Kanpur critical edition corrections).

---

## 🌟 Highlights

* **Keyless & 100% Free:** Zero registration, zero rate limits, and hosted directly via GitHub Pages CDN.
* **Comprehensive Dataset:** All **7 Kandas**, **645 Sargas (Chapters)**, and **23,334 indexed Shlokas (Verses)** in this edition.
* **Multilingual:** Sanskrit text in original Devanagari script, IAST romanized transliteration, and English/regional translations.
* **Fast & Static:** Powered by pre-rendered, minified JSON static files served with zero latency.

---

## 📖 API Endpoints

### Base URL
```
https://bitwisebro.github.io/ramayana-api/
```

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/kandas.json` | List all 7 Kandas with descriptions and totals |
| `GET` | `/kanda/:kanda_id.json` | Get details and overview of a specific Kanda (1 to 7) |
| `GET` | `/kanda/:kanda_id/sargas.json` | List all chapters (Sargas) in a Kanda with verse counts |
| `GET` | `/kanda/:kanda_id/sarga/:sarga_id.json` | Get a complete chapter with all its verses |
| `GET` | `/slok/:kanda_id/:sarga_id/:verse_id.json` | Get a specific verse with text, IAST, and translations |

---

## ⚡ Quick Examples

### 1. Fetching a Specific Verse (cURL)

```bash
# Bala Kanda, Chapter 1, Verse 1
curl -s https://bitwisebro.github.io/ramayana-api/slok/1/1/1.json
```

**Response:**
```json
{
  "kanda": 1,
  "kanda_name": "Bala Kanda",
  "kanda_name_sanskrit": "बालकाण्डम्",
  "sarga": 1,
  "verse": 1,
  "sloka": "तपस्स्वाध्याय निरतं तपस्वी वाग्विदां वरम् ।नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुंगवम् ॥१-१-१॥",
  "transliteration": "tapassvādhyāya nirataṁ tapasvī vāgvidāṁ varam ।nāradaṁ paripapraccha vālmīkirmunipuṁgavam ॥1-1-1॥",
  "translations": {
    "english": "Ascetic Valmiki enquired of Narada, preeminent among the sages ever engaged in the practice of religious austerities or study of the Vedas and best among the eloquent.",
    "hindi": "",
    "telugu": "తపశ్శీలుడును, వేదాధ్యయననిరతుడును, వాక్చతురులలొ అగ్రేసరుడును..."
  }
}
```

### 2. JavaScript / TypeScript (fetch)

```javascript
const res = await fetch('https://bitwisebro.github.io/ramayana-api/slok/5/1/1.json');
const verse = await res.json();
console.log(verse.sloka);
console.log(verse.translations.english);
```

### 3. Python

```python
import requests

url = "https://bitwisebro.github.io/ramayana-api/slok/1/1/1.json"
data = requests.get(url).json()

print(data["sloka"])
print(data["translations"]["english"])
```

---

## 📚 Structure of the Epic (The 7 Kandas)

1. **Bala Kanda** (`बालकाण्डम्`) — 77 Sargas, 2,267 Verses
2. **Ayodhya Kanda** (`अयोध्याकाण्डम्`) — 119 Sargas, 4,307 Verses
3. **Aranya Kanda** (`अरण्यकाण्डम्`) — 75 Sargas, 2,447 Verses
4. **Kishkindha Kanda** (`किष्किन्धाकाण्डम्`) — 67 Sargas, 2,462 Verses
5. **Sundara Kanda** (`सुन्दरकाण्डम्`) — 68 Sargas, 2,810 Verses
6. **Yuddha Kanda** (`युद्धकाण्डम्`) — 128 Sargas, 5,578 Verses
7. **Uttara Kanda** (`उत्तरकाण्डम्`) — 111 Sargas, 3,463 Verses

---

## 🛠️ Local Development & Scripts

### Rebuilding the Database & Static API
To regenerate the SQLite database and static JSON files from the source files:

```bash
# 1. Build SQLite DB & FTS5 full-text search index
python scripts/build_database.py

# 2. Generate static API JSON tree in docs/
python scripts/generate_static_api.py
```

### Testing the Web Portal Locally
Run Python's built-in HTTP server from the `docs/` folder:

```bash
cd docs
python -m http.server 8000
```
Then visit `http://localhost:8000` to open the interactive playground.

---

## 🚀 Deploying to GitHub Pages

1. Push this project to `https://github.com/bitwisebro/ramayana-api`:
   ```bash
   git add .
   git commit -m "feat: complete Valmiki Ramayana static API & documentation"
   git branch -M main
   git remote add origin https://github.com/bitwisebro/ramayana-api.git
   git push -u origin main
   ```
3. In your GitHub repository settings, go to **Settings &rarr; Pages**:
   * **Source:** Deploy from a branch
   * **Branch:** `main`
   * **Folder:** `/docs`
4. Click **Save**! Within 1-2 minutes, your Ramayana API will be live globally.

---

## 📜 Credits & Acknowledgments

* Text sourced and aligned from Sanskrit Wikisource, IIT Kanpur Gita Supersite, and open digital scripture repositories.
* English translations based on Manmatha Nath Dutt (1891–1894).
* Inspired by the wonderful open-source work of **[vedicscriptures](https://github.com/vedicscriptures)**.
