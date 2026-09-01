#!/usr/bin/env python3
"""
Fills in the Commentary tab: adds NET translator notes and Matthew Henry
alongside Enduring Word, and gives the 217 chapters that had no Commentary tab
at all one of their own.

Why those 217 were empty: they are Psalms (150) and the twelve Minor Prophets
(67). Enduring Word's URL for the Psalms uses the singular, /psalm-23/, and
whoever generated the links used the plural, so every Psalm 404'd and the book
was skipped. The Minor Prophets appear to have been missed in the same pass.
All 66 books were re-checked against both sites before this ran; every slug and
every book code returns 200.

What gets added, and why these three:

  Enduring Word      David Guzik, already the site's commentary. Existing
                     hand-written per-chapter descriptions are preserved
                     verbatim; only missing entries get a generated one.
  NET notes          The single richest freely usable commentary resource, and
                     the site already ships NET as a translation, so it is
                     already within that licence. 60,000+ notes.
  Matthew Henry      Public domain, 1710, devotional and verse-by-verse. Served
                     via Blue Letter Bible, which has a stable URL pattern.

Nothing is copied from any of these. Each entry is a link, exactly as the
Enduring Word entry always was.

Usage:
    python3 add_commentaries.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^([a-z0-9]+?)(\d+)\.html$")

# site slug -> (Enduring Word slug, Blue Letter Bible code, NET book name)
BOOKS = {
    "genesis": ("genesis", "Gen", "Genesis"),
    "exodus": ("exodus", "Exd", "Exodus"),
    "leviticus": ("leviticus", "Lev", "Leviticus"),
    "numbers": ("numbers", "Num", "Numbers"),
    "deuteronomy": ("deuteronomy", "Deu", "Deuteronomy"),
    "joshua": ("joshua", "Jos", "Joshua"),
    "judges": ("judges", "Jdg", "Judges"),
    "ruth": ("ruth", "Rth", "Ruth"),
    "1samuel": ("1-samuel", "1Sa", "1 Samuel"),
    "2samuel": ("2-samuel", "2Sa", "2 Samuel"),
    "1kings": ("1-kings", "1Ki", "1 Kings"),
    "2kings": ("2-kings", "2Ki", "2 Kings"),
    "1chronicles": ("1-chronicles", "1Ch", "1 Chronicles"),
    "2chronicles": ("2-chronicles", "2Ch", "2 Chronicles"),
    "ezra": ("ezra", "Ezr", "Ezra"),
    "nehemiah": ("nehemiah", "Neh", "Nehemiah"),
    "esther": ("esther", "Est", "Esther"),
    "job": ("job", "Job", "Job"),
    "psalms": ("psalm", "Psa", "Psalm"),
    "proverbs": ("proverbs", "Pro", "Proverbs"),
    "ecclesiastes": ("ecclesiastes", "Ecc", "Ecclesiastes"),
    "songofsolomon": ("song-of-solomon", "Sng", "Song of Solomon"),
    "isaiah": ("isaiah", "Isa", "Isaiah"),
    "jeremiah": ("jeremiah", "Jer", "Jeremiah"),
    "lamentations": ("lamentations", "Lam", "Lamentations"),
    "ezekiel": ("ezekiel", "Eze", "Ezekiel"),
    "daniel": ("daniel", "Dan", "Daniel"),
    "hosea": ("hosea", "Hos", "Hosea"),
    "joel": ("joel", "Jol", "Joel"),
    "amos": ("amos", "Amo", "Amos"),
    "obadiah": ("obadiah", "Oba", "Obadiah"),
    "jonah": ("jonah", "Jon", "Jonah"),
    "micah": ("micah", "Mic", "Micah"),
    "nahum": ("nahum", "Nam", "Nahum"),
    "habakkuk": ("habakkuk", "Hab", "Habakkuk"),
    "zephaniah": ("zephaniah", "Zep", "Zephaniah"),
    "haggai": ("haggai", "Hag", "Haggai"),
    "zechariah": ("zechariah", "Zec", "Zechariah"),
    "malachi": ("malachi", "Mal", "Malachi"),
    "matthew": ("matthew", "Mat", "Matthew"),
    "mark": ("mark", "Mar", "Mark"),
    "luke": ("luke", "Luk", "Luke"),
    "john": ("john", "Jhn", "John"),
    "acts": ("acts", "Act", "Acts"),
    "romans": ("romans", "Rom", "Romans"),
    "1corinthians": ("1-corinthians", "1Co", "1 Corinthians"),
    "2corinthians": ("2-corinthians", "2Co", "2 Corinthians"),
    "galatians": ("galatians", "Gal", "Galatians"),
    "ephesians": ("ephesians", "Eph", "Ephesians"),
    "philippians": ("philippians", "Phl", "Philippians"),
    "colossians": ("colossians", "Col", "Colossians"),
    "1thessalonians": ("1-thessalonians", "1Th", "1 Thessalonians"),
    "2thessalonians": ("2-thessalonians", "2Th", "2 Thessalonians"),
    "1timothy": ("1-timothy", "1Ti", "1 Timothy"),
    "2timothy": ("2-timothy", "2Ti", "2 Timothy"),
    "titus": ("titus", "Tit", "Titus"),
    "philemon": ("philemon", "Phm", "Philemon"),
    "hebrews": ("hebrews", "Hbr", "Hebrews"),
    "james": ("james", "Jam", "James"),
    "1peter": ("1-peter", "1Pe", "1 Peter"),
    "2peter": ("2-peter", "2Pe", "2 Peter"),
    "1john": ("1-john", "1Jo", "1 John"),
    "2john": ("2-john", "2Jo", "2 John"),
    "3john": ("3-john", "3Jo", "3 John"),
    "jude": ("jude", "Jde", "Jude"),
    "revelation": ("revelation", "Rev", "Revelation"),
}

LINK = ('<a href="{url}" target="_blank" '
        'style="color:var(--accent-link);text-decoration:none;'
        'border-bottom:1px dotted var(--accent-link);">{label}</a>')


def guzik_li(slug, ch):
    ew = BOOKS[slug][0]
    url = f"https://enduringword.com/bible-commentary/{ew}-{ch}/"
    link = LINK.format(url=url, label="enduringword.com")
    return (f'<li><strong>Enduring Word (David Guzik):</strong> {link} '
            f"Verse-by-verse commentary on this chapter, written for the "
            f"everyday reader and freely available online.</li>")


def net_li(slug, ch):
    book = BOOKS[slug][2]
    url = f"https://netbible.org/bible/{book.replace(' ', '+')}+{ch}"
    link = LINK.format(url=url, label="netbible.org")
    return (f'<li><strong>NET Bible translator notes:</strong> {link} '
            f"More than 60,000 notes across the Bible explaining textual "
            f"decisions, the underlying Hebrew and Greek, and alternative "
            f"renderings. The NET is one of the five translations on this "
            f"page.</li>")


def henry_li(slug, ch):
    code = BOOKS[slug][1]
    url = (f"https://www.blueletterbible.org/comm/mhc/"
           f"{code}/{code}_{int(ch):03d}.cfm")
    link = LINK.format(url=url, label="blueletterbible.org")
    return (f"<li><strong>Matthew Henry's Exposition (1710):</strong> {link} "
            f"A devotional verse-by-verse commentary in the Puritan tradition, "
            f"still among the most widely read three centuries on. Public "
            f"domain.</li>")


TAB_BUTTON = '<div class="study-tab" data-tab="commentary">Commentary</div>'


def build_tab(items):
    inner = "\n                    ".join(items)
    return ('            <div class="tab-content" id="tab-commentary">\n'
            "                <h3>Commentary</h3>\n"
            "                <ul>\n"
            f"                    {inner}\n"
            "                </ul>\n"
            "            </div>\n")


def main():
    check = "--check" in sys.argv
    pages = []
    for n in sorted(os.listdir(DOCS)):
        m = CHAPTER.match(n)
        if m and m.group(1) in BOOKS:
            pages.append((n, m.group(1), int(m.group(2))))

    added_tab = kept = changed = 0
    problems = []

    for name, slug, ch in pages:
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()
        original = text

        if "netbible.org" in text and "blueletterbible.org" in text:
            continue  # already done, safe to re-run

        existing = re.search(
            r'<div class="tab-content" id="tab-commentary">(.*?)</div>\s*\n',
            text, re.S)

        # Preserve the hand-written Guzik line where there is one; those
        # descriptions are chapter-specific and worth keeping.
        guzik = None
        if existing:
            m = re.search(r"<li><strong>Enduring Word.*?</li>",
                          existing.group(1), re.S)
            if m:
                guzik = m.group(0)
                kept += 1
        if guzik is None:
            guzik = guzik_li(slug, ch)

        block = build_tab([guzik, net_li(slug, ch), henry_li(slug, ch)])

        if existing:
            text = text[:existing.start()] + block + text[existing.end():]
        else:
            # no Commentary tab at all: add the button and the content pane,
            # both immediately before Videos
            btn = '<div class="study-tab" data-tab="videos">Videos</div>'
            if btn not in text:
                problems.append(f"{name}: no Videos tab to anchor against")
                continue
            text = text.replace(
                btn, TAB_BUTTON + "\n                " + btn, 1)
            vid = '            <div class="tab-content" id="tab-videos">'
            if vid not in text:
                problems.append(f"{name}: no Videos pane to anchor against")
                continue
            text = text.replace(vid, block + vid, 1)
            added_tab += 1

        o, c = len(re.findall(r"<div\b", text)), len(re.findall(r"</div>", text))
        if o != c:
            problems.append(f"{name}: would unbalance divs ({o} vs {c})")
            continue

        if text != original:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(text)

    verb = "would change" if check else "changed"
    print(f"{verb} {changed} pages")
    print(f"  Commentary tab created where there was none : {added_tab}")
    print(f"  existing Guzik descriptions preserved       : {kept}")
    for p in problems[:15]:
        print(f"    {p}")
    if len(problems) > 15:
        print(f"    ... {len(problems)} problems total")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
