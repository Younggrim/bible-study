#!/usr/bin/env python3
"""Add chapter-level Classification + Key Themes to a first batch of pages
missing them: Titus, 2 Peter, 2 Thessalonians, 2 Timothy, Colossians,
Philippians (chapters 2+, since chapter 1 of each already carries the pair).

Inserts the two new auth-items immediately before the first verse-range
section item (the first auth-label containing "(v"), matching that item's
indentation. Idempotent: skips a page that already has Key Themes.

    python3 add_key_themes_batch1.py            # apply
    python3 add_key_themes_batch1.py --check     # verify only, no write
"""
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

# (classification, key themes)
DATA = {
    "titus2": (
        "Epistle — Pauline, Pastoral Epistle",
        "Instruction sorted by age and household rather than delivered in general, "
        "sound doctrine judged by the life it produces, grace appearing as a teacher "
        "of self-control rather than only a rescue, a peculiar people purified and "
        "zealous of good works, and doctrine handed to one man to speak aloud where "
        "he could be despised for it",
    ),
    "titus3": (
        "Epistle — Pauline, Pastoral Epistle",
        "Obedience to pagan magistrates commanded rather than debated, a former life "
        "catalogued without excuse, salvation by mercy against a works clause it "
        "explicitly rules out, the Spirit poured out and renewal named as "
        "regeneration, and a letter that ends in errands and unfinished travel plans",
    ),
    "2peter2": (
        "Epistle — General",
        "False teachers named by their greed before their doctrine, three Old "
        "Testament judgments cited as one argument for a fourth, God shown rescuing "
        "and reserving in the same verse, wells without water and clouds without "
        "rain, and an end pronounced worse than a beginning never reached",
    ),
    "2peter3": (
        "Epistle — General",
        "Scoffers who turn a delay into their whole argument, a day with the Lord "
        "not counted the way a day is counted, patience read as the reason for "
        "waiting rather than proof against it, the heavens dissolving and the "
        "elements melting with fervent heat, and Paul's letters counted among the "
        "rest of scripture",
    ),
    "2thessalonians2": (
        "Epistle — Pauline",
        "A forged letter or claimed prophecy spreading panic that the Day had "
        "already come, a falling away and a man of sin required before it can "
        "arrive, something currently restraining what is not yet revealed, a "
        "strong delusion sent on those who refused to love the truth, and a people "
        "called and chosen set against those who perish",
    ),
    "2thessalonians3": (
        "Epistle — Pauline",
        "A prayer request for deliverance from unreasonable men before any command "
        "is given, idleness treated as a discipline problem rather than a doctrine "
        "problem, Paul's own labor offered as the standard rather than only the "
        "argument, a rule that ties eating to working, and withdrawal from a "
        "disorderly brother that stops short of treating him as an enemy",
    ),
    "2timothy2": (
        "Epistle — Pauline, Pastoral Epistle",
        "A chain of transmission carried through four generations, endurance "
        "argued from a soldier, an athlete and a farmer, a word of God that stays "
        "free even when the man who preaches it is chained, a workman who must "
        "rightly divide the word of truth, and a servant who corrects opponents "
        "gently in hope that God grants them repentance",
    ),
    "2timothy3": (
        "Epistle — Pauline, Pastoral Epistle",
        "Eighteen vices used to describe the last days rather than a distant "
        "future, a form of godliness that denies its own power, persecution "
        "promised to everyone who lives godly rather than reserved for the unusual "
        "case, scripture named as both the source of wisdom for salvation and the "
        "tool that equips for every good work, and Timothy's whole life held up as "
        "a witness Paul can appeal to",
    ),
    "2timothy4": (
        "Epistle — Pauline, Pastoral Epistle",
        "A charge delivered before God and Christ as if in a courtroom, itching "
        "ears preferred to sound doctrine, a life summarized in three perfect-tense "
        "verbs before the sentence is passed, a crown offered to everyone who loves "
        "Christ's appearing and not to Paul alone, and a list of deserters and "
        "companions closing a letter written by a man who expects to die",
    ),
    "colossians2": (
        "Epistle — Pauline, Prison Epistle",
        "Completeness in Christ argued against four distinct rivals in turn, "
        "philosophy named first among the threats, festivals and sabbaths called "
        "shadows of a substance already present, angel worship diagnosed as a loss "
        "of connection to the Head, and rules against touching and tasting shown to "
        "have no power against the flesh they claim to restrain",
    ),
    "colossians3": (
        "Epistle — Pauline, Prison Epistle",
        "A life already hidden with Christ in God before it is described, two "
        "catalogued lists of sins put off before any list of virtues is put on, "
        "love named above every other virtue rather than merely included among "
        "them, a household code applied to wives and husbands, children and "
        "fathers, servants and masters alike, and every relationship reframed as "
        "service done to the Lord rather than to a person",
    ),
    "colossians4": (
        "Epistle — Pauline, Prison Epistle",
        "A master's duty completing a household code rather than left as an "
        "afterthought, speech asked to be gracious and seasoned with salt toward "
        "outsiders, a network of named co-workers filling out the early church's "
        "map, Mark's restoration to fellowship despite the break of Acts 15, and "
        "Demas greeted here still present, not yet the deserter of the second "
        "letter to Timothy",
    ),
    "philippians2": (
        "Epistle — Pauline, Prison Epistle",
        "Unity appealed to on the ground of humility rather than agreement, a hymn "
        "tracing Christ from equality with God down to a cross and back up to the "
        "name above every name, salvation worked out rather than worked for, two "
        "men — Timothy and Epaphroditus — offered as living examples of the "
        "pattern the hymn describes, and Epaphroditus commended for an illness "
        "that nearly cost him his life in Paul's service",
    ),
    "philippians3": (
        "Epistle — Pauline, Prison Epistle",
        "Judaizers named dogs in a deliberate reversal of a slur, an impressive "
        "Jewish pedigree listed in full before being called refuse, righteousness "
        "sought as a gift received by faith rather than earned by the law, a race "
        "run by a man who insists he has not yet arrived, and citizenship claimed "
        "in heaven while the body still waits to be changed",
    ),
    "philippians4": (
        "Epistle — Pauline, Prison Epistle",
        "Two named women in conflict addressed by name rather than left "
        "anonymous, joy commanded rather than merely encouraged, anxiety answered "
        "with prayer and thanksgiving rather than argued away, contentment "
        "described as something learned rather than natural to Paul, and "
        "greetings closing from converts inside Caesar's own household",
    ),
}

