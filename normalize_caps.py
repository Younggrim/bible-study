#!/usr/bin/env python3
"""
Removes emphatic capitals from Authorship & Background, so formatting is uniform
across all 1189 chapters.

Some paragraphs shout for emphasis - "a NARRATIVE about the prophet", "he wants
them DESTROYED", "always DOWNWARD". 413 chapters carry 1,115 such words. Ruth,
Jonah and everything written to the target format use sentence case, so these are
a formatting inconsistency rather than content.

Only formatting changes. No wording is altered, nothing is added or removed, and
chapter-specific and book-specific content is left exactly as written.

What is never touched, because the capitals are correct:
  the divine name    LORD, GOD, YHWH, JEHOVAH
  translations       ESV, KJV, ASV, NET, WEB, BSB, NIV, NASB, LXX, MT
  eras and canon     BC, AD, NT, OT
  roman numerals     II, III, IV, VI, VII, VIII, IX, XI, XII
  initialisms        USA, PDF and anything else on KEEP below

A word is only lowered when it appears inside a sentence. A capitalised word that
opens a sentence keeps its initial capital, so "NOT so" becomes "Not so" at the
start of a sentence and "not so" mid-sentence.

Usage:
    python3 normalize_caps.py [--check] [--book <slug>] [--list]

--list  print every distinct all-caps word found, with counts, and stop. Run
        this and read it before applying, so anything that should be on KEEP is
        caught first.
"""
import os
import re
import sys
from collections import Counter

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^([a-z0-9]+?)(\d+)\.html$")

KEEP = {
    # the divine name and its forms
    "LORD", "GOD", "YHWH", "YAHWEH", "JEHOVAH", "ELOHIM", "ADONAI", "SHADDAI",
    # translations and text-critical shorthand
    "ESV", "KJV", "ASV", "NET", "WEB", "BSB", "NIV", "NASB", "NKJV", "CSB",
    "LXX", "MT", "NT", "OT", "BC", "AD", "CE", "BCE",
    # roman numerals
    "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV",
    # the writing on the wall, Daniel 5:25, conventionally set in capitals
    "MENE", "TEKEL", "UPHARSIN", "PERES",
    # Hebrew letter names, which head the acrostic stanzas of Psalm 119
    "ALEPH", "BETH", "GIMEL", "DALETH", "HE", "WAW", "VAV", "ZAYIN", "HETH",
    "TETH", "YOD", "YODH", "KAPH", "LAMED", "MEM", "NUN", "SAMEKH", "AYIN",
    "PE", "TSADE", "TZADI", "QOPH", "RESH", "SIN", "SHIN", "TAW", "TAV",
    # misc
    "USA", "PDF", "HTML", "URL", "API", "AM", "PM",
}

WORD = re.compile(r"\b[A-Z]{2,}\b")

