#!/usr/bin/env python3
"""
Finishes Genesis, Leviticus, Judges and Revelation. Fourteen pages.

The omissions in this batch are larger and more surprising than the last, because
in several places what was left out is the passage the chapter exists for:

  genesis9 had sections for Noah's drunkenness and the curse on Canaan, and nothing
  for the covenant, the blessing, the charge about blood, or the rainbow. Twenty-one
  of twenty-nine verses, including the first covenant God makes with humanity.
  revelation1 had one section, 'Structure of Revelation (v.19)'. The vision of the
  Son of Man among the lampstands, the greeting, Patmos, 'I am he that liveth, and
  was dead' were all undescribed.
  revelation6 had the fifth and sixth seals and not the first four, which is to say
  it omitted the four horsemen.
  revelation13 had the beast from the sea and not the beast from the earth, so the
  mark and the number were missing.
  leviticus16 covered the Day of Atonement except vv.15-19, the blood carried inside
  the veil, which is the moment the chapter is about.
  judges19 skipped vv.5-12, the four days of delay that put the travellers at Gibeah
  after dark rather than at Jebus in daylight. The delay is why the chapter happens.

Smaller but the same kind: leviticus6 vv.14-23 on the grain offering, leviticus10
vv.4-11 where Aaron is forbidden to mourn his own sons, leviticus20 vv.17-21,
judges5 vv.9-13 and the curse on Meroz at v.23 and the song's last line at v.31,
judges18 vv.27-31 where Laish burns and the idol is installed, judges20 vv.12-17
where the demand is refused and the armies are counted, revelation8 vv.7-12 which is
the first four trumpets, revelation14 vv.6-13 which is the three angels.

Usage:
    python3 finish_four_narrative_books.py [--check]
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
RANGE_IN_LABEL = re.compile(r"\(vv?\.[^)]*\)(?=\s*:?\s*$)")

OPS = {
"genesis9": [
 ("insert", "", "The Blessing and the Charge (vv.1-7)",
  "God blessed Noah and his sons, and the first words are the words of Genesis 1, be "
  "fruitful, and multiply, and replenish the earth. The world starts again on the same "
  "instruction. But the terms have changed. The fear of you and the dread of you shall be "
  "upon every beast, which is not the dominion of the garden but something colder, and "
  "every moving thing that liveth shall be meat for you, where before it had been the green "
  "herb. Then two limits on the new permission, and both concern blood: flesh with the life "
  "thereof shall ye not eat, and whoso sheddeth man's blood, by man shall his blood be "
  "shed. The reason given for the second is the image, for in the image of God made he man, "
  "which is why the prohibition on killing is grounded in what a human being is rather than "
  "in what killing costs."),
 ("insert", "The Blessing and the Charge",
  "The Covenant and the Rainbow (vv.8-17)",
  "I establish my covenant with you, and with your seed after you. It is the first covenant "
  "in the Bible and the widest, because the parties named include every living creature, "
  "the fowl, the cattle and every beast of the earth, and the term is stated as perpetual "
  "generations. The promise is a negative one, neither shall there any more be a flood to "
  "destroy the earth, and it is unconditional, nothing is asked of Noah in return. Then the "
  "sign: I do set my bow in the cloud. A war bow hung up in the sky, and the remembering is "
  "assigned to God rather than to Noah, I will look upon it, that I may remember the "
  "everlasting covenant. The rainbow is not there to reassure the man, it is there as "
  "something God undertakes to see."),
 ("insert", "The Covenant and the Rainbow", "The Sons of Noah (vv.18-19)",
  "The sons of Noah that went forth of the ark were Shem, and Ham, and Japheth. Two verses "
  "of names, and one clause tucked inside them that the rest of the chapter turns on: and "
  "Ham is the father of Canaan. The reader is told who Canaan is before he is told what is "
  "said about him, which is how the curse in verse 25 lands on a nation rather than on a "
  "boy."),
 ("insert", "The Prophecy", "Noah's Death (vv.28-29)",
  "Noah lived after the flood three hundred and fifty years, and all his days were nine "
  "hundred and fifty years, and he died. The formula belongs to the genealogy of chapter 5 "
  "and it returns here to close the man's life the same way the others closed, which places "
  "the survivor of the flood back inside the ordinary record of death."),
],
"leviticus6": [
 ("insert", "The Law of the Burnt Offering for Priests",
  "The Law of the Grain Offering (vv.14-18)",
  "This is the law of the meat offering, and it is addressed to the priests rather than to "
  "the worshipper. A handful of the flour and the oil with all the frankincense is burnt as "
  "the memorial, and the remainder is eaten by Aaron and his sons, without leaven, in the "
  "court of the tabernacle. The portion is described as their food, and the reason it may "
  "not be taken home is stated plainly, it is most holy, as is the sin offering and as the "
  "trespass offering. The closing clause, whatsoever shall touch them shall be holy, treats "
  "holiness as something that spreads by contact."),
 ("insert", "The Law of the Grain Offering",
  "The Anointed Priest's Daily Offering (vv.19-23)",
  "One offering in the chapter is made by the priest for himself rather than eaten by him, "
  "and it is the one that begins on the day he is anointed. A tenth part of an ephah of "
  "flour, half in the morning and half at night, baked on a griddle and brought in pieces. "
  "It shall be wholly burnt, it shall not be eaten. The man who lives on the offerings of "
  "others has one offering he may take nothing from, which is the chapter's way of saying "
  "the priesthood is not a livelihood."),
],
"leviticus10": [
 ("insert", "The Sin of Nadab and Abihu",
  "Carried Out in Their Coats (vv.4-7)",
  "Two cousins are called to carry the bodies out of the camp, and the detail the text "
  "keeps is that they were carried in their coats, still wearing the priestly tunics they "
  "died in. Then the hardest instruction in the book is given to their father: uncover not "
  "your heads, neither rend your clothes, lest ye die. Aaron and his surviving sons are "
  "forbidden the ordinary signs of grief, and the reason is that the anointing oil of the "
  "LORD is upon you. The mourning is delegated, but let your brethren, the whole house of "
  "Israel, bewail the burning. Israel may weep for them. Their father may not."),
 ("insert", "Carried Out in Their Coats",
  "No Wine, and the Duty to Distinguish (vv.8-11)",
  "Do not drink wine nor strong drink, thou, nor thy sons with thee, when ye go into the "
  "tabernacle. The prohibition arrives immediately after the deaths, which has led readers "
  "for centuries to suspect what Nadab and Abihu had been doing. Then the reason, and it is "
  "the job description of a priest in two clauses: that ye may put difference between holy "
  "and unholy, and between unclean and clean, and that ye may teach the children of Israel "
  "all the statutes. Judgment and instruction, and neither survives drink."),
],
"leviticus16": [
 ("insert", "The Two Goats",
  "The Blood Brought Within the Veil (vv.15-19)",
  "This is the centre of the chapter and of the year. The goat of the sin offering is killed "
  "and its blood brought within the veil, sprinkled upon the mercy seat and before it, and "
  "the reason given is that the holy place itself needs cleansing, because of the "
  "uncleanness of the children of Israel, and because of their transgressions in all their "
  "sins. The place where God meets them has been contaminated by the people it was built "
  "for. There shall be no man in the tabernacle when he goeth in to make an atonement, so "
  "the one act on which the whole nation depends is performed with no witnesses. Then the "
  "blood is put on the altar and sprinkled seven times, to cleanse it and hallow it."),
],
"leviticus20": [
 ("insert", "Incest and Sexual Perversion",
  "Further Degrees of Kindred (vv.17-21)",
  "The penalties change here, and the change is the point. Where the previous verses "
  "specified death, these prescribe being cut off from among their people, or bearing their "
  "iniquity, or dying childless. Sister, menstruating wife, aunt, uncle's wife, brother's "
  "wife, each with a consequence that is not execution. The law is grading offences rather "
  "than levelling them, and the sanctions that land on the family line rather than the body, "
  "they shall be childless, fall on precisely the offences that confuse a family line."),
],
"judges5": [
 ("insert", "The Desperate Conditions",
  "Speak, Ye That Ride on White Asses (vv.9-13)",
  "The song turns to its audience and sorts them. Ye that ride on white asses, ye that sit "
  "in judgment, and ye that walk by the way, which is to say the wealthy, the magistrates "
  "and the ordinary traveller, all three told to speak. The archers at the watering places "
  "are told to rehearse the righteous acts of the LORD, because a well is where news "
  "travels. Then the self-address that gives the chapter its energy, awake, awake, Deborah, "
  "awake, awake, utter a song, arise, Barak. And the summary of who fought, the LORD made "
  "me have dominion over the mighty."),
 ("extend", "Jael Celebrated", "(vv.23-27)",
  "Before Jael is praised, a town is cursed. Curse ye Meroz, said the angel of the LORD, "
  "because they came not to the help of the LORD against the mighty. Meroz appears nowhere "
  "else in the Bible and is remembered for one thing, which is not turning up. It is placed "
  "immediately before the blessing on a foreign woman who did, and the contrast is "
  "deliberate."),
 ("extend", "Sisera's Mother", "(vv.28-31)",
  "The song ends by widening from the window to the world, so let all thine enemies perish, "
  "O LORD, but let them that love him be as the sun when he goeth forth in his might. Then "
  "the flattest possible closing line, and the land had rest forty years, which is the "
  "book's refrain and, this time, the last calm one for a while."),
],
"judges18": [
 ("insert", "Micah's Futile Pursuit",
  "Laish Burned and the Idol Set Up (vv.27-31)",
  "The chapter ends the way it was always going to. Laish is taken, and the text notes why "
  "it fell easily, the people were quiet and secure, and there was no deliverer, because it "
  "was far from Zidon. The Danites burn it, rebuild it, and rename it Dan, and the tribe "
  "that could not hold the coastal plain it was allotted now holds a town in the far north. "
  "Then the stolen idol is installed, and the priest is named at last: Jonathan, the son of "
  "Gershom, the son of Manasseh. Older manuscripts read Moses. Whichever it is, a "
  "Levite of the founding family is set up over a graven image, and the text says it stayed "
  "there all the time that the house of God was in Shiloh."),
],
"judges19": [
 ("insert", "The Levite and His Concubine",
  "Four Days of Delay and the Road North (vv.5-12)",
  "Eight verses of hospitality that read as comedy until you see what they cost. Four times "
  "the Levite tries to leave and four times his father-in-law presses him to stay, comfort "
  "thine heart with a morsel of bread, tarry all night, and the day wears away. When they "
  "finally go it is late afternoon. At Jebus the servant suggests stopping, and the Levite "
  "refuses on principle, we will not turn aside hither into the city of a stranger, that is "
  "not of the children of Israel. So they press on to Gibeah because it is Israelite and "
  "therefore safe. Every delay and every choice in this passage is ordinary, and together "
  "they put these travellers in a Benjamite town after dark."),
],
"judges20": [
 ("insert", "Israel Assembles at Mizpah",
  "The Demand Refused and the Armies Numbered (vv.12-17)",
  "Before any fighting, Israel does the lawful thing and sends messengers through the whole "
  "tribe of Benjamin with a single demand: deliver us the men, the children of Belial, which "
  "are in Gibeah, that we may put them to death. It is the response the law would require, "
  "and Benjamin refuses to hearken to the voice of their brethren. So a criminal case becomes "
  "a civil war by the choice of the tribe protecting the criminals. Then the numbers, and "
  "they are given carefully: twenty-six thousand from Benjamin plus seven hundred chosen men "
  "of Gibeah, and seven hundred left-handed slingers who could sling stones at an hair "
  "breadth and not miss, against four hundred thousand of Israel."),
],
"revelation1": [
 ("insert", "", "The Prologue and the Blessing (vv.1-3)",
  "The book names itself in its first three words, the Revelation of Jesus Christ, and then "
  "traces its route: from God, to Jesus, by his angel, unto his servant John, to be shown "
  "unto his servants. Four hands before it reaches a reader. Then the only beatitude in the "
  "book's opening, and it is aimed at a meeting rather than a scholar, blessed is he that "
  "readeth, and they that hear the words of this prophecy, and keep those things which are "
  "written therein. One reader aloud and a room listening, which is how it was meant to "
  "arrive. And the reason for urgency, for the time is at hand."),
 ("insert", "The Prologue and the Blessing",
  "Greeting from Him Which Is, and Which Was (vv.4-8)",
  "John to the seven churches which are in Asia. The greeting names its source three times "
  "over, from him which is, and which was, and which is to come, from the seven Spirits, and "
  "from Jesus Christ. Then three titles for Jesus that set the book's terms, the faithful "
  "witness, the first begotten of the dead, and the prince of the kings of the earth, and a "
  "doxology to him that loved us and washed us from our sins in his own blood. Behold, he "
  "cometh with clouds, and every eye shall see him, and they also which pierced him, which "
  "is Zechariah 12 quoted at the start rather than the end. I am Alpha and Omega, the "
  "beginning and the ending, saith the Lord."),
 ("insert", "Greeting from Him Which Is, and Which Was",
  "John on Patmos (vv.9-11)",
  "I John, who also am your brother, and companion in tribulation. He introduces himself by "
  "what he shares rather than by his office, and locates himself precisely: in the isle that "
  "is called Patmos, for the word of God, and for the testimony of Jesus Christ. A penal "
  "island in the Aegean. I was in the Spirit on the Lord's day, and heard behind me a great "
  "voice, as of a trumpet, and the instruction is to write and send to seven named churches, "
  "which turns a vision into correspondence."),
 ("insert", "John on Patmos",
  "The Son of Man Among the Lampstands (vv.12-16)",
  "He turns to see the voice and sees seven golden candlesticks, and one like unto the Son "
  "of man in the midst of them. The description is assembled from Daniel and Ezekiel and "
  "runs head to foot: hair white like wool, eyes as a flame of fire, feet like fine brass, "
  "voice as the sound of many waters, seven stars in his right hand, a sharp two-edged sword "
  "out of his mouth, countenance as the sun shineth in his strength. The detail that "
  "governs the next two chapters is the position, in the midst of them, because the letters "
  "are written by someone standing among the churches rather than over them."),
 ("insert", "The Son of Man Among the Lampstands",
  "Fear Not, I Am the First and the Last (vv.17-18)",
  "And when I saw him, I fell at his feet as dead. The response is collapse, and the remedy "
  "is a hand: he laid his right hand upon me, saying unto me, Fear not. The same hand that "
  "held the seven stars. Then the credentials that make the command reasonable, I am the "
  "first and the last, I am he that liveth, and was dead, and behold, I am alive for "
  "evermore, and have the keys of hell and of death. The one telling a frightened man not to "
  "be afraid is the one who has already been through the thing he is afraid of."),
 ("insert", "Structure of Revelation",
  "The Seven Stars and the Lampstands (v.20)",
  "The chapter closes by explaining its own symbols, which the book rarely does again. The "
  "seven stars are the angels of the seven churches, and the seven candlesticks are the "
  "seven churches. The word rendered angels is the ordinary word for messengers, which is "
  "why readers have argued ever since over whether the letters are addressed to heavenly "
  "guardians or to the men who carried them."),
],
"revelation6": [
 ("insert", "", "The Four Horsemen (vv.1-8)",
  "The Lamb opens the seals and each of the first four is answered by one of the living "
  "creatures saying Come and see, and a horse goes out. White, with a bow and a crown given "
  "him, and he went forth conquering. Red, and power was given to him that sat thereon to "
  "take peace from the earth. Black, with a pair of balances, and a voice pricing wheat and "
  "barley at a day's wage for a day's food while telling the rider to spare the oil and the "
  "wine, which is famine described as an inflation report. Then pale, and his name that sat "
  "on him was Death, and Hell followed with him, with power over a fourth part of the earth "
  "by sword, hunger, death and the beasts. The verb that recurs is given: the authority in "
  "all four is handed out rather than seized."),
],
"revelation8": [
 ("insert", "Prayers and Fire", "The First Four Trumpets (vv.7-12)",
  "Four trumpets, and each strikes a third of something. Hail and fire mingled with blood "
  "on the earth, and a third of the trees burnt. A great mountain burning cast into the sea, "
  "and a third of the sea became blood. A star called Wormwood falling on the rivers, and "
  "many men died of the waters because they were made bitter. Then a third of the sun and "
  "moon and stars struck, so that the day shone not for a third part of it. The pattern is "
  "the plagues of Egypt run at a larger scale and stopped short each time, which is the "
  "point of the fraction: this is warning rather than end."),
],
"revelation13": [
 ("insert", "The Beast from the Sea",
  "The Beast from the Earth and the Mark (vv.11-18)",
  "A second beast, and everything about it is imitation. It comes up out of the earth rather "
  "than the sea, it has two horns like a lamb, and it spake as a dragon. Its work is "
  "entirely promotional: it causeth the earth to worship the first beast, does great "
  "wonders, brings fire down from heaven, and gives breath to an image so that the image "
  "speaks. Then the economic instrument, and it is the detail the chapter is remembered for, "
  "that no man might buy or sell, save he that had the mark, in his right hand, or in his "
  "forehead. Worship enforced through commerce rather than through the sword. The chapter "
  "ends by handing the reader a puzzle instead of an answer, here is wisdom, let him that "
  "hath understanding count the number of the beast, for it is the number of a man, and his "
  "number is six hundred threescore and six."),
],
"revelation14": [
 ("insert", "The 144,000 with the Lamb",
  "Three Angels and Two Blessings (vv.6-13)",
  "Three angels fly in succession, each with one thing to say. The first has the everlasting "
  "gospel to preach unto every nation, and kindred, and tongue, and people, and its content "
  "is a command to fear God and worship the Creator. The second announces a fall in the past "
  "tense, Babylon is fallen, is fallen, that great city. The third pronounces the severest "
  "warning in the book on those who take the mark. Then, set directly against it, two "
  "sentences of comfort: here is the patience of the saints, here are they that keep the "
  "commandments of God, and blessed are the dead which die in the Lord from henceforth, that "
  "they may rest from their labours, and their works do follow them."),
],
}


def find(items, prefix):
    for i, (label, _) in enumerate(items):
        if H.unescape(label).strip().startswith(prefix):
            return i
    return -1


def first_section(items):
    for i, (label, _) in enumerate(items):
        if re.search(r"\(vv?\.[^)]*\)\s*:?\s*$", H.unescape(label).strip()):
            return i
    return len(items)


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, ops in OPS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        for op in ops:
            kind = op[0]
            if kind == "extend":
                _, prefix, rng, prose = op
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: extend target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                items[i][1] += " " + prose
                notes.append(f"{page}: extended {prefix!r} to {rng}")
            elif kind == "insert":
                _, after, label, prose = op
                at = first_section(items) if after == "" else find(items, after) + 1
                if after and at == 0:
                    problems.append(f"{page}: insert anchor {after!r} not found")
                    continue
                items.insert(at, [label + ":", prose])
                notes.append(f"{page}: inserted {label!r}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new
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
    print(f"{'would touch' if check else 'touched'} {len(planned)} pages, "
          f"{len(notes)} change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
