#!/usr/bin/env python3
"""
Re-fetch and reformat all ESV files using the raw [N] verse markers from the API,
splitting cleanly into one verse per line.
"""
import ssl, urllib.request, urllib.parse, urllib.error, json, os, re, time

ESV_TOKEN = "c577a41c8607e92598297705b575bd6ebdac76ab"
BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study"

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

books = [
    ("Old Testament/01 - Genesis",        "Genesis",          50),
    ("Old Testament/02 - Exodus",         "Exodus",           40),
    ("Old Testament/03 - Leviticus",      "Leviticus",        27),
    ("Old Testament/04 - Numbers",        "Numbers",          36),
    ("Old Testament/05 - Deuteronomy",    "Deuteronomy",      34),
    ("Old Testament/06 - Joshua",         "Joshua",           24),
    ("Old Testament/07 - Judges",         "Judges",           21),
    ("Old Testament/08 - Ruth",           "Ruth",              4),
    ("Old Testament/09 - 1 Samuel",       "1 Samuel",         31),
    ("Old Testament/10 - 2 Samuel",       "2 Samuel",         24),
    ("Old Testament/11 - 1 Kings",        "1 Kings",          22),
    ("Old Testament/12 - 2 Kings",        "2 Kings",          25),
    ("Old Testament/13 - 1 Chronicles",   "1 Chronicles",     29),
    ("Old Testament/14 - 2 Chronicles",   "2 Chronicles",     36),
    ("Old Testament/15 - Ezra",           "Ezra",             10),
    ("Old Testament/16 - Nehemiah",       "Nehemiah",         13),
    ("Old Testament/17 - Esther",         "Esther",           10),
    ("Old Testament/18 - Job",            "Job",              42),
    ("Old Testament/19 - Psalms",         "Psalms",          150),
    ("Old Testament/20 - Proverbs",       "Proverbs",         31),
    ("Old Testament/21 - Ecclesiastes",   "Ecclesiastes",     12),
    ("Old Testament/22 - Song of Solomon","Song of Solomon",   8),
    ("Old Testament/23 - Isaiah",         "Isaiah",           66),
    ("Old Testament/24 - Jeremiah",       "Jeremiah",         52),
    ("Old Testament/25 - Lamentations",   "Lamentations",      5),
    ("Old Testament/26 - Ezekiel",        "Ezekiel",          48),
    ("Old Testament/27 - Daniel",         "Daniel",           12),
    ("Old Testament/28 - Hosea",          "Hosea",            14),
    ("Old Testament/29 - Joel",           "Joel",              3),
    ("Old Testament/30 - Amos",           "Amos",              9),
    ("Old Testament/31 - Obadiah",        "Obadiah",           1),
    ("Old Testament/32 - Jonah",          "Jonah",             4),
    ("Old Testament/33 - Micah",          "Micah",             7),
    ("Old Testament/34 - Nahum",          "Nahum",             3),
    ("Old Testament/35 - Habakkuk",       "Habakkuk",          3),
    ("Old Testament/36 - Zephaniah",      "Zephaniah",         3),
    ("Old Testament/37 - Haggai",         "Haggai",            2),
    ("Old Testament/38 - Zechariah",      "Zechariah",        14),
    ("Old Testament/39 - Malachi",        "Malachi",           4),
    ("New Testament/01 - Matthew",        "Matthew",          28),
    ("New Testament/02 - Mark",           "Mark",             16),
    ("New Testament/03 - Luke",           "Luke",             24),
    ("New Testament/04 - John",           "John",             21),
    ("New Testament/05 - Acts",           "Acts",             28),
    ("New Testament/06 - Romans",         "Romans",           16),
    ("New Testament/07 - 1 Corinthians",  "1 Corinthians",    16),
    ("New Testament/08 - 2 Corinthians",  "2 Corinthians",    13),
    ("New Testament/09 - Galatians",      "Galatians",         6),
    ("New Testament/10 - Ephesians",      "Ephesians",         6),
    ("New Testament/11 - Philippians",    "Philippians",       4),
    ("New Testament/12 - Colossians",     "Colossians",        4),
    ("New Testament/13 - 1 Thessalonians","1 Thessalonians",   5),
    ("New Testament/14 - 2 Thessalonians","2 Thessalonians",   3),
    ("New Testament/15 - 1 Timothy",      "1 Timothy",         6),
    ("New Testament/16 - 2 Timothy",      "2 Timothy",         4),
    ("New Testament/17 - Titus",          "Titus",             3),
    ("New Testament/18 - Philemon",       "Philemon",          1),
    ("New Testament/19 - Hebrews",        "Hebrews",          13),
    ("New Testament/20 - James",          "James",             5),
    ("New Testament/21 - 1 Peter",        "1 Peter",           5),
    ("New Testament/22 - 2 Peter",        "2 Peter",           3),
    ("New Testament/23 - 1 John",         "1 John",            5),
    ("New Testament/24 - 2 John",         "2 John",            1),
    ("New Testament/25 - 3 John",         "3 John",            1),
    ("New Testament/26 - Jude",           "Jude",              1),
    ("New Testament/27 - Revelation",     "Revelation",       22),
]

