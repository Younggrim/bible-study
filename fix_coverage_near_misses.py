#!/usr/bin/env python3
"""
Closes the 45 pages that the conformance audit flags for small defects: 35 missing
between one and three verses, and 10 whose only fault is an overlapping range or an
all-capital label.

These are the pages that look finished and are not, which makes them the worst kind
of defect to leave standing.

Four kinds of repair, and the distinction matters:

  extend   widen a section's range AND append prose describing the verses taken in.
           Widening a label without describing the verse would only silence the
           audit, so every extend here carries text.
  insert   add a section for verses no existing section can honestly absorb, such as
           1corinthians8 vv.4-6 on the one God and one Lord, or philippians4's
           closing greetings.
  merge    fold a nested sub-point back into its parent, for the cases where a
           sub-point was promoted to a sibling and the same verses were therefore
           described twice: ruth2 v.12 inside vv.4-16, deuteronomy15 vv.16-17 inside
           vv.12-18, and six more.
  relabel  take the shouting out of a label. leviticus26 ran CYCLE 1 to CYCLE 5,
           deuteronomy33 shouted eleven tribe names, deuteronomy18 shouted MOSES and
           PROPHET, deuteronomy6 shouted SHEMA. None is an acronym or a KJV
           typographical convention, so all are written normally.

Where an umbrella section sat over its own sub-points (genesis5 vv.1-31 over Noah's
birth at vv.28-32, joshua8 vv.1-8 over the ambush at vv.3-23, job7, ephesians3,
revelation9, judges21, numbers26) the umbrella is narrowed to the verses it alone
covers rather than deleted, because its prose is about those verses.

Usage:
    python3 fix_coverage_near_misses.py [--check]
"""
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
ITEM_RE = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')
RANGE_IN_LABEL = re.compile(r"\(vv?\.[^)]*\)(?=\s*:?\s*$)")

