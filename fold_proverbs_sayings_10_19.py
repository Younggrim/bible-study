#!/usr/bin/env python3
"""
Proverbs 10 to 19: the first block of collected sayings. Ten pages.

These chapters need a different treatment from 1 to 9, and the reason is measurable.
The inherited sublists here are not outlines. proverbs14's covers nine verses of
thirty-five, proverbs20's covers nine of thirty, and several overlap themselves
because a single proverb can be indexed under two topics. Folding them into sections
the way Hosea's outline was folded would produce large gaps and duplicate coverage.

They are a topical index, and a useful one, so they are preserved as a field rather
than discarded. That follows the decision made for Song of Solomon's speaker
attributions: an inherited field that does real work and is not an outline keeps its
content, in a labelled field, without a sublist.

The sections themselves are written new, as contiguous blocks labelled by what the
block actually contains. This is the honest form for a miscellany. Where a chapter
does have a real cluster the section follows it, as at 16:1-9 on the LORD and human
planning. Where it does not, the label says what range of subjects a reader will meet
rather than pretending to a unity the text has not got. Sections here are shorter than
in the narrative books on purpose: a chapter of thirty unconnected couplets does not
support the same kind of exposition as a chapter of Mark, and padding it would
misdescribe the material.

Usage:
    python3 fold_proverbs_sayings_10_19.py [--check]
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
"proverbs10": [
 ("The Righteous and the Wicked Contrasted (vv.1-14)",
  "The collection proper begins here, and the form changes completely: no more discourse, just "
  "single verses in pairs, most of them built on but. The opening verse sets the frame for the "
  "whole book, a wise son maketh a glad father, but a foolish son is the heaviness of his mother. "
  "The block runs through treasures of wickedness, the slack hand and the diligent hand, "
  "harvesting in summer and sleeping in harvest, and then a run on the mouth: the mouth of the "
  "wicked, the mouth of the righteous as a well of life, and the observation that love covereth "
  "all sins. Verse 12 is quoted in 1 Peter 4."),
 ("Speech, Labour and Their Outcomes (vv.15-24)",
  "The middle of the chapter turns on what work and words produce. The rich man's wealth is his "
  "strong city, and the destruction of the poor is their poverty, stated as observation rather "
  "than approval. Then the verse that stands apart from the pattern because it credits the source "
  "rather than the effort, the blessing of the LORD, it maketh rich, and he addeth no sorrow with "
  "it. The block closes on restraint, in the multitude of words there wanteth not sin, but he that "
  "refraineth his lips is wise, and on the tongue of the just as choice silver."),
 ("What the Righteous Gain and the Wicked Lose (vv.25-32)",
  "The last eight verses are almost all about duration. The whirlwind passes and the righteous is "
  "an everlasting foundation. The fear of the LORD prolongeth days, but the years of the wicked "
  "shall be shortened. The righteous shall never be removed. And the closing pair returns to the "
  "mouth, where the chapter began, the mouth of the just bringeth forth wisdom, but the froward "
  "tongue shall be cut out."),
],
"proverbs11": [
 ("Weights, Pride and Integrity (vv.1-11)",
  "The chapter opens with commerce, a false balance is abomination to the LORD, but a just weight "
  "is his delight, which is one of the few proverbs that names a specific business practice. Then "
  "pride and shame, and a run on what riches cannot do, riches profit not in the day of wrath. The "
  "block closes on a civic note that is unusual in the collection, by the blessing of the upright "
  "the city is exalted, so a private virtue is described as having a public effect."),
 ("Counsel, Surety and the Company Kept (vv.12-21)",
  "A cluster on discretion and advice. He that is void of wisdom despiseth his neighbour, but a "
  "man of understanding holdeth his peace. A talebearer revealeth secrets, but he that is of a "
  "faithful spirit concealeth the matter. Then the verse that has shaped centuries of committee "
  "practice, in the multitude of counsellors there is safety, and beside it a warning against "
  "standing surety for a stranger. The block includes the merciful man doing good to his own soul "
  "and the cruel man troubling his own flesh, which is the collection's habitual argument that "
  "conduct rebounds on the actor."),
 ("Generosity, Greed and the Fruit of the Righteous (vv.22-31)",
  "The most memorable image in the chapter opens the block, as a jewel of gold in a swine's snout, "
  "so is a fair woman which is without discretion. Then the paradox the chapter is remembered for, "
  "there is that scattereth, and yet increaseth, and there is that withholdeth more than is meet, "
  "and it tendeth to poverty, followed by the liberal soul that shall be made fat and he that "
  "watereth being watered himself. The block closes on the fruit of the righteous as a tree of "
  "life, and he that winneth souls is wise."),
],
"proverbs12": [
 ("The Virtuous Wife, Words and Roots (vv.1-14)",
  "The block opens on correction, whoso loveth instruction loveth knowledge, but he that hateth "
  "reproof is brutish, and includes one of the collection's bluntest domestic sayings, a virtuous "
  "woman is a crown to her husband, but she that maketh ashamed is as rottenness in his bones. "
  "Then a run on speech as a weapon or a rescue, the words of the wicked are to lie in wait for "
  "blood, but the mouth of the upright shall deliver them. The image that holds the block together "
  "is the root, the root of the righteous shall not be moved."),
 ("Truth, Prudence and the Tongue (vv.15-22)",
  "A cluster on self-control in speech. There is that speaketh like the piercing of a sword, but "
  "the tongue of the wise is health. A fool's wrath is known the same day, where a prudent man "
  "covereth shame. And the verse the block turns on, lying lips are abomination to the LORD, but "
  "they that deal truly are his delight, which pairs with the false balance that opened chapter 11."),
 ("Diligence, Anxiety and the Way of Life (vv.23-28)",
  "The chapter ends on work and worry. The hand of the diligent shall bear rule, but the slothful "
  "shall be under tribute. Then a verse that sits oddly among sayings about industry and is the "
  "kindest in the chapter, heaviness in the heart of man maketh it stoop, but a good word maketh it "
  "glad. The closing line states the collection's whole premise in eight words, in the way of "
  "righteousness is life."),
],
"proverbs13": [
 ("Words, Wealth and Discipline (vv.1-12)",
  "The block opens with a son hearing instruction and a scorner who will not, and runs through the "
  "keeping of the mouth, he that keepeth his mouth keepeth his life. It contains two observations "
  "about money that pull against each other on purpose, the ransom of a man's life are his riches, "
  "and there is that maketh himself rich, yet hath nothing. And it closes on the verse most often "
  "quoted from the chapter, hope deferred maketh the heart sick, but when the desire cometh, it is "
  "a tree of life."),
 ("Instruction, Company and the Rod (vv.13-25)",
  "The second half runs on who a person learns from. He that walketh with wise men shall be wise, "
  "but a companion of fools shall be destroyed, which is the chapter's plainest sentence. The block "
  "includes the much-argued verse on discipline, he that spareth his rod hateth his son, and a "
  "line about inheritance that reaches past one lifetime, a good man leaveth an inheritance to his "
  "children's children. The closing verse is about sufficiency rather than plenty, the righteous "
  "eateth to the satisfying of his soul."),
],
"proverbs14": [
 ("The House, the Heart and the Simple (vv.1-14)",
  "The block opens with building and demolition, every wise woman buildeth her house, but the "
  "foolish plucketh it down with her hands, and includes an agricultural aside that is unusually "
  "practical, where no oxen are, the crib is clean, but much increase is by the strength of the ox. "
  "Then the verse that appears twice in the book and is the collection's warning against "
  "self-assurance, there is a way which seemeth right unto a man, but the end thereof are the ways "
  "of death. And immediately before it, the loneliest sentence in Proverbs, the heart knoweth his "
  "own bitterness, and a stranger doth not intermeddle with his joy."),
 ("Poverty, Anger and the Fear of the LORD (vv.15-27)",
  "A cluster on temper and on how the poor are treated. He that is slow to wrath is of great "
  "understanding, but he that is hasty of spirit exalteth folly. Then two verses on friendship and "
  "money placed together without comment, the poor is hated even of his own neighbour, and the rich "
  "hath many friends, followed by he that hath mercy on the poor, happy is he. The block closes on "
  "the fear of the LORD as a fountain of life and a place of refuge for a man's children."),
 ("Nations, Kings and the Oppressed (vv.28-35)",
  "The last eight verses widen from the household to the state, and they are the most political in "
  "the chapter. In the multitude of people is the king's honour. Righteousness exalteth a nation, "
  "but sin is a reproach to any people. And the verse that gives the collection's theological "
  "ground for social conduct, he that oppresseth the poor reproacheth his Maker, but he that "
  "honoureth him hath mercy on the poor. The chapter ends at court, the king's favour is toward a "
  "wise servant."),
],
"proverbs15": [
 ("The Soft Answer and the Watching Eyes (vv.1-15)",
  "The chapter opens with the best-known verse in the collection, a soft answer turneth away "
  "wrath, but grievous words stir up anger, and keeps returning to the tongue throughout the block. "
  "Two verses stand out for making the LORD the observer rather than the judge, the eyes of the "
  "LORD are in every place, beholding the evil and the good, and the sacrifice of the wicked is an "
  "abomination, but the prayer of the upright is his delight. The block closes on contentment "
  "rather than provision, he that is of a merry heart hath a continual feast."),
 ("Correction, Counsel and the Household (vv.16-23)",
  "A cluster in which two verses set the terms by comparison rather than by rule: better is little "
  "with the fear of the LORD than great treasure with trouble, and better is a dinner of herbs "
  "where love is, than a stalled ox and hatred therewith. Both prefer the smaller portion. Then "
  "advice on planning that has outlived its setting, without counsel purposes are disappointed, "
  "but in the multitude of counsellors they are established."),
 ("Pride, Instruction and the Answer of the Heart (vv.24-33)",
  "The last block turns on who is willing to be told. The LORD will destroy the house of the proud, "
  "but he will establish the border of the widow. He that refuseth instruction despiseth his own "
  "soul. And the closing pair puts the chapter's whole argument in order of operations, the fear of "
  "the LORD is the instruction of wisdom, and before honour is humility."),
],
"proverbs16": [
 ("The LORD and Human Planning (vv.1-9)",
  "This is a real cluster rather than a miscellany, and it is the densest theological passage in "
  "the collected sayings. Nine verses, six of which name the LORD, and all of them are about the "
  "gap between intention and outcome. The preparations of the heart in man, and the answer of the "
  "tongue, is from the LORD. All the ways of a man are clean in his own eyes, but the LORD "
  "weigheth the spirits. Commit thy works unto the LORD, and thy thoughts shall be established. "
  "And the verse that closes the block and states it most plainly, a man's heart deviseth his way, "
  "but the LORD directeth his steps."),
 ("Kings, Pride and the Way of Life (vv.10-22)",
  "The middle of the chapter is court wisdom, and the sayings assume a reader near power: a divine "
  "sentence is in the lips of the king, the wrath of a king is as messengers of death, in the light "
  "of the king's countenance is life. Between them sits the most quoted verse in the chapter, pride "
  "goeth before destruction, and an haughty spirit before a fall, and beside it a preference stated "
  "as a bargain, better it is to be of an humble spirit with the lowly, than to divide the spoil "
  "with the proud."),
 ("Words, Restraint and Grey Hair (vv.23-33)",
  "The closing block returns to speech and then to self-command. Pleasant words are as an "
  "honeycomb, sweet to the soul, and health to the bones. Then the verse that measures strength by "
  "what it does not do, he that is slow to anger is better than the mighty, and he that ruleth his "
  "spirit than he that taketh a city. The hoary head is a crown of glory, if it be found in the way "
  "of righteousness, where the condition is doing real work. And the last verse leaves the outcome "
  "elsewhere, the lot is cast into the lap, but the whole disposing thereof is of the LORD."),
],
"proverbs17": [
 ("Quietness, Kin and the Crucible (vv.1-14)",
  "The opening verse prefers less of everything, better is a dry morsel, and quietness therewith, "
  "than an house full of sacrifices with strife. The block contains the chapter's hardest image, "
  "the fining pot is for silver, and the furnace for gold, but the LORD trieth the hearts, and its "
  "warmest, a friend loveth at all times, and a brother is born for adversity. It closes on the "
  "beginning of a quarrel described as a leak, the beginning of strife is as when one letteth out "
  "water, therefore leave off contention before it be meddled with."),
 ("Fools, Friends and the Merry Heart (vv.15-28)",
  "A cluster on speech and its absence. A merry heart doeth good like a medicine, but a broken "
  "spirit drieth the bones. He that hath knowledge spareth his words. And the chapter closes on two "
  "verses that make silence the test rather than eloquence, even a fool, when he holdeth his peace, "
  "is counted wise, and he that shutteth his lips is esteemed a man of understanding. In a book "
  "about instruction, the last word of the chapter is about keeping quiet."),
],
"proverbs18": [
 ("The Isolated Man, the Tongue and the Name (vv.1-12)",
  "The block opens on someone who has withdrawn, he that is alone seeketh his own desire, and "
  "meddleth with all wisdom, and includes two verses on hearing a case that any judge would "
  "recognise, he that answereth a matter before he heareth it, it is folly and shame unto him. Two "
  "images of refuge sit near each other and are deliberately unequal, the name of the LORD is a "
  "strong tower, and the rich man's wealth is his strong city. The block closes on the order the "
  "collection insists upon, before honour is humility."),
 ("Words, Wounds and the Wife (vv.13-24)",
  "The second half is almost entirely about speech and its aftermath. The words of a talebearer are "
  "as wounds. Death and life are in the power of the tongue. A brother offended is harder to win "
  "than a strong city. The chapter also contains a sentence about litigation that anyone who has "
  "sat in a hearing will recognise, he that is first in his own cause seemeth just, but his "
  "neighbour cometh and searcheth him. And the closing verse distinguishes between quantity and "
  "quality of company, a man that hath friends must shew himself friendly, and there is a friend "
  "that sticketh closer than a brother."),
],
"proverbs19": [
 ("Poverty, Haste and the Household (vv.1-14)",
  "The block opens by preferring integrity to speech, better is the poor that walketh in his "
  "integrity, than he that is perverse in his lips. Several verses observe how poverty affects "
  "friendship without moralising about it, wealth maketh many friends, but the poor is separated "
  "from his neighbour. Two sayings about temper are placed near each other, he that is hasty of "
  "spirit sinneth, and the discretion of a man deferreth his anger. And the block closes on "
  "domestic life with the chapter's most quoted line, a continual dropping, and beside it a house "
  "and riches are the inheritance of fathers, but a prudent wife is from the LORD."),
 ("Instruction, Kindness and the Fear of the LORD (vv.15-29)",
  "The second half is about correction and about who deserves care. He that hath pity upon the poor "
  "lendeth unto the LORD, and that which he hath given will he pay him again, which is the "
  "collection's boldest statement about charity. Then a cluster on raising children, chasten thy "
  "son while there is hope, and hear counsel, that thou mayest be wise in thy latter end. The "
  "chapter ends on the fear of the LORD tending to life, and on judgment prepared for scorners."),
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
