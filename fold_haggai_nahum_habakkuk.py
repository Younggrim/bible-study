#!/usr/bin/env python3
"""
Folds three complete books: Haggai, Nahum and Habakkuk. Eight chapters.

Each page already carried Author, Classification, Key Themes and Historical
Context, plus a Structure: sublist giving the section headings and verse ranges.
Those headings are carried over, adjusted only where noted below, and the bullets
are replaced with exposition.

Headless continuation paragraphs. Each of these panes has one or two headless
auth-item divs that continue Historical Context. The reference pages -- jonah1,
ruth1, philemon1, genesis1 -- carry none, so these are appended to the Historical
Context body rather than left as bare paragraphs.

Two pages also carry a field whose label is a sentence fragment rather than a field
name: nahum3's "Nahum uses Thebes (No-Amon) as a precedent:" and habakkuk3's "The
structure mirrors the book's journey:". Both hold real content, folded into the
relevant section prose.

Corrections to the inherited skeleton:
  habakkuk2  "the Answer" -> "The Answer", and v.5 was missing between v.4 and
             vv.6-8, so the range becomes vv.4-5
  haggai1    nine single-verse headings consolidated to six, since WORKFLOW.md
             targets 4-5 sections for a chapter under 20 verses
  nahum1     seven consolidated to five, same reason
  nahum2     six consolidated to five

Follows the format in WORKFLOW.md. Writes nothing if any page fails a check.

Usage:
    python3 fold_haggai_nahum_habakkuk.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"haggai1": 15, "haggai2": 23, "nahum1": 15, "nahum2": 13,
          "nahum3": 19, "habakkuk1": 17, "habakkuk2": 20, "habakkuk3": 19}

# Labels kept above the sections, in this order.
HEADER_ORDER = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

# Sentence-fragment labels whose content is folded into a section instead.
ABSORB = {
    "nahum3": "Nahum uses Thebes (No-Amon) as a precedent:",
    "habakkuk3": "The structure mirrors the book&#x27;s journey:",
}

SECTIONS = {
"haggai1": [
  ("The Date and the Two Leaders (v.1)",
   "Haggai is dated to the day: the second year of Darius, sixth month, first day, "
   "which is late August of 520 BC. That precision matters because the whole book "
   "turns on a moment. The word comes through the prophet to Zerubbabel the governor "
   "and Joshua the high priest, civil and religious authority addressed together, "
   "since the work in question needed both."),
  ("\u201cThe Time Is Not Come\u201d: Misplaced Priorities (vv.2-4)",
   "The people are quoted before they are answered: the time has not come to build "
   "the LORD's house. Sixteen years had passed since the foundation was laid and "
   "opposition had stopped the work, so the excuse had history behind it. God's reply "
   "is a question about their own houses, which are not merely built but "
   "\u201cceiled\u201d \u2014 panelled, finished to a standard. The charge is not "
   "idleness. They had been building steadily, just not this."),
  ("Consider Your Ways: Much Sown, Little Reaped (vv.5-6)",
   "\u201cConsider your ways\u201d recurs through the book and is closer to "
   "\u201cset your heart on your paths\u201d. What follows is a list of efforts that "
   "do not add up: much sown and little reaped, eating without being filled, wages "
   "put into a bag with holes. Anyone who has worked hard through a poor season "
   "recognises the description. Haggai's claim is that the futility is not economic "
   "accident but message."),
  ("Go Up to the Mountain and Build (vv.7-8)",
   "The remedy is specific and physical: go to the hills, bring timber, build the "
   "house. No sacrifice or ceremony is prescribed first. The stated purpose is that "
   "God will take pleasure in it and be glorified, which puts the point of the "
   "building outside the builders. Note what is not promised \u2014 prosperity is not "
   "offered as the reason to obey."),
  ("Why the Heavens Withheld (vv.9-11)",
   "The diagnosis is made explicit: you looked for much and it came to little, and "
   "\u201cI did blow upon it\u201d. The drought is attributed directly to God and its "
   "reach is itemised, over the ground, the grain, the new wine, the oil, and the "
   "labour of human hands. The logic is covenantal rather than punitive in a general "
   "sense: the terms of Deuteronomy had named exactly this consequence, so the "
   "hearers would have recognised the pattern."),
  ("The People Obeyed, and the Spirit Was Stirred (vv.12-15)",
   "The response is immediate and, among the prophets, unusual \u2014 no argument, no "
   "delay, no partial compliance. The people obeyed and \u201cdid fear before the "
   "LORD\u201d. God's answer to their obedience is one clause, \u201cI am with "
   "you\u201d, which is the whole of the encouragement offered. Verse 14 credits the "
   "stirring of their spirit to God, so the obedience just recorded is also "
   "attributed to Him, and work resumes twenty-three days after the first word came."),
],
"haggai2": [
  ("Encouragement to the Discouraged Builders (vv.1-5)",
   "Seven weeks into the work, morale has fallen. The question in v.3 is put to the "
   "oldest men present: who remembers the first house, and is this not nothing by "
   "comparison? Some of them had seen Solomon's temple before 586 BC, and the honest "
   "answer was yes. The encouragement does not dispute the comparison. It changes the "
   "subject to presence \u2014 be strong, work, for I am with you \u2014 and grounds "
   "it in the covenant made at the exodus."),
  ("The Shaking of Nations and the Greater Glory (vv.6-9)",
   "\u201cYet once, it is a little while, and I will shake\u201d extends the horizon "
   "past the building site to heaven, earth, sea and all nations. The promise that "
   "\u201cthe desire of all nations shall come\u201d has been read both as the "
   "Messiah and as the wealth of the nations arriving, and the following verse about "
   "silver and gold supports the second while not excluding the first. The claim in "
   "v.9 is the point: the latter glory of this house will exceed the former. Measured "
   "in stonework that was false, which is why the measure has changed."),
  ("The Lesson of Holiness and Defilement (vv.10-14)",
   "Haggai puts two questions to the priests, and their answers are the argument. "
   "Does consecrated meat make what it touches holy? No. Does a corpse make what it "
   "touches unclean? Yes. Holiness does not transmit by contact; defilement does. The "
   "application in v.14 is unsparing \u2014 the people's offerings had been unclean "
   "because the people were \u2014 and it explains why sixteen years of sacrifice at "
   "a neglected site had not helped them."),
  ("The Turning Point: From This Day I Will Bless (vv.15-19)",
   "The date is given again, the twenty-fourth day of the ninth month, and it is "
   "treated as a hinge. Haggai reviews the barren years, then points forward: from "
   "this day, consider. Verse 19 concedes that nothing is yet visible \u2014 the seed "
   "is still in the ground, the vine and the fig have not yet borne \u2014 and "
   "promises blessing anyway. The promise is dated before the evidence, which is the "
   "shape of most of what the book asks of them."),
  ("Zerubbabel: God's Chosen Signet Ring (vv.20-23)",
   "The final oracle comes the same day and addresses one man. Kingdoms will be "
   "overthrown and Zerubbabel will be made \u201cas a signet\u201d \u2014 a signet "
   "ring, the instrument that carried a king's authority and was never lent casually. "
   "The weight of it is that his grandfather Jehoiachin had been told the opposite in "
   "Jeremiah 22:24, that God would pluck him off as a signet from His hand. The "
   "reversal is deliberate, and Zerubbabel appears in both genealogies of Jesus."),
],
"nahum1": [
  ("The Burden Against Nineveh (v.1)",
   "The book is titled twice over, \u201cthe burden of Nineveh\u201d and \u201cthe "
   "book of the vision of Nahum the Elkoshite\u201d. \u201cBurden\u201d is the "
   "prophetic term for an oracle of weight, usually against a foreign power. That it "
   "is also called a book suggests something composed to be read rather than only "
   "delivered, which suits the tight poetic construction of what follows."),
  ("A Hymn to the Avenging God (vv.2-6)",
   "The book opens not with Nineveh but with God's character, and the first word of "
   "the poem is jealous. Slow to anger is set inside the same sentence as great in "
   "power and one who will not acquit the guilty, so patience is presented as "
   "restraint rather than tolerance. The imagery is storm and earthquake, the sea "
   "dried, Bashan and Carmel withering, and it ends on a question \u2014 who can "
   "stand? \u2014 which the rest of the book answers with a name."),
  ("Good to Those Who Trust Him, an End to the Rest (vv.7-11)",
   "Verse 7 is the hinge of the chapter and the reason it is not merely fierce: "
   "\u201cThe LORD is good, a strong hold in the day of trouble; and he knoweth them "
   "that trust in him.\u201d The same power that dries the sea is a refuge. What "
   "follows turns to Nineveh with an overrunning flood and pursuit into darkness, and "
   "v.11 names the offence as counsel devised against the LORD \u2014 the city's "
   "policy, not merely its armies."),
  ("A Decree Against the Dynasty (vv.12-14)",
   "Judah is addressed directly with a promise of relief: though Assyria is many, it "
   "will be cut down, and \u201cI will break his yoke from off thee\u201d. Assyria "
   "had taken tribute from Judah for generations, so the yoke was literal. The decree "
   "in v.14 is aimed at the Assyrian king's line, cutting off name and posterity and "
   "cutting the idols out of the temple, which strikes at the two things such a king "
   "relied on to outlast his own death."),
  ("Good Tidings on the Mountains (v.15)",
   "The chapter closes with a runner on the hills carrying good news and publishing "
   "peace, the same line Isaiah 52:7 applies to the return from exile and Paul later "
   "applies to the gospel. Here the good news is specific and grim in its cause: the "
   "wicked one shall no more pass through. Judah is told to keep its feasts and pay "
   "its vows, ordinary religious life resumed, which for an occupied people is the "
   "practical shape of deliverance."),
],
"nahum2": [
  ("The Siege Begins, and Jacob's Majesty Returned (vv.1-2)",
   "The chapter opens mid-action, addressing Nineveh with mock advice \u2014 keep the "
   "fortress, watch the road, make your loins strong \u2014 the tone of someone "
   "telling a doomed defender to try harder. Verse 2 gives the reason underneath the "
   "military description: the LORD is restoring the excellency of Jacob. The fall of "
   "one city is presented as the other side of the recovery of a people, which is why "
   "a book of destruction sits in a canon of promise."),
  ("The Assault: Chariots, Torches, and Panic (vv.3-5)",
   "The poetry accelerates into fragments \u2014 shields red, chariots flaming, fir "
   "trees shaken, chariots raging in the streets and jostling in the broad ways, "
   "running like lightning. Nahum's Hebrew is famously rapid here, and the effect is "
   "closer to camera work than narration. The defenders are described stumbling in "
   "their walk, which in the middle of so much motion is the detail that carries the "
   "outcome."),
  ("The Breakthrough: Gates of the Rivers Opened (vv.6-7)",
   "\u201cThe gates of the rivers shall be opened, and the palace shall be "
   "dissolved.\u201d Nineveh sat on the Tigris and depended on canal works, and "
   "ancient accounts of the 612 BC fall describe water breaching the defences. "
   "Whether the line is prediction or image, the result is stated as dissolution "
   "rather than assault. Verse 7 leaves the queen or the city personified led away, "
   "with attendants beating their breasts."),
  ("The Flight: Nineveh Emptied Like a Pool (vv.8-10)",
   "The city is a pool of water whose people drain away, and the shouted commands to "
   "stand are ignored. Then the spoil: silver, gold, and \u201call pleasant "
   "furniture\u201d, wealth accumulated from a century of tribute now carried out by "
   "someone else. Verse 10 stacks three near-identical Hebrew words for emptiness, an "
   "effect no translation quite carries, and ends on knees knocking and faces "
   "blackened."),
  ("The Lion's Den Emptied, and \u201cI Am Against Thee\u201d (vv.11-13)",
   "Assyria's own favourite image is turned back on it. Assyrian kings decorated "
   "their palaces with lion hunts and described themselves as lions; Nahum asks where "
   "the lion's den is now, the place where prey was carried for the cubs. The chapter "
   "ends with the sentence that governs the book: \u201cBehold, I am against thee, "
   "saith the LORD of hosts.\u201d Everything described in the chapter is attributed "
   "to that one fact rather than to Babylonian and Median strategy."),
],
"nahum3": [
  ("The Indictment: Woe to the Bloody City (vv.1-4)",
   "The charge sheet is short and specific: bloody, full of lies and robbery. Then "
   "the sound of it \u2014 whip, wheel, prancing horses, jumping chariots \u2014 and "
   "the aftermath, corpses without number. Assyrian records themselves boast of "
   "flaying captives and stacking heads, so Nahum is not exaggerating for effect. "
   "Verse 4 shifts metaphor to a harlot selling nations, which names the deeper charge: "
   "Assyria traded in other peoples."),
  ("The Sentence: Public Shaming (vv.5-7)",
   "The punishment is described as exposure, the treatment a captured city and a "
   "convicted prostitute both received, and it is deliberately humiliating rather "
   "than merely fatal. \u201cI will cast abominable filth upon thee.\u201d The "
   "closing question is the sharpest line in the chapter: who will bemoan her, and "
   "where shall I seek comforters for thee? A city that had left no one to mourn for "
   "others will find no mourners."),
  ("The Precedent: The Fall of Thebes (vv.8-10)",
   "Nahum argues from history rather than assertion. Thebes \u2014 No-Amon \u2014 sat "
   "among the waters of the Nile with Ethiopia and Egypt for strength and Put and Lubim "
   "for helpers, and it fell in 663 BC despite all of it. The argument is devastating "
   "because Assyria itself had sacked Thebes, under Ashurbanipal, within living memory. "
   "Nineveh had watched infants dashed and nobles taken by lot, and Nahum's point is "
   "that she is about to receive what she gave."),
  ("The Application: Nineveh Will Share That Fate (vv.11-13)",
   "The comparison lands: Nineveh will be drunk, will hide, will look for strength "
   "and find it gone. The strongholds are figs on a tree, ready to fall into the "
   "mouth of whoever shakes them. The soldiers are called women and the gates set open "
   "and the bars burned, which for a city whose reputation rested on its walls is a "
   "targeted insult rather than a general one."),
  ("The Mockery: Futile Preparations (vv.14-17)",
   "Draw water, strengthen the brickwork, prepare for siege \u2014 orders given so "
   "that their pointlessness registers. Then locusts, the image turned twice: make "
   "yourself many as locusts, and your merchants and captains are locusts that camp in "
   "the cold and fly away when the sun rises. Assyria's traders and officers are "
   "described as opportunists who will not be there for the ending."),
  ("The Epitaph: An Incurable Wound (vv.18-19)",
   "The book ends addressed to the Assyrian king with his shepherds asleep and his "
   "people scattered on the mountains with no one to gather them. \u201cThere is no "
   "healing of thy bruise\u201d \u2014 the wound is not survivable. The final line is "
   "everyone who hears clapping their hands, and the question it rests on assumes its "
   "own answer: upon whom has thy wickedness not passed continually? Nineveh fell in "
   "612 BC and was never rebuilt."),
],
"habakkuk1": [
  ("Superscription (v.1)",
   "\u201cThe burden which Habakkuk the prophet did see.\u201d Nothing is said about "
   "his home, family or reign, which is unusual, and \u201cprophet\u201d is stated as "
   "his office rather than inferred. What follows is also unusual in kind: most "
   "prophets speak to the people for God, while Habakkuk spends two chapters speaking "
   "to God about the people."),
  ("The First Complaint: How Long? (vv.2-4)",
   "The book opens on unanswered prayer. How long shall I cry and thou wilt not hear? "
   "The grievance is domestic rather than foreign \u2014 violence, strife and "
   "contention inside Judah, with the law slacked and judgment never going forth. "
   "Verse 4's picture of the wicked surrounding the righteous so that justice comes "
   "out crooked is a description of a court system, not a battlefield. That the "
   "complaint is preserved in Scripture rather than corrected is itself notable."),
  ("God's First Answer: I Raise Up the Chaldeans (vv.5-11)",
   "The answer is worse than the silence. God is working \u2014 \u201cye would not "
   "believe, though it be told you\u201d \u2014 and the work is Babylon, described "
   "across seven verses as bitter, hasty, terrible, swifter than leopards, gathering "
   "captives like sand, scoffing at kings and fortresses. Verse 11 names the flaw in "
   "the instrument in passing: he imputes his own power to his god. The answer "
   "concedes what the next complaint will press."),
  ("The Second Complaint: How Can You Use the Wicked? (vv.12-17)",
   "Habakkuk does not retreat; he argues from God's character. \u201cArt thou not from "
   "everlasting... thou art of purer eyes than to behold evil.\u201d The question is "
   "sharper than the first: not why the wicked prosper, but why God would use a nation "
   "more wicked than the one being judged. The fisherman image runs to the end \u2014 "
   "men caught in a net, the fisher sacrificing to his own tackle \u2014 and the "
   "chapter closes on a question, with the answer held over to chapter 2."),
],
"habakkuk2": [
  ("The Watchman's Posture: Waiting for an Answer (v.1)",
   "Having argued, Habakkuk takes a position: \u201cI will stand upon my watch, and "
   "set me upon the tower, and will watch to see what he will say unto me, and what I "
   "shall answer when I am reproved.\u201d The verse assumes he may be corrected and "
   "waits anyway, which distinguishes complaint from accusation. He expects a reply, "
   "and expects to have to respond to it."),
  ("Write the Vision Plainly (vv.2-3)",
   "The instruction is to write it, make it plain, and make it legible to someone "
   "moving \u2014 \u201cthat he may run that readeth it\u201d. The answer is meant to "
   "outlive the conversation. Verse 3 sets an appointed time and concedes delay in the "
   "same breath: though it tarry, wait for it. Waiting is built into the answer rather "
   "than being the absence of one."),
  ("The Just Shall Live by His Faith (vv.4-5)",
   "The reply is compressed into a contrast. The proud soul is not upright in him; "
   "the just shall live by his faith. Paul quotes the second half in Romans and "
   "Galatians and Hebrews quotes it again, which has made this the most consequential "
   "verse in the Minor Prophets. In context it is an answer about survival: Babylon "
   "will not last on the strength of its pride, and the righteous will come through on "
   "the strength of trust. Verse 5 then sketches the proud man enlarging his appetite "
   "like the grave and never satisfied, which introduces the five woes."),
  ("First and Second Woes: Plunder and Exploitative Gain (vv.6-11)",
   "The nations Babylon looted take up a taunting proverb against her, so the judgment "
   "is spoken in the voice of the victims. The first woe is against increase by "
   "plunder, and its logic is reversal \u2014 those you spoiled will spoil you. The "
   "second is against building a house by wrongful gain and setting a nest on high for "
   "safety. Verse 11 gives the arresting image: the stone will cry out of the wall and "
   "the beam will answer it. The building materials testify to how they were bought."),
  ("Third Woe: Building with Blood (vv.12-14)",
   "Woe to him that builds a town with blood and establishes a city by iniquity. The "
   "answer is that such labour is spent for nothing, the people wearying themselves "
   "\u201cfor very vanity\u201d. Then the verse that lifts the chapter out of its "
   "immediate subject: the earth shall be filled with the knowledge of the glory of "
   "the LORD, as the waters cover the sea. Babylon's monuments are set against an "
   "outcome that does not depend on them."),
  ("Fourth and Fifth Woes: Debauchery and Idolatry (vv.15-19)",
   "The fourth woe is against making a neighbour drunk in order to shame him, with "
   "the sentence framed as the cup coming round \u2014 thou shalt be filled with shame "
   "instead of glory. Verse 17 attaches the violence done to Lebanon and its beasts, "
   "which extends the charge past people. The fifth woe turns on idols and asks the "
   "practical question: what profit is a teacher of lies, a thing overlaid with gold "
   "with no breath in it? Saying \u201cawake\u201d to carved wood is offered as the "
   "reduction of the whole enterprise."),
  ("The LORD in His Temple: Let the Earth Keep Silence (v.20)",
   "Against idols that must be told to wake, the chapter ends with the LORD in His "
   "holy temple and the whole earth commanded to be silent before Him. It answers "
   "chapter 1 without addressing its arguments again. The silence is not resignation, "
   "and chapter 3 shows what Habakkuk does with it."),
],
"habakkuk3": [
  ("Superscription and a Prayer for Revival (vv.1-2)",
   "The chapter is titled a prayer \u201cupon Shigionoth\u201d, a musical direction "
   "nobody can now define, and it ends with instructions for stringed instruments. "
   "This is a psalm, and it was sung. Verse 2 is the whole book in one sentence: I "
   "have heard, and I was afraid; revive thy work; in wrath remember mercy. He does "
   "not ask for the judgment to be cancelled, only for mercy inside it. The three "
   "chapters trace a movement from complaint to faith to worship, and this is where "
   "the third stage begins."),
  ("Theophany: God's Coming in Glory (vv.3-7)",
   "The poem turns to memory, and the memory is Sinai \u2014 God coming from Teman "
   "and Paran, brightness like light, horns or rays from His hand. Pestilence and "
   "burning coals go before Him, the everlasting mountains scatter, and the tents of "
   "Cushan and Midian tremble. Habakkuk is answering his own fear by recalling that "
   "this has happened before, which is a different move from arguing himself into calm."),
  ("Power Over Nature and Nations (vv.8-12)",
   "A series of questions asks whether God is angry with the rivers and the sea, and "
   "the answer implied is that the water was never the target. The mountains see Him "
   "and tremble, the deep utters its voice, the sun and moon stand still \u2014 "
   "language that gathers the Red Sea, the Jordan and Joshua's long day into one "
   "picture. The march is described as being through the land in indignation, and the "
   "threshing of the nations is the purpose of it."),
  ("The Salvation of His People (vv.13-15)",
   "The purpose is finally named: thou wentest forth for the salvation of thy people. "
   "Everything preceding \u2014 the shaking, the trembling, the rivers \u2014 was "
   "instrumental to that. The wounding of the head of the wicked house and the piercing "
   "of his own weapons return the enemy's violence to him, and v.15 closes the "
   "sequence back at the sea, where it started."),
  ("The Prophet's Trembling and Waiting (v.16)",
   "The honest verse. When I heard, my belly trembled, my lips quivered, rottenness "
   "entered into my bones, I trembled in myself. The vision does not soothe him. What "
   "changes is not his body but his intention: \u201cthat I might rest in the day of "
   "trouble\u201d. He is describing composure chosen while still shaking, which is why "
   "the confession that follows carries weight."),
  ("The Supreme Confession of Faith (vv.17-19)",
   "The conditions are listed exhaustively and without softening: no figs, no fruit "
   "on the vine, the olive failing, no meat in the fields, the flock cut off, no herd "
   "in the stalls. That is total agricultural collapse, which for this economy is "
   "everything. Then \u201cyet I will rejoice in the LORD\u201d. The joy is placed in "
   "God rather than in provision, and the chapter ends with feet like hinds' feet on "
   "high places, sure footing on ground that should not be walkable. The book that "
   "opened with \u201chow long\u201d ends in a song."),
],
}


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
        body = pane.group(2)

        fields, extra, absorbed = {}, [], None
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', body, re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in HEADER_ORDER:
                fields[name] = rest
            elif name is not None and name == ABSORB.get(page):
                absorbed = rest
            elif name is None and rest == "Structure:":
                pass
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in HEADER_ORDER:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        if ABSORB.get(page) and absorbed is None:
            problems.append(f"{page}: expected {ABSORB[page]!r}, not found")

        # Headless continuation paragraphs join Historical Context.
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields.get("Historical Context:", "")] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged into "
                         f"Historical Context")

        sections = SECTIONS[page]
        if absorbed:
            notes.append(f"{page}: {ABSORB[page]!r} folded into section prose")

        covered = set()
        for head, prose in sections:
            if "*" in prose:
                problems.append(f"{page}: markdown asterisk in prose")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)",
                                 head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                covered |= set(range(a, z + 1))
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: sections leave verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for want in HEADER_ORDER:
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
