#!/usr/bin/env python3
"""Print the KJV verse text for a range of psalms.

    python3 dump_kjv.py 91 96
"""
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
BLOCK = re.compile(r'<div class="translation-block"[^>]*data-translation="KJV"[^>]*>(.*?)</div>',
                   re.S)
VERSE = re.compile(r'<span class="verse-num">(\d+)</span>(.*?)</p>', re.S)


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for n in range(lo, hi + 1):
        raw = open(os.path.join(DOCS, f"psalms{n}.html"), encoding="utf-8").read()
        m = BLOCK.search(raw)
        if not m:
            print(f"--- psalms{n}: no KJV block ---")
            continue
        print(f"--- psalms{n} ---")
        for num, txt in VERSE.findall(m.group(1)):
            txt = H.unescape(re.sub(r"<.*?>", "", txt)).strip()
            print(f"{num}. {txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
