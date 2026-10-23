#!/usr/bin/env python3
"""Find Bible Brain (Faith Comes By Hearing) audio for each translation on the
site, so the BIBLE_BRAIN table in supabase/functions/bible-audio/handler.ts
can be confirmed or filled in.

A recording is only useful when it is the same translation as the text on the
page; the KJV read aloud under the KJV text, never some other English Bible.
So this lists candidates and lets a person choose. It writes nothing.

    BIBLE_BRAIN_KEY=... python3 find_bible_brain_audio.py          # every translation
    BIBLE_BRAIN_KEY=... python3 find_bible_brain_audio.py FRA KJV  # just these

For each site translation it prints:
  - the Bible Brain ID handler.ts maps it to (if any), with that Bible's name,
    language, and MP3 audio filesets (non-drama marked), or why it is wrong;
  - every other Bible in that language that has audio, with its name, so a
    missing match can be spotted and added.

The key is read from the environment only. Never commit it.
"""
import os
import re
import sys
import urllib.parse

import automation_http

API = "https://4.dbt.io/api"
HANDLER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "supabase", "functions", "bible-audio", "handler.ts")

# Site code -> (Bible Brain language iso, the edition shown on the page).
# Names follow docs/site/translations.js and the six English Bibles on every chapter page.
SITE = {
    "ESV": ("eng", "English Standard Version (played from the ESV API, not Bible Brain)"),
    "BSB": ("eng", "Berean Standard Bible"), "KJV": ("eng", "King James Version"),
    "ASV": ("eng", "American Standard Version (1901)"), "NET": ("eng", "New English Translation"),
    "WEB": ("eng", "World English Bible"),
    "HAU": ("hau", "Sabon Rai Don Kowa (Biblica)"), "YOR": ("yor", "Yorùbá Òde-Òní (Biblica)"),
    "IBO": ("ibo", "Igbo Ndị Ugbu a (Biblica)"), "SWA": ("swh", "Neno: Bibilia Takatifu (Biblica)"),
    "TWI": ("twi", "Akuapem Twi Nkwa Asɛm (Biblica)"), "TWA": ("twi", "Asante Twi Nkwa Asɛm (Biblica)"),
    "URD": ("urd", "Urdu Geo Version"), "HIN": ("hin", "Indian Revised Version Hindi"),
    "BEN": ("ben", "Indian Revised Version Bengali"), "TAM": ("tam", "Indian Revised Version Tamil"),
    "TEL": ("tel", "Indian Revised Version Telugu"), "MAL": ("mal", "Indian Revised Version Malayalam"),
    "MAR": ("mar", "Indian Revised Version Marathi"), "GUJ": ("guj", "Indian Revised Version Gujarati"),
    "KAN": ("kan", "Indian Revised Version Kannada"), "ORI": ("ory", "Indian Revised Version Odia"),
    "ASM": ("asm", "Indian Revised Version Assamese"), "PAN": ("pan", "Indian Revised Version Punjabi"),
    "NEP": ("npi", "Nepali Unlocked Literal Bible"), "RV09": ("spa", "Reina-Valera 1909"),
    "FRA": ("fra", "Louis Segond 1910"), "POR": ("por", "Bíblia Livre"), "ARA": ("arb", "Van Dyck"),
    "FAS": ("pes", "Old Persian Version"), "ZHS": ("cmn", "Chinese Union Version (simplified)"),
    "ZHT": ("cmn", "Chinese Union Version (traditional)"), "VIE": ("vie", "Kinh Thánh 1934"),
    "TGL": ("tgl", "Tagalog Unlocked Literal Bible"), "HAT": ("hat", "Bib La"),
}


def mapped():
    """The site code -> Bible Brain ID table currently in handler.ts."""
    text = open(HANDLER, encoding="utf-8").read()
    block = re.search(r"BIBLE_BRAIN[^{]*=\s*{(.*?)\n};", text, re.S).group(1)
    return {m.group(1): m.group(2) for m in re.finditer(r'(\w+):\s*{\s*bible:\s*"(\w+)"', block)}


def call(key, path, **params):
    qs = urllib.parse.urlencode({"v": "4", "key": key, **params})
    status, data = automation_http.get_json(f"{API}{path}?{qs}")
    return status, data


def audio_filesets(bible):
    out = []
    for group in (bible.get("filesets") or {}).values():
        for fs in group or []:
            if fs.get("type") in ("audio", "audio_drama"):
                out.append(fs)
    return out


def describe(fs):
    kind = "non-drama" if fs.get("type") == "audio" else "drama"
    codec = "opus" if "-" in fs.get("id", "") else "mp3"
    return f'{fs.get("id")} ({kind}, {fs.get("size")}, {codec})'


def main():
    key = os.environ.get("BIBLE_BRAIN_KEY")
    if not key:
        sys.exit("Set BIBLE_BRAIN_KEY in the environment first.")
    wanted = [a.upper() for a in sys.argv[1:]] or list(SITE)
    table = mapped()
    by_lang = {}

    for code in wanted:
        if code not in SITE:
            print(f"{code}: not a site translation code"); continue
        iso, edition = SITE[code]
        print(f"\n== {code}  {edition}  [{iso}]")
        if code in table:
            status, data = call(key, f"/bibles/{table[code]}")
            bible = (data or {}).get("data") or {}
            if status != 200 or not bible:
                print(f"   handler.ts: {table[code]}  NOT FOUND (HTTP {status}) -> remove or correct it")
            else:
                fss = audio_filesets(bible)
                lang_ok = bible.get("iso") == iso
                print(f'   handler.ts: {table[code]}  "{bible.get("name")}"  iso={bible.get("iso")}'
                      + ("" if lang_ok else f"  WRONG LANGUAGE (expected {iso})"))
                print("      audio: " + (", ".join(describe(f) for f in fss) or "NONE -> remove it"))
        else:
            print("   handler.ts: no entry (plays the device voice)")

        if iso not in by_lang:
            found, page = [], 1
            while page <= 10:
                status, data = call(key, "/bibles", language_code=iso, media="audio", page=page, limit=50)
                rows = (data or {}).get("data") or []
                found += rows
                last = (((data or {}).get("meta") or {}).get("pagination") or {}).get("total_pages", 1)
                if not rows or page >= last:
                    break
                page += 1
            by_lang[iso] = found
        others = [b for b in by_lang[iso] if b.get("abbr") != table.get(code)]
        for b in others:
            print(f'   candidate: {b.get("abbr")}  "{b.get("name")}"  {b.get("date") or ""}'.rstrip())
        if not others and code not in table:
            print("   no Bible with audio in this language")
    print("\nOnly map a code to a Bible that is the same edition as the page text.")


if __name__ == "__main__":
    main()
