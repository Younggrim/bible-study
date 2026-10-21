#!/usr/bin/env python3
"""Build docs/bible/<CODE>/<page>.json, the other-language Bibles that
docs/site/translations.js loads when a reader picks one.

Source: the USFM zips eBible.org publishes, https://ebible.org/Scriptures/<id>_usfm.zip

    code  eBible id   translation                                   licence
    RV09  spaRV1909   Santa Biblia Reina-Valera 1909                 public domain
    HAU   hausa       Biblica Open Hausa Contemporary Bible          CC BY-SA 4.0
    YOR   yor         Biblica Open Yoruba Contemporary Bible         CC BY-SA 4.0
    IBO   ibo         Biblica Open Igbo Contemporary Bible           CC BY-SA 4.0
    URD   urdgvu      Urdu Geo Version (Urdu script)                 CC BY-NC-ND 4.0
    HIN   hin2017     Indian Revised Version (IRV) Hindi 2019        CC BY-SA 4.0

The verse text is kept exactly as published. Footnotes, cross references,
section headings and introductions are left out; a psalm's title (\\d) is
kept and shown above its first verse. Each translation's credit line lives in
translations.js and is shown under every chapter, as the licences require.
URD is "no derivatives": its words are never altered, only displayed.

    python3 build_bibles.py <dir with the *_usfm.zip files>           # write
    python3 build_bibles.py <dir> --check                            # report only

Reports, per translation, any chapter whose verse count differs from the
site's BSB text, since that is how a numbering difference or a damaged
download shows up. Writes nothing for a translation missing any of the
1189 chapters.
"""
import glob
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "bible")

SOURCES = [("RV09", "spaRV1909"), ("HAU", "hausa"), ("YOR", "yor"),
           ("IBO", "ibo"), ("URD", "urdgvu"), ("HIN", "hin2017"),
           # India: Indian Revised Version, CC BY-SA 4.0
           ("BEN", "benirv"), ("TAM", "tam2017"), ("TEL", "tel2017"), ("MAL", "mal"),
           ("MAR", "mar"), ("GUJ", "guj2017"), ("KAN", "kanirv"), ("ORI", "ory"),
           ("ASM", "asmfb"), ("PAN", "pan"),
           ("NEP", "npiulb"),                                   # Unlocked Literal Bible, CC BY-SA 4.0
           # Africa
           ("SWA", "swhonen"), ("TWI", "twi"), ("TWA", "twiasante"),   # Biblica Open, CC BY-SA 4.0
           # world
           ("ARA", "arb-vd"), ("FRA", "fraLSG"), ("ZHS", "cmn-cu89s"), ("ZHT", "cmn-cu89t"),
           ("FAS", "pesOPV"), ("VIE", "vie1934"), ("HAT", "hat"),   # public domain
           # not used: russyn (Russian Synodal) numbers the Psalms the Greek way, so its Psalm 23 is our 24;
           #           ind (Indonesian) is New Testament plus part of the Old
           ("POR", "porbr2018"),                                # Biblia Livre, CC BY 4.0
           ("TGL", "tglulb")]                                   # Unlocked Literal Bible, CC BY-SA 4.0

