#!/usr/bin/env python3
"""
Folds five Pauline openers onto the target Authorship format:
Galatians 1, Ephesians 1, Philippians 1, Colossians 1 and 1 Thessalonians 1.

Each is the opening chapter of a Pauline letter carrying book-introduction fields
with no per-passage exposition. Existing fields are preserved verbatim, including
the page-specific "The Crisis:", "Chapter 1 Content:", "Chapter 1 Overview:" and
"Audience:", all of which carry substance a generic field would not improve on.
Added are Classification, Key Themes, and the verse-range sections these pages
lacked.

Prose uses curly quotes for cited terms. No markdown emphasis: asterisks are not
markup in HTML and render as visible characters.

Follows the format in WORKFLOW.md. Refuses to write on div imbalance.

Usage:
    python3 fold_openers_batch3.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

# Verse totals, asserted so a section range can never overrun the chapter.
VERSES = {"galatians1": 24, "ephesians1": 23, "philippians1": 30,
          "colossians1": 29, "1thessalonians1": 10}

WORK = {
"galatians1": (
 "Epistle \u2014 Pauline",
 "Apostleship received directly rather than through men, a gospel that admits no "
 "alternative, astonishment in place of thanksgiving, a former life of zeal in "
 "Judaism, and a chronology offered as evidence of independence",
 [
  ("Greeting: An Apostle Not Sent by Men (vv.1-5)",
   "Paul qualifies the word \u201capostle\u201d in his first breath \u2014 \u201cnot "
   "of men, neither by man, but by Jesus Christ\u201d. His other letters state his "
   "apostleship without defending it, and the immediate defence here signals what is "
   "being disputed. The greeting also states the gospel before the argument for it "
   "begins: Christ \u201cgave himself for our sins, that he might deliver us from "
   "this present evil world\u201d. Everything contested in the letter is already "
   "present in the salutation."),
  ("No Other Gospel: Astonishment in Place of Thanksgiving (vv.6-9)",
   "Paul's letters open with thanksgiving. This one does not, and to first readers "
   "the omission would have been loud. \u201cI marvel that ye are so soon "
   "removed\u201d stands where gratitude belongs. The rival message is called "
   "\u201canother gospel: which is not another\u201d \u2014 a different thing wearing "
   "a borrowed name. The anathema of vv.8-9 is pronounced twice, the repetition "
   "deliberate, and it falls on the message and its messengers rather than on the "
   "Galatians themselves, who are being warned rather than condemned."),
  ("Not Seeking to Please Men (vv.10-12)",
   "Behind the rhetorical question lies the accusation that Paul trimmed his "
   "requirements to make converts easier to win among Gentiles. His answer is that "
   "the gospel he preaches is \u201cnot after man\u201d: he neither received it from "
   "a human source nor was taught it, but received it by revelation. That claim is "
   "not left as an assertion \u2014 the remainder of the chapter is the evidence for "
   "it, laid out as dates and movements."),
  ("His Former Life in the Jews' Religion (vv.13-14)",
   "Paul produces his own past as exhibit rather than confession. He persecuted the "
   "church \u201cand wasted it\u201d, and outpaced his contemporaries in zeal for "
   "ancestral tradition. The argument is about direction of travel: no human "
   "persuasion produced this change, because he was moving hard the other way and "
   "had every incentive to keep going."),
  ("Separated from the Womb, Sent to the Gentiles (vv.15-17)",
   "The calling is dated before his birth and attributed to God's pleasure rather "
   "than to any search of his own. The detail that carries the argument is what he "
   "did next: he went into Arabia, and did not go up to Jerusalem to those who were "
   "apostles before him. He is establishing that his commission never passed through "
   "Jerusalem for authorisation, because a commission that needed approval could be "
   "revised by whoever granted it."),
  ("Three Years Later, Fifteen Days with Peter (vv.18-20)",
   "The first Jerusalem visit comes three years on, lasts fifteen days, and involves "
   "Peter and James alone. The precision is the point: fifteen days is a visit, not "
   "an apprenticeship, and too short to account for what he preaches. Verse 20's "
   "oath \u2014 \u201cbefore God, I lie not\u201d \u2014 shows that these were "
   "contested facts rather than uncontroversial background."),
  ("Unknown by Face, Glorified in Report (vv.21-24)",
   "Paul was personally unknown to the churches of Judea, which knew him only by "
   "report: the man who once destroyed the faith now preaches it. \u201cThey "
   "glorified God in me\u201d closes the chapter with an irony aimed at his critics. "
   "The congregations nearest Jerusalem accepted him on the evidence of the change "
   "itself, which is precisely what the teachers in Galatia would not do."),
 ]),
"ephesians1": (
 "Epistle \u2014 Pauline, Prison Epistle",
 "Blessing chosen before the foundation of the world, adoption and redemption, the "
 "mystery of all things gathered up in Christ, the Spirit given as a deposit, and "
 "power measured by the resurrection",
 [
  ("Greeting, and a Textual Question (vv.1-2)",
   "\u201cAt Ephesus\u201d is missing from the earliest manuscripts, which has long "
   "suggested a circular letter carried among the churches of Asia with the "
   "destination left open. The contents fit that reading: no individuals are "
   "greeted, no local dispute is addressed, and although Paul spent some three years "
   "in Ephesus he writes as though his readers know of him by report (3:2). The "
   "result is a letter about the church as such rather than about one congregation."),
  ("Chosen Before the Foundation of the World (vv.3-6)",
   "Verses 3-14 form a single sentence in Greek, an accumulating blessing rather "
   "than a chain of arguments. Election is dated before creation, and its stated "
   "purpose is character \u2014 \u201cthat we should be holy and without blame before "
   "him in love\u201d \u2014 not status alone. Adoption follows, described as "
   "according to God's good pleasure, and the refrain arrives for the first of three "
   "times: \u201cto the praise of the glory of his grace\u201d."),
  ("Redemption Through His Blood (vv.7-8)",
   "Redemption and forgiveness are named together and grounded in blood rather than "
   "in decision, measured \u201caccording to the riches of his grace\u201d. The verb "
   "in v.8 describes grace not merely supplied but lavished, abounding toward its "
   "recipients. The scale language matters in a letter that will shortly ask readers "
   "to grasp dimensions they cannot measure."),
  ("The Mystery Made Known: All Things Gathered Up (vv.9-10)",
   "The mystery is not information withheld but a plan now disclosed. \u201cGather "
   "together in one\u201d renders a term used of summing a column of figures and "
   "bringing it to a single head, and its stated scope is everything in heaven and "
   "on earth. This is the widest horizon in the letter, and Paul states it before "
   "asking anything of anyone \u2014 the pattern of the whole epistle, three chapters "
   "of what is true before three of what to do."),
  ("An Inheritance Obtained, a Spirit Given as Deposit (vv.11-14)",
   "Jew and Gentile are set deliberately side by side: \u201cwe\u201d who first "
   "trusted, and \u201cye also\u201d who heard and believed. The Spirit is called the "
   "earnest of the inheritance, a commercial word for a down payment that legally "
   "commits the payer to the remainder. Sealing indicates ownership and security "
   "together. The long sentence closes with its refrain a third time, \u201cunto the "
   "praise of his glory\u201d."),
  ("Paul's Prayer: Eyes to See What Is Already True (vv.15-19)",
   "Having catalogued the blessings, Paul prays not for additions but for "
   "perception: a spirit of wisdom and revelation, \u201cthe eyes of your "
   "understanding being enlightened\u201d, that they may know the hope, the riches of "
   "the inheritance, and the greatness of the power. Nothing requested is new. The "
   "prayer assumes the problem is not lack of provision but failure to recognise what "
   "has been given."),
  ("The Measure of the Power: Raised and Seated (vv.20-23)",
   "The power is quantified by an event rather than described in the abstract: the "
   "same working that raised Christ and seated Him above every name, in this age and "
   "the age to come. The chapter then ties that exalted position to the church, given "
   "to Him as a body and called \u201cthe fulness of him that filleth all in "
   "all\u201d. Headship is exercised on the church's behalf, not merely over it, "
   "which is why the argument can move from cosmic authority to ordinary "
   "congregations without changing subject."),
 ]),
"philippians1": (
 "Epistle \u2014 Pauline, Prison Epistle",
 "Partnership in the gospel from the first day, a good work God will finish, "
 "imprisonment turned to advance, rivals preaching Christ from mixed motives, life "
 "and death both gain, and suffering described as a gift",
 [
  ("Greeting: Servants, Bishops, and Deacons (vv.1-2)",
   "Paul and Timothy are introduced as \u201cservants\u201d rather than apostles, "
   "the only letter to open this way, and this is the only greeting to name church "
   "officers directly. Both details suit a letter written to friends rather than to a "
   "crisis, and they set the register for a chapter that persuades by affection "
   "rather than by asserting authority."),
  ("Confident of This Very Thing (vv.3-6)",
   "The thanksgiving names a partnership running \u201cfrom the first day until "
   "now\u201d, roughly a decade by the time of writing. Verse 6 locates his "
   "confidence in the one who started the work rather than in the Philippians' "
   "consistency: \u201che which hath begun a good work in you will perform it until "
   "the day of Jesus Christ\u201d. The promise is corporate before it is personal, "
   "addressed to a church he expects God to finish."),
  ("Partakers of Grace, in Bonds and in Defence (vv.7-8)",
   "The Philippians are described as sharing his grace in both his imprisonment and "
   "his legal defence, which is how Paul understands the money they sent: not charity "
   "but participation in the same work. The affection of v.8 is unusually direct even "
   "for this letter, and he calls God to witness it, which suggests he means it as "
   "more than a courtesy."),
  ("Prayer for Love That Discerns (vv.9-11)",
   "Love is asked to abound and then immediately qualified \u2014 \u201cin knowledge "
   "and in all judgment\u201d. The aim is the capacity to approve what is excellent "
   "and to arrive sincere and without offence at the day of Christ. Love and "
   "discernment are not set against each other here; the prayer expects the first to "
   "produce the second."),
  ("The Gospel Advanced by a Chain (vv.12-14)",
   "Paul reframes his confinement as forward motion. His chains have become known "
   "\u201cin all the palace\u201d \u2014 the praetorium, the imperial guard cycling "
   "through his custody \u2014 so the gospel entered a place no travelling preacher "
   "could reach. The second effect is on other believers, who were made bolder rather "
   "than more cautious by seeing what happened to him, which is the opposite of what "
   "an imprisoned leader would normally produce."),
  ("Christ Preached, Whatever the Motive (vv.15-18)",
   "Some preach from goodwill and some from envy and strife, intending to add to his "
   "affliction while he cannot answer. Paul does not defend himself; he compares "
   "outcomes and stops there: \u201cChrist is preached; and I therein do rejoice\u201d. "
   "He is not endorsing the motive, and elsewhere he is fierce about false content. "
   "The distinction he draws is between rivals preaching truth badly and teachers "
   "preaching something else."),
  ("To Live Is Christ, To Die Is Gain (vv.19-26)",
   "The dilemma is genuine rather than rhetorical \u2014 he is \u201cin a strait "
   "betwixt two\u201d, pressed from both sides. \u201cDepart\u201d in v.23 is a term "
   "used of loosing a ship from its moorings. What settles the question is not his "
   "preference but their need, and he expects release for their \u201cfurtherance and "
   "joy of faith\u201d. The calculus assumes that death is gain and therefore not the "
   "worst outcome available, which is what makes the choice difficult."),
  ("Citizens Standing Fast, Given the Gift of Suffering (vv.27-30)",
   "\u201cLet your conversation be as it becometh the gospel\u201d uses a civic verb "
   "\u2014 live as citizens \u2014 which lands pointedly in Philippi, a Roman colony "
   "proud of its status. The chapter closes with suffering placed alongside believing "
   "as something granted: \u201cit is given you in the behalf of Christ\u201d. "
   "Hardship is treated as a gift rather than an accident or a failure, and Paul "
   "notes that it is a conflict they share with him rather than one he has escaped."),
 ]),
"colossians1": (
 "Epistle \u2014 Pauline, Prison Epistle",
 "A church Paul had never visited, faith and love resting on hope laid up in "
 "heaven, transfer out of darkness into a kingdom, Christ as image and firstborn "
 "holding creation together, reconciliation through the blood of the cross, and a "
 "mystery now disclosed",
 [
  ("Greeting to a Church He Had Not Seen (vv.1-2)",
   "Paul writes to a congregation he neither founded nor visited (2:1), planted "
   "through Epaphras during the Ephesian years. That distance shapes the letter. He "
   "has to establish common ground before correcting anything, which is why this "
   "chapter spends most of its length describing Christ and barely mentions the error "
   "it exists to answer."),
  ("Faith, Love, and a Hope Laid Up (vv.3-8)",
   "The thanksgiving orders the triad deliberately: faith and love spring from hope "
   "\u201claid up for you in heaven\u201d, the settled thing on which the other two "
   "rest. The gospel is described as bearing fruit and increasing throughout the "
   "world, which quietly answers a teaching that offered something additional to a "
   "select few. Epaphras is named as their source and commended, which matters for a "
   "church about to be told its teachers are wrong."),
  ("Prayer: Filled with Knowledge, Walking Worthy (vv.9-12)",
   "The request is for knowledge of God's will issuing in a walk that pleases Him, "
   "with fruitfulness, growth and strengthening. Verse 11 attaches the strengthening "
   "to patience and longsuffering rather than to visible achievement, and v.12 turns "
   "it toward thanksgiving. The inheritance language introduced here is what the next "
   "two verses explain."),
  ("Delivered and Translated (vv.13-14)",
   "Two verbs describe a change of jurisdiction: delivered from the power of "
   "darkness, translated into the kingdom of His Son. The second was used of "
   "relocating a population from one territory to another, an act performed on people "
   "rather than by them. Redemption and forgiveness are named as what the transfer "
   "secured, and the description of the one who carried it out follows immediately."),
  ("The Image of the Invisible God (vv.15-17)",
   "\u201cFirstborn of every creature\u201d asserts rank and right rather than "
   "origin, as the following clause makes plain: all things were created by Him, "
   "including the thrones and powers the Colossian teaching was preoccupied with. He "
   "is before all things, and \u201cby him all things consist\u201d \u2014 held "
   "together continuously, not merely set in motion once. The argument leaves no gap "
   "for an intermediary to fill, which is the whole point."),
  ("Head of the Body, Firstborn from the Dead (vv.18-20)",
   "The second half of the hymn moves from creation to the church, with the stated "
   "purpose \u201cthat in all things he might have the preeminence\u201d. "
   "Reconciliation extends to all things in heaven and earth, and the means is named "
   "plainly and physically: \u201cthe blood of his cross\u201d. A passage of cosmic "
   "scope ends at an execution, and the juxtaposition is deliberate rather than "
   "incidental."),
  ("Once Enemies, Now to Be Presented Holy (vv.21-23)",
   "The sweep narrows to the readers: alienated, enemies in mind, and now reconciled "
   "in order to be presented holy and unblameable. Verse 23's \u201cif ye continue in "
   "the faith\u201d is the letter's first note of warning, mild at this stage and "
   "developed in chapter 2. It rests on the hope of the gospel they have already "
   "heard rather than on anything further being required of them."),
  ("Christ in You: The Mystery Now Revealed (vv.24-29)",
   "Paul speaks of filling up \u201cthat which is behind of the afflictions of "
   "Christ\u201d, his own suffering understood as service to the body rather than as "
   "any supplement to the cross. The mystery hidden through ages is stated in four "
   "words \u2014 \u201cChrist in you, the hope of glory\u201d \u2014 and its scope is "
   "\u201cevery man\u201d, repeated three times in v.28 against any teaching reserved "
   "for insiders. His labour is described with a word drawn from athletic contest, "
   "which is how he characterises the work of getting people to maturity."),
 ]),
"1thessalonians1": (
 "Epistle \u2014 Pauline",
 "Faith, love and hope shown in work, labour and patience, election evidenced by "
 "the gospel&#x27;s effect, imitation producing further imitation, a report that "
 "travelled ahead of the apostles, and a turn from idols to serving and waiting",
 [
  ("Greeting from Three Names (v.1)",
   "Paul, Silvanus and Timothy write jointly \u2014 the team present when the church "
   "was founded. This is likely the earliest of Paul's surviving letters, written "
   "from Corinth within months of his forced departure from Thessalonica. That timing "
   "makes the confidence of the chapter notable: the congregation was only weeks old "
   "and had been left under pressure almost immediately."),
  ("Work of Faith, Labour of Love, Patience of Hope (vv.2-3)",
   "The triad appears here for the first time in Paul's letters, and each term is "
   "tied to something visible. Faith produces work, love produces labour, hope "
   "produces endurance. He remembers not their sentiments but their effects, which "
   "sets the method for the rest of the chapter \u2014 everything he commends is "
   "something that could be observed from outside."),
  ("Election Known by Its Effect (vv.4-5)",
   "Paul says he knows their election, and the evidence offered is not their "
   "profession but the manner of the gospel's arrival: \u201cnot in word only, but "
   "also in power, and in the Holy Ghost, and in much assurance\u201d. He adds the "
   "conduct of the messengers as part of that evidence, since what the Thessalonians "
   "became was bound up with what they had watched."),
  ("Followers Who Became Examples (vv.6-7)",
   "They became imitators of the apostles and of the Lord, receiving the word "
   "\u201cin much affliction, with joy of the Holy Ghost\u201d \u2014 the affliction "
   "and the joy named in the same breath rather than set against each other. The "
   "result reverses the direction: imitators became a pattern themselves for "
   "believers across Macedonia and Achaia."),
  ("The Word Sounded Out (v.8)",
   "The verb pictures a sound carried outward, as of a trumpet or an echo off a "
   "hillside. The report travelled beyond the province so thoroughly that Paul says "
   "he had no need to speak of it himself. Their reputation preceded his account of "
   "them, which for a church of a few weeks' standing is a considerable claim to "
   "make."),
  ("Turned, Serving, Waiting (vv.9-10)",
   "Paul quotes the report itself, and it summarises conversion in three movements: "
   "they turned from idols, to serve the living and true God, and to wait for His Son "
   "from heaven. The turning is finished, the serving present, the waiting ongoing. "
   "The chapter ends on deliverance \u201cfrom the wrath to come\u201d, introducing "
   "the return of Christ that the letter keeps circling back to."),
 ]),
}

RANGE = re.compile(r"\(vv?\.(\d+)[a-z]?(?:[-,:\s]+(\d+)[a-z]?)*\)")


def main():
    check = "--check" in sys.argv
    changed = 0
    problems = []

    for page, (genre, themes, sections) in sorted(WORK.items()):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()

        # No section may cite a verse beyond the chapter's actual length.
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

        existing = re.findall(r'<div class="auth-item">.*?</div>', pane.group(2), re.S)
        if not existing:
            problems.append(f"{page}: no existing auth-items to preserve")
            continue

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for item in existing:
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

        changed += 1
        if not (check or problems):
            open(path, "w", encoding="utf-8").write(new)

    verb = "would fold" if check else "folded"
    print(f"{verb} {changed} Pauline openers")
    for p in problems:
        print(f"    {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
