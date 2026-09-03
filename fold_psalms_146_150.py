#!/usr/bin/env python3
"""
Psalms 146 to 150. Five pages, 59 verses. All five outlines are gapless and are folded. This is
the last of the Psalms scripts and completes the fold of all 150 pages.

These are the final five hallelujah psalms, each opening and closing with praise ye the LORD.
Read as a set they widen at every step, from one soul in 146:1 to everything that breathes in
150:6, and the pages note that movement where it shows.

psalms149:6 puts a two-edged sword in the hand of the congregation, and the verse has a bad
history: it was preached at crusades and at the sack of Münster. The section says so, and says
what the psalm itself limits the sword to, the judgment written, which is a sentence already
passed rather than a licence to pass one. Leaving that history unmentioned on this page would be
the easier choice and the wrong one.

psalms150 ends the psalter with thirteen imperatives and no petition. A book that opened on two
ways and spent a hundred and fifty poems complaining, pleading, confessing and cursing closes
without asking for anything, and the section names that rather than treating the last psalm as
decoration.

Usage:
    python3 fold_psalms_146_150.py [--check]
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
"psalms146": [
 ("While I Live Will I Praise the LORD (vv.1-2)",
  "Praise ye the LORD. Praise the LORD, O my soul. The first of the five psalms that close the psalter, each "
  "of which begins and ends with hallelujah. The opening instruction is to itself, as in Psalms 103 and 104, "
  "and the term set on it is a lifetime, while I live will I praise the LORD: I will sing praises unto my God "
  "while I have any being."),
 ("Put Not Your Trust in Princes (vv.3-4)",
  "Put not your trust in princes, nor in the son of man, in whom there is no help. The warning is not that "
  "rulers are wicked but that they are temporary, which the next verse spells out without any malice, his "
  "breath goeth forth, he returneth to his earth; in that very day his thoughts perish. What dies with a man "
  "is his planning, and that is the reason given for not building on him."),
 ("Happy Is He That Hath the God of Jacob for His Help (v.5)",
  "Happy is he that hath the God of Jacob for his help, whose hope is in the LORD his God. The alternative to "
  "the princes, and the title chosen is deliberate: the God of Jacob is the God of a man who spent his life "
  "being outmanoeuvred and was kept anyway."),
 ("Which Keepeth Truth for Ever (v.6)",
  "Which made heaven, and earth, the sea, and all that therein is: which keepeth truth for ever. The "
  "credential is the maker's, as in the Songs of Ascents, and the last clause is the answer to the perishing "
  "thoughts of verse 4: this one keeps his word past his own lifetime, having none to end."),
 ("The LORD Looseth the Prisoners (vv.7-9)",
  "Which executeth judgment for the oppressed: which giveth food to the hungry. The LORD looseth the "
  "prisoners. Nine actions in three verses and every one of them concerns somebody with no standing, the "
  "hungry, the imprisoned, the blind, the bowed down, the stranger, the fatherless and the widow. It is the "
  "same list Jesus reads out of Isaiah at Nazareth in Luke 4 and sends back to John in Matthew 11, and the "
  "psalm treats it as a description of what God does routinely rather than a programme for the future. But the "
  "way of the wicked he turneth upside down."),
 ("The LORD Shall Reign for Ever (v.10)",
  "The LORD shall reign for ever, even thy God, O Zion, unto all generations. Praise ye the LORD. The last "
  "verse answers the princes of verse 3 with the one thing they lacked, and it addresses the city rather than "
  "the singer, so a psalm that began with one soul ends with a nation."),
],
"psalms147": [
 ("He Telleth the Number of the Stars (vv.1-6)",
  "Praise ye the LORD: for it is good to sing praises unto our God; for it is pleasant; and praise is comely. "
  "Three reasons, and none of them is duty. The occasion is a rebuilding, the LORD doth build up Jerusalem: he "
  "gathereth together the outcasts of Israel, which places the psalm after the return from exile. Then the "
  "juxtaposition the psalm is remembered for, he healeth the broken in heart, and bindeth up their wounds. He "
  "telleth the number of the stars; he calleth them all by their names. The two verses are set side by side "
  "without a joint, and the argument is that the same attention does both."),
 ("He Delighteth Not in the Strength of the Horse (vv.7-11)",
  "Sing unto the LORD with thanksgiving; sing praise upon the harp unto our God. The provision described is "
  "weather and fodder, who prepareth rain for the earth, who maketh grass to grow upon the mountains, and it "
  "reaches creatures nobody farms, he giveth to the beast his food, and to the young ravens which cry. Then "
  "the psalm says what does not impress God, and both examples are military assets, he delighteth not in the "
  "strength of the horse: he taketh not pleasure in the legs of a man. Horses meant cavalry and legs meant "
  "infantry. The LORD taketh pleasure in them that fear him, in those that hope in his mercy."),
 ("He Maketh Peace in Thy Borders (vv.12-14)",
  "Praise the LORD, O Jerusalem; praise thy God, O Zion. The city is addressed directly and the blessings "
  "listed are the ones a recently rebuilt city notices, he hath strengthened the bars of thy gates; he hath "
  "blessed thy children within thee. He maketh peace in thy borders, and filleth thee with the finest of the "
  "wheat. Gates, children, borders and bread, in that order, which is the order of a place that has been "
  "unsafe."),
 ("He Giveth Snow like Wool (vv.15-18)",
  "He sendeth forth his commandment upon earth: his word runneth very swiftly. The psalter's only winter, and "
  "it is described in kitchen and household terms, he giveth snow like wool: he scattereth the hoar frost like "
  "ashes. He casteth forth his ice like morsels: who can stand before his cold? The thaw is worked by the same "
  "means as the freeze, he sendeth out his word, and melteth them, so the word of verse 15 turns out to be "
  "what the weather is."),
 ("He Hath Not Dealt So with Any Nation (vv.19-20)",
  "He sheweth his word unto Jacob, his statutes and his judgments unto Israel. The word that made the snow and "
  "melted it is now the word given as law, and the psalm makes that pun the point of its ending. He hath not "
  "dealt so with any nation: and as for his judgments, they have not known them. It is a claim of privilege "
  "rather than of merit, and Paul makes the same observation in Romans 3:2 before arguing that it settles less "
  "than it appears to. Praise ye the LORD."),
],
"psalms148": [
 ("Praise Ye the LORD from the Heavens (vv.1-6)",
  "Praise ye the LORD. Praise ye the LORD from the heavens: praise him in the heights. The psalm works through "
  "creation issuing orders, and it starts at the top with the angels, then the sun and moon and stars, then "
  "the heavens of heavens, and ye waters that be above the heavens. The reason given is manufacture, for he "
  "commanded, and they were created, and the sun and moon are told to praise rather than being worshipped, "
  "which is the ordinary Hebrew treatment of the sky. He hath made a decree which shall not pass. The Greek "
  "additions to Daniel 3 turn this psalm into the canticle called the Benedicite, sung in the Western church "
  "at morning prayer for centuries."),
 ("Praise the LORD from the Earth (vv.7-12)",
  "Praise the LORD from the earth, ye dragons, and all deeps. Dragons renders tanninim, the great sea "
  "creatures, and they head the list because the psalm is working downward from the sky and they live at the "
  "bottom. Then the weather, fire, and hail; snow, and vapours; stormy wind fulfilling his word, and after it "
  "the land, mountains, and all hills; fruitful trees, and all cedars. Animals come next and people last, and "
  "when people arrive they are sorted by rank and then by age, kings of the earth, and all people; princes, "
  "and all judges, both young men, and maidens; old men, and children. Humanity is one item in a long "
  "inventory, arriving after the cattle."),
 ("His Name Alone Is Excellent (vv.13-14)",
  "Let them praise the name of the LORD: for his name alone is excellent; his glory is above the earth and "
  "heaven. The two halves of the psalm are gathered into one command, and the reason given is that the name is "
  "the only thing in the inventory that is not made. He also exalteth the horn of his people, the praise of "
  "all his saints; even of the children of Israel, a people near unto him. After sun, sea-monsters and kings, "
  "the psalm ends on nearness, which is the one thing none of the rest of the list was said to have."),
],
"psalms149": [
 ("Sing unto the LORD a New Song (vv.1-3)",
  "Praise ye the LORD. Sing unto the LORD a new song, and his praise in the congregation of saints. The new "
  "song asks for something composed rather than inherited, which is a strange request in a book of a hundred "
  "and fifty existing songs and is made several times in it. Let Israel rejoice in him that made him, where "
  "the making is of the nation rather than of the world. The praise is physical, let them praise his name in "
  "the dance: let them sing praises unto him with the timbrel and harp."),
 ("He Will Beautify the Meek with Salvation (v.4)",
  "For the LORD taketh pleasure in his people: he will beautify the meek with salvation. Pleasure taken in "
  "people is the ground offered for the dancing, and the second clause reverses the ordinary direction of "
  "adornment: the salvation is what makes them worth looking at, rather than their beauty attracting it."),
 ("A Twoedged Sword in Their Hand (vv.5-6)",
  "Let the saints be joyful in glory: let them sing aloud upon their beds. Singing in bed is the psalter's "
  "quietest image of confidence, and it is followed immediately by its most dangerous line. Let the high "
  "praises of God be in their mouth, and a twoedged sword in their hand. The verse has been used to sanction "
  "religious violence more than once; it was preached at the crusades and by the men who took Münster in 1534, "
  "and any honest page on this psalm has to say so. What the psalm itself does with the sword is set out in "
  "the next three verses, and it is narrower than those uses assumed."),
 ("To Execute upon Them the Judgment Written (vv.7-9)",
  "To execute vengeance upon the heathen, and punishments upon the people; to bind their kings with chains, "
  "and their nobles with fetters of iron. The targets are kings and nobles rather than populations, which is "
  "the first limit. The second is in the last line and it is the important one, to execute upon them the "
  "judgment written, so the congregation carries out a sentence already passed and recorded, not one it "
  "decides. Nothing in the psalm authorises anybody to write a new judgment. This honour have all his saints. "
  "Read within the Old Testament the verses look back to the conquest and forward to the day the prophets "
  "promise; read forward into the New Testament, the weapon the church is given in Ephesians 6:17 and Hebrews "
  "4:12 is also a two-edged sword and it is the word of God. Praise ye the LORD."),
],
"psalms150": [
 ("Praise God in His Sanctuary (v.1)",
  "Praise ye the LORD. Praise God in his sanctuary: praise him in the firmament of his power. Six verses close "
  "the psalter and they contain thirteen imperatives and nothing else. The first verse settles where, and it "
  "names the two ends of the range, the temple on the ground and the vault of the sky, so the same act is "
  "asked for in the smallest room and the largest."),
 ("According to His Excellent Greatness (v.2)",
  "Praise him for his mighty acts: praise him according to his excellent greatness. The two reasons cover what "
  "God has done and what God is, which between them is everything the previous hundred and forty-nine psalms "
  "have been about. According to sets no achievable measure and the psalm knows it."),
 ("Praise Him upon the Loud Cymbals (vv.3-5)",
  "Praise him with the sound of the trumpet: praise him with the psaltery and harp. The orchestra is listed by "
  "family, wind, strings, percussion, and it takes in the dance as well, praise him with the timbrel and "
  "dance. Organs renders ugab, a pipe of some kind, and has nothing to do with the instrument the word now "
  "means. The list ends by getting louder twice over, praise him upon the loud cymbals: praise him upon the "
  "high sounding cymbals, and the psalter's last instruction about volume is to increase it."),
 ("Let Every Thing That Hath Breath Praise the LORD (v.6)",
  "Let every thing that hath breath praise the LORD. Praise ye the LORD. The qualification for the choir is "
  "breathing, which is the lowest bar the psalter could have set and the widest membership it could have "
  "named. And there the book ends. A collection that opened on the two ways in Psalm 1 and spent its length "
  "complaining, pleading, confessing, arguing and cursing closes with no petition in it at all: nothing is "
  "asked for in these six verses. Psalm 88 is still in the book and never turns, Psalm 137 is still in the "
  "book and ends where it ends, and the psalter does not withdraw either of them. What it does is put this "
  "last, which is a claim about where all of it was going rather than a denial of where it has been."),
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
