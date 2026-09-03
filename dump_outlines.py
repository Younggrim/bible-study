#!/usr/bin/env python3
"""Print the inherited outline for a range of psalms, with verse totals and coverage.

    python3 dump_outlines.py 91 102
"""
import html as H
import os
import re
import sys

import audit_authorship as A

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
SUB = re.compile(r'<li>(.*?)</li>', re.S)
FIELD = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
WANT = ("Classification:", "Attributed Author:", "Key Themes:")


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for n in range(lo, hi + 1):
        path = os.path.join(DOCS, f"psalms{n}.html")
        raw = open(path, encoding="utf-8").read()
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', raw)}
        total = max(nums) if nums else 0
        pane = A.PANE.search(raw).group(2)
        items = SUB.findall(pane)
        fields = {H.unescape(l).strip(): H.unescape(re.sub(r"<.*?>", "", b)).strip()
                  for l, b in FIELD.findall(pane)}
        print(f"\n=== psalms{n} ({total} verses, {len(items)} outline items) ===")
        for k in WANT:
            if k in fields:
                v = fields[k]
                print(f"  {k} {v if len(v) < 400 else v[:400] + ' ...'}")
        covered = set()
        for it in items:
            it = H.unescape(re.sub(r"<.*?>", "", it)).strip()
            m = A.TAIL.search(it + ":")
            got = A.halves(m.group(1)) if m else set()
            covered |= got
            print(f"    - {it}")
        want = {(v, h) for v in range(1, total + 1) for h in ("a", "b")}
        gaps = sorted({v for v, _ in (want - covered)})
        if gaps:
            print(f"  GAPS: {gaps}")
        if not items:
            print("  NO SUBLIST")
    return 0


if __name__ == "__main__":
    sys.exit(main())
