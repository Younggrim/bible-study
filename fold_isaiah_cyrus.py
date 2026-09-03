#!/usr/bin/env python3
"""
Isaiah 45 to 48: Cyrus, the fall of Babylon, and the summons to leave. Four pages,
75 verses.

Three of the four outlines fold as they stand. isaiah47's does not: it carried a section
at verses 8 to 9 and another at verse 9, so verse 9 was described twice. The two are
merged, since the boast and the sudden loss that answers it are one movement and the
Hebrew puts them in one breath.

Chapter 45 is where the Cyrus material comes to a point, and it does something no other
Old Testament text does: it calls a foreign king the LORD's anointed, which is the word
messiah. The section says so plainly, and also says what the chapter says about it, that
Cyrus does not know whose purpose he is serving.

Usage:
    python3 fold_isaiah_cyrus.py [--check]
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
"isaiah45": [
 ("To His Anointed, to Cyrus (vv.1-7)",
  "Thus saith the LORD to his anointed, to Cyrus. The word is mashiach, messiah, and this is the only "
  "place in the Old Testament where it is applied to a foreign king. What is promised him is military and "
  "specific, I will loose the loins of kings, I will open before him the two leaved gates, and the gates "
  "shall not be shut, I will break in pieces the gates of brass, and cut in sunder the bars of iron. "
  "Babylon fell in 539 BC without a siege, the gates opened. Then the clause the chapter turns on, "
  "repeated twice, though thou hast not known me. Cyrus is described as serving a purpose he cannot "
  "identify. And the section closes on the most sweeping claim in the book, I form the light, and create "
  "darkness, I make peace, and create evil, I the LORD do all these things, which leaves no second "
  "agency to blame and has been argued over ever since."),
 ("Let the Skies Pour Down Righteousness (v.8)",
  "One verse, and it is a hymn dropped into the middle of a political oracle. Drop down, ye heavens, from "
  "above, and let the skies pour down righteousness, let the earth open, and let them bring forth "
  "salvation, and let righteousness spring up together. The imagery is rainfall and germination, so "
  "righteousness is described as weather and salvation as a crop, and both are asked for rather than "
  "announced."),
 ("Woe unto Him That Striveth with His Maker (vv.9-13)",
  "Woe unto him that striveth with his Maker, and the objection being answered is presumably to the Cyrus "
  "policy itself: a pagan king as deliverer was not what anyone had prayed for. Shall the clay say to "
  "him that fashioneth it, What makest thou. Then a second and sharper figure, woe unto him that saith to "
  "his father, What begettest thou, so the complaint is put as a child auditing its own conception. And "
  "the answer returns to the man, I have raised him up in righteousness, and will direct all his ways, he "
  "shall build my city, and he shall let go my captives, not for price nor reward. Cyrus will not be paid "
  "for it."),
 ("They Shall Come After Thee in Chains (vv.14-17)",
  "The labour of Egypt, and merchandise of Ethiopia and of the Sabeans shall come over unto thee, and "
  "they shall be thine, they shall come after thee, in chains they shall come over. Then what they say on "
  "arrival, which turns the picture from a triumph into a confession, and they shall fall down unto thee, "
  "they shall make supplication unto thee, saying, Surely God is in thee, and there is none else, there is "
  "no God. And in the middle of it a line that stands apart from everything round it, verily thou art a "
  "God that hidest thyself, O God of Israel, the Saviour."),
 ("I Have Not Spoken in Secret (vv.18-19)",
  "For thus saith the LORD that created the heavens, and the phrase used of the earth is the one from "
  "Genesis 1:2, he created it not in vain, which is the same word rendered without form. Then the claim "
  "about method, and it answers the hidden God of verse 15 from another direction, I have not spoken in "
  "secret, in a dark place of the earth, I said not unto the seed of Jacob, Seek ye me in vain. Whatever "
  "hiddenness means here, it does not mean that the instructions were withheld or that the oracles were "
  "riddles, which is a direct contrast with the way surrounding religions delivered them."),
 ("Every Knee Shall Bow (vv.20-25)",
  "Assemble yourselves and come, draw near together, ye that are escaped of the nations, and the court of "
  "chapters 41 and 43 sits for the last time. The idol-carriers are dismissed in one clause, they have no "
  "knowledge that set up the wood of their graven image. Then the invitation, which is the widest in the "
  "book, look unto me, and be ye saved, all the ends of the earth. And the oath, I have sworn by myself, "
  "that unto me every knee shall bow, every tongue shall swear. Paul quotes that verse twice, at Romans "
  "14:11 of the judgment seat and in Philippians 2:10 of Christ, which makes it one of the most heavily "
  "used sentences in the Old Testament."),
],
"isaiah46": [
 ("Bel Boweth Down (vv.1-2)",
  "Bel boweth down, Nebo stoopeth, their idols were upon the beasts, and upon the cattle. What is being "
  "described is a New Year procession in reverse: Babylon's chief gods were carried through the streets "
  "on carts as a display of power, and here they are on the carts because the city is being evacuated. "
  "They stoop, they bow down together, they could not deliver the burden, but themselves are gone into "
  "captivity. The gods are cargo."),
 ("I Have Made, and I Will Bear (vv.3-4)",
  "Hearken unto me, O house of Jacob, which are borne by me from the belly, which are carried from the "
  "womb. The contrast with the previous section is exact and it turns on one verb: Babylon's gods are "
  "carried by their worshippers, and Israel is carried by its God. Then the promise runs to the far end "
  "of a life, and even to your old age I am he, and even to hoar hairs will I carry you, I have made, and "
  "I will bear, even I will carry, and will deliver you. Four verbs of lifting in one sentence."),
 ("To Whom Will Ye Liken Me (vv.5-7)",
  "To whom will ye liken me, and make me equal, and compare me, that we may be like. The workshop is "
  "described once more and the detail chosen this time is transport and installation, they bear him upon "
  "the shoulder, they carry him, and set him in his place, and he standeth, from his place shall he not "
  "remove. A god that has to be positioned and then cannot move from where it was put. And the "
  "consequence, yea, one shall cry unto him, yet can he not answer, nor save him out of his trouble."),
 ("Declaring the End from the Beginning (vv.8-11)",
  "Remember the former things of old, for I am God, and there is none else, I am God, and there is none "
  "like me. Then the sentence that states the book's whole criterion for that claim, declaring the end "
  "from the beginning, and from ancient times the things that are not yet done, saying, My counsel shall "
  "stand, and I will do all my pleasure. And the man is named again by figure rather than by name, "
  "calling a ravenous bird from the east, the man that executeth my counsel from a far country."),
 ("My Righteousness Is Near (vv.12-13)",
  "Hearken unto me, ye stouthearted, that are far from righteousness. The address is to the obstinate "
  "rather than to the devout, which is characteristic of these chapters. And the answer to their distance "
  "is not an instruction but an announcement about proximity, I bring near my righteousness, it shall not "
  "be far off, and my salvation shall not tarry, and I will place salvation in Zion, for Israel my "
  "glory."),
],
"isaiah47": [
 ("Come Down and Sit in the Dust (vv.1-4)",
  "Come down, and sit in the dust, O virgin daughter of Babylon, sit on the ground, there is no throne. "
  "The city is addressed as a woman of rank being put to work, take the millstones, and grind meal, "
  "which was the labour of the lowest household servant. And the humiliation is public, thy nakedness "
  "shall be uncovered, thy shame shall be seen. The section closes with the name of the party doing it, "
  "as for our redeemer, the LORD of hosts is his name, the Holy One of Israel."),
 ("Thou Didst Shew Them No Mercy (vv.5-7)",
  "Sit thou silent, and get thee into darkness, O daughter of the Chaldeans, for thou shalt no more be "
  "called, The lady of kingdoms. Then the charge, and it is carefully limited: I was wroth with my "
  "people, I have polluted mine inheritance, and given them into thine hand, so the conquest itself was "
  "commissioned. What is charged is the manner, thou didst shew them no mercy, thou hast very heavily "
  "laid thy yoke upon the ancient. Mistreating the old is the specific instance named. And the "
  "self-assessment that made it possible is quoted, thou saidst, I shall be a lady for ever, so that thou "
  "didst not lay these things to thy heart."),
 ("I Am, and None Else Beside Me (vv.8-9)",
  "Thou that art given to pleasures, that dwellest carelessly, that sayest in thine heart, I am, and none "
  "else beside me. The phrase is the one God uses of himself throughout these chapters, said here by a "
  "city, which is the offence rather than the pride. Two specific fears are then named as impossible, I "
  "shall not sit as a widow, neither shall I know the loss of children. And both arrive in the same "
  "clause, and they arrive together, but these two things shall come to thee in a moment in one day, the "
  "loss of children, and widowhood. The exact two immunities she claimed, cancelled in a sentence, which "
  "is why the boast and the answer belong in one section."),
 ("Thy Wisdom and Thy Knowledge (vv.10-13)",
  "For thou hast trusted in thy wickedness, thou hast said, None seeth me, thy wisdom and thy knowledge, "
  "it hath perverted thee. Then the failure is located in the professions Babylon was famous for, and "
  "they are listed by trade: the multitude of thy sorceries, the great abundance of thine enchantments, "
  "thy enchanters, the astrologers, the stargazers, the monthly prognosticators. Babylonian celestial "
  "omen literature was the most sophisticated in the ancient world, and the sentence on it is practical, "
  "let them stand up, if they may profit, or if they may prevail. And the closing image is the same as "
  "44:16, they shall not be coals to warm at, nor fire to sit before."),
 ("None Shall Save Thee (vv.14-15)",
  "Behold, they shall be as stubble, the fire shall burn them. The experts of the previous section are "
  "the ones burning, and the last verse extends it to everyone the city had employed, thus shall they be "
  "unto thee with whom thou hast laboured, thy merchants from thy youth, they shall wander every one to "
  "his quarter. Business partners dispersing to their own countries. And the chapter ends with the "
  "sentence that answers the whole of it, none shall save thee."),
],
"isaiah48": [
 ("Which Swear by the Name of the LORD, but Not in Truth (vv.1-5)",
  "Hear ye this, O house of Jacob, which are called by the name of Israel, and are come forth out of the "
  "waters of Judah, which swear by the name of the LORD, and make mention of the God of Israel, but not "
  "in truth, nor in righteousness. The oracle opens by conceding that the religion is being practised and "
  "denying that it is being meant. Then the reason the predictions were given in advance is stated, and "
  "it is not flattering, I have even from the beginning declared it to thee, before it came to pass I "
  "shewed it thee, lest thou shouldest say, Mine idol hath done them. The prophecies were dated early to "
  "close off a specific excuse."),
 ("New Things, Created Now (vv.6-8)",
  "I have shewed thee new things from this time, even hidden things, and thou didst not know them. The "
  "phrase created now is doing precise work in the argument of these chapters: some of what is being "
  "announced is not an old prediction being repeated but a fresh one, and the reason is the same as "
  "above, lest thou shouldest say, Behold, I knew them. And the assessment of the audience is blunter "
  "than anywhere else in this half of the book, I knew that thou wouldest deal very treacherously, and "
  "thou wast called a transgressor from the womb."),
 ("For My Name's Sake Will I Defer (vv.9-11)",
  "For my name's sake will I defer mine anger, and for my praise will I refrain for thee, that I cut thee "
  "not off. The motive clause of Ezekiel 36:22 and Isaiah 43:25 stated a third time, and here with a "
  "metallurgical image attached, behold, I have refined thee, but not with silver, I have chosen thee in "
  "the furnace of affliction. The exile is described as refining that did not produce silver, which is "
  "the same disappointing assay as Jeremiah 6:29 and Ezekiel 22:20. And the reason given is proprietary, "
  "for how should my name be polluted, and I will not give my glory unto another."),
 ("I Am the First, and I Am the Last (vv.12-16)",
  "Hearken unto me, O Jacob and Israel my called, I am he, I am the first, I also am the last. Then the "
  "credentials again, mine hand also hath laid the foundation of the earth, and the summons of the man "
  "from the north, the LORD hath loved him, he will do his pleasure on Babylon. And the section closes on "
  "a claim about openness that repeats 45:19, I have not spoken in secret, from the beginning, and a "
  "final clause that is grammatically difficult and much discussed, and now the Lord GOD, and his Spirit, "
  "hath sent me."),
 ("O That Thou Hadst Hearkened (vv.17-19)",
  "I am the LORD thy God which teacheth thee to profit, which leadeth thee by the way that thou shouldest "
  "go. Then the sentence in the book that comes closest to regret, O that thou hadst hearkened to my "
  "commandments, then had thy peace been as a river, and thy righteousness as the waves of the sea. The "
  "grammar is a wish about a past that did not happen. And what was forfeited is stated in the terms of "
  "the promise to Abraham, thy seed also had been as the sand, and the offspring of thy bowels like the "
  "gravel thereof."),
 ("Go Ye Forth of Babylon (vv.20-21)",
  "Go ye forth of Babylon, flee ye from the Chaldeans, with a voice of singing declare ye, tell this, "
  "utter it even to the end of the earth. The imperatives are the practical conclusion of eight chapters "
  "of argument: the whole case about who directs history was made in order to get people to pack. And "
  "the exodus is used as the guarantee, he led them through the deserts, they thirsted not, he clave the "
  "rock also, and the waters gushed out."),
 ("No Peace unto the Wicked (v.22)",
  "One verse, and it is placed as a full stop rather than as a threat. There is no peace, saith the LORD, "
  "unto the wicked. The same sentence closes the next block of chapters at 57:21, and the book's final "
  "chapter ends on a related note, so the line functions as a structural divider in this half of Isaiah "
  "as well as a verdict."),
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
