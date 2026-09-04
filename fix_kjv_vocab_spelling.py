#!/usr/bin/env python3
"""Americanises a hand-reviewed subset of classic-KJV-vocabulary British
spellings (honour, neighbour, labour, favour, saviour, defence, offence,
rumour, valour, behaviour, splendour, humour, colour) in the site's own
commentary voice -- the harder half of handoff item 4 that
normalize_british_spelling.py deliberately left alone.

This is NOT a word-list pass. Every one of the 111 candidate occurrences
below (words outside <div class="scripture-container">, not immediately
adjacent to a quote mark, and not matching a >=20-character run of the same
page's own KJV translation-block text) was read by hand in its full sentence
before being marked FIX (the site's own analytical voice, no relation to any
specific verse's wording) or left alone as LEAVE (a paraphrase or clear echo
of a specific verse -- Proverbs 3:16 "riches and honour in her left",
Philippians 1:7 "the defence and confirmation of the gospel", 1 Thessalonians
1:3's "labour of love" triad, a quoted verse from a *different* chapter such
as Exodus 21:14 or 2 Samuel 12:11, etc.). See CLAUDE_HANDOFF.md item 4 for the
full accounting.

Each entry below is (file, exact American replacement, a substring unique to
that one occurrence's sentence) so that only the specific flagged word in the
specific flagged sentence is touched -- other occurrences of the same word
elsewhere on the same page, including ones deliberately left as an echo, are
untouched.

    python3 fix_kjv_vocab_spelling.py [--check]
"""
import glob
import re
import sys

# (relative path, american spelling to insert, unique substring of the
# sentence containing the flagged British word -- used both to locate the
# occurrence and, via the enclosed original word, to do the replacement)
FIXES = [
    ("docs/1corinthians1.html", "offense", "being an offence to the first and absurd to the second"),
    ("docs/1samuel15.html", "honor", "a confession more concerned with honour than with restoration"),
    ("docs/2chronicles8.html", "labor", "the labour is accounted for as carefully as in chapter 2"),
    ("docs/2kings19.html", "labor", "a labour that cannot be completed"),
    ("docs/acts21.html", "rumor", "the rumour to be dealt with is that paul teaches jews to forsake moses"),
    ("docs/colossians1.html", "labor", "his labour is described with a word drawn from athletic contest"),
    ("docs/esther10.html", "Honored", "Honoured by the empire and by his own people"),
    ("docs/esther3.html", "offense", "personal offence does"),
    ("docs/esther5.html", "honor", "empty an empire's worth of honour"),
    ("docs/esther6.html", "honor", "he proposes the most extravagant honour he can imagine"),
    ("docs/exodus39.html", "color", "the ephod's colour marks the difference in office"),
    ("docs/ezekiel13.html", "offense", "is the specific offence"),
    ("docs/ezekiel25.html", "neighbors", "something the neighbours said while jerusalem burned"),
    ("docs/ezekiel28.html", "offense", "no specific offence is named"),
    ("docs/ezekiel30.html", "behavior", "the annual behaviour of one river"),
    ("docs/ezra1.html", "favor", "persian policy did favour restoring displaced peoples"),
    ("docs/ezra5.html", "defense", "elders who name their fathers' sin as part of their defence"),
    ("docs/galatians1.html", "defense", "the immediate defence here signals"),
    ("docs/hosea13.html", "labor", "a labour that stops halfway kills both"),
    ("docs/hosea5.html", "neighbor", "committed at night against a neighbour who cannot prove it"),
    ("docs/hosea8.html", "offense", "the multiplication is itself the offence"),
    ("docs/isaiah10.html", "offense", "which is a distinct offence from the violence"),
    ("docs/isaiah15.html", "neighbor", "an oracle of judgment against a hostile neighbour"),
    ("docs/isaiah16.html", "neighbor", "a hostile neighbour is invited to shelter refugees"),
    ("docs/isaiah26.html", "defenses", "the defences named are not masonry"),
    ("docs/isaiah26.html", "Labor", "Labour with no birth at the end of it"),
    ("docs/isaiah3.html", "defense", "nine categories, covering defence, law, religion"),
    ("docs/isaiah36.html", "defenses", "looked like dismantling the defences"),
    ("docs/isaiah47.html", "offense", "which is the offence rather than the pride"),
    ("docs/isaiah62.html", "labor", "this time the labour is the people's own"),
    ("docs/jeremiah10.html", "neighbors", "the one sentence the exiles are handed to say to their neighbours is written"),
    ("docs/jeremiah10.html", "neighbors", "is written in the language the neighbours actually spoke"),
    ("docs/jeremiah13.html", "coloring", "it has become as fixed as colouring"),
    ("docs/jeremiah14.html", "defense", "being misled is not treated as a defence"),
    ("docs/jeremiah20.html", "offense", "the same offence as the peace-prophets of chapter 14"),
    ("docs/jeremiah24.html", "favor", "taking their survival as evidence of favour"),
    ("docs/jeremiah26.html", "Defense", "The Defence (vv.12-15)"),
    ("docs/jeremiah26.html", "defense", "The defence has three parts"),
    ("docs/jeremiah48.html", "offense", "a nation whose only offence in this section"),
    ("docs/jeremiah48.html", "neighbor", "forty-six verses of judgment on a hostile neighbour"),
    ("docs/jeremiah49.html", "neighbor's", "opportunism at a neighbour's funeral"),
    ("docs/jeremiah49.html", "offense", "the same offence edom is charged with"),
    ("docs/jeremiah9.html", "neighboring", "a list of neighbouring nations that also practised circumcision"),
    ("docs/joel3.html", "offense", "human trafficking is named as the offence"),
    ("docs/john10.html", "offense", "they take up stones and name the offence"),
    ("docs/john13.html", "honor", "a gesture of honour to the guest at a meal"),
    ("docs/john21.html", "rumor", "the gospel then corrects a rumour that had grown out of the reply"),
    ("docs/john4.html", "labor-saving", "which she hears as a labour-saving offer"),
    ("docs/john7.html", "defense", "it is not a defence of jesus so much as of due process"),
    ("docs/joshua16.html", "labor", "but put to forced labour"),
    ("docs/leviticus2.html", "labor", "grain as the fruit of human labour given back"),
    ("docs/leviticus20.html", "offenses", "grading offences rather than levelling them"),
    ("docs/leviticus20.html", "offenses", "fall on precisely the offences that confuse a family line"),
    ("docs/leviticus27.html", "labor", "amounts track what a person&#x27;s labour was worth"),
    ("docs/leviticus5.html", "offense", "keeping quiet is the offence"),
    ("docs/leviticus5.html", "defense", "remove ignorance as a defence entirely"),
    ("docs/malachi2.html", "offenses", "it is treated as two offences at once"),
    ("docs/matthew11.html", "behavior", "the objection was never about the behaviour"),
    ("docs/micah1.html", "neighbors", "these were micah's own neighbours"),
    ("docs/micah2.html", "offense", "the mechanism of the offence turned round"),
    ("docs/micah3.html", "offense", "the offence is not unbelief"),
    ("docs/nahum2.html", "defenses", "describe water breaching the defences"),
    ("docs/nehemiah10.html", "neighbors", "when neighbours bring wares"),
    ("docs/nehemiah5.html", "labor", "the unpaid labour of the wall itself"),
    ("docs/nehemiah9.html", "offense", "the point where the offence is worst"),
    ("docs/obadiah1.html", "neighbor", "occupied with judgment on one neighbour"),
    ("docs/obadiah1.html", "neighbor", "it ends by looking well past that neighbour"),
    ("docs/philemon1.html", "favor", "he is about to ask a favour"),
    ("docs/psalms101.html", "offenses", "the offences singled out are all"),
    ("docs/psalms101.html", "offenses", "are all offences of speech"),
    ("docs/psalms108.html", "neighbors", "to disposing of neighbours"),
    ("docs/psalms109.html", "defense", "standing where a defence counsel should be"),
    ("docs/psalms141.html", "favor", "calls a blow from the right person a favour"),
    ("docs/psalms40.html", "favor", "the rejection of sacrifice in favour of obedience"),
    ("docs/psalms82.html", "offense", "the offence is favouritism on the bench"),
    ("docs/psalms83.html", "neighbor", "which reads as every neighbour at once"),
    ("docs/psalms96.html", "splendor", "as worship in the splendour that holiness is"),
    ("docs/songofsolomon3.html", "splendor", "keeps the splendour from being weightless"),
]


