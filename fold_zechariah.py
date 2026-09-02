#!/usr/bin/env python3
"""
Folds Zechariah, all 14 chapters.

Dirtier input than Hosea. Three separate defects had to be repaired before the
sections could be written:

Fragment labels. Five prose sentences had been cut at a colon and promoted into
labels: 'The chapter then pivots to the ultimate resolution:' (z3), "God's answer
is devastating:" and 'God then reminds them what He actually requires:' (z7),
'Then comes the astonishing verse 9:' (z9), 'The most astonishing detail:' (z11).
Each is merged back onto the end of Historical Context, where it reads as the
sentence it always was.

Overlapping inherited skeletons. zechariah5 listed six items for eleven verses
with sub-points promoted to siblings, so vv.2-3 and v.4 sat inside vv.1-4 and
vv.7-8 inside vv.5-8. zechariah13 split one verse across two headings, v.7 and
v.7b. Both are restructured to the vision's own divisions with no overlap.

A gap. zechariah2 ran v.8 then vv.10-12, leaving verse 9 undescribed. Verses 8
and 9 are now taken together, which is how they read.

Emphatic capitals are repaired one at a time: FILTHY, PURGING, THEIR three
times, HUMBLE, PIECES, SILVER, CLEANSING, UNCLEANNESS. Two all-capital words are
deliberately kept because the KJV sets them that way and they are not emphasis:
BRANCH at 3:8 and 6:12, and HOLINESS at 14:20, which is an inscription on the
bells of the horses. 'Matt' is expanded to 'Matthew', which the corpus prefers
115 to 15.

Usage:
    python3 fold_zechariah.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
ITEM_RE = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')
KEEP = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]
CAPS = re.compile(r"\b[A-Z]{2,}\b")
CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "BRANCH", "HOLINESS"}
VERSES = {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14,
          8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21}

FIXES = {
    3: [("Joshua wears FILTHY garments", "Joshua wears filthy garments")],
    5: [("deal with the PURGING of sin", "deal with the purging of sin")],
    7: [("about THEIR grief, THEIR national identity, THEIR religious routine",
         "about their grief, their national identity, their religious routine")],
    9: [("having salvation, and HUMBLE", "having salvation, and humble"),
        ("(Matt 21:1-9)", "(Matthew 21:1-9)")],
    11: [("thirty PIECES of SILVER", "thirty pieces of silver"),
         ("(Matt 26:15)", "(Matthew 26:15)"),
         ("(Matt 27:3-10)", "(Matthew 27:3-10)")],
    13: [("leads to the CLEANSING of 13:1", "leads to the cleansing of 13:1"),
         ("not for ritual washing but for sin and UNCLEANNESS",
          "not for ritual washing but for sin and uncleanness")],
}

SECTIONS = {
1: [
 ("The Call to Repentance: Return unto Me (vv.1-6)",
  "The book opens two months after Haggai's first oracle, in the eighth month of Darius' "
  "second year, and it does not open with a vision. It opens with an argument from family "
  "history. Turn ye unto me, and I will turn unto you. Your fathers, where are they? and "
  "the prophets, do they live for ever? Both generations are dead, the warned and the "
  "warners, and only one thing outlasted them, my words did take hold of them. The point is "
  "aimed at men rebuilding a temple: the previous generation heard this and lost the city. "
  "And the response is recorded, they returned and said, Like as the LORD of hosts thought "
  "to do unto us, so hath he dealt with us."),
 ("The First Night Vision: Horsemen Among the Myrtles (vv.7-11)",
  "Three months later, in a single night, eight visions arrive. The first is a man on a red "
  "horse standing among the myrtle trees in a low place, with horses behind him. Their "
  "report is the problem the whole book answers: we have walked to and fro through the "
  "earth, and behold, all the earth sitteth still, and is at rest. That sounds like good "
  "news and it is not. The empires are comfortable, and Jerusalem is a building site with "
  "no walls. The patrol has found a settled world that has forgotten what it did."),
 ("The Angel's Intercession and God's Answer (vv.12-17)",
  "The angel of the LORD asks the question the returned exiles could not ask out loud. O "
  "LORD of hosts, how long wilt thou not have mercy on Jerusalem, against which thou hast "
  "had indignation these threescore and ten years? Seventy years is Jeremiah's number, and "
  "it has run out. The answer comes in good words and comfortable words. I am jealous for "
  "Jerusalem with a great jealousy, and I am very sore displeased with the heathen, for I "
  "was but a little displeased, and they helped forward the affliction. The instruments of "
  "judgment exceeded their brief. Then the promise, my house shall be built in it, and a "
  "line shall be stretched forth upon Jerusalem."),
 ("The Second Vision: Four Horns and Four Craftsmen (vv.18-21)",
  "Four horns, which are the powers that scattered Judah and Israel and Jerusalem. Then "
  "four carpenters, and the word covers any worker in wood or metal or stone. They come to "
  "fray them, to cast out the horns of the nations. The arithmetic is deliberate, one "
  "craftsman for each horn, and the vision answers the first one: the earth is at rest, and "
  "there are already four workmen on the way. Nothing is asked of Judah in this vision at "
  "all."),
],
2: [
 ("The Third Vision: A Man Measuring Jerusalem (vv.1-2)",
  "A man with a measuring line in his hand, going to measure Jerusalem, to see what is the "
  "breadth thereof, and what is the length thereof. It is exactly the right thing to be "
  "doing. The city has no walls, walls need a survey, and a survey needs a line. The vision "
  "does not correct his intention, it interrupts his measurement, which is a harder thing "
  "to accept."),
 ("The Angel's Message: No Walls Needed (vv.3-5)",
  "Run, speak to this young man, saying, Jerusalem shall be inhabited as towns without "
  "walls, for the multitude of men and cattle therein. The survey is called off because the "
  "measurement would be wrong, not because walls are wrong. Then the substitute, and it is "
  "not a smaller thing: I will be unto her a wall of fire round about, and will be the glory "
  "in the midst of her. Defense and glory in one sentence, and both of them a person rather "
  "than masonry. A wall marks a limit, and the promise is that the city will outgrow any "
  "limit drawn now."),
 ("The Call to Flee Babylon (vv.6-7)",
  "Ho, ho, come forth, and flee from the land of the north. Most of the Jewish community "
  "was still in Babylon and comfortable there, two decades after Cyrus' decree allowed the "
  "return. The call is urgent and it is aimed at the successful, deliver thyself, O Zion, "
  "that dwellest with the daughter of Babylon. Staying is treated as a danger rather than a "
  "choice, because the north is where judgment is stored."),
 ("The Apple of God's Eye and the Hand Shaken (vv.8-9)",
  "He that toucheth you toucheth the apple of his eye. The Hebrew is the pupil, the part of "
  "the body most instinctively defended and least able to defend itself, and the nations "
  "that handled Judah are told what they were handling. Then the reversal, I will shake mine "
  "hand upon them, and they shall be a spoil to their servants. The plunderers become the "
  "plunder, and the proof offered is the prophet himself, ye shall know that the LORD of "
  "hosts hath sent me."),
 ("The LORD Comes to Dwell in Zion, and All Flesh Silent (vv.10-13)",
  "Sing and rejoice, O daughter of Zion, for, lo, I come, and will dwell in the midst of "
  "thee. What the exiles had lost was not primarily a building but a presence, and the "
  "promise addresses the loss directly. Then the reach widens, many nations shall be joined "
  "to the LORD, and shall be my people, which puts Gentiles inside the covenant formula "
  "itself. The vision closes not with celebration but with an order to stop talking, be "
  "silent, O all flesh, before the LORD, for he is raised up out of his holy habitation."),
],
3: [
 ("Joshua Before the Angel: Satan the Accuser (vv.1-2)",
  "The fourth vision is a courtroom, and the man in the dock is the high priest. Joshua "
  "stands before the angel of the LORD, and Satan stands at his right hand to resist him. "
  "The reply is not a defense, it is a rebuke, the LORD rebuke thee, O Satan, and then a "
  "reason that concedes everything, is not this a brand plucked out of the fire? The "
  "argument for Joshua is that he was rescued, not that he was innocent. Nothing is said "
  "against the accusation."),
 ("The Filthy Garments Removed (vv.3-4)",
  "Now Joshua was clothed with filthy garments. The Hebrew word is the strongest available "
  "for defilement, and it is worn by the man who represents the nation before God on the "
  "Day of Atonement, so the problem is not private. The remedy is issued as a command to "
  "the attendants rather than as a demand on Joshua: take away the filthy garments from "
  "him. Then the interpretation, I have caused thine iniquity to pass from thee, and I will "
  "clothe thee with change of raiment. He does nothing in the whole exchange but stand "
  "there."),
 ("The Clean Turban and Pure Vestments (v.5)",
  "And I said, Let them set a fair mitre upon his head. The prophet interrupts his own "
  "vision to ask for one more item, and it is the turban that carried the plate engraved "
  "HOLINESS unto the LORD across the high priest's forehead. Without it the office is not "
  "restored, only the man is cleaned. The request is granted, and the angel of the LORD "
  "stood by, which is the vision's way of saying the appointment is witnessed."),
 ("The Charge to Walk Faithfully (vv.6-7)",
  "If thou wilt walk in my ways, and if thou wilt keep my charge, then thou shalt judge my "
  "house. The conditions arrive after the cleansing, not before it, which is the order the "
  "whole chapter is built on. What is promised is jurisdiction, and then something further, "
  "I will give thee places to walk among them that stand by, meaning access among the "
  "attending angels of the vision itself."),
 ("The Branch and the Stone with Seven Eyes (vv.8-9)",
  "Hear now, O Joshua the high priest, behold, I will bring forth my servant the BRANCH. "
  "The title is Jeremiah's for the coming son of David, and it lands on a priest in a "
  "vision about priesthood, which is where chapter 6 will take it. Then a second image, a "
  "stone laid before Joshua with seven eyes upon it, and an engraving. The promise attached "
  "is the largest in the chapter, I will remove the iniquity of that land in one day. Not "
  "annually, as the Day of Atonement required, and not gradually. One day."),
 ("Vine and Fig Tree (v.10)",
  "In that day shall ye call every man his neighbor under the vine and under the fig tree. "
  "After a courtroom, a change of clothes and a stone with seven eyes, the chapter ends in "
  "a garden with people talking over a fence. It is the standing biblical picture of peace, "
  "used of Solomon's reign and of Micah's future, and it is put here as the consequence of "
  "iniquity removed rather than as a separate blessing."),
],
4: [
 ("The Vision: A Golden Lampstand with Olive Trees (vv.1-3)",
  "The angel wakes him, as a man that is wakened out of his sleep, which suggests the "
  "night's visions had not been restful. What he sees is a candlestick all of gold with a "
  "bowl on the top and seven lamps, and seven pipes to each lamp, and two olive trees "
  "standing beside it. The temple lampstand was tended daily by priests carrying oil. This "
  "one is plumbed. Nobody carries anything."),
 ("Zechariah's Question and the Angel's Challenge (vv.4-5)",
  "What are these, my lord? The angel answers with a question, Knowest thou not what these "
  "be? and the prophet says no. The exchange is left in the text rather than tidied away, "
  "and it is the honest position of a man looking at working machinery whose purpose he "
  "cannot read. The vision is not self-explanatory and is not treated as though it should "
  "be."),
 ("Not by Might, Nor by Power, But by My Spirit (v.6)",
  "The answer skips the symbolism entirely and gives the meaning. This is the word of the "
  "LORD unto Zerubbabel, saying, Not by might, nor by power, but by my spirit, saith the "
  "LORD of hosts. Zerubbabel is a governor under Persian licence with no army, a small "
  "population and a half-built temple, and the sentence removes both of the things he does "
  "not have from the list of what the work requires. The lampstand fed without hands is the "
  "picture of it."),
 ("The Mountain Becomes a Plain (v.7)",
  "Who art thou, O great mountain? before Zerubbabel thou shalt become a plain. The "
  "obstacle is addressed rather than described, which is a particular kind of confidence. "
  "And he shall bring forth the headstone thereof with shoutings, crying, Grace, grace unto "
  "it. The last stone is placed to a shout about grace, not about workmanship."),
 ("Zerubbabel Will Finish It and the Day of Small Things (vv.8-10)",
  "The hands of Zerubbabel have laid the foundation of this house, his hands shall also "
  "finish it. A promise of completion given to men who had stopped for sixteen years. Then "
  "the question that names their real difficulty, for who hath despised the day of small "
  "things? The older men had seen Solomon's temple and wept at this one's foundation, and "
  "the reply is not that the building is bigger than it looks but that the plummet in "
  "Zerubbabel's hand is being watched by seven eyes that run through the whole earth."),
 ("The Two Olive Trees Explained (vv.11-14)",
  "The prophet asks twice, because the first answer did not cover the trees. What be these "
  "two olive branches which through the two golden pipes empty the golden oil out of "
  "themselves? The answer is compressed to the point of obscurity, these are the two "
  "anointed ones, that stand by the Lord of the whole earth. The Hebrew is literally the "
  "two sons of oil. Read against the chapter, they are the offices already in the room, "
  "Joshua the priest of chapter 3 and Zerubbabel the governor of this one, and what passes "
  "through them is not their own."),
],
5: [
 ("The Sixth Vision: The Flying Scroll (vv.1-2)",
  "A flying roll, and the angel asks what he sees, which the prophet answers with "
  "measurements: the length thereof twenty cubits, and the breadth thereof ten cubits. "
  "Thirty feet by fifteen. Those are the dimensions of the porch of Solomon's temple and of "
  "the holy place in the tabernacle, so the document is the size of the room where God met "
  "Israel, and it is airborne over the whole land."),
 ("The Curse Against Theft and False Swearing (vv.3-4)",
  "This is the curse that goeth forth over the face of the whole earth. Two offences are "
  "named out of all the possibilities, every one that stealeth and every one that sweareth "
  "falsely by my name, and they are one from each table of the law, a crime against a "
  "neighbor and a crime against God. The curse is not abstract, it is given an address: it "
  "shall enter into the house of the thief, and shall remain in the midst of his house, and "
  "shall consume it, the timber thereof and the stones thereof. It goes indoors and stays."),
 ("The Seventh Vision: The Woman in the Ephah (vv.5-8)",
  "An ephah, a dry measure of about half a bushel, the commercial container of ordinary "
  "trade, and the angel says this is their resemblance through all the earth. A talent of "
  "lead is lifted and there is a woman sitting inside the basket. The naming is flat and "
  "final, this is wickedness, and the response is not argument but containment, he cast it "
  "into the midst of the ephah, and he cast the weight of lead upon the mouth thereof. Sin "
  "is measured in the vessel used for buying and selling and then sealed under a lid too "
  "heavy to lift."),
 ("Wickedness Carried to Shinar (vv.9-11)",
  "Two women with wings like the wings of a stork, and the wind in their wings, carrying "
  "the sealed basket. Whither do these bear the ephah? To build it an house in the land of "
  "Shinar. Shinar is Babel, where the tower was built in Genesis 11, and the point is not "
  "destruction but relocation. Wickedness is not annihilated in this vision, it is deported "
  "to its own country and given a house there, which is how the restored community is made "
  "clean."),
],
6: [
 ("The Eighth Vision: Four Chariots from Bronze Mountains (vv.1-3)",
  "Four chariots come out from between two mountains of brass, with red horses, black "
  "horses, white horses and grisled and bay. The night began with horses standing still "
  "among myrtles in a hollow and it ends with chariots coming out between bronze mountains, "
  "and the movement is the whole point. What was a patrol at rest is now a deployment."),
 ("The Interpretation: Four Spirits of Heaven (vv.4-8)",
  "These are the four spirits of the heavens, which go forth from standing before the Lord "
  "of all the earth. The word covers both spirits and winds, and both readings work, agents "
  "sent from a throne room and weather going out over a map. They are directed north and "
  "south, which is where the empires were, and the closing line answers the complaint of "
  "chapter 1 exactly: they have quieted my spirit in the north country. The earth sat still "
  "while Jerusalem suffered, and now the stillness is God's own and it is deliberate."),
 ("The Symbolic Crowning of Joshua (vv.9-11)",
  "The visions end and an instruction follows that has to be carried out in daylight. Take "
  "silver and gold from named men newly arrived from Babylon, make crowns, and set them "
  "upon the head of Joshua the son of Josedech, the high priest. Not on Zerubbabel, who is "
  "the descendant of David in the room. A crown on a priest breaks the separation of the "
  "two offices that the law had kept apart since Aaron, and the whole point is that it is "
  "done in public with imported gold."),
 ("The Branch Prophecy: Priest-King (vv.12-13)",
  "Behold the man whose name is The BRANCH, and he shall build the temple of the LORD, and "
  "he shall bear the glory, and shall sit and rule upon his throne, and he shall be a "
  "priest upon his throne. The crowned priest standing there is a sign of somebody else. "
  "Then the clause that explains why the two offices had to be joined, and the counsel of "
  "peace shall be between them both. Where king and priest are two men there is always "
  "negotiation between them, and Israel's history is largely the record of that "
  "negotiation failing."),
 ("The Crown as a Memorial and Those Far Off (vv.14-15)",
  "The crowns are not left on Joshua's head. They shall be for a memorial in the temple of "
  "the LORD, kept as an object rather than worn, because the coronation was a statement and "
  "not an appointment. Then the reach past the returned community, they that are far off "
  "shall come and build in the temple of the LORD. The chapter closes on a condition, and "
  "this shall come to pass, if ye will diligently obey the voice of the LORD your God."),
],
7: [
 ("The Delegation's Question: Should We Still Fast? (vv.1-3)",
  "Two years on, in the fourth year of Darius, men arrive from Bethel with a procedural "
  "question. Should I weep in the fifth month, separating myself, as I have done these so "
  "many years? The fast of the fifth month marked the burning of the temple, and the temple "
  "is now nearly rebuilt, so the question is reasonable and narrow: is the mourning still "
  "required? Seventy years of practice stand behind it."),
 ("God's Probing Response: Was It Really for Me? (vv.4-6)",
  "The answer does not address the calendar. When ye fasted and mourned in the fifth and "
  "seventh month, even those seventy years, did ye at all fast unto me, even to me? The "
  "question is about the object of the act rather than its continuation. Then it is widened "
  "so no one can treat fasting as the special case, and when ye did eat, and when ye did "
  "drink, did not ye eat for yourselves, and drink for yourselves? Feasting and fasting are "
  "put on the same footing, and both are found pointed inward."),
 ("The True Requirement: Justice and Mercy (vv.7-10)",
  "Are not these the words which the LORD hath cried by the former prophets? The generation "
  "asking about fasts is referred to the generation that lost the city, and the content of "
  "the earlier message is restated as four commands and one prohibition: execute true "
  "judgment, show mercy and compassion every man to his brother, oppress not the widow, the "
  "fatherless, the stranger, nor the poor, and let none of you imagine evil against his "
  "brother in your heart. Not one item concerns the calendar."),
 ("The Fathers' Stubborn Refusal (vv.11-12)",
  "But they refused to hearken, and pulled away the shoulder, and stopped their ears. The "
  "shoulder is an ox refusing the yoke, an animal that will not take the harness. Then the "
  "hardest image in the chapter, they made their hearts as an adamant stone, lest they "
  "should hear the law. Adamant is the hardest substance the language had a word for, and "
  "the hardening is described as something they did on purpose and for a purpose, so as not "
  "to hear."),
 ("The Terrible Consequence: As I Called, They Refused (vv.13-14)",
  "Therefore it is come to pass, that as he cried, and they would not hear, so they cried, "
  "and I would not hear. The symmetry is exact and is stated as the mechanism rather than "
  "as revenge. I scattered them with a whirlwind among all the nations, and the land was "
  "desolate after them, that no man passed through. The closing clause is the answer to the "
  "delegation's question, put in the form of a consequence: the empty land is why there is "
  "a fast in the fifth month at all."),
],
8: [
 ("God's Jealousy for Zion (vv.1-2)",
  "Chapter 8 answers the fasting question by changing the subject to what God intends, and "
  "it does so through ten oracles each opening with thus saith the LORD of hosts. The first "
  "is short. I was jealous for Zion with a great jealousy, and I was jealous for her with "
  "great fury. The same word carried the threat in earlier prophets and here it carries the "
  "commitment, because jealousy is what a husband feels about a wife and not what a "
  "landlord feels about a property."),
 ("The Faithful City: Elderly and Children at Peace (vv.3-5)",
  "I am returned unto Zion, and Jerusalem shall be called a city of truth. Then the picture "
  "of what that looks like, and it is domestic rather than imperial: old men and old women "
  "shall dwell in the streets of Jerusalem, and every man with his staff in his hand for "
  "very age, and the streets of the city shall be full of boys and girls playing. The two "
  "groups named are the ones who cannot survive a siege or a war. Their presence outdoors "
  "is the whole proof."),
 ("Nothing Too Hard, and the Gathering from East and West (vv.6-8)",
  "If it be marvellous in the eyes of the remnant of this people in these days, should it "
  "also be marvellous in mine eyes? The promise is set against the audience's own sense of "
  "scale, and the question is left as a question. Then the mechanism, I will save my people "
  "from the east country, and from the west country, and I will bring them, and they shall "
  "dwell in the midst of Jerusalem. The covenant formula closes it, they shall be my "
  "people, and I will be their God, in truth and in righteousness, the sentence Hosea's "
  "children had been named to cancel."),
 ("Let Your Hands Be Strong (vv.9-13)",
  "Let your hands be strong, ye that hear in these days the words of the prophets. The "
  "instruction is addressed to men on a building site and it is argued from their own recent "
  "experience: before these days there was no hire for man, nor for beast, and no peace from "
  "the affliction. Now it is different, the seed shall be prosperous, the vine shall give "
  "her fruit, and the ground her increase. Then the reversal that runs to the nations, as ye "
  "were a curse among the heathen, so I will save you, and ye shall be a blessing. What they "
  "were used for as a warning they will be used for as a promise."),
 ("God's Purpose to Do Good (vv.14-15)",
  "As I thought to punish you, and I repented not, so again have I thought in these days to "
  "do good unto Jerusalem. The same settled intention is described running in the opposite "
  "direction, and the phrase I repented not is the guarantee rather than the threat: the "
  "judgment came because God does not change his mind halfway, and that is now the ground "
  "for confidence. Fear ye not."),
 ("Ethical Requirements: Truth, Justice, Peace (vv.16-17)",
  "These are the things that ye shall do. Speak ye every man the truth to his neighbor, "
  "execute the judgment of truth and peace in your gates, let none of you imagine evil in "
  "your hearts against his neighbor, and love no false oath. The list is nearly the same as "
  "the one their fathers refused in chapter 7, handed back to a generation with the "
  "promises attached rather than the warnings. The gates are where cases were heard, so "
  "this is about courts, not sentiment."),
 ("Fasts Become Feasts (vv.18-19)",
  "Here at last is the direct answer to the men from Bethel, and it took two chapters to "
  "arrive. The fast of the fourth month, and the fast of the fifth, and the fast of the "
  "seventh, and the fast of the tenth, shall be to the house of Judah joy and gladness, and "
  "cheerful feasts. All four fasts of the exile are named and none of them is abolished, "
  "they are converted. Then the condition that was the point all along, therefore love the "
  "truth and peace."),
 ("The Nations Seek the LORD (vv.20-23)",
  "It shall yet come to pass, that there shall come people, and the inhabitants of many "
  "cities. The movement is described as contagious, the inhabitants of one city going to "
  "another and saying, Let us go speedily to pray before the LORD, I will go also. Then the "
  "closing image, ten men out of all languages taking hold of the skirt of one Jew and "
  "saying, We will go with you, for we have heard that God is with you. The community that "
  "asked whether it still had to mourn is told that men from every language will one day "
  "hold on to its clothing."),
],
9: [
 ("Judgment on Damascus, Hamath, Tyre and Sidon (vv.1-4)",
  "Chapter 9 begins the undated burdens, and the tone changes with the dating. The oracle "
  "travels down the map from the north, Hadrach and Damascus, Hamath, then Tyre and Sidon. "
  "Tyre gets the most attention because Tyre had the most confidence, Tyrus did build "
  "herself a strong hold, and heaped up silver as the dust, and fine gold as the mire of "
  "the streets. The city on its island had survived a thirteen-year Babylonian siege. "
  "Behold, the Lord will cast her out, and he will smite her power in the sea, and she "
  "shall be devoured with fire."),
 ("The Philistine Cities and a Guard Set on God's House (vv.5-8)",
  "Ashkelon shall see it, and fear, Gaza also shall see it, and be very sorrowful. Four of "
  "the five Philistine cities are named, and the sentence on them is not extermination, I "
  "will take away his blood out of his mouth, and he shall be as a governor in Judah. The "
  "old enemy is absorbed rather than erased. Then the turn toward Jerusalem, and I will "
  "encamp about mine house because of the army, and no oppressor shall pass through them "
  "any more, for now have I seen with mine eyes. The house has a garrison, and the garrison "
  "is God."),
 ("The King on a Donkey and Dominion to the Ends of the Earth (vv.9-10)",
  "Rejoice greatly, O daughter of Zion, behold, thy King cometh unto thee, he is just, and "
  "having salvation, lowly, and riding upon an ass, and upon a colt the foal of an ass. "
  "Every word of it is deliberate and the animal is the argument, because a king came to "
  "war on a horse and to peace on a donkey, and this one is described as bringing salvation "
  "while riding the wrong animal for a conquest. All four Gospels record the entry, and "
  "Matthew quotes this verse for it. Then verse 10 disarms his own side, I will cut off the "
  "chariot from Ephraim, and the horse from Jerusalem, and the battle bow shall be cut off, "
  "and he shall speak peace unto the heathen, and his dominion shall be from sea even to "
  "sea."),
 ("Prisoners of Hope Set Free (vv.11-12)",
  "By the blood of thy covenant I have sent forth thy prisoners out of the pit wherein is "
  "no water. A dry cistern was a holding cell, which is where Joseph and Jeremiah were both "
  "put, and the release is credited to covenant blood rather than to a change of policy. "
  "Then the phrase the chapter is remembered for, turn you to the strong hold, ye prisoners "
  "of hope. Tyre built herself a strong hold in verse 3 and lost it, and the prisoners are "
  "pointed to a different one."),
 ("Judah as a Bow and Ephraim as an Arrow (vv.13-15)",
  "When I have bent Judah for me, and filled the bow with Ephraim, and raised up thy sons, "
  "O Zion, against thy sons, O Greece. The two kingdoms that split under Jeroboam are "
  "described as parts of a single weapon, one the bow and one the arrow, useless apart. The "
  "naming of Greece is striking two centuries before Alexander. Then the LORD shall be seen "
  "over them, and his arrow shall go forth as the lightning, and the imagery turns "
  "sacrificial at the end, they shall be filled like bowls, and as the corners of the "
  "altar."),
 ("The LORD Saves His Flock (vv.16-17)",
  "The LORD their God shall save them in that day as the flock of his people, for they "
  "shall be as the stones of a crown, lifted up as an ensign upon his land. Two images in "
  "one breath, sheep and jewels, the first about being kept and the second about being "
  "worth keeping. The chapter that opened over Damascus and Tyre closes over grain and new "
  "wine, corn shall make the young men cheerful, and new wine the maids, which is the "
  "ordinary evidence that the war is over."),
],
10: [
 ("Ask the LORD for Rain, Not Idols (vv.1-2)",
  "Ask ye of the LORD rain in the time of the latter rain. Everything in an agricultural "
  "economy turned on the spring rain, and the instruction is simply to ask the right party "
  "for it, so the LORD shall give you showers of rain, to every one grass in his field. "
  "What they had done instead is named without softening: the idols have spoken vanity, and "
  "the diviners have seen a lie, and have told false dreams, they comfort in vain. The "
  "consequence is a flock without a shepherd, therefore they went their way as a flock, "
  "they were troubled, because there was no shepherd."),
 ("Anger Against the Shepherds and Strength from Judah (vv.3-5)",
  "Mine anger was kindled against the shepherds, and I punished the goats. The leaders are "
  "held responsible for the scattering described in the previous verse. Then a sequence of "
  "four things coming out of Judah, and each is a load-bearing item rather than a "
  "decoration: out of him came forth the corner, out of him the nail, out of him the battle "
  "bow, out of him every oppressor together. Cornerstone, tent peg, weapon. And the result "
  "in the field, they shall be as mighty men, which tread down their enemies in the mire of "
  "the streets, because the LORD is with them."),
 ("The Full Restoration of Judah and Ephraim (vv.6-7)",
  "I will strengthen the house of Judah, and I will save the house of Joseph. Both kingdoms "
  "are named, and the northern one had been gone two hundred years when this was written. "
  "The promise is put in terms of memory, they shall be as though I had not cast them off, "
  "and the ground of it is not their return but his hearing, for I am the LORD their God, "
  "and will hear them. Ephraim's response is described physically, their heart shall "
  "rejoice as through wine, and their children shall see it, and be glad."),
 ("God Whistles for His Scattered People (vv.8-10)",
  "I will hiss for them, and gather them. The word is a shepherd's whistle, the sound used "
  "to bring in animals that know the voice, and it is a small and domestic thing to use for "
  "an international regathering. And I will sow them among the people, which reads the "
  "scattering as planting rather than waste. The destinations named are Egypt and Assyria, "
  "and the ground promised is Gilead and Lebanon, and the closing clause admits the "
  "difficulty, place shall not be found for them, there will not be room."),
 ("Through the Sea and Strengthened in His Name (vv.11-12)",
  "He shall pass through the sea with affliction, and shall smite the waves in the sea, and "
  "all the deeps of the river shall dry up. The exodus is invoked deliberately, and the "
  "empires that follow, the pride of Assyria shall be brought down, and the sceptre of "
  "Egypt shall depart. Then the last verse puts the whole chapter in two clauses, I will "
  "strengthen them in the LORD, and they shall walk up and down in his name. Strength from "
  "him, and then ordinary walking about under his name."),
],
11: [
 ("The Devastation of the Land (vv.1-3)",
  "Open thy doors, O Lebanon, that the fire may devour thy cedars. The chapter that "
  "contains the book's most famous Messianic detail opens as a funeral for a landscape, "
  "cedar, fir and oak in turn, howl, fir tree, for the cedar is fallen. Then the sound of "
  "the men who lived off it, there is a voice of the howling of the shepherds, for their "
  "glory is spoiled, and a voice of the roaring of young lions, for the pride of Jordan is "
  "spoiled. Nothing is explained yet. The trees come down first."),
 ("The Shepherd of the Doomed Flock (vv.4-7)",
  "Feed the flock of the slaughter. The prophet is told to take a job whose outcome is "
  "stated in its title, and the reason is given, their own shepherds pity them not, whose "
  "possessors slay them and hold themselves not guilty, and say, Blessed be the LORD, for I "
  "am rich. Piety and profit in one sentence, over the bodies of the flock. He takes the "
  "work and two staffs, and names them, the one I called Beauty, and the other I called "
  "Bands, which are favor and union, the two things the flock has lost."),
 ("The Shepherd Rejected by the Flock (vv.8-9)",
  "I cut off three shepherds in one month, and then the sentence that turns the chapter, my "
  "soul loathed them, and their soul also abhorred me. The revulsion is mutual and it is "
  "stated in that order. What follows is the withdrawal of the care they refused, I will "
  "not feed you, that that dieth, let it die, and let the rest eat every one the flesh of "
  "another. The judgment is simply the removal of the shepherd, and the flock is left to do "
  "to itself what it wanted."),
 ("The Staff Beauty Broken: Covenant Annulled (vv.10-11)",
  "I took my staff, even Beauty, and cut it asunder, that I might break my covenant which I "
  "had made with all the people. The first staff was named favor, and breaking it is not "
  "temper, it is a legal act performed with a visual aid. And it was broken in that day, "
  "and so the poor of the flock that waited upon me knew that it was the word of the LORD. "
  "Only the poor of the flock recognize what has happened, which is the chapter's own note "
  "on who was paying attention."),
 ("Thirty Pieces of Silver and the Breaking of Bands (vv.12-14)",
  "Give me my price, and if not, forbear. So they weighed for my price thirty pieces of "
  "silver. The figure is the compensation Exodus 21:32 sets for a slave killed by an ox, "
  "and the shepherd's own comment is bitter, a goodly price that I was prised at. Then the "
  "instruction, cast it unto the potter in the house of the LORD, and he does it. Matthew "
  "27 records thirty pieces of silver paid for Jesus, thrown down in the temple, and used "
  "to buy the potter's field, and the fit is close enough that Matthew cites it. Then the "
  "second staff, I cut asunder mine other staff, even Bands, that I might break the "
  "brotherhood between Judah and Israel."),
 ("The Rise of the Foolish Shepherd (vv.15-17)",
  "Take unto thee yet the instruments of a foolish shepherd. A second piece of theatre, and "
  "it is the consequence of the first: a flock that drives out the shepherd it had does not "
  "end up with none, it ends up with a worse one. I will raise up a shepherd in the land, "
  "which shall not visit those that be cut off, but shall eat the flesh of the fat, and "
  "tear their claws. The chapter ends with a woe on him, and a sword on his arm and his "
  "right eye, the strength and the sight a shepherd needs."),
],
12: [
 ("God's Credentials as Creator (v.1)",
  "The burden of the word of the LORD for Israel, saith the LORD, which stretcheth forth "
  "the heavens, and layeth the foundation of the earth, and formeth the spirit of man "
  "within him. Before a word is said about the siege, the speaker is identified by three "
  "acts of creation, and the third is the one that matters for what follows, because the "
  "chapter will turn on a spirit poured out on men. The one who forms the human spirit is "
  "the one who can pour out grace on it."),
 ("Jerusalem a Cup of Staggering and a Heavy Stone (vv.2-3)",
  "I will make Jerusalem a cup of trembling unto all the people round about. The first "
  "image is a drink that takes the legs out from under whoever swallows it. The second is "
  "heavier, I will make Jerusalem a burdensome stone for all people, all that burden "
  "themselves with it shall be cut in pieces. A stone too heavy to lift injures the man who "
  "tries, and the injury is self-inflicted in the act of lifting. Though all the people of "
  "the earth be gathered together against it."),
 ("The Enemies Struck with Confusion (vv.4-5)",
  "I will smite every horse with astonishment, and his rider with madness. The cavalry is "
  "disabled from inside rather than defeated in the field, blindness on the horses and "
  "panic on the men, and mine eyes will be open upon the house of Judah. Then what Judah's "
  "own leaders conclude, the governors of Judah shall say in their heart, The inhabitants "
  "of Jerusalem shall be my strength in the LORD of hosts their God. The relief is read "
  "correctly by the people who receive it."),
 ("Judah as Fire Among Wood (v.6)",
  "I will make the governors of Judah like an hearth of fire among the wood, and like a "
  "torch of fire in a sheaf, and they shall devour all the people round about. Both images "
  "are of a small thing dropped into a large quantity of fuel, and both describe an "
  "outcome disproportionate to the size of what starts it. And Jerusalem shall be inhabited "
  "again in her own place, even in Jerusalem, which is a deliberately flat ending to a "
  "violent verse."),
 ("The Weak Made Strong and the Nations Destroyed (vv.7-9)",
  "The LORD also shall save the tents of Judah first, that the glory of the house of David "
  "and of the inhabitants of Jerusalem do not magnify themselves. The order of rescue is "
  "arranged to prevent the capital taking credit, which is a striking thing to legislate "
  "inside a promise. Then the levelling, he that is feeble among them at that day shall be "
  "as David, and the house of David shall be as God, as the angel of the LORD before them. "
  "And in that day I will seek to destroy all the nations that come against Jerusalem."),
 ("The Spirit Poured Out: Looking on the Pierced One (v.10)",
  "I will pour upon the house of David the spirit of grace and of supplications, and they "
  "shall look upon me whom they have pierced. The grammar is the difficulty and the point. "
  "God says they pierced me, and then speaks of the pierced one in the third person, they "
  "shall mourn for him, as one mourneth for his only son. John quotes the verse at the "
  "crucifixion and Revelation quotes it of the return. The mourning is produced by the "
  "spirit of grace, not by remorse arriving on its own."),
 ("The Great Mourning, Every Family Apart (vv.11-14)",
  "The mourning is compared to the mourning of Hadadrimmon in the valley of Megiddon, which "
  "is the grief over Josiah's death, the last good king, remembered as the deepest national "
  "sorrow available. Then it is broken down household by household, the family of the house "
  "of David apart, and their wives apart, the family of the house of Nathan apart, Levi "
  "apart, Shimei apart. Royal line, prophetic line, priestly line, and all the families "
  "that remain. The word apart is repeated until it is unmistakable: this is not a crowd "
  "weeping, it is every house on its own."),
],
13: [
 ("The Fountain Opened for Sin and Uncleanness (v.1)",
  "In that day there shall be a fountain opened to the house of David and to the "
  "inhabitants of Jerusalem for sin and for uncleanness. The mourning of chapter 12 runs "
  "straight into this without a break, and what is opened is a spring rather than a basin. "
  "The law's provision for uncleanness was water carried, measured and used up, and a "
  "fountain is the one form of water that cannot be exhausted by the number of people using "
  "it."),
 ("The Purging of Idols and False Prophets (vv.2-6)",
  "I will cut off the names of the idols out of the land, and they shall no more be "
  "remembered. Not just the objects but the names, so the vocabulary goes as well. Then the "
  "prophets, and the treatment is severe: a man whose own father and mother put him to "
  "death for speaking lies in the LORD's name. The result is a trade in disguises, they "
  "shall be ashamed every one of his vision, and shall not wear a rough garment to deceive. "
  "Each denies the office, I am no prophet, I am an husbandman. And the wounds in his hands "
  "get an explanation, those with which I was wounded in the house of my friends, a line "
  "read for centuries as pointing past the false prophet to the true one."),
 ("The Sword Against the Shepherd and the Scattered Sheep (v.7)",
  "Awake, O sword, against my shepherd, and against the man that is my fellow, saith the "
  "LORD of hosts, smite the shepherd, and the sheep shall be scattered. The sword is "
  "commanded, and it is commanded by God against a man he calls his fellow, his own "
  "associate. Jesus quotes the verse on the way to Gethsemane and applies the scattering to "
  "the disciples that night. The verse ends with a hand turned not in anger, and I will "
  "turn mine hand upon the little ones, the smallest of the flock kept while the rest run."),
 ("Two Parts Cut Off and the Third Refined (vv.8-9)",
  "Two parts therein shall be cut off and die, but the third shall be left therein. The "
  "arithmetic is brutal and it is stated without mitigation. Then what happens to the "
  "remainder, and I will bring the third part through the fire, and will refine them as "
  "silver is refined, and will try them as gold is tried. Survival is not the end of the "
  "process, it is entry into it. And the outcome is the covenant formula restored from both "
  "sides, they shall call on my name, and I will hear them, I will say, It is my people, "
  "and they shall say, The LORD is my God."),
],
14: [
 ("The Nations Gathered and the City Taken (vv.1-2)",
  "Behold, the day of the LORD cometh, and the chapter begins with the city losing. I will "
  "gather all nations against Jerusalem to battle, and the city shall be taken, and the "
  "houses rifled, and the women ravished, and half of the city shall go forth into "
  "captivity. Nothing is softened, and the gathering is credited to God rather than to the "
  "nations' ambition. Then the clause the rest of the chapter grows from, and the residue "
  "of the people shall not be cut off from the city. Half taken, and a remainder left."),
 ("The LORD Goes Forth and His Feet on the Mount of Olives (vv.3-5)",
  "Then shall the LORD go forth, and fight against those nations, as when he fought in the "
  "day of battle. And his feet shall stand in that day upon the mount of Olives, which is "
  "before Jerusalem on the east, and the mount of Olives shall cleave in the midst thereof. "
  "The location is specific, the same ridge from which Acts 1 records the ascension and the "
  "promise of a return in like manner. The mountain splits east and west and makes a valley "
  "to escape through, and the escape is compared to a remembered earthquake in the days of "
  "Uzziah, and the LORD my God shall come, and all the saints with thee."),
 ("A Day Neither Day Nor Night, and Living Waters (vv.6-8)",
  "It shall come to pass in that day, that the light shall not be clear, nor dark, but it "
  "shall be one day which shall be known to the LORD, not day, nor night, but at evening "
  "time it shall be light. The ordinary division of time stops working, and the light "
  "arrives at the hour it normally leaves. Then the water, and it shall be in that day, "
  "that living waters shall go out from Jerusalem, half of them toward the former sea, and "
  "half toward the hinder sea, in summer and in winter shall it be. Jerusalem sits on a "
  "ridge with no river, and the two seas named are the Dead Sea and the Mediterranean."),
 ("The LORD King Over All the Earth (v.9)",
  "And the LORD shall be king over all the earth, in that day shall there be one LORD, and "
  "his name one. The whole book has been arguing toward this sentence, and it is put in the "
  "plainest terms available. The last clause takes up the confession of Deuteronomy 6, the "
  "Shema, and treats it as something that becomes visible rather than something recited."),
 ("The Land Made Plain and Jerusalem Safely Inhabited (vv.10-11)",
  "All the land shall be turned as a plain, and the city lifted up and inhabited in her "
  "place, described by its own landmarks, from Benjamin's gate to the place of the first "
  "gate, from the tower of Hananeel unto the king's winepresses. The topography around "
  "Jerusalem is flattened and the city alone is raised, which reverses the ordinary "
  "geography of a hill town in a range of hills. Then the sentence that answers chapter 2's "
  "vision of a city without walls, and there shall be no more utter destruction, but "
  "Jerusalem shall be safely inhabited."),
 ("The Plague on the Enemies (vv.12-15)",
  "This shall be the plague wherewith the LORD will smite all the people that have fought "
  "against Jerusalem, their flesh shall consume away while they stand upon their feet. What "
  "follows is not battle but collapse from within, a great tumult from the LORD among them, "
  "and they shall lay hold every one on the hand of his neighbor, and his hand shall rise "
  "up against the hand of his neighbor. The army destroys itself, the wealth is collected, "
  "and the plague is extended to the animals in the camp, the horse, the mule, the camel "
  "and the ass."),
 ("The Nations Keep the Feast of Tabernacles (vv.16-19)",
  "Every one that is left of all the nations shall even go up from year to year to worship "
  "the King, the LORD of hosts, and to keep the feast of tabernacles. Of the three annual "
  "feasts this is the one that required living in booths, remembering a nation with no "
  "houses and no land, and it is the one the nations are given to keep. The sanction is "
  "rain, which is the ordinary business of Baal in the earlier prophets, upon them shall be "
  "no rain, and Egypt is named specifically, a country whose water came from a river rather "
  "than the sky."),
 ("Holiness on the Bells of the Horses (vv.20-21)",
  "In that day shall there be upon the bells of the horses, HOLINESS unto the LORD. The "
  "engraving from the high priest's turban, the plate of gold in Exodus 39, ends up on "
  "harness fittings. And the pots in the LORD's house shall be like the bowls before the "
  "altar, so the ordinary cooking pot is levelled up to the sacred vessel rather than the "
  "sacred vessel brought down. Every pot in Jerusalem becomes usable for sacrifice, and the "
  "last line of the book removes the one thing that would make that impossible, there shall "
  "be no more the Canaanite in the house of the LORD of hosts."),
],
}


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for ch in range(1, 15):
        page = f"zechariah{ch}"
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        old = pane.group(2)
        fields, extra = {}, []
        for label, body in ITEM_RE.findall(old):
            label = label.strip()
            if label in KEEP:
                fields[label] = body.strip()
            else:
                extra.append(f"{label} {body.strip()}")
        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
                continue
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} fragment label(s) merged back")
        for old_s, new_s in FIXES.get(ch, []):
            if old_s not in fields["Historical Context:"]:
                problems.append(f"{page}: fix target absent {old_s!r}")
                continue
            fields["Historical Context:"] = fields["Historical Context:"].replace(
                old_s, new_s)
            notes.append(f"{page}: repaired {old_s[:44]!r}")
        sections = SECTIONS[ch]
        covered = set()
        for label, text in [(w, fields[w]) for w in KEEP] + \
                           [(f"section {h!r}", p) for h, p in sections]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            for bad, why in [("*", "markdown asterisk"), (" -- ", "double hyphen"),
                             ("\u2013", "en-dash")]:
                if bad in text:
                    problems.append(f"{page}: {why} in {label}")
            if re.search(r"\b([A-Za-z]{2,})- ([a-z]{2,})\b", text):
                problems.append(f"{page}: broken hyphenation in {label}")
            if re.search(r"\bMatt\b", text):
                problems.append(f"{page}: abbreviated Matt in {label}")
        for head, _ in sections:
            if "!" in head:
                problems.append(f"{page}: exclamation in {head!r}")
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[ch]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[ch]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[ch] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for want in KEEP:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new
    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