# ("extend", label prefix, new range, prose appended)
# ("insert", after label prefix or "" for before first section, label, prose)
# ("merge",  nested label prefix, parent label prefix)
# ("relabel", label prefix, replacement label without trailing colon)
OPS = {
"1corinthians8": [
 ("insert", "Knowledge vs. Love", "One God, One Lord (vv.4-6)",
  "Paul states the position he has just qualified. We know that an idol is nothing at "
  "all in the world, and that there is no God but one. Then the concession, that there "
  "are so-called gods in heaven and on earth, and the confession set against it: for us "
  "there is but one God, the Father, from whom all things came, and one Lord, Jesus "
  "Christ, through whom all things came. The argument about food is settled at the level "
  "of who God is before it is settled at the level of what may be eaten."),
],
"1corinthians11": [
 ("extend", "Head Coverings", "(vv.1-16)",
  "The chapter opens with the sentence that closes the previous argument and governs "
  "this one, be ye followers of me, even as I also am of Christ. What follows about "
  "covering is offered as imitation rather than regulation."),
],
"1john2": [
 ("insert", "The Command to Love", "Little Children, Fathers, Young Men (vv.12-14)",
  "Three groups addressed twice over, and each address gives a reason rather than a "
  "command. The little children because their sins are forgiven and because they know "
  "the Father, the fathers because they have known him that is from the beginning, the "
  "young men because they are strong and have overcome the wicked one. Nothing is asked "
  "in these verses. John is telling his readers what is already true of them before he "
  "tells them what to avoid."),
],
"1kings15": [
 ("extend", "Baasha's Reign", "(vv.32-34)",
  "The notice that there was war between Asa and Baasha all their days is repeated here "
  "from verse 16, which is the writer's way of framing Baasha's reign by the conflict "
  "that defined it."),
],
"1kings18": [
 ("extend", "The Challenge on Carmel", "(vv.17-24)",
  "The meeting comes first, and the opening line is Ahab's: Art thou he that troubleth "
  "Israel? Elijah returns the charge without softening it, I have not troubled Israel, "
  "but thou, and thy father's house, in that ye have forsaken the commandments of the "
  "LORD. The drought is placed at the king's door before the contest is proposed."),
],
"1samuel2": [
 ("extend", "The Sins of Eli's Sons", "(vv.11-17)",
  "The section opens with the parting: Elkanah goes home to Ramah and the child is left "
  "ministering unto the LORD before Eli. That one verse sets the contrast the rest of "
  "the chapter runs on, a borrowed child serving faithfully in the same house as two "
  "sons of the priest who do not."),
],
"1timothy6": [
 ("insert", "Instructions for the Rich", "The Final Charge and Benediction (vv.20-21)",
  "O Timothy, keep that which is committed to thy trust. The letter ends on the word "
  "guard rather than on an instruction to do anything new, and what is to be avoided is "
  "named as vain babblings and oppositions of science falsely so called. Some have erred "
  "concerning the faith by professing it. Then four words to close, grace be with thee."),
],
"2corinthians3": [
 ("extend", "Old Covenant vs. New Covenant", "(vv.4-11)",
  "Before the comparison begins, Paul locates his confidence outside himself. Such trust "
  "have we through Christ to God-ward, not that we are sufficient of ourselves to think "
  "any thing, but our sufficiency is of God. The ministry he is about to call glorious is "
  "one he has just said he is not competent to hold."),
],
"2kings3": [
 ("extend", "Elisha's Prophecy", "(vv.10-19)",
  "The section opens with the king of Israel's verdict on the situation, that the LORD "
  "has called three kings together to deliver them into the hand of Moab. He reads the "
  "waterless march as divine hostility, and it is that despair the prophet is then sent "
  "into."),
],
"2samuel18": [
 ("extend", "Absalom's Death", "(vv.9-16)",
  "Joab blows the trumpet at the end of it and the people come back from pursuing "
  "Israel, because Joab held them back. The killing of the king's son and the halting of "
  "the army are the same decision, taken by the same man, in the same hour."),
 ("extend", "The Messengers", "(vv.19-32)",
  "Cushi arrives behind Ahimaaz with the news itself, tidings, my lord the king, for the "
  "LORD hath avenged thee this day of all them that rose up against thee. David asks the "
  "only question he has, Is the young man Absalom safe, and the answer comes as a wish "
  "rather than a fact, that the king's enemies be as that young man is."),
],
"acts3": [
 ("extend", "Peter's Second Sermon", "(vv.12-18)",
  "The crowd runs together in the porch called Solomon's, greatly wondering, and the "
  "sermon is preached into that astonishment. Peter's first move is to refuse the credit, "
  "why look ye so earnestly on us, as though by our own power we had made this man to "
  "walk."),
 ("extend", "The Healing at the Beautiful Gate", "(vv.1-11)",
  "The healed man holds on to Peter and John as the people gather, which is how the "
  "miracle becomes a congregation."),
],
"acts6": [
 ("extend", "The Conflict", "(vv.1-4)",
  "The twelve refuse to leave the word of God to serve tables and hand the selection to "
  "the congregation, look ye out among you seven men of honest report, full of the Holy "
  "Ghost and wisdom."),
 ("insert", "The Seven", "The Word of God Increased (v.7)",
  "And the word of God increased, and the number of the disciples multiplied in Jerusalem "
  "greatly, and a great company of the priests were obedient to the faith. The result of "
  "settling an argument about food distribution is recorded as growth, and the group named "
  "as joining is the one with most to lose by joining."),
],
"acts7": [
 ("extend", "Stephen's Speech", "(vv.1-53)",
  "The speech is an answer to a question, and the question is one line from the high "
  "priest: Are these things so? Everything that follows is the reply to it."),
],
"acts12": [
 ("insert", "Herod's Death", "The Word Grew; Barnabas and Saul Return (vv.24-25)",
  "But the word of God grew and multiplied. The sentence is placed immediately after "
  "Herod's death, and the contrast is the point: the king who accepted the acclaim of a "
  "god is dead, and the word he tried to suppress is spreading. Then Barnabas and Saul "
  "return from Jerusalem having fulfilled their errand, and take with them John whose "
  "surname was Mark."),
],
"deuteronomy6": [
 ("relabel", "The SHEMA", "The Shema (vv.4-5)"),
 ("insert", "The Danger of Prosperity", "Keep the Commandments Diligently (vv.17-19)",
  "Ye shall diligently keep the commandments of the LORD your God, and his testimonies, "
  "and his statutes. Then the standard is put in a form that reaches past the list, and "
  "thou shalt do that which is right and good in the sight of the LORD. The promise "
  "attached is possession of the land and the driving out of enemies, so obedience and "
  "inheritance are tied together rather than traded against each other."),
],
"deuteronomy14": [
 ("insert", "", "Sons of the LORD, a Holy People (vv.1-2)",
  "The food laws are introduced by an identity rather than a rule. Ye are the children of "
  "the LORD your God, and the first application is funeral practice, ye shall not cut "
  "yourselves nor make any baldness between your eyes for the dead. The mourning customs "
  "of the neighbors are excluded because thou art an holy people unto the LORD thy God, "
  "chosen to be a peculiar people unto himself. Everything about clean and unclean that "
  "follows hangs on that sentence."),
],
"genesis10": [
 ("extend", "Japheth's Descendants", "(vv.1-5)",
  "The chapter opens with its own heading, now these are the generations of the sons of "
  "Noah, Shem, Ham, and Japheth, and unto them were sons born after the flood. The order "
  "in the heading is not the order of the table, which takes Japheth first and Shem last, "
  "because the line the book is following is saved for the end."),
],
"genesis14": [
 ("extend", "Melchizedek", "(vv.17-20)",
  "Two kings come out to meet Abram returning from the slaughter, and the chapter puts "
  "them side by side deliberately. The king of Sodom goes out to him at the valley of "
  "Shaveh, and then Melchizedek king of Salem brings bread and wine. One comes to "
  "negotiate and one comes to bless."),
],
"genesis49": [
 ("insert", "", "Gather Around, Sons of Jacob (vv.1-2)",
  "Jacob calls his sons and states what he is about to do, that I may tell you that which "
  "shall befall you in the last days. What follows is therefore not a set of farewells but "
  "a set of futures, and the summons is repeated in verse 2 as poetry, gather yourselves "
  "together, and hear, ye sons of Jacob, and hearken unto Israel your father. Both of his "
  "names are used in the one line."),
 ("extend", "Dan", "(vv.16-18)",
  "Then the poem breaks off mid-sequence for a single line of prayer, I have waited for "
  "thy salvation, O LORD. It sits between Dan and Gad with nothing to introduce it, and "
  "it is the only place in the blessings where Jacob speaks to God rather than about his "
  "sons."),
],
"job2": [
 ("extend", "Job's Wife", "(vv.9-10)",
  "His answer treats her words as a category rather than an insult, thou speakest as one "
  "of the foolish women speaketh. Then the question that holds the book together, shall "
  "we receive good at the hand of God, and shall we not receive evil? The verdict follows "
  "immediately, in all this did not Job sin with his lips."),
],
"job9": [
 ("extend", "God's Overwhelming Power", "(vv.1-13)",
  "Then Job answered. The speech is a reply to Bildad, and it concedes Bildad's premise "
  "in order to destroy his conclusion."),
],
"job23": [
 ("extend", "Job's Confidence", "(vv.10-12)",
  "The confidence is then given its grounds, and they are specific rather than "
  "sentimental. My foot hath held his steps, his way have I kept, and have not declined. "
  "Neither have I gone back from the commandment of his lips, I have esteemed the words of "
  "his mouth more than my necessary food. He is not claiming to be sinless, he is claiming "
  "to have stayed on the road."),
],
"job26": [
 ("extend", "Job's Sarcasm", "(vv.1-4)",
  "But Job answered and said. The reply is aimed at Bildad's short speech in the previous "
  "chapter, and the sarcasm begins in the first breath of it."),
],
"joshua10": [
 ("extend", "The Battle and the Sun Standing Still", "(vv.10-15)",
  "The day ends with the plainest sentence in the chapter, and Joshua returned, and all "
  "Israel with him, unto the camp to Gilgal. After hailstones and a stopped sun, the army "
  "walks back to where it started."),
],
"judges4": [
 ("extend", "Barak's Commission and Condition", "(vv.6-11)",
  "A note is dropped in before the battle that will matter after it: Heber the Kenite had "
  "separated himself from the Kenites and pitched his tent by the plain of Zaanaim, which "
  "is by Kedesh. The tent Sisera runs to has already been placed on the map."),
 ("extend", "Jael Kills Sisera", "(vv.17-24)",
  "The chapter closes on the campaign rather than the tent. So God subdued on that day "
  "Jabin the king of Canaan before the children of Israel, and the hand of the children "
  "of Israel prospered, and prevailed against Jabin, until they had destroyed him. The "
  "single night's work is set inside a war that took longer."),
],
"judges15": [
 ("extend", "God Provides Water", "(vv.18-20)",
  "Then the closing line, and he judged Israel in the days of the Philistines twenty "
  "years. It is the first time the chapter calls him a judge, and it is placed after the "
  "only prayer he has prayed."),
],
"leviticus13": [
 ("insert", "Leprosy on a Bald Head", "The Unclean Person Outside the Camp (vv.45-46)",
  "The examinations stop and the consequence is described. His clothes shall be rent, and "
  "his head bare, and he shall put a covering upon his upper lip, and shall cry, Unclean, "
  "unclean. The signs are those of mourning, worn by a living man about himself. He shall "
  "dwell alone, without the camp shall his habitation be, and the isolation is stated as "
  "lasting all the days wherein the plague shall be in him, which is the one clause that "
  "leaves the door open."),
],
"leviticus14": [
 ("extend", "The Two-Bird Ceremony", "(vv.1-7)",
  "The law is introduced as the law of the leper in the day of his cleansing, and the "
  "first instruction is about where the priest goes: he shall go forth out of the camp. "
  "The examination happens outside, where the unclean man has been living, before anything "
  "is brought in."),
],
"leviticus26": [
 ("insert", "", "No Idols, Keep My Sabbaths (vv.1-2)",
  "The chapter opens with two commands standing in for the whole covenant, and they are "
  "the first and fourth words of the Decalogue. Ye shall make you no idols nor graven "
  "image, neither rear you up a standing image. Ye shall keep my sabbaths, and reverence "
  "my sanctuary. Worship of the right God and observance of his time, and everything that "
  "follows about blessing and discipline is measured against these two."),
 ("relabel", "CYCLE 1", "First Cycle of Discipline (vv.14-17)"),
 ("relabel", "CYCLE 2", "Second Cycle of Discipline (vv.18-20)"),
 ("relabel", "CYCLE 3", "Third Cycle of Discipline (vv.21-22)"),
 ("relabel", "CYCLE 4", "Fourth Cycle of Discipline (vv.23-26)"),
 ("relabel", "CYCLE 5", "Fifth Cycle of Discipline (vv.27-39)"),
 ("merge", "The Five Cycles of Discipline", "Blessings for Obedience"),
],
"numbers18": [
 ("extend", "Priestly Provisions", "(vv.8-20)",
  "The provisions end with the reason for them, given to Aaron directly. Thou shalt have "
  "no inheritance in their land, neither shalt thou have any part among them, I am thy "
  "part and thine inheritance among the children of Israel. The priesthood is paid from "
  "the offerings because it is deliberately left out of the land settlement."),
],
"numbers21": [
 ("extend", "Victory over Sihon", "(vv.21-32)",
  "Moses sends to spy out Jaazer at the end of it, and they take its villages and "
  "dispossess the Amorites that were there. The victory over Sihon is followed "
  "immediately by occupation rather than by celebration."),
],
"philippians4": [
 ("insert", "The Secret of Contentment", "Final Greetings and Grace (vv.21-23)",
  "Salute every saint in Christ Jesus. The brethren which are with me greet you. Then the "
  "detail that is easy to read past, chiefly they that are of Caesar's household, sent "
  "from a man writing under Roman guard. The letter that has argued for joy in any "
  "circumstance ends by naming converts inside the establishment that is holding him, and "
  "closes with grace be with you all."),
],
"ruth2": [
 ("merge", "The Blessing of Wings", "Boaz's Character Revealed"),
 ("insert", "Boaz's Character Revealed", "Ruth Beats Out an Ephah (vv.17-18)",
  "She gleaned until evening and beat out what she had gathered, and it was about an ephah "
  "of barley. The figure is the point of the verse: something near thirty pounds of grain, "
  "far beyond what a day's gleaning normally yielded, which is the measure of what Boaz "
  "had quietly arranged. She carries it into the city, and brings out what she had kept "
  "back from her own meal and gives it to Naomi."),
],
"ruth3": [
 ("insert", "Boaz's Honorable Response", "Ruth Returns with Six Measures (vv.16-17)",
  "Naomi's question is two words in the Hebrew and it is the right question, Who art "
  "thou, my daughter? She is asking what Ruth's standing is now, not who she is. Ruth "
  "tells her all that the man had done, and produces the six measures of barley with the "
  "message that came with them, Go not empty unto thy mother-in-law. The grain is sent to "
  "Naomi specifically, which is Boaz answering the older woman's emptiness of chapter 1."),
],
"titus2": [
 ("extend", "The Grace of God", "(vv.11-15)",
  "The chapter ends by handing the whole of it to Titus as a task. These things speak, and "
  "exhort, and rebuke with all authority, let no man despise thee. The doctrine is not "
  "left as description, it is given to a man to say out loud in a place where he is likely "
  "to be dismissed."),
],
# defect-only pages
"deuteronomy15": [
 ("merge", "The Willing Bond-Servant", "Release of Hebrew Servants"),
],
"deuteronomy18": [
 ("relabel", "The PROPHET like MOSES", "A Prophet Like Moses (vv.15-19)"),
],
"deuteronomy33": [
 ("relabel", "REUBEN", "Reuben (v.6)"),
 ("relabel", "JUDAH", "Judah (v.7)"),
 ("relabel", "LEVI", "Levi (vv.8-11)"),
 ("relabel", "BENJAMIN", "Benjamin (v.12)"),
 ("relabel", "JOSEPH", "Joseph (vv.13-17)"),
 ("relabel", "ZEBULUN", "Zebulun and Issachar (vv.18-19)"),
 ("relabel", "GAD", "Gad (vv.20-21)"),
 ("relabel", "DAN", "Dan (v.22)"),
 ("relabel", "NAPHTALI", "Naphtali (v.23)"),
 ("relabel", "ASHER", "Asher (vv.24-25)"),
],
"ephesians3": [
 ("extend", "Paul's Digression", "(v.1)",
  "The sentence is broken off before it is finished. For this cause I, Paul, the prisoner "
  "of Jesus Christ for you Gentiles, and then the thought is abandoned and not picked up "
  "again until verse 14."),
],
"genesis5": [
 ("extend", "The Refrain of Death", "(vv.1-27)",
  "Eight generations, and the same closing clause on each one."),
],
"job7": [
 ("extend", "Job's Direct Address to God", "(vv.7-16)",
  "The address begins by asking God to remember, and it is addressed upward rather than at "
  "the friends for the first time in the book."),
],
"joshua8": [
 ("extend", "God's Encouragement and Strategy", "(vv.1-2)",
  "Fear not, neither be thou dismayed. The instruction that follows differs from Jericho in "
  "one respect the men would have noticed at once: the spoil and the cattle of Ai ye shall "
  "take for a prey unto yourselves. What was devoted at Jericho is released here."),
],
"judges21": [
 ("extend", "The Book's Conclusion", "(vv.24-25)",
  "The people disperse to their inheritances, and then the line the book has been building "
  "toward: in those days there was no king in Israel, every man did that which was right in "
  "his own eyes."),
],
"numbers26": [
 ("extend", "The Tribes Numbered", "(vv.5-7,12-32,34-51)",
  "The tribal totals run in order, each with its clans named."),
],
"revelation9": [
 ("extend", "Sixth Trumpet / Second Woe", "(vv.13-19)",
  "The four angels bound at the Euphrates are loosed, and the army numbered at two hundred "
  "thousand thousand is described by its horses rather than its riders."),
],
}