def recase(matched, replacement):
    if matched[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


BRITISH = re.compile(
    r"\b(honour|neighbour|labour|favour|saviour|defence|offence|rumour|"
    r"valour|behaviour|splendour|humour|colour)(?:'s|s|ed|ing|hood)?\b", re.I)


def apply_fix(content, american, needle):
    idx = content.lower().find(needle.lower())
    if idx == -1:
        return content, False
    # search for the British word within this needle's span in the real content
    span = content[idx:idx + len(needle) + 20]
    m = BRITISH.search(span)
    if not m:
        return content, False
    matched = m.group(0)
    # american already carries any suffix (e.g. "neighbor's", "labor-saving");
    # only recase to match matched word's capitalisation.
    repl = recase(matched, american)
    new_span = span[:m.start()] + repl + span[m.end():]
    new_content = content[:idx] + new_span + content[idx + len(span):]
    return new_content, True


def main():
    check = "--check" in sys.argv
    by_file = {}
    for path, american, needle in FIXES:
        by_file.setdefault(path, []).append((american, needle))

    total = 0
    for path, fixes in sorted(by_file.items()):
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        changed = False
        for american, needle in fixes:
            new_content, ok = apply_fix(content, american, needle)
            if not ok:
                print(f"MISS: {path}: could not locate {needle!r}")
                continue
            content = new_content
            changed = True
            total += 1
        if changed and not check:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
        print(f"{path}: {'would fix' if check else 'fixed'} {len(fixes)}")
    print(f"\ntotal: {total} occurrences across {len(by_file)} files")


if __name__ == "__main__":
    main()
