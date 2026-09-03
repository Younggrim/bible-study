#!/usr/bin/env python3
"""
Isaiah 58 to 62: true fasting, the anointing, and the renaming of Zion. Five pages,
70 verses. All five outlines are gapless and are folded.

Chapter 58 is the most concrete definition of religious practice in the book, and it works
by rejecting one activity and substituting a list. Chapter 61 opens with the passage Jesus
reads in the synagogue at Nazareth in Luke 4, and the section notes where he stopped
reading, which is mid-verse.

Usage:
    python3 fold_isaiah_zion.py [--check]
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
"isaiah58": [
 ("Cry Aloud, Spare Not (v.1)",
  "Cry aloud, spare not, lift up thy voice like a trumpet, and shew my people their transgression, and "
  "the house of Jacob their sins. One verse of instruction, and the striking thing about it is the "
  "audience: my people and the house of Jacob, a community that is fasting and enquiring and keeping a "
  "calendar. The chapter is addressed to religious people in good standing."),
 ("Wherefore Have We Fasted (vv.2-3a)",
  "Yet they seek me daily, and delight to know my ways, they ask of me the ordinances of justice, they "
  "take delight in approaching to God. The description is complimentary and it is meant to be, which is "
  "what makes the complaint that follows worth answering. Then the grievance is quoted in their own "
  "words, wherefore have we fasted, say they, and thou seest not, wherefore have we afflicted our soul, "
  "and thou takest no knowledge. They have done the work and want to know why nothing happened."),
 ("Ye Fast for Strife (vv.3b-5)",
  "Behold, in the day of your fast ye find pleasure, and exact all your labours. The answer identifies "
  "what was happening on the fast days, and it is industrial relations: work extracted from employees "
  "while the employer fasted. Behold, ye fast for strife and debate, and to smite with the fist of "
  "wickedness. Then the theatre of it is described and dismissed, is it such a fast that I have chosen, a "
  "day for a man to afflict his soul, is it to bow down his head as a bulrush. The bulrush is exact: a "
  "reed bends convincingly and springs straight back."),
 ("Is Not This the Fast (vv.6-7)",
  "Is not this the fast that I have chosen, to loose the bands of wickedness, to undo the heavy burdens, "
  "and to let the oppressed go free, and that ye break every yoke. Four clauses about releasing people, "
  "and then four about supplying them, is it not to deal thy bread to the hungry, and that thou bring the "
  "poor that are cast out to thy house, when thou seest the naked, that thou cover him. And the last "
  "clause closes the escape route, and that thou hide not thyself from thine own flesh, that is, from "
  "your own relatives, which is where such duty is most easily avoided."),
 ("Then Shall Thy Light Break Forth (vv.8-12)",
  "Then shall thy light break forth as the morning, and thine health shall spring forth speedily. The "
  "promises are conditional on the previous section and they are stated in the same order: light, "
  "healing, an answer to prayer, and guidance. Then the condition is restated in the middle, if thou draw "
  "out thy soul to the hungry, and satisfy the afflicted soul. And the images that follow are all about "
  "water in a dry place, thou shalt be like a watered garden, and like a spring of water, whose waters "
  "fail not. The last verse gives a title that would have meant a great deal to a community living in "
  "rubble, thou shalt be called, The repairer of the breach, the restorer of paths to dwell in."),
 ("If Thou Turn Away Thy Foot (vv.13-14)",
  "If thou turn away thy foot from the sabbath, from doing thy pleasure on my holy day, and call the "
  "sabbath a delight. The word delight is the operative one, since the chapter has just spent five verses "
  "on a fast that was misery for the fasters and worse for their workers. Sabbath is being offered as the "
  "opposite of that, not as a further austerity. And the promise attached is inheritance, then shalt thou "
  "delight thyself in the LORD, and I will cause thee to ride upon the high places of the earth, and feed "
  "thee with the heritage of Jacob thy father."),
],
"isaiah59": [
 ("Your Iniquities Have Separated (vv.1-2)",
  "Behold, the LORD's hand is not shortened, that it cannot save, neither his ear heavy, that it cannot "
  "hear. Both clauses answer complaints made earlier in the book, at 50:2 and 58:3, and they answer them "
  "by denying the premise rather than by explaining the delay. Then the cause is located, but your "
  "iniquities have separated between you and your God, and your sins have hid his face from you, that he "
  "will not hear. The hiddenness of 45:15 and 57:17 is here given an address."),
 ("Their Webs Shall Not Become Garments (vv.3-8)",
  "For your hands are defiled with blood, and your fingers with iniquity. The catalogue that follows is "
  "the longest in the second half of the book and it is organised by body part, hands, fingers, lips, "
  "tongue, feet. The legal system is described as unusable, none calleth for justice, nor any pleadeth "
  "for truth. Then two images from natural history, they hatch cockatrice eggs, and weave the spider's "
  "web, with the point of each spelled out: the eggs produce something that bites, and their webs shall "
  "not become garments, that is, all that effort and nothing you could wear. Paul quotes verses 7 and 8 in "
  "Romans 3."),
 ("We Grope for the Wall (vv.9-15a)",
  "Therefore is judgment far from us, neither doth justice overtake us, we wait for light, but behold "
  "obscurity. This is a confession in the first person plural and it does not plead extenuation. The "
  "images are of impaired movement, we grope for the wall like the blind, and we grope as if we had no "
  "eyes, we stumble at noonday as in the night. Then the sounds, we roar all like bears, and mourn sore "
  "like doves. And the summary is legal, judgment is turned away backward, and justice standeth afar off, "
  "for truth is fallen in the street, and equity cannot enter."),
 ("There Was No Intercessor (vv.15b-16a)",
  "And the LORD saw it, and it displeased him that there was no judgment. Then the sentence that answers "
  "Ezekiel 22:30 and Jeremiah 5:1 from the same direction, and he saw that there was no man, and wondered "
  "that there was no intercessor. Three prophets looking for one person to stand in the gap and reporting "
  "the same result. The half-verse division here is the text's own: the sentence turns at the middle of "
  "verse 16 from what was not found to what was done instead."),
 ("He Put On Righteousness as a Breastplate (vv.16b-19)",
  "Therefore his arm brought salvation unto him, and his righteousness, it sustained him. Since no human "
  "intercessor was available, the intervention is direct, and it is described as a man dressing for "
  "battle: for he put on righteousness as a breastplate, and an helmet of salvation upon his head, and he "
  "put on the garments of vengeance for clothing. Paul redistributes the same armour to the church in "
  "Ephesians 6. And the outcome is geographical, so shall they fear the name of the LORD from the west, "
  "and his glory from the rising of the sun."),
 ("The Redeemer Shall Come to Zion (v.20)",
  "One verse, and the Redeemer shall come to Zion, and unto them that turn from transgression in Jacob, "
  "saith the LORD. Paul quotes it at the climax of his argument in Romans 11:26, where the direction is "
  "slightly different in the Greek. The word Redeemer is the family term used throughout these chapters, "
  "the relative obliged to buy his kinsman out."),
 ("My Words in Thy Mouth (v.21)",
  "As for me, this is my covenant with them, saith the LORD, My spirit that is upon thee, and my words "
  "which I have put in thy mouth, shall not depart out of thy mouth, nor out of the mouth of thy seed, nor "
  "out of the mouth of thy seed's seed, from henceforth and for ever. Three generations named in one "
  "clause, and what is promised is not protection or land but the continuance of a message. It is the same "
  "pairing of spirit and words that opens the next chapter but one at 61:1."),
],
"isaiah60": [
 ("Arise, Shine (vv.1-3)",
  "Arise, shine, for thy light is come, and the glory of the LORD is risen upon thee. The command assumes "
  "the light has already arrived, so what is asked is response rather than effort. Then the contrast, and "
  "it is unusually stark, for behold, the darkness shall cover the earth, and gross darkness the people, "
  "but the LORD shall arise upon thee. And the effect on others is stated as traffic, and the Gentiles "
  "shall come to thy light, and kings to the brightness of thy rising."),
 ("Lift Up Thine Eyes (vv.4-9)",
  "Lift up thine eyes round about, and see, all they gather themselves together, they come to thee, thy "
  "sons shall come from far, and thy daughters shall be nursed at thy side. The arrival is described as "
  "freight, and the manifest is specific: the multitude of camels, the dromedaries of Midian and Ephah, "
  "gold and incense from Sheba, the flocks of Kedar and the rams of Nebaioth, and the ships of Tarshish "
  "first. Matthew 2 has gold and frankincense arriving from the east, and this is the passage behind the "
  "tradition that the visitors were kings. And the reaction is physical, then thou shalt see, and flow "
  "together, and thine heart shall fear, and be enlarged."),
 ("Strangers Shall Build Up Thy Walls (vv.10-14)",
  "And the sons of strangers shall build up thy walls, and their kings shall minister unto thee. The "
  "reversal is precise, since foreigners had pulled the walls down. Then the gates, therefore thy gates "
  "shall be open continually, they shall not be shut day nor night, which Revelation 21:25 repeats of the "
  "new Jerusalem, and the reason given here is commercial, that men may bring unto thee the forces of the "
  "Gentiles. A city with permanently open gates has nothing to fear and something to import."),
 ("Instead of Being Forsaken (vv.15-16)",
  "Whereas thou hast been forsaken and hated, so that no man went through thee, I will make thee an "
  "eternal excellency, a joy of many generations. The complaint of 49:14 and 62:4 is quoted and answered "
  "in the same sentence. And the provision is described in the same nursing image as verse 4, thou shalt "
  "also suck the milk of the Gentiles, and shalt suck the breast of kings, which is deliberately "
  "undignified for the kings and is the point."),
 ("Gold for Brass (vv.17-18)",
  "For brass I will bring gold, and for iron I will bring silver, and for wood brass, and for stones "
  "iron. Every material is upgraded one step, which reverses 1:22 where the silver had become dross and "
  "2 Chronicles 12:10 where Solomon's gold shields were replaced with brass. Then the government named as "
  "the real upgrade, I will also make thy officers peace, and thine exactors righteousness. And the "
  "outcome is the absence of a sound, violence shall no more be heard in thy land."),
 ("The LORD an Everlasting Light (vv.19-20)",
  "The sun shall be no more thy light by day, neither for brightness shall the moon give light unto thee, "
  "but the LORD shall be unto thee an everlasting light, and thy God thy glory. Revelation 21:23 says the "
  "same of the new Jerusalem. And the consequence drawn is not cosmological but emotional, thy sun shall "
  "no more go down, neither shall thy moon withdraw itself, and the days of thy mourning shall be ended, "
  "which ties the end of grief to the end of nightfall."),
 ("A Little One Shall Become a Thousand (vv.21-22)",
  "Thy people also shall be all righteous, they shall inherit the land for ever, the branch of my "
  "planting, the work of my hands, that I may be glorified. Then the last verse, addressed to a community "
  "whose problem was that it was small, a little one shall become a thousand, and a small one a strong "
  "nation. And the closing clause answers the impatience the whole book has been arguing with, I the LORD "
  "will hasten it in his time."),
],
"isaiah61": [
 ("The Spirit of the Lord GOD Is upon Me (vv.1-3)",
  "The Spirit of the Lord GOD is upon me, because the LORD hath anointed me to preach good tidings unto "
  "the meek. This is the passage Jesus reads in the synagogue at Nazareth in Luke 4, and where he stops "
  "reading is part of the account: he closes the book after to proclaim the acceptable year of the LORD, "
  "leaving out the next clause, and the day of vengeance of our God. The commission is a list of "
  "beneficiaries rather than of duties, the meek, the brokenhearted, the captives, the bound, them that "
  "mourn. And the exchanges at the end are all three of the same shape, beauty for ashes, the oil of joy "
  "for mourning, the garment of praise for the spirit of heaviness."),
 ("They Shall Build the Old Wastes (vv.4-5)",
  "And they shall build the old wastes, they shall raise up the former desolations, and they shall repair "
  "the waste cities, the desolations of many generations. The word desolations occurs three times in one "
  "verse, and what is promised is construction work on ground that has been derelict for lifetimes. Then "
  "the labour supply, and strangers shall stand and feed your flocks, and the sons of the alien shall be "
  "your plowmen, which is the same reversal as 60:10."),
 ("Ye Shall Be Named the Priests of the LORD (vv.6-7)",
  "But ye shall be named the Priests of the LORD, men shall call you the Ministers of our God. The whole "
  "community is given the office, which Exodus 19:6 had promised and which 1 Peter 2:9 takes up. Then the "
  "arithmetic of restitution, for your shame ye shall have double, and for confusion they shall rejoice in "
  "their portion, therefore in their land they shall possess the double. The double of 40:2 was punishment "
  "received; the double here is compensation, and the same word is doing both jobs."),
 ("An Everlasting Covenant (vv.8-9)",
  "For I the LORD love judgment, I hate robbery for burnt offering, which puts the two halves of this "
  "book's argument in one sentence: the objection was never to the offerings but to what funded them. And "
  "I will make an everlasting covenant with them. Then the visibility of it, and their seed shall be known "
  "among the Gentiles, all that see them shall acknowledge that they are the seed which the LORD hath "
  "blessed."),
 ("As a Bridegroom Decketh Himself (vv.10-11)",
  "I will greatly rejoice in the LORD, my soul shall be joyful in my God, for he hath clothed me with the "
  "garments of salvation, he hath covered me with the robe of righteousness. The comparison is drawn from "
  "a wedding and it names both parties, as a bridegroom decketh himself with ornaments, and as a bride "
  "adorneth herself with her jewels. And the closing image is botanical and returns to the growth "
  "language of 45:8, for as the earth bringeth forth her bud, so the Lord GOD will cause righteousness "
  "and praise to spring forth before all the nations."),
],
"isaiah62": [
 ("For Zion's Sake I Will Not Hold My Peace (vv.1-3)",
  "For Zion's sake will I not hold my peace, and for Jerusalem's sake I will not rest. The silence that "
  "the book has repeatedly described, at 42:14 and 57:11 and 64:12, is here refused, and the terms are "
  "given, until the righteousness thereof go forth as brightness, and the salvation thereof as a lamp "
  "that burneth. Then a new name promised but not yet given, and thou shalt be called by a new name, "
  "which the mouth of the LORD shall name, and the naming happens in the next section. And the closing "
  "image is jewellery held up, thou shalt also be a crown of glory in the hand of the LORD."),
 ("Hephzibah and Beulah (vv.4-5)",
  "Thou shalt no more be termed Forsaken, neither shall thy land any more be termed Desolate, but thou "
  "shalt be called Hephzibah, and thy land Beulah. The old names are the complaint of 49:14 turned into "
  "titles, and the new ones are translated in the verse itself, for the LORD delighteth in thee, and thy "
  "land shall be married. Then the comparison, and it is startling, for as a young man marrieth a virgin, "
  "so shall thy sons marry thee, and as the bridegroom rejoiceth over the bride, so shall thy God rejoice "
  "over thee."),
 ("Ye That Make Mention of the LORD, Keep Not Silence (vv.6-7)",
  "I have set watchmen upon thy walls, O Jerusalem, which shall never hold their peace day nor night. The "
  "watchmen of 56:10 could not bark; these are appointed not to stop. And what they are told to do is the "
  "boldest instruction in the book, ye that make mention of the LORD, keep not silence, and give him no "
  "rest, till he establish, and till he make Jerusalem a praise in the earth. Prayer described as "
  "deliberately refusing to let God alone."),
 ("The LORD Hath Sworn (vv.8-9)",
  "The LORD hath sworn by his right hand, and by the arm of his strength, Surely I will no more give thy "
  "corn to be meat for thine enemies. The promise is agricultural and it addresses the specific misery of "
  "an occupied country, which is growing food for somebody else's army. And the alternative is described "
  "as a meal in a particular place, but they that have gathered it shall eat it, and praise the LORD, and "
  "they that have brought it together shall drink it in the courts of my holiness."),
 ("Prepare the Way of the People (vv.10-12)",
  "Go through, go through the gates, prepare ye the way of the people, cast up, cast up the highway, "
  "gather out the stones. The road of 40:3 is being built again and this time the labour is the people's "
  "own. Then the announcement, say ye to the daughter of Zion, Behold, thy salvation cometh, behold, his "
  "reward is with him, which Revelation 22:12 repeats. And the chapter closes with the last of the new "
  "names, and they shall call them, The holy people, The redeemed of the LORD, and thou shalt be called, "
  "Sought out, A city not forsaken. Sought out is the answer to nobody going through her at 60:15."),
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
