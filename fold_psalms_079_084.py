#!/usr/bin/env python3
"""
Psalms 79 to 84. Six pages, 88 verses. All six outlines are gapless and are folded.

psalms80 carries a refrain at verses 3, 7 and 19, each time with the divine title expanded,
and the sections keep the three labels distinct while naming what they are, since two
identical labels on one page read as a defect even when the psalm intends the repetition.

psalms81's outline divides at a half verse, 1-5a and 5b-7, because the voice changes there
from the congregation's to God's in the middle of the line. The split is kept.

psalms82 is the passage Jesus quotes in John 10:34, ye are gods, and the section says what
the verse is doing in its own psalm before noting the use he makes of it.

Usage:
    python3 fold_psalms_079_084.py [--check]
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
KEEP = ("Author:", "Date:", "Attributed Author:", "Classification:", "Key Themes:",
        "Historical Context:")
REPAIRS = {}

SECTIONS = {
"psalms79": [
 ("The Heathen Are Come into Thine Inheritance (vv.1-4)",
  "O God, the heathen are come into thine inheritance, thy holy temple have they defiled, they have laid "
  "Jerusalem on heaps. The psalm stands where psalms74 stands, in a destroyed sanctuary, and what it "
  "reports first is a failure of burial, the dead bodies of thy servants have they given to be meat unto "
  "the fowls of the heaven, their blood have they shed like water, and there was none to bury them. Then "
  "the reputational damage, we are become a reproach to our neighbours, a scorn and derision to them that "
  "are round about us."),
 ("How Long, LORD (v.5)",
  "How long, LORD, wilt thou be angry for ever, shall thy jealousy burn like fire. One verse, and the two "
  "halves of it do not quite agree: how long assumes an end and for ever denies one. The psalter lets the "
  "contradiction stand, which is what a question asked under pressure looks like."),
 ("Pour Out Thy Wrath upon the Heathen (vv.6-7)",
  "Pour out thy wrath upon the heathen that have not known thee, and upon the kingdoms that have not called "
  "upon thy name. Two verses of imprecation, and the charge is not the destruction itself but ignorance of "
  "God, which the next clause identifies as the licence for it, for they have devoured Jacob, and laid "
  "waste his dwelling place. Jeremiah 10:25 has almost the same sentence."),
 ("Remember Not Against Us Former Iniquities (vv.8-9)",
  "O remember not against us former iniquities, let thy tender mercies speedily prevent us, for we are "
  "brought very low. The psalm concedes the guilt, which psalms44 refused to do, and asks for the account "
  "to be closed rather than disputed. And the ground offered is God's reputation rather than Israel's case, "
  "help us, O God of our salvation, for the glory of thy name, and deliver us, and purge away our sins, for "
  "thy name's sake."),
 ("Wherefore Should the Heathen Say (vv.10-12)",
  "Wherefore should the heathen say, Where is their God. The taunt of Psalm 42:3 quoted at national scale, "
  "and it is the argument the psalm rests on: the reputation at stake is not Israel's. Then a petition "
  "about the imprisoned, let the sighing of the prisoner come before thee, according to the greatness of "
  "thy power preserve thou those that are appointed to die."),
 ("We Thy People Will Praise Thee For Ever (v.13)",
  "So we thy people and sheep of thy pasture will give thee thanks for ever, we will shew forth thy praise "
  "to all generations. The psalm ends on the same shepherd image psalms74 opened with, and on a promise "
  "made from inside the ruins with nothing having changed."),
],
"psalms80": [
 ("Give Ear, O Shepherd of Israel (vv.1-2)",
  "Give ear, O Shepherd of Israel, thou that leadest Joseph like a flock. The tribes named through this "
  "psalm are northern, Joseph, Ephraim, Benjamin, Manasseh, which is why it is usually read as a lament "
  "over the fall of Samaria. And the address invokes the ark, thou that dwellest between the cherubims, "
  "shine forth."),
 ("Turn Us Again, O God (v.3)",
  "Turn us again, O God, and cause thy face to shine, and we shall be saved. The refrain appears three "
  "times in this psalm, here and at verses 7 and 19, and each time the divine title is longer than the "
  "last. What is asked for is not rescue but reversal of a condition, and the verb is causative: they ask "
  "to be turned rather than promising to turn."),
 ("Thou Feedest Them with the Bread of Tears (vv.4-6)",
  "O LORD God of hosts, how long wilt thou be angry against the prayer of thy people. The complaint is "
  "sharper than most in the psalter because the object of the anger is the praying itself. Then the diet, "
  "thou feedest them with the bread of tears, and givest them tears to drink in great measure, so grief is "
  "described as the ration."),
 ("Turn Us Again, O God of Hosts (v.7)",
  "Turn us again, O God of hosts, and cause thy face to shine, and we shall be saved. The refrain a second "
  "time, with of hosts added to the title. Nothing else changes, and the repetition is the psalm's "
  "structure rather than an oversight."),
 ("Thou Hast Brought a Vine out of Egypt (vv.8-16)",
  "Thou hast brought a vine out of Egypt, thou hast cast out the heathen, and planted it. The allegory runs "
  "for nine verses and its first half is expansion, she sent out her boughs unto the sea, and her branches "
  "unto the river. Then the question that turns it, why hast thou then broken down her hedges, so that all "
  "they which pass by the way do pluck her. Isaiah 5 and Jeremiah 2:21 use the same vine, and Jesus takes "
  "it up in John 15. And the damage is described in two agents, the boar out of the wood doth waste it, and "
  "the wild beast of the field doth devour it."),
 ("The Man of Thy Right Hand (vv.17-18)",
  "Let thy hand be upon the man of thy right hand, upon the son of man whom thou madest strong for "
  "thyself. The figure is not identified and the psalm does not explain him, which is why the verse has "
  "been read both of the king and messianically. What is promised in return is stated modestly, so will not "
  "we go back from thee, quicken us, and we will call upon thy name."),
 ("Turn Us Again, O LORD God of Hosts (v.19)",
  "Turn us again, O LORD God of hosts, cause thy face to shine, and we shall be saved. The refrain for the "
  "third and last time, with the title at its fullest. The psalm has not reported an answer anywhere in "
  "nineteen verses; what it has done is ask the same thing three times with the name of the one being "
  "asked getting longer."),
],
"psalms81": [
 ("Sing Aloud unto God Our Strength (vv.1-5a)",
  "Sing aloud unto God our strength, make a joyful noise unto the God of Jacob. The instruction is "
  "festival music, take a psalm, and bring hither the timbrel, the pleasant harp with the psaltery. Then "
  "the occasion is dated to the calendar, blow up the trumpet in the new moon, in the time appointed, on "
  "our solemn feast day, which points to the seventh-month festivals. And the last clause names it as a "
  "statute rather than a custom. The section stops in the middle of verse 5 because the voice changes "
  "there."),
 ("I Removed His Shoulder from the Burden (vv.5b-7)",
  "God begins to speak inside verse 5 and continues to the end of the psalm, which is what makes this poem "
  "unusual: a call to worship that turns into a complaint from the one being worshipped. I removed his "
  "shoulder from the burden, his hands were delivered from the pots, which is the brickmaking of Exodus 1. "
  "Then the testing is named as well as the rescue, I proved thee at the waters of Meribah, so the same "
  "history contains both."),
 ("Open Thy Mouth Wide (vv.8-10)",
  "Hear, O my people, and I will testify unto thee. The first commandment is quoted almost verbatim, there "
  "shall no strange god be in thee, neither shalt thou worship any strange god, I am the LORD thy God, "
  "which brought thee out of the land of Egypt. Then an invitation that has no parallel in the psalter for "
  "sheer openness, open thy mouth wide, and I will fill it."),
 ("My People Would Not Hearken (vv.11-12)",
  "But my people would not hearken to my voice, and Israel would none of me. Two verses, and the judgment "
  "in them is the one Romans 1 restates: they are given what they chose, so I gave them up unto their own "
  "hearts' lust, and they walked in their own counsels. Nothing is imposed."),
 ("Oh That My People Had Hearkened (vv.13-16)",
  "Oh that my people had hearkened unto me, and Israel had walked in my ways. The grammar is a wish about a "
  "past that did not happen, which is what Isaiah 48:18 does in the same words. What was forfeited is then "
  "listed, and it is military and agricultural, I should soon have subdued their enemies, and he should "
  "have fed them also with the finest of the wheat. And the psalm ends on an image of extravagant supply "
  "left undelivered, and with honey out of the rock should I have satisfied thee."),
],
"psalms82": [
 ("God Standeth in the Congregation of the Mighty (v.1)",
  "God standeth in the congregation of the mighty, he judgeth among the gods. One verse, and it is the "
  "difficulty the whole psalm turns on: a divine council is described and God is judging the members of it. "
  "The Hebrew word elohim is used both of God and of the ones being judged, and readers have taken those "
  "to be heavenly beings, or Israel's judges addressed with deliberate irony, or both. The psalm does not "
  "settle it, and what follows suggests human officials since the charge is judicial."),
 ("How Long Will Ye Judge Unjustly (v.2)",
  "How long will ye judge unjustly, and accept the persons of the wicked. One verse of charge, and the "
  "phrase accept the persons is the Hebrew idiom for showing partiality, lifting somebody's face. The "
  "offence is favouritism on the bench, which is the specific corruption the prophets return to most "
  "often."),
 ("Defend the Poor and Fatherless (vv.3-4)",
  "Defend the poor and fatherless, do justice to the afflicted and needy, deliver the poor and needy, rid "
  "them out of the hand of the wicked. Two verses and five imperatives, and every one of them names a "
  "beneficiary rather than a principle. This is the clearest statement in the psalter of what a court is "
  "for."),
 ("They Know Not, Neither Will They Understand (v.5)",
  "They know not, neither will they understand, they walk on in darkness, all the foundations of the earth "
  "are out of course. One verse, and the last clause is the psalm's largest claim: corrupt courts are "
  "described as a structural problem in creation rather than a local scandal. Isaiah 24:5 uses the same "
  "reasoning about a broken covenant."),
 ("Ye Shall Die Like Men (vv.6-7)",
  "I have said, Ye are gods, and all of you are children of the most High. But ye shall die like men, and "
  "fall like one of the princes. The two verses have to be read together, since the title is granted in "
  "the first and cancelled in the second. Jesus quotes verse 6 in John 10:34 when he is accused of "
  "blasphemy, and his argument is from the lesser to the greater: if scripture can call those men gods, "
  "the charge against him does not follow automatically."),
 ("Arise, O God, Judge the Earth (v.8)",
  "Arise, O God, judge the earth, for thou shalt inherit all nations. The psalm ends by asking God to do "
  "the job himself, which is the conclusion the previous seven verses have been forcing. The council has "
  "been found unfit and the case is referred upward."),
],
"psalms83": [
 ("Keep Not Thou Silence, O God (vv.1-4)",
  "Keep not thou silence, O God, hold not thy peace, and be not still, O God. Three requests for the same "
  "thing in one verse, which is the psalm's measure of how long the silence has lasted. Then the enemy's "
  "intention is quoted and it is total, they have said, Come, and let us cut them off from being a nation, "
  "that the name of Israel may be no more in remembrance."),
 ("They Have Taken Crafty Counsel (vv.5-8)",
  "For they have consulted together with one consent, they are confederate against thee. Ten peoples are "
  "then named, Edom, the Ishmaelites, Moab, the Hagarenes, Gebal, Ammon, Amalek, the Philistines, Tyre and "
  "Assyria, which is a coalition no historical record attests and which reads as every neighbour at once. "
  "And the last clause names who benefits, they have holpen the children of Lot."),
 ("Do unto Them as unto the Midianites (vv.9-12)",
  "Do unto them as unto the Midianites, as to Sisera, as to Jabin, at the brook of Kison. The precedents "
  "are all from Judges, Gideon's victory and Deborah's, and the psalm asks for a repeat rather than "
  "something new. Then the enemy leaders are quoted stating their aim, who said, Let us take to ourselves "
  "the houses of God in possession."),
 ("Make Them Like a Wheel (vv.13-17)",
  "O my God, make them like a wheel, as the stubble before the wind. The images are all of things blown "
  "about or burned, chaff, a forest fire, a flame that setteth the mountains on fire. And the purpose asked "
  "for is shame rather than annihilation, fill their faces with shame, that they may seek thy name, O LORD, "
  "which is a request that the defeat should teach them something."),
 ("That Men May Know That Thou Art the Most High (v.18)",
  "That men may know that thou, whose name alone is JEHOVAH, art the most high over all the earth. The "
  "psalm's last verse states the object of the whole imprecation, and it is not Israel's safety but "
  "recognition. This is one of only four places in the King James Bible where the divine name is rendered "
  "JEHOVAH rather than the LORD."),
],
"psalms84": [
 ("How Amiable Are Thy Tabernacles (vv.1-4)",
  "How amiable are thy tabernacles, O LORD of hosts, my soul longeth, yea, even fainteth for the courts of "
  "the LORD. The psalm is a pilgrim's song and what it wants is a building. Then the image the psalm is "
  "loved for, and it is a piece of observation from inside the courts, yea, the sparrow hath found an "
  "house, and the swallow a nest for herself, where she may lay her young, even thine altars. Birds nest in "
  "the temple and he cannot get there, which is the whole complaint in one picture."),
 ("The Valley of Baca (vv.5-7)",
  "Blessed is the man whose strength is in thee, in whose heart are the ways of them. The Hebrew of that "
  "last phrase means something like the highways are in their hearts: they are already on the road in their "
  "minds. Then the valley, who passing through the valley of Baca make it a well, where Baca means weeping "
  "or possibly balsam trees, so a dry place is turned into water by the people walking through it. And the "
  "closing line reverses the usual arithmetic of a journey, they go from strength to strength."),
 ("Behold, O God Our Shield (vv.8-9)",
  "O LORD God of hosts, hear my prayer, give ear, O God of Jacob. Two verses, and the petition is for "
  "somebody else, behold, O God our shield, and look upon the face of thine anointed. A pilgrim's psalm "
  "stopping to pray for the king is one of the reasons this poem is thought to belong to a festival "
  "liturgy."),
 ("A Doorkeeper in the House of My God (vv.10-12)",
  "For a day in thy courts is better than a thousand. Then the comparison the psalm is best known for, and "
  "it is deliberately menial, I had rather be a doorkeeper in the house of my God, than to dwell in the "
  "tents of wickedness. The lowest post inside is preferred to residence outside. And the closing promise "
  "pairs two things the psalter usually keeps apart, for the LORD God is a sun and shield, the LORD will "
  "give grace and glory, no good thing will he withhold from them that walk uprightly."),
],
}


def verify(planned):
    """Run the audit's own checks against the planned HTML, without writing it."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import audit_authorship as A
    found = []
    for path, html in planned.items():
        page = os.path.basename(path)[:-5]
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', html)}
        total = max(nums) if nums else 0
        pane = A.PANE.search(html).group(2)
        labels = [H.unescape(x).strip() for x in A.LABEL.findall(pane)]
        secs = [(l, A.TAIL.search(l)) for l in labels]
        secs = [(l, m.group(1)) for l, m in secs if m]
        covered, repeated, starts = set(), set(), []
        for label, spec in secs:
            got = A.halves(spec)
            repeated |= got & covered
            covered |= got
            starts.append(min(v for v, _ in got) if got else 0)
            if total and max(v for v, _ in got) > total:
                found.append(f"{page}: {label!r} runs past verse {total}")
        want = {(v, h) for v in range(1, total + 1) for h in ("a", "b")}
        missing = sorted({v for v, _ in (want - covered)})
        if missing:
            found.append(f"{page}: verses uncovered {missing}")
        if repeated:
            found.append(f"{page}: verses described twice "
                         f"{sorted({v for v, _ in repeated})}")
        if starts != sorted(starts):
            found.append(f"{page}: sections out of verse order")
        if "<li>" in pane or "auth-sublist" in pane:
            found.append(f"{page}: sublist survived the fold")
        if len(set(labels)) != len(labels):
            dup = sorted({l for l in labels if labels.count(l) > 1})
            found.append(f"{page}: duplicate label(s) {dup}")
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label)
                            if w not in A.CAPS_OK})
            if stray and A.TAIL.search(label):
                found.append(f"{page}: capitals {stray} in {label!r}")
    return found


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, sections in SECTIONS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body_html = pane.group(2)
        found = [H.unescape(l).strip() for l, _ in ITEM_RE.findall(body_html)]
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if not keep:
            problems.append(f"{page}: no book fields found to preserve")
            continue
        for label in found:
            if label not in KEEP:
                notes.append(f"{page}: dropped inherited item {label!r}")
        for i, (label, body) in enumerate(keep):
            for old, new in REPAIRS.get(page, []):
                if old in body:
                    keep[i][1] = body = body.replace(old, new)
                    notes.append(f"{page}: repaired {old!r} in {label}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        notes.append(f"{page}: kept {len(keep)} book field(s)")
        for label, prose in sections:
            parts.append(ITEM.format(label=label + ":", body=prose) + "\n")
            notes.append(f"{page}: {label}")
        new_body = "".join(parts) + "            </div>\n\n            "
        planned[path] = html[:pane.start(2)] + new_body + html[pane.end(2):]
    problems += verify(planned)
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
    print(f"{'would fold' if check else 'folded'} {len(planned)} pages, "
          f"{sum(len(v) for v in SECTIONS.values())} section(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
