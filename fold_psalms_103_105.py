#!/usr/bin/env python3
"""
Psalms 103 to 105. Three pages, 102 verses. All three outlines are gapless and are folded.
Three pages rather than six because these psalms are long and the sections run to the length
the material needs.

psalms104 has a genuine comparative question attached to it. The Egyptian Hymn to the Aten,
from the reign of Akhenaten, moves through the same subjects in nearly the same order: light
as clothing, night and the beasts that come out in it, the day and man going to work, the sea
and the ships. The section states the parallel and states what it does not settle, since a
shared way of praising the sun-lit world is not by itself evidence of borrowing in either
direction.

psalms105 rehearses Israel's history and stops at the entry to the land, telling it as a
record of God keeping a promise and saying nothing about Israel's failures. Psalm 106 tells the
same history as a record of rebellion. The pair is deliberate and neither half is the whole
account; the section on 105 says so rather than leaving a reader with one side.

Usage:
    python3 fold_psalms_103_105.py [--check]
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
"psalms103": [
 ("Bless the LORD, O My Soul (vv.1-2)",
  "Bless the LORD, O my soul: and all that is within me, bless his holy name. The psalm opens by giving an "
  "order to itself, which is a device worth noticing: the singer does not report that he feels grateful but "
  "instructs the part of him that ought to be. And the second verse names the enemy of praise as memory "
  "rather than doubt, forget not all his benefits."),
 ("Who Forgiveth All Thine Iniquities (vv.3-5)",
  "Who forgiveth all thine iniquities; who healeth all thy diseases. Five participles in three verses, each "
  "one a benefit, and forgiveness is put first with healing beside it, which is the pairing Jesus makes at "
  "the paralytic's mat in Mark 2. Then rescue and honour, who redeemeth thy life from destruction, who "
  "crowneth thee with lovingkindness. The last is renewal, so that thy youth is renewed like the eagle's, "
  "an image of moulting rather than of the legend about the bird burning and rising."),
 ("The LORD Is Merciful and Gracious (vv.6-10)",
  "The LORD executeth righteousness and judgment for all that are oppressed. The psalm turns from what God "
  "has done for one man to what he does as a matter of practice, and it grounds the claim in a text rather "
  "than in feeling, he made known his ways unto Moses. The words that follow are quoted from Exodus 34:6, "
  "the LORD is merciful and gracious, slow to anger, and plenteous in mercy, which is the sentence the Old "
  "Testament repeats more often than any other about God's character. Then the limit set on anger, he will "
  "not always chide, and the plainest denial of tit for tat in the psalter, he hath not dealt with us after "
  "our sins."),
 ("As Far as the East Is from the West (vv.11-14)",
  "For as the heaven is high above the earth, so great is his mercy toward them that fear him. Two "
  "measurements, and both are chosen because they cannot be completed: height has no ceiling and east and "
  "west never meet, as far as the east is from the west, so far hath he removed our transgressions from us. "
  "The psalm then drops from cosmology to the household, like as a father pitieth his children, and gives "
  "the reason for the pity in a line that refuses to flatter, for he knoweth our frame; he remembereth that "
  "we are dust. Being known is here a mercy rather than an exposure."),
 ("His Days Are as Grass (vv.15-18)",
  "As for man, his days are as grass: as a flower of the field, so he flourisheth. The wind passeth over it, "
  "and it is gone; and the place thereof shall know it no more. That last clause is the hardest sentence in "
  "the psalm, since it denies even the consolation of being missed by the ground. What is set against it is "
  "not human durability but God's, but the mercy of the LORD is from everlasting to everlasting upon them "
  "that fear him. And the psalm attaches a condition without softening it, to such as keep his covenant, "
  "and to those that remember his commandments to do them."),
 ("Bless the LORD, All His Works (vv.19-22)",
  "The LORD hath prepared his throne in the heavens; and his kingdom ruleth over all. Having begun with one "
  "soul, the psalm ends by conscripting everything else, the angels that excel in strength, all ye his "
  "hosts, all his works in all places of his dominion. Then it closes where it opened, bless the LORD, O my "
  "soul, so the widest possible choir is bracketed by a single man talking to himself."),
],
"psalms104": [
 ("Clothed with Honour and Majesty (vv.1-4)",
  "Bless the LORD, O my soul. O LORD my God, thou art very great; thou art clothed with honour and majesty. "
  "The psalm follows Psalm 103's opening line and then turns outward to creation instead of inward to "
  "benefits. Light is the garment, who coverest thyself with light as with a garment, and the sky is fabric, "
  "who stretchest out the heavens like a curtain. The weather is transport, who maketh the clouds his "
  "chariot, who walketh upon the wings of the wind. Verse 4, who maketh his angels spirits, his ministers a "
  "flaming fire, is quoted in Hebrews 1:7 to argue that angels are servants and the Son is not; the Hebrew "
  "can equally be read as making winds his messengers, and the epistle's argument depends on the reading it "
  "took."),
 ("Thou Hast Set a Bound That They May Not Pass (vv.5-9)",
  "Who laid the foundations of the earth, that it should not be removed for ever. The order of Genesis 1 is "
  "visible here, and so is the older poetry of the sea, since the waters flee at a rebuke, at thy rebuke "
  "they fled; at the voice of thy thunder they hasted away. But the psalm gives the sea no personality and "
  "no fight. What it gets instead is a boundary, thou hast set a bound that they may not pass over, that "
  "they turn not again to cover the earth, which reads as a standing arrangement rather than a victory."),
 ("He Sendeth the Springs into the Valleys (vv.10-18)",
  "He sendeth the springs into the valleys, which run among the hills. Nine verses of provision, and the "
  "recipients are named in an order that puts animals before people, every beast of the field, the wild "
  "asses, the fowls of the heaven which sing among the branches. Man arrives as one item on a list, and "
  "what he gets is farmed rather than gathered, herb for the service of man, that he may bring forth food "
  "out of the earth. Then three products named for what they do to a person, and wine that maketh glad the "
  "heart of man, and oil to make his face to shine, and bread which strengtheneth man's heart. The section "
  "ends with creatures whose habitats are useless to anybody, the stork in the fir trees, the wild goats on "
  "the high hills, and the rocks for the conies, which is the psalm declining to make the world about human "
  "benefit."),
 ("The Sun Knoweth His Going Down (vv.19-23)",
  "He appointed the moon for seasons: the sun knoweth his going down. In the surrounding religions these two "
  "were gods; here they keep a timetable. Night is described from the animals' side, wherein all the beasts "
  "of the forest do creep forth, and the young lions roar after their prey, and seek their meat from God, "
  "which puts predation inside providence without comment. Then day, and man appears in a single line at the "
  "end of the shift change, man goeth forth unto his work and to his labour until the evening."),
 ("O LORD, How Manifold Are Thy Works (vv.24-26)",
  "O LORD, how manifold are thy works! in wisdom hast thou made them all: the earth is full of thy riches. "
  "The psalm stops describing and exclaims, and the ground it gives is number and variety rather than "
  "usefulness. The sea it feared in verse 9 is now a place worth looking at, wherein are things creeping "
  "innumerable. And leviathan, which is a monster in Job 41 and in Psalm 74, is here a pet, there is that "
  "leviathan, whom thou hast made to play therein."),
 ("Thou Openest Thine Hand (vv.27-30)",
  "These wait all upon thee; that thou mayest give them their meat in due season. Four verses on dependence, "
  "and they are the most unsentimental in the psalm, because the same hand that fills also withdraws, thou "
  "hidest thy face, they are troubled: thou takest away their breath, they die, and return to their dust. "
  "Death is inside the providence rather than outside it. Then the line the church reads at Pentecost, thou "
  "sendest forth thy spirit, they are created: and thou renewest the face of the earth, where the Hebrew "
  "word is breath and spirit at once."),
 ("I Will Sing unto the LORD as Long as I Live (vv.31-35)",
  "The glory of the LORD shall endure for ever: the LORD shall rejoice in his works. Delight is attributed "
  "to God as well as to the singer, which is unusual and is the psalm's warmest claim. The response offered "
  "is lifelong and interior, I will sing unto the LORD as long as I live, my meditation of him shall be "
  "sweet. Then a jarring last request, let the sinners be consumed out of the earth, and let the wicked be "
  "no more. It sits badly after thirty-four verses of open-handed provision, and the psalm makes no attempt "
  "to reconcile them; what it appears to mean is that the only thing spoiling the world described is the "
  "one creature acting against it. The book's first hallelujah closes the psalm, praise ye the LORD."),
],
"psalms105": [
 ("Make Known His Deeds Among the People (vv.1-6)",
  "O give thanks unto the LORD; call upon his name: make known his deeds among the people. These verses "
  "stand almost word for word in 1 Chronicles 16:8-22, sung when David brought the ark to Jerusalem, which "
  "is the ground for associating the psalm with him though it carries no superscription. The instruction is "
  "to talk, talk ye of all his wondrous works, and then to remember, remember his marvellous works that he "
  "hath done. The audience is named by descent, O ye seed of Abraham his servant, which sets up the whole "
  "psalm as a family record."),
 ("He Hath Remembered His Covenant for Ever (vv.7-11)",
  "He hath remembered his covenant for ever, the word which he commanded to a thousand generations. The "
  "psalm's thesis is here and it is about God's memory, not Israel's. The covenant is traced through three "
  "generations, made with Abraham, sworn to Isaac, confirmed unto Jacob, and its content is reduced to one "
  "clause, unto thee will I give the land of Canaan, the lot of your inheritance. Everything that follows is "
  "the working out of that sentence."),
 ("Touch Not Mine Anointed (vv.12-15)",
  "When they were but a few men in number; yea, very few, and strangers in it. The patriarchs are described "
  "by their weakness, which is the psalm's way of making the protection remarkable. He suffered no man to do "
  "them wrong: yea, he reproved kings for their sakes. The quoted warning, touch not mine anointed, and do "
  "my prophets no harm, applies both titles to Abraham, Isaac and Jacob, none of whom was a king or held "
  "prophetic office in the later sense; the psalm is using the words for men God had claimed."),
 ("He Sent a Man Before Them, Even Joseph (vv.16-22)",
  "Moreover he called for a famine upon the land: he brake the whole staff of bread. The famine is God's "
  "doing, stated without hedging, and so is what follows, he sent a man before them, even Joseph, who was "
  "sold for a servant. The psalm passes over the brothers entirely and reads the sale as a sending. Whose "
  "feet they hurt with fetters: he was laid in iron. Then the release, and the reason given is the word "
  "rather than the dream, until the time that his word came: the word of the LORD tried him. Senators in "
  "verse 22 renders a word for elders; KJV reached for a Roman title."),
 ("Wonders in the Land of Ham (vv.23-36)",
  "Israel also came into Egypt; and Jacob sojourned in the land of Ham. Fourteen verses on Egypt, and the "
  "hardest line is the one about the Egyptians' change of mind, he turned their heart to hate his people, "
  "which credits God with the hostility as directly as verse 16 credited him with the famine. The psalm "
  "states this and does not explain it, and it is the same difficulty Exodus raises when it hardens "
  "Pharaoh's heart. The plagues are then listed out of the order Exodus gives them, darkness first and the "
  "death of the firstborn last, with hail, locusts and flies between; the psalm is arranging for effect "
  "rather than reporting a sequence, and the count is seven rather than ten."),
 ("He Brought Them Forth with Silver and Gold (vv.37-41)",
  "He brought them forth also with silver and gold: and there was not one feeble person among their tribes. "
  "The departure is described as a success without a casualty, and Egypt's relief is noted with something "
  "close to humour, Egypt was glad when they departed. The wilderness provision is given in three lines and "
  "no complaint appears in any of them, he spread a cloud for a covering, the people asked, and he brought "
  "quails, he opened the rock, and the waters gushed out. Anyone who knows Exodus and Numbers will notice "
  "what has been left out; Psalm 106 supplies it."),
 ("That They Might Observe His Statutes (vv.42-45)",
  "For he remembered his holy promise, and Abraham his servant. The psalm returns to its thesis and closes "
  "the circle, and the entry into the land is stated as a handover, he gave them the lands of the heathen. "
  "The last verse gives the purpose of the whole history, that they might observe his statutes, and keep his "
  "laws, so the gift was for obedience rather than for comfort. Praise ye the LORD. Read alone this psalm is "
  "a record of unbroken faithfulness on one side only, and that is deliberate: the psalter puts the other "
  "side immediately after it."),
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
