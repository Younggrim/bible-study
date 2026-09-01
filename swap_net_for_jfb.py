#!/usr/bin/env python3
"""
Replaces the NET Bible entry in the Commentary tab with Jamieson-Fausset-Brown.

The NET entry was a mistake on my part. netbible.org/bible/<Book>+<Chapter>
serves the chapter text to read; its translator notes are loaded client-side and
only appear once you interact with a verse. Listing that next to Guzik and
Matthew Henry as a commentary promised something the click did not deliver.
lumina.bible.org is the same application, byte for byte, so it is no better.

NET's notes are genuinely valuable, but they are a translation apparatus rather
than a commentary. If they are ever wanted, the right shape is inline footnotes
attached to the NET translation block on the page, not an outbound link.

Jamieson-Fausset-Brown (1871) replaces it:
  - a real commentary that opens as commentary
  - public domain
  - served by Blue Letter Bible, the same host and URL pattern already proven
    for Matthew Henry, so no new failure mode
  - verified to carry substantial content across the canon, from 26,000 to
    94,000 characters depending on the chapter

Also checked and rejected on the same host: Darby's Synopsis and Scofield's
notes both return an identical 25,144-character page for Genesis 1 and Romans 8,
which means it is a placeholder rather than content.

Usage:
    python3 swap_net_for_jfb.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^([a-z0-9]+?)(\d+)\.html$")

BLB_CODE = {
    "genesis": "Gen", "exodus": "Exd", "leviticus": "Lev", "numbers": "Num",
    "deuteronomy": "Deu", "joshua": "Jos", "judges": "Jdg", "ruth": "Rth",
    "1samuel": "1Sa", "2samuel": "2Sa", "1kings": "1Ki", "2kings": "2Ki",
    "1chronicles": "1Ch", "2chronicles": "2Ch", "ezra": "Ezr",
    "nehemiah": "Neh", "esther": "Est", "job": "Job", "psalms": "Psa",
    "proverbs": "Pro", "ecclesiastes": "Ecc", "songofsolomon": "Sng",
    "isaiah": "Isa", "jeremiah": "Jer", "lamentations": "Lam",
    "ezekiel": "Eze", "daniel": "Dan", "hosea": "Hos", "joel": "Jol",
    "amos": "Amo", "obadiah": "Oba", "jonah": "Jon", "micah": "Mic",
    "nahum": "Nam", "habakkuk": "Hab", "zephaniah": "Zep", "haggai": "Hag",
    "zechariah": "Zec", "malachi": "Mal", "matthew": "Mat", "mark": "Mar",
    "luke": "Luk", "john": "Jhn", "acts": "Act", "romans": "Rom",
    "1corinthians": "1Co", "2corinthians": "2Co", "galatians": "Gal",
    "ephesians": "Eph", "philippians": "Phl", "colossians": "Col",
    "1thessalonians": "1Th", "2thessalonians": "2Th", "1timothy": "1Ti",
    "2timothy": "2Ti", "titus": "Tit", "philemon": "Phm", "hebrews": "Hbr",
    "james": "Jam", "1peter": "1Pe", "2peter": "2Pe", "1john": "1Jo",
    "2john": "2Jo", "3john": "3Jo", "jude": "Jde", "revelation": "Rev",
}

LINK = ('<a href="{url}" target="_blank" '
        'style="color:var(--accent-link);text-decoration:none;'
        'border-bottom:1px dotted var(--accent-link);">{label}</a>')


def jfb_li(slug, ch):
    code = BLB_CODE[slug]
    url = (f"https://www.blueletterbible.org/comm/jfb/"
           f"{code}/{code}_{int(ch):03d}.cfm")
    link = LINK.format(url=url, label="blueletterbible.org")
    return ("<li><strong>Jamieson-Fausset-Brown (1871):</strong> "
            f"{link} A critical and explanatory commentary on the whole Bible, "
            "more concise than Matthew Henry and closer to the Hebrew and Greek, "
            "with attention to historical and geographical detail. Public "
            "domain.</li>")


# the NET entry as written by add_commentaries.py
NET_LI = re.compile(r"<li><strong>NET Bible translator notes:</strong>.*?</li>",
                    re.S)


def main():
    check = "--check" in sys.argv
    changed = 0
    skipped = 0
    problems = []

    for name in sorted(os.listdir(DOCS)):
        m = CHAPTER.match(name)
        if not m or m.group(1) not in BLB_CODE:
            continue
        slug, ch = m.group(1), int(m.group(2))
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()

        if "comm/jfb/" in text:
            skipped += 1
            continue
        if not NET_LI.search(text):
            problems.append(f"{name}: no NET entry to replace")
            continue

        new = NET_LI.sub(lambda _: jfb_li(slug, ch), text, count=1)
        if "netbible.org" in new:
            problems.append(f"{name}: a netbible.org link survived the swap")
            continue
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{name}: would unbalance divs")
            continue

        changed += 1
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    verb = "would swap" if check else "swapped"
    print(f"{verb} NET -> Jamieson-Fausset-Brown on {changed} pages")
    if skipped:
        print(f"  {skipped} pages already had JFB, skipped")
    for p in problems[:15]:
        print(f"    {p}")
    if len(problems) > 15:
        print(f"    ... {len(problems)} problems total")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
