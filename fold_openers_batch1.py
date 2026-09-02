#!/usr/bin/env python3
"""
Folds the five single-chapter books onto the target Authorship format:
Philemon, 2 John, 3 John, Jude and Obadiah.

These are grouped because each is an entire book in one chapter, so finishing
them completes five books rather than leaving five partials.

Existing book-introduction fields are kept as they are. Recipient, Purpose,
Theme, Significance and Crete carry real book-level substance and are more
specific than a generic Historical Context would be, so they stay. What gets
added is Classification, Key Themes where absent, and the verse-range
exposition sections these pages had none of.

Follows the format in WORKFLOW.md. Refuses to write on div imbalance, which is
the guard that caught a dropped closing tag on the first Jonah run.

Usage:
    python3 fold_openers_batch1.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

# page -> (classification, key themes or None, [(heading with verses, prose)])
WORK = {
"philemon1": (
 "Epistle \u2014 Personal Letter",
 "Intercession for another, a slave received as a brother, moral persuasion "
 "instead of apostolic command, the gospel reshaping a household, and a debt "
 "voluntarily assumed",
 [
  ("Greeting: A Prisoner, Not an Apostle (vv.1-3)",
   "Paul opens by calling himself \u201ca prisoner of Jesus Christ\u201d rather than "
   "an apostle, which is unusual for him and sets the tone for everything that "
   "follows. He is about to ask a favour, not issue a directive, and he begins by "
   "putting aside the authority he could have used. The letter is addressed to "
   "Philemon, to Apphia and Archippus, and to the church meeting in Philemon's "
   "house \u2014 so a private matter is being raised in front of the congregation "
   "that gathers under that roof. That is deliberate pressure, gently applied."),
  ("Thanksgiving: Naming What Is Already True (vv.4-7)",
   "Before raising the request Paul commends what he already knows of Philemon: "
   "his love, his faith, and the refreshment he has brought to \u201cthe bowels of "
   "the saints\u201d. This is not flattery laid down to soften a blow. Paul is "
   "describing the character on which he is about to rely, and v.6 states his hope "
   "that Philemon's faith will become effective through acknowledging every good "
   "thing in him. The argument of the letter is that a man like this will know what "
   "to do without being told."),
  ("The Request: Receive Him as a Brother (vv.8-16)",
   "Now the substance. Onesimus was Philemon's slave, had run away, and has since "
   "become a Christian under Paul's ministry in Rome. Paul says plainly that he "
   "could command \u2014 \u201cI might be much bold in Christ to enjoin thee\u201d "
   "\u2014 and then refuses to, asking instead \u201cfor love's sake\u201d. He puns "
   "on the name, which means useful: once unprofitable, now profitable. The pivot "
   "is v.16: receive him \u201cnot now as a servant, but above a servant, a brother "
   "beloved\u201d. Paul does not stage a public argument about the institution of "
   "slavery; he makes it impossible for this Christian household to keep treating "
   "this particular man as property."),
  ("Paul Assumes the Debt (vv.17-21)",
   "\u201cIf he hath wronged thee, or oweth thee ought, put that on mine "
   "account.\u201d Paul writes it in his own hand as a legally weighted promissory "
   "note, then adds the quiet counter-reckoning that Philemon owes him his own "
   "spiritual life. Whatever Onesimus took when he fled, Paul will cover. Christian "
   "readers have long heard the shape of substitution here: one party voluntarily "
   "absorbing another's debt so the relationship can be restored. Paul closes with "
   "confidence that Philemon will do \u201cmore than I say\u201d, which most likely "
   "means manumission without naming it."),
  ("Closing: Prepare Me a Lodging (vv.22-25)",
   "Paul asks that a guest room be readied, since he expects to be released and to "
   "visit. It is an affectionate note and also a practical one: the man who wrote "
   "this letter intends to see how it was received. Greetings follow from "
   "Epaphras, Mark, Aristarchus, Demas and Luke, the same circle named in "
   "Colossians, which is part of why the two letters are usually dated together and "
   "read as having travelled by the same hand."),
 ]),
"2john1": (
 "Epistle \u2014 Personal Letter",
 "Truth and love held together, walking in the commandments, the test of "
 "confessing Christ come in the flesh, and hospitality withheld from those who "
 "carry a false gospel",
 [
  ("Greeting: The Elder to the Elect Lady (vv.1-3)",
   "The writer calls himself simply \u201cthe elder\u201d, and the vocabulary "
   "throughout \u2014 truth, love, commandment, abiding \u2014 matches 1 John and "
   "the Fourth Gospel closely enough that the traditional attribution to the apostle "
   "John has strong support. The addressee, \u201cthe elect lady and her "
   "children\u201d, is read either as an individual woman and her household or as a "
   "local congregation addressed figuratively; both readings have a long history and "
   "the letter works either way. \u201cTruth\u201d appears five times in the first "
   "four verses, which signals the concern before the argument begins."),
  ("Walking in Truth and Love (vv.4-6)",
   "John is glad to find her children \u201cwalking in truth\u201d, then restates "
   "the commandment that runs through all his writing: that we love one another, "
   "which is not new but was there \u201cfrom the beginning\u201d. Verse 6 closes "
   "the loop tightly \u2014 love is defined as walking in His commandments, and the "
   "commandment is that we walk in love. The two cannot be separated into rival "
   "priorities, which matters because the rest of the letter is about refusing "
   "someone, and John wants that refusal understood as an act of love rather than "
   "an exception to it."),
  ("The Deceivers: Christ Come in the Flesh (vv.7-9)",
   "The problem is named: many deceivers who do not confess that Jesus Christ has "
   "come in the flesh. This is the early docetic denial, holding that the Son only "
   "appeared to be human, and John treats it as disqualifying rather than as a "
   "difference of opinion. His test is Christological and specific. Verse 9 draws "
   "the line: whoever goes beyond the doctrine of Christ does not have the Father, "
   "and whoever abides in it has both. Innovation past the apostolic teaching is "
   "presented as loss, not progress."),
  ("Do Not Receive Them (vv.10-11)",
   "\u201cIf there come any unto you, and bring not this doctrine, receive him not "
   "into your house, neither bid him God speed.\u201d In a movement whose teachers "
   "travelled and depended on household hospitality, this is not social rudeness "
   "but the withdrawal of logistical support. Offering a bed and a blessing would "
   "have made the host a partner in the teaching being carried on to the next town, "
   "which is exactly what v.11 says. The command is narrow \u2014 it concerns those "
   "propagating a denial of the incarnation, not anyone with whom one disagrees."),
  ("Closing: Face to Face (vv.12-13)",
   "John has more to say and declines to write it, preferring to come and speak "
   "\u201cface to face, that our joy may be full\u201d. The same preference appears "
   "at the end of 3 John. It is a reminder that these letters were stopgaps between "
   "visits rather than treatises, which is part of why they are so short and so "
   "pointed. Greetings from the children of her elect sister close the letter."),
 ]),
"3john1": (
 "Epistle \u2014 Personal Letter",
 "Hospitality to travelling teachers, walking in truth as a cause for joy, one "
 "man's abuse of authority in a congregation, and reputation as evidence of "
 "character",
 [
  ("Greeting and the Prayer for Gaius (vv.1-4)",
   "The elder writes to Gaius, whom he loves \u201cin the truth\u201d. The wish that "
   "he may prosper and be in health \u201ceven as thy soul prospereth\u201d is a "
   "conventional epistolary greeting of the period rather than a promise of "
   "prosperity, and it carries an implicit compliment: John can safely wish that "
   "Gaius's circumstances match his spiritual condition. Verse 4 gives the writer's "
   "settled joy \u2014 no greater gladness than hearing that his children walk in "
   "truth."),
  ("Commendation: Receiving the Brethren (vv.5-8)",
   "Gaius has hosted travelling teachers who were strangers to him, and John asks "
   "him to send them on \u201cafter a godly sort\u201d, meaning properly provisioned "
   "for the next stage. These men took nothing from the Gentiles they went to, so "
   "support from believing households was the whole of their income. Verse 8 draws "
   "the conclusion that gives Christian hospitality its dignity: those who receive "
   "them become \u201cfellowhelpers to the truth\u201d. The host shares in the work "
   "he makes possible."),
  ("Diotrephes: Loving Preeminence (vv.9-11)",
   "Against Gaius stands Diotrephes, who \u201cloveth to have the preeminence\u201d. "
   "The charges are concrete: he ignores John's letters, speaks against him, refuses "
   "the travelling brethren himself, and expels from the congregation anyone who "
   "receives them. Note what is not alleged \u2014 no false doctrine is named. The "
   "problem is a man using position to control a church, which the New Testament "
   "treats as seriously as error. Verse 11 gives the response: do not imitate evil "
   "but good, since conduct reveals whose one is."),
  ("Demetrius and the Closing (vv.12-14)",
   "Demetrius is commended, with his reputation attested by the congregation, by "
   "the truth itself, and by John. In a period when a stranger arriving with a "
   "letter could be either a genuine teacher or an opportunist, that layered "
   "testimony was how a church decided whom to trust. As in 2 John the writer stops "
   "short, preferring to speak in person, and closes with peace and greetings by "
   "name \u2014 a reminder that these were real congregations of people who knew one "
   "another."),
 ]),
"jude1": (
 "Epistle \u2014 General",
 "Contending for the faith once delivered, false teachers who infiltrate rather "
 "than announce themselves, judgment illustrated from history, and believers kept "
 "by God while keeping themselves",
 [
  ("Greeting and the Change of Subject (vv.1-4)",
   "Jude introduces himself as the servant of Jesus Christ and brother of James, "
   "which identifies him as a half-brother of Jesus who declines to say so. He "
   "intended to write about \u201cthe common salvation\u201d and changed course "
   "because circumstances demanded it: certain men have crept in unnoticed, turning "
   "grace into licence and denying the Lord. Hence the letter's charge to "
   "\u201cearnestly contend for the faith which was once delivered unto the "
   "saints\u201d \u2014 a faith with fixed content, handed over rather than "
   "developed."),
  ("Three Examples of Judgment (vv.5-7)",
   "Jude reaches for three cases his readers already knew: Israel saved out of "
   "Egypt and then destroyed in the wilderness for unbelief, angels who abandoned "
   "their proper place, and Sodom and Gomorrah. The first is the sharpest \u2014 "
   "being delivered is not the same as arriving. Together they establish that "
   "privileged position does not exempt anyone from judgment, which is precisely "
   "what the false teachers were claiming."),
  ("The Character of the Intruders (vv.8-16)",
   "The description is unsparing: they despise authority, speak of what they do not "
   "understand, and follow instinct rather than the Spirit. Jude sets Michael's "
   "restraint in disputing over the body of Moses against their recklessness, then "
   "piles up images \u2014 clouds without water, trees without fruit, wandering "
   "stars. Cain, Balaam and Korah supply the pattern of envy, greed and rebellion. "
   "Verses 14-15 quote a prophecy attributed to Enoch, which Jude uses as a "
   "recognisable witness to coming judgment without thereby settling anything about "
   "that book's status."),
  ("Building Yourselves Up (vv.17-23)",
   "The tone turns from warning to instruction, and it is practical: remember what "
   "the apostles said, build yourselves up in the faith, pray in the Holy Spirit, "
   "keep yourselves in the love of God, wait for mercy. Then the harder part \u2014 "
   "how to treat those already affected. Jude distinguishes cases: have compassion "
   "on some, and save others \u201cwith fear, pulling them out of the fire\u201d, "
   "hating the garment spotted by the flesh. Rescue is expected, and so is care "
   "about being pulled in while attempting it."),
  ("Doxology: Able to Keep You (vv.24-25)",
   "The letter that began by describing believers as \u201cpreserved in Jesus "
   "Christ\u201d ends by ascribing that preservation to God: able to keep you from "
   "falling and to present you faultless. Set beside the command in v.21 to keep "
   "yourselves in the love of God, the two are held together rather than played off "
   "\u2014 the same tension the whole letter maintains. It is one of the fullest "
   "doxologies in the New Testament, and after twenty-three verses of warning it "
   "lands on security rather than fear."),
 ]),
"obadiah1": (
 "Prophetic Oracle",
 "Judgment on Edom for pride and for gloating over a brother's ruin, the folly of "
 "trusting inaccessible terrain, measure-for-measure recompense, and the day of "
 "the LORD reaching every nation",
 [
  ("The Vision Against Edom (vv.1-4)",
   "The shortest book in the Old Testament opens with a report from among the "
   "nations: rise up against Edom. The Edomites were descendants of Esau, Jacob's "
   "twin, which makes this a family matter and gives the book its edge. Their "
   "strongholds lay in the rock country south-east of the Dead Sea, terrain later "
   "associated with Petra, where settlements sat behind cliffs and narrow "
   "approaches. Verse 3 names the sin as pride and locates its source in "
   "geography \u2014 \u201cthou that dwellest in the clefts of the rock\u201d \u2014 "
   "and v.4 answers it: though you build among the stars, I will bring you down."),
  ("Plundered and Betrayed (vv.5-9)",
   "The imagery is of theft that leaves nothing, unlike thieves who take only what "
   "they can carry or grape-gatherers who miss a few clusters. Edom will be "
   "stripped bare. The bitterest stroke is that the betrayal comes from allies: the "
   "men of her own confederacy set the trap. Edom's celebrated wise men and mighty "
   "men are specifically named as failing, since the things a nation trusts are "
   "exactly the things judgment removes first."),
  ("The Charge: You Stood By (vv.10-14)",
   "Here is the case against Edom, and it is not conquest but complicity. When "
   "foreigners breached Jerusalem, Edom \u201cstood on the other side\u201d, looked "
   "on, rejoiced, entered the gate, took the spoil, and cut off those trying to "
   "escape. Eight prohibitions in the past tense list what should not have been "
   "done, each escalating from watching to profiting to blocking the fugitives. The "
   "repeated phrase \u201cin the day\u201d hammers the point. Doing nothing was the "
   "first step, not a neutral position."),
  ("The Day of the LORD (vv.15-18)",
   "The scope widens from Edom to \u201call the heathen\u201d, and the principle is "
   "stated plainly: as you have done, it shall be done unto you. Judgment is "
   "measured, not arbitrary. Verse 17 turns toward deliverance \u2014 on Mount Zion "
   "there shall be deliverance and holiness \u2014 and v.18 gives the outcome in "
   "stark terms: the house of Jacob will be fire, the house of Esau stubble, and "
   "there shall not be any remaining of the house of Esau. The nation that gloated "
   "over a brother's fall does not outlast him."),
  ("Possession and Kingdom (vv.19-21)",
   "The book closes with restored borders and returning exiles, a list of regions "
   "reclaimed. The final clause is the point of the whole oracle: \u201cthe kingdom "
   "shall be the LORD's.\u201d Edom's collapse is not presented as Israel's revenge "
   "but as one instance of a wider settlement in which every arrogant claim gives "
   "way. For a small book almost entirely occupied with judgment on one neighbour, "
   "it ends by looking well past that neighbour."),
 ]),
}


def main():
    check = "--check" in sys.argv
    changed = 0
    problems = []

    for page, (genre, themes, sections) in sorted(WORK.items()):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()

        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body = pane.group(2)

        # keep every existing auth-item exactly as written
        existing = re.findall(r'<div class="auth-item">.*?</div>', body, re.S)
        if not existing:
            problems.append(f"{page}: no existing auth-items to preserve")
            continue

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for item in existing:
            parts.append("                " + item + "\n")
        parts.append(ITEM.format(label="Classification:", body=genre) + "\n")
        if themes:
            parts.append(ITEM.format(label="Key Themes:", body=themes) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        # the captured region includes the pane's own closing tag
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue

        changed += 1
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    verb = "would fold" if check else "folded"
    print(f"{verb} {changed} single-chapter books")
    for p in problems:
        print(f"    {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
