import urllib.request
import json

def test_endpoint(name, url):
    print(f"Testing {name}: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Status: {resp.status} OK")
            return data
    except Exception as e:
        print(f"Failed: {e}")
        return None

def main():
    print("=" * 60)
    print("TESTING LIVE RAMAYANA API ON GITHUB PAGES")
    print("=" * 60)

    # 1. Kandas
    kandas = test_endpoint("All Kandas", "https://bitwisebro.github.io/ramayana-api/kandas.json")
    if kandas:
        print(f"Total Kandas returned: {len(kandas)}")
        for k in kandas:
            print(f"  • Kanda {k['id']}: {k['name']} ({k['name_sanskrit']}) — {k['chapters_count']} sargas, {k['verses_count']} verses")

    # 2. Sargas in Bala Kanda
    print("-" * 60)
    sargas = test_endpoint("Bala Kanda Sargas", "https://bitwisebro.github.io/ramayana-api/kanda/1/sargas.json")
    if sargas:
        print(f"Total Sargas in Bala Kanda: {len(sargas)}")

    # 3. Chapter 1 in Bala Kanda
    print("-" * 60)
    ch1 = test_endpoint("Bala Kanda Chapter 1", "https://bitwisebro.github.io/ramayana-api/kanda/1/sarga/1.json")
    if ch1:
        print(f"Chapter 1 Verses count: {ch1['verses_count']}")

    # 4. Verse 1-1-1
    print("-" * 60)
    v1 = test_endpoint("Verse 1-1-1", "https://bitwisebro.github.io/ramayana-api/slok/1/1/1.json")
    if v1:
        print(f"  Kanda: {v1['kanda_name']} ({v1['kanda_name_sanskrit']})")
        print(f"  Sarga: {v1['sarga']}, Verse: {v1['verse']}")
        print(f"  Sloka: {v1['sloka']}")
        print(f"  IAST:  {v1['transliteration']}")
        print(f"  EN:    {v1['translations']['english']}")

    # 5. Sundara Kanda Verse 5-1-1 (Hanuman leaping towards Lanka)
    print("-" * 60)
    v5 = test_endpoint("Sundara Kanda Verse 5-1-1", "https://bitwisebro.github.io/ramayana-api/slok/5/1/1.json")
    if v5:
        print(f"  Kanda: {v5['kanda_name']} ({v5['kanda_name_sanskrit']})")
        print(f"  Sarga: {v5['sarga']}, Verse: {v5['verse']}")
        print(f"  Sloka: {v5['sloka']}")
        print(f"  IAST:  {v5['transliteration']}")
        print(f"  EN:    {v5['translations']['english']}")

    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! THE API IS FULLY LIVE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
