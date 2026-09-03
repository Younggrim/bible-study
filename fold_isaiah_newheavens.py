#!/usr/bin/env python3
"""
Isaiah 63 to 66: the winepress, the last prayer, and the new heavens. Four pages,
80 verses. All four outlines are gapless and are folded.

Chapters 63 and 64 are one long prayer with a violent preface, and it is the most
unresolved passage in the book: it asks where art thou, accuses God of hardening, and ends
on a question that is never answered, wilt thou hold thy peace, and afflict us very sore.
Chapter 65 answers it, and the answer begins by saying that the people who were not
looking are the ones who found him.

The book ends on two verses that most readers find difficult, and the section says what
they contain rather than passing over them: perpetual worship in 66:23 and the unquenched
fire of 66:24, in consecutive sentences, with the worshippers looking at the corpses. Jesus
quotes the last verse three times in Mark 9.

Usage:
    python3 fold_isaiah_newheavens.py [--check]
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
"isaiah63": [
 ("Who Is This from Edom (vv.1-6)",
  "Who is this that cometh from Edom, with dyed garments from Bozrah, this that is glorious in his "
  "apparel, travelling in the greatness of his strength. The passage opens as a challenge from a watchman "
  "to an approaching figure, and the answer identifies both the stains and the work, I have trodden the "
  "winepress alone, and of the people there was none with me. The imagery is a grape harvest and the "
  "juice is blood, and their blood shall be sprinkled upon my garments. Revelation 19:13-15 takes it up "
  "of the rider on the white horse. Two details are worth holding on to. The aloneness is stated twice, "
  "which connects to 59:16, where no intercessor could be found. And the motive given is legal, for the "
  "day of vengeance is in mine heart, and the year of my redeemed is come, so the vengeance and the "
  "redemption are one date."),
 ("I Will Mention the Lovingkindnesses (vv.7-9)",
  "I will mention the lovingkindnesses of the LORD, and the praises of the LORD, according to all that the "
  "LORD hath bestowed on us. The tone changes completely from the winepress and stays changed for the "
  "rest of the chapter. Then a sentence about identification that has no real parallel in the Old "
  "Testament, in all their affliction he was afflicted, and the angel of his presence saved them. And the "
  "carrying image of 46:4 returns, in his love and in his pity he redeemed them, and he bare them, and "
  "carried them all the days of old."),
 ("They Rebelled and Vexed His Holy Spirit (vv.10-14)",
  "But they rebelled, and vexed his holy Spirit, therefore he was turned to be their enemy, and he fought "
  "against them. That last clause is among the hardest in the book, and Paul's grieve not the Holy Spirit "
  "in Ephesians 4:30 is drawing on this verse. Then the memory works backwards through the exodus, where "
  "is he that brought them up out of the sea with the shepherd of his flock, where is he that put his holy "
  "Spirit within him. The questions are asked in the past tense about a God who is present, which is what "
  "makes them a prayer rather than a history. And the closing image is livestock finding shelter, as a "
  "beast that goeth down into the valley, so didst thou lead thy people, to make thyself a glorious name."),
 ("Where Is Thy Zeal (vv.15-19)",
  "Look down from heaven, and behold from the habitation of thy holiness and of thy glory, where is thy "
  "zeal and thy strength, the sounding of thy bowels and of thy mercies toward me, are they restrained. "
  "Then the appeal goes behind the ancestors to the only relationship left, doubtless thou art our father, "
  "though Abraham be ignorant of us, and Israel acknowledge us not, thou, O LORD, art our father, our "
  "redeemer. And the boldest sentence in the prayer is put as a question, O LORD, why hast thou made us to "
  "err from thy ways, and hardened our heart from thy fear. The prophet who was told at 6:10 to make the "
  "heart of the people fat is now asking why it was done."),
],
"isaiah64": [
 ("Oh That Thou Wouldest Rend the Heavens (vv.1-3)",
  "Oh that thou wouldest rend the heavens, that thou wouldest come down, that the mountains might flow "
  "down at thy presence. The prayer of chapter 63 continues and it asks for a tearing rather than an "
  "opening, and the model cited is Sinai, when thou didst terrible things which we looked not for, thou "
  "camest down, the mountains flowed down at thy presence. What is being requested is a repeat of the "
  "most frightening event in the national memory, on the grounds that it would at least be "
  "unmistakable."),
 ("Neither Hath the Eye Seen (v.4)",
  "One verse, and for since the beginning of the world men have not heard, nor perceived by the ear, "
  "neither hath the eye seen, O God, beside thee, what he hath prepared for him that waiteth for him. "
  "Paul quotes it in 1 Corinthians 2:9, and in both places the point is the same: the thing being waited "
  "for has no precedent in anybody's experience, so nobody's imagination is the measure of it. And the "
  "condition attached is the one this book returns to more than any other, for him that waiteth for him."),
 ("All Our Righteousnesses Are as Filthy Rags (vv.5-7)",
  "Behold, thou art wroth, for we have sinned, in those is continuance, and we shall be saved. Then the "
  "confession that the chapter is known for, and it does not exempt the good conduct, but we are all as an "
  "unclean thing, and all our righteousnesses are as filthy rags. The image after it is autumnal, and we "
  "all do fade as a leaf, and our iniquities, like the wind, have taken us away. And the last verse "
  "describes the state of religious practice, and there is none that calleth upon thy name, that stirreth "
  "up himself to take hold of thee, with the cause assigned to God in the same breath, for thou hast hid "
  "thy face from us, and hast consumed us, because of our iniquities."),
 ("We Are the Clay (v.8)",
  "One verse, and it is the turn of the whole prayer. But now, O LORD, thou art our father, we are the "
  "clay, and thou our potter, and we all are the work of thy hand. Where the potter image is used in "
  "45:9 and Jeremiah 18 to silence an objection, here it is picked up by the objectors themselves and "
  "used as a plea: if we are your work, the state we are in is your concern. It is the strongest argument "
  "in the prayer and it is made in eight words."),
 ("Wilt Thou Hold Thy Peace (vv.9-12)",
  "Be not wroth very sore, O LORD, neither remember iniquity for ever, behold, see, we beseech thee, we "
  "are all thy people. Then the state of the buildings, which dates the prayer, thy holy cities are a "
  "wilderness, Zion is a wilderness, Jerusalem a desolation, our holy and our beautiful house, where our "
  "fathers praised thee, is burned up with fire. And the chapter, and the prayer, ends on a question that "
  "is left standing: wilt thou refrain thyself for these things, O LORD, wilt thou hold thy peace, and "
  "afflict us very sore. Chapter 65 is the answer, and it does not begin the way the prayer expected."),
],
"isaiah65": [
 ("I Am Found of Them That Sought Me Not (v.1)",
  "I am sought of them that asked not for me, I am found of them that sought me not, I said, Behold me, "
  "behold me, unto a nation that was not called by my name. This is the answer to two chapters of prayer "
  "and it begins by pointing somewhere else entirely: the people who were not looking are the ones who "
  "found him. Paul quotes it in Romans 10:20 of the Gentiles, and reads the following verse of Israel. "
  "The doubled Behold me, behold me is the note of availability the prayer had said was missing."),
 ("I Have Spread Out My Hands All the Day (vv.2-7)",
  "I have spread out my hands all the day unto a rebellious people. The hiddenness complained of at 64:7 "
  "is answered with a posture: hands out, all day. Then the practices, and they are specifically the "
  "cults of the dead and of the underworld, which remain among the graves, and lodge in the monuments, "
  "which eat swine's flesh, and broth of abominable things. And the quoted attitude is the worst of it, "
  "which say, Stand by thyself, come not near to me, for I am holier than thou. People engaged in that "
  "list telling others to keep their distance for reasons of purity."),
 ("As the New Wine in the Cluster (vv.8-12)",
  "Thus saith the LORD, As the new wine is found in the cluster, and one saith, Destroy it not, for a "
  "blessing is in it, so will I do for my servants' sake, that I may not destroy them all. The remnant is "
  "described as a reason not to clear a whole vineyard: one good bunch stays the harvester's hand. Then "
  "the division within the people is made by name and it is a division of function, my servants shall eat, "
  "but ye shall be hungry, my servants shall drink, but ye shall be thirsty. And the charge in the last "
  "verse is about answering, because when I called, ye did not answer, when I spake, ye did not hear."),
 ("Ye Shall Leave Your Name for a Curse (vv.13-16)",
  "Behold, my servants shall sing for joy of heart, but ye shall cry for sorrow of heart, and shall howl "
  "for vexation of spirit. The contrast is drawn six times in four verses, which is the same device as "
  "the woes of chapter 5. Then the sentence on the name, and ye shall leave your name for a curse unto my "
  "chosen, and the LORD God shall slay thee, and call his servants by another name. And the title given in "
  "the last verse is unusual and precise, the God of truth, twice, which in Hebrew is the God of Amen."),
 ("New Heavens and a New Earth (vv.17-25)",
  "For, behold, I create new heavens and a new earth, and the former shall not be remembered, nor come "
  "into mind. Revelation 21:1 takes up the phrase, and what is striking here is how ordinary the content "
  "is. What follows is a description of a working town: no more infant deaths, people living out their "
  "lives, houses built by the people who will live in them, vineyards planted by the people who will "
  "drink from them. And they shall not build, and another inhabit, they shall not plant, and another eat, "
  "which reverses the specific misery of Deuteronomy 28:30 and of an occupied country. Prayer answered "
  "before it is finished, and it shall come to pass, that before they call, I will answer. And the chapter "
  "closes with 11:6 repeated in shorter form, the wolf and the lamb shall feed together, and the lion "
  "shall eat straw like the bullock, with one clause added, and dust shall be the serpent's meat, which "
  "leaves Genesis 3 in force in the middle of a new creation."),
],
"isaiah66": [
 ("The Heaven Is My Throne (vv.1-2)",
  "Thus saith the LORD, The heaven is my throne, and the earth is my footstool, where is the house that ye "
  "build unto me, and where is the place of my rest. Stephen quotes this in Acts 7 against the temple "
  "authorities, and Solomon had made the same point at the dedication in 2 Chronicles 6:18. Then the "
  "answer to the question, and it is a person rather than a building, but to this man will I look, even to "
  "him that is poor and of a contrite spirit, and trembleth at my word. Three qualifications, none of "
  "them architectural."),
 ("He That Killeth an Ox, as If He Slew a Man (vv.3-4)",
  "He that killeth an ox is as if he slew a man, he that sacrificeth a lamb, as if he cut off a dog's "
  "neck. Four legitimate offerings are each paired with an atrocity, which is the sharpest form the "
  "book's argument about worship takes, and it goes back to 1:11. The reason is given in the same verse "
  "and it is about pleasure rather than procedure, their soul delighteth in their abominations. And the "
  "consequence is a matching silence, I also will choose their delusions, and will bring their fears upon "
  "them, because when I called, none did answer."),
 ("Your Brethren That Hated You (vv.5-6)",
  "Hear the word of the LORD, ye that tremble at his word, and what follows is unusual: a word addressed "
  "to the devout about being excluded by other religious people. Your brethren that hated you, that cast "
  "you out for my name's sake, said, Let the LORD be glorified, and their sneer is quoted with the pious "
  "formula intact. And the answer comes from the building itself, a voice of noise from the city, a voice "
  "from the temple, a voice of the LORD that rendereth recompence to his enemies."),
 ("Before She Travailed, She Brought Forth (vv.7-9)",
  "Before she travailed, she brought forth, before her pain came, she was delivered of a man child. The "
  "birth is described as impossibly quick, which is the point of the questions that follow, who hath "
  "heard such a thing, who hath seen such things, shall the earth be made to bring forth in one day. And "
  "the argument closes with the most practical image in the chapter, shall I bring to the birth, and not "
  "cause to bring forth, saith the LORD. A midwife who does not abandon a delivery half way."),
 ("As One Whom His Mother Comforteth (vv.10-14)",
  "Rejoice ye with Jerusalem, and be glad with her, all ye that love her, rejoice for joy with her, all ye "
  "that mourn for her. The invitation is addressed to the mourners specifically. Then the nursing image "
  "that has run through 49:23 and 60:16 reaches its fullest form, that ye may suck, and be satisfied with "
  "the breast of her consolations, and behold, I will extend peace to her like a river, and the glory of "
  "the Gentiles like a flowing stream. And then the comparison the book has been working toward, as one "
  "whom his mother comforteth, so will I comfort you, which finally supplies the subject of the imperative "
  "at 40:1."),
 ("The LORD Will Come with Fire (vv.15-17)",
  "For, behold, the LORD will come with fire, and with his chariots like a whirlwind, to render his anger "
  "with fury. The scale is universal, and the slain of the LORD shall be many. Then the specific "
  "practices named one last time, they that sanctify themselves and purify themselves in the gardens, "
  "eating swine's flesh, and the abomination, and the mouse. The list is deliberately petty against the "
  "chariots and the whirlwind, and that is its force: the fire is coming about the garden rituals."),
 ("I Will Send Them unto the Nations (vv.18-21)",
  "And I will gather all nations and tongues, and they shall come, and see my glory. Then something the "
  "Old Testament almost never says, and I will send those that escape of them unto the nations, and the "
  "list of destinations is geographical and distant, Tarshish, Pul, Lud, Tubal, Javan, and the isles afar "
  "off, that have not heard my fame, neither have seen my glory, and they shall declare my glory among the "
  "Gentiles. Missionaries sent out rather than pilgrims coming in. And the last verse goes further than "
  "anything before it, and I will also take of them for priests and for Levites, saith the LORD, so the "
  "foreigners of 56:6 are not merely admitted to the temple but ordained in it."),
 ("From One New Moon to Another (vv.22-24)",
  "For as the new heavens and the new earth which I will make shall remain before me, so shall your seed "
  "and your name remain. Then worship described as a permanent schedule rather than an event, and it "
  "shall come to pass, that from one new moon to another, and from one sabbath to another, shall all flesh "
  "come to worship before me. And then the last verse of the book, which most readers find difficult and "
  "which is quoted three times by Jesus in Mark 9: they shall go forth, and look upon the carcases of the "
  "men that have transgressed against me, for their worm shall not die, neither shall their fire be "
  "quenched, and they shall be an abhorring unto all flesh. The valley outside the walls where the fires "
  "burned is the ge-hinnom of Jeremiah 7 and 19, which becomes the New Testament word for hell. The book "
  "ends with worshippers and corpses in consecutive sentences, and it does not soften the join. Jewish "
  "synagogue practice repeats verse 23 after verse 24 so that the reading does not close on it, which is "
  "itself an acknowledgement of how the ending lands."),
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
