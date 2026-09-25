#!/usr/bin/env python3
"""Serves the topical and life-study hero photos at a size that fits the
screen.

Every hero is an Unsplash photo, and Unsplash resizes and re-encodes on
request (w=, q=, auto=format for WebP/AVIF). The home page and life-studies
index already used a srcset; the rest did not, so a phone downloaded the
desktop image:

  * 25 life-study pages set the hero as a CSS background at w=1200 with no
    auto=format, 100-400 KB of JPEG. They gain auto=format, and a
    phone-width rule (<=700px) that asks for w=750. Measured: 211 KB -> 27 KB,
    412 KB -> 130 KB, 323 KB -> 124 KB.
  * 7 topical pages use a plain <img> at w=1400. They gain the same
    640/1000/1600 srcset the home page uses, with sizes="100vw".

Idempotent: a page that already has the rule or the srcset is left alone.

    python3 optimize_hero_images.py [--check]
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

BG = re.compile(
    r'(\.topic-hero::before\s*\{[^}]*?url\(")(https://images\.unsplash\.com/photo-[\w-]+)\?w=1200&q=80("\))')
IMG = re.compile(
    r'<img src="(https://images\.unsplash\.com/photo-[\w-]+)\?w=1400&q=80&auto=format"(?![^>]*srcset)')
PHONE_RULE = ('\n        @media (max-width: 700px) {{ .topic-hero::before {{ '
              'background-image: url("{base}?w=750&q=80&auto=format"); }} }}')


def fix(h):
    n = 0
    m = BG.search(h)
    if m and "?w=750&q=80&auto=format" not in h:
        base = m.group(2)
        h = h[:m.start()] + m.group(1) + base + "?w=1200&q=80&auto=format" + m.group(3) + h[m.end():]
        h = h.replace("</style>", PHONE_RULE.format(base=base) + "\n    </style>", 1)
        n += 1

    def srcset(mm):
        base = mm.group(1)
        return (f'<img src="{base}?w=1400&q=80&auto=format" '
                f'srcset="{base}?w=640&q=80&auto=format 640w, '
                f'{base}?w=1000&q=80&auto=format 1000w, '
                f'{base}?w=1600&q=80&auto=format 1600w" sizes="100vw"')
    h, k = IMG.subn(srcset, h)
    return h, n + k


def main():
    check = "--check" in sys.argv
    total = 0
    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        h = open(path, encoding="utf-8").read()
        new, n = fix(h)
        if n:
            total += n
            print(f"{os.path.basename(path)}: {n}")
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    print(f"{total} hero image(s) {'to update' if check else 'updated'}")


if __name__ == "__main__":
    main()
