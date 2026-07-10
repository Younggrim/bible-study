#!/usr/bin/env python3
"""Fetch only the missing KJV and ESV chapters with aggressive backoff."""
import urllib.request
import urllib.parse
import urllib.error
import ssl
import json
import os
import time
import re

BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study"
ESV_TOKEN = "c577a41c8607e92598297705b575bd6ebdac76ab"

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

books = [
    ("Old Testament/01 - Genesis",        "Genesis",          "GEN", 50),
    ("Old Testament/02 - Exodus",         "Exodus",           "EXO", 40),
    ("Old Testament/03 - Leviticus",      "Leviticus",        "LEV", 27),
    ("Old Testament/04 - Numbers",        "Numbers",          "NUM", 36),
    ("Old Testament/05 - Deuteronomy",    "Deuteronomy",      "DEU", 34),
    ("Old Testament/06 - Joshua",         "Joshua",           "JOS", 24),
    ("Old Testament/07 - Judges",         "Judges",           "JDG", 21),
    ("Old Testament/08 - Ruth",           "Ruth",             "RUT",  4),
    ("Old Testament/09 - 1 Samuel",       "1 Samuel",         "1SA", 31),
    ("Old Testament/10 - 2 Samuel",       "2 Samuel",         "2SA", 24),
    ("Old Testament/11 - 1 Kings",        "1 Kings",          "1KI", 22),
    ("Old Testament/12 - 2 Kings",        "2 Kings",          "2KI", 25),
    ("Old Testament/13 - 1 Chronicles",   "1 Chronicles",     "1CH", 29),
    ("Old Testament/14 - 2 Chronicles",   "2 Chronicles",     "2CH", 36),
    ("Old Testament/15 - Ezra",           "Ezra",             "EZR", 10),
    ("Old Testament/16 - Nehemiah",       "Nehemiah",         "NEH", 13),
    ("Old Testament/17 - Esther",         "Esther",           "EST", 10),
    ("Old Testament/18 - Job",            "Job",              "JOB", 42),
    ("Old Testament/19 - Psalms",         "Psalms",           "PSA",150),
    ("Old Testament/20 - Proverbs",       "Proverbs",         "PRO", 31),
    ("Old Testament/21 - Ecclesiastes",   "Ecclesiastes",     "ECC", 12),
    ("Old Testament/22 - Song of Solomon","Song of Solomon",  "SNG",  8),
    ("Old Testament/23 - Isaiah",         "Isaiah",           "ISA", 66),
    ("Old Testament/24 - Jeremiah",       "Jeremiah",         "JER", 52),
    ("Old Testament/25 - Lamentations",   "Lamentations",     "LAM",  5),
    ("Old Testament/26 - Ezekiel",        "Ezekiel",          "EZK", 48),
    ("Old Testament/27 - Daniel",         "Daniel",           "DAN", 12),
    ("Old Testament/28 - Hosea",          "Hosea",            "HOS", 14),
    ("Old Testament/29 - Joel",           "Joel",             "JOL",  3),
    ("Old Testament/30 - Amos",           "Amos",             "AMO",  9),
    ("Old Testament/31 - Obadiah",        "Obadiah",          "OBA",  1),
    ("Old Testament/32 - Jonah",          "Jonah",            "JON",  4),
    ("Old Testament/33 - Micah",          "Micah",            "MIC",  7),
    ("Old Testament/34 - Nahum",          "Nahum",            "NAM",  3),
    ("Old Testament/35 - Habakkuk",       "Habakkuk",         "HAB",  3),
    ("Old Testament/36 - Zephaniah",      "Zephaniah",        "ZEP",  3),
    ("Old Testament/37 - Haggai",         "Haggai",           "HAG",  2),
    ("Old Testament/38 - Zechariah",      "Zechariah",        "ZEC", 14),
    ("Old Testament/39 - Malachi",        "Malachi",          "MAL",  4),
    ("New Testament/01 - Matthew",        "Matthew",          "MAT", 28),
    ("New Testament/02 - Mark",           "Mark",             "MRK", 16),
    ("New Testament/03 - Luke",           "Luke",             "LUK", 24),
    ("New Testament/04 - John",           "John",             "JHN", 21),
    ("New Testament/05 - Acts",           "Acts",             "ACT", 28),
    ("New Testament/06 - Romans",         "Romans",           "ROM", 16),
    ("New Testament/07 - 1 Corinthians",  "1 Corinthians",    "1CO", 16),
    ("New Testament/08 - 2 Corinthians",  "2 Corinthians",    "2CO", 13),
    ("New Testament/09 - Galatians",      "Galatians",        "GAL",  6),
    ("New Testament/10 - Ephesians",      "Ephesians",        "EPH",  6),
    ("New Testament/11 - Philippians",    "Philippians",      "PHP",  4),
    ("New Testament/12 - Colossians",     "Colossians",       "COL",  4),
    ("New Testament/13 - 1 Thessalonians","1 Thessalonians",  "1TH",  5),
    ("New Testament/14 - 2 Thessalonians","2 Thessalonians",  "2TH",  3),
    ("New Testament/15 - 1 Timothy",      "1 Timothy",        "1TI",  6),
    ("New Testament/16 - 2 Timothy",      "2 Timothy",        "2TI",  4),
    ("New Testament/17 - Titus",          "Titus",            "TIT",  3),
    ("New Testament/18 - Philemon",       "Philemon",         "PHM",  1),
    ("New Testament/19 - Hebrews",        "Hebrews",          "HEB", 13),
    ("New Testament/20 - James",          "James",            "JAS",  5),
    ("New Testament/21 - 1 Peter",        "1 Peter",          "1PE",  5),
    ("New Testament/22 - 2 Peter",        "2 Peter",          "2PE",  3),
    ("New Testament/23 - 1 John",         "1 John",           "1JN",  5),
    ("New Testament/24 - 2 John",         "2 John",           "2JN",  1),
    ("New Testament/25 - 3 John",         "3 John",           "3JN",  1),
    ("New Testament/26 - Jude",           "Jude",             "JUD",  1),
    ("New Testament/27 - Revelation",     "Revelation",       "REV", 22),
]

