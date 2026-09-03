#!/usr/bin/env python3
"""
Proverbs 20 to 29: the second block of collected sayings. Ten pages.

Same treatment as 10 to 19, and for the same measured reason. The inherited sublists
on these ten pages are topical indexes, not outlines. proverbs20's covers nine verses
of thirty and proverbs28's indexes verse 22 twice under two different headings, so
folding them as though they were outlines would leave large gaps and duplicate
coverage. They are preserved in a labelled field, and the sections are written new as
contiguous blocks.

Two of these chapters carry a real structural seam, and the sections follow it rather
than dividing on a round number. proverbs22 changes collection at verse 17, where the
Solomonic couplets stop and the words of the wise begin, and proverbs24 changes again
at verse 23 with a second heading of its own. proverbs25 opens the collection that
Hezekiah's men copied out, which is the only place in the Old Testament that describes
its own editorial history. proverbs26 is the exception in the other direction: it is
genuinely built in three blocks, fools, then the sluggard, then the troublemaker, so
the sections coincide with the chapter's own joints.

Usage:
    python3 fold_proverbs_sayings_20_29.py [--check]
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
LI = re.compile(r"<li>(.*?)</li>", re.S)

SECTIONS = {
"proverbs20": [
 ("Wine, Kings and the Clean Heart (vv.1-11)",
  "The chapter opens on drink and does not soften it, wine is a mocker, strong drink is raging, "
  "and whosoever is deceived thereby is not wise. Then a run on the weight of a king's anger, the "
  "honour of leaving off strife, and the sluggard who will not plow by reason of the cold and so "
  "shall beg in harvest. The block turns on the question at verse 9, who can say, I have made my "
  "heart clean, I am pure from my sin, which is the nearest the collection comes to the doctrine "
  "of universal guilt that Paul argues at length in Romans 3. It closes on false weights being an "
  "abomination and on the observation that a child is known by his doings."),
 ("Trade, Counsel and the Hasty Inheritance (vv.12-21)",
  "The middle of the chapter is mostly about buying, selling and borrowing, and it contains the "
  "sharpest piece of market observation in the book, it is naught, it is naught, saith the buyer, "
  "when he is gone his way, then he boasteth. Around it sit the hearing ear and the seeing eye "
  "which the LORD hath made both of them, the warning not to love sleep, the pledge given for a "
  "stranger, and bread of deceit that is sweet before it turns to gravel. The block closes on "
  "money that arrives too easily, an inheritance may be gotten hastily at the beginning, but the "
  "end thereof shall not be blessed."),
 ("Vengeance Left to God, and the King's Sifting (vv.22-30)",
  "The last stretch begins with a prohibition the New Testament takes up directly, say not thou, "
  "I will recompense evil, but wait on the LORD, and he shall save thee. What follows is a group "
  "of sayings about limits on human knowledge and human self-rule, man's goings are of the LORD, "
  "how can a man then understand his own way, and the spirit of man is the candle of the LORD, "
  "searching all the inward parts. The king appears twice, scattering evil with his eyes and "
  "preserved by mercy and truth. The chapter ends on a pair about age and about pain that "
  "instructs, the glory of young men is their strength, and the beauty of old men is the grey head."),
],
"proverbs21": [
 ("The King's Heart and the Weighing of Ways (vv.1-8)",
  "The opening verse claims more than any other saying in the collection, the king's heart is in "
  "the hand of the LORD, as the rivers of water, he turneth it whithersoever he will, which places "
  "the most powerful human will inside another's. Verse 2 puts the reader in the same position, "
  "every way of a man is right in his own eyes, but the LORD pondereth the hearts. Verse 3 states "
  "the priority the prophets spent whole books on, to do justice and judgment is more acceptable "
  "to the LORD than sacrifice. The block closes on the thoughts of the diligent, on treasure got "
  "by a lying tongue, and on the way of a man being froward and strange."),
 ("The Housetop Corner and the Price of Pleasure (vv.9-20)",
  "This block collects the chapter's domestic and economic complaints. It is better to dwell in a "
  "corner of the housetop than with a brawling woman in a wide house, a saying repeated almost "
  "word for word at verse 19 with the wilderness in place of the roof, which is one sign that "
  "these chapters were assembled rather than composed. Between them stand the ear stopped at the "
  "cry of the poor, the gift that pacifies anger, and the pair of verses on appetite, he that "
  "loveth pleasure shall be a poor man, and there is treasure and oil in the dwelling of the wise, "
  "but a foolish man spendeth it up."),
 ("Guarded Speech, and the Horse Prepared for Battle (vv.21-31)",
  "The chapter ends on speech and on the limits of preparation. Whoso keepeth his mouth and his "
  "tongue keepeth his soul from troubles is the plainest sentence in it. The desire of the "
  "slothful killeth him, and the sacrifice of the wicked is abomination, which repeats the "
  "priority set at verse 3. The last two verses close the chapter where the first opened it, on "
  "the futility of setting anything against God, there is no wisdom, nor understanding, nor "
  "counsel, against the LORD, and then the image the chapter is remembered for, the horse is "
  "prepared against the day of battle, but safety is of the LORD."),
],
"proverbs22": [
 ("The Last of the Solomonic Couplets (vv.1-16)",
  "These sixteen verses end the collection that began at chapter 10, and they are weighted toward "
  "money and class. The rich and poor meet together, the LORD is the maker of them all, and then "
  "the sentence that has described debt ever since, the rich ruleth over the poor, and the "
  "borrower is servant to the lender. The block contains the most quoted and most argued verse in "
  "the book, train up a child in the way he should go, and when he is old, he will not depart from "
  "it, whose Hebrew is terse enough that it has been read both as a promise and as a plain "
  "observation about habit. It closes on oppression of the poor for private gain."),
 ("The Words of the Wise Begin (vv.17-29)",
  "Verse 17 starts a new collection with a new voice, bow down thine ear, and hear the words of "
  "the wise, and the form changes with it, from single couplets back to short addressed "
  "instructions of two and three verses each. Verse 20 says the writer has already written "
  "excellent things, a phrase whose Hebrew some read as thirty sayings, and scholars have long "
  "noted how closely this section through 24:22 tracks the Egyptian Instruction of Amenemope, "
  "which is arranged in thirty chapters and dates several centuries earlier. The block warns "
  "against robbing the poor because the LORD will plead their cause, against friendship with an "
  "angry man, against standing surety, and against removing the ancient landmark, and it ends on "
  "competence as a way into the room, a man diligent in his business shall stand before kings."),
],
"proverbs23": [
 ("At a Ruler's Table, and Riches That Fly Away (vv.1-11)",
  "The instructions continue, and the first is about a meal that is a test rather than a courtesy, "
  "when thou sittest to eat with a ruler, consider diligently what is before thee. Then the "
  "warning the chapter is best known for, labour not to be rich, followed by its image, riches "
  "certainly make themselves wings, they fly away as an eagle toward heaven. The block includes "
  "the grudging host whose bread should not be eaten, counsel not to waste words on a fool, and "
  "the old landmark again, this time with a reason attached that gives the orphan a legal "
  "advocate, their redeemer is mighty, he shall plead their cause with thee."),
 ("Correction, and a Father's Gladness (vv.12-18)",
  "A short block on discipline given and received. Withhold not correction from the child is set "
  "beside the motive that runs under all of it, my son, if thine heart be wise, my heart shall "
  "rejoice, even mine. The teacher here is not enforcing rules but hoping to be gladdened. The "
  "block closes on patience with the apparent success of the wicked, let not thine heart envy "
  "sinners, but be thou in the fear of the LORD all the day long, and on the assurance that there "
  "is a latter end and the hope of it shall not be cut off."),
 ("Winebibbers, Gluttons and the Deep Ditch (vv.19-28)",
  "The chapter gathers its warnings about appetite. Be not among winebibbers, among riotous eaters "
  "of flesh, because the drunkard and the glutton shall come to poverty and drowsiness shall "
  "clothe a man with rags. Between them stands the line that treats truth as a purchase to be "
  "made once and never resold, buy the truth, and sell it not, and the request that is the "
  "emotional center of these instructions, my son, give me thine heart. The block ends on the "
  "strange woman as a deep ditch and a narrow pit, lying in wait as for a prey."),
 ("The Portrait of the Drunkard (vv.29-35)",
  "The last seven verses are the longest sustained passage in the collections and the only one "
  "built as a scene. It opens with a riddle, who hath woe, who hath sorrow, and answers it, they "
  "that tarry long at the wine. Then the instruction, look not thou upon the wine when it is red, "
  "when it giveth his colour in the cup, and the reason, at the last it biteth like a serpent, and "
  "stingeth like an adder. What follows is observed from inside: the swimming eyes, the ground that "
  "will not hold still, the beating not felt, when shall I awake. The closing line is the point of "
  "the whole portrait, I will seek it yet again."),
],
"proverbs24": [
 ("The House Built by Wisdom, and the Duty to Rescue (vv.1-12)",
  "The instructions turn to strength and its sources. Through wisdom is an house builded, and by "
  "understanding it is established, which uses the same building language chapter 9 used of "
  "wisdom's own house. A wise man is strong, and by wise counsel thou shalt make thy war, so "
  "competence is treated as a form of power. Verse 10 is the shortest measure of character in the "
  "book, if thou faint in the day of adversity, thy strength is small. The block closes on an "
  "obligation stated with no way around it, deliver them that are drawn unto death, and refuses "
  "the excuse in advance, if thou sayest, Behold, we knew it not, doth not he that pondereth the "
  "heart consider it."),
 ("The Just Man Rising Again, and the End of the Wicked (vv.13-22)",
  "This block ends the words of the wise. It contains the verse most often used as a description "
  "of resilience, a just man falleth seven times, and riseth up again, but the wicked shall fall "
  "into mischief. Beside it is a discipline about enemies that the New Testament repeats twice, "
  "rejoice not when thine enemy falleth, and let not thine heart be glad when he stumbleth. And "
  "the reason given is not sympathy but restraint, lest the LORD see it, and it displease him. The "
  "collection closes on fearing the LORD and the king, and on calamity that rises suddenly."),
 ("A Further Word to the Wise, and the Sluggard's Field (vv.23-34)",
  "Verse 23 opens a short appendix with a heading of its own, these things also belong to the "
  "wise, and it begins in a courtroom, he that saith unto the wicked, Thou art righteous, him "
  "shall the people curse. Then a group about order of operations and about honesty between "
  "neighbours, prepare thy work without, and afterwards build thine house, and say not, I will do "
  "so to him as he hath done to me. The chapter ends on the one piece of reportage in these "
  "chapters, a walk past the field of the slothful, all grown over with thorns and its stone wall "
  "broken down, and the conclusion drawn from looking at it, yet a little sleep, a little slumber, "
  "so shall thy poverty come as one that travelleth."),
],
"proverbs25": [
 ("Hezekiah's Men, the King's Court and Words Fitly Spoken (vv.1-14)",
  "Verse 1 is a piece of editorial history no other book in the Old Testament supplies about "
  "itself, these are also proverbs of Solomon, which the men of Hezekiah king of Judah copied out. "
  "Hezekiah reigned around 700 BC, roughly two and a half centuries after Solomon, so the note "
  "records a collection being gathered and copied long after its sayings were first spoken. What "
  "follows is court material. It is the glory of God to conceal a thing, but the honour of kings "
  "is to search out a matter. Put not forth thyself in the presence of the king, better it be said "
  "unto thee, Come up hither, which Jesus turns into a parable about wedding seats in Luke 14. And "
  "the chapter's best known line about language, a word fitly spoken is like apples of gold in "
  "pictures of silver."),
 ("Honey, Neighbours and Coals of Fire (vv.15-28)",
  "The second half is built almost entirely of similes, and most of them are about knowing when to "
  "stop. Hast thou found honey, eat so much as is sufficient for thee. Withdraw thy foot from thy "
  "neighbour's house, lest he be weary of thee. A soft tongue breaketh the bone. The block "
  "contains the instruction Paul quotes in Romans 12, if thine enemy be hungry, give him bread to "
  "eat, together with the promise attached to it, thou shalt heap coals of fire upon his head, "
  "which is read either as shaming him into repentance or as leaving the judgment to God. The "
  "chapter closes on the failure all these measures are guarding against, he that hath no rule "
  "over his own spirit is like a city that is broken down, without walls."),
],
"proverbs26": [
 ("The Fool, Answered and Not Answered (vv.1-12)",
  "The chapter is one of the few in the collections that is genuinely built in blocks, and the "
  "first is twelve verses on the fool. It works by comparison throughout, as snow in summer, as "
  "rain in harvest, as a whip for the horse and a bridle for the ass so a rod for the fool's back, "
  "as he that bindeth a stone in a sling. At its centre sit the two verses most often used to "
  "argue that the book contradicts itself, answer not a fool according to his folly, lest thou "
  "also be like unto him, and immediately answer a fool according to his folly, lest he be wise in "
  "his own conceit. Placed side by side deliberately, they say that the same reply can be right or "
  "wrong depending on what it costs. The block ends where it will sting a reader rather than a "
  "fool, a man wise in his own conceit is further from help than the fool is."),
 ("The Sluggard on His Hinges (vv.13-16)",
  "Four verses, and they are comic rather than severe. The slothful man says there is a lion in the "
  "way, which is an excuse elaborate enough to be a kind of work. He turns upon his bed as the "
  "door turneth upon his hinges, active and going nowhere. He hides his hand in his bosom and it "
  "grieves him to bring it to his mouth again. And the last verse ties this block to the one "
  "before it by the same fault, he is wiser in his own conceit than seven men that can render a "
  "reason."),
 ("The Meddler, the Talebearer and the Flattering Mouth (vv.17-28)",
  "The last block is about damage done with words and with interference. He that passeth by, and "
  "meddleth with strife belonging not to him, is like one that taketh a dog by the ears. The man "
  "who deceives his neighbour and then says, Am not I in sport, is set beside a madman throwing "
  "firebrands. Where no wood is, there the fire goeth out, so where there is no talebearer, the "
  "strife ceaseth. The block gives the collection's clearest account of flattery as concealment, a "
  "potsherd covered with silver dross, and ends on consequences that come back to the sender, "
  "whoso diggeth a pit shall fall therein, and a flattering mouth worketh ruin."),
],
"proverbs27": [
 ("Tomorrow, Friends and Open Rebuke (vv.1-14)",
  "The chapter opens on the limits of planning, boast not thyself of tomorrow, for thou knowest "
  "not what a day may bring forth, which James expands into a paragraph in his fourth chapter. "
  "What follows is the fullest treatment of friendship in the book, and it is unsentimental. Open "
  "rebuke is better than secret love. Faithful are the wounds of a friend, but the kisses of an "
  "enemy are deceitful. Better is a neighbour that is near than a brother far off. The block also "
  "carries the observation that envy is harder to stand before than wrath, and the one genuinely "
  "funny verse in the chapter, blessing your friend loudly and early in the morning counts as a "
  "curse."),
 ("Iron Sharpening Iron, and the State of the Flocks (vv.15-27)",
  "The second half turns on how people are formed and what they are responsible for. Iron "
  "sharpeneth iron, so a man sharpeneth the countenance of his friend, and beside it as in water "
  "face answereth to face, so the heart of man to man, both saying that character is made in "
  "company rather than alone. The fining pot tries silver and praise tries a man. The chapter then "
  "ends in an unexpected place for a wisdom collection, in a farmyard, be thou diligent to know "
  "the state of thy flocks, because riches are not for ever and the crown does not pass by itself "
  "to every generation. The closing verses count the return, goats' milk enough for thy food, for "
  "the food of thy household, and for the maintenance for thy maidens."),
],
"proverbs28": [
 ("Bold as a Lion, and Sin Confessed (vv.1-14)",
  "The chapter opens with a contrast in bearing rather than in outcome, the wicked flee when no man "
  "pursueth, but the righteous are bold as a lion. Much of the block is about government and "
  "money, for the transgression of a land many are the princes, and the substance increased by "
  "usury and unjust gain that will be gathered by someone who pities the poor. Twice it prefers "
  "the poor man who walks uprightly to the rich man who is perverse. At verse 13 it states the "
  "condition the rest of the Bible builds a doctrine on, he that covereth his sins shall not "
  "prosper, but whoso confesseth and forsaketh them shall have mercy, and it is immediately "
  "balanced by a blessing on the man who is never quite at ease, happy is the man that feareth "
  "alway."),
 ("Hasty Riches, Self-Trust and the Rising of the Wicked (vv.15-28)",
  "The second half is a study in haste and in misplaced confidence. He that maketh haste to be "
  "rich shall not be innocent, and the man who hastens after wealth has an evil eye and does not "
  "consider that poverty shall come upon him. Against that stands slow work, he that tilleth his "
  "land shall have plenty of bread. The two verses at the turn state the choice the chapter has "
  "been circling, he that putteth his trust in the LORD shall be made fat, and he that trusteth in "
  "his own heart is a fool. The last verse repeats the opening image from the other side, when the "
  "wicked rise, men hide themselves, but when they perish, the righteous increase."),
],
"proverbs29": [
 ("The Hardened Neck, and Rulers Who Hear (vv.1-14)",
  "The chapter opens on the point past which correction stops working, he that being often "
  "reproved hardeneth his neck shall suddenly be destroyed, and that without remedy. Most of the "
  "block is about public life, which is the concern that runs through this last collection more "
  "than any other. When the righteous are in authority, the people rejoice, but when the wicked "
  "beareth rule, the people mourn. The king by judgment establisheth the land. If a ruler hearken "
  "to lies, all his servants are wicked, which makes the character of a court the responsibility "
  "of the man at the top of it. The block closes on the poor twice, meeting the rich as equals "
  "before their maker, and judged faithfully by a king whose throne is established by doing it."),
 ("The Rod, the Vision and the Fear of Man (vv.15-27)",
  "The second half returns to discipline in the household and then widens. Verse 18 is the most "
  "quoted line in the chapter and the most often misused, where there is no vision, the people "
  "perish, but he that keepeth the law, happy is he. The vision meant is prophetic revelation, not "
  "ambition or strategic planning, and the second half of the verse says so by putting the law in "
  "parallel with it. Around it sit the rod and reproof that give wisdom, the servant who will not "
  "be corrected by words, the man hasty in his words, and pride that brings a man low. The "
  "collection ends on where a person looks for safety, the fear of man bringeth a snare, but whoso "
  "putteth his trust in the LORD shall be safe."),
],
}

INDEX_LABEL = "Themes in This Chapter:"


def verify(planned):
    """Apply the audit's rules to the planned HTML without writing it."""
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
            found.append(f"{page}: described twice {sorted({v for v, _ in repeated})}")
        if starts != sorted(starts):
            found.append(f"{page}: sections out of verse order")
        if "<li>" in pane:
            found.append(f"{page}: sublist survived")
        if INDEX_LABEL not in [l for l in labels]:
            found.append(f"{page}: topical index was lost")
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label) if w not in A.CAPS_OK})
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
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in ("Author:", "Historical Context:")]
        if len(keep) != 2:
            problems.append(f"{page}: expected two book fields, found {len(keep)}")
            continue
        topics = [H.unescape(re.sub(r"<.*?>", "", x)).strip() for x in LI.findall(body_html)]
        if not topics:
            problems.append(f"{page}: no topical index to preserve")
            continue
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        parts.append(ITEM.format(label=INDEX_LABEL, body="; ".join(topics)) + "\n")
        notes.append(f"{page}: preserved {len(topics)} indexed themes")
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
    print(f"{'would fold' if check else 'folded'} {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
