#!/usr/bin/env python3
"""Build docs/site/plans-data.js, the day-by-day chapter lists of the reading
plans, for docs/site/plans.js.

    python3 build_plans.py

Each plan is a list of days; each day a list of chapter pages ("john3").
The script checks that every plan reads each of its chapters exactly once
and, for the Bible in a year, that all 1189 chapters are covered.

The year plan is chronological at the level of whole chapters, which is what
the site's pages are. It follows the broad order most chronological plans
use: Job beside Genesis, the Psalms and wisdom books with David and Solomon,
the prophets beside the kings they spoke to, Ezra-Nehemiah-Esther after the
exile, and Paul's letters placed inside Acts where they were written. Where
scholars disagree on a date (Joel, Obadiah, some psalms), it takes a common
placement rather than claiming precision.
"""
import json
import os

BOOKS = [("genesis", 50), ("exodus", 40), ("leviticus", 27), ("numbers", 36), ("deuteronomy", 34), ("joshua", 24),
         ("judges", 21), ("ruth", 4), ("1samuel", 31), ("2samuel", 24), ("1kings", 22), ("2kings", 25),
         ("1chronicles", 29), ("2chronicles", 36), ("ezra", 10), ("nehemiah", 13), ("esther", 10), ("job", 42),
         ("psalms", 150), ("proverbs", 31), ("ecclesiastes", 12), ("songofsolomon", 8), ("isaiah", 66),
         ("jeremiah", 52), ("lamentations", 5), ("ezekiel", 48), ("daniel", 12), ("hosea", 14), ("joel", 3),
         ("amos", 9), ("obadiah", 1), ("jonah", 4), ("micah", 7), ("nahum", 3), ("habakkuk", 3), ("zephaniah", 3),
         ("haggai", 2), ("zechariah", 14), ("malachi", 4), ("matthew", 28), ("mark", 16), ("luke", 24), ("john", 21),
         ("acts", 28), ("romans", 16), ("1corinthians", 16), ("2corinthians", 13), ("galatians", 6), ("ephesians", 6),
         ("philippians", 4), ("colossians", 4), ("1thessalonians", 5), ("2thessalonians", 3), ("1timothy", 6),
         ("2timothy", 4), ("titus", 3), ("philemon", 1), ("hebrews", 13), ("james", 5), ("1peter", 5), ("2peter", 3),
         ("1john", 5), ("2john", 1), ("3john", 1), ("jude", 1), ("revelation", 22)]
N = dict(BOOKS)


def ch(book, a=1, b=None):
    return [f"{book}{c}" for c in range(a, (b or N[book]) + 1)]


