#!/usr/bin/env python3
"""
Psalms 73 to 78. Six pages, 165 verses. All six outlines are gapless and are folded.

This block opens Book III of the psalter, and the change of tone is immediate. Book III is
the darkest of the five: psalms74 and 79 describe the temple in ruins, psalms77 asks whether
God's mercy is clean gone for ever, and the book will end at 89 with the covenant with
David apparently cancelled. The sections say where a psalm is answering that question and
where it declines to.

psalms73 and psalms78 are the two long ones here and they work in opposite directions.
73 argues from one man's near-collapse to a conclusion, and its turn is located precisely,
at the sanctuary in verse 17. 78 recites the national history at length in order to explain
why it must be taught to children, which the psalm states as its purpose before it begins.

Usage:
    python3 fold_psalms_073_078.py [--check]
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
"psalms73": [
 ("Truly God Is Good to Israel (v.1)",
  "Truly God is good to Israel, even to such as are of a clean heart. One verse, and it is the conclusion "
  "of the psalm placed at the front. Everything that follows is the account of how nearly it was lost, so "
  "the opening line is not a premise the poem argues from but the thing it comes back to."),
 ("My Feet Were Almost Gone (vv.2-14)",
  "But as for me, my feet were almost gone, my steps had well nigh slipped. The admission is stated before "
  "the reason, and the reason is envy, for I was envious at the foolish, when I saw the prosperity of the "
  "wicked. What follows is thirteen verses of accurate observation, which is what makes the psalm honest: "
  "there are no bands in their death, their strength is firm, they are not in trouble as other men. And "
  "their reasoning is quoted, how doth God know, and is there knowledge in the most High. Then the "
  "conclusion he had reached, verily I have cleansed my heart in vain, and washed my hands in innocency, "
  "which is the position the whole psalm exists to answer."),
 ("If I Should Speak Thus (vv.15-16)",
  "If I say, I will speak thus, behold, I should offend against the generation of thy children. Two "
  "verses, and the restraint in them is pastoral rather than pious: he does not say it out loud because of "
  "what it would do to other people. Then the effort of thinking it through is described as work, when I "
  "thought to know this, it was too painful for me."),
 ("Until I Went into the Sanctuary (vv.17-20)",
  "Until I went into the sanctuary of God, then understood I their end. The turn is located in a place "
  "rather than in an argument, and nothing in the psalm says what happened there. What changed was the "
  "time horizon: the previous section looked at the prosperous now, and this one looks at the end. Then "
  "the images of collapse, thou castest them down into destruction, how are they brought into desolation, "
  "as a dream when one awaketh."),
 ("So Foolish Was I (vv.21-22)",
  "Thus my heart was grieved, and I was pricked in my reins. So foolish was I, and ignorant, I was as a "
  "beast before thee. Two verses of self-assessment, and the comparison with an animal is the same one "
  "Psalm 49:20 makes of the rich man who does not understand. The psalm applies it to itself."),
 ("Whom Have I in Heaven but Thee (vv.23-28)",
  "Nevertheless I am continually with thee, thou hast holden me by my right hand. The word nevertheless "
  "carries the whole psalm. Then the sentence it is remembered for, whom have I in heaven but thee, and "
  "there is none upon earth that I desire beside thee. And the concession that makes it costly, my flesh "
  "and my heart faileth, so the claim is not that the trouble has lifted. God is described as the portion "
  "of Psalm 16:5 rather than as a solution, but God is the strength of my heart, and my portion for ever."),
],
"psalms74": [
 ("Why Hast Thou Cast Us Off For Ever (vv.1-3)",
  "O God, why hast thou cast us off for ever, why doth thine anger smoke against the sheep of thy pasture. "
  "The complaint is national and the imagery is the shepherd's, which makes the abandonment a professional "
  "failure rather than a change of mood. Then the request, lift up thy feet unto the perpetual desolations, "
  "even all that the enemy hath done wickedly in the sanctuary. The psalm is standing in a wrecked "
  "building."),
 ("They Have Set Up Their Ensigns (vv.4-8)",
  "Thine enemies roar in the midst of thy congregations, they set up their ensigns for signs. Five verses "
  "of eyewitness description, and the detail is carpentry and arson: a man was famous according as he had "
  "lifted up axes upon the thick trees, they break down the carved work thereof with axes and hammers, "
  "they have cast fire into thy sanctuary. And their stated intention is total, they said in their hearts, "
  "Let us destroy them together, they have burned up all the synagogues of God in the land."),
 ("There Is No More Any Prophet (vv.9-11)",
  "We see not our signs, there is no more any prophet, neither is there among us any that knoweth how "
  "long. The absence described is not of help but of information: nobody can say what the timetable is. "
  "Then the question that follows from it, O God, how long shall the adversary reproach. And the boldest "
  "line in the psalm, why withdrawest thou thy hand, even thy right hand, pluck it out of thy bosom."),
 ("Thou Didst Divide the Sea (vv.12-17)",
  "For God is my King of old, working salvation in the midst of the earth. The argument turns to what has "
  "been done before, and it reaches past the exodus into creation myth, thou brakest the heads of the "
  "dragons in the waters, thou brakest the heads of leviathan in pieces. Then the ordinary order of "
  "things is credited to the same hand, thou hast prepared the light, thou hast set all the borders of the "
  "earth, thou hast made summer and winter. The psalm's case is that whoever arranged the seasons can "
  "manage the present."),
 ("Remember Thy Congregation (vv.18-23)",
  "Remember this, that the enemy hath reproached, O LORD, and that the foolish people have blasphemed thy "
  "name. The petitions are all about memory and they are stated four times, remember, forget not. And the "
  "argument offered is God's own reputation rather than Israel's deserving, arise, O God, plead thine own "
  "cause. The psalm ends with no answer given, forget not the voice of thine enemies, which is where "
  "several of the Book III laments stop."),
],
"psalms75": [
 ("Unto Thee, O God, Do We Give Thanks (v.1)",
  "Unto thee, O God, do we give thanks, unto thee do we give thanks, for that thy name is near. One verse, "
  "and the thanksgiving is doubled for emphasis. What is thanked for is proximity rather than an act, thy "
  "name is near, thy wondrous works declare, which sets this psalm directly against the absence complained "
  "of in the two on either side of it."),
 ("I Will Judge Uprightly (vv.2-5)",
  "God speaks for four verses in the first person, which is unusual in the psalter, and the first thing he "
  "says is about timing, when I shall receive the congregation I will judge uprightly. The delay is "
  "presented as a schedule rather than an absence. Then a claim about maintenance, the earth and all the "
  "inhabitants thereof are dissolved, I bear up the pillars of it. And the instruction to the confident, "
  "lift not up the horn, speak not with a stiff neck."),
 ("Promotion Cometh Neither from the East nor from the West (vv.6-8)",
  "For promotion cometh neither from the east, nor from the west, nor from the south. Three directions are "
  "ruled out and the fourth is left unspoken, which is the sentence's device: north is where the throne "
  "sits in Psalm 48:2. Then the answer, but God is the judge, he putteth down one, and setteth up another. "
  "And the cup image returns, in the hand of the LORD there is a cup, and the wine is red, it is full of "
  "mixture, which runs from here through Jeremiah 25 to Gethsemane."),
 ("All the Horns of the Wicked Will I Cut Off (vv.9-10)",
  "But I will declare for ever, I will sing praises to the God of Jacob. The singer answers God's four "
  "verses with two of his own. And the closing line picks up the horn imagery of verse 4 and finishes it, "
  "all the horns of the wicked also will I cut off, but the horns of the righteous shall be exalted, so "
  "the same word is used of what is lowered and what is raised."),
],
"psalms76": [
 ("In Judah Is God Known (vv.1-3)",
  "In Judah is God known, his name is great in Israel. In Salem also is his tabernacle, and his dwelling "
  "place in Zion. Salem is the older name of Jerusalem, used in Genesis 14, so the psalm reaches back "
  "behind the monarchy. And what is broken in the last verse is equipment rather than armies, there brake "
  "he the arrows of the bow, the shield, and the sword, and the battle."),
 ("Thou Art More Glorious Than the Mountains of Prey (vv.4-6)",
  "Thou art more glorious and excellent than the mountains of prey. Then a picture of a defeated army "
  "described entirely by what it is no longer doing, the stouthearted are spoiled, they have slept their "
  "sleep, and none of the men of might have found their hands. And the last verse names how it happened, "
  "at thy rebuke, O God of Jacob, both the chariot and horse are cast into a dead sleep. No battle is "
  "described."),
 ("Who May Stand in Thy Sight (vv.7-9)",
  "Thou, even thou, art to be feared, and who may stand in thy sight when once thou art angry. Then the "
  "purpose of the judgment is stated and it is not punishment, when God arose to judgment, to save all the "
  "meek of the earth. The verdict from heaven is described as a rescue at ground level."),
 ("The Wrath of Man Shall Praise Thee (v.10)",
  "Surely the wrath of man shall praise thee, the remainder of wrath shalt thou restrain. One verse, and "
  "it is the psalm's hardest thought: human anger is described as ending up serving a purpose it did not "
  "intend, and the surplus is simply held back. It is the same knot Isaiah 10:5-7 ties about Assyria."),
 ("Vow, and Pay unto the LORD (vv.11-12)",
  "Vow, and pay unto the LORD your God, let all that be round about him bring presents unto him that ought "
  "to be feared. The instruction is addressed outward to the surrounding nations rather than to Israel. "
  "And the last verse gives the reason in political terms, he cutteth off the spirit of princes, he is "
  "terrible to the kings of the earth."),
],
"psalms77": [
 ("I Cried unto God with My Voice (vv.1-3)",
  "I cried unto God with my voice, even unto God with my voice, and he gave ear unto me. The doubling in "
  "the first line is insistence rather than elegance. Then the posture, in the day of my trouble I sought "
  "the Lord, my sore ran in the night, and ceased not. And a clause that reverses what most psalms claim, "
  "I remembered God, and was troubled, so remembering is here the cause of the distress rather than the "
  "cure for it."),
 ("Thou Holdest Mine Eyes Waking (vv.4-6)",
  "Thou holdest mine eyes waking, I am so troubled that I cannot speak. The insomnia is attributed "
  "directly to God, which is unusually blunt. Then the mind goes backwards, I have considered the days of "
  "old, the years of ancient times, I call to remembrance my song in the night. And the last clause "
  "describes the process without claiming a result, and my spirit made diligent search."),
 ("Will the Lord Cast Off For Ever (vv.7-9)",
  "Six questions in three verses, and they are the bleakest sequence in the psalter. Will the Lord cast off "
  "for ever, and will he be favourable no more. Is his mercy clean gone for ever, doth his promise fail "
  "for evermore. Hath God forgotten to be gracious, hath he in anger shut up his tender mercies. Every one "
  "of them is left unanswered on the page, and the psalm does not retract them; it changes the subject."),
 ("I Will Remember the Years of the Right Hand (vv.10-12)",
  "And I said, This is my infirmity, but I will remember the years of the right hand of the most High. The "
  "turn is a decision rather than a discovery, and the verb is the same one that caused the trouble in "
  "verse 3: he had remembered God and been troubled, and now he chooses to remember the works. I will "
  "remember the works of the LORD, surely I will remember thy wonders of old. Repeated three times in two "
  "verses, which is what a deliberate act looks like."),
 ("Thy Way Is in the Sanctuary (v.13)",
  "Thy way, O God, is in the sanctuary, who is so great a God as our God. One verse, and it locates the "
  "answer where Psalm 73:17 located it, which is worth noticing in a book where the sanctuary is being "
  "described elsewhere as burned. The question at the end is rhetorical and is the hinge into the "
  "recital."),
 ("Thy Way Is in the Sea (vv.14-20)",
  "Thou hast declared thy strength among the people, thou hast with thine arm redeemed thy people. The "
  "psalm answers its six questions by retelling the exodus, and the poetry is at its best here, the waters "
  "saw thee, they were afraid, the depths also were troubled, the clouds poured out water, thine arrows "
  "also went abroad. Then the phrase that sets against verse 13, thy way is in the sea, and thy path in "
  "the great waters, and thy footsteps are not known. And the psalm ends without returning to its "
  "questions, on a single quiet image of management, thou leddest thy people like a flock by the hand of "
  "Moses and Aaron."),
],
"psalms78": [
 ("We Will Not Hide Them from Their Children (vv.1-8)",
  "Give ear, O my people, to my law, I will open my mouth in a parable. Matthew 13:35 quotes that line of "
  "Jesus' teaching in parables. The psalm states its purpose before it begins, and the purpose is "
  "transmission across three generations, we will not hide them from their children, shewing to the "
  "generation to come the praises of the LORD. And the reason is given as a hope about the outcome, that "
  "they might set their hope in God, and not be as their fathers, a stubborn and rebellious generation. "
  "Everything that follows is evidence for that last clause."),
 ("The Children of Ephraim Turned Back (vv.9-11)",
  "The children of Ephraim, being armed, and carrying bows, turned back in the day of battle. Ephraim "
  "stands for the northern kingdom throughout this psalm, and the charge against them is stated as a "
  "failure of memory rather than of courage, they kept not the covenant of God, and forgat his works, and "
  "his wonders that he had shewed them."),
 ("He Divided the Sea (vv.12-16)",
  "Marvellous things did he in the land of Egypt, in the field of Zoan. The recital begins and its selection "
  "is water throughout: he divided the sea, and caused them to pass through, he clave the rocks in the "
  "wilderness, and gave them drink as out of the great depths. And the detail at the end is deliberately "
  "excessive, he brought streams also out of the rock, and caused waters to run down like rivers."),
 ("Can God Furnish a Table in the Wilderness (vv.17-31)",
  "And they sinned yet more against him by provoking the most High in the wilderness. The quoted complaint "
  "is the centre of this section and it is a question, yea, they spake against God, they said, Can God "
  "furnish a table in the wilderness. Then the answer, given in the most generous terms available, he had "
  "commanded the clouds from above, and rained down manna upon them, man did eat angels' food. And then "
  "the sting: the request for meat is granted and the granting is itself the judgment, while their meat "
  "was yet in their mouths, the wrath of God came upon them. The psalm calls the quails an answered prayer "
  "and a disaster in the same breath."),
 ("He, Being Full of Compassion, Forgave (vv.32-39)",
  "For all this they sinned still, and believed not for his wondrous works. Then the pattern is described "
  "as a cycle, when he slew them, then they sought him, and they returned and enquired early after God, "
  "and the psalm's assessment of that repentance is unsparing, nevertheless they did flatter him with "
  "their mouth, and they lied unto him with their tongue. And against that, the verse the section turns "
  "on, but he, being full of compassion, forgave their iniquity, and destroyed them not. The reason given "
  "is physiological rather than moral, for he remembered that they were but flesh, a wind that passeth "
  "away, and cometh not again."),
 ("He Turned Their Rivers into Blood (vv.40-55)",
  "How oft did they provoke him in the wilderness, and grieve him in the desert. The plagues are recited "
  "and the selection is not the familiar order, blood, flies, frogs, caterpillars, hail, frost, thunder, "
  "and the death of the firstborn. What the psalm keeps returning to is not the miracles but the failure "
  "to draw a conclusion from them, they remembered not his hand, nor the day when he delivered them from "
  "the enemy. And the section ends at the settlement, he cast out the heathen also before them, and divided "
  "them an inheritance by line."),
 ("He Forsook the Tabernacle of Shiloh (vv.56-64)",
  "Yet they tempted and provoked the most high God, and kept not his testimonies. The rebellion continues "
  "after the land is given, and the specific charge is worship, they provoked him to anger with their high "
  "places. Then the event this section exists for, and it is the one Jeremiah 7 argues from, so that he "
  "forsook the tabernacle of Shiloh, the tent which he placed among men, and delivered his strength into "
  "captivity. The ark was captured, the priests killed, and the sanctuary abandoned, which is the "
  "precedent for everything Book III is lamenting."),
 ("He Chose David His Servant (vv.65-72)",
  "Then the Lord awaked as one out of sleep, and like a mighty man that shouteth by reason of wine. The "
  "image is startling and the psalm offers no apology for it. What follows is a choice stated as a "
  "rejection and a selection, moreover he refused the tabernacle of Joseph, and chose not the tribe of "
  "Ephraim, but chose the tribe of Judah, the mount Zion which he loved. And the psalm's last word is not "
  "about a building or a nation but about one man's competence, he chose David also his servant, and took "
  "him from the sheepfolds, so he fed them according to the integrity of his heart, and guided them by the "
  "skilfulness of his hands. After seventy verses of failure, the resolution is a shepherd who is good at "
  "the job."),
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
