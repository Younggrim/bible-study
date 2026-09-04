#!/usr/bin/env python3
"""Print condensed authorship-pane content for chapters missing Key Themes, to
compose Classification + Key Themes from. Not a repo tool - scratch helper.

    python3 dump_for_themes.py genesis 2 5
"""
import html as H
import os
import re
import sys

import audit_authorship as A

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
FIELD = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)


def main():
    book = sys.argv[1]
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for n in range(lo, hi + 1):
        path = os.path.join(DOCS, f"{book}{n}.html")
        if not os.path.exists(path):
            continue
        raw = open(path, encoding="utf-8").read()
        m = A.PANE.search(raw)
        if not m:
            continue
        pane = m.group(2)
        fields = [(H.unescape(l).strip(), H.unescape(re.sub(r"<.*?>", "", b)).strip())
                  for l, b in FIELD.findall(pane)]
        has_kt = any(l == "Key Themes:" for l, _ in fields)
        print(f"\n=== {book}{n} === {'[HAS KEY THEMES]' if has_kt else '[MISSING]'}")
        for label, body in fields:
            if label in ("Author:", "Title:", "Purpose:", "Audience:"):
                continue
            short = body if len(body) < 600 else body[:600] + " ..."
            print(f"  {label} {short}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
