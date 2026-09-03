#!/usr/bin/env python3
"""
Isaiah 54 to 57: the barren woman, the free invitation, and the house of prayer for all
peoples. Four pages, 61 verses.

Two of these outlines had overlaps and both are resolved by merging rather than by
splitting. isaiah56 had a section on verses 2 to 8 and another on verse 7, so verse 7 was
described twice; the house of prayer for all peoples sits inside the passage about the
foreigner and the eunuch and is treated as part of it, which is what the text does.
isaiah57 had a section on verses 17 to 19 and another on verse 19, so verse 19 was
described twice; peace to the far and the near is the conclusion of the healing promise
and belongs with it.

Usage:
    python3 fold_isaiah_covenant.py [--check]
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
"isaiah54": [
 ("Sing, O Barren (vv.1-3)",
  "Sing, O barren, thou that didst not bear, break forth into singing, and cry aloud, thou that didst not "
  "travail with child. The address is to the one person in that society with least reason to sing, and "
  "the reason given is comparative, for more are the children of the desolate than the children of the "
  "married wife. Then the practical instruction, enlarge the place of thy tent, lengthen thy cords, and "
  "strengthen thy stakes, which is what a household does when it has outgrown its accommodation. Paul "
  "quotes the opening verse in Galatians 4:27."),
 ("Thy Maker Is Thine Husband (vv.4-8)",
  "Fear not, for thou shalt not be ashamed, for thou shalt forget the shame of thy youth, and shalt not "
  "remember the reproach of thy widowhood any more. Then the relationship named, for thy Maker is thine "
  "husband, the LORD of hosts is his name. The estrangement is described in terms of duration rather than "
  "of degree, and the proportions are the point, for a small moment have I forsaken thee, but with great "
  "mercies will I gather thee. In a little wrath I hid my face from thee for a moment, but with "
  "everlasting kindness will I have mercy on thee. A moment set against everlasting."),
 ("As the Waters of Noah (vv.9-10)",
  "For this is as the waters of Noah unto me, for as I have sworn that the waters of Noah should no more "
  "go over the earth, so have I sworn that I would not be wroth with thee. The precedent chosen is the "
  "one covenant in scripture made with the whole earth and secured by a visible sign. Then the durability "
  "is tested against geology, for the mountains shall depart, and the hills be removed, but my kindness "
  "shall not depart from thee, neither shall the covenant of my peace be removed."),
 ("Thy Stones with Fair Colours (vv.11-12)",
  "O thou afflicted, and tossed with tempest, and not comforted, behold, I will lay thy stones with fair "
  "colours, and lay thy foundations with sapphires. Then the specification, and I will make thy windows of "
  "agates, and thy gates of carbuncles, and all thy borders of pleasant stones. Revelation 21 builds its "
  "new Jerusalem out of the same materials, and what is striking here is which parts of the city are "
  "named: the foundations, the windows and the gates, that is, the structure rather than the ornament."),
 ("All Thy Children Taught of the LORD (v.13)",
  "One verse, and all thy children shall be taught of the LORD, and great shall be the peace of thy "
  "children. Jesus quotes it in John 6:45 in the middle of an argument about who comes to him, and it is "
  "worth noticing what it promises: not that they will be told about God but that they will be taught by "
  "him, which is the same thing Jeremiah 31:34 says will make the teaching profession unnecessary."),
 ("No Weapon Formed Against Thee (vv.14-17)",
  "In righteousness shalt thou be established, thou shalt be far from oppression, for thou shalt not fear. "
  "Then a clause that gives away more than the popular use of this passage usually allows, behold, I have "
  "created the smith that bloweth the coals in the fire, and that bringeth forth an instrument for his "
  "work. The armourer is on the same payroll. Which is why the promise that follows is about outcome "
  "rather than about absence, no weapon that is formed against thee shall prosper. Weapons will be made "
  "and will not succeed, and the last clause names the source, this is the heritage of the servants of "
  "the LORD, and their righteousness is of me."),
],
"isaiah55": [
 ("Come, Buy Without Money (vv.1-2)",
  "Ho, every one that thirsteth, come ye to the waters, and he that hath no money, come ye, buy, and eat, "
  "yea, come, buy wine and milk without money and without price. The invitation is a market cry and the "
  "terms contradict the setting, which is the point. Then the question that gives it its edge, and it is "
  "about waste rather than about sin, wherefore do ye spend money for that which is not bread, and your "
  "labour for that which satisfieth not. And the promise, hearken diligently unto me, and let your soul "
  "delight itself in fatness."),
 ("The Sure Mercies of David (vv.3-5)",
  "Incline your ear, and come unto me, hear, and your soul shall live, and I will make an everlasting "
  "covenant with you, the sure mercies of David. What is remarkable is who the covenant is offered to: "
  "the promise made to one king is being extended to a whole discouraged community. Paul quotes the "
  "phrase in Acts 13:34. Then the role is transferred with it, behold, thou shalt call a nation that thou "
  "knowest not, and nations that knew not thee shall run unto thee, so what David was to the tribes, this "
  "people will be to the nations."),
 ("Seek Ye the LORD While He May Be Found (vv.6-7)",
  "Seek ye the LORD while he may be found, call ye upon him while he is near. The clause while he may be "
  "found implies a window, which is the one note of urgency in an otherwise open-handed chapter. Then "
  "what turning consists of, stated as two departures and two arrivals, let the wicked forsake his way, "
  "and the unrighteous man his thoughts, and let him return unto the LORD. And the ground of it is "
  "capacity rather than leniency, for he will abundantly pardon."),
 ("My Thoughts Are Not Your Thoughts (vv.8-9)",
  "For my thoughts are not your thoughts, neither are your ways my ways, saith the LORD. The verses are "
  "usually quoted to explain a disappointment, and in context they are doing the opposite: they follow "
  "immediately on he will abundantly pardon, so what is being said to be beyond human reckoning is the "
  "scale of the forgiveness. And the measure given is vertical, for as the heavens are higher than the "
  "earth, so are my ways higher than your ways."),
 ("As the Rain Cometh Down (vv.10-11)",
  "For as the rain cometh down, and the snow from heaven, and returneth not thither, but watereth the "
  "earth, and maketh it bring forth and bud. The comparison is with weather that does not go back up "
  "unused. So shall my word be that goeth forth out of my mouth, it shall not return unto me void, but it "
  "shall accomplish that which I please. The claim is about reliability of effect rather than of "
  "prediction, and it is the answer to forty chapters of preaching that appeared to achieve nothing."),
 ("Ye Shall Go Out with Joy (vv.12-13)",
  "For ye shall go out with joy, and be led forth with peace, the mountains and the hills shall break "
  "forth before you into singing, and all the trees of the field shall clap their hands. Then the change "
  "described botanically, instead of the thorn shall come up the fir tree, and instead of the brier shall "
  "come up the myrtle tree. The thorns and briers are the standing image of ruin from 5:6 and 7:23, and "
  "what replaces them here is not merely useful but ornamental. And the last clause is about permanence, "
  "and it shall be to the LORD for a name, for an everlasting sign that shall not be cut off."),
],
"isaiah56": [
 ("Keep Ye Judgment (v.1)",
  "Thus saith the LORD, Keep ye judgment, and do justice, for my salvation is near to come, and my "
  "righteousness to be revealed. One verse, and it does the work of a hinge. What is asked is conduct, "
  "and the reason given is timing rather than obligation, which sets up the two groups the rest of the "
  "chapter is about: people who were told they did not qualify, and people who assumed they did."),
 ("The Eunuch and the Stranger (vv.2-8)",
  "The passage names two categories that the law had explicitly excluded and admits both. Deuteronomy 23 "
  "barred the eunuch from the congregation and restricted the foreigner, and their objections are quoted "
  "here in their own words, let not the eunuch say, Behold, I am a dry tree, and neither let the son of "
  "the stranger say, The LORD hath utterly separated me from his people. What is offered the eunuch is "
  "exactly what he cannot have any other way, I will give them an everlasting name, that shall not be cut "
  "off, better than of sons and of daughters. And the foreigners are given the temple itself, mine house "
  "shall be called an house of prayer for all people, which is the clause Jesus quotes when he clears the "
  "courts in Mark 11, in a temple that had by then built a wall to keep foreigners out of them. The "
  "qualification in both cases is the same and it is not descent, every one that keepeth the sabbath from "
  "polluting it, and taketh hold of my covenant."),
 ("The Watchmen Are Blind (vv.9-12)",
  "All ye beasts of the field, come to devour, and the animals are being invited in because nobody is "
  "guarding the flock. Then the leadership described by what it cannot do, his watchmen are blind, they "
  "are all dumb dogs, they cannot bark, sleeping, lying down, loving to slumber. A guard dog that will "
  "not bark is the most economical picture of useless authority in the prophets. And the last verse "
  "quotes them at table, come ye, say they, I will fetch wine, and we will fill ourselves with strong "
  "drink, and tomorrow shall be as this day. Set against the previous section the contrast is deliberate: "
  "the outsiders are keeping the sabbath and the appointed watchmen are asleep."),
],
"isaiah57": [
 ("The Righteous Perisheth (vv.1-2)",
  "The righteous perisheth, and no man layeth it to heart, and merciful men are taken away, none "
  "considering that the righteous is taken away from the evil to come. Two verses on a death nobody "
  "notices, and the interpretation offered is unusual: the early death is described as a removal from "
  "something worse rather than as a loss. And the rest given is domestic, he shall enter into peace, they "
  "shall rest in their beds, each one walking in his uprightness."),
 ("Under Every Green Tree (vv.3-10)",
  "But draw near hither, ye sons of the sorceress, the seed of the adulterer and the whore. The practices "
  "are then named specifically and they are the worst list in the second half of the book: enflaming "
  "yourselves with idols under every green tree, slaying the children in the valleys under the clifts of "
  "the rocks, and offerings poured to the smooth stones of the stream. Then the diplomacy described in "
  "the same terms as the idolatry, thou wentest to the king with ointment, and didst increase thy "
  "perfumes, and sentest thy messengers far off. And the closing observation is about persistence, thou "
  "art wearied in the greatness of thy way, yet saidst thou not, There is no hope."),
 ("Of Whom Hast Thou Been Afraid (vv.11-13)",
  "And of whom hast thou been afraid or feared, that thou hast lied, and hast not remembered me. The "
  "diagnosis is fear rather than desire, which is the same account 8:12 gave of the conspiracy panic. "
  "Then a clause that explains a great deal of the book, have not I held my peace even of old, and thou "
  "fearest me not, so the silence had been read as absence. And the challenge, when thou criest, let them "
  "deliver thee, but he that putteth his trust in me shall possess the land."),
 ("The High and Lofty One (vv.14-16)",
  "Cast ye up, cast ye up, prepare the way, take up the stumblingblock out of the way of my people. Then "
  "the sentence the chapter is best known for, and its two halves are deliberately hard to hold together, "
  "thus saith the high and lofty One that inhabiteth eternity, whose name is Holy, I dwell in the high "
  "and holy place, with him also that is of a contrite and humble spirit. Two addresses, both current. "
  "And the reason given for not pressing the judgment further is physiological, for I will not contend "
  "for ever, neither will I be always wroth, for the spirit should fail before me, and the souls which I "
  "have made."),
 ("Peace to the Far and to the Near (vv.17-19)",
  "For the iniquity of his covetousness was I wroth, and smote him, I hid me, and he was wroth, and went "
  "on frowardly. Then the turn, and it is unprompted, I have seen his ways, and will heal him, I will "
  "lead him also, and restore comforts unto him and to his mourners. What is created is speech, I create "
  "the fruit of the lips, and the content of it is one word said twice, peace, peace, to him that is far "
  "off, and to him that is near. Paul takes up the far and the near in Ephesians 2:17 of Jew and Gentile. "
  "The doubling is the same emphatic form as 26:3."),
 ("No Peace to the Wicked (vv.20-21)",
  "But the wicked are like the troubled sea, when it cannot rest, whose waters cast up mire and dirt. The "
  "image is of a condition rather than a punishment: not a sea being stirred but a sea that cannot "
  "settle. And the closing verse repeats 48:22 word for word, there is no peace, saith my God, to the "
  "wicked, which places the same sentence at the end of two consecutive blocks of nine chapters and makes "
  "it a structural marker in this half of the book."),
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
