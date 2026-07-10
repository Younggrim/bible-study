#!/usr/bin/env python3
import urllib.request
import urllib.parse
import urllib.error
import ssl
import json
import os
import time
import re

BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study"

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

books = [
    # Old Testament
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
    # New Testament
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

# Translation definitions: (label, filename_tag, fetch_function_name)
translations = [
    ("World English Bible (WEB)",        "WEB", "web"),
    ("American Standard Version (ASV)",  "ASV", "asv"),
    ("NET Bible (NET)",                  "NET", "net"),
]

def fetch_bible_api(book_id, ch, translation_id):
    """Fetch from bible-api.com (WEB, ASV)"""
    url = f"https://bible-api.com/data/{translation_id}/{book_id}/{ch}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
        data = json.loads(resp.read().decode())
    verses = data.get("verses", [])
    lines = []
    for v in verses:
        clean = " ".join(v['text'].split())
        lines.append(f"{v['verse']}. {clean}")
    return "\n".join(lines)

def fetch_net(book_name, ch):
    """Fetch from labs.bible.org (NET Bible)"""
    passage = urllib.parse.quote(f"{book_name} {ch}")
    url = f"https://labs.bible.org/api/?passage={passage}&type=json"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
        data = json.loads(resp.read().decode())
    lines = []
    for v in data:
        # Strip any HTML tags from NET text
        text = re.sub(r'<[^>]+>', '', v['text']).strip()
        text = " ".join(text.split())
        lines.append(f"{v['verse']}. {text}")
    return "\n".join(lines)

def fetch_with_retry(fetch_fn, *args):
    for attempt in range(4):
        try:
            return fetch_fn(*args)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                wait = 5 * (attempt + 1)
                print(f"  ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
        except Exception:
            if attempt < 3:
                time.sleep(3)
            else:
                raise

total_chapters = sum(b[3] for b in books)
total_files = total_chapters * len(translations)
done = 0
errors = []

full_names = {
    "WEB": "World English Bible (WEB)",
    "ASV": "American Standard Version (ASV)",
    "NET": "NET Bible (NET)",
}

for (folder, book_name, book_id, num_chapters) in books:
    print(f"\n📖 {book_name} ({num_chapters} chapters)")
    for ch in range(1, num_chapters + 1):
        for (full_label, tag, api_id) in translations:
            out_path = os.path.join(BASE, folder, f"Chapter {ch}", f"Chapter {ch} - {tag}.txt")
            if os.path.exists(out_path):
                done += 1
                continue
            try:
                if tag == "NET":
                    text = fetch_with_retry(fetch_net, book_name, ch)
                else:
                    text = fetch_with_retry(fetch_bible_api, book_id, ch, api_id.lower())

                content = (
                    f"{book_name} - Chapter {ch}\n"
                    f"Translation: {full_label}\n"
                    f"{'=' * 40}\n\n"
                    f"{text}\n"
                )
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content)
                done += 1
                print(f"  ✓ Ch {ch} {tag}  [{done}/{total_files}]")
            except Exception as e:
                errors.append((folder, ch, tag, str(e)))
                print(f"  ✗ Ch {ch} {tag} ERROR: {e}")

            time.sleep(0.5)

print(f"\n\n✅ Complete! {done}/{total_files} files saved.")
if errors:
    print(f"⚠️  {len(errors)} errors:")
    for e in errors:
        print(f"   {e}")