BOOKS = [("GEN", "genesis"), ("EXO", "exodus"), ("LEV", "leviticus"), ("NUM", "numbers"), ("DEU", "deuteronomy"),
         ("JOS", "joshua"), ("JDG", "judges"), ("RUT", "ruth"), ("1SA", "1samuel"), ("2SA", "2samuel"),
         ("1KI", "1kings"), ("2KI", "2kings"), ("1CH", "1chronicles"), ("2CH", "2chronicles"), ("EZR", "ezra"),
         ("NEH", "nehemiah"), ("EST", "esther"), ("JOB", "job"), ("PSA", "psalms"), ("PRO", "proverbs"),
         ("ECC", "ecclesiastes"), ("SNG", "songofsolomon"), ("ISA", "isaiah"), ("JER", "jeremiah"),
         ("LAM", "lamentations"), ("EZK", "ezekiel"), ("DAN", "daniel"), ("HOS", "hosea"), ("JOL", "joel"),
         ("AMO", "amos"), ("OBA", "obadiah"), ("JON", "jonah"), ("MIC", "micah"), ("NAM", "nahum"),
         ("HAB", "habakkuk"), ("ZEP", "zephaniah"), ("HAG", "haggai"), ("ZEC", "zechariah"), ("MAL", "malachi"),
         ("MAT", "matthew"), ("MRK", "mark"), ("LUK", "luke"), ("JHN", "john"), ("ACT", "acts"), ("ROM", "romans"),
         ("1CO", "1corinthians"), ("2CO", "2corinthians"), ("GAL", "galatians"), ("EPH", "ephesians"),
         ("PHP", "philippians"), ("COL", "colossians"), ("1TH", "1thessalonians"), ("2TH", "2thessalonians"),
         ("1TI", "1timothy"), ("2TI", "2timothy"), ("TIT", "titus"), ("PHM", "philemon"), ("HEB", "hebrews"),
         ("JAS", "james"), ("1PE", "1peter"), ("2PE", "2peter"), ("1JN", "1john"), ("2JN", "2john"),
         ("3JN", "3john"), ("JUD", "jude"), ("REV", "revelation")]
SLUG = dict(BOOKS)

# Paragraph-level markers whose content is not verse text.
SKIP = re.compile(r"^(id|ide|usfm|h|toc\d*|toca\d*|mt\d*|mte\d*|ms\d*|mr|s\d*|sr|r|rem|sts|cl|cd|"
                  r"imt\d*|imte\d*|ip|ipi|ipq|ipr|iq\d*|im|imi|ili\d*|is\d*|io\d*|ior|iot|iex|ie|ib|"
                  r"sp|qa|lit|periph|cp|ca|va|vp|restore)$")
# Paragraph-level markers that continue verse text (poetry lines, paragraphs, lists, tables).
PARA = re.compile(r"^(p|m|po|pr|cls|pmo|pm|pmc|pmr|pi\d*|mi|nb|pc|ph\d*|b|q\d*|qr|qc|qm\d*|qd|"
                  r"li\d*|lh|lf|lim\d*|tr|th\d*|thr\d*|tc\d*|tcr\d*|pb)$")
NOTES = re.compile(r"\\(f|fe|ef|x|ex)\s.*?\\\1\*", re.S)
FIG = re.compile(r"\\fig\s.*?\\fig\*", re.S)
ATTRS = re.compile(r"\|[^\\|]*(?=\\\+?[a-z][a-z0-9]*\*)")      # \w word|strong="H1234"\w*
TOKEN = re.compile(r"\\\+?([a-z][a-z0-9]*)(\*?)")
SPACE = re.compile(r"\s+")


def parse_book(text):
    """Return {chapter: [[verse, text, label|None, title|None], ...]} for one USFM book."""
    text = NOTES.sub("", text)
    text = FIG.sub("", text)
    text = ATTRS.sub("", text)
    chapters, ch, rows, mode, title = {}, None, None, "skip", []
    pos, cur = 0, None   # cur: the verse row being filled

    def emit(s):
        nonlocal cur
        if mode == "verse" and cur is not None:
            cur[1] += s
        elif mode == "title":
            title.append(s)

    for m in TOKEN.finditer(text):
        emit(text[pos:m.start()])
        pos = m.end()
        name, closing = m.group(1), m.group(2)
        if closing:
            continue                                   # end of a character style: keep its text
        if name not in ("c", "v") and pos < len(text) and text[pos] in " \t":
            pos += 1                                   # the one space after an opening marker belongs to the marker
        if name == "c":
            mm = re.match(r"\s*(\d+)", text[pos:])
            ch = int(mm.group(1)); pos += mm.end()
            rows = chapters.setdefault(ch, [])
            cur, mode, title = None, "skip", []
        elif name == "v":
            mm = re.match(r"\s*(\d+)[a-z]?(?:[\s\u200e\u200f]*[-\u2013][\s\u200e\u200f]*(\d+)[a-z]?)?[\s\u200e\u200f]?", text[pos:])
            pos += mm.end()
            v1, v2 = int(mm.group(1)), mm.group(2)
            cur = [v1, "", f"{v1}\u2013{v2}" if v2 and int(v2) != v1 else None,
                   " ".join(SPACE.sub(" ", "".join(title)).split()) or None]
            title = []
            rows.append(cur)
            mode = "verse"
        elif name == "d":
            mode, title = "title", []
        elif SKIP.match(name):
            mode = "skip"
        elif PARA.match(name):
            if cur is not None and ch is not None:
                mode = "verse"; cur[1] += " "
        # anything else is a character style (wj, add, nd, w, k, sc, qs, bk, ...): keep its text
    emit(text[pos:])
    for rows in chapters.values():
        for r in rows:
            r[1] = SPACE.sub(" ", r[1]).strip()
    return chapters


