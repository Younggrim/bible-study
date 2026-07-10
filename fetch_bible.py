#!/usr/bin/env python3
import urllib.request
import urllib.error
import ssl
import json
import os
import time

# Fix macOS SSL certificate verification issue
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study"

# Each book: (folder name, API book ID, chapter count)
books = [
    # Old Testament
    ("Old Testament/01 - Genesis",        "GEN", 50),
    ("Old Testament/02 - Exodus",         "EXO", 40),
    ("Old Testament/03 - Leviticus",      "LEV", 27),
    ("Old Testament/04 - Numbers",        "NUM", 36),
    ("Old Testament/05 - Deuteronomy",    "DEU", 34),
    ("Old Testament/06 - Joshua",         "JOS", 24),
    ("Old Testament/07 - Judges",         "JDG", 21),
    ("Old Testament/08 - Ruth",           "RUT",  4),
    ("Old Testament/09 - 1 Samuel",       "1SA", 31),
    ("Old Testament/10 - 2 Samuel",       "2SA", 24),
    ("Old Testament/11 - 1 Kings",        "1KI", 22),
    ("Old Testament/12 - 2 Kings",        "2KI", 25),
    ("Old Testament/13 - 1 Chronicles",   "1CH", 29),
    ("Old Testament/14 - 2 Chronicles",   "2CH", 36),
    ("Old Testament/15 - Ezra",           "EZR", 10),
    ("Old Testament/16 - Nehemiah",       "NEH", 13),
    ("Old Testament/17 - Esther",         "EST", 10),
    ("Old Testament/18 - Job",            "JOB", 42),
    ("Old Testament/19 - Psalms",         "PSA",150),
    ("Old Testament/20 - Proverbs",       "PRO", 31),
    ("Old Testament/21 - Ecclesiastes",   "ECC", 12),
    ("Old Testament/22 - Song of Solomon","SNG",  8),
    ("Old Testament/23 - Isaiah",         "ISA", 66),
    ("Old Testament/24 - Jeremiah",       "JER", 52),
    ("Old Testament/25 - Lamentations",   "LAM",  5),
    ("Old Testament/26 - Ezekiel",        "EZK", 48),
    ("Old Testament/27 - Daniel",         "DAN", 12),
    ("Old Testament/28 - Hosea",          "HOS", 14),
    ("Old Testament/29 - Joel",           "JOL",  3),
    ("Old Testament/30 - Amos",           "AMO",  9),
    ("Old Testament/31 - Obadiah",        "OBA",  1),
    ("Old Testament/32 - Jonah",          "JON",  4),
    ("Old Testament/33 - Micah",          "MIC",  7),
    ("Old Testament/34 - Nahum",          "NAM",  3),
    ("Old Testament/35 - Habakkuk",       "HAB",  3),
    ("Old Testament/36 - Zephaniah",      "ZEP",  3),
    ("Old Testament/37 - Haggai",         "HAG",  2),
    ("Old Testament/38 - Zechariah",      "ZEC", 14),
    ("Old Testament/39 - Malachi",        "MAL",  4),
    # New Testament
    ("New Testament/01 - Matthew",        "MAT", 28),
    ("New Testament/02 - Mark",           "MRK", 16),
    ("New Testament/03 - Luke",           "LUK", 24),
    ("New Testament/04 - John",           "JHN", 21),
    ("New Testament/05 - Acts",           "ACT", 28),
    ("New Testament/06 - Romans",         "ROM", 16),
    ("New Testament/07 - 1 Corinthians",  "1CO", 16),
    ("New Testament/08 - 2 Corinthians",  "2CO", 13),
    ("New Testament/09 - Galatians",      "GAL",  6),
    ("New Testament/10 - Ephesians",      "EPH",  6),
    ("New Testament/11 - Philippians",    "PHP",  4),
    ("New Testament/12 - Colossians",     "COL",  4),
    ("New Testament/13 - 1 Thessalonians","1TH",  5),
    ("New Testament/14 - 2 Thessalonians","2TH",  3),
    ("New Testament/15 - 1 Timothy",      "1TI",  6),
    ("New Testament/16 - 2 Timothy",      "2TI",  4),
    ("New Testament/17 - Titus",          "TIT",  3),
    ("New Testament/18 - Philemon",       "PHM",  1),
    ("New Testament/19 - Hebrews",        "HEB", 13),
    ("New Testament/20 - James",          "JAS",  5),
    ("New Testament/21 - 1 Peter",        "1PE",  5),
    ("New Testament/22 - 2 Peter",        "2PE",  3),
    ("New Testament/23 - 1 John",         "1JN",  5),
    ("New Testament/24 - 2 John",         "2JN",  1),
    ("New Testament/25 - 3 John",         "3JN",  1),
    ("New Testament/26 - Jude",           "JUD",  1),
    ("New Testament/27 - Revelation",     "REV", 22),
]

total_chapters = sum(b[2] for b in books)
done = 0
errors = []

for (folder, book_id, num_chapters) in books:
    book_name = folder.split(" - ", 1)[1]
    print(f"\n📖 {book_name} ({num_chapters} chapters)")
    for ch in range(1, num_chapters + 1):
        out_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - KJV.txt")
        # Skip if already done
        if os.path.exists(out_path):
            done += 1
            continue
        url = f"https://bible-api.com/data/kjv/{book_id}/{ch}"
        try:
            retries = 3
            data = None
            for attempt in range(retries):
                try:
                    with urllib.request.urlopen(url, timeout=15, context=ssl_ctx) as resp:
                        data = json.loads(resp.read().decode())
                    break
                except urllib.error.HTTPError as he:
                    if he.code == 429 and attempt < retries - 1:
                        wait = 5 * (attempt + 1)
                        print(f"  ⏳ Rate limited, waiting {wait}s...")
                        time.sleep(wait)
                    else:
                        raise
            if data is None:
                raise Exception("No data after retries")
            verses = data.get("verses", [])
            lines = [
                f"{book_name} - Chapter {ch}\n",
                f"Translation: King James Version (KJV)\n",
                f"{'=' * 40}\n\n",
            ]
            for v in verses:
                # Clean up mid-sentence line breaks from the API
                clean_text = " ".join(v['text'].split())
                lines.append(f"{v['verse']}. {clean_text}\n")
            with open(out_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            done += 1
            print(f"  ✓ Chapter {ch}/{num_chapters}  [{done}/{total_chapters}]")
        except Exception as e:
            errors.append((folder, ch, str(e)))
            print(f"  ✗ Chapter {ch} ERROR: {e}")
        time.sleep(0.8)  # respect rate limits

print(f"\n\n✅ Complete! {done}/{total_chapters} chapters saved.")
if errors:
    print(f"⚠️  {len(errors)} errors:")
    for e in errors:
        print(f"   {e}")
