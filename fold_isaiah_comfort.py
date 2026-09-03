#!/usr/bin/env python3
"""
Isaiah 40 to 44: comfort, the first servant song, and the idol satire. Five pages,
141 verses. All five outlines are gapless and are folded.

Chapter 40 begins the second half of the book and the change of address is total. The
first thirty-nine chapters argue with a government that still has choices; from here the
audience is a people for whom the worst has already happened, and the opening word is
comfort ye, comfort ye my people.

Two features of these chapters are worth naming because they run through all of them.
The first is a legal argument about prediction: the gods of the nations are challenged to
say what will happen, at 41:22-23 and 43:9 and 44:7, and the challenge is presented as
the test that settles the question. The second is the servant, introduced at 42:1 and
identified as Israel at 41:8 and 44:21, which is the tension the four servant songs
develop and which chapter 53 brings to a point.

Usage:
    python3 fold_isaiah_comfort.py [--check]
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
KEEP = ("Author:", "Date:", "Classification:", "Key Themes:", "Historical Context:")
REPAIRS = {}

SECTIONS = {
"isaiah40": [
 ("Comfort Ye My People (vv.1-2)",
  "Comfort ye, comfort ye my people, saith your God. The imperative is plural and it is addressed to "
  "unnamed hearers, so the chapter opens by commissioning somebody to console rather than by consoling "
  "directly. What they are to say is legal in form, speak ye comfortably to Jerusalem, and cry unto her, "
  "that her warfare is accomplished, that her iniquity is pardoned, that she hath received of the LORD's "
  "hand double for all her sins. The sentence has been served, and the word double is doing something "
  "uncomfortable that the text does not soften."),
 ("The Voice in the Wilderness (vv.3-5)",
  "The voice of him that crieth in the wilderness, Prepare ye the way of the LORD, make straight in the "
  "desert a highway for our God. What is described is road-building for a royal progress, and the "
  "engineering is specified, every valley shall be exalted, and every mountain and hill shall be made "
  "low, and the crooked shall be made straight, and the rough places plain. All four Gospels apply these "
  "verses to John the Baptist, and the Hebrew punctuation allows either a voice crying in the wilderness "
  "or a voice crying that a way should be prepared in the wilderness."),
 ("All Flesh Is Grass (vv.6-8)",
  "The voice said, Cry. And he said, What shall I cry. The answer is not encouraging, all flesh is grass, "
  "and all the goodliness thereof is as the flower of the field. The comparison is developed as a "
  "specific event rather than a general truth, the grass withereth, the flower fadeth, because the spirit "
  "of the LORD bloweth upon it. And then the contrast the whole passage exists for, but the word of our "
  "God shall stand for ever. To an audience whose empire, temple and monarchy had all proved to be grass, "
  "the point is not pessimism. It is about which of the two things they had been relying on."),
 ("O Zion, That Bringest Good Tidings (vv.9-11)",
  "O Zion, that bringest good tidings, get thee up into the high mountain, lift up thy voice with "
  "strength, be not afraid. The messenger is Zion herself, so the city that was to be comforted is now "
  "doing the announcing. Then two pictures of the same arrival, and holding them together is the point: "
  "behold, the Lord GOD will come with strong hand, and his arm shall rule for him. And immediately, he "
  "shall feed his flock like a shepherd, he shall gather the lambs with his arm, and carry them in his "
  "bosom, and shall gently lead those that are with young. The strong arm and the carried lamb are the "
  "same arm."),
 ("Who Hath Measured the Waters (vv.12-17)",
  "Who hath measured the waters in the hollow of his hand, and meted out heaven with the span, and "
  "comprehended the dust of the earth in a measure. The argument runs by questions rather than "
  "assertions, and the units are all handspans and scales, so immensity is being described with the "
  "instruments of a market stall. Then the nations put on the same scales, behold, the nations are as a "
  "drop of a bucket, and are counted as the small dust of the balance. And Lebanon, the source of the "
  "most valuable timber in the region, is described as not enough for one fire, all nations before him "
  "are as nothing."),
 ("To Whom Then Will Ye Liken God (vv.18-20)",
  "To whom then will ye liken God, or what likeness will ye compare unto him. The answer is given by "
  "describing the alternative in workshop terms, the workman melteth a graven image, and the goldsmith "
  "spreadeth it over with gold, and casteth silver chains. Then the budget version, and it is the "
  "sharpest detail, he that is poor chooseth a tree that will not rot, and hires a craftsman, and the "
  "requirement stated for the finished god is that it should not fall over. The satire is procedural, "
  "which is the same method as 44:9-20 and Jeremiah 10."),
 ("The Circle of the Earth (vv.21-26)",
  "Have ye not known, have ye not heard, hath it not been told you from the beginning. It is he that "
  "sitteth upon the circle of the earth, and that stretcheth out the heavens as a curtain. Then the "
  "governments, which is where this passage lands rather than in cosmology, that bringeth the princes to "
  "nothing, he maketh the judges of the earth as vanity. And the closing image is an army roll call "
  "applied to the sky, lift up your eyes on high, and behold who hath created these things, that "
  "bringeth out their host by number, he calleth them all by names. Stars mustered like troops, none "
  "missing."),
 ("Why Sayest Thou, My Way Is Hid (vv.27-28)",
  "Why sayest thou, O Jacob, and speakest, O Israel, My way is hid from the LORD, and my judgment is "
  "passed over from my God. The complaint is quoted rather than described, and it is not disbelief in "
  "God but a conviction of having been overlooked, which is a harder thing to answer. The reply is a "
  "single sentence about stamina, the everlasting God, the LORD, the Creator of the ends of the earth, "
  "fainteth not, neither is weary."),
 ("They Shall Mount Up with Wings (vv.29-31)",
  "He giveth power to the faint, and to them that have no might he increaseth strength. The argument is "
  "then made by contrast rather than by promise, even the youths shall faint and be weary, and the young "
  "men shall utterly fall, so natural stamina is precisely what is not sufficient. And the closing verse "
  "runs its verbs in an order that surprises people who quote it, but they that wait upon the LORD shall "
  "renew their strength, they shall mount up with wings as eagles, they shall run, and not be weary, and "
  "they shall walk, and not faint. Flying, then running, then walking. The list descends to the thing "
  "hardest to keep doing."),
],
"isaiah41": [
 ("Let the Nations Come Near (vv.1-4)",
  "Keep silence before me, O islands, and let the people renew their strength, let them come near, then "
  "let them speak, let us come near together to judgment. What is being convened is a court, and the "
  "case concerns a conqueror already on the move, who raised up the righteous man from the east, called "
  "him to his foot, gave the nations before him. The man is not named until chapter 44, and the argument "
  "is not about him but about who is directing him, who hath wrought and done it, calling the "
  "generations from the beginning, I the LORD, the first, and with the last, I am he."),
 ("They Helped Every One His Neighbour (vv.5-7)",
  "The isles saw it, and feared, the ends of the earth were afraid, they drew near, and came. Then a "
  "scene of mutual encouragement that turns out to be a workshop, they helped every one his neighbour, "
  "and every one said to his brother, Be of good courage, so the carpenter encouraged the goldsmith, and "
  "he that smootheth with the hammer him that smote the anvil. Their answer to a political crisis is to "
  "manufacture a god faster, and the last clause is the same requirement as 40:20, he fastened it with "
  "nails, that it should not be moved."),
 ("Thou Art My Servant (vv.8-9)",
  "But thou, Israel, art my servant, Jacob whom I have chosen, the seed of Abraham my friend. This is the "
  "first use of the title servant in the second half of the book and it is applied unambiguously to the "
  "nation, which is why the servant songs beginning at 42:1 raise the question they do. And the choice "
  "is dated to the patriarch rather than to Sinai, thou whom I have taken from the ends of the earth, "
  "and called thee from the chief men thereof."),
 ("Fear Thou Not, for I Am with Thee (vv.10-13)",
  "Fear thou not, for I am with thee, be not dismayed, for I am thy God, I will strengthen thee, yea, I "
  "will help thee, yea, I will uphold thee with the right hand of my righteousness. Four promises in one "
  "verse, and the formula fear not, for I am with thee recurs through these chapters as their standing "
  "refrain. Then what happens to the opposition is stated in the perfect tense, behold, all they that "
  "were incensed against thee shall be ashamed and confounded, and the section closes by repeating the "
  "opening, for I the LORD thy God will hold thy right hand, saying unto thee, Fear not."),
 ("Fear Not, Thou Worm Jacob (vv.14-16)",
  "Fear not, thou worm Jacob, ye men of Israel, and the insult is the point: the nation is addressed at "
  "its own estimate of itself and then given a job. Behold, I will make thee a new sharp threshing "
  "instrument having teeth, thou shalt thresh the mountains, and beat them small. A worm turned into a "
  "threshing sledge with iron teeth, and set to work on mountains. And the credit is assigned in the "
  "same breath, thou shalt rejoice in the LORD, and shalt glory in the Holy One of Israel."),
 ("I Will Open Rivers in High Places (vv.17-20)",
  "When the poor and needy seek water, and there is none, and their tongue faileth for thirst, I the LORD "
  "will hear them. The provision is described as a planting programme rather than a single spring, and "
  "the species are listed, the cedar, the shittah tree, and the myrtle, and the oil tree, the fir tree, "
  "and the pine, and the box tree together. Seven trees named in the desert. And the purpose is "
  "evidential, that they may see, and know, and consider, and understand together, that the hand of the "
  "LORD hath done this."),
 ("Shew Us What Shall Happen (vv.21-24)",
  "Produce your cause, saith the LORD, bring forth your strong reasons. The court of verse 1 reconvenes "
  "and the test is set out precisely: let them shew the former things, what they be, or declare us things "
  "for to come. Prediction is proposed as the criterion, and the reasoning is given, that we may know "
  "that ye are gods. Then the verdict, and it is delivered in the language of a case collapsing, behold, "
  "ye are of nothing, and your work of nought, he that chooseth you is an abomination."),
 ("One from the North (vv.25-29)",
  "I have raised up one from the north, and he shall come, from the rising of the sun shall he call upon "
  "my name. The claim being made is about disclosure rather than about the man, and the challenge is "
  "repeated in a form nobody can meet, who hath declared from the beginning, that we may know. And the "
  "closing assessment answers the court case of the whole chapter, behold, they are all vanity, their "
  "works are nothing, their molten images are wind and confusion."),
],
"isaiah42": [
 ("Behold My Servant (vv.1-4)",
  "The first of the four servant songs. Behold my servant, whom I uphold, mine elect, in whom my soul "
  "delighteth, I have put my spirit upon him, he shall bring forth judgment to the Gentiles. What is "
  "striking is the method, which is stated entirely in negatives: he shall not cry, nor lift up, nor "
  "cause his voice to be heard in the street. And then the sentence Matthew 12 quotes in full of Jesus, "
  "a bruised reed shall he not break, and the smoking flax shall he not quench. A reed already damaged "
  "and a wick already going out are the two things a person would naturally discard, and they are named "
  "as the two things he will not. The persistence is stated in the same breath, he shall not fail nor be "
  "discouraged, till he have set judgment in the earth."),
 ("A Covenant of the People, a Light of the Gentiles (vv.5-9)",
  "Thus saith God the LORD, he that created the heavens, and stretched them out, and the credentials come "
  "before the commission. Then the appointment, I will give thee for a covenant of the people, for a "
  "light of the Gentiles. A person described as a covenant rather than as a party to one. And the work is "
  "listed as four actions, to open the blind eyes, to bring out the prisoners from the prison, and them "
  "that sit in darkness out of the prison house. The section closes on the argument of chapter 41, I am "
  "the LORD, that is my name, and my glory will I not give to another."),
 ("Sing unto the LORD a New Song (vv.10-17)",
  "Sing unto the LORD a new song, and his praise from the end of the earth, and the choir assembled is "
  "geographical, the isles, the wilderness, the villages of Kedar, the inhabitants of the rock, the tops "
  "of the mountains. Then the imagery changes completely and becomes military, the LORD shall go forth as "
  "a mighty man, he shall stir up jealousy like a man of war, he shall cry, yea, roar. Set beside the "
  "servant who does not lift up his voice in the street, the contrast is deliberate. And a striking "
  "admission follows, I have long time holden my peace, I have been still, and refrained myself, so the "
  "silence of the preceding decades is described as restraint rather than absence."),
 ("Who Is Blind but My Servant (vv.18-25)",
  "Hear, ye deaf, and look, ye blind, that ye may see. Then the question that makes this section "
  "difficult and important, who is blind, but my servant, or deaf, as my messenger that I sent. The same "
  "title given to the figure in verses 1 to 4 is here applied to a nation that cannot see or hear, which "
  "is the tension the servant songs are built on and which is not resolved until chapter 53. The rest is "
  "an account of the exile as something Israel went through without understanding it, therefore he hath "
  "poured upon him the fury of his anger, and it hath set him on fire, yet he knew not, and it burned "
  "him, yet he laid it not to heart."),
],
"isaiah43": [
 ("When Thou Passest Through the Waters (vv.1-7)",
  "But now thus saith the LORD that created thee, O Jacob, Fear not, for I have redeemed thee, I have "
  "called thee by thy name, thou art mine. Then the promise the chapter is best known for, and its form "
  "is worth noticing, when thou passest through the waters, I will be with thee, and through the rivers, "
  "they shall not overflow thee, when thou walkest through the fire, thou shalt not be burned. Not "
  "instead of the water and the fire but through them. And the price is stated in currency that would "
  "have startled the original hearers, I gave Egypt for thy ransom, Ethiopia and Seba for thee, followed "
  "by the reason, since thou wast precious in my sight."),
 ("Ye Are My Witnesses (vv.8-13)",
  "Bring forth the blind people that have eyes, and the deaf that have ears. The court of chapter 41 "
  "reconvenes and this time Israel is put in the witness box, and the qualification for the role is "
  "memory rather than insight, ye are my witnesses, saith the LORD, and my servant whom I have chosen. "
  "The nations are challenged again to produce prediction, who can declare this, and shew us former "
  "things. And the testimony required is a single sentence, that ye may know and believe me, and "
  "understand that I am he, before me there was no God formed, neither shall there be after me."),
 ("Remember Ye Not the Former Things (vv.14-21)",
  "For your sake I have sent to Babylon, and have brought down all their nobles. Then the exodus is "
  "recalled in full, which makes the next verse startling: behold, I will do a new thing, remember ye not "
  "the former things, neither consider the things of old. A book that has argued from the exodus for "
  "forty chapters now tells its readers to stop looking at it. What replaces it is described in the same "
  "terms, I will even make a way in the wilderness, and rivers in the desert, and the audience for it is "
  "animal, the beast of the field shall honour me, the dragons and the owls."),
 ("Thou Hast Not Brought Me the Small Cattle (vv.22-24)",
  "But thou hast not called upon me, O Jacob, but thou hast been weary of me, O Israel. Then a charge "
  "that is put with unusual care, I have not caused thee to serve with an offering, nor wearied thee with "
  "incense. What is complained of is not neglect of a burdensome system but weariness with a light one, "
  "and the accounting is reversed in the last verse, but thou hast made me to serve with thy sins, thou "
  "hast wearied me with thine iniquities. The one being served is God."),
 ("I, Even I, Am He That Blotteth Out (vv.25-28)",
  "I, even I, am he that blotteth out thy transgressions for mine own sake, and will not remember thy "
  "sins. The motive clause is the same as Ezekiel 36:22 and it is stated here before any request has "
  "been made. Then the court returns one last time with an invitation to argue, put me in remembrance, "
  "let us plead together, declare thou, that thou mayest be justified. And the section ends by conceding "
  "the history, thy first father hath sinned, and thy teachers have transgressed against me, so the "
  "pardon of verse 25 is not granted on a revised view of the facts."),
],
"isaiah44": [
 ("I Will Pour My Spirit upon Thy Seed (vv.1-5)",
  "Yet now hear, O Jacob my servant, and Israel, whom I have chosen. The promise is agricultural and "
  "generational, I will pour water upon him that is thirsty, and floods upon the dry ground, I will pour "
  "my spirit upon thy seed, and my blessing upon thine offspring. Then the result is described as people "
  "signing their names, one shall say, I am the LORD's, and another shall subscribe with his hand unto "
  "the LORD, and surname himself by the name of Israel. Voluntary enrolment, written down, which is a "
  "quiet answer to the register of 4:3."),
 ("I Am the First and I Am the Last (vv.6-8)",
  "Thus saith the LORD the King of Israel, and his redeemer the LORD of hosts, I am the first, and I am "
  "the last, and beside me there is no God. Then the challenge of chapter 41 stated once more and tied to "
  "Israel's own experience, have not I told thee from that time, and have declared it, ye are even my "
  "witnesses. And the closing image is domestic and unexpected in the middle of a court case, is there a "
  "God beside me, yea, there is no God, I know not any."),
 ("He Warmeth Himself, and Saith, Aha (vv.9-20)",
  "The longest and most detailed idol satire in the Bible, and the whole force of it is in following one "
  "piece of wood through a single afternoon. The smith works with tongs and hammers and gets hungry and "
  "thirsty. The carpenter measures with a line, marks it with a rule, and fits it with compasses. He "
  "cuts down a cedar and takes the wood home, and then the accounting begins: he burneth part thereof in "
  "the fire, with part thereof he eateth flesh, he roasteth roast, and is satisfied, yea, he warmeth "
  "himself, and saith, Aha, I am warm, I have seen the fire. And the residue thereof he maketh a god, and "
  "falleth down unto it, and saith, Deliver me, for thou art my god. The same log, half of it firewood "
  "and half of it a deity, and the man does not notice. The verdict is a failure of attention, they know "
  "not, neither understand, for he hath shut their eyes."),
 ("Remember These, O Jacob (vv.21-23)",
  "Remember these, O Jacob and Israel, for thou art my servant, I have formed thee, thou art my servant. "
  "The title is repeated three times in two verses, immediately after twelve verses about people who "
  "manufacture gods, and the contrast is the argument: this servant was formed rather than made. Then the "
  "pardon in a single image, I have blotted out, as a thick cloud, thy transgressions. And the response "
  "is ordered from the creation rather than from the people, sing, O ye heavens, break forth into "
  "singing, ye mountains, O forest, and every tree therein."),
 ("Cyrus Named (vv.24-28)",
  "The chapter ends by naming him. That saith of Cyrus, He is my shepherd, and shall perform all my "
  "pleasure, even saying to Jerusalem, Thou shalt be built, and to the temple, Thy foundation shall be "
  "laid. Cyrus took Babylon in 539 BC and issued the decree Ezra 1 records, and the naming of a Persian "
  "king a century and a half in advance is the single most disputed feature of the book: it is the main "
  "argument for a later author for chapters 40 to 66, and the main argument for predictive prophecy for "
  "those who hold the book unified. The chapter itself treats the naming as the point of the whole court "
  "case, since prediction is the criterion it has proposed four times, and it stacks the credentials "
  "immediately before it, that frustrateth the tokens of the liars, and maketh diviners mad."),
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