def split(chapters, days):
    """Spread chapters over a number of days as evenly as possible, in order."""
    out, n = [], len(chapters)
    for d in range(days):
        out.append(chapters[n * d // days: n * (d + 1) // days])
    return out


def nt():
    return [p for b, _ in BOOKS[39:] for p in ch(b)]


def chronological():
    seq = []
    add = lambda *parts: [seq.extend(x) for x in parts]
    # Beginnings and the patriarchs
    add(ch("genesis", 1, 11), ch("job"), ch("genesis", 12, 50))
    # Exodus to the edge of the promised land
    add(ch("exodus"), ch("leviticus"), ch("numbers"), ch("deuteronomy"), ch("psalms", 90, 90))
    # The land and the judges
    add(ch("joshua"), ch("judges"), ch("ruth"))
    # Samuel, Saul and David, with the Psalms of David's life and the Chronicler's account
    add(ch("1samuel"), ch("2samuel"), ch("1chronicles"),
        ch("psalms", 1, 41), ch("psalms", 42, 72), ch("psalms", 73, 89))
    # Solomon and his writings
    add(ch("1kings", 1, 11), ch("2chronicles", 1, 9), ch("proverbs"), ch("songofsolomon"), ch("ecclesiastes"))
    # The divided kingdom and the prophets sent to it
    add(ch("1kings", 12, 22), ch("2kings", 1, 14), ch("2chronicles", 10, 25),
        ch("obadiah"), ch("joel"), ch("jonah"), ch("amos"), ch("hosea"),
        ch("2kings", 15, 17), ch("2chronicles", 26, 28), ch("micah"), ch("isaiah"),
        ch("2kings", 18, 25), ch("2chronicles", 29, 36), ch("nahum"), ch("zephaniah"), ch("habakkuk"))
    # Exile
    add(ch("jeremiah"), ch("lamentations"), ch("ezekiel"), ch("daniel"))
    # Return and rebuilding, and the rest of the Psalms
    add(ch("psalms", 91, 150), ch("ezra", 1, 6), ch("haggai"), ch("zechariah"), ch("esther"),
        ch("ezra", 7, 10), ch("nehemiah"), ch("malachi"))
    # The Gospels
    add(ch("luke", 1, 2), ch("john", 1, 1), ch("matthew"), ch("mark"), ch("luke", 3, 24), ch("john", 2, 21))
    # The church, with each letter where it was written
    add(ch("acts", 1, 14), ch("james"), ch("galatians"), ch("acts", 15, 18), ch("1thessalonians"), ch("2thessalonians"),
        ch("acts", 19, 19), ch("1corinthians"), ch("2corinthians"), ch("romans"), ch("acts", 20, 28),
        ch("ephesians"), ch("philippians"), ch("colossians"), ch("philemon"),
        ch("1timothy"), ch("titus"), ch("1peter"), ch("hebrews"), ch("2timothy"), ch("2peter"), ch("jude"),
        ch("1john"), ch("2john"), ch("3john"), ch("revelation"))
    return seq


def psalms_proverbs():
    days, ps = [], ch("psalms")
    for d in range(30):
        days.append(ps[d * 5:(d + 1) * 5] + [f"proverbs{d + 1}"])
    days[-1].append("proverbs31")
    return days


def advent():
    """Dec 1-25: the promise of the Messiah through the Old Testament, then his coming.
    One chapter a day, ending with the birth on Christmas Day."""
    return [[p] for p in [
        "genesis3", "genesis12", "genesis49", "numbers24", "deuteronomy18", "2samuel7", "psalms2", "psalms110",
        "isaiah7", "isaiah9", "isaiah11", "isaiah40", "isaiah53", "jeremiah23", "micah5", "malachi3", "isaiah61",
        "luke1", "matthew1", "john1", "galatians4", "philippians2", "hebrews1", "matthew2", "luke2"]]


def new_believer():
    """A first month: Mark's Gospel, then what the good news means (Romans,
    Ephesians), a few psalms to pray, and 1 John on living it."""
    return [[p] for p in ch("mark") + [
        "psalms23", "romans3", "romans5", "ephesians2", "romans8", "psalms51", "romans12", "psalms139", "psalms1"]
        + ch("1john")]


def holy_week():
    """Palm Sunday to Easter Sunday, a day of readings for each day of the week."""
    return [
        ["matthew21"],                          # Sunday: the entry into Jerusalem
        ["mark11"],                             # Monday: the temple cleared
        ["matthew23", "matthew24"],             # Tuesday: teaching in the temple and on the Mount of Olives
        ["matthew26"],                          # Wednesday: anointed at Bethany; Judas agrees to betray him
        ["john13", "john14", "john17"],         # Thursday: the upper room
        ["isaiah53", "mark15", "john19"],       # Friday: the cross
        ["matthew27"],                          # Saturday: the tomb sealed and guarded
        ["luke24", "john20"],                   # Sunday: he is risen
    ]


PAUL = ["romans", "1corinthians", "2corinthians", "galatians", "ephesians", "philippians", "colossians",
        "1thessalonians", "2thessalonians", "1timothy", "2timothy", "titus", "philemon"]

PLANS = [
    ("john-21", "Gospel of John in 21 days", [[p] for p in ch("john")]),
    ("nt-90", "New Testament in 90 days", split(nt(), 90)),
    ("psalms-proverbs-30", "Psalms and Proverbs in 30 days", psalms_proverbs()),
    ("bible-year", "Bible in a year (chronological)", split(chronological(), 365)),
    ("gospels-40", "Life of Jesus: the four Gospels in 40 days",
     split(ch("matthew") + ch("mark") + ch("luke") + ch("john"), 40)),
    ("new-believer-30", "New believer: your first 30 days", new_believer()),
    ("acts-28", "Acts: the early church in 28 days", [[p] for p in ch("acts")]),
    ("paul-30", "Paul's letters in 30 days", split([p for b in PAUL for p in ch(b)], 30)),
    ("genesis-50", "Genesis in 50 days", [[p] for p in ch("genesis")]),
    ("proverbs-31", "Proverbs in a month", [[p] for p in ch("proverbs")]),
    ("advent-25", "Advent: 25 days to Christmas (start Dec 1)", advent()),
    ("holy-week-8", "Easter: Holy Week in 8 days (start Palm Sunday)", holy_week()),
]


def main():
    every = {p for b, _ in BOOKS for p in ch(b)}
    out = []
    for pid, name, days in PLANS:
        flat = [p for d in days for p in d]
        assert len(flat) == len(set(flat)), f"{pid}: a chapter is read twice"
        assert set(flat) <= every, f"{pid}: unknown chapter"
        assert all(days), f"{pid}: an empty day"
        out.append({"id": pid, "name": name, "days": days})
        print(f"{pid}: {len(days)} days, {len(flat)} chapters")
    days = {p["id"]: len(p["days"]) for p in out}
    assert days["advent-25"] == 25 and days["new-believer-30"] == 30 and days["holy-week-8"] == 8 and days["paul-30"] == 30
    assert len({p["id"] for p in out}) == len(out), "plan ids must be unique"
    year = next(p for p in out if p["id"] == "bible-year")
    assert {p for d in year["days"] for p in d} == every, "bible-year must cover every chapter"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "site", "plans-data.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write("/* Written by build_plans.py; do not edit by hand. */\nwindow.BIBLE_PLANS = ")
        json.dump(out, f, separators=(",", ":"))
        f.write(";\n")
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
