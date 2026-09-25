#!/usr/bin/env python3
"""Moves the warm neutral colors on the topical, life-study and home pages
onto CSS custom properties, so New River renders its own palette there.

These pages carry their own <style> blocks. Their per-topic accents (the teal,
green, purple and brown of each topic card, the gold labels) are deliberate
splashes of color and stay literal, per WORKFLOW.md. What moves is the warm
neutral scaffolding that was really the bible-study palette in disguise: page
background, tints, soft rules, body and list text, light text on dark heroes,
and the home page's prayer-band gradient. On New River these rendered cream
and brown against a black-and-white palette.

The tokens are defined in docs/site/style.css in both repositories. Their
bible-study values equal the literals they replace (light text on dark heroes
is unified on #f5ebe0, a difference of a few units), so bible-study looks the
same after this runs.

    python3 tokenize_neutral_colors.py [--check]
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

GRADIENT = ("linear-gradient(180deg, #1a1410 0%, #2a1f14 15%, var(--ink-deep) 40%, "
            "#4a3828 60%, #6b5040 72%, #a08060 82%, #d4bea0 90%, #f5ebe0 96%, #faf5ed 100%)")

# (regex on a CSS declaration, replacement). Order matters: the gradient first.
RULES = [
    (re.escape(GRADIENT), "var(--prayer-gradient)"),
    (r"(background(?:-color)?:\s*)#faf5ed", r"\1var(--bg-page)"),
    (r"(color:\s*)#faf5ed", r"\1var(--bg-page)"),
    (r"(background(?:-color)?:\s*)#f5ebe0", r"\1var(--bg-tint)"),
    (r"(color:\s*)#f5ebe0", r"\1var(--text-on-dark)"),
    (r"linear-gradient\((\d+deg), #faf5ed 0%, #f5ebe0 100%\)",
     r"linear-gradient(\1, var(--bg-page) 0%, var(--bg-tint) 100%)"),
    (r"linear-gradient\((\d+deg), #f5ebe0 0%, #faf3e0 100%\)",
     r"linear-gradient(\1, var(--bg-tint) 0%, var(--bg-tint-2) 100%)"),
    (r"(border(?:-bottom|-top)?:\s*1px solid )#f0e8dc", r"\1var(--rule-soft)"),
    (r"(color:\s*)#(?:f0e8dc|f5f0e8|f0e4d4)", r"\1var(--text-on-dark)"),
    (r"(color:\s*)#3d332b", r"\1var(--text-body)"),
    (r"(color:\s*)#4a3f35", r"\1var(--text-list)"),
    (r"(color:\s*)#(?:5a4e44|5c5248)", r"\1var(--text-muted)"),
]
# 404.html's heading and secondary button are the site's brown, not a topic
PAGE_RULES = {
    "404.html": [(r"(color:\s*)#6b5040", r"\1var(--accent-brown)"),
                 (r"(color:\s*)#6b4c3b", r"\1var(--accent-brown)")],
}


def main():
    check = "--check" in sys.argv
    total = 0
    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        if re.search(r"[a-z]\d+\.html$", name):
            continue  # chapter pages carry no neutral literals
        h = open(path, encoding="utf-8").read()
        new, n = h, 0
        for rx, rep in RULES + PAGE_RULES.get(name, []):
            new, k = re.subn(rx, rep, new)
            n += k
        if n:
            total += n
            print(f"{name}: {n}")
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    print(f"{total} replacement(s){' (check only)' if check else ''}")


if __name__ == "__main__":
    main()
