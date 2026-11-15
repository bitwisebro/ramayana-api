"""Devanagari to IAST (International Alphabet of Sanskrit Transliteration) Converter."""

VOWELS = {
    'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
    'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ', 'ए': 'e', 'ऐ': 'ai',
    'ओ': 'o', 'औ': 'au'
}

MATRAS = {
    'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
    'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ', 'े': 'e', 'ै': 'ai',
    'ो': 'o', 'ौ': 'au'
}

CONSONANTS = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ',
    'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
    'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
    'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h',
    'ळ': 'ḻ'
}

MODIFIERS = {
    'ं': 'ṁ',
    'ः': 'ḥ',
    'ँ': 'm̐',
    'ऽ': "'"
}

VIRAMA = '्'

NUMERALS = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

def to_iast(text: str) -> str:
    """Converts Devanagari text to IAST romanization."""
    if not text:
        return ""
    
    result = []
    i = 0
    n = len(text)
    
    while i < n:
        ch = text[i]
        
        if ch in NUMERALS:
            result.append(NUMERALS[ch])
            i += 1
        elif ch in VOWELS:
            result.append(VOWELS[ch])
            i += 1
        elif ch in CONSONANTS:
            base = CONSONANTS[ch]
            if i + 1 < n:
                next_ch = text[i + 1]
                if next_ch == VIRAMA:
                    result.append(base)
                    i += 2
                elif next_ch in MATRAS:
                    result.append(base + MATRAS[next_ch])
                    i += 2
                else:
                    result.append(base + 'a')
                    i += 1
            else:
                result.append(base + 'a')
                i += 1
        elif ch in MATRAS:
            result.append(MATRAS[ch])
            i += 1
        elif ch in MODIFIERS:
            result.append(MODIFIERS[ch])
            i += 1
        else:
            result.append(ch)
            i += 1
            
    return "".join(result)
