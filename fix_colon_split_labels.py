#!/usr/bin/env python3
"""
Repairs field labels that were cut at the wrong colon.

The pattern is always the same. A heading like

    The First Plague: Water to Blood (vv.14-25)

was split at its first colon, so the label became 'The First Plague:' and the rest
of the heading, verse range included, was stranded at the front of the body:

    <span class="auth-label">The First Plague:</span> Water to Blood (vv.14-25):
    God sends Moses to meet Pharaoh at the Nile...

The visible effect is a heading that names a topic but not its verses, and a
paragraph that opens with its own title. The effect on the audit is worse: the page
appears to have no section for those verses at all, so exodus7 read as twelve
verses undescribed when the description was sitting right there.

The repair moves the stranded fragment back into the label. Nothing is written and
nothing is deleted.

Book-level fields are excluded by name, because a sentence in Historical Context
that happens to cite a verse range early on is not a split label. deuteronomy6 and
isaiah59 both match the shape and both are ordinary prose.

leviticus23 needs the shouting removed at the same time. Its seven feasts were
labelled FEAST 1 through FEAST 7 with PASSOVER, UNLEAVENED BREAD, FIRSTFRUITS,
PENTECOST, TRUMPETS, ATONEMENT and TABERNACLES in capitals inside the stranded
fragment. Rejoining without fixing that would move eight all-capital words from
body text into headings.

Usage:
    python3 fix_colon_split_labels.py [--check]
"""
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
ITEM_RE = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')
TAIL = re.compile(r'\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)\s*:\s*$')
LEAD = re.compile(r'^(.{1,90}?\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\))\s*:\s+')
BOOK_FIELDS = {
    "Author:", "Historical Context:", "Classification:", "Key Themes:", "Purpose:",
    "Date Written:", "Audience:", "Recipient:", "Theme:", "Prologue:", "Notable:",
    "Speakers:", "Date:", "Subscription:",
}
CAPS = re.compile(r"\b[A-Z]{2,}\b")
CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "BRANCH", "HOLINESS", "PE", "AYIN", "MENE", "TEKEL",
           "UPHARSIN"}

# Titles that arrive in capitals and have to be written normally before they are
# promoted into a heading. Every one is an ordinary noun, not an acronym.
DECAPS = {
    "FEAST 1": "Feast 1", "FEAST 2": "Feast 2", "FEAST 3": "Feast 3",
    "FEAST 4": "Feast 4", "FEAST 5": "Feast 5", "FEAST 6": "Feast 6",
    "FEAST 7": "Feast 7",
    "PASSOVER": "Passover", "UNLEAVENED BREAD": "Unleavened Bread",
    "FIRSTFRUITS": "Firstfruits", "PENTECOST": "Pentecost",
    "FEAST of WEEKS": "Feast of Weeks", "TRUMPETS": "Trumpets",
    "ATONEMENT": "Atonement", "TABERNACLES": "Tabernacles", "BOOTHS": "Booths",
}


def decap(text):
    for bad, good in sorted(DECAPS.items(), key=lambda kv: -len(kv[0])):
        text = text.replace(bad, good)
    return text


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        page = name[:-5]
        path = os.path.join(DOCS, name)
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        touched = False
        for it in items:
            label = H.unescape(it[0]).strip()
            if label in BOOK_FIELDS or TAIL.search(label):
                continue
            if label.startswith("Chapter ") or label.startswith("Purpose of"):
                continue
            plain = H.unescape(re.sub(r"<.*?>", "", it[1])).strip()
            m = LEAD.match(plain)
            if not m:
                continue
            lead = m.group(1)
            # Cut the same span off the raw body, which may carry entities or tags.
            raw = it[1]
            cut = raw
            idx = 0
            seen = 0
            target = len(m.group(0))
            while idx < len(raw) and seen < target:
                if raw[idx] == "&":
                    end = raw.find(";", idx)
                    idx = end + 1 if end != -1 else idx + 1
                elif raw[idx] == "<":
                    end = raw.find(">", idx)
                    idx = end + 1 if end != -1 else idx + 1
                    continue
                else:
                    idx += 1
                seen += 1
            cut = raw[idx:].lstrip()
            new_label = decap(label.rstrip(":") + ": " + lead) + ":"
            stray = sorted({w for w in CAPS.findall(new_label) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} would enter label {new_label!r}")
                continue
            if not TAIL.search(new_label):
                problems.append(f"{page}: rejoined label has no trailing range: {new_label!r}")
                continue
            if not cut:
                problems.append(f"{page}: body would be empty after cutting {lead!r}")
                continue
            it[0], it[1] = new_label, cut
            touched = True
            notes.append(f"{page}: {label!r} + {lead!r} -> {new_label!r}")
        if not touched:
            continue
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    for n in notes:
        print(f"    {n}")
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would rejoin' if check else 'rejoined'} {len(notes)} label(s) "
          f"across {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
