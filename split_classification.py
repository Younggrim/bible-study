#!/usr/bin/env python3
"""
Splits the Classification field, which on 396 chapters holds two or three fields
run together in one div.

The label text was written into the body instead of being marked up, so the pane
renders as one long line:

    Classification: Prophetic Oracle - A Call to Rebuild the Temple Key Themes:
    Misplaced priorities, divine discipline through economic hardship, ...

    Classification: Wisdom Psalm Attributed Author: Anonymous (no superscription)
    Key Themes: Two ways of life, blessedness, ...

WORKFLOW.md specifies Classification as genre only, with Key Themes separate. This
splits on the two labels that are genuinely labels and emits one div each.

Only " Key Themes:" and " Attributed Author:" are treated as split points. Other
colons in these bodies belong to the genre title or to a parenthetical and must be
left alone:

    Oracle Against the Nations (Egypt Series: 1 of 7)
    Prophetic Oracle - The Valley of Decision: Final Judgment on the Nations
    Penitential Psalm (2nd of 7 Penitential Psalms: 6, 32, 38, ...)

Attributed Author is kept as its own field rather than folded away. On Psalms it is
the per-psalm attribution taken from the superscription, while the Author field
carries the same book-level text on all 150 chapters.

Only the Classification div is rewritten. The rest of the pane is untouched, so
this cannot disturb anything else on the page. Every new div is balanced, and the
script asserts that no text is lost: the concatenated new bodies must equal the old
body with the label strings removed.

Usage:
    python3 split_classification.py [--check] [--limit N]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('<div class="auth-item"><span class="auth-label">{label}</span> {body}</div>')

CLS = re.compile(r'<div class="auth-item"><span class="auth-label">'
                 r'Classification:</span>(.*?)</div>', re.S)

THEMES = " Key Themes:"
ATTRIB = " Attributed Author:"


def norm(s):
    return " ".join(s.split())


def split_body(body):
    """Returns [(label, value), ...] or None if there is nothing to split."""
    if THEMES not in body:
        return None
    head, themes = body.split(THEMES, 1)
    attrib = None
    if ATTRIB in head:
        head, attrib = head.split(ATTRIB, 1)
    out = [("Classification:", norm(head))]
    if attrib is not None:
        out.append(("Attributed Author:", norm(attrib)))
    out.append(("Key Themes:", norm(themes)))
    return out


def main():
    check = "--check" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    pages = sorted(f for f in os.listdir(DOCS)
                   if re.match(r"^[a-z0-9]+\d+\.html$", f) and f != "404.html")
    problems, planned, stats = [], {}, {"themes": 0, "attrib": 0}

    for fname in pages:
        path = os.path.join(DOCS, fname)
        page = fname[:-5]
        html = open(path, encoding="utf-8").read()

        pane = re.search(r'id="tab-authorship">(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            continue
        hit = CLS.search(pane.group(1))
        if not hit:
            continue

        fields = split_body(hit.group(1))
        if fields is None:
            continue

        for label, value in fields:
            if not value:
                problems.append(f"{page}: empty {label}")
            if THEMES.strip() in value or ATTRIB.strip() in value:
                problems.append(f"{page}: label survived inside {label}")
        genre = fields[0][1]
        if len(genre) > 220:
            problems.append(f"{page}: genre implausibly long ({len(genre)})")

        # Nothing may be lost: old body minus the labels must equal the new bodies.
        want = norm(hit.group(1).replace(THEMES, " ").replace(ATTRIB, " "))
        got = norm(" ".join(v for _, v in fields))
        if want != got:
            problems.append(f"{page}: text would change")
            continue

        block = "\n                    ".join(ITEM.format(label=l, body=v)
                                              for l, v in fields)
        start = pane.start(1) + hit.start()
        end = pane.start(1) + hit.end()
        new = html[:start] + block + html[end:]

        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue

        planned[path] = new
        stats["themes"] += 1
        if len(fields) == 3:
            stats["attrib"] += 1
        if limit and len(planned) >= limit:
            break

    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems[:20]:
            print(f"    {p}")
        return 1

    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)

    print(f"{'would split' if check else 'split'} {len(planned)} pages "
          f"({stats['attrib']} also had Attributed Author)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
