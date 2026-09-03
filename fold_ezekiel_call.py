#!/usr/bin/env python3
"""
Ezekiel 1 to 11: the call, the sign-acts, and the glory leaving the temple. Eleven
pages, 217 verses.

These pages are different from 2 Chronicles' in one important way: the inherited
sublists here are real outlines. Measured against each chapter's own verse count, all
eleven cover every verse exactly once with no overlaps, which is what an outline does
and what a topical index does not. So they are folded rather than preserved as a field,
which is the treatment Hosea and Zechariah got. The divisions are kept, the labels are
rewritten into the corpus's nominal style, and prose exposition is written for each.

The four book fields are kept as they stand, and ezekiel1 keeps its Date field as well.
One repair is made in passing: ezekiel2's Historical Context contains won'T, a casualty
of some earlier uppercasing pass, and it is the only occurrence of that corruption in
the corpus.

The three stages of the glory's departure are the spine of this block, and the sections
say so where they fall: the threshold at 9:3, the east gate at 10:18-19, and the
mountain on the east side of the city at 11:23. Nothing has been destroyed yet when the
building is already empty.

Usage:
    python3 fold_ezekiel_call.py [--check]
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
KEEP = ("Author:", "Date:", "Classification:", "Key Themes:", "Historical Context:",
        "Notable:")

# Body-level repairs applied to preserved fields. Raw HTML, so entities as stored.
REPAIRS = {
    "ezekiel2": [("won&#x27;T listen", "won&#x27;t listen")],
}

SECTIONS = {
"ezekiel1": [
 ("Date and Place, by the River Chebar (vv.1-3)",
  "The book opens with two datings that do not obviously agree. The first is the thirtieth year, "
  "fourth month, fifth day, with no era named. The second is the fifth year of Jehoiachin's "
  "captivity, which fixes it at 593 BC. The usual reading of the thirtieth year is Ezekiel's own "
  "age, which matters because thirty is the age at which a priest entered service; the son of Buzi "
  "the priest reaches it beside an irrigation canal in Babylonia and will never serve in a temple. "
  "The other oddity is grammatical, verse 1 is first person and verse 3 is third, and the book "
  "keeps switching. What both verses agree on is location, among the captives by the river of "
  "Chebar, in the land of the Chaldeans, and the hand of the LORD was there upon him."),
 ("The Storm out of the North (v.4)",
  "One verse to establish the direction everything else comes from. A whirlwind out of the north, a "
  "great cloud, and a fire infolding itself, with a brightness about it, and out of the midst of it "
  "the colour of amber. North is the compass point Babylonian armies arrived from, and it is also "
  "where the storm gods of the region were held to live. The vision comes from the direction the "
  "trouble comes from."),
 ("The Four Living Creatures (vv.5-14)",
  "Four creatures, each with four faces and four wings, the likeness of a man about them, straight "
  "feet like a calf's, and human hands under the wings. The faces are man, lion, ox and eagle, and "
  "the movement is the detail Ezekiel keeps returning to, they went every one straight forward, and "
  "they turned not when they went. Their appearance is like burning coals and lamps, and they run "
  "and return as the appearance of a flash of lightning. Revelation 4 draws directly on this "
  "description, redistributing the four faces so that each of its creatures carries one."),
 ("The Wheels, and a Wheel Within a Wheel (vv.15-21)",
  "Beside each creature a wheel on the ground, the colour of a beryl, and constructed so that it "
  "could move in any direction without turning, as it were a wheel in the middle of a wheel. Their "
  "rings are full of eyes round about. When the creatures went, the wheels went by them, and when "
  "they were lifted up the wheels were lifted with them, and the reason given is not mechanical, "
  "for the spirit of the living creature was in the wheels. Everything about this apparatus is "
  "designed to be mobile, and for a man among deportees that is the whole point of it. The throne "
  "is not fixed in Jerusalem."),
 ("The Firmament Above Their Heads (vv.22-25)",
  "Over the creatures a firmament, the colour of the terrible crystal, stretched forth over their "
  "heads above. The noise of their wings is described three ways in one verse, like the noise of "
  "great waters, as the voice of the Almighty, the noise of an host. When they stood still, they let "
  "down their wings, and there was a voice from the firmament that was over their heads. The account "
  "moves upward one layer at a time, and each layer is quieter about what it is describing than the "
  "one below."),
 ("The Throne, and the Likeness of a Man Upon It (vv.26-28)",
  "Above the firmament the likeness of a throne, as the appearance of a sapphire stone, and upon it "
  "the likeness as the appearance of a man, amber and fire above the loins and below them, with a "
  "brightness round about like the bow in the cloud in the day of rain. Every noun in these three "
  "verses is hedged, likeness, appearance, as the colour of, so that the prophet is describing a "
  "resemblance and saying so at every step. The summary he gives is careful in exactly the same "
  "way, this was the appearance of the likeness of the glory of the LORD. His response is not "
  "analysis, and I fell upon my face, and I heard a voice of one that spake."),
],
"ezekiel2": [
 ("Son of Man, and the Spirit That Set Him on His Feet (vv.1-2)",
  "The address used here will be used ninety-three times in the book, and in Hebrew it means simply "
  "human being, mortal. Set against the throne of the previous chapter it functions as a "
  "counterweight, and the two verses make the point structurally as well: he is told to stand upon "
  "his feet, and he cannot do it until the spirit entered into me, and set me upon my feet. The "
  "commission begins with a man who has to be stood up before he can be spoken to."),
 ("The Commission to a Rebellious House (vv.3-5)",
  "The terms are stated without optimism. I send thee to the children of Israel, to a rebellious "
  "nation, and the description is stacked, impudent children and stiffhearted, or in the Hebrew "
  "idiom hard of face and hard of heart. Then the clause that separates this commission from a "
  "mission statement, whether they will hear, or whether they will forbear. Success is redefined so "
  "that it does not depend on the audience at all, yet shall know that there hath been a prophet "
  "among them. That is the standard the whole book is written to."),
 ("Briers, Thorns and Scorpions (vv.6-7)",
  "Twice in two verses he is told not to be afraid, once of their words and once of their looks, be "
  "not dismayed at their looks. The imagery is of a man walking through ground that will tear at "
  "him, briers and thorns and scorpions. And the instruction is repeated verbatim from the previous "
  "section, thou shalt speak my words unto them, whether they will hear or forbear, which is this "
  "book's method: it says a thing, and then says it again in the same words, until the reader stops "
  "expecting a different outcome."),
 ("The Roll Written Within and Without (vv.8-10)",
  "A hand appears holding the roll of a book, and it is spread before him. Two details are given "
  "about it. It was written within and without, that is, on both sides, which for a scroll means "
  "there is no space left for anything else. And there was written therein lamentations, and "
  "mourning, and woe. Before the prophet has said anything, the content of his message has been "
  "shown to him and it is all of one kind. He is also told to eat it, which is where chapter 3 "
  "begins."),
],
"ezekiel3": [
 ("The Roll Eaten, and Sweet as Honey (vv.1-3)",
  "Eat that thou findest, eat this roll, and go speak unto the house of Israel. The order of "
  "operations is the point: the message is internalised before it is delivered, and it goes in "
  "before it goes out. What surprises is the taste, then did I eat it, and it was in my mouth as "
  "honey for sweetness, given that the contents were lamentations, mourning and woe. Revelation 10 "
  "repeats the scene almost exactly and adds the other half of the experience, sweet in the mouth "
  "and bitter in the belly."),
 ("Sent to Israel, Who Will Not Hearken (vv.4-11)",
  "The argument here is uncomfortable and deliberately so. He is not sent to a people of a strange "
  "speech, and the reason given is not convenience: had he been sent to strangers, they would have "
  "hearkened unto thee. It is his own people who will not. Against that, the equipment he is given "
  "is entirely defensive, behold, I have made thy face strong against their faces, and thy forehead "
  "strong against their foreheads. The name Ezekiel means God strengthens, and the verse is built on "
  "that pun. He is sent to the captivity with a single instruction, whether they hear or whether "
  "they forbear."),
 ("The Spirit Lifts Him, and He Sits Seven Days (vv.12-15)",
  "A noise of a great rushing, and a doxology that will matter later in the book, blessed be the "
  "glory of the LORD from his place. Then the flattest and most human sentence in the chapter, so "
  "the spirit lifted me up, and took me away, and I went in bitterness, in the heat of my spirit. "
  "He arrives at Tel-abib and the verb chosen is precise, I sat where they sat, and remained there "
  "astonished among them seven days. The commission does not begin with speech. It begins with a "
  "week of silence in the middle of the people he has been sent to."),
 ("The Watchman (vv.16-21)",
  "After the seven days the word comes, and the office is defined in terms of liability rather than "
  "of results. If the watchman does not give warning, the wicked man dies in his iniquity and his "
  "blood will I require at thine hand. If he warns and is not heard, then thou hast delivered thy "
  "soul. The same reasoning is applied to the righteous man who turns aside. What the watchman "
  "controls is whether the warning was given, and nothing else. This commission is restated at "
  "length in 33:1-9, after Jerusalem has fallen, so the whole book of oracles sits between two "
  "statements of the same job description."),
 ("The Plain, the Bands, and the Tongue Made Dumb (vv.22-27)",
  "He is sent out into the plain, sees the glory again, and is given three restrictions. Shut "
  "thyself within thine house. They shall put bands upon thee. And I will make thy tongue cleave to "
  "the roof of thy mouth, that thou shalt be dumb. The dumbness is not total, and the exception is "
  "stated in the same breath, but when I speak with thee, I will open thy mouth. What he loses is "
  "ordinary conversation, not prophecy; he becomes a man who can only say what he is given to say. "
  "The condition holds until the night the news of Jerusalem's fall arrives, at 33:22."),
],
"ezekiel4": [
 ("The Tile, the Fort and the Iron Pan (vv.1-3)",
  "The first of the sign-acts, and it is a scale model. Portray the city upon a tile, then lay siege "
  "against it, build a fort, cast a mount, set the camp and set battering rams against it round "
  "about. The iron pan set between the prophet and the city has been read as the impenetrability of "
  "the siege works and as a barrier between God and Jerusalem, and the text does not decide. What is "
  "certain is the posture, thou shalt set thy face against it, and it shall be besieged. The siege "
  "he is modelling is about four years away."),
 ("Three Hundred and Ninety Days on the Left Side (vv.4-5)",
  "Lie upon thy left side, and lay the iniquity of the house of Israel upon it, with the conversion "
  "rate stated, I have appointed thee each day for a year. The arithmetic of three hundred and "
  "ninety has never been settled against any period anyone can name, and the Septuagint reads a "
  "hundred and ninety instead, which suggests the difficulty is old. What the sign communicates does "
  "not depend on solving it: a man lying in the street for over a year, in public, bearing a "
  "quantity of guilt measured out in days."),
 ("Forty Days on the Right Side (vv.6-8)",
  "Then forty days on the right side for the house of Judah, again a day for a year. The physical "
  "conditions are specified, the arm uncovered as a man's arm is for work or for striking, the face "
  "set toward the model of the siege, and bands laid on him so that he could not turn himself from "
  "one side to another till the days of the siege were ended. The sign is immobilisation, which is "
  "what a siege is."),
 ("Siege Bread, Weighed and Measured (vv.9-17)",
  "The ration is specified as a recipe, wheat, barley, beans, lentils, millet and fitches in one "
  "vessel, which is what is left when no single grain can be had in quantity. Twenty shekels of "
  "bread a day, about eight ounces, and the sixth part of an hin of water, and both are to be taken "
  "by weight and by measure. Then the instruction he objects to, baking it over human dung, and his "
  "objection is a priest's, Ah Lord GOD, behold, my soul hath not been polluted. It is the first "
  "time he speaks in the book and it is a complaint, and it is partly granted, cow's dung instead. "
  "The purpose of the whole sign is given at the end and it is about dread rather than hunger, that "
  "they may eat bread by weight, and with care, and drink water by measure, and with astonishment."),
],
"ezekiel5": [
 ("The Razor, and the Hair Divided in Three (vv.1-4)",
  "Take thee a sharp knife, take thee a barber's razor, and cause it to pass upon thine head and "
  "upon thy beard. For a priest this is itself a violation, since Leviticus 21 forbids it, and that "
  "is part of the sign. The hair is then weighed and divided: a third burnt in the midst of the "
  "city, a third cut with the knife, a third scattered in the wind. A few hairs are bound in his "
  "skirt, which looks like a promise of a remnant until the next clause takes some of those and "
  "throws them into the fire too. The sign refuses the comfort it appears to be offering."),
 ("This Is Jerusalem, Worse Than the Nations (vv.5-8)",
  "The interpretation is given plainly, this is Jerusalem, I have set it in the midst of the "
  "nations. The charge is comparative and it is the sharpest form of it in the book: she hath "
  "changed my judgments into wickedness more than the nations, and my statutes more than the "
  "countries that are round about her. Privileged position is treated as aggravation rather than as "
  "protection. And the sentence is announced in the first person twice over, behold, I, even I, am "
  "against thee, and will execute judgments in the midst of thee in the sight of the nations."),
 ("What Has Not Been Done Before (vv.9-10)",
  "I will do in thee that which I have not done, and whereunto I will not do any more the like, "
  "because of all thine abominations, which claims the coming judgment as unique in both directions, "
  "unprecedented and never to be repeated. Then the specific it is illustrated with, the fathers "
  "shall eat the sons in the midst of thee, and the sons shall eat their fathers. That is not "
  "invented rhetoric. It is the covenant curse written out in Leviticus 26 and Deuteronomy 28, "
  "quoted back as a thing about to happen."),
 ("Pestilence, Sword and Wind (vv.11-12)",
  "The oath formula, as I live, saith the Lord GOD, and the ground of it stated as a specific "
  "offence, because thou hast defiled my sanctuary with all thy detestable things. Then the three "
  "portions of hair are decoded: a third shall die with the pestilence and with famine, a third "
  "shall fall by the sword round about thee, and a third I will scatter into all the winds. And the "
  "scattering is not an escape, and I will draw out a sword after them."),
 ("My Fury Accomplished, and My Comfort Taken (vv.13-17)",
  "Thus shall mine anger be accomplished, and I will be comforted, which is language borrowed from "
  "consolation and used of judgment, and it is one of the hardest turns in the book. What Jerusalem "
  "becomes is described in terms of how she will be seen, a reproach and a taunt, an instruction and "
  "an astonishment unto the nations that are round about. Then famine, evil beasts, pestilence and "
  "blood, four agents named in a row. The section closes on the refrain that will end dozens of "
  "oracles from here on, and they shall know that I the LORD have spoken it."),
],
"ezekiel6": [
 ("The Oracle Addressed to the Mountains (vv.1-2)",
  "Set thy face toward the mountains of Israel, and prophesy against them. Addressing terrain rather "
  "than people is a way of naming the problem without naming a town: the high places were on "
  "hilltops, so an oracle against the mountains is an oracle against the shrines on them. The book "
  "uses this device repeatedly, and later turns it around, since chapter 36 is addressed to the same "
  "mountains with the opposite message."),
 ("The High Places Broken, and the Bones Scattered (vv.3-7)",
  "I will destroy your high places, and your altars shall be desolate, and your images shall be "
  "broken. Then the part that goes beyond demolition, and I will cast down your slain men before "
  "your idols, and I will lay the dead carcases of the children of Israel before their idols, and I "
  "will scatter your bones round about your altars. The desecration is deliberate and it is "
  "irreversible: a shrine with human remains in it cannot be used again, so the worshippers are "
  "made into the thing that ruins the place they worshipped at. And ye shall know that I am the "
  "LORD."),
 ("A Remnant That Will Loathe Itself (vv.8-10)",
  "Yet will I leave a remnant, that ye may have some that shall escape the sword among the nations. "
  "What that remnant does is described in an order worth noticing. First they remember me among the "
  "nations whither they shall be carried captives. Then they shall loathe themselves for the evils "
  "which they have committed in all their abominations. In this book recognition and self-disgust "
  "come before anything that could be called repentance, and the sequence is stated the same way "
  "again at 20:43 and 36:31."),
 ("The Gesture, and the Slain Among Their Idols (vv.11-14)",
  "Smite with thine hand, and stamp with thy foot, and say, Alas. The gesture belongs to grief and "
  "to derision both, and the text does not separate them. Sword, famine and pestilence again, and "
  "then a survey of where the bodies will be found which doubles as a list of where the worship "
  "happened: upon every high hill, in all the tops of the mountains, under every green tree, and "
  "under every thick oak. The oracle closes by measuring the desolation geographically, from the "
  "wilderness toward Diblath, and then they shall know that I am the LORD."),
],
"ezekiel7": [
 ("An End Upon the Four Corners of the Land (vv.1-4)",
  "The word this chapter is built on is the end, and it is repeated until it stops being an "
  "announcement and becomes a sound. An end, the end is come upon the four corners of the land. Now "
  "is the end come upon thee. What follows is judgment described as accounting, I will judge thee "
  "according to thy ways, and will recompense upon thee all thine abominations, with the withdrawal "
  "stated twice, mine eye shall not spare thee, neither will I have pity."),
 ("An Evil, an Only Evil (vv.5-9)",
  "This block says the same thing as the last one with small variations, an evil, an only evil, "
  "behold, it is come. That is how the chapter works. It does not develop an argument, it repeats "
  "one with the intervals shortening, which is a formal imitation of what it describes. The day of "
  "trouble is near, and not the sounding again of the mountains, that is, not the echo of a shout "
  "but the thing itself. And the refrain lands again, ye shall know that I am the LORD that "
  "smiteth."),
 ("The Rod Has Blossomed (vv.10-13)",
  "Behold the day, behold, it is come, the morning is gone forth, the rod hath blossomed, pride hath "
  "budded. Growing imagery used of a punishment is characteristic of this book. Then the practical "
  "consequence, and it is economic: let not the buyer rejoice, nor the seller mourn, because the "
  "seller shall not return to that which is sold. Land in Israel was inalienable in principle and "
  "reverted at the jubilee; the announcement here is that the machinery of property has stopped "
  "meaning anything, because there will be nobody to inherit."),
 ("The Trumpet Blown, and Nobody Goes (vv.14-18)",
  "They have blown the trumpet, and made ready, but none goeth to the battle, which is the most "
  "economical picture of collapse in the chapter: the alarm still works and the response does not. "
  "The sword is without and pestilence and famine within, so both leaving and staying are fatal. "
  "Those who escape to the mountains are compared to doves of the valleys, all of them mourning. "
  "The physical description that follows became standard prophetic shorthand, all hands shall be "
  "feeble, and all knees shall be weak as water, with sackcloth and baldness upon all heads."),
 ("Silver in the Streets (vv.19-22)",
  "They shall cast their silver in the streets, and their gold shall be removed, and the reason is "
  "given in terms of what money can and cannot buy, their silver and their gold shall not be able to "
  "deliver them in the day of the wrath of the LORD, they shall not satisfy their souls, neither "
  "fill their bowels. Then the aggravation, that the same metal had been the material of the idols, "
  "it is the stumblingblock of their iniquity. The section ends with the temple itself handed over, "
  "I will give it into the hands of strangers for a prey, and they shall pollute it."),
 ("The Chain, and the Collapse of Every Office (vv.23-27)",
  "Make a chain, for the land is full of bloody crimes, and the city is full of violence. Peace is "
  "specifically ruled out, they shall seek peace, and there shall be none, and rumour follows rumour "
  "and mischief follows mischief. The last verses take the society apart by function, which is the "
  "most complete such list in the prophets: the law shall perish from the priest, and counsel from "
  "the ancients, the king shall mourn, the prince shall be clothed with desolation, and the hands of "
  "the people of the land shall be troubled. Every office named is one that was supposed to hold "
  "things together."),
],
"ezekiel8": [
 ("Carried in Vision to Jerusalem (vv.1-4)",
  "The date is the sixth year, sixth month, fifth day, about fourteen months after the call, and the "
  "setting is domestic, the elders of Judah sat before me in mine house. What happens next is not "
  "domestic. A form with the appearance of fire puts out a hand and takes him by a lock of his head, "
  "and the spirit lifts him up in the visions of God to Jerusalem, to the door of the inner gate "
  "that looketh toward the north. The glory of the God of Israel is there, as he had seen it by the "
  "plain, which is the vision's way of saying that what he saw in Babylonia and what is in the "
  "temple are the same."),
 ("The Image of Jealousy at the Gate (vv.5-6)",
  "The tour is structured as four exhibits, and each one ends with the same escalation, turn thee "
  "yet again, and thou shalt see greater abominations. The first is an image standing northward at "
  "the gate of the altar. The question put to the prophet is not about the object but about the "
  "consequence, seest thou what they do, even the great abominations that the house of Israel "
  "committeth here, that I should go far off from my sanctuary. The departure of chapters 9 to 11 is "
  "announced here as a response, not as an abandonment."),
 ("The Chamber of Imagery, and the Seventy Elders (vv.7-13)",
  "A hole in the wall, an instruction to dig, a door, and behind it a room with every form of "
  "creeping thing and abominable beast portrayed upon the wall round about. Seventy of the ancients "
  "of the house of Israel are inside with censers, and one of them is named, Jaazaniah the son of "
  "Shaphan, from a family that had served Josiah's reform. What they say while they do it is the "
  "sentence the entire vision is answering, the LORD seeth us not, the LORD hath forsaken the earth. "
  "The private conviction underneath the private worship is that God has already left."),
 ("The Women Weeping for Tammuz (vv.14-15)",
  "At the door of the north gate, women sitting and weeping for Tammuz. Tammuz was a Mesopotamian "
  "god whose annual death was mourned with ritual weeping and whose return was celebrated with the "
  "coming of the growing season. What is being described is not a lapse but a foreign liturgical "
  "calendar being kept, on schedule, inside the temple precinct."),
 ("Sun Worship with Their Backs to the Temple (vv.16-18)",
  "The fourth exhibit is the worst and the reason is geography. Between the porch and the altar, "
  "which is the most sacred standing ground in the courts, five and twenty men with their backs "
  "toward the temple of the LORD and their faces toward the east, worshipping the sun. They are in "
  "the holiest available position, facing away from it. The response is stated in the terms the tour "
  "has been building toward, therefore will I also deal in fury, mine eye shall not spare, neither "
  "will I have pity, and though they cry in mine ears with a loud voice, yet will I not hear them."),
],
"ezekiel9": [
 ("Six Men with Slaughter Weapons (vv.1-2)",
  "A loud voice gives an order to unnamed hearers, cause them that have charge over the city to draw "
  "near, and six men come from the way of the higher gate which lieth toward the north, every man "
  "with a slaughter weapon in his hand. With them is a seventh, clothed with linen, which is "
  "priestly dress, and carrying a writer's inkhorn by his side. The instrument that distinguishes "
  "him from the other six is a pen."),
 ("The Glory at the Threshold, and the Mark on the Foreheads (vv.3-4)",
  "The glory of the God of Israel goes up from the cherub whereupon he was, to the threshold of the "
  "house, and that movement is the first stage of a departure completed in chapter 11. The order to "
  "the man with the inkhorn is to go through the midst of the city and set a mark upon the foreheads "
  "of the men that sigh and that cry for all the abominations that be done in the midst thereof. The "
  "people spared are identified by grief rather than by conduct. The Hebrew word for the mark is "
  "taw, the last letter of the alphabet, written in that period as a cross, and Revelation 7 takes "
  "up the same idea of sealing foreheads before judgment."),
 ("The Slaughter, Beginning at the Sanctuary (vv.5-7)",
  "The instruction to the six is the hardest set of clauses in the book: go after him through the "
  "city, and smite, let not your eye spare, neither have ye pity, slay utterly old and young, both "
  "maids, and little children, and women, with the one exception, but come not near any man upon "
  "whom is the mark. And then the place to start, and begin at my sanctuary. The narration confirms "
  "that they did, then they began at the ancient men which were before the house, which are the "
  "seventy of the previous chapter. Judgment beginning with the people responsible for worship is "
  "the principle 1 Peter 4:17 restates."),
 ("Ezekiel's Protest, and the Answer (vv.8-11)",
  "He falls on his face and intercedes, Ah Lord GOD, wilt thou destroy all the residue of Israel in "
  "thy pouring out of thy fury upon Jerusalem. It is the second time he objects in the book and he "
  "gets no comfort. The answer restates the charge, the iniquity of the house of Israel and Judah is "
  "exceeding great, and the land is full of blood, and the city full of perverseness, and quotes the "
  "elders' own sentence back as the reason, for they say, The LORD hath forsaken the earth, and the "
  "LORD seeth not. The chapter ends with the man in linen filing a report in nine words, I have done "
  "as thou hast commanded me."),
],
"ezekiel10": [
 ("Coals of Fire Taken from Between the Cherubim (vv.1-8)",
  "The firmament and the sapphire throne are described again, and then the man clothed with linen is "
  "sent between the wheels to fill his hand with coals of fire from between the cherubims and "
  "scatter them over the city. The provenance of the fire is the point: what will burn Jerusalem is "
  "taken from under the throne. The transfer is described physically, one cherub stretched forth his "
  "hand from between the cherubims and put it into the hands of him that was clothed with linen. "
  "Meanwhile the cloud filled the inner court, and the court was full of the brightness of the "
  "LORD's glory."),
 ("The Wheels, the Faces and the Eyes (vv.9-14)",
  "The apparatus is inventoried a second time, four wheels the colour of a beryl stone, a wheel in "
  "the middle of a wheel, going without turning, and their whole body, their backs, their hands, "
  "their wings and the wheels themselves full of eyes round about. The faces are listed again with "
  "one change: where chapter 1 had an ox, this has the face of a cherub. That is the vision "
  "correcting or clarifying itself, and it is the closest the Old Testament comes to telling us what "
  "a cherub's face looked like, by saying it was the one he had earlier called an ox."),
 ("The Same Creatures He Saw by Chebar (vv.15-17)",
  "This is stated twice in three verses, and it is doing real work. The prophet is telling readers "
  "that the throne apparatus now leaving the temple in Jerusalem is the same one that appeared to "
  "him over an irrigation canal in Babylonia, which means the vision in chapter 1 was not a "
  "consolation prize for a man far from the sanctuary. The connection between the creatures and the "
  "wheels is repeated for the same reason, when they stood, these stood, and when they were lifted "
  "up, these lifted up themselves also, for the spirit of the living creature was in them."),
 ("The Glory Goes to the East Gate (vv.18-22)",
  "Then the glory of the LORD departed from off the threshold of the house, and stood over the "
  "cherubims. They mount up from the earth in his sight and stop at the door of the east gate of the "
  "LORD's house. That is the second of the three stages, from the inner sanctuary to the threshold in "
  "chapter 9, to the east gate here, to the mountain outside the city in chapter 11. Nothing has "
  "been demolished at this point in the vision. The building is intact and it is empty, and the "
  "order of those two facts is the argument of the whole section."),
],
"ezekiel11": [
 ("The Five and Twenty Men at the East Gate (vv.1-4)",
  "The spirit brings him to the east gate, where five and twenty men are standing, and two are "
  "named, Jaazaniah the son of Azur and Pelatiah the son of Benaiah, described as princes of the "
  "people. Their slogan is quoted, and it is a piece of political theology in two clauses: it is not "
  "near, let us build houses, that is, the danger is exaggerated and normal life should continue; "
  "and this city is the caldron, and we be the flesh, that is, we are the valuable contents and the "
  "walls will hold. The implication for those already deported is that they were the scraps thrown "
  "out."),
 ("The Caldron Turned Around (vv.5-12)",
  "The reply takes the image and inverts it clause by clause. Your slain are the flesh in the midst "
  "of it, and it is the dead who are inside the pot; ye shall be brought forth out of the midst of "
  "it, so being taken out of the city is the judgment rather than the escape. I will deliver you "
  "into the hands of strangers, and ye shall fall by the sword. And the location is specified, I "
  "will judge you in the border of Israel, which is what happened: 2 Kings 25 records Zedekiah's "
  "officers being taken to Riblah, on the northern border, and executed there."),
 ("Pelatiah Dies, and Ezekiel Cries Out (v.13)",
  "One verse, and it is the sharpest interruption in the book. One of the two men named in verse 1 "
  "falls dead while Ezekiel is watching in vision, and the prophet's reaction is intercession again, "
  "then fell I down upon my face, and cried with a loud voice, and said, Ah Lord GOD, wilt thou make "
  "a full end of the remnant of Israel. It is the third time he has asked a version of this "
  "question, and this time the answer that follows is the most hopeful thing he has yet heard."),
 ("A Little Sanctuary in the Countries (vv.14-16)",
  "The answer begins by quoting what the people in Jerusalem have been saying about the deportees, "
  "get you far from the LORD, unto us is this land given in possession, which treats distance from "
  "the temple as distance from God and possession of the land as proof of favour. Both halves are "
  "then contradicted. Although I have cast them far off among the heathen, yet will I be to them a "
  "little sanctuary in the countries where they shall come. For a readership with no temple, no "
  "altar and no festivals, this is the single most consequential sentence in the first half of the "
  "book: the sanctuary is relocated to the people rather than the people to the sanctuary."),
 ("A New Heart and a New Spirit (vv.17-21)",
  "The promise runs in three stages, gathering, return, and possession of the land of Israel, and "
  "then turns inward for the part that makes the rest work. I will give them one heart, and I will "
  "put a new spirit within you, and I will take the stony heart out of their flesh, and will give "
  "them an heart of flesh, that they may walk in my statutes. Obedience is described as something "
  "produced rather than demanded, which is the difference between this and every warning in the "
  "preceding chapters. The same promise is made at greater length at 36:26. The section closes with "
  "the alternative left standing, but as for them whose heart walketh after their detestable things, "
  "I will recompense their way upon their own heads."),
 ("The Glory Departs to the Mountain on the East (vv.22-25)",
  "The cherubims lift up their wings, with the wheels beside them and the glory of the God of Israel "
  "over them above, and then the sentence the last three chapters have been moving toward, and the "
  "glory of the LORD went up from the midst of the city, and stood upon the mountain which is on the "
  "east side of the city. That is the mount of Olives, and the vision ends with the presence "
  "outside the walls looking back at them. Then the spirit takes Ezekiel back to the captivity, and "
  "the last verse is the only thing he does with any of it, then I spake unto them of the captivity "
  "all the things that the LORD had shewed me."),
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
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if not keep:
            problems.append(f"{page}: no book fields found to preserve")
            continue
        for i, (label, body) in enumerate(keep):
            for old, new in REPAIRS.get(page, []):
                if old in body:
                    keep[i][1] = body = body.replace(old, new)
                    notes.append(f"{page}: repaired {old!r} in {label}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        notes.append(f"{page}: kept {len(keep)} book field(s), dropped the sublist")
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
