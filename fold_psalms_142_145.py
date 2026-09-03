#!/usr/bin/env python3
"""
Psalms 142 to 145. Four pages, 55 verses. All four outlines are gapless and are folded.

psalms144:3 asks the question Psalm 8:4 asks, in almost the same words, and gives the opposite
answer. Psalm 8 says man is crowned with glory and honour; this psalm says man is like to
vanity. The section names the pair, because the psalter putting both on record is the point and
neither one is its final word.

psalms145 is the last psalm attributed to David and an alphabet acrostic with a letter missing.
The Hebrew text jumps from mem to samekh between verses 13 and 14, leaving out nun, and a line
supplying it appears in the Greek and in the Dead Sea scroll of the psalms. The section states
the fact and states that the English versions differ over whether to print the extra line,
since a reader comparing two Bibles at this verse will find them disagreeing.

Usage:
    python3 fold_psalms_142_145.py [--check]
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
"psalms142": [
 ("I Poured Out My Complaint Before Him (vv.1-2)",
  "I cried unto the LORD with my voice; with my voice unto the LORD did I make my supplication. The "
  "superscription says a prayer when he was in the cave, which points to Adullam in 1 Samuel 22 or En-gedi in "
  "1 Samuel 24, both times when David was hiding rather than reigning. Voice is insisted on twice, so this is "
  "not silent prayer. I poured out my complaint before him; I shewed before him my trouble, where pouring out "
  "is the psalter's usual figure for saying everything without arranging it."),
 ("Then Thou Knewest My Path (v.3)",
  "When my spirit was overwhelmed within me, then thou knewest my path. The claim is that God's knowledge was "
  "the one thing still working when the speaker's own sense of direction failed. In the way wherein I walked "
  "have they privily laid a snare for me, which is what made the path a question."),
 ("No Man Cared for My Soul (v.4)",
  "I looked on my right hand, and beheld, but there was no man that would know me: refuge failed me; no man "
  "cared for my soul. The right hand is where a defender stands, and the verse reports it empty. This is the "
  "flattest statement of abandonment in the psalter, and the psalm does not qualify it or hint that friends "
  "were there after all."),
 ("My Refuge and My Portion in the Land of the Living (v.5)",
  "I cried unto thee, O LORD: I said, Thou art my refuge and my portion in the land of the living. The two "
  "words answer verse 4 exactly, since refuge is the thing that failed and portion is the inheritance a man "
  "with no land has. In the land of the living means now rather than after death, which is what a man in a "
  "cave needs it to mean."),
 ("Bring My Soul out of Prison (vv.6-7)",
  "Attend unto my cry; for I am brought very low: deliver me from my persecutors; for they are stronger than "
  "I. The admission of relative weakness is offered as a reason rather than concealed. Bring my soul out of "
  "prison, that I may praise thy name, and the prison is most likely the cave itself, described from inside as "
  "confinement rather than shelter. The last line expects company again, the righteous shall compass me about, "
  "which answers the empty right hand of verse 4."),
],
"psalms143": [
 ("No Man Living Shall Be Justified (vv.1-2)",
  "Hear my prayer, O LORD, give ear to my supplications: in thy faithfulness answer me, and in thy "
  "righteousness. The last of the seven penitential psalms, and the ground it stands on is God's character "
  "rather than the speaker's case. Then the verse that had a long future, and enter not into judgment with thy "
  "servant: for in thy sight shall no man living be justified. Paul argues from this in Romans 3:20 and "
  "Galatians 2:16, and the psalm has already conceded the point he uses it to make: the speaker does not want "
  "his day in court."),
 ("As Those That Have Been Long Dead (vv.3-4)",
  "For the enemy hath persecuted my soul; he hath smitten my life down to the ground; he hath made me to dwell "
  "in darkness, as those that have been long dead. The comparison is not to the newly dead but to the long "
  "dead, which is a colder image: not grief but oblivion. Therefore is my spirit overwhelmed within me; my "
  "heart within me is desolate."),
 ("My Soul Thirsteth After Thee, as a Thirsty Land (vv.5-6)",
  "I remember the days of old; I meditate on all thy works; I muse on the work of thy hands. The three verbs "
  "describe deliberate work done on memory, which is this psalm's only method for getting out of verse 4. I "
  "stretch forth my hands unto thee: my soul thirsteth after thee, as a thirsty land, and the image is of "
  "ground cracked open rather than of a person wanting a drink."),
 ("Cause Me to Hear Thy Lovingkindness in the Morning (vv.7-10)",
  "Hear me speedily, O LORD: my spirit faileth: hide not thy face from me. Four verses of requests, and what "
  "is asked for is mostly guidance rather than rescue, cause me to know the way wherein I should walk, teach "
  "me to do thy will. Cause me to hear thy lovingkindness in the morning, which asks for news at the hour when "
  "a night of trouble ends. Then one of the few lines in the Old Testament about being led by the Spirit, thy "
  "spirit is good; lead me into the land of uprightness, where the land of uprightness is level ground, the "
  "opposite of the snare-strewn path of Psalm 142."),
 ("For I Am Thy Servant (vv.11-12)",
  "Quicken me, O LORD, for thy name's sake: for thy righteousness' sake bring my soul out of trouble. Both "
  "reasons offered are God's own, which is consistent with verse 2 having ruled out the speaker's merits. And "
  "of thy mercy cut off mine enemies. Mercy is named as the motive for their destruction, which is jarring and "
  "is the psalm's own logic: the mercy is toward the speaker. The last three words are the only claim he "
  "makes for himself, for I am thy servant."),
],
"psalms144": [
 ("Which Teacheth My Hands to War (vv.1-2)",
  "Blessed be the LORD my strength, which teacheth my hands to war, and my fingers to fight. The psalm opens "
  "with a stack of titles taken almost entirely from Psalm 18, my fortress, my high tower, my deliverer, my "
  "shield, which is one of several places where a late psalm is built out of an earlier one. The skill is "
  "attributed rather than claimed: the hands were taught."),
 ("Man Is like to Vanity (vv.3-4)",
  "LORD, what is man, that thou takest knowledge of him! or the son of man, that thou makest account of him! "
  "Psalm 8:4 asks this in nearly the same words and answers that man is crowned with glory and honour. This "
  "psalm answers differently, man is like to vanity: his days are as a shadow that passeth away, where vanity "
  "is hebel, the word Ecclesiastes uses throughout for breath or vapour. Both answers are in the psalter and "
  "neither is presented as correcting the other, which is worth knowing before either is quoted alone."),
 ("Bow Thy Heavens, O LORD, and Come Down (vv.5-8)",
  "Bow thy heavens, O LORD, and come down: touch the mountains, and they shall smoke. The request is for a "
  "theophany on the pattern of Sinai, and the weapons asked for are the storm's, cast forth lightning, and "
  "scatter them: shoot out thine arrows. Then the trouble is named and it is oddly domestic after all that, "
  "rid me, and deliver me out of great waters, from the hand of strange children, whose mouth speaketh "
  "vanity, and their right hand is a right hand of falsehood. A right hand of falsehood is a hand raised to "
  "swear an oath it will not keep, so the psalm asks for lightning against perjury."),
 ("I Will Sing a New Song unto Thee (vv.9-11)",
  "I will sing a new song unto thee, O God: upon a psaltery and an instrument of ten strings will I sing "
  "praises unto thee. The vow of praise comes before the deliverance, which is the ordinary shape of a lament. "
  "It is he that giveth salvation unto kings: who delivereth David his servant from the hurtful sword. Then "
  "verse 8 is repeated word for word at verse 11, which reads as a refrain rather than an error and suggests "
  "the psalm was sung with a repeat."),
 ("Happy Is That People, Whose God Is the LORD (vv.12-15)",
  "That our sons may be as plants grown up in their youth; that our daughters may be as corner stones, "
  "polished after the similitude of a palace. The last four verses change subject entirely and describe the "
  "peace that would follow the rescue, and it is all agriculture and family: full granaries, sheep bringing "
  "forth thousands, oxen strong to labour. The Hebrew behind corner stones is uncertain and may mean carved "
  "corner pillars, an image of stately ornament either way. What is wished for at the end is negative and very "
  "concrete, that there be no breaking in, nor going out; that there be no complaining in our streets. Then "
  "the psalm's conclusion, said twice with the ground shifted the second time, happy is that people, that is "
  "in such a case: yea, happy is that people, whose God is the LORD, so the prosperity is put second to the "
  "one who gives it."),
],
"psalms145": [
 ("His Greatness Is Unsearchable (vv.1-3)",
  "I will extol thee, my God, O king; and I will bless thy name for ever and ever. The last psalm in the "
  "psalter attributed to David, and an acrostic running the Hebrew alphabet a line at a time. It is the core "
  "of the Ashrei, said three times daily in Jewish prayer. Every day will I bless thee. Then a claim that "
  "limits everything the psalm goes on to say, and his greatness is unsearchable, so the twenty verses "
  "following are offered as a report from a subject that cannot be finished."),
 ("One Generation Shall Praise Thy Works to Another (vv.4-7)",
  "One generation shall praise thy works to another, and shall declare thy mighty acts. Praise is described as "
  "a chain of transmission rather than an emotion, and the psalm keeps alternating between what I will say and "
  "what they shall say. And men shall speak of the might of thy terrible acts, where terrible keeps its older "
  "sense of awe-inspiring. They shall abundantly utter the memory of thy great goodness."),
 ("His Tender Mercies Are over All His Works (vv.8-9)",
  "The LORD is gracious, and full of compassion; slow to anger, and of great mercy. Exodus 34:6 again, the "
  "sentence the Old Testament quotes about God more than any other. Then the psalm pushes it further than most "
  "of its uses go, the LORD is good to all: and his tender mercies are over all his works, which extends the "
  "kindness past Israel to everything made."),
 ("Thy Kingdom Is an Everlasting Kingdom (vv.10-13)",
  "All thy works shall praise thee, O LORD; and thy saints shall bless thee. The subject for four verses is "
  "the kingdom, and what is said of it is duration, thy kingdom is an everlasting kingdom, and thy dominion "
  "endureth throughout all generations. Something is missing here. The acrostic goes from mem at verse 13 to "
  "samekh at verse 14 and skips nun, and a line beginning with that letter, faithful is the LORD in all his "
  "words, appears in the Septuagint and in the Dead Sea scroll of the psalms. English Bibles differ over "
  "whether to print it, some giving it in the text and some in a note, so two readers comparing versions at "
  "this verse will not find the same number of lines. The Hebrew tradition preserved the gap and did not fill "
  "it."),
 ("Thou Openest Thine Hand (vv.14-16)",
  "The LORD upholdeth all that fall, and raiseth up all those that be bowed down. After four verses on an "
  "everlasting kingdom the psalm turns to people who cannot stand up, which is the sequence it wants. The eyes "
  "of all wait upon thee; and thou givest them their meat in due season. Then a line Psalm 104 also uses of "
  "the animals, thou openest thine hand, and satisfiest the desire of every living thing, so the feeding is "
  "not confined to the congregation."),
 ("The LORD Is Nigh unto All Them That Call upon Him (vv.17-20)",
  "The LORD is righteous in all his ways, and holy in all his works. What follows is the psalm's warmest "
  "claim and it comes with a qualification attached, the LORD is nigh unto all them that call upon him, to all "
  "that call upon him in truth. In truth rules out the calling that is only noise, and it is the one condition "
  "the psalm sets. He will fulfil the desire of them that fear him. The last line is the psalm's only hard "
  "sentence and it is not softened, the LORD preserveth all them that love him: but all the wicked will he "
  "destroy."),
 ("Let All Flesh Bless His Holy Name (v.21)",
  "My mouth shall speak the praise of the LORD: and let all flesh bless his holy name for ever and ever. The "
  "acrostic ends where it began, with one man's mouth, and then hands the sentence to everything alive. All "
  "flesh is the widest term available, and this last verse of the last Davidic psalm sets up the five "
  "hallelujah psalms that close the book by making the congregation the whole of creation."),
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