ITEM = re.compile(
    r'( *)<div class="auth-item"><span class="auth-label">(.*?)</span>', re.S)


def esc(s):
    return H.escape(s, quote=True).replace("'", "&#x27;")


def process(book, classification, themes, check):
    path = os.path.join(DOCS, f"{book}.html")
    raw = open(path, encoding="utf-8").read()
    if 'auth-label">Key Themes:' in raw:
        return "already-has"

    m = None
    for cand in ITEM.finditer(raw):
        label = H.unescape(cand.group(2))
        if re.search(r"\(vv?\.\d", label):
            m = cand
            break
    if m is None:
        return "NO-SECTION-FOUND"

    indent = m.group(1)
    insert = (
        f'{indent}<div class="auth-item"><span class="auth-label">Classification:'
        f'</span> {esc(classification)}</div>\n'
        f'{indent}<div class="auth-item"><span class="auth-label">Key Themes:'
        f'</span> {esc(themes)}</div>\n'
    )
    new_raw = raw[: m.start()] + insert + raw[m.start():]

    if not check:
        open(path, "w", encoding="utf-8").write(new_raw)
    return "ok"


def main():
    check = "--check" in sys.argv
    bad = 0
    for book, (classification, themes) in DATA.items():
        status = process(book, classification, themes, check)
        print(f"{book}: {status}")
        if status not in ("ok", "already-has"):
            bad += 1
    print(f"\n{'checked' if check else 'wrote'} {len(DATA)} pages, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