def fetch_kjv(book_id, ch, book_name):
    url = f"https://bible-api.com/data/kjv/{book_id}/{ch}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=20, context=ssl_ctx) as resp:
        data = json.loads(resp.read().decode())
    verses = data.get("verses", [])
    lines = []
    for v in verses:
        clean = " ".join(v['text'].split())
        lines.append(f"{v['verse']}. {clean}")
    content = (
        f"{book_name} - Chapter {ch}\n"
        f"Translation: King James Version (KJV)\n"
        f"{'=' * 40}\n\n"
        + "\n".join(lines) + "\n"
    )
    return content

def fetch_esv(book_name, ch):
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
    req = urllib.request.Request(url, headers={"Authorization": f"Token {ESV_TOKEN}"})
    with urllib.request.urlopen(req, timeout=20, context=ssl_ctx) as resp:
        data = json.loads(resp.read().decode())
    raw = data.get("passages", [""])[0]
    # Parse [N] markers
    parts = re.split(r'\[(\d+)\]', raw)
    verse_lines = []
    i = 1
    while i < len(parts) - 1:
        verse_num = parts[i].strip()
        verse_text = " ".join(parts[i + 1].split()).strip()
        if verse_text:
            verse_lines.append(f"{verse_num}. {verse_text}")
        i += 2
    content = (
        f"{book_name} - Chapter {ch}\n"
        f"Translation: English Standard Version (ESV)\n"
        f"{'=' * 40}\n\n"
        + "\n".join(verse_lines) + "\n"
    )
    return content

# Find missing files
missing_kjv = []
missing_esv = []

for (folder, book_name, book_id, num_chapters) in books:
    for ch in range(1, num_chapters + 1):
        kjv_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - KJV.txt")
        esv_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - ESV.txt")
        if not os.path.exists(kjv_path):
            missing_kjv.append((folder, book_name, book_id, ch))
        if not os.path.exists(esv_path):
            missing_esv.append((folder, book_name, book_id, ch))

print(f"Missing KJV: {len(missing_kjv)} chapters")
print(f"Missing ESV: {len(missing_esv)} chapters")
print()

# Fetch missing KJV with long delays
if missing_kjv:
    print("=== Fetching missing KJV chapters ===")
    for i, (folder, book_name, book_id, ch) in enumerate(missing_kjv):
        out_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - KJV.txt")
        for attempt in range(6):
            try:
                content = fetch_kjv(book_id, ch, book_name)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✓ KJV {book_name} Ch {ch}  [{i+1}/{len(missing_kjv)}]")
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = 30 * (attempt + 1)
                    print(f"  ⏳ Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  ✗ KJV {book_name} Ch {ch} ERROR: {e}")
                    break
            except Exception as e:
                print(f"  ✗ KJV {book_name} Ch {ch} ERROR: {e}")
                break
        time.sleep(5)  # 5 seconds between successful requests

# Fetch missing ESV with long delays
if missing_esv:
    print("\n=== Fetching missing ESV chapters ===")
    for i, (folder, book_name, book_id, ch) in enumerate(missing_esv):
        out_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - ESV.txt")
        for attempt in range(6):
            try:
                content = fetch_esv(book_name, ch)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✓ ESV {book_name} Ch {ch}  [{i+1}/{len(missing_esv)}]")
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = 30 * (attempt + 1)
                    print(f"  ⏳ Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  ✗ ESV {book_name} Ch {ch} ERROR: {e}")
                    break
            except Exception as e:
                print(f"  ✗ ESV {book_name} Ch {ch} ERROR: {e}")
                break
        time.sleep(5)  # 5 seconds between successful requests

print("\n✅ Done!")
