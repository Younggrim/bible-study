#!/usr/bin/env python3
"""Fixes emphatic (shouting) capital letters embedded in the Author: and
Historical Context: bodies -- handoff item 3. These are words the author-fold
scripts preserved verbatim from source notes that used ALL CAPS for rhetorical
emphasis ("God is SPIRIT", "the PRIEST", "a FLOOD from the north"). None of
this corpus's own scripture quotations style ordinary words that way -- the
site's KJV/WEB text renders these words lowercase (e.g. Job 19:25 "my redeemer
liveth", Job 4:17 "his maker"), so the emphatic caps are corrected to plain
lowercase, matching the site's own quotations elsewhere.

The exception is words that are genuinely proper nouns/adjectives (personal and
place names) -- these are restored to Title Case, not lowercased, since the
corpus writes them that way everywhere else (Genesis, Babylon, Yahweh, ...).

Checked by hand against every occurrence before writing this list (see the
audit notes in CLAUDE_HANDOFF.md item 3): none of the flagged words turned out
to be a case needing special handling beyond these two buckets -- no
sentence-initial capitalization was needed (no flagged word sits at the very
start of a field or immediately after a period), and no divine-title word
(MAKER, REDEEMER, WITNESS, SPIRIT, INSTRUMENT) is capitalized in the site's own
KJV quotations, so those are lowercased along with the rest.

    python3 fix_emphatic_capitals.py [--check]
"""
import glob
import re
import sys

# A possessive "'S" (as in "LEVIATHAN'S") is a separate token under \b, since
# the apostrophe -- literal or the &#x27; entity used throughout this corpus --
# breaks the word boundary and a lone "S" fails the {2,} minimum, so it's
# captured here as an optional suffix and handled together with its stem.
CAPS = re.compile(r"\b[A-Z]{2,}\b(?:(?:['’]|&#x27;)S\b)?")

# Same allowlist as audit_authorship.py's CAPS_OK, plus LXX (a legitimate
# abbreviation for the Septuagint, not emphasis).
CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "III", "IV", "BRANCH", "HOLINESS", "PE", "AYIN", "MENE",
           "TEKEL", "UPHARSIN", "LXX"}

# Personal and place names -- restored to Title Case, not lowercased.
PROPER = {"AGUR", "BABYLON", "BABYLONIAN", "CYRUS", "DAVID", "DAVIDIC",
          "ISRAEL", "JERUSALEM", "SARAH", "ZION", "LEVIATHAN", "YAHWEH"}

FIELD = re.compile(
    r'(<span class="auth-label">(?:Author|Historical Context):</span>\s*)(.*?)(</div>)', re.S)


def fix_text(text):
    def repl(m):
        full = m.group(0)
        suffix = ""
        w = full
        if full.endswith("&#x27;S"):
            w, suffix = full[:-len("&#x27;S")], "&#x27;s"
        elif full[-2:] in ("'S", "’S"):
            w, suffix = full[:-2], full[-2:-1] + "s"
        if w in CAPS_OK:
            return w + suffix
        if w in PROPER:
            return w.capitalize() + suffix
        return w.lower() + suffix
    return CAPS.sub(repl, text)


def process(path, check):
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    changed = False

    def field_repl(m):
        nonlocal changed
        new_body = fix_text(m.group(2))
        if new_body != m.group(2):
            changed = True
        return m.group(1) + new_body + m.group(3)

    new_content = FIELD.sub(field_repl, content)

    if not changed:
        return "clean"
    if check:
        return "would-fix"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    return "fixed"


def main():
    check = "--check" in sys.argv
    counts = {}
    for path in sorted(glob.glob("docs/*.html")):
        result = process(path, check)
        counts[result] = counts.get(result, 0) + 1
        if result != "clean":
            print(f"{path}: {result}")
    print()
    print(counts)


if __name__ == "__main__":
    main()
