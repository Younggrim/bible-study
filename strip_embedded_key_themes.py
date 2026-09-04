#!/usr/bin/env python3
"""Strips the book-level 'Key themes: ...' sentence embedded in the Author: field
on 386 chapter pages -- a leftover from before each page had its own chapter-level
Key Themes: field (see add_key_themes_batch1.py through batch30.py). Handoff item 2.

Must run only after every chapter has its own Key Themes: field (item 1, done),
so no page is ever left without themes.

    python3 strip_embedded_key_themes.py [--check]
"""
import glob
import re
import sys

AUTHOR = re.compile(r'(auth-label">Author:</span> )(.*?)(</div>)', re.S)
KT_TAIL = re.compile(r'( ?Key [Tt]hemes:.*)$', re.S)


def process(path, check):
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    m = AUTHOR.search(content)
    if not m:
        return "no-author-field"

    author_text = m.group(2)
    km = KT_TAIL.search(author_text)
    if not km:
        return "clean"

    new_author_text = author_text[:km.start()]
    trimmed = new_author_text.rstrip()
    # Trailing closing quotes (literal or HTML entity) may follow the period.
    trimmed = re.sub(r"(&#x27;|&quot;|'|\")+$", "", trimmed).rstrip()
    if not trimmed.endswith("."):
        return f"unexpected-boundary: {new_author_text[-40:]!r}"

    new_content = content[:m.start()] + m.group(1) + new_author_text + m.group(3) + content[m.end():]

    if check:
        return "would-strip"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    return "stripped"


def main():
    check = "--check" in sys.argv
    counts = {}
    for path in sorted(glob.glob("docs/*.html")):
        result = process(path, check)
        counts[result] = counts.get(result, 0) + 1
        if result not in ("clean",):
            print(f"{path}: {result}")
    print()
    print(counts)


if __name__ == "__main__":
    main()