def find(items, prefix):
    for i, (label, _) in enumerate(items):
        if H.unescape(label).strip().startswith(prefix):
            return i
    return -1


def first_section(items):
    for i, (label, _) in enumerate(items):
        if re.search(r"\(vv?\.[^)]*\)\s*:?\s*$", H.unescape(label).strip()):
            return i
    return len(items)


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, ops in OPS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        if not items:
            problems.append(f"{page}: no fields parsed")
            continue
        for op in ops:
            kind = op[0]
            if kind == "extend":
                _, prefix, rng, prose = op
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: extend target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                items[i][1] = items[i][1] + " " + prose
                notes.append(f"{page}: extended {prefix!r} to {rng}")
            elif kind == "insert":
                _, after, label, prose = op
                at = first_section(items) if after == "" else find(items, after) + 1
                if after and at == 0:
                    problems.append(f"{page}: insert anchor {after!r} not found")
                    continue
                items.insert(at, [label + ":", prose])
                notes.append(f"{page}: inserted {label!r}")
            elif kind == "merge":
                _, nested, parent = op
                i, j = find(items, nested), find(items, parent)
                if i < 0 or j < 0:
                    problems.append(f"{page}: merge {nested!r} into {parent!r} not found")
                    continue
                items[j][1] = items[j][1] + " " + items[i][1]
                del items[i]
                notes.append(f"{page}: merged {nested!r} into {parent!r}")
            elif kind == "relabel":
                _, prefix, label = op
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: relabel target {prefix!r} not found")
                    continue
                items[i][0] = label + ":"
                notes.append(f"{page}: relabelled {prefix!r} to {label!r}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
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
    for n in notes:
        print(f"    {n}")
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would touch' if check else 'touched'} {len(planned)} pages, "
          f"{len(notes)} repair(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