# Only words on this list are ever changed. Everything else is left exactly as
# written.
#
# This is deliberately an allow list of ordinary English rather than a block list
# of names. Two attempts at detecting names automatically both failed: a word
# appearing in Title Case tells you nothing, because sentences start with "The"
# and "Not" constantly, and restricting to mid-sentence Title Case still learned
# 4,718 "names" including NOT, ALL, THE and TOTAL, because capitals also follow
# colons, dashes and open quotes. Under that rule only 138 of 595 words would
# have been touched, and several real names were still at risk.
#
# So the safe direction is the other one. Anything not listed here survives
# untouched, which means a shouted name is left shouting rather than being
# quietly turned into a common noun. Add to this list as more are confirmed.
LOWER = {
    # function words and common verbs, the bulk of the shouting
    "NOT", "AND", "ALL", "THE", "IS", "IF", "IN", "TO", "NO", "WILL", "OF",
    "BEFORE", "ONE", "WHY", "THEN", "BOTH", "YOU", "FIRST", "AFTER", "FOR",
    "NOW", "HOW", "RIGHT", "TAKE", "CAN", "WITH", "FROM", "KNOW", "ONLY",
    "MORE", "NEW", "UP", "OWN", "HIMSELF", "WHO", "HIS", "AGAIN", "EVERYTHING",
    "BUT", "BY", "AT", "ANY", "ARE", "AS", "BE", "COME", "DAY", "DAYS", "DID",
    "DO", "DOES", "DONE", "DOWN", "EACH", "END", "EVEN", "EVER", "GAVE", "GIVE",
    "GO", "HAD", "HAS", "HAVE", "HE", "HEAR", "HER", "HERE", "HIGH", "HOPE",
    "INTO", "IT", "LAST", "LEFT", "LESS", "LIKE", "LIVE", "LONG", "MADE", "MAY",
    "ME", "MOST", "MUST", "MY", "NEAR", "NONE", "ON", "OPEN", "OR", "OUR",
    "OUT", "OVER", "PAID", "PAST", "PUT", "READ", "SAME", "SAW", "SEE", "SEEK",
    "SEEN", "SENT", "SHOW", "SOME", "STAY", "THAT", "THEE", "THEM", "THEY",
    "THIS", "TOP", "TORN", "TRUE", "TRY", "TURN", "TWO", "UNTO", "WAKE", "WANT",
    "WARN", "WAS", "WE", "WELL", "WERE", "WHAT", "WHEN", "WON", "WORD", "YOUR",
    "YOURSELVES", "FOUR", "FREE", "FULL", "SIX", "THIRTY", "ALREADY", "ALONE",
    "ALSO", "ALWAYS", "AMONG", "ANOTHER", "AROUND", "AGAINST", "BESIDE",
    "BETTER", "BEYOND", "BECAUSE", "BECOME", "BECOMES", "ABOUT",
    # emphatic content words, safe because none is a biblical name
    "DESTROYED", "CLIMAX", "TOTAL", "PARALLEL", "RESPOND", "CONSTANT", "PURE",
    "MYSTERY", "GREAT", "DARKEST", "UNITY", "HUMILITY", "FRIENDSHIP", "LOVE",
    "CHOICES", "ANSWERS", "REMEMBERS", "SWORE", "TODAY", "CALL", "BELIEVE",
    "PREACHER", "FACT", "ACTION", "TEACHES", "ARRIVAL", "COMMANDS", "NATIONS",
    "PEOPLES", "ENEMIES", "LETTER", "NARRATIVE", "DOWNWARD", "SIMPLEST",
    "SHORTEST", "POWERFUL", "FURIOUS", "KNEW", "HAND", "HEAD", "LAND", "LAW",
    "LIFE", "MAN", "MEN", "NAME", "OIL", "SEA", "SHIP", "SIN", "SONG", "WOOD",
    "EAST", "EASE", "EAR", "EYES", "FAST", "FIRE", "FOOL", "FOOT", "FUEL",
    "FURY", "GAP", "HIDE", "HOLY", "IRON", "LIES", "MARK", "PLUS", "TOWN",
    "TYPE", "CAMP", "DEAD", "BEST",
}



def collect_words():
    counts = Counter()
    for name in sorted(os.listdir(DOCS)):
        if not CHAPTER.match(name):
            continue
        t = open(os.path.join(DOCS, name), encoding="utf-8").read()
        m = re.search(r'id="tab-authorship">(.*?)(?=<div class="tab-content")',
                      t, re.S)
        if not m:
            continue
        plain = re.sub(r"<[^>]+>", " ", m.group(1))
        for w in WORD.findall(plain):
            counts[w] += 1
    return counts


def normalize(body):
    """Lower emphatic capitals in the pane body. Returns (new_body, n)."""
    count = 0

    def repl(m):
        nonlocal count
        w = m.group(0)
        if w not in LOWER:
            return w
        count += 1
        before = body[:m.start()]
        tail = re.sub(r"(\s|</?[a-zA-Z][^>]*>)+$", "", before)
        starts_sentence = (tail == "" or tail[-1] in ".!?:" or tail.endswith("—"))
        return w.capitalize() if starts_sentence else w.lower()

    return WORD.sub(repl, body), count


def main():
    if "--list" in sys.argv:
        counts = collect_words()
        print(f"{len(counts)} distinct all-caps words, "
              f"{sum(counts.values())} occurrences\n")
        for w, c in counts.most_common():
            print(f"  {c:>5}  {w}")
        return 0

    check = "--check" in sys.argv
    only = None
    if "--book" in sys.argv:
        only = sys.argv[sys.argv.index("--book") + 1]

    files = words = 0
    per_book = Counter()
    for name in sorted(os.listdir(DOCS)):
        m = CHAPTER.match(name)
        if not m or (only and m.group(1) != only):
            continue
        path = os.path.join(DOCS, name)
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            continue

        new_body, n = normalize(pane.group(2))
        if not n:
            continue
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]

        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            print(f"  SKIPPED {name}: div imbalance {o} vs {c}")
            continue
        # the body must only differ in letter case
        if new_body.lower() != pane.group(2).lower():
            print(f"  SKIPPED {name}: change was not case-only")
            continue

        files += 1
        words += n
        per_book[m.group(1)] += n
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    verb = "would normalize" if check else "normalized"
    print(f"{verb} {words} words across {files} chapters")
    for b, c in per_book.most_common(15):
        print(f"    {b:18}{c:>5}")
    if len(per_book) > 15:
        print(f"    ... {len(per_book)} books total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
