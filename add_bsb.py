#!/usr/bin/env python3
"""
One-time: add the Berean Standard Bible as a baked-in translation on every
chapter page.

The BSB was dedicated to the public domain on 30 April 2023, so unlike the ESV
it needs no API, no key and no proxy. That matters here: it makes BSB the only
modern-readable translation on the site that works offline and cannot fail at
runtime. It is baked into the HTML exactly like KJV, ASV, NET and WEB.

Source: https://bereanbible.com/bsb.txt — tab separated, "Book C:V<TAB>text",
31,102 verses across all 66 books. Verified before writing anything: BSB's verse
count matches the page's existing KJV block in all 1189 chapters, so the
versification agrees and no chapter needs a judgement call.

BSB is inserted directly after ESV rather than appended last, because both are
modern readable translations and burying it behind three archaic ones would
hide the point of adding it.

Usage:
    python3 add_bsb.py /path/to/bsb.txt [--check]
"""
import html
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^([a-z0-9]+?)(\d+)\.html$")


def parse_bsb(path):
    """(slug, chapter) -> {verse_number: text}"""
    out = {}
    skipped = 0
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            if "\t" not in line:
                continue
            ref, text = line.split("\t", 1)
            m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref.strip())
            if not m:
                skipped += 1
                continue
            book, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
            slug = book.lower().replace(" ", "")
            if slug == "psalm":          # BSB says Psalm, the site says psalms
                slug = "psalms"
            out.setdefault((slug, ch), {})[vs] = text.strip()
    return out, skipped


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_block(verses):
    lines = ['        <div class="translation-block" data-translation="BSB">']
    for n in sorted(verses):
        lines.append(f'            <p class="verse">'
                     f'<span class="verse-num">{n}</span>{esc(verses[n])}</p>')
    lines.append("        </div>")
    return "\n".join(lines)


def kjv_verse_count(text):
    i = text.find('data-translation="KJV"')
    if i < 0:
        return None
    j = text.find('data-translation="ASV"', i)
    seg = text[i:j] if j > 0 else text[i:]
    return len(re.findall(r'class="verse-num">(\d+)<', seg))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    if not args:
        sys.exit(__doc__)
    bsb, skipped = parse_bsb(args[0])
    print(f"BSB: {len(bsb)} chapters, {sum(len(v) for v in bsb.values())} verses "
          f"({skipped} header lines skipped)")

    # Only real chapter pages. The filename pattern alone also matches things
    # like 404.html, which parses as book "4" chapter 4.
    books = {slug for slug, _ in bsb}
    pages = []
    for n in sorted(os.listdir(DOCS)):
        m = CHAPTER.match(n)
        if m and m.group(1) in books:
            pages.append(n)
    print(f"chapter pages to process: {len(pages)}")

    done = already = nodata = countbad = 0
    problems = []

    for name in pages:
        m = CHAPTER.match(name)
        slug, ch = m.group(1), int(m.group(2))
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()

        if 'data-translation="BSB"' in text:
            already += 1
            continue
        verses = bsb.get((slug, ch))
        if not verses:
            nodata += 1
            problems.append(f"{name}: no BSB text for {slug} {ch}")
            continue

        # refuse to write if versification disagrees with what is already there
        kjv = kjv_verse_count(text)
        if kjv and kjv != len(verses):
            countbad += 1
            problems.append(f"{name}: KJV has {kjv} verses, BSB has {len(verses)}")
            continue

        # insert immediately after the ESV block's closing tag
        i = text.find('data-translation="ESV"')
        if i < 0:
            problems.append(f"{name}: no ESV block found")
            continue
        close = text.find("\n        </div>", i)
        if close < 0:
            problems.append(f"{name}: could not find the end of the ESV block")
            continue
        at = close + len("\n        </div>")
        new = text[:at] + "\n\n" + build_block(verses) + text[at:]

        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{name}: would unbalance divs ({o} vs {c})")
            continue

        if not check:
            open(path, "w", encoding="utf-8").write(new)
        done += 1

    verb = "would add" if check else "added"
    print(f"{verb} BSB to {done} pages")
    if already:
        print(f"  {already} pages already had it, skipped")
    if nodata:
        print(f"  {nodata} pages had no matching BSB text")
    if countbad:
        print(f"  {countbad} pages had a verse-count disagreement")
    for p in problems[:20]:
        print(f"    {p}")
    if len(problems) > 20:
        print(f"    ... {len(problems)} problems total")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
