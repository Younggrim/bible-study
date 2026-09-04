#!/usr/bin/env python3
"""
Americanises a fixed set of British spellings in the site's own prose (item 4
of the WORKFLOW.md handoff outstanding list).

Scope, deliberately narrow: only words that never occur in KJV vocabulary at
all -- centre, theatre, programme, organise/organised/..., cancelled,
travelled/traveller, recognise/recognised, realise/realised, summarise/...,
emphasise/..., criticise/..., apologise/..., characterise/..., symbolise/...,
minimise/..., jewellery, grey, licence, modelling. Because the KJV simply does
not use this vocabulary, any occurrence in this corpus is guaranteed to be the
site's own commentary voice, never an unmarked echo of scripture wording.

Deliberately EXCLUDED from this pass: honour, neighbour, labour, favour,
saviour, defence, offence, rumour, valour, behaviour, splendour, humour,
colour. These are classic KJV vocabulary, and this corpus's writing style
frequently echoes KJV phrasing inline without quotation marks (e.g.
"thinkest thou that David doth honour thy father" in 1chronicles19's
Authorship & Background pane, lifted almost verbatim from the verse text
right above it). Distinguishing the site's own voice from an unmarked
scripture echo for those words needs sentence-by-sentence judgment, not a
word list -- that is future work, not something this script attempts.

Case-preserving: a capitalised match ("Organised") becomes a capitalised
replacement ("Organized"); anything else is lowercased.

Runs everywhere outside <div class="scripture-container">...</div>, so it
covers the Authorship & Background pane, reflection questions, commentary,
articles notes and map/geography text alike -- not just auth-item bodies.

Usage:
    python3 normalize_british_spelling.py [--check]
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

# british -> american, lowercase keys/values; matching is case-insensitive,
# replacement re-cases to match the matched text's capitalisation.
MAP = {
    "centre": "center", "centrepiece": "centerpiece", "theatre": "theater",
    "programme": "program", "programmes": "programs",
    "jewellery": "jewelry", "grey": "gray", "modelling": "modeling",
    "licence": "license", "licenced": "licensed",
    "organise": "organize", "organised": "organized",
    "organises": "organizes", "organiser": "organizer",
    "organisers": "organizers",
    "cancelled": "canceled",
    "travelled": "traveled", "traveller": "traveler",
    "travellers": "travelers",
    "recognise": "recognize", "recognised": "recognized",
    "realise": "realize", "realised": "realized",
    "summarise": "summarize", "summarised": "summarized",
    "summarises": "summarizes",
    "emphasise": "emphasize", "emphasised": "emphasized",
    "criticise": "criticize", "criticised": "criticized",
    "apologise": "apologize", "apologised": "apologized",
    "characterise": "characterize", "characterised": "characterized",
    "symbolise": "symbolize", "symbolised": "symbolized",
    "minimise": "minimize", "minimised": "minimized",
}
PAT = re.compile(r"\b(" + "|".join(MAP.keys()) + r")\b", re.I)
CONTAINER = re.compile(r'<div class="scripture-container">')


def recase(matched, replacement):
    if matched[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def div_end(text, open_pos):
    depth = 0
    for m in re.finditer(r"<div\b|</div>", text[open_pos:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            return open_pos + m.end()
    return len(text)


def fix_file(raw):
    m = CONTAINER.search(raw)
    if not m:
        head, container, tail = raw, "", ""
    else:
        end = div_end(raw, m.start())
        head, container, tail = raw[:m.start()], raw[m.start():end], raw[end:]

    n = 0

    def repl(mm):
        nonlocal n
        n += 1
        return recase(mm.group(0), MAP[mm.group(0).lower()])

    head = PAT.sub(repl, head)
    tail = PAT.sub(repl, tail)
    return head + container + tail, n


def main():
    check = "--check" in sys.argv
    total = 0
    files = 0
    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        raw = open(path, encoding="utf-8").read()
        new_raw, n = fix_file(raw)
        if n:
            files += 1
            total += n
            if not check:
                open(path, "w", encoding="utf-8").write(new_raw)
    print(f"{'would fix' if check else 'fixed'} {total} occurrences across {files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
