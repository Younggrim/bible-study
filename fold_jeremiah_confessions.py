#!/usr/bin/env python3
"""
Jeremiah 11 to 20: the covenant, the sign-acts, and the confessions. Ten pages,
214 verses. All ten sublists are gapless outlines and are folded.

This block contains the passages usually called Jeremiah's confessions, at 11:18-23,
12:1-6, 15:10-21, 17:14-18, 18:19-23 and 20:7-18, and they are the reason this book
reads differently from every other prophet. The sections do not tidy them. At 15:18
he compares God to a wadi that runs in the wet season and is dry when needed. At
18:21 he asks that his neighbours' children be given to famine. At 20:7 he says he
was deceived, and six verses after a hymn of praise he curses the day he was born.

The arrangement is the argument. The editor put the birth-curse immediately after the
praise with no attempt to reconcile them, so the book does not present faith as a
line that goes upward. A note that smoothed that out would be describing a different
book.

Chapters 18 and 19 are a matched pair worth reading together: wet clay on the wheel
can be made again, and a fired pot cannot.

Usage:
    python3 fold_jeremiah_confessions.py [--check]
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
"jeremiah11": [
 ("The Words of This Covenant (vv.1-5)",
  "Hear ye the words of this covenant, and the word covenant is used five times in five verses. The "
  "structure is a document with a curse attached to it, cursed be the man that obeyeth not the words "
  "of this covenant, and the promise on the other side is the standard formula, so shall ye be my "
  "people, and I will be your God. That shape is Deuteronomy's shape, and many read this chapter "
  "against Josiah's discovery of the book of the law in 622 BC, five years after Jeremiah's call. On "
  "that reading he is being sent to promote a covenant renewal that has already been held, and the "
  "rest of the chapter reports how little it changed. His own reply is two words, so be it, O LORD."),
 ("Proclaim These Words (vv.6-8)",
  "Proclaim all these words in the cities of Judah, and in the streets of Jerusalem. What follows is "
  "the pattern this book states over and over, and the detail that carries it is the diligence of the "
  "sending, I earnestly protested unto your fathers in the day that I brought them up out of the land "
  "of Egypt, rising early and protesting. Then the outcome, yet they obeyed not, nor inclined their "
  "ear, but walked every one in the imagination of their evil heart."),
 ("A Conspiracy Among the Men of Judah (vv.9-13)",
  "A conspiracy is found among the men of Judah, and the word is worth pausing on: apostasy is being "
  "described as an organised undertaking rather than a drift. They are turned back to the iniquities "
  "of their fathers. Then the count from chapter 2 repeated exactly, according to the number of thy "
  "cities are thy gods, O Judah, which works out at one shrine per town. And the door closed, though "
  "they shall cry unto me, I will not hearken unto them."),
 ("Pray Not for This People (vv.14-17)",
  "The second of the three prohibitions, therefore pray not thou for this people, neither lift up a "
  "cry or prayer for them, for I will not hear them in the time that they cry unto me for their "
  "trouble. Then an image chosen for its value, the LORD called thy name a green olive tree, fair, "
  "and of goodly fruit, with the fire kindled upon it and the branches broken. An olive was the "
  "longest-lived and most valuable tree a family owned, took a generation to come into full bearing, "
  "and could not be quickly replaced, which is exactly why it is the tree in the picture."),
 ("The Plot from Anathoth (vv.18-23)",
  "The first of the confessions. It begins with the prophet learning something he had not seen coming, "
  "the LORD gave me knowledge of it, and I knew it, and thou shewedst me their doings, but I was like "
  "a lamb or an ox that is brought to the slaughter, and I knew not that they had devised devices "
  "against me. The men doing it are from his own town, the men of Anathoth, saying, Let us cut him off "
  "from the land of the living, that his name may be no more remembered. His response is a request "
  "for vengeance, let me see thy vengeance on them, for unto thee have I revealed my cause, and the "
  "answer granted is in the same terms. Whether a prophet ought to pray that way is a question this "
  "book raises repeatedly and never settles."),
],
"jeremiah12": [
 ("Why Does the Way of the Wicked Prosper (vv.1-4)",
  "The complaint is framed with care: he concedes the verdict before he files the objection, righteous "
  "art thou, O LORD, when I plead with thee, yet let me talk with thee of thy judgments, wherefore "
  "doth the way of the wicked prosper. What makes it sting is the horticultural language, which is "
  "God's own language in this book, thou hast planted them, yea, they have taken root, they grow, yea, "
  "they bring forth fruit. And the diagnosis, thou art near in their mouth, and far from their reins. "
  "The request is blunt, pull them out like sheep for the slaughter. Job and Psalm 73 ask the same "
  "question at greater length; this is the shortest and most personal version of it."),
 ("If Thou Hast Run with the Footmen (vv.5-6)",
  "The answer does not address the question, and the refusal to address it is the answer. If thou hast "
  "run with the footmen, and they wearied thee, then how wilt thou do when thou contendest with "
  "horses, and if in the land of peace, wherein thou trustedst, they wearied thee, then how wilt thou "
  "do in the swelling of Jordan. What is offered is not an explanation but notice that the conditions "
  "will get harder. Then a specific that makes the previous chapter worse, for even thy brethren, and "
  "the house of thy father, even they have dealt treacherously with thee. The plot at Anathoth "
  "included his family."),
 ("I Have Forsaken Mine Heritage (vv.7-13)",
  "The voice changes to God's and what it expresses is grief rather than anger, I have forsaken mine "
  "house, I have given the dearly beloved of my soul into the hand of her enemies. Then a sentence "
  "that is among the hardest in the book because of where it sits, mine heritage is unto me as a lion "
  "in the forest, it crieth out against me, therefore have I hated it. Hatred stated in the middle of "
  "a lament, about the same object. The land follows, they have made my pleasant portion a desolate "
  "wilderness, and the reason no one noticed is given as an aside that indicts everybody, because no "
  "man layeth it to heart."),
 ("Even the Neighbours May Be Restored (vv.14-17)",
  "Against all mine evil neighbours that touch the inheritance, behold, I will pluck them out of their "
  "land, and pluck out the house of Judah from among them. Then the reversal, and after that I will "
  "return, and have compassion on them, and will bring them again, every man to his heritage, which "
  "extends the promise past Israel to the nations doing the invading. The condition attached is a neat "
  "piece of symmetry, if they will diligently learn the ways of my people, to swear by my name, The "
  "LORD liveth, as they taught my people to swear by Baal, then shall they be built in the midst of my "
  "people. The nations that taught Israel one oath can be built up by learning another."),
],
"jeremiah13": [
 ("The Linen Girdle (vv.1-11)",
  "Go and get thee a linen girdle, and put it upon thy loins, and put it not in water. Then hide it in "
  "a hole of the rock, and after many days go back for it, and behold, the girdle was marred, it was "
  "profitable for nothing. The interpretation is about attachment, as the girdle cleaveth to the loins "
  "of a man, so have I caused to cleave unto me the whole house of Israel and the whole house of "
  "Judah, that they might be unto me for a people, and for a name, and for a praise, and for a glory, "
  "but they would not hear. Two details get discussed. Linen was priestly material. And the place is "
  "Perath, usually rendered Euphrates, which would mean two round trips of some seven hundred miles "
  "each; some read it instead as Parah, a village a few miles from Anathoth. The sign works either "
  "way, and the text does not resolve it."),
 ("Every Bottle Filled with Wine (vv.12-14)",
  "Thou shalt speak unto them this word, Every bottle shall be filled with wine. It sounds like a "
  "harvest blessing and it is quoted at them as a saying they will recognise, along with their "
  "anticipated reply, do we not certainly know that. The interpretation turns it inside out, I will "
  "fill all the inhabitants of this land with drunkenness, and I will dash them one against another, "
  "even the fathers and the sons together, and the closing triplet leaves no exemption, I will not "
  "pity, nor spare, nor have mercy."),
 ("Give Glory Before the Darkness (vv.15-17)",
  "Hear ye, and give ear, be not proud, for the LORD hath spoken. What is asked is put as a matter of "
  "timing, give glory to the LORD your God, before he cause darkness, and before your feet stumble "
  "upon the dark mountains. Then a private note in the middle of a public oracle, but if ye will not "
  "hear it, my soul shall weep in secret places for your pride, and mine eye shall weep sore, and run "
  "down with tears, because the LORD's flock is carried away captive. The tears are described as "
  "hidden, which is worth noticing in a book where so much of the grief is performed in public."),
 ("To the King and the Queen Mother (vv.18-19)",
  "Say unto the king and to the queen, Humble yourselves, sit down, for your principalities shall come "
  "down, even the crown of your glory. The queen here is the queen mother, which in Judah was an "
  "office with real standing rather than a courtesy, and the pair is generally identified as Jehoiachin "
  "and Nehushta, who were deported together in 597 BC as 2 Kings 24 records. Two verses, addressed to "
  "the only two people still in a position to change the outcome."),
 ("Can the Ethiopian Change His Skin (vv.20-27)",
  "Lift up your eyes, and behold them that come from the north, where is the flock that was given "
  "thee, thy beautiful flock. Then the question the chapter is known by, can the Ethiopian change his "
  "skin, or the leopard his spots, then may ye also do good, that are accustomed to do evil. The "
  "operative word is accustomed: what is described is not a nature but a habit so practised that it "
  "has become as fixed as colouring. The chapter ends in the vocabulary of public shaming, therefore "
  "will I discover thy skirts upon thy face, that thy shame may appear, and then a last question that "
  "is left open, wilt thou not be made clean, when shall it once be."),
],
"jeremiah14": [
 ("The Dearth (vv.1-6)",
  "Judah mourneth, and the gates thereof languish, they are black unto the ground. The drought is "
  "described from the ground up and in working detail: the nobles sent their servants to the pits and "
  "they came back with empty vessels and covered heads, the ground is chapt, for there was no rain in "
  "the earth, the ploughmen are ashamed. Then the animals, which is where the section lands its "
  "weight, because the hind calved in the field and forsook it, and the wild asses did stand in the "
  "high places, and did snuff up the wind, their eyes did fail, because there was no grass. Animals "
  "make no rhetorical case and do not exaggerate, which is why they are the measure here."),
 ("The First Intercession (vv.7-9)",
  "Though our iniquities testify against us, do thou it for thy name's sake, for our backslidings are "
  "many, we have sinned against thee. The argument is from reputation rather than merit, which is what "
  "Moses argues at Sinai and what Ezekiel 36 makes the ground of the whole restoration. Then two "
  "images that come close to reproach, why shouldest thou be as a stranger in the land, and as a "
  "wayfaring man that turneth aside to tarry for a night, why shouldest thou be as a man astonied, as "
  "a mighty man that cannot save. And the plea it ends on, yet thou, O LORD, art in the midst of us, "
  "and we are called by thy name, leave us not."),
 ("The First Refusal (vv.10-12)",
  "The prayer is refused and a reason is given, thus have they loved to wander, therefore the LORD "
  "doth not accept them. Then the third and last of the prohibitions, pray not thou for this people "
  "for their good. What follows closes the two channels that were left, when they fast, I will not "
  "hear their cry, and when they offer burnt offering and an oblation, I will not accept them. Fasting "
  "and sacrifice both named and both ruled out."),
 ("The Prophets Who Said Ye Shall Not See the Sword (vv.13-16)",
  "Then said I, Ah, Lord GOD, behold, the prophets say unto them, Ye shall not see the sword, neither "
  "shall ye have famine. It is an attempt to excuse the people by blaming their teachers, and the "
  "answer accepts the fact and refuses the excuse. The prophets prophesy lies in my name, I sent them "
  "not, and they shall be consumed by sword and famine. And then the people they taught, in the same "
  "sentence, shall be cast out in the streets of Jerusalem, they and their wives and their sons and "
  "their daughters. Being misled is not treated as a defence."),
 ("Mine Eyes Run Down with Tears (vv.17-18)",
  "The daughter of my people is broken with a great breach, with a very grievous blow. Then two "
  "clauses that describe a man with nowhere to stand, if I go forth into the field, then behold the "
  "slain with the sword, and if I enter into the city, then behold them that are sick with famine. "
  "Outside the walls and inside them, the same result by two different routes."),
 ("The Second Intercession (vv.19-22)",
  "Hast thou utterly rejected Judah, hath thy soul lothed Zion, why hast thou smitten us, and there is "
  "no healing for us. This time the confession is complete, we acknowledge, O LORD, our wickedness, and "
  "the iniquity of our fathers, for we have sinned against thee. Then the appeal moves to what God has "
  "at stake, do not disgrace the throne of thy glory, remember, break not thy covenant with us. And "
  "the closing argument is meteorological, are there any among the vanities of the Gentiles that can "
  "cause rain, art not thou he, O LORD our God, therefore we will wait upon thee. It is the best "
  "prayer in the book, and the first four verses of chapter 15 are the answer to it."),
],
"jeremiah15": [
 ("Though Moses and Samuel Stood Before Me (vv.1-4)",
  "Then said the LORD unto me, Though Moses and Samuel stood before me, yet my mind could not be "
  "toward this people. The two men named are the two great intercessors of the history, Moses at Sinai "
  "and Samuel at Mizpah, and both are declared insufficient here; Ezekiel makes the identical argument "
  "with Noah, Daniel and Job at 14:14. Then four kinds appointed, the sword to slay, the dogs to tear, "
  "the fowls of the heaven and the beasts of the earth to devour. And the cause is pinned to one "
  "reign, sixty years earlier, because of Manasseh the son of Hezekiah king of Judah, for that which "
  "he did in Jerusalem."),
 ("Who Shall Go Aside to Ask How Thou Doest (vv.5-9)",
  "For who shall have pity upon thee, O Jerusalem, or who shall go aside to ask how thou doest. It is "
  "the picture of a city nobody stops for, and it is a quieter kind of judgment than the sword. Thou "
  "hast forsaken me, therefore will I stretch out my hand against thee, and then a clause that is "
  "startling in the middle of it, I am weary with repenting. The losses are counted household by "
  "household, and the closing figure reverses the greatest blessing available to a woman in that "
  "culture, she that hath borne seven languisheth, she hath given up the ghost."),
 ("Woe Is Me, My Mother (vv.10-14)",
  "Woe is me, my mother, that thou hast borne me a man of strife and a man of contention to the whole "
  "earth. The grievance that follows is financial and precise, I have neither lent upon usury, nor men "
  "have lent to me on usury, yet every one of them doth curse me. He has stayed clear of the one "
  "transaction that reliably makes enemies in a village and is hated anyway, so the hostility has "
  "nothing to do with his conduct. The reply promises endurance rather than relief, and ends on the "
  "exile, I will make thee to pass with thine enemies into a land which thou knowest not."),
 ("A Deceitful Brook (vv.15-18)",
  "The sharpest of the confessions, and it is built as a legal brief. First the record, thy words were "
  "found, and I did eat them, and thy word was unto me the joy and rejoicing of mine heart. Then the "
  "cost, I sat not in the assembly of the mockers, nor rejoiced, I sat alone because of thy hand. Then "
  "the accusation, why is my pain perpetual, and my wound incurable, which refuseth to be healed, wilt "
  "thou be altogether unto me as a liar, and as waters that fail. In that climate a wadi that runs "
  "after rain and is dry when you actually need it is the most damaging comparison available, and he "
  "applies it to God."),
 ("If Thou Return, Then Will I Bring Thee Again (vv.19-21)",
  "The answer is a rebuke and a restoration in one sentence, if thou return, then will I bring thee "
  "again, and thou shalt stand before me. A condition is attached to the office itself, and if thou "
  "take forth the precious from the vile, thou shalt be as my mouth. Then a clause that answers the "
  "loneliness of the complaint by refusing to relieve it, let them return unto thee, but return not "
  "thou unto them. And the promise of chapter 1 repeated word for word to a man who has just compared "
  "God to a dry streambed, I will make thee unto this people a fenced brasen wall, and they shall "
  "fight against thee, but they shall not prevail against thee."),
],
"jeremiah16": [
 ("Thou Shalt Not Take Thee a Wife (vv.1-4)",
  "Thou shalt not take thee a wife, neither shalt thou have sons or daughters in this place. Jeremiah "
  "is the only prophet forbidden to marry, and the reason given is not discipline but forecast, "
  "because the children would die, they shall die of a grievous death, they shall not be lamented, "
  "neither shall they be buried. In a society where a man's name continued only through his children "
  "this is a significant deprivation, and it is imposed as a sign. His own life is the sermon, which "
  "is the working method of this book."),
 ("Neither Go to Mourn (vv.5-7)",
  "Enter not into the house of mourning, neither go to lament nor bemoan them, for I have taken away "
  "my peace from this people. The prohibited customs are then listed, and it is their absence that "
  "carries the message: they shall not be buried, neither shall men lament for them, nor cut "
  "themselves, nor make themselves bald, nor give the cup of consolation to drink. Funerals are being "
  "cancelled in advance, and the prophet is made to stop attending them now so that people ask why."),
 ("Nor Go to Feast (vv.8-9)",
  "Thou shalt not go into the house of feasting, to sit with them to eat and to drink, and the reason "
  "again looks forward, behold, I will cause to cease out of this place the voice of mirth, and the "
  "voice of gladness, the voice of the bridegroom, and the voice of the bride. Taken with the two "
  "sections above it, he is barred from marriage, from funerals and from weddings, which in a small "
  "town is the whole of social life. The isolation he complains of at 15:17 turns out to have been "
  "imposed rather than chosen."),
 ("Wherefore Hath the LORD Pronounced This Evil (vv.10-13)",
  "The question the people will ask is supplied in advance, wherefore hath the LORD pronounced all "
  "this great evil against us, or what is our iniquity. The answer comes in two parts and the second "
  "is the one that closes the escape, because your fathers have forsaken me, and ye have done worse "
  "than your fathers. Then the sentence, and it reads the exile as getting exactly what was asked for, "
  "at scale, therefore will I cast you out of this land into a land that ye know not, and there shall "
  "ye serve other gods day and night."),
 ("A Greater Deliverance Than Egypt (vv.14-15)",
  "Two verses that reverse the direction of everything around them. The days come, saith the LORD, "
  "that it shall no more be said, The LORD liveth, that brought up the children of Israel out of the "
  "land of Egypt, but, The LORD liveth, that brought up the children of Israel from the land of the "
  "north. The exodus was the reference point of every oath, festival and creed in Israel's life, and "
  "what is said here is that it will be superseded as the standard example of rescue."),
 ("Fishers and Hunters (vv.16-18)",
  "I will send for many fishers, and they shall fish them, and after will I send for many hunters, and "
  "they shall hunt them from every mountain, and out of the holes of the rocks. Two methods in "
  "sequence, nets first for whatever can be taken in quantity and then tracking for whatever hid, so "
  "that nothing is left. And the reason the second method works, for mine eyes are upon all their "
  "ways, they are not hid from my face, neither is their iniquity hid from mine eyes."),
 ("The Nations Shall Come (vv.19-21)",
  "The voice changes to the prophet's and the horizon widens past Judah entirely, O LORD, my strength "
  "and my fortress, the Gentiles shall come unto thee from the ends of the earth, and shall say, "
  "Surely our fathers have inherited lies. The idol satire of chapter 10 is compressed into one line, "
  "shall a man make gods unto himself, and they are no gods. And the chapter closes on the outcome "
  "rather than the judgment, and they shall know that my name is The LORD."),
],
"jeremiah17": [
 ("Graven with a Pen of Iron (vv.1-4)",
  "The sin of Judah is written with a pen of iron, and with the point of a diamond, graven upon the "
  "table of their heart, and upon the horns of your altars. Two surfaces are named, one internal and "
  "one liturgical, and the tools are chosen for permanence: this is not written, it is cut. Then the "
  "sentence, I will give thy substance and all thy treasures to the spoil, and ye shall serve your "
  "enemies in the land which thou knowest not."),
 ("The Shrub and the Tree (vv.5-8)",
  "Cursed be the man that trusteth in man, and maketh flesh his arm, for he shall be like the heath in "
  "the desert, and shall not see when good cometh. Against it, blessed is the man that trusteth in the "
  "LORD, for he shall be as a tree planted by the waters, that spreadeth out her roots by the river, "
  "and shall not be careful in the year of drought. The point is that these could be the same plant. "
  "What differs is the water supply, which ties the passage to the broken cisterns of chapter 2 and to "
  "the failed brook of 15:18. Psalm 1 works the same pair of images the same way."),
 ("The Heart Is Deceitful (vv.9-10)",
  "The heart is deceitful above all things, and desperately wicked, who can know it. The verse is "
  "usually quoted by itself, and its answer is the next line, I the LORD search the heart, I try the "
  "reins, even to give every man according to his ways, and according to the fruit of his doings. The "
  "question is not left hanging as a piece of pessimism. It is asked and then answered, and the answer "
  "is that someone does know it."),
 ("The Partridge That Sitteth on Eggs (v.11)",
  "One verse, and the natural history behind it is no longer recoverable: as the partridge sitteth on "
  "eggs, and hatcheth them not, so he that getteth riches, and not by right, shall leave them in the "
  "midst of his days, and at his end shall be a fool. Whether the bird was believed to gather another "
  "bird's eggs or to abandon its own is disputed. The application is not, and the sting is in the last "
  "clause: not that he loses the money but that he is finally shown to have been a fool."),
 ("The Hope of Israel, and the Fountain (vv.12-13)",
  "A throne of glory, and then the pairing this book keeps returning to, O LORD, the hope of Israel, "
  "all that forsake thee shall be ashamed, because they have forsaken the LORD, the fountain of living "
  "waters. That last phrase is word for word the one at 2:13, so these two verses tie the middle of "
  "the book back to the charge it opened with, and they sit here as a hinge between the proverbs above "
  "and the confession below."),
 ("Heal Me, and Let Them Be Confounded (vv.14-18)",
  "Heal me, O LORD, and I shall be healed, save me, and I shall be saved, for thou art my praise. Then "
  "the taunt he is enduring, quoted directly, behold, they say unto me, Where is the word of the LORD, "
  "let it come now, which is what people say when a warning has been running for years and nothing has "
  "happened yet. His defence is his record, I have not hastened from being a pastor to follow thee, "
  "and his request is again for vengeance, let them be confounded, but let not me be confounded. The "
  "confessions do not grow more serene as the book proceeds."),
 ("The Sabbath Sermon in the Gate (vv.19-27)",
  "Stand in the gate of the children of the people, and the whole close of the chapter is one "
  "commandment, take heed that ye bear no burden on the sabbath day, neither carry forth a burden out "
  "of your houses. What is attached to it is out of all proportion to the size of the request: kings "
  "and princes sitting upon the throne of David, riding in chariots and on horses, and this city shall "
  "remain for ever. The alternative is the same size, then will I kindle a fire in the gates thereof, "
  "and it shall devour the palaces of Jerusalem, and it shall not be quenched. Sabbath is being "
  "treated as the visible test of whether any of the rest is real, which is the weight Ezekiel 20 "
  "gives it and the thing Nehemiah 13 finally acts on."),
],
"jeremiah18": [
 ("The Potter's House (vv.1-4)",
  "Arise, and go down to the potter's house, and there I will cause thee to hear my words. What he is "
  "sent to watch is a failure followed by a recovery, and the wording is exact, the vessel that he "
  "made of clay was marred in the hand of the potter, so he made it again another vessel, as seemed "
  "good to the potter to make it. The clay is not thrown out and it does not become something other "
  "than clay. It is made again."),
 ("As the Clay Is in the Potter's Hand (vv.5-10)",
  "Cannot I do with you as this potter, saith the LORD, behold, as the clay is in the potter's hand, so "
  "are ye in mine hand. The image is usually cited for unlimited freedom, and what the passage states "
  "is a rule with two symmetrical halves. If I speak concerning a nation to pluck up and to destroy "
  "it, if that nation turn from their evil, I will repent of the evil that I thought to do. And if I "
  "speak concerning a nation to build and to plant it, if it do evil, then I will repent of the good. "
  "The potter's freedom is exercised in response to the clay, which is why so few announcements in "
  "this book turn out to be final. Paul uses the same figure to a different end in Romans 9."),
 ("But They Said, There Is No Hope (vv.11-12)",
  "Behold, I frame evil against you, and devise a device against you, return ye now every one from his "
  "evil way. And the reply is the most complete refusal recorded in the book, but they said, There is "
  "no hope, for we will walk after our own devices. It is not a denial that the prophet is right. It "
  "is agreement, followed by indifference, which is harder to answer than argument."),
 ("Will a Man Leave the Snow of Lebanon (vv.13-17)",
  "Ask ye now among the heathen, who hath heard such things. The argument is once again from the "
  "reliability of natural things: will a man leave the snow of Lebanon, shall the cold flowing waters "
  "be forsaken, which is to say nobody walks away from a dependable spring. But my people hath "
  "forgotten me, and they have caused them to stumble from the ancient paths, to walk in paths, in a "
  "way not cast up, that is, off the made road. The sentence is stated as a withdrawal, I will shew "
  "them the back, and not the face, in the day of their calamity."),
 ("Come, and Let Us Devise Devices (v.18)",
  "One verse, and it turns the previous section's own word back on the prophet: then said they, Come, "
  "and let us devise devices against Jeremiah. Their confidence rests on the institutions being "
  "intact, for the law shall not perish from the priest, nor counsel from the wise, nor the word from "
  "the prophet, which is precisely the list Ezekiel 7:26 says is about to fail. And the weapon chosen "
  "is speech, let us smite him with the tongue."),
 ("The Hardest Prayer in the Book (vv.19-23)",
  "Hearken to me, O LORD, and hearken to the voice of them that contend with me. He opens with a claim "
  "that is fair on the evidence, remember that I stood before thee to speak good for them, to turn "
  "away thy wrath from them, since the book shows him doing exactly that three times and being "
  "forbidden three times. Then the petition, and nothing in it is held back: deliver up their children "
  "to the famine, let their wives be bereaved of their children, and be widows, let their men be put "
  "to death, forgive not their iniquity, neither blot out their sin from thy sight. This is the "
  "imprecation that troubles readers most, and the text offers no gloss to soften it. What it does "
  "instead is print it as it was prayed, by a man who had been told not to pray for these people at "
  "all."),
],
"jeremiah19": [
 ("Get a Potter's Earthen Bottle (vv.1-2a)",
  "Go and get a potter's earthen bottle, and take of the ancients of the people, and of the ancients "
  "of the priests. Bringing witnesses is part of the sign rather than a precaution: what is about to "
  "be done needs to be seen by the men who can report it officially. The destination is named "
  "precisely, go forth unto the valley of the son of Hinnom, which is by the entry of the east gate, "
  "the same valley as the temple sermon of chapter 7. The section stops in the middle of verse 2 "
  "because the proclamation begins there."),
 ("The Proclamation at Topheth (vv.2b-9)",
  "The charges are cumulative and each is specific: they have forsaken me, and have estranged this "
  "place, and have burned incense in it unto other gods, and have filled this place with the blood of "
  "innocents, and have built the high places of Baal, to burn their sons with fire. And again the "
  "clause that disowns the practice entirely, which I commanded not, nor spake it, neither came it "
  "into my mind. The sentence includes a renaming, this place shall no more be called Tophet, but the "
  "valley of slaughter, and the siege detail this book returns to twice more, I will cause them to eat "
  "the flesh of their sons and the flesh of their daughters."),
 ("Break the Bottle (vv.10-11)",
  "Then shalt thou break the bottle in the sight of the men that go with thee, and say, Even so will I "
  "break this people and this city, as a potter's vessel that cannot be made whole again. This is why "
  "the two chapters belong together. In the potter's house the marred clay was still on the wheel and "
  "was made again. A bottle has been through the kiln, and the difference between wet clay and fired "
  "pottery is the whole distance between chapter 18 and chapter 19. The sign is a statement about how "
  "late it has become."),
 ("The City Made Like Topheth (vv.12-13)",
  "Thus will I do unto this place, and even make this city as Tophet, and the houses of Jerusalem "
  "shall be defiled as the place of Tophet. What extends it from a valley to a city is named in the "
  "next clause, because of all the houses upon whose roofs they have burned incense unto all the host "
  "of heaven. Flat roofs were the ordinary place for household devotion, so the practice is being "
  "located in every home rather than at one shrine outside the walls."),
 ("Then Came Jeremiah from Topheth (vv.14-15)",
  "He walks back up from the valley, stands in the court of the LORD's house, and says the whole thing "
  "again to everyone, behold, I will bring upon this city and upon all her towns all the evil that I "
  "have pronounced against it, because they have hardened their necks, that they might not hear my "
  "words. Two verses, and their function is to set up what follows: the next thing that happens in the "
  "book is that the temple's chief officer has him beaten."),
],
"jeremiah20": [
 ("Pashur Smote Jeremiah, and Put Him in the Stocks (vv.1-2)",
  "Pashur the son of Immer the priest, who was also chief governor in the house of the LORD, heard "
  "that Jeremiah prophesied these things. The response is administrative and physical at once, then "
  "Pashur smote Jeremiah the prophet, and put him in the stocks that were in the high gate of "
  "Benjamin. The stocks held the body bent in a public place, so humiliation was as much the point as "
  "pain, and the whole thing is carried out by the temple's own senior official on temple premises "
  "against a man who had been preaching in its courts."),
 ("Thy Name Shall Be Magor-missabib (vv.3-6)",
  "On the morrow Pashur brought him forth out of the stocks, and the first thing the prophet does is "
  "rename him, the LORD hath not called thy name Pashur, but Magor-missabib, which the text glosses "
  "as terror round about. The sentence is personal and specific, thou shalt go to Babylon, and there "
  "thou shalt die, and shalt be buried there, thou, and all thy friends. And the charge attached is "
  "worth reading carefully, to whom thou hast prophesied lies. The chief officer of the temple is here "
  "accused of the same offence as the peace-prophets of chapter 14."),
 ("O LORD, Thou Hast Deceived Me (vv.7-10)",
  "The last and most quoted of the confessions, and its first word is strong enough that translators "
  "have rendered it several ways, from deceived to enticed to overpowered. O LORD, thou hast deceived "
  "me, and I was deceived, thou art stronger than I, and hast prevailed, I am in derision daily, every "
  "one mocketh me. Then the attempt to resign and the reason it failed, I said, I will not make "
  "mention of him, nor speak any more in his name, but his word was in mine heart as a burning fire "
  "shut up in my bones, and I was weary with forbearing, and I could not stay. And the detail that "
  "shows how the abuse had spread, the people around him have taken up his own nickname for Pashur "
  "and are using it of him, for I heard the defaming of many, fear on every side."),
 ("But the LORD Is with Me (vv.11-13)",
  "The same passage turns without a transition, but the LORD is with me as a mighty terrible one, "
  "therefore my persecutors shall stumble, and they shall not prevail. It ends in praise, sing unto "
  "the LORD, praise ye the LORD, for he hath delivered the soul of the poor from the hand of "
  "evildoers. A reader looking for a tidy resolution will take these three verses as the end of the "
  "matter, and the next five make that impossible."),
 ("Cursed Be the Day Wherein I Was Born (vv.14-18)",
  "Cursed be the day wherein I was born, let not the day wherein my mother bare me be blessed. He "
  "curses the man who carried the news of his birth to his father, and wishes he had been killed "
  "before delivery, wherefore came I forth out of the womb to see labour and sorrow, that my days "
  "should be consumed with shame. Job 3 does the same thing in almost the same words. What matters "
  "most here is the placement: the editor set this immediately after the hymn of verse 13 and made no "
  "attempt to reconcile them, so the book refuses to present faith as a line that only goes upward. "
  "It is also the last of the confessions. After chapter 20 Jeremiah stops arguing with God, and the "
  "book turns to the kings."),
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
                notes.append(f"{page}: dropped inherited item {label!r}, "
                             f"its content is folded into the sections")
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
