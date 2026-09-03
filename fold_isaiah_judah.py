#!/usr/bin/env python3
"""
Isaiah 1 to 12: the lawsuit, the vineyard, the call, and Immanuel. Twelve pages,
252 verses.

Eleven of the twelve carry gapless outlines and are folded. isaiah6 has no sublist at
all, so its four sections are written from scratch, divided where the chapter divides:
the throne, the coal, the commission, and the question about duration.

The labels on isaiah5 are restyled more than most. The inherited outline numbered the
six woes with a hash symbol, Woe #1 through Woe #6, which no other page in the corpus
does, so they are rewritten to name what each woe is about.

Two passages in this block get a stated difficulty rather than a resolution. At 7:14
the Hebrew almah means a young woman of marriageable age, the Septuagint rendered it
parthenos, specifically a virgin, and Matthew 1 quotes the Greek; the section says both
things and also says what the sign did in its own setting, which was to function as a
clock. And at 10:5-7 Assyria is called the rod of mine anger and then said to mean not
so, neither doth his heart think so, which is the same knot Jeremiah 51:20-26 ties and
neither book unties.

Usage:
    python3 fold_isaiah_judah.py [--check]
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
"isaiah1": [
 ("Hear, O Heavens (vv.1-2)",
  "The vision of Isaiah the son of Amoz, which he saw concerning Judah and Jerusalem in the days of "
  "Uzziah, Jotham, Ahaz, and Hezekiah. Four reigns, running from about 740 BC into the reign that "
  "faced Sennacherib. Then the oracle opens as a lawsuit, hear, O heavens, and give ear, O earth. "
  "Heaven and earth are summoned because they were the witnesses to the covenant in Deuteronomy 30 and "
  "32, so what is being convened is a covenant action with the original witnesses called. And the "
  "charge is domestic rather than legal, I have nourished and brought up children, and they have "
  "rebelled against me."),
 ("The Ox Knows His Owner (vv.3-4)",
  "The ox knoweth his owner, and the ass his master's crib, but Israel doth not know, my people doth "
  "not consider. The comparison is deliberately unflattering: two animals proverbial for dullness are "
  "credited with something Israel cannot manage. Then the verbs stack up, they have forsaken the LORD, "
  "they have provoked the Holy One of Israel unto anger, they are gone away backward. That title, the "
  "Holy One of Israel, occurs about twenty-five times in this book and scarcely anywhere else in "
  "scripture, and this is its first appearance."),
 ("From the Sole of the Foot to the Head (vv.5-9)",
  "The nation is described as a body beaten past the point where beating achieves anything, why should "
  "ye be stricken any more, ye will revolt more and more. From the sole of the foot even unto the head "
  "there is no soundness in it, but wounds, and bruises, and putrifying sores, they have not been "
  "closed, neither bound up, neither mollified with ointment. Then the same condition described "
  "geographically, your country is desolate, your cities are burned with fire, and Zion left as a "
  "cottage in a vineyard, a lodge in a garden of cucumbers, a besieged city. And the margin is named in "
  "the last verse, except the LORD of hosts had left unto us a very small remnant, we should have been "
  "as Sodom."),
 ("I Delight Not in the Blood of Bullocks (vv.10-15)",
  "To what purpose is the multitude of your sacrifices unto me, saith the LORD. What is refused is then "
  "itemised, and every item is something scripture elsewhere commands: burnt offerings, rams, the fat "
  "of fed beasts, the blood of bullocks, lambs and he goats, incense, new moons, sabbaths, the calling "
  "of assemblies, and the appointed feasts. Your new moons and your appointed feasts my soul hateth, "
  "they are a trouble unto me, I am weary to bear them. The reason is held back to the last verse and "
  "it is not about ritual at all, and when ye spread forth your hands, I will hide mine eyes from you, "
  "your hands are full of blood."),
 ("Wash You, Make You Clean (vv.16-20)",
  "What is asked instead is a list of actions, and every one of them is directed at another person: "
  "cease to do evil, learn to do well, seek judgment, relieve the oppressed, judge the fatherless, "
  "plead for the widow. Then the verse the chapter is best known for, come now, and let us reason "
  "together, saith the LORD, though your sins be as scarlet, they shall be as white as snow, though "
  "they be red like crimson, they shall be as wool. And the terms attached to it, if ye be willing and "
  "obedient, ye shall eat the good of the land, but if ye refuse and rebel, ye shall be devoured with "
  "the sword."),
 ("Thy Silver Is Become Dross (vv.21-23)",
  "How is the faithful city become an harlot, it was full of judgment, righteousness lodged in it, but "
  "now murderers. Then the metallurgy Ezekiel 22 also uses, thy silver is become dross, thy wine mixed "
  "with water, which describes adulteration rather than destruction: the substance is still there and "
  "has been thinned. And the charge against the officials is specific about the mechanism, thy princes "
  "are companions of thieves, every one loveth gifts, and followeth after rewards, they judge not the "
  "fatherless, neither doth the cause of the widow come unto them."),
 ("I Will Purely Purge Away Thy Dross (vv.24-31)",
  "The judgment continues the previous section's figure and turns it constructive, and I will turn my "
  "hand upon thee, and purely purge away thy dross, and take away all thy tin. What it is for is "
  "stated as a restoration of function, and I will restore thy judges as at the first, and thy "
  "counsellors as at the beginning, afterward thou shalt be called, The city of righteousness, the "
  "faithful city. Then a phrase that puts two words together which are usually opposed, Zion shall be "
  "redeemed with judgment. The chapter ends at the shrines, they shall be ashamed of the oaks which ye "
  "have desired, and ye shall be as an oak whose leaf fadeth, and the maker of it as a spark."),
],
"isaiah2": [
 ("The Mountain of the LORD's House (vv.1-4)",
  "It shall come to pass in the last days, that the mountain of the LORD's house shall be established "
  "in the top of the mountains, and all nations shall flow unto it. The movement is inward and "
  "voluntary, and what draws them is instruction rather than conquest, he will teach us of his ways, "
  "and we will walk in his paths. Then the sentence carved on the wall across from the United Nations "
  "in New York, they shall beat their swords into plowshares, and their spears into pruninghooks, "
  "nation shall not lift up sword against nation, neither shall they learn war any more. Micah 4 has "
  "the same passage almost word for word, and which prophet had it first cannot be determined."),
 ("Let Us Walk in the Light (v.5)",
  "One verse, and it is the hinge of the chapter. O house of Jacob, come ye, and let us walk in the "
  "light of the LORD. The nations in verse 3 had said let us go up to the mountain of the LORD, and "
  "here Israel is invited to do what the foreigners were pictured doing. Everything before this verse "
  "is the future and everything after it is the present, and the invitation sits at the join."),
 ("Full of the Customs of the East (vv.6-9)",
  "Therefore thou hast forsaken thy people the house of Jacob, because they are replenished from the "
  "east, and are soothsayers like the Philistines. Then a list built on one repeated phrase, and the "
  "repetition is the argument: their land is full of silver and gold, their land is full of horses and "
  "chariots, their land is also full of idols. Wealth, military capacity and religion counted as three "
  "instances of the same problem. And the section ends on a clause left deliberately unresolved, "
  "therefore forgive them not."),
 ("Enter into the Rock (vv.10-22)",
  "The rest of the chapter is one sustained passage about a day, and it works by stating a single idea "
  "and then repeating it with the subject changed: the lofty looks of man shall be humbled, and the "
  "LORD alone shall be exalted in that day. What is listed for levelling is everything tall or costly, "
  "the cedars of Lebanon, the oaks of Bashan, the high mountains, every high tower, every fenced wall, "
  "the ships of Tarshish, and all pleasant pictures. Then the idols are shown being got rid of in a "
  "hurry, in that day a man shall cast his idols of silver, which he made each one for himself to "
  "worship, to the moles and to the bats. And the chapter closes on one instruction with a reason "
  "attached, cease ye from man, whose breath is in his nostrils, for wherein is he to be accounted of."),
],
"isaiah3": [
 ("The Stay and the Staff (vv.1-3)",
  "The LORD doth take away from Jerusalem and from Judah the stay and the staff, and what follows is "
  "not an army but a personnel list: the mighty man, and the man of war, the judge, and the prophet, "
  "and the prudent, and the ancient, the captain of fifty, and the honourable man, and the counsellor, "
  "and the cunning artificer, and the eloquent orator. Nine categories, covering defence, law, "
  "religion, administration and the trades. The judgment described is the removal of competence rather "
  "than the arrival of an enemy."),
 ("Children Shall Rule (vv.4-7)",
  "And I will give children to be their princes, and babes shall rule over them, which follows from "
  "the list above rather than being an additional punishment. The collapse is then shown from inside, "
  "the people shall be oppressed, every one by his neighbour, the child shall behave himself proudly "
  "against the ancient. And there is a scene that makes the shortage concrete: a man is seized by his "
  "own relatives and told, thou hast clothing, be thou our ruler, and he refuses, I will not be an "
  "healer, for in my house is neither bread nor clothing. Owning a coat is the qualification, and even "
  "so nobody wants the job."),
 ("They Declare Their Sin as Sodom (vv.8-9)",
  "Jerusalem is ruined, and Judah is fallen, because their tongue and their doings are against the "
  "LORD. Then the aggravation, which is not the conduct but the openness of it, the shew of their "
  "countenance doth witness against them, and they declare their sin as Sodom, they hide it not. "
  "Shamelessness is treated as a charge in its own right, and it will be answered in the next chapter "
  "by a city that is called holy."),
 ("Say Ye to the Righteous (vv.10-11)",
  "Two verses of plain retribution set in the middle of a chapter about collapse, say ye to the "
  "righteous, that it shall be well with him, for they shall eat the fruit of their doings, woe unto "
  "the wicked, it shall be ill with him, for the reward of his hands shall be given him. The placement "
  "is the point. The disaster described on either side of these verses is not being presented as "
  "indiscriminate."),
 ("Ye Grind the Faces of the Poor (vv.12-15)",
  "As for my people, children are their oppressors, and women rule over them, O my people, they which "
  "lead thee cause thee to err. Then the courtroom of chapter 1 reconvenes, the LORD standeth up to "
  "plead, and standeth to judge the people, and the defendants are named, the ancients of his people, "
  "and the princes thereof. The charge is put as two questions and they are the sharpest lines in the "
  "chapter, what mean ye that ye beat my people to pieces, and grind the faces of the poor. And the "
  "stolen property is located, ye have eaten up the vineyard, the spoil of the poor is in your houses."),
 ("The Daughters of Zion (vv.16-26)",
  "Because the daughters of Zion are haughty, and walk with stretched forth necks and wanton eyes, "
  "walking and mincing as they go, and making a tinkling with their feet. What follows is the longest "
  "catalogue of clothing and jewellery in the Bible, twenty-one items across four verses, from the "
  "tinkling ornaments and the round tires like the moon to the crisping pins, the glasses, the hoods "
  "and the veils. Several of the words occur nowhere else and their exact sense is now guesswork. The "
  "reversal is then made item for item, instead of sweet smell there shall be stink, instead of a "
  "girdle a rent, instead of well set hair baldness, and burning instead of beauty. And the chapter "
  "ends with the city itself in that posture, and she being desolate shall sit upon the ground."),
],
"isaiah4": [
 ("Seven Women to One Man (v.1)",
  "And in that day seven women shall take hold of one man, saying, We will eat our own bread, and wear "
  "our own apparel, only let us be called by thy name, to take away our reproach. The verse belongs "
  "with the end of chapter 3 and is the demographic arithmetic of the war described there: the men are "
  "dead. Women offering to support themselves entirely in exchange for a nominal marriage is a picture "
  "of a society that has lost a generation of its young men, and it is stated without comment."),
 ("The Branch of the LORD (v.2)",
  "In that day shall the branch of the LORD be beautiful and glorious, and the fruit of the earth shall "
  "be excellent and comely for them that are escaped of Israel. The word here is tsemach, a growing "
  "shoot, and it is the term Jeremiah 23:5 and Zechariah 3:8 use as a messianic title. Whether this "
  "verse means a person or the land's produce is genuinely disputed, and the verse itself puts the "
  "phrase in parallel with the fruit of the earth, which allows either reading."),
 ("He That Is Left Shall Be Called Holy (v.3)",
  "And it shall come to pass, that he that is left in Zion, and he that remaineth in Jerusalem, shall "
  "be called holy, even every one that is written among the living in Jerusalem. Two things in one "
  "verse. The city that declared its sin as Sodom at 3:9 is now called holy. And the survivors are "
  "identified by a written register, which is the earliest form of the book of life imagery that runs "
  "through the Psalms, Daniel 12 and Revelation 20."),
 ("The Spirit of Judgment and of Burning (v.4)",
  "When the Lord shall have washed away the filth of the daughters of Zion, and shall have purged the "
  "blood of Jerusalem from the midst thereof, by the spirit of judgment, and by the spirit of burning. "
  "Two cleaning operations, one domestic and one industrial, and the agent of both is called spirit. "
  "What that does is make the judgment of chapter 3 the means of the holiness of verse 3, rather than "
  "an interruption of it."),
 ("A Cloud by Day, a Fire by Night (vv.5-6)",
  "And the LORD will create upon every dwelling place of mount Zion a cloud and smoke by day, and the "
  "shining of a flaming fire by night. The exodus pillar is being promised over every house rather than "
  "over one tent in the middle of the camp, so what had guided a nation is redistributed to domestic "
  "scale. And the last verse names its practical use rather than its glory, a tabernacle for a shadow "
  "in the daytime from the heat, and for a place of refuge, and for a covert from storm and from rain."),
],
"isaiah5": [
 ("The Song of the Vineyard (vv.1-7)",
  "Now will I sing to my wellbeloved a song of my beloved touching his vineyard. It opens as a love "
  "song and the audience would have settled in for one, which is the trap: they are asked to judge the "
  "case before they know it is about them, and now, O inhabitants of Jerusalem, and men of Judah, "
  "judge, I pray you, betwixt me and my vineyard. Every reasonable measure had been taken, he fenced "
  "it, and gathered out the stones thereof, and planted it with the choicest vine, and built a tower in "
  "the midst of it, and also made a winepress therein. And it brought forth wild grapes. The "
  "interpretation turns on a pun that only works in Hebrew: he looked for judgment, mishpat, and found "
  "oppression, mispach, for righteousness, tsedaqah, and found a cry, tseaqah. Jesus retells this "
  "parable in Matthew 21 with the tenants added."),
 ("Woe to Those Who Join House to House (vv.8-10)",
  "The first of six woes, and it concerns land, woe unto them that join house to house, that lay field "
  "to field, till there be no place, that they may be placed alone in the midst of the earth. Israel's "
  "land law existed to keep holdings in families, so consolidating estates was not merely acquisitive, "
  "it dismantled the system. The penalty is stated in yields, ten acres of vineyard shall yield one "
  "bath, and the seed of an homer shall yield an ephah, which is about a tenth of what was sown."),
 ("Woe to Those Who Rise Early for Drink (vv.11-17)",
  "Woe unto them that rise up early in the morning, that they may follow strong drink, that continue "
  "until night till wine inflame them. The charge is not the drinking by itself but the inattention "
  "that comes with it, and the harp, and the viol, the tabret, and pipe, and wine, are in their feasts, "
  "but they regard not the work of the LORD. And the consequence is put as an appetite of its own, "
  "therefore hell hath enlarged herself, and opened her mouth without measure."),
 ("Woe to Those Who Draw Iniquity with a Cord (vv.18-19)",
  "Woe unto them that draw iniquity with cords of vanity, and sin as it were with a cart rope, which "
  "is a picture of people hauling their own wrongdoing along behind them by main force. What condemns "
  "them is what they say, let him make speed, and hasten his work, that we may see it. That is a dare "
  "rather than a doubt, and it is the same taunt Jeremiah reports at 17:15."),
 ("Woe to Those Who Call Evil Good (v.20)",
  "One verse, and the most quoted in the chapter. Woe unto them that call evil good, and good evil, "
  "that put darkness for light, and light for darkness, that put bitter for sweet, and sweet for "
  "bitter. Three pairs, each reversed. What is described is not wrongdoing but the redefinition of the "
  "vocabulary, which is why it is placed in the middle of the list rather than at either end."),
 ("Woe to the Wise in Their Own Eyes (v.21)",
  "One verse, woe unto them that are wise in their own eyes, and prudent in their own sight. It is the "
  "same fault Proverbs 26:12 says leaves a man further from help than a fool, and its brevity here is "
  "part of the effect: there is nothing to add to it."),
 ("Woe to Those Who Justify the Wicked for Reward (vv.22-23)",
  "The last woe comes back to drink and joins it to the courts, woe unto them that are mighty to drink "
  "wine, and men of strength to mingle strong drink, which justify the wicked for reward, and take away "
  "the righteousness of the righteous from him. The two halves belong in one sentence on purpose: the "
  "men described as champions at the table are the men deciding cases."),
 ("He Will Hiss for Them (vv.24-30)",
  "The judgment is fire in dry stubble and a root that will not hold, because they have cast away the "
  "law of the LORD of hosts. Then the invader is summoned with a gesture borrowed from beekeeping, he "
  "will hiss unto them from the end of the earth, and behold, they shall come with speed swiftly. What "
  "follows reads like an inspection report on a professional army, none shall be weary nor stumble "
  "among them, none shall slumber nor sleep, neither shall the girdle of their loins be loosed, nor the "
  "latchet of their shoes be broken, their arrows sharp, and all their bows bent, their horses' hoofs "
  "like flint. And the chapter ends without relief, if one look unto the land, behold darkness and "
  "sorrow."),
],
"isaiah6": [
 ("In the Year That King Uzziah Died (vv.1-4)",
  "The date is a death and it is doing work. Uzziah had reigned fifty-two years, the longest and most "
  "prosperous reign since Solomon, and had died a leper excluded from the temple after carrying a "
  "censer into it, which 2 Chronicles 26 records. In the year the throne in Jerusalem emptied, Isaiah "
  "saw the LORD sitting upon a throne, high and lifted up, and his train filled the temple. The "
  "seraphims are described by what they do with their wings, with twain he covered his face, and with "
  "twain he covered his feet, and with twain he did fly, so four of the six are used for concealment. "
  "And the cry, Holy, holy, holy, is the LORD of hosts. Threefold repetition is the Hebrew superlative, "
  "and this is the only place in the Old Testament where it is applied to holiness."),
 ("Woe Is Me, for I Am Undone (vv.5-7)",
  "The reaction is not awe, it is collapse, woe is me, for I am undone, because I am a man of unclean "
  "lips, and I dwell in the midst of a people of unclean lips. What he names as the fault is the organ "
  "of his own trade, and he names his people in the same breath. The remedy is applied to the same "
  "place and it is not gentle: a live coal taken with the tongs from off the altar and laid on his "
  "mouth. Then two clauses which are the whole of the chapter's good news, and they are stated as "
  "already accomplished before anything is asked of him, lo, thine iniquity is taken away, and thy sin "
  "purged."),
 ("Whom Shall I Send (vv.8-10)",
  "The question is put in the plural, who will go for us, and the answer is volunteered rather than "
  "extracted, here am I, send me. Then the commission, which is the hardest given to any prophet: go, "
  "and tell this people, Hear ye indeed, but understand not, make the heart of this people fat, and "
  "make their ears heavy, and shut their eyes, lest they see with their eyes, and hear with their ears, "
  "and understand with their heart, and convert, and be healed. The preaching is described as producing "
  "the deafness. It is the most quoted commission in the New Testament, appearing in all four Gospels "
  "and in Acts 28 and Romans 11, and it is cited every time to explain why a hearing failed."),
 ("How Long, and the Holy Seed (vv.11-13)",
  "His only question is about duration, then said I, Lord, how long. The answer is until the cities are "
  "wasted without inhabitant, and even that is not the end of it, and it shall return, and shall be "
  "eaten, so a second stage follows the first. The image the chapter closes on is a felled tree, as a "
  "teil tree, and as an oak, whose substance is in them, when they cast their leaves. And the last "
  "clause is the only relief in the chapter, so the holy seed shall be the substance thereof. What "
  "remains after the felling is a stump with life in it, which is exactly where chapter 11 begins."),
],
"isaiah7": [
 ("The Syro-Ephraimite Alliance (vv.1-2)",
  "Rezin king of Syria and Pekah son of Remaliah, king of Israel, went up toward Jerusalem to war "
  "against it. The situation is 735 BC. Damascus and Samaria have allied against Assyria, they want "
  "Judah in the coalition, and verse 6 says they intend to replace Ahaz with a compliant king. The "
  "reaction in Jerusalem is reported physically rather than politically, his heart was moved, and the "
  "heart of his people, as the trees of the wood are moved with the wind."),
 ("Fear Not, Neither Be Fainthearted (vv.3-9)",
  "Isaiah is sent to meet the king at the end of the conduit of the upper pool, which means the king is "
  "inspecting the water supply against a siege. He is told to bring his son, and the son's name is part "
  "of the message: Shear-jashub means a remnant shall return. The two kings are dismissed as smoking "
  "firebrands and the coalition given a shelf life, within threescore and five years shall Ephraim be "
  "broken. And the chapter's key sentence is a wordplay on believing and standing firm that survives "
  "translation only roughly, if ye will not believe, surely ye shall not be established."),
 ("Ask Thee a Sign (vv.10-11)",
  "The LORD spake again unto Ahaz, saying, Ask thee a sign of the LORD thy God, ask it either in the "
  "depth, or in the height above. The offer has no limit and no condition on it, which is what makes "
  "the next verse remarkable. A king under military threat is invited to name any sign he likes."),
 ("I Will Not Ask (v.12)",
  "But Ahaz said, I will not ask, neither will I tempt the LORD. The refusal is dressed as piety and "
  "even quotes Deuteronomy 6:16. What 2 Kings 16 records him doing instead settles what it actually "
  "was: he sent the silver and gold of the temple to the king of Assyria and asked for help, and had a "
  "Damascene altar copied for the temple courts. He had already chosen a protector, and declining the "
  "sign was how he avoided being told so."),
 ("Behold, a Virgin Shall Conceive (vv.13-16)",
  "The sign is given anyway, therefore the Lord himself shall give you a sign, Behold, a virgin shall "
  "conceive, and bear a son, and shall call his name Immanuel. The Hebrew word is almah, a young woman "
  "of marriageable age; the Septuagint translators rendered it parthenos, which does mean virgin "
  "specifically, and Matthew 1:23 quotes that Greek of the birth of Jesus. What the sign does in its "
  "own setting is act as a clock, and the next verse says so, before the child shall know to refuse the "
  "evil and choose the good, the land that thou abhorrest shall be forsaken of both her kings. Damascus "
  "fell in 732 and Samaria in 722, so the sign was measurable inside a childhood."),
 ("Assyria as a Hired Razor (vv.17-25)",
  "The consequence of the choice Ahaz has already made, the LORD shall bring upon thee the king of "
  "Assyria. The images are domestic and humiliating rather than martial: the LORD shall hiss for the "
  "fly that is in Egypt and for the bee in Assyria, and in the same day shall the Lord shave with a "
  "razor that is hired, the head, and the hair of the feet, and shall also consume the beard. A hired "
  "razor is a foreign army on the payroll, which is precisely what the tribute bought. And the chapter "
  "ends with farmland reverting to scrub, a man keeping a cow and two sheep and living on curds and "
  "honey because the vineyards are gone, and all the hills become briers and thorns."),
],
"isaiah8": [
 ("Maher-shalal-hash-baz (vv.1-4)",
  "Take thee a great roll, and write in it with a man's pen, and what is written is a name, "
  "Maher-shalal-hash-baz, which means speed to the spoil, hasten to the prey. Two witnesses are named "
  "for the document, Uriah the priest and Zechariah the son of Jeberechiah, so the prophecy is "
  "notarised before the event it describes. Then the child is born and the timetable is attached to "
  "him, before the child shall have knowledge to cry, My father, and my mother, the riches of Damascus "
  "and the spoil of Samaria shall be taken away."),
 ("The Waters of Shiloah, and the Waters of the River (vv.5-8)",
  "Because this people refuseth the waters of Shiloah that go softly, and the contrast is hydraulic and "
  "local: Shiloah is Jerusalem's own quiet spring-fed channel, and the river is the Euphrates. Now "
  "therefore the Lord bringeth up upon them the waters of the river, strong and many, and the flood is "
  "measured against a body, he shall reach even to the neck. Then a phrase that lands strangely in the "
  "middle of a threat, and shall fill the breadth of thy land, O Immanuel. The name from the previous "
  "chapter is used here as the name of the country."),
 ("Take Counsel Together, and It Shall Come to Nought (vv.9-10)",
  "Associate yourselves, O ye people, and ye shall be broken in pieces, gird yourselves, and ye shall "
  "be broken in pieces. The reason is held to the end, take counsel together, and it shall come to "
  "nought, speak the word, and it shall not stand, for God is with us. That final clause is Immanuel "
  "translated into English, so the name appears for the third time in two chapters, and this time it "
  "functions as the argument rather than as a label."),
 ("Say Ye Not, A Confederacy (vv.11-13)",
  "The instruction is private and it is about resisting a mood rather than a policy, say ye not, A "
  "confederacy, to all them to whom this people shall say, A confederacy, neither fear ye their fear, "
  "nor be afraid. The word rendered confederacy is also the word for conspiracy, and what is being "
  "described is the standing panic of a small state convinced that everyone is plotting. The "
  "replacement is offered in the same vocabulary, sanctify the LORD of hosts himself, and let him be "
  "your fear, and let him be your dread."),
 ("A Stone of Stumbling (vv.14-15)",
  "And he shall be for a sanctuary, but for a stone of stumbling and for a rock of offence to both the "
  "houses of Israel. The same object is refuge and hazard, and which it is depends entirely on the "
  "approach. Paul quotes it in Romans 9 and Peter in 1 Peter 2, both of them applying it to Christ, and "
  "both keeping the double sense the verse has here."),
 ("Bind Up the Testimony (vv.16-18)",
  "Bind up the testimony, seal the law among my disciples, which is an instruction to archive rather "
  "than to broadcast. Then the most personal sentence in the chapter, and I will wait upon the LORD, "
  "that hideth his face from the house of Jacob, and I will look for him. Waiting on a God described in "
  "the same breath as hiding is the position the prophet takes once the king has stopped listening. And "
  "the last verse makes his household the message, behold, I and the children whom the LORD hath given "
  "me are for signs and for wonders in Israel, a verse Hebrews 2:13 quotes."),
 ("To the Law and to the Testimony (vv.19-22)",
  "And when they shall say unto you, Seek unto them that have familiar spirits, and unto wizards that "
  "peep, and that mutter. The reply is a question, should not a people seek unto their God, for the "
  "living to the dead. Then the standard, and it is a documentary one, to the law and to the testimony, "
  "if they speak not according to this word, it is because there is no light in them. The chapter ends "
  "in the dark rather than in the light, they shall pass through it, hardly bestead and hungry, and "
  "shall look unto the earth, and behold trouble and darkness."),
],
"isaiah9": [
 ("Light in Galilee (vv.1-2)",
  "The land of Zebulun and the land of Naphtali are named specifically, and they are named because that "
  "is the territory Assyria overran and deported first, so the darkest ground in the country. Beyond "
  "Jordan, in Galilee of the nations. The people that walked in darkness have seen a great light, they "
  "that dwell in the land of the shadow of death, upon them hath the light shined. Matthew 4 quotes "
  "these two verses of the beginning of Jesus' public ministry, which took place in exactly those "
  "districts and is the reason the quotation is more than decorative."),
 ("The Joy of Harvest, and the Burning of Boots (vv.3-5)",
  "Thou hast multiplied the nation, and increased the joy, and the measure is agricultural and military "
  "at once, they joy according to the joy in harvest, and as men rejoice when they divide the spoil. "
  "The yoke and the rod are broken as in the day of Midian, which is Gideon's victory in Judges 7, won "
  "with three hundred men and no battle worth the name. And the last verse describes demobilisation in "
  "physical terms, for every battle of the warrior is with confused noise, and garments rolled in "
  "blood, but this shall be with burning and fuel of fire. The uniforms are burned rather than stored "
  "for next time."),
 ("Unto Us a Child Is Born (vv.6-7)",
  "For unto us a child is born, unto us a son is given, and the government shall be upon his shoulder. "
  "The titles are stacked without conjunctions, Wonderful, Counsellor, The mighty God, The everlasting "
  "Father, The Prince of Peace, and whether the first two are one title or two has been argued since "
  "antiquity. The reign is described by two measures, of the increase of his government and peace there "
  "shall be no end, and it is located on a specific throne, upon the throne of David, and upon his "
  "kingdom, to order it, and to establish it with judgment and with justice from henceforth even for "
  "ever. The last clause is what keeps it from being a coronation hymn for a particular king, the zeal "
  "of the LORD of hosts will perform this."),
 ("The Bricks Are Fallen, We Will Build with Hewn Stones (vv.8-12)",
  "A new oracle begins here and runs through to 10:4 in four stanzas, each closing with the same "
  "refrain, for all this his anger is not turned away, but his hand is stretched out still. The first "
  "stanza quotes the northern kingdom's response to a disaster, and it is the most recognisable "
  "sentence in the chapter, the bricks are fallen down, but we will build with hewn stones, the "
  "sycomores are cut down, but we will change them into cedars. Rebuilding better, offered as a "
  "substitute for asking why the thing fell down."),
 ("The Head and the Tail (vv.13-17)",
  "For the people turneth not unto him that smiteth them, neither do they seek the LORD of hosts. Then "
  "an image the text stops to define, therefore the LORD will cut off from Israel head and tail, branch "
  "and rush, in one day, and the gloss follows immediately, the ancient and honourable, he is the head, "
  "and the prophet that teacheth lies, he is the tail. And the refrain returns unchanged, which is how "
  "each stanza in this poem ends."),
 ("Manasseh, Ephraim, and Judah (vv.18-21)",
  "Wickedness is described as a fire that consumes its own fuel, it shall devour the briers and thorns, "
  "and shall kindle in the thickets of the forest. Then the civil war stated as a sequence of names, "
  "Manasseh, Ephraim, and Ephraim, Manasseh, and they together shall be against Judah, so the tribes "
  "consume each other and then turn on the south. And the refrain closes the stanza for the third time, "
  "for all this his anger is not turned away, but his hand is stretched out still."),
],
"isaiah10": [
 ("Woe unto Them That Decree Unrighteous Decrees (vv.1-4)",
  "The fourth and last stanza of the poem that began at 9:8, and its target is legislators rather than "
  "criminals, woe unto them that decree unrighteous decrees, and that write grievousness which they "
  "have prescribed, to turn aside the needy from judgment. Injustice enacted correctly, with "
  "paperwork, which is a distinct offence from the violence charged elsewhere in these chapters. And "
  "the refrain lands for the last time, his hand is stretched out still."),
 ("Assyria, the Rod of Mine Anger (vv.5-11)",
  "O Assyrian, the rod of mine anger, and the staff in their hand is mine indignation. The empire is "
  "described as a tool with a purpose assigned to it, I will send him against an hypocritical nation. "
  "And then the difficulty is raised in the very next verse rather than left for a reader to find, "
  "howbeit he meaneth not so, neither doth his heart think so, but it is in his heart to destroy. The "
  "instrument has intentions of its own and they are not the same intentions. Both halves are stated "
  "and neither is withdrawn, which is the knot Jeremiah 51 also ties. Assyria is then quoted boasting, "
  "and the boast contains a piece of theology, as my hand hath found the kingdoms of the idols, shall I "
  "not do to Jerusalem as I have done to Samaria. He has filed Jerusalem's God with the rest."),
 ("Shall the Axe Boast Against Him That Heweth (vv.12-19)",
  "The reply is a series of impossible pictures, shall the axe boast itself against him that heweth "
  "therewith, or the saw magnify itself against him that shaketh it, as if the rod should shake itself "
  "against them that lift it up. Then the sentence, which reduces a world empire first to a sick man "
  "and then to a cleared wood, the light of Israel shall be for a fire, and it shall burn and devour "
  "his thorns and his briers in one day. And the closing measure is deliberately small, the remnant of "
  "the trees shall be few, that a child may write them."),
 ("The Remnant Shall Return (vv.20-23)",
  "The remnant of Israel shall no more again stay upon him that smote them, but shall stay upon the "
  "LORD, the Holy One of Israel, in truth. The name of Isaiah's son from 7:3 is used here as the "
  "doctrine, the remnant shall return, even the remnant of Jacob, unto the mighty God. And the double "
  "edge stays in it, since the same phrase promises survival and concedes scale, though the number be "
  "as the sand of the sea, yet a remnant of them shall return."),
 ("Be Not Afraid of the Assyrian (vv.24-27)",
  "Be not afraid of the Assyrian, and the argument is from precedent twice over, as it was in Egypt, "
  "and according to the slaughter of Midian at the rock of Oreb. Two rescues in which Israel's own "
  "military contribution was negligible. Then the yoke image of 9:4 returns, and his yoke shall be "
  "taken away from off thy neck, and the yoke shall be destroyed because of the anointing."),
 ("The Assyrian March, Town by Town (vv.28-34)",
  "The last section is a route march recited stage by stage, Aiath, Migron, Michmash, Geba, Ramah, "
  "Gibeah, Gallim, Laish, Anathoth, Madmenah, Gebim, Nob, and it stops at Nob within sight of the "
  "walls, he shall shake his hand against the mount of the daughter of Zion. Naming the villages is "
  "what makes the passage frightening rather than rhetorical: a reader in Jerusalem could count the "
  "days on his fingers. And then the sentence arrives in the language of forestry, behold, the Lord "
  "shall lop the bough with terror, and he shall cut down the thickets of the forest with iron, and "
  "Lebanon shall fall by a mighty one."),
],
"isaiah11": [
 ("A Rod Out of the Stem of Jesse (v.1)",
  "And there shall come forth a rod out of the stem of Jesse, and a Branch shall grow out of his roots. "
  "The image follows directly from the felled forest that closed the previous chapter and from the "
  "stump at 6:13, and the choice of Jesse rather than David is the point of the verse: it reaches back "
  "behind the monarchy to the family the monarchy came from, at a moment when the dynasty as an "
  "institution is a cut stump."),
 ("The Spirit of the LORD Shall Rest upon Him (v.2)",
  "And the spirit of the LORD shall rest upon him, followed by three pairs, the spirit of wisdom and "
  "understanding, the spirit of counsel and might, the spirit of knowledge and of the fear of the LORD. "
  "Seven terms in total, which is where the later phrase the sevenfold spirit comes from. Each pair "
  "joins a faculty to a capacity, so knowing is paired with deciding and both are anchored in "
  "reverence."),
 ("He Shall Not Judge After the Sight of His Eyes (vv.3-5)",
  "The qualification given is a negative one and it concerns method, he shall not judge after the sight "
  "of his eyes, neither reprove after the hearing of his ears, that is, not on appearances and not on "
  "testimony alone. Then who benefits, and it is not the influential, but with righteousness shall he "
  "judge the poor, and reprove with equity for the meek of the earth. And the weapon is speech, he "
  "shall smite the earth with the rod of his mouth, which Revelation 19 takes up as a sword coming "
  "out of the mouth."),
 ("The Wolf Also Shall Dwell with the Lamb (vv.6-9)",
  "The wolf also shall dwell with the lamb, and the leopard shall lie down with the kid, and the calf "
  "and the young lion and the fatling together, and a little child shall lead them. The list runs on "
  "through the cow and the bear, the lion eating straw like an ox, and a child playing at the hole of "
  "an asp. What is described is not animals being tamed but predation itself being removed, and the "
  "reason given is not sentiment, for the earth shall be full of the knowledge of the LORD, as the "
  "waters cover the sea."),
 ("An Ensign to the People (v.10)",
  "And in that day there shall be a root of Jesse, which shall stand for an ensign of the people, to it "
  "shall the Gentiles seek, and his rest shall be glorious. Paul quotes this verse at the end of Romans "
  "15 in a chain of texts assembled to establish that the Gentile mission was in the plan from the "
  "beginning, and this is the verse in that chain that says the nations do the seeking."),
 ("A Second Time, and a Highway (vv.11-16)",
  "The LORD shall set his hand again the second time to recover the remnant of his people, and the "
  "phrase the second time makes the exodus the pattern for what follows. The gathering is listed by "
  "country, Assyria, Egypt, Pathros, Cush, Elam, Shinar, Hamath, and the islands of the sea. Then the "
  "old division is healed, the envy of Ephraim shall depart, and Judah shall not vex Ephraim. And the "
  "chapter ends in engineering, the LORD shall utterly destroy the tongue of the Egyptian sea, and "
  "there shall be an highway for the remnant of his people, like as it was to Israel in the day that he "
  "came up out of the land of Egypt."),
],
"isaiah12": [
 ("O LORD, I Will Praise Thee (vv.1-3)",
  "And in that day thou shalt say, O LORD, I will praise thee, though thou wast angry with me, thine "
  "anger is turned away, and thou comfortedst me. The song is in the first person singular and it does "
  "not deny the anger, it dates it. Then the confession, behold, God is my salvation, I will trust, and "
  "not be afraid, which borrows its wording from the Song of the Sea in Exodus 15. And the closing "
  "line is an action rather than a statement, therefore with joy shall ye draw water out of the wells "
  "of salvation. That verse became the text sung at the water-drawing ceremony of Tabernacles, which is "
  "the setting in which Jesus stands up and speaks about thirst in John 7."),
 ("Declare His Doings Among the People (vv.4-6)",
  "The second song turns outward and into the plural, praise the LORD, call upon his name, declare his "
  "doings among the people, make mention that his name is exalted. The audience widens as far as it "
  "will go, sing unto the LORD, for he hath done excellent things, let this be known in all the earth. "
  "And the last verse gives the reason in the title from 1:4, for great in the midst of thee is the "
  "Holy One of Israel, which was an accusation the first time it appeared and is a comfort here. Six "
  "verses close the first movement of the book, and chapter 13 opens the oracles against the nations."),
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