# Spacing left by word-by-word markup (\w ... \w*) in two editions. Spaces only; never words.
FIXUPS = {
    "FRA": [(re.compile(r"(\w[’'])\s+(?=\w)"), r"\1")],          # qu’ il -> qu’il
    "RV09": [(re.compile(r"([¡¿])\s+"), r"\1")],                   # ¡ OH -> ¡OH
}


def load_zip(path):
    books = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not n.lower().endswith((".usfm", ".sfm")):
                continue
            t = z.read(n).decode("utf-8-sig")
            m = re.search(r"\\id\s+([A-Z0-9]{3})", t)
            if m and m.group(1) in SLUG:
                books[m.group(1)] = parse_book(t)
    return books


def site_counts():
    """Verse count of the BSB text on every chapter page, the reference numbering."""
    counts = {}
    for path in glob.glob(os.path.join(DOCS, "*.html")):
        name = os.path.basename(path)[:-5]
        t = open(path, encoding="utf-8").read()
        m = re.search(r'data-translation="BSB">(.*?)</div>', t, re.S)
        if m:
            counts[name] = len(re.findall(r'<p class="verse"', m.group(1)))
    return counts


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src, check = sys.argv[1], "--check" in sys.argv
    ref = site_counts()
    bad = 0
    for code, eid in SOURCES:
        zp = os.path.join(src, f"{eid}_usfm.zip")
        if not os.path.exists(zp):
            print(f"{code}: MISSING {zp}"); bad += 1; continue
        books = load_zip(zp)
        pages, diffs, empty = {}, [], 0
        for usfm, slug in BOOKS:
            for ch, rows in sorted(books.get(usfm, {}).items()):
                page = f"{slug}{ch}"
                if page not in ref:
                    diffs.append(f"{page} (no such page)"); continue
                empty += sum(1 for r in rows if not r[1])
                for rx, rep in FIXUPS.get(code, []):
                    for r in rows:
                        r[1] = rx.sub(rep, r[1])
                rows = [[r[0], r[1]] + ([r[2]] if r[2] or r[3] else []) + ([r[3]] if r[3] else []) for r in rows if r[1]]
                pages[page] = rows
                covered = sum((int(r[2].split("\u2013")[1]) - r[0] + 1) if len(r) > 2 and r[2] else 1 for r in rows)
                if covered != ref[page]:
                    diffs.append(f"{page} {covered}/{ref[page]}")
        missing = sorted(set(ref) - set(pages))
        print(f"{code}: {len(pages)} chapters, {sum(len(v) for v in pages.values())} verses, "
              f"{empty} empty verses, {len(missing)} missing chapters, {len(diffs)} chapters numbered differently from BSB")
        if missing:
            print("   missing:", " ".join(missing[:20]), "..." if len(missing) > 20 else "")
            bad += 1
            continue
        if diffs:
            print("   differ:", " ".join(diffs[:40]), "..." if len(diffs) > 40 else "")
        if not check:
            d = os.path.join(OUT, code)
            os.makedirs(d, exist_ok=True)
            for page, rows in pages.items():
                with open(os.path.join(d, page + ".json"), "w", encoding="utf-8") as f:
                    json.dump({"v": rows}, f, ensure_ascii=False, separators=(",", ":"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
