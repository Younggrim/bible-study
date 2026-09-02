#!/usr/bin/env python3
"""
Folds the remaining Pauline letter openers onto the target Authorship format:
2 Thessalonians 1, 1 Timothy 1, 2 Timothy 1 and Titus 1.

Three of the four are Pastoral Epistles. Each carried book-introduction fields
with no per-passage exposition. Existing fields are preserved verbatim, including
the page-specific "Chapter 1 Overview:" and Titus's "Crete:", which carry
substance a generic field would not improve on. Added are Classification, Key
Themes, and the verse-range sections these pages lacked.

Prose uses curly quotes for cited terms. No markdown emphasis: asterisks are not
markup in HTML and render as visible characters.

Follows the format in WORKFLOW.md. Writes nothing if any page fails a check.

Usage:
    python3 fold_openers_batch4.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

# Verse totals, asserted so a section range can never overrun the chapter.
VERSES = {"2thessalonians1": 12, "1timothy1": 20, "2timothy1": 18, "titus1": 16}

WORK = {
"2thessalonians1": (
 "Epistle \u2014 Pauline",
 "Faith growing and love abounding under persecution, present suffering as "
 "evidence rather than contradiction, the revelation of Christ in flaming fire, "
 "judgment described as recompense, and a prayer that God would count them worthy",
 [
  ("Greeting from the Same Three (vv.1-2)",
   "Paul, Silvanus and Timothy write again, within months of the first letter and "
   "from the same stay in Corinth. Same team, same church, same pressure. The "
   "greeting is brief and adds nothing new, which suits a letter written to correct "
   "one specific confusion rather than to lay foundations already laid."),
  ("Faith Growing, Love Abounding (vv.3-4)",
   "In the first letter Paul said he had no need to speak of their reputation. Here "
   "he says thanks is \u201cmeet\u201d \u2014 owed. Both verbs are continuous: faith "
   "\u201cgroweth exceedingly\u201d and love \u201caboundeth\u201d, which is a "
   "notable thing to report of a congregation under active persecution. He adds that "
   "he boasts of them in the other churches, giving their suffering a use they had "
   "probably not considered."),
  ("Suffering as Evidence, Not Contradiction (vv.5-7a)",
   "The pastoral core of the chapter. Their persecution is called \u201ca manifest "
   "token of the righteous judgment of God\u201d \u2014 proof that a verdict is "
   "coming, not that God has withdrawn. The reasoning is that a just God will not "
   "leave the account unsettled, and rest is promised to the afflicted in the same "
   "breath as recompense to those afflicting them. Nothing here suggests the trouble "
   "means they got something wrong."),
  ("Revealed in Flaming Fire (vv.7b-9)",
   "The return is described in the language of Old Testament theophany, fire and "
   "angels, bringing recompense on those who do not know God and do not obey the "
   "gospel. \u201cEverlasting destruction\u201d is defined by the passage itself in "
   "the next clause \u2014 \u201cfrom the presence of the Lord\u201d \u2014 which "
   "makes it exclusion rather than annihilation. The definition is supplied on the "
   "spot rather than left to inference."),
  ("Glorified in His Saints (vv.10-12)",
   "The stated purpose of the coming is admiration rather than retribution: that He "
   "may be glorified in His saints and admired in all who believe. The prayer that "
   "closes the chapter asks God to count them worthy of the calling and to fulfil "
   "\u201call the good pleasure of his goodness\u201d, which makes worth something "
   "God supplies rather than something they must produce while under pressure."),
 ]),
"1timothy1": (
 "Epistle \u2014 Pauline, Pastoral Epistle",
 "A charge to stay and correct, endless genealogies set against love from a pure "
 "heart, the lawful use of the law, Paul as chief of sinners and pattern of mercy, "
 "and faith either held or shipwrecked",
 [
  ("Greeting: An Apostle by Commandment (vv.1-2)",
   "Paul is an apostle \u201cby the commandment of God\u201d rather than by "
   "permission, and Timothy is \u201cmy own son in the faith\u201d. The letter is "
   "personal without being private: it would be read aloud in the church, which means "
   "the opening lends Paul's authority to Timothy in front of the very people he has "
   "been left to correct."),
  ("Charged to Stay at Ephesus (vv.3-4)",
   "The reason for writing arrives in the first substantive sentence: remain, and "
   "charge some that they teach no other doctrine. The problem is named as fables and "
   "endless genealogies that raise questions rather than build anything. The objection "
   "is less that the material is false than that it leads nowhere, which is why the "
   "corrective is a purpose rather than a refutation."),
  ("The End of the Commandment Is Love (vv.5-7)",
   "The standard is stated positively: charity out of a pure heart, a good "
   "conscience, and faith unfeigned. The teachers have \u201cswerved\u201d, a word "
   "for missing a mark, and turned aside to vain talk. Paul's assessment is blunt "
   "\u2014 they want to be teachers of the law while understanding neither what they "
   "say nor what they insist on \u2014 and it names confidence without comprehension "
   "as the actual fault."),
  ("What the Law Is For (vv.8-11)",
   "The law is good when used lawfully, and its use is diagnostic rather than "
   "speculative: not made for a righteous man but for the lawless. The vice list "
   "tracks the second table of the Ten Commandments roughly in order, which is the "
   "argument in miniature. The law names what is wrong with people, while the false "
   "teachers were mining it for material."),
  ("Enabled, Though Formerly a Blasphemer (vv.12-14)",
   "Paul turns to himself as the evidence. He was a blasphemer, a persecutor and "
   "injurious, and obtained mercy \u201cbecause I did it ignorantly in unbelief\u201d "
   "\u2014 offered as explanation rather than excuse, since he has just called the "
   "conduct what it was. Grace is described as exceeding abundant, and it arrives "
   "with faith and love rather than in place of them."),
  ("Chief of Sinners, Pattern of Mercy (vv.15-17)",
   "\u201cThis is a faithful saying\u201d marks a formula the churches already used. "
   "Paul puts himself first among sinners in the present tense, not the past, and then "
   "gives the reason it matters: he is a pattern, so that nobody afterward can suppose "
   "themselves past the reach of the same mercy. The doxology in v.17 interrupts the "
   "argument, which is what tends to happen when a writer stops arguing."),
  ("War a Good Warfare: Faith Shipwrecked (vv.18-20)",
   "The charge is renewed in military terms and tied to prophecies spoken over "
   "Timothy earlier. Hymenaeus and Alexander are named as men who put away a good "
   "conscience and made shipwreck of faith \u2014 conscience first, then doctrine, in "
   "that order. The stated aim of handing them over is corrective, \u201cthat they may "
   "learn not to blaspheme\u201d, which sets the temperature for the discipline "
   "instructions later in the letter."),
 ]),
"2timothy1": (
 "Epistle \u2014 Pauline, Pastoral Epistle",
 "Faith inherited through a grandmother and a mother, a gift needing to be stirred "
 "into flame, power and love and a sound mind against fear, a deposit committed and "
 "kept, and companions who turned away while one man did not",
 [
  ("Greeting and a Remembered Household (vv.1-5)",
   "This is almost certainly the last of Paul's surviving letters, written from a "
   "harder imprisonment than the first. He recalls Timothy's tears and traces his "
   "faith through Lois and Eunice, grandmother and mother. Citing two women as the "
   "pedigree for a man holding contested office is unusual, and it is offered as "
   "genuine ground for confidence rather than as warmth before business."),
  ("Stir Up the Gift (v.6)",
   "The verb describes fanning a fire back into flame, which presupposes embers "
   "rather than ashes. The gift is present and needs rousing, not replacing. That "
   "Paul has to say it at all suggests Timothy had gone quiet under exactly the "
   "pressure the rest of the chapter goes on to name."),
  ("Not Fear, But Power, Love, and a Sound Mind (v.7)",
   "The alternative to fear comes in three terms, and the third is not what a list "
   "about courage would predict: a sound mind, self-command, clear judgment. Courage "
   "here is not a surge of feeling but the composure to keep thinking straight, which "
   "is the first thing a frightened leader loses."),
  ("Be Not Ashamed of the Testimony (vv.8-11)",
   "Shame is the chapter's real subject and it is named outright. Timothy is told to "
   "take his share of affliction rather than avoid it, on the ground of a purpose "
   "given \u201cbefore the world began\u201d and a Saviour who \u201chath abolished "
   "death\u201d. Paul states his appointment as preacher and apostle in the same "
   "breath as his chains, declining to treat the two as contradicting each other."),
  ("I Know Whom I Have Believed (v.12)",
   "The confidence rests on a person rather than an outcome \u2014 \u201cI know whom "
   "I have believed\u201d, not what. Whether the thing kept is what Paul entrusted to "
   "God or what God entrusted to Paul, the grammar permits both, and the next verse "
   "turns the same term around so that Timothy is holding a deposit of his own."),
  ("Keep the Deposit (vv.13-14)",
   "The pattern of sound words is to be held onto, and \u201cthat good thing which "
   "was committed unto thee\u201d is guarded by the Holy Ghost rather than by "
   "vigilance alone. The image is of goods left with a custodian: valuable, and not "
   "his. That is how the letter treats doctrine throughout \u2014 something received "
   "and passed on intact rather than developed."),
  ("Onesiphorus, and Those Who Turned Away (vv.15-18)",
   "The chapter ends with names. All those in Asia turned away, Phygellus and "
   "Hermogenes among them. Set against that, Onesiphorus searched Rome until he found "
   "Paul and \u201cwas not ashamed of my chain\u201d \u2014 the same word as v.8, "
   "which is why the story sits here rather than in the closing greetings. He "
   "refreshed Paul often, and the wish for mercy on his household reads like a man "
   "who had learned to count his visitors."),
 ]),
"titus1": (
 "Epistle \u2014 Pauline, Pastoral Epistle",
 "Truth defined by the godliness it produces, a task left unfinished on purpose, "
 "elders qualified by character and household, a bishop able to hold and to refute, "
 "and a local proverb turned into a diagnosis",
 [
  ("Greeting: Truth That Leads to Godliness (vv.1-4)",
   "The longest greeting in the Pastorals, and it does the letter's theological work "
   "before the instructions begin. Truth is identified by what it produces \u2014 "
   "\u201cthe truth which is after godliness\u201d \u2014 and hope rests on a promise "
   "made before the world began by a God \u201cthat cannot lie\u201d. That last phrase "
   "is placed deliberately: lying becomes the subject in v.12. Titus is addressed as "
   "\u201cmine own son after the common faith\u201d."),
  ("Left in Crete to Finish What Was Lacking (v.5)",
   "Titus was left behind on purpose, and the assignment is stated without softening: "
   "set in order the things that are wanting, and ordain elders in every city. The "
   "work was incomplete by design rather than through neglect, which frames the whole "
   "letter as a commission being carried out rather than a failure being repaired."),
  ("Qualified in Household and Character (vv.6-8)",
   "The qualifications start at home \u2014 blameless, husband of one wife, children "
   "not open to the charge of riot or disobedience. Then the negatives: not selfwilled, "
   "not soon angry, not given to wine, no striker, not greedy of filthy lucre. Then "
   "hospitality and self-control. Nothing on the list is a skill or a gift. Every item "
   "is either settled character or an observable record."),
  ("Holding Fast, Able to Convince (v.9)",
   "The single requirement touching capability is stated twice over: holding fast the "
   "faithful word so as to be able both to exhort and to convince those who "
   "contradict. Building up and refuting are treated as one competence, because where "
   "false teachers are active a man who can only encourage cannot protect anyone."),
  ("Vain Talkers Whose Mouths Must Be Stopped (vv.10-11)",
   "The reason for the standard now appears. There are many unruly and vain talkers, "
   "\u201cspecially they of the circumcision\u201d, subverting whole households and "
   "teaching for \u201cfilthy lucre's sake\u201d. The instruction is to stop their "
   "mouths, and the motive assigned is money rather than conviction \u2014 which "
   "explains why argument alone was never going to settle it."),
  ("A Cretan Prophet, and a Sharp Diagnosis (vv.12-14)",
   "Paul quotes a line attributed to Epimenides, himself a Cretan, about Cretans being "
   "liars and idle, and says the testimony is true. It functions as a local proverb "
   "turned against local complacency rather than as a judgment on a people, and the "
   "purpose given in v.13 is repair: \u201crebuke them sharply, that they may be sound "
   "in the faith\u201d. Jewish fables and the commandments of men are named as what "
   "they must stop giving attention to."),
  ("To the Pure All Things Are Pure (vv.15-16)",
   "The chapter closes on the gap between ritual purity and real purity. To the pure "
   "all things are pure, and to the defiled nothing is, because the defilement sits in "
   "the mind and conscience rather than in the object being handled. Verse 16 lands the "
   "charge: they profess to know God and deny Him by their works. That is precisely "
   "what the letter's opening definition of truth \u2014 the truth that produces "
   "godliness \u2014 rules out."),
 ]),
}


def main():
    check = "--check" in sys.argv
    problems = []
    planned = {}

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

        planned[path] = new

    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1

    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)

    print(f"{'would fold' if check else 'folded'} {len(planned)} Pauline openers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