def parse_esv_raw(raw_text, book_name, ch):
    """Parse ESV raw API text with [N] markers into clean verse-per-line format."""
    # Split on [N] markers — these are unambiguous
    parts = re.split(r'\[(\d+)\]', raw_text)
    # parts: ['intro text', '1', 'verse 1 text', '2', 'verse 2 text', ...]
    verse_lines = []
    i = 1
    while i < len(parts) - 1:
        verse_num = parts[i].strip()
        verse_text = parts[i + 1].strip()
        # Collapse internal whitespace/newlines within a verse
        verse_text = " ".join(verse_text.split())
        if verse_text:
            verse_lines.append(f"{verse_num}. {verse_text}")
        i += 2
    return verse_lines

total = sum(b[2] for b in books)
done = 0
errors = []

for (folder, book_name, num_chapters) in books:
    print(f"\n📖 {book_name}")
    for ch in range(1, num_chapters + 1):
        out_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - ESV.txt")
        query = urllib.parse.quote(f"{book_name} {ch}")
        url = (
            f"https://api.esv.org/v3/passage/text/"
            f"?q={query}"
            f"&include-verse-numbers=true"
            f"&include-headings=false"
            f"&include-footnotes=false"
            f"&include-passage-references=false"
            f"&include-short-copyright=false"
            f"&indent-paragraphs=0"
            f"&indent-poetry=false"
        )
        try:
            for attempt in range(4):
                try:
                    req = urllib.request.Request(url, headers={"Authorization": f"Token {ESV_TOKEN}"})
                    with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
                        data = json.loads(resp.read().decode())
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt < 3:
                        wait = 5 * (attempt + 1)
                        print(f"  ⏳ Rate limited, waiting {wait}s...")
                        time.sleep(wait)
                    else:
                        raise

            raw = data.get("passages", [""])[0]
            verse_lines = parse_esv_raw(raw, book_name, ch)

            content = (
                f"{book_name} - Chapter {ch}\n"
                f"Translation: English Standard Version (ESV)\n"
                f"{'=' * 40}\n\n"
                + "\n".join(verse_lines) + "\n"
            )
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            done += 1
            print(f"  ✓ Ch {ch}/{num_chapters}  [{done}/{total}]")
        except Exception as e:
            errors.append((folder, ch, str(e)))
            print(f"  ✗ Ch {ch} ERROR: {e}")
        time.sleep(0.8)

print(f"\n✅ Done! {done}/{total} ESV files reformatted.")
if errors:
    print(f"⚠️  {len(errors)} errors:")
    for e in errors:
        print(f"   {e}")
