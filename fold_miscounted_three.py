#!/usr/bin/env python3
"""
Folds the three chapters that were being counted as done and never were:
lamentations4, ezekiel24 and daniel9.

Each carries a field whose label is a sentence fragment that happens to contain a
parenthesised verse range:

    Daniel's prayer (vv.4-19) is entirely about GOD:
    The boiling pot parable (vv.3-14) echoes Ezekiel 11:
    The comparison to Sodom (v.6) is devastating:

The progress query matched "any label containing a verse range", so these three
registered as folded. A real section heading ends with its range -- "Seventy Weeks
(vv.24-27):" -- and these have prose after it. Retested strictly, the true totals
are 644 of 1189 rather than 647, and 47 complete books rather than 48. Lamentations
was the book wrongly called complete, and this batch genuinely finishes it.

All three fragment fields hold real content, folded into the section covering the
same verses: the Sodom comparison turning on duration rather than severity, the
boiling pot inverting the leaders' own metaphor from Ezekiel 11:3, and Daniel's
prayer containing no self-justification.

Caps normalised in the preserved fields: INSTANTLY, PROLONGED, PRAYED. GOD is left
alone -- it is the divine name, already on the allow-list.

lamentations4's inherited skeleton skipped v.12 between v.11 and vv.13-16. Closed.

Usage:
    python3 fold_miscounted_three.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"lamentations4": 22, "ezekiel24": 27, "daniel9": 27}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

DROP = {
    "lamentations4": ["The comparison to Sodom (v.6) is devastating:"],
    "ezekiel24": ["The boiling pot parable (vv.3-14) echoes Ezekiel 11:"],
    "daniel9": ["Daniel&#x27;s prayer (vv.4-19) is entirely about GOD:"],
}

NORMALISE = {"INSTANTLY": "instantly", "PROLONGED": "prolonged",
             "PRAYED": "prayed"}

SECTIONS = {
"lamentations4": [
  ("The Gold Grown Dim (vv.1-2)",
   "The chapter opens on devaluation rather than destruction: the gold become dim, the "
   "most fine gold changed, the stones of the sanctuary poured out in the streets. Then "
   "the same movement applied to people -- the precious sons of Zion, once comparable "
   "to fine gold, now esteemed as earthen pitchers. Nothing has been annihilated. "
   "Everything has been reduced in worth, which is the particular grief this chapter "
   "works in."),
  ("Children Starving; Mothers Worse Than Jackals (vv.3-6)",
   "Even the sea monsters give suck to their young, but the daughter of the people has "
   "become cruel. The comparison is deliberately to animals, and the people come out "
   "worse. Infants ask for bread and no one breaks it to them. Verse 6 makes the "
   "comparison the chapter is remembered for: the punishment is greater than the sin of "
   "Sodom. What makes it greater is duration rather than severity -- Sodom was "
   "destroyed in a moment, while Jerusalem endured eighteen months of siege and slow "
   "starvation. Quick destruction is treated here as the mercy."),
  ("The Nazarites: From Rubies to Coal (vv.7-8)",
   "Those set apart by vow, once described as purer than snow and more ruddy than "
   "rubies, are now blacker than coal and unrecognisable in the streets. Their skin "
   "cleaves to their bones. The point of choosing the Nazarites for this contrast is "
   "that they were the visibly consecrated, so the degradation reaches the people who "
   "had most publicly belonged to God."),
  ("Better Slain by the Sword Than by Famine (vv.9-12)",
   "The judgement is stated flatly: they that be slain with the sword are better than "
   "they that be slain with hunger. What follows in v.10 is the detail the book will "
   "not look away from, women cooking their own children. Verse 11 attributes it "
   "without softening -- the LORD hath accomplished his fury -- and v.12 records that "
   "no king or inhabitant of the world had believed an adversary could enter the gates "
   "of Jerusalem. The city's reputation for impregnability is part of what fell."),
  ("Prophets and Priests: Blood in the Streets (vv.13-18)",
   "The cause is named: for the sins of her prophets and the iniquities of her priests, "
   "who shed the blood of the just. They wander as blind men, polluted with blood, and "
   "are told to depart as unclean -- the leaders treated as lepers. The nations say "
   "they shall no more sojourn there. Verses 17-18 record eyes failing while watching "
   "for a help that never came, which is a reference to the Egyptian alliance the "
   "prophets had condemned."),
  ("The Anointed Taken, and Edom's Turn (vv.19-22)",
   "The pursuers were swifter than eagles, and \u201cthe breath of our nostrils, the "
   "anointed of the LORD\u201d was taken in their pits -- Zedekiah, caught fleeing "
   "through the walls at night, his sons killed in front of him before his eyes were "
   "put out. The royal language makes the capture theological rather than merely "
   "political. The chapter then turns to Edom, told to rejoice while it lasts, and "
   "closes with the one hopeful clause in it: the punishment of Zion's iniquity is "
   "accomplished."),
],
"ezekiel24": [
  ("The Date the Siege Began (vv.1-2)",
   "The chapter is dated to the day: the ninth year, tenth month, tenth day, which is "
   "15 January 588 BC. That is the exact day Nebuchadnezzar's army closed on Jerusalem, "
   "as 2 Kings 25:1 and Jeremiah 39:1 independently record. Ezekiel is in Babylon, "
   "hundreds of miles away, and is told to write the date down. The point of the "
   "instruction is verification later, when news finally travels."),
  ("The Boiling Pot, Corroded Beyond Cleaning (vv.3-14)",
   "The parable takes an image the Jerusalem leaders had used of themselves. In Ezekiel "
   "11:3 they called themselves the flesh in the pot, meaning protected. Here the "
   "metaphor is turned round: the pot is boiling, the choice pieces are being cooked, "
   "and the scum or rust on it will not come off. So the vessel is set empty on the "
   "coals until it burns, because the corrosion cannot be scoured out. The judgement is "
   "described as cleansing that failed and therefore became destruction."),
  ("The Desire of Thine Eyes (vv.15-18)",
   "The most personally costly sign-act in Scripture. God tells Ezekiel that his wife, "
   "\u201cthe desire of thine eyes\u201d, will die, and forbids the mourning that "
   "custom and decency required: no weeping aloud, no removing the turban, no covering "
   "the lip. Verse 18 reports it in one sentence -- I spake unto the people in the "
   "morning, and at even my wife died, and I did in the morning as I was commanded. The "
   "brevity is the effect."),
  ("Forbidden Mourning as Prophecy (vv.19-24)",
   "The people ask what it means, which is what the sign was for. The answer is that "
   "they will lose the sanctuary, \u201cthe desire of your eyes\u201d, and their sons "
   "and daughters, and will not mourn either -- struck too numb for ritual. Ezekiel's "
   "silent grief is a rehearsal of theirs. Making a prophet's bereavement into a public "
   "sign is the hardest thing God asks of anyone in the book."),
  ("When the News Comes, Thou Shalt Speak (vv.25-27)",
   "The chapter closes with a promise about Ezekiel's own voice. He has been under "
   "restraint since chapter 3, and when a fugitive arrives with word that the city has "
   "fallen, his mouth will be opened and he will no longer be dumb. That happens at "
   "33:21-22, some two years later. So the siege's beginning and the prophet's release "
   "are tied together from the outset."),
],
"daniel9": [
  ("Daniel Reads Jeremiah (vv.1-3)",
   "In the first year of Darius, the year Babylon fell, Daniel is reading Jeremiah's "
   "seventy-year prophecy at 25:11-12 and 29:10. Sixty-six years had passed, so "
   "restoration was close. What he does with that is the point: rather than wait, he "
   "sets himself to pray with fasting and sackcloth. The promise fuels the prayer "
   "instead of removing the need for it. He is roughly eighty-two years old."),
  ("Confession: We Have Sinned (vv.4-14)",
   "The prayer is almost entirely about God -- His greatness, faithfulness, covenant, "
   "righteousness and mercy -- and contains no self-justification anywhere. Daniel says "
   "\u201cwe have sinned\u201d throughout, including himself in a confession he had no "
   "personal need of, since chapter 6 shows his enemies could find no fault in him. He "
   "identifies with his people rather than distinguishing himself from them, which is "
   "what makes the prayer a model rather than a performance."),
  ("The Plea: For Thine Own Sake (vv.15-19)",
   "The petition when it comes rests on nothing in the petitioners: we do not present "
   "our supplications before thee for our righteousnesses, but for thy great mercies. "
   "The reason given for God to act is His own reputation -- thy city and thy people "
   "are called by thy name. Verse 19's short imperatives, hear, forgive, hearken and "
   "do, are the most urgent lines in the book."),
  ("Gabriel: Greatly Beloved (vv.20-23)",
   "The answer arrives while he is still speaking, and Gabriel says the commandment "
   "came forth at the beginning of the supplications. The prayer was answered before it "
   "finished. \u201cThou art greatly beloved\u201d is said to a man who has just spent "
   "sixteen verses confessing, which is worth noticing about how the chapter "
   "understands confession."),
  ("Seventy Weeks (vv.24-27)",
   "Four verses that have generated more interpretation than almost anything else in "
   "the Old Testament. Seventy sevens are decreed, with six stated purposes including "
   "to finish transgression and to bring in everlasting righteousness. The periods are "
   "divided seven, sixty-two and one, with an anointed one cut off after the "
   "sixty-ninth and a prince whose people destroy the city and the sanctuary. Whether "
   "the weeks run consecutively, where the starting decree falls, and whether the final "
   "week is future are all genuinely disputed, and the chapter does not settle them."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        want_drop = DROP[page]
        fields, dropped, extra = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None and rest == "Structure:":
                pass
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")
        notes.append(f"{page}: fragment label {dropped[0][:44]!r} folded into prose")

        for want in KEEP:
            for bad, good in NORMALISE.items():
                if re.search(rf"\b{bad}\b", fields[want]):
                    fields[want] = re.sub(rf"\b{bad}\b", good, fields[want])
                    notes.append(f"{page}: {want} {bad}->{good}")

        sections = SECTIONS[page]
        covered = set()
        for want in KEEP:
            stray = sorted({w for w in CAPS.findall(fields[want]) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} still in {want}")
        for head, body in sections:
            stray = sorted({w for w in CAPS.findall(body) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {head!r}")
            if "*" in body:
                problems.append(f"{page}: markdown asterisk in {head!r}")
            # a heading must END with its range, which is what the loose query missed
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for want in KEEP:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if "auth-sublist" in new:
            problems.append(f"{page}: sublist survived")
            continue
        planned[path] = new

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
