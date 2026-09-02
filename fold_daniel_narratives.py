#!/usr/bin/env python3
"""
Folds Daniel 1 to 6, the narrative half of the book. Chapters 7 to 12 follow.

The split is the book's own: 1-6 are third-person court narratives, 7-12 are
first-person visions. It also roughly follows the language seam, since 2:4b-7:28 is
Aramaic and the rest Hebrew.

An overlap inherited from the skeleton, fixed. daniel4 listed both "The fulfillment
(vv.28-33)" and "Seven Years of Madness (v.33)", so v.33 belonged to two sections.
Merged into vv.28-33. This is the second overlapping skeleton after Lamentations 3,
and the guard added there caught it.

Capitals. STONE, THREE and EVERY are normalised, being ordinary words set for
emphasis. MENE, TEKEL and UPHARSIN are kept -- they are the transliterated Aramaic
of the writing on the wall, and daniel5's own section heading needs them. That makes
a fourth protected case after PE and AYIN, I AM, and Jeroboam II.

Usage:
    python3 fold_daniel_narratives.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"daniel1": 21, "daniel2": 49, "daniel3": 30, "daniel4": 37,
          "daniel5": 31, "daniel6": 28}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "MENE", "TEKEL", "UPHARSIN"}

KEEP = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

DROP = {
    "daniel1": ["God&#x27;s sovereignty frames the entire chapter:"],
    "daniel4": ["The chapter is structured as ancient testimony:"],
}

NORMALISE = {"STONE": "stone", "THREE": "three", "EVERY": "every"}

SECTIONS = {
"daniel1": [
  ("Babylon Takes Jerusalem, and the Vessels (vv.1-2)",
   "In 605 BC Nebuchadnezzar beat Pharaoh Necho at Carchemish and turned south. This "
   "was the first of three deportations, and rather than sack the city he took hostages "
   "-- the ablest young nobles -- to secure Judah's compliance and absorb its talent. "
   "The chapter's theology is set in v.2 before any of it: the Lord gave Jehoiakim into "
   "his hand. Even the exile is attributed to God rather than to Babylonian arms."),
  ("Selection and Re-education (vv.3-7)",
   "The programme is three years of Chaldean language, literature and custom, and the "
   "selection criteria are physical and intellectual. The renaming is the sharpest "
   "detail: names referring to the God of Israel are replaced with names referring to "
   "Babylonian gods. Daniel, meaning God is my judge, becomes Belteshazzar, meaning Bel "
   "protect his life. The aim is not education but the replacement of an identity."),
  ("Daniel Purposed in His Heart (vv.8-16)",
   "The refusal is limited and deliberate. Daniel does not object to the language, the "
   "literature or the service, only to the food and wine, which had been offered to "
   "idols. He asks rather than defies, and proposes a ten-day test with a fallback. "
   "Verse 9 credits the outcome to God bringing him into favour with his keeper, so the "
   "sovereignty of v.2 is shown working inside the exile as well as bringing it about."),
  ("Ten Times Better (vv.17-21)",
   "God gives the four knowledge and skill in all learning, and Daniel understanding in "
   "visions and dreams -- the ability that shapes the rest of the book. Examined by the "
   "king they are found ten times better than all the magicians in his realm. The last "
   "verse jumps to the first year of Cyrus, so the chapter closes by noting that Daniel "
   "outlasted the empire that captured him."),
],
"daniel2": [
  ("The King's Impossible Demand (vv.1-13)",
   "Nebuchadnezzar's dream comes in his second year, at the height of Babylon's power, "
   "and his demand is unprecedented: tell me the dream and its interpretation, without "
   "being told the dream. The logic is a test of the trade -- anyone with genuine access "
   "to the gods should not need the content supplied. The wise men's protest that no "
   "king has ever asked such a thing is an admission, and the sentence is death for all "
   "of them, Daniel included."),
  ("Daniel Asks for Time, and for Prayer (vv.14-18)",
   "Daniel answers the captain of the guard with counsel and wisdom, asks the king for "
   "time, and then does the thing the chapter turns on: he goes to his three friends and "
   "asks them to seek mercies of God concerning this secret. The response to a death "
   "sentence is a prayer meeting. Nothing in the passage suggests he expected the answer "
   "to come any other way."),
  ("Blessed Be the Name of God For Ever (vv.19-23)",
   "The secret is revealed in a night vision, and Daniel's first act is not to go to the "
   "king but to bless God. The prayer names what the dream will illustrate: he changes "
   "the times and the seasons, he removes kings and sets up kings, he gives wisdom and "
   "reveals the deep and secret things. The theology of the whole book is stated here in "
   "four verses, before the political content arrives."),
  ("There Is a God in Heaven (vv.24-30)",
   "Brought before the king, Daniel begins by clearing the ground: the secret cannot be "
   "revealed by the wise men, the astrologers or the soothsayers. But there is a God in "
   "heaven that revealeth secrets. Verse 30 goes further and disclaims himself -- not "
   "for any wisdom that I have more than any living. The credit is refused twice before "
   "the interpretation is given."),
  ("The Image of Gold, Silver, Brass, Iron (vv.31-35)",
   "The dream is described before it is explained: a great image, head of fine gold, "
   "breast and arms of silver, belly and thighs of brass, legs of iron, feet part iron "
   "and part clay. Then a stone cut out without hands strikes the feet, and the whole "
   "thing becomes chaff the wind carries away. The stone grows into a mountain filling "
   "the earth. The descending value of the metals and the ascending strength are working "
   "against each other, which is part of the point."),
  ("The Interpretation: Four Kingdoms (vv.36-45)",
   "Only the first kingdom is named outright: thou art this head of gold. The others are "
   "described rather than identified, which is why the identifications, commonly "
   "Medo-Persia, Greece and Rome, are interpretation rather than text. The iron mixed "
   "with clay is explained as a kingdom partly strong and partly broken. What the passage "
   "does state plainly is the ending: the God of heaven shall set up a kingdom which "
   "shall never be destroyed, and the stone was cut without hands."),
  ("Nebuchadnezzar Falls on His Face (vv.46-49)",
   "The reaction is extraordinary and ambiguous. The most powerful man alive falls on "
   "his face before a captive and orders an offering made to him, then confesses that "
   "Daniel's God is a God of gods. Whether this is conversion or the addition of one "
   "more god to a crowded pantheon is left open, and chapter 3 suggests the latter. "
   "Daniel is promoted, and asks that his three friends be placed as well."),
],
"daniel3": [
  ("The Image on the Plain of Dura (vv.1-7)",
   "The image is gold throughout, which reads as an answer to chapter 2. Told his "
   "kingdom was the head of gold and would be succeeded, Nebuchadnezzar builds a statue "
   "with no silver, brass or iron in it. The dimensions, sixty cubits by six, and the "
   "sixfold list of officials and instruments give the ceremony a deliberate rhythm. "
   "Attendance is compulsory and the penalty is stated before anyone refuses."),
  ("Certain Jews Accused (vv.8-12)",
   "The accusation is made by Chaldeans and is carefully framed: these men whom thou "
   "hast set over the affairs of Babylon. Resentment at foreigners holding office is "
   "doing as much work as religious zeal. Daniel is not among the accused and the "
   "chapter never says why -- he may have been away on state business or exempt by "
   "rank. The focus stays on the three."),
  ("Who Is That God? (vv.13-15)",
   "The king offers a second chance, which is more dangerous than the threat. Then the "
   "question that the rest of the chapter answers: who is that God that shall deliver "
   "you out of my hands? Asked by a man who had confessed a God of gods one chapter "
   "earlier, it shows how little that confession had settled."),
  ("But If Not (vv.16-18)",
   "The reply is the high point of the book's narrative half, and its force is in the "
   "second half rather than the first. Our God is able to deliver us, and he will "
   "deliver us -- and but if not, be it known unto thee that we will not serve thy gods. "
   "The obedience is detached from the outcome. They are not predicting rescue; they are "
   "saying rescue is not the condition of their obedience."),
  ("Seven Times Hotter, and a Fourth in the Fire (vv.19-25)",
   "The furnace was probably a brick kiln, common in Babylonian industry, and seven "
   "times hotter is idiom for maximum rather than a measurement. The detail that "
   "establishes the miracle is administrative: the soldiers who carried them up were "
   "killed by the heat, while the bound men inside were unharmed. Then the king counts "
   "four figures walking loose, and the fourth is like the Son of God."),
  ("Not a Hair Singed; the King's Decree (vv.26-30)",
   "The inspection is thorough and slightly comic: the officials gather to confirm that "
   "the fire had no power, not a hair singed, coats unchanged, no smell of smoke. "
   "Nebuchadnezzar's decree that follows protects the God of these three men from insult, "
   "which is progress of a kind, though it is still a king legislating about a God rather "
   "than submitting to one. The three are promoted."),
],
"daniel4": [
  ("Nebuchadnezzar's Proclamation (vv.1-4)",
   "The chapter is written as a royal testimony addressed to all people, nations and "
   "languages, and it is one of the few passages in Scripture composed by a Gentile "
   "king. It opens at the end of the story, with the signs and wonders already "
   "acknowledged, then goes back to the beginning: I was at rest in mine house and "
   "flourishing in my palace. The structure is life before the humbling, the warning, "
   "the interpretation, the fulfilment, and the restoration."),
  ("The Dream of the Tree (vv.5-18)",
   "The dream is a great tree, its height reaching to heaven and its shade sheltering "
   "beasts and birds, and then a watcher orders it cut down, leaving the stump bound "
   "with iron and brass. The language shifts mid-dream from a tree to a person -- let "
   "him be wet with the dew, let his portion be with the beasts, and seven times pass "
   "over him. The stated purpose in v.17 is that the living may know that the most High "
   "ruleth in the kingdom of men."),
  ("Daniel's Reluctant Interpretation (vv.19-27)",
   "Daniel is astonished and silent for an hour, and his opening line is unusual for a "
   "prophet: my lord, let the dream trouble thee not. He does not enjoy this. The "
   "interpretation is plain -- the tree is the king, and he will be driven from men to "
   "eat grass like oxen until he knows who rules. Verse 27 is the part often missed: "
   "Daniel offers a way out, break off thy sins, show mercy to the poor, it may be the "
   "sentence is lengthened."),
  ("Twelve Months Later: Is Not This Great Babylon? (vv.28-33)",
   "A year passes with nothing happening, which is the interval the counsel of v.27 was "
   "given for. Then the boast, walking on the palace roof: is not this great Babylon "
   "that I have built by the might of my power and for the honour of my majesty? The "
   "achievement was real -- the Ishtar Gate, the terraced gardens, walls broad enough "
   "to drive on. The sentence falls while the words are still in his mouth, and the "
   "condition described, believing oneself an animal, matches what is now called "
   "boanthropy. Babylonian building inscriptions have a gap in his later reign."),
  ("I Lifted Up Mine Eyes unto Heaven (vv.34-37)",
   "Reason returns at the end of the days, and the act that marks it is looking up. What "
   "follows is doxology from the man who had claimed the credit: his dominion is an "
   "everlasting dominion, he doeth according to his will in the army of heaven, none can "
   "stay his hand or say unto him what doest thou. The kingdom is restored with more "
   "added. The final clause is the lesson stated by the one who learned it: those that "
   "walk in pride he is able to abase."),
],
"daniel5": [
  ("Belshazzar's Feast and the Holy Vessels (vv.1-4)",
   "Belshazzar was Nebuchadnezzar's grandson through Nabonidus, and the Aramaic word "
   "rendered father means predecessor. Cuneiform records confirm him as co-regent while "
   "Nabonidus was absent. The feast for a thousand lords is held on 12 October 539 BC "
   "with a Persian army already outside the walls, which is the first measure of his "
   "confidence. Calling for the vessels taken from the temple in Jerusalem and drinking "
   "from them while praising gods of gold and silver is the second, and it is deliberate "
   "blasphemy rather than carelessness."),
  ("The Handwriting on the Wall (vv.5-9)",
   "A hand appears and writes on the plaster opposite the lampstand, so the whole room "
   "sees it. The king's reaction is physical -- his countenance changed, his thoughts "
   "troubled, the joints of his loins loosed, his knees smote one against another. The "
   "wise men are summoned with the usual rewards offered and can read nothing, which "
   "repeats chapter 2's failure a generation later."),
  ("The Queen Mother Remembers Daniel (vv.10-12)",
   "Daniel had been forgotten by the new court and has to be recalled by the queen "
   "mother, who remembers his reputation from Nebuchadnezzar's day. Sixty years of "
   "service and a court that does not know his name. Her description is precise -- an "
   "excellent spirit, knowledge and understanding, interpreting dreams and dissolving "
   "doubts -- so somebody had kept the memory even if the king had not."),
  ("Daniel Refuses the Rewards (vv.13-17)",
   "The king offers the scarlet, the gold chain and the third place in the kingdom, and "
   "Daniel declines before speaking: let thy gifts be to thyself. Refusing payment "
   "first is what makes the next section possible. He is not delivering a verdict he was "
   "paid to soften, and he says he will read the writing anyway."),
  ("Thou Knewest All This (vv.18-24)",
   "The interpretation is preceded by a history lesson. Daniel recounts what happened "
   "to Nebuchadnezzar -- greatness given, pride, the humbling, the restoration -- and "
   "then lands it: thou his son hast not humbled thine heart, though thou knewest all "
   "this. The charge is not ignorance but disregard of a precedent inside his own "
   "family, and lifting himself against the Lord of heaven."),
  ("MENE, MENE, TEKEL, UPHARSIN (vv.25-31)",
   "The words are weights and measures, which is part of why the wise men could read the "
   "letters and make nothing of them. Daniel reads them as verdicts: numbered, weighed, "
   "divided. Thy kingdom is divided and given to the Medes and Persians. Belshazzar keeps "
   "his word and clothes Daniel in scarlet, and the chapter ends in one sentence -- that "
   "night he was slain, and Darius took the kingdom. Cyrus's general had diverted the "
   "Euphrates and walked troops in along the dry riverbed."),
],
"daniel6": [
  ("First of the Three Presidents (vv.1-3)",
   "The Medo-Persian reorganisation puts a hundred and twenty princes under three "
   "presidents, and Daniel is first of the three because an excellent spirit was in him. "
   "He is a foreigner and by now an old man, set over natives. The chapter states the "
   "motive of what follows without needing to editorialise: the king thought to set him "
   "over the whole realm."),
  ("No Fault, Except Concerning His God (vv.4-9)",
   "The conspirators' own admission is the highest compliment in the book: they sought "
   "occasion against Daniel concerning the kingdom and could find none, because he was "
   "faithful and there was no error or fault in him. Sixty years of public office with "
   "nothing to use. So they legislate against the one thing he will not stop doing, and "
   "flatter the king into a thirty-day decree. The law of the Medes and Persians could "
   "not be revoked once signed, which traps two men rather than one."),
  ("He Prayed as He Did Aforetime (vv.10-13)",
   "Daniel's response is to change nothing. Windows open toward Jerusalem, following "
   "Solomon's prayer at the temple dedication, three times a day as before. He does not "
   "increase it in defiance or reduce it in prudence. The phrase \u201cas he did "
   "aforetime\u201d is the whole point: the consistency that made him a target is the "
   "same consistency that vindicates him. The conspirators find him praying, which they "
   "had every reason to expect."),
  ("The King Trapped by His Own Law (vv.14-18)",
   "Darius is sore displeased with himself and labours till sundown to find a way out, "
   "which tells you the decree was never really about Daniel for him. His parting words "
   "at the den, thy God whom thou servest continually will deliver thee, are hope rather "
   "than faith. The stone, the seal and the sleepless night close the section, and the "
   "king fasts while the prophet is in the den."),
  ("Is Thy God Able to Deliver Thee? (vv.19-24)",
   "Darius comes at dawn and calls with a lamentable voice, and the question he asks is "
   "the chapter's counterpart to chapter 3's -- there a king asked who could deliver, "
   "here one asks whether Daniel's God was able. The answer comes from inside the den. "
   "Daniel's explanation is innocence before God and before the king, so the deliverance "
   "is presented as vindication rather than rescue. What happens to the accusers is "
   "reported without comment."),
  ("Darius Writes to All Peoples (vv.25-28)",
   "The decree that follows is the third such proclamation in six chapters, after "
   "Nebuchadnezzar's two, and it goes furthest: the God of Daniel is the living God, "
   "steadfast for ever, whose kingdom shall not be destroyed. Pagan kings keep ending up "
   "as the ones who state the book's theme. The narrative half closes with Daniel "
   "prospering into the reign of Cyrus, having outlasted every ruler who tried to own "
   "him."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[6:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        want_drop = DROP.get(page, [])
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
        if dropped:
            notes.append(f"{page}: fragment label folded into prose")

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
