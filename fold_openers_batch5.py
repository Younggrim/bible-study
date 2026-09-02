#!/usr/bin/env python3
"""
Folds the four remaining tracked openers onto the target Authorship format:
Genesis 1, Acts 1, Romans 12 and Revelation 16.

These are not a uniform group, and unlike earlier batches three of them carry
content in the pane that is not an auth-item div.

Sublist handling. A pane may end with a headless auth-item heading followed by
<ul class="auth-sublist">. Where every list item carries a verse range the list
is an outline, and the verse-range sections replace it with the same ranges plus
exposition -- that is the fold working as intended, and it is what happened for
Obadiah, Jonah and Revelation 16 here. Where items lack verse ranges the list is
not an outline and dropping it would lose content, so this script refuses to touch
such a page unless it is named in DROP_SUBLIST with a reason.

Genesis 1 is the one such page in this batch. Its "Structure of the Six Days"
list states the forming/filling pattern, which is the organising insight of the
chapter rather than an outline of it. It is folded into the prose of the day
sections instead of kept as a stray list, since no other folded page has one.

Repository-wide, 13 pages carry non-outline sublists: genesis1, isaiah53,
proverbs25, proverbs26, revelation6 and songofsolomon1 through 8. Whoever runs the
bulk fold needs the same guard.

Prose uses curly quotes for cited terms. No markdown emphasis.

Follows the format in WORKFLOW.md. Writes nothing if any page fails a check.

Usage:
    python3 fold_openers_batch5.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"genesis1": 31, "acts1": 26, "romans12": 21, "revelation16": 21}

# Fields to drop rather than preserve, with the reason. Only for fields the
# verse-range sections genuinely supersede.
DROP_FIELDS = {
    "romans12": {"Structure:": "an outline of vv.1-2 / 3-8 / 9-21 that the "
                                "verse-range sections restate with exposition"},
}

# Pages where a non-outline sublist may be dropped, with the reason.
DROP_SUBLIST = {
    "genesis1": "the forming/filling pattern is stated in the prose of the day "
                "sections instead",
}

VR_ANY = re.compile(r"\(vv?\.\s*\d")

WORK = {
"genesis1": (
 "Narrative \u2014 Creation Account",
 "Creation by word alone, a formless void first given shape and then filled, "
 "light before the luminaries, humanity made in God&#x27;s image as male and "
 "female, dominion granted as stewardship, and a sevenfold verdict of goodness",
 [
  ("In the Beginning God Created (vv.1-2)",
   "The first sentence makes God the subject and everything else the object. There "
   "is no account of God's own origin and no rival power to negotiate with, which "
   "distinguishes this opening from the cosmogonies of surrounding cultures where "
   "creation follows conflict among gods. Verse 2 states the problem the six days "
   "will solve: the earth was \u201cwithout form, and void\u201d \u2014 unshaped and "
   "unfilled. Those two lacks are addressed in that order, days one to three giving "
   "shape and days four to six filling what was shaped, so the structure of the "
   "chapter is announced before the work begins."),
  ("Day One: Light Called Out of Darkness (vv.3-5)",
   "\u201cAnd God said\u201d appears here for the first of ten times in the chapter, "
   "and light arrives by speech rather than by struggle. God then names day and "
   "night, and naming is an act of authority in the ancient world rather than a "
   "convenience. Light exists three days before the sun, which the account states "
   "without any sign of difficulty \u2014 whatever else is happening here, light is "
   "not being made dependent on the luminaries."),
  ("Day Two: The Firmament Divides the Waters (vv.6-8)",
   "The second day separates the waters above from the waters below and produces the "
   "sky between them. This is the only day that does not receive the verdict "
   "\u201cit was good\u201d, an omission readers have noticed for centuries without "
   "agreeing on a reason. The work is again separation, continuing the shaping begun "
   "on day one."),
  ("Day Three: Land, Seas, and Vegetation (vv.9-13)",
   "The waters gather, dry land appears, and this day receives the verdict twice. "
   "Vegetation is described as yielding seed \u201cafter his kind\u201d, which gives "
   "created things their own means of continuance rather than requiring fresh acts of "
   "creation. With sky, sea and land now distinguished, the shaping work is finished "
   "\u2014 and nothing is yet living in any of the three regions."),
  ("Day Four: Lights to Rule Day and Night (vv.14-19)",
   "The filling begins, and it fills the domain made on day one. The sun and moon "
   "are not named. They are \u201cthe greater light\u201d and \u201cthe lesser "
   "light\u201d, which in cultures that worshipped both is a deliberate demotion, and "
   "they are given work to do \u2014 to divide, to rule, to serve for signs and "
   "seasons. Appointed instruments rather than deities, and the pairing with day one "
   "is the first of three."),
  ("Day Five: Waters and Sky Filled (vv.20-23)",
   "Sea creatures and birds fill the regions separated on day two. The first blessing "
   "in the Bible is spoken here, and it is spoken over animals: be fruitful and "
   "multiply. The verb \u201ccreated\u201d returns for the first time since v.1, used "
   "of the great sea creatures, which reads as a quiet answer to myths in which sea "
   "monsters were gods to be subdued rather than creatures to be made."),
  ("Day Six: Land Animals, and Humanity in God's Image (vv.24-28)",
   "The land of day three is filled, completing the pattern, and then the account "
   "slows. \u201cLet us make man in our image\u201d shifts from command to "
   "deliberation, and the image is defined in the same breath as belonging to both "
   "sexes: \u201cmale and female created he them\u201d. Dominion is granted alongside "
   "it, which grounds authority in resemblance to God rather than in strength, and "
   "the blessing given to the animals is repeated over humanity with the addition of "
   "responsibility."),
  ("Provision, and Very Good (vv.29-31)",
   "Food is assigned to people and animals alike, and what is described is "
   "vegetarian. The chapter then gives its verdict for the seventh time and "
   "strengthens it once: not good but \u201cvery good\u201d, and the assessment is of "
   "the whole rather than of any part. The sixth day ends with the work complete and "
   "nothing yet said about rest, which belongs to the opening verses of chapter 2."),
 ]),
"acts1": (
 "Historical Narrative",
 "A former treatise continued, forty days of instruction, a question about timing "
 "redirected, power promised for witness, a visible ascension with a promise of "
 "return, and a vacancy filled by lot",
 [
  ("The Former Treatise, and Forty Days (vv.1-3)",
   "Luke addresses Theophilus again and refers back to his Gospel, which makes Acts "
   "the second volume of a single work rather than a sequel. The resurrection "
   "appearances are summarised as spanning forty days with \u201cmany infallible "
   "proofs\u201d, and their subject is named: things pertaining to the kingdom of God. "
   "That Jesus spent the period teaching rather than only appearing is easy to read "
   "past."),
  ("Wait for the Promise (vv.4-5)",
   "The command given to men holding a worldwide commission is to stay put. The "
   "promise is identified by contrast with John's baptism, and the interval is left "
   "deliberately vague \u2014 \u201cnot many days hence\u201d \u2014 so that the "
   "waiting is real rather than scheduled. Nothing in the chapter treats the delay as "
   "wasted time."),
  ("It Is Not for You to Know the Times (vv.6-7)",
   "The disciples ask about restoring the kingdom to Israel. The chapter neither "
   "mocks the question nor answers it: Jesus declines the timetable specifically, "
   "placing times and seasons in the Father's authority. What is refused is the "
   "schedule rather than the hope, a distinction worth holding onto given how often "
   "the question has been pressed since."),
  ("Ye Shall Be Witnesses (v.8)",
   "Information is replaced with assignment: power when the Spirit comes, then "
   "witness in Jerusalem, Judea, Samaria, and to the uttermost part of the earth. "
   "That geography is also the shape of the book, so the verse doubles as a table of "
   "contents. The word for witness is the ordinary term for someone testifying to "
   "what they have seen, which is why the qualification in v.21 matters later."),
  ("Taken Up, and a Promise of Return (vv.9-11)",
   "The ascension is reported plainly and briefly \u2014 taken up, received by a "
   "cloud, out of sight. Two men in white clothing ask why they stand looking up, and "
   "give the promise that has shaped Christian expectation since: He will come "
   "\u201cin like manner as ye have seen him go\u201d. The question is gentle but it "
   "is a correction, and it turns them back toward the assignment just given."),
  ("Continuing in Prayer with One Accord (vv.12-14)",
   "The eleven are listed, and with them the women, Mary the mother of Jesus, and "
   "His brothers \u2014 brothers who had not believed during His ministry (John 7:5), "
   "so their presence records a change without commenting on it. They are in an upper "
   "room and continuing with one accord in prayer. This is the last mention of Mary "
   "in the New Testament."),
  ("Peter Reads the Vacancy from Scripture (vv.15-22)",
   "Peter stands among about a hundred and twenty and treats Judas's defection as "
   "something Scripture had already accounted for, citing two psalms. Luke adds the "
   "account of the field and the death as an aside for readers who would not know "
   "Jerusalem. The qualifications set for a replacement are strict and entirely "
   "backward-looking: present from John's baptism through the ascension, and able to "
   "witness to the resurrection."),
  ("Matthias Chosen by Lot (vv.23-26)",
   "Two candidates are put forward, the assembly prays that God would show which He "
   "has chosen, and lots are cast. The method has been argued over ever since, partly "
   "because lots never appear again in Acts once the Spirit comes. Matthias is not "
   "mentioned again either, and of the two silences the one about the practice may be "
   "the more telling."),
 ]),
"romans12": (
 "Epistle \u2014 Pauline",
 "Mercies as the ground of obedience, bodies presented as a living sacrifice, a "
 "renewed mind against conformity, gifts measured by faith and exercised in a body, "
 "and love worked out as far as the treatment of enemies",
 [
  ("Present Your Bodies a Living Sacrifice (vv.1-2)",
   "The \u201ctherefore\u201d turns eleven chapters of doctrine toward conduct, and "
   "the appeal is made by mercies rather than by apostolic authority. What is asked "
   "for is the body, which keeps a letter that has spent chapters on justification "
   "grounded in something physical. \u201cLiving sacrifice\u201d is deliberately "
   "paradoxical, since a sacrifice was by definition killed. The two commands that "
   "follow pull opposite ways: stop being shaped by the present age, be transformed "
   "by the renewing of the mind \u2014 and the passive voice in the second does quiet "
   "work, since the transforming is not self-administered."),
  ("Think Soberly: Measured by Faith (vv.3-5)",
   "Humility is defined as accurate self-assessment rather than low self-assessment: "
   "think soberly, according to the measure of faith God has dealt out. The body "
   "image follows immediately and is what makes accuracy possible, since a part "
   "cannot be judged in isolation. Members are said to belong to one another, not "
   "merely to the whole, which rules out both self-importance and self-erasure."),
  ("Gifts Differing, Given by Grace (vv.6-8)",
   "Seven gifts are listed with brief instructions attached, and most of the "
   "instructions concern manner rather than method: give with simplicity, rule with "
   "diligence, show mercy with cheerfulness. Public and unglamorous roles sit in the "
   "same list without ranking. Each differs \u201caccording to the grace that is "
   "given to us\u201d, a clause that removes grounds for boasting and for comparison "
   "at the same time."),
  ("Let Love Be Without Dissimulation (vv.9-13)",
   "The chapter shifts into rapid imperatives, most of them lacking a main verb in "
   "the Greek, so they read like a list of headings. Love without hypocrisy comes "
   "first and governs what follows: affectionate, preferring one another in honour, "
   "fervent, patient in tribulation, given to hospitality. \u201cDistributing to the "
   "necessity of saints\u201d keeps the sequence from staying abstract, and in a "
   "church that housed travelling messengers hospitality meant taking in strangers."),
  ("Bless, Weep, and Be Not Wise in Your Own Conceits (vv.14-16)",
   "Blessing persecutors is stated without qualification or exception. Of the two "
   "halves of v.15, rejoicing with those who rejoice is arguably the harder, since "
   "sorrow draws sympathy more naturally than someone else's success does. The "
   "instruction to be of the same mind and to keep company with the lowly ends by "
   "warning against being wise in one's own estimation \u2014 which is exactly where "
   "a chapter about spiritual gifts could otherwise lead."),
  ("Overcome Evil with Good (vv.17-21)",
   "Retaliation is ruled out, and vengeance is not denied but reassigned: "
   "\u201cVengeance is mine; I will repay, saith the Lord\u201d. That reassignment is "
   "what makes restraint possible without pretending the wrong was small. Verse 18 "
   "concedes that peace is not always attainable \u2014 \u201cif it be possible, as "
   "much as lieth in you\u201d \u2014 and still requires the attempt. The coals of "
   "fire quoted from Proverbs lead to the chapter's closing statement of the "
   "principle in positive form: overcome evil with good."),
 ]),
"revelation16": (
 "Apocalyptic Prophecy \u2014 The Seven Bowl Judgments",
 "Wrath poured out rather than partially released, plagues echoing Egypt on a "
 "global scale, judgment declared righteous by heaven itself, repeated blasphemy "
 "without repentance, kings gathered by deception, and a finished work announced",
 [
  ("Go Your Ways and Pour Out (v.1)",
   "A great voice from the temple sends the seven angels, and the command is to pour "
   "rather than to sound or to open. That verb governs the chapter. Where the seals "
   "revealed and the trumpets warned, the bowls empty, and nothing in the series is "
   "partial \u2014 which is the structural difference from everything preceding it."),
  ("The First Bowl: Sores on the Marked (v.2)",
   "The plague falls specifically on those bearing the beast's mark and worshipping "
   "his image, so its target is defined by allegiance rather than by geography. "
   "\u201cA noisome and grievous sore\u201d recalls the boils of Exodus 9. The "
   "judgment lands on the body, in a book where the mark itself was received on the "
   "body."),
  ("The Second and Third Bowls: Sea and Rivers to Blood (vv.3-7)",
   "Sea and then fresh water turn to blood, and both are total where the "
   "corresponding trumpets struck a third. The interruption in vv.5-7 is the point of "
   "the passage rather than a digression: the angel of the waters declares God "
   "righteous in these judgments, and the altar answers that His judgments are true "
   "and righteous. The reason given is proportion \u2014 those who shed blood are "
   "given blood to drink."),
  ("The Fourth Bowl: Scorched, and Still Blaspheming (vv.8-9)",
   "The sun is given power to scorch, reversing its ordinary role as provision. What "
   "the text records is not the suffering but the response: men blasphemed the name "
   "of God \u201cand repented not to give him glory\u201d. This is the chapter's "
   "refrain and its argument at once. Judgment on its own does not produce "
   "repentance, which answers anyone supposing that sufficient severity eventually "
   "would."),
  ("The Fifth Bowl: Darkness on the Beast's Kingdom (vv.10-11)",
   "This bowl is poured on the beast's throne, striking the regime directly, and the "
   "result is darkness and pain. The reaction is again blasphemy without repentance, "
   "and v.11 adds \u201cof their deeds\u201d \u2014 the deeds are known and held onto. "
   "The darkness recalls the ninth Egyptian plague, which likewise fell on a throne "
   "claiming divinity."),
  ("The Sixth Bowl: Euphrates Dried, Kings Gathered (vv.12-16)",
   "The river is dried to open a road for kings from the east, and the gathering is "
   "carried out by unclean spirits working signs, sent from the dragon, the beast and "
   "the false prophet. Deception assembles the armies rather than force. Verse 15 "
   "breaks in with a beatitude addressed to readers rather than to the scene \u2014 "
   "\u201cBehold, I come as a thief. Blessed is he that watcheth\u201d. The place is "
   "named Armageddon, and the chapter says nothing further about a battle there."),
  ("The Seventh Bowl: It Is Done (vv.17-21)",
   "The voice from the throne says \u201cIt is done\u201d, and what follows is the "
   "largest disturbance described in the book: an earthquake beyond any before it, "
   "the great city split in three, Babylon remembered for judgment, islands and "
   "mountains gone. Hailstones of enormous weight fall, recalling Exodus once more. "
   "The last line is the refrain a final time, men blaspheming God because of the "
   "plague. The series closes without a single recorded repentance, which is the "
   "verdict the whole chapter has been building toward."),
 ]),
}


def main():
    check = "--check" in sys.argv
    problems = []
    planned = {}
    notes = []

    for page, (genre, themes, sections) in sorted(WORK.items()):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()

        limit = VERSES[page]
        for head, _ in sections:
            for num in re.findall(r"\d+", head[head.rfind("(v"):]):
                if int(num) > limit:
                    problems.append(f"{page}: {head!r} exceeds {limit} verses")

        if "*" in "".join(p for _, p in sections) + themes:
            problems.append(f"{page}: markdown asterisk in prose")

        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body = pane.group(2)

        # A sublist whose items are all verse ranges is an outline the sections
        # supersede. Anything else is content, and may only be dropped by name.
        items = re.findall(r"<li>(.*?)</li>", body, re.S)
        if items:
            plain = [i for i in items if not VR_ANY.search(i)]
            if plain and page not in DROP_SUBLIST:
                problems.append(f"{page}: sublist has {len(plain)} non-outline "
                                f"item(s); would be lost")
            elif plain:
                notes.append(f"{page}: dropping {len(plain)} non-outline sublist "
                             f"item(s) -- {DROP_SUBLIST[page]}")
            else:
                notes.append(f"{page}: dropping {len(items)}-item verse outline, "
                             f"superseded by sections")

        existing = re.findall(r'<div class="auth-item">.*?</div>', body, re.S)
        if not existing:
            problems.append(f"{page}: no existing auth-items to preserve")
            continue

        drop = DROP_FIELDS.get(page, {})
        kept = []
        for item in existing:
            lab = re.search(r'class="auth-label">([^<]+)</span>', item)
            name = lab.group(1).strip() if lab else None
            # A headless auth-item immediately before a sublist is that list's
            # heading, and goes with it.
            if name is None and items and item.rstrip().endswith(":</div>"):
                notes.append(f"{page}: dropping sublist heading {item[item.find('>')+1:-6]!r}")
                continue
            if name in drop:
                notes.append(f"{page}: dropping {name} -- {drop[name]}")
                continue
            kept.append(item)

        for name in drop:
            if not any(name in i for i in existing):
                problems.append(f"{page}: {name} marked for drop but not present")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for item in kept:
            parts.append("                " + item + "\n")
        parts.append(ITEM.format(label="Classification:", body=genre) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=themes) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if "auth-sublist" in new:
            problems.append(f"{page}: sublist survived into output")
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

    print(f"{'would fold' if check else 'folded'} {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
