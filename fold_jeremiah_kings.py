#!/usr/bin/env python3
"""
Jeremiah 21 to 29: the kings, the false prophets, and the letter to Babylon. Nine
pages, 227 verses. All nine sublists are gapless outlines and are folded.

This is the block where the book stops being mostly poetry and becomes mostly record.
Chapter 26 is the trial transcript for the temple sermon that chapter 7 gives as a
text, and it contains the only place in the Old Testament where one prophetic book is
quoted by name in argument, when the elders cite Micah 3:12 as precedent. Chapter 28
is a public confrontation Jeremiah loses on the day. Chapter 29 is the only prophetic
letter preserved anywhere in scripture, and the reply to it is preserved too, so the
chapter is a complete exchange of correspondence in both directions.

Two things in this block are routinely quoted away from what they say. The promise at
29:11 is addressed to deportees who have just been told to build houses because they
will not be going home for seventy years, so most of them would die in Babylon. And
21:8-10 sets life and death before the people in Deuteronomy's formula and then makes
surrender the way of life, which is why the treason charge in chapters 37 and 38 was
not baseless.

Usage:
    python3 fold_jeremiah_kings.py [--check]
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
"jeremiah21": [
 ("Zedekiah Sends to Enquire (vv.1-2)",
  "Zedekiah sends two officials, and the request is a request for a repeat performance: enquire, I "
  "pray thee, of the LORD for us, for Nebuchadrezzar king of Babylon maketh war against us, if so be "
  "that the LORD will deal with us according to all his wondrous works, that he may go up from us. "
  "The wondrous works he has in mind are specific. In 701 BC Sennacherib's army had withdrawn from "
  "Hezekiah's Jerusalem overnight, and the king is citing that precedent and asking for it again. The "
  "Pashur named here is a different man from the one who put Jeremiah in the stocks in chapter 20."),
 ("I Myself Will Fight Against You (vv.3-7)",
  "The answer inverts the precedent instead of granting it. Behold, I will turn back the weapons of "
  "war that are in your hands, and I myself will fight against you with an outstretched hand and with "
  "a strong arm, even in anger, and in fury, and in great wrath. The phrase outstretched hand and "
  "strong arm is exodus language, used throughout Deuteronomy of God fighting for Israel against "
  "Egypt, and here it is turned round and aimed at Jerusalem. Then the sentence, and the withdrawal of "
  "every mitigating clause, he shall not spare them, neither have pity, nor have mercy."),
 ("The Way of Life and the Way of Death (vv.8-10)",
  "Behold, I set before you the way of life, and the way of death, which is Deuteronomy 30's formula "
  "exactly. What fills it in is the opposite of what Deuteronomy meant: he that abideth in this city "
  "shall die by the sword, and by the famine, and by the pestilence, but he that goeth out, and "
  "falleth to the Chaldeans, he shall live, and his life shall be unto him for a prey. Surrender is "
  "the way of life. This is the counsel that gets him charged with treason in chapters 37 and 38, and "
  "it is worth being honest that the charge had substance: he was standing in a besieged city telling "
  "its defenders to desert."),
 ("Execute Judgment in the Morning (vv.11-14)",
  "To the house of the king of Judah, execute judgment in the morning, and deliver him that is spoiled "
  "out of the hand of the oppressor. Morning was when the royal court sat to hear cases, so this is a "
  "job description rather than a general exhortation about being fair. Then the palace is addressed by "
  "its setting and quoted in its confidence, O inhabitant of the valley, and rock of the plain, which "
  "say, Who shall come down unto us. The fire is promised in its forest, which is the house of the "
  "forest of Lebanon, the cedar hall Solomon built and the kings still used."),
],
"jeremiah22": [
 ("Do Justice, and This House Shall Not Be a Desolation (vv.1-9)",
  "Go down to the house of the king of Judah, and speak there this word. What is required is listed as "
  "actions with named beneficiaries, execute ye judgment and righteousness, and deliver the spoiled "
  "out of the hand of the oppressor, and do no violence to the stranger, the fatherless, nor the widow, "
  "neither shed innocent blood in this place. The conditional runs both ways and is stated in full: if "
  "ye do this thing indeed, then there shall enter in by the gates of this house kings sitting upon "
  "the throne of David, and if ye will not hear, this house shall become a desolation. The picture the "
  "section ends on is of passers-by asking questions, all nations shall pass by this city, and they "
  "shall say every man to his neighbour, Wherefore hath the LORD done thus unto this great city."),
 ("Shallum, Who Will Not Return (vv.10-12)",
  "Weep ye not for the dead, neither bemoan him, but weep sore for him that goeth away, for he shall "
  "return no more, nor see his native country. The dead man is Josiah, killed at Megiddo and mourned "
  "nationally. The one to weep for is Shallum, who is Jehoahaz, on the throne three months before "
  "Necho deported him to Egypt, as 2 Kings 23 records. The comparison is the point of the three "
  "verses: a king who died at home came off better than a king taken away alive."),
 ("Woe to the Builder of the Panelled House (vv.13-19)",
  "This is Jehoiakim, and it is the most specific indictment of a named individual in the prophets. Woe "
  "unto him that buildeth his house by unrighteousness, that saith, I will build me a wide house and "
  "large chambers, and cutteth him out windows, and it is cieled with cedar, and painted with "
  "vermilion. The offence is named plainly and it is a labour offence, that useth his neighbour's "
  "service without wages, and giveth him not for his work. Then the comparison with his father, which "
  "is the heart of the passage, did not thy father eat and drink, and do judgment and justice, and "
  "then it was well with him, he judged the cause of the poor and needy, then it was well with him, "
  "was not this to know me, saith the LORD. Knowing God is there defined as judging the cause of the "
  "poor, and it is the plainest such definition in the Old Testament. The sentence is the ugliest in "
  "the book, he shall be buried with the burial of an ass, drawn and cast forth beyond the gates of "
  "Jerusalem."),
 ("Coniah, the Signet Plucked Off (vv.20-30)",
  "Coniah is Jehoiachin, eighteen years old and three months on the throne before the deportation of "
  "597 BC. The image used against him is the most intimate emblem of authority available, though thou "
  "wert the signet upon my right hand, yet would I pluck thee thence, since a signet ring is how a "
  "king's own hand is put to a document. Then a question thrown to the crowd, is this Coniah a "
  "despised broken idol. And the sentence that raises a real difficulty, write ye this man childless, "
  "no man of his seed shall prosper, sitting upon the throne of David. Jehoiachin did have sons, "
  "1 Chronicles 3 lists seven of them, and the line continues through Zerubbabel; Matthew's genealogy "
  "runs the descent to Jesus through Jechonias while Luke's traces a different route through Nathan. "
  "The verse is precise about what it forbids, which is a descendant sitting on the throne, not "
  "descendants."),
],
"jeremiah23": [
 ("Woe to the Pastors That Scatter (vv.1-4)",
  "Woe be unto the pastors that destroy and scatter the sheep of my pasture. The charge turns on one "
  "verb used twice in opposite senses, which is clearer in the Hebrew than in English: ye have not "
  "visited them, therefore behold, I will visit upon you the evil of your doings. They failed to look "
  "in on the flock, so they will be looked in on. Then the reversal, I will gather the remnant of my "
  "flock, and will bring them again to their folds, and I will set up shepherds over them which shall "
  "feed them. Ezekiel 34 works the same material at four times the length."),
 ("The Righteous Branch (vv.5-8)",
  "Behold, the days come, that I will raise unto David a righteous Branch, and a King shall reign and "
  "prosper, and shall execute judgment and justice in the earth. The title is the point of the "
  "passage, and this is his name whereby he shall be called, The LORD Our Righteousness. In Hebrew "
  "that is Yahweh Tsidkenu, which is deliberately close to the name of the king then on the throne: "
  "Zedekiah means the LORD is my righteousness. So the promise of a righteous king of David's line is "
  "announced in a wordplay on the name of the last and worst one. Zechariah takes up the same title at "
  "3:8 and 6:12."),
 ("Both Prophet and Priest Are Profane (vv.9-15)",
  "Mine heart within me is broken because of the prophets, all my bones shake, which is the physical "
  "register this book uses for its own reactions. The charge is moral before it is doctrinal, for both "
  "prophet and priest are profane, and the comparison drawn is with the north and it goes against "
  "Jerusalem: I have seen folly in the prophets of Samaria, they prophesied in Baal, but in the "
  "prophets of Jerusalem an horrible thing, they commit adultery, and walk in lies, and strengthen the "
  "hands of evildoers. Prophesying in the name of the wrong god is called folly; this is called "
  "horrible."),
 ("They Speak a Vision of Their Own Heart (vv.16-22)",
  "Hearken not unto the words of the prophets that prophesy unto you, they speak a vision of their own "
  "heart, and not out of the mouth of the LORD. Their message is quoted, ye shall have peace, and no "
  "evil shall come upon you, and the test proposed is not about accuracy but about attendance, for who "
  "hath stood in the counsel of the LORD. Then the criterion this chapter is most useful for, and it "
  "is measured by effect rather than by content, if they had stood in my counsel, then they should have "
  "turned them from their evil way. A word that came from God changes conduct, and one that did not, "
  "does not."),
 ("Can Any Hide Himself (vv.23-24)",
  "Am I a God at hand, saith the LORD, and not a God afar off, can any hide himself in secret places "
  "that I shall not see him, do not I fill heaven and earth. Two verses of omnipresence dropped into "
  "the middle of a chapter about prophets, and their function here is evidential rather than "
  "devotional: men claiming private revelation are being told there is no such category as private."),
 ("Dreams, and the Word Like a Hammer (vv.25-32)",
  "I have heard what the prophets said, that prophesy lies in my name, saying, I have dreamed, I have "
  "dreamed. The comparison offered is agricultural and dismissive, what is the chaff to the wheat. Then "
  "the two images this chapter is best known for, is not my word like as a fire, saith the LORD, and "
  "like a hammer that breaketh the rock in pieces. And the specific charges are trade practices rather "
  "than heresies: they steal my words every one from his neighbour, and they use their tongues, and "
  "say, He saith. Plagiarism, and a verbal formula deployed without anything behind it."),
 ("The Burden of the LORD (vv.33-40)",
  "This whole section is a pun that has to be explained before it works in English. The Hebrew massa "
  "means both a burden and an oracle, and the people are using the double sense as a joke, asking the "
  "prophet What is the burden of the LORD. The reply takes the other meaning and turns it on them, I "
  "will even forsake you, saith the LORD, ye are the burden. Then the word itself is confiscated, ye "
  "shall mention no more the burden of the LORD, for every man's word shall be his burden. A joke made "
  "at revelation's expense is answered by removing the term the joke depended on."),
],
"jeremiah24": [
 ("Two Baskets of Figs Set Before the Temple (v.1)",
  "The LORD shewed me, and behold, two baskets of figs were set before the temple of the LORD. The "
  "date in this verse governs everything that follows: after that Nebuchadrezzar had carried away "
  "captive Jeconiah, and the princes of Judah, with the carpenters and smiths. So the deportation of "
  "597 has already happened, and the vision is about how to read an event rather than about how to "
  "avoid one. The trades named are worth noticing, carpenters and smiths, because those are the "
  "skilled men an empire deports on purpose."),
 ("One Basket Very Good, the Other Very Bad (vv.2-3)",
  "One basket had very good figs, even like the figs that are first ripe, and the other basket had "
  "very naughty figs, which could not be eaten, they were so bad. First-ripe figs were a delicacy and "
  "the standard image for something desirable, so the contrast is between the best available and the "
  "actively inedible with nothing in between. Then the question and the answer follow the pattern of "
  "chapter 1, what seest thou, Jeremiah, and I said, Figs."),
 ("The Good Figs Are the Exiles (vv.4-7)",
  "Like these good figs, so will I acknowledge them that are carried away captive of Judah, whom I "
  "have sent out of this place into the land of the Chaldeans for their good. That last phrase "
  "overturns the whole popular reading of the deportation. The natural assumption was that the "
  "deported were the ones under judgment and those left in Jerusalem were the ones spared, and this "
  "vision says the reverse. What is promised the exiles is inward and unconditional, I will give them "
  "an heart to know me, that I am the LORD, and they shall be my people, and I will be their God, for "
  "they shall return unto me with their whole heart."),
 ("The Bad Figs Are Those Who Remain (vv.8-10)",
  "As the evil figs, which cannot be eaten, so will I give Zedekiah the king of Judah, and his "
  "princes, and the residue of Jerusalem that remain in this land, and them that dwell in the land of "
  "Egypt. For anyone still in Jerusalem taking their survival as evidence of favour, this is the "
  "sharpest thing in the book, and it is aimed at exactly the audience most likely to be pleased with "
  "itself. The sentence is the familiar triplet, I will send the sword, the famine, and the pestilence "
  "among them, till they be consumed."),
],
"jeremiah25": [
 ("Three and Twenty Years (vv.1-7)",
  "Dated the fourth year of Jehoiakim, which the text identifies as the first year of Nebuchadrezzar, "
  "605 BC, the year of Carchemish. The prophet then dates his own ministry and gives its result in one "
  "sentence: from the thirteenth year of Josiah, even unto this day, that is the three and twentieth "
  "year, the word of the LORD hath come unto me, and I have spoken unto you, rising early and "
  "speaking, but ye have not hearkened. Twenty-three years, summarised. And what had been asked was "
  "modest, turn ye again now every one from his evil way, and dwell in the land that the LORD hath "
  "given unto you and to your fathers."),
 ("Seventy Years (vv.8-14)",
  "I will send and take all the families of the north, and Nebuchadrezzar the king of Babylon, my "
  "servant. That last phrase is used of him three times in this book and it is startling every time: "
  "the invading pagan emperor is called God's servant. Then the number, these nations shall serve the "
  "king of Babylon seventy years. It is the figure Daniel 9 is reading and praying over, the one "
  "2 Chronicles 36 uses to interpret the exile through the land's unkept sabbaths, and the one Ezra 1 "
  "treats as run out. And the sentence has a second half that is often forgotten, when seventy years "
  "are accomplished, I will punish the king of Babylon, and that nation."),
 ("The Cup of the Wine of This Fury (vv.15-29)",
  "Take the wine cup of this fury at my hand, and cause all the nations to whom I send thee to drink "
  "it. The list of who drinks is effectively a table of contents for chapters 46 to 51: Egypt, Uz, the "
  "Philistine cities, Edom, Moab, Ammon, Tyre, Zidon, the isles, Dedan, Tema, Buz, Arabia, Elam, the "
  "Medes, all the kings of the north, and last of all Sheshach, which is a cipher for Babylon itself. "
  "The reason nobody is exempt is put as an argument from precedent, and it is hard to answer, for lo, "
  "I begin to bring evil upon the city which is called by my name, and should ye be utterly "
  "unpunished. Judgment that starts at the temple cannot stop at the border."),
 ("The LORD Shall Roar from on High (vv.30-38)",
  "The LORD shall roar from on high, he shall give a shout, as they that tread the grapes, against all "
  "the inhabitants of the earth. The imagery then moves from the winepress to the sheepfold, howl, ye "
  "shepherds, and cry, and wallow yourselves in the ashes, ye principal of the flock, with the reason "
  "given as a practical one, the shepherds shall have no way to flee. And the closing line supplies "
  "the register for the whole chapter, he hath forsaken his covert, as the lion."),
],
"jeremiah26": [
 ("The Sermon and the Seizure (vv.1-9)",
  "Dated in the beginning of the reign of Jehoiakim, and what this chapter records is the trial that "
  "followed the temple sermon chapter 7 gives as a text. The instruction includes a warning against "
  "editing, speak unto all the cities of Judah, diminish not a word. The offer is still open at this "
  "point, if so be they will hearken, and turn every man from his evil way, that I may repent me of "
  "the evil. What he says is the Shiloh comparison, and the reaction is immediate: the priests and the "
  "prophets and all the people took him, saying, Thou shalt surely die. Note who makes the arrest. It "
  "is the clergy, and among his accusers the prophets are named first."),
 ("The Trial Before the Princes (vv.10-11)",
  "When the princes of Judah heard these things, they came up from the king's house unto the house of "
  "the LORD, and sat down in the entry of the new gate. The civil authority convenes a court on temple "
  "ground, which is itself a jurisdictional fact worth noticing. The charge is laid by the priests and "
  "the prophets, this man is worthy to die, for he hath prophesied against this city, as ye have heard "
  "with your ears. It is a capital charge and the only evidence offered is the sermon itself."),
 ("The Defence (vv.12-15)",
  "The defence has three parts and no plea in mitigation. Jurisdiction first, the LORD sent me to "
  "prophesy against this house and against this city all the words that ye have heard. Then the offer "
  "repeated to the court that is trying him, therefore now amend your ways and your doings, and obey "
  "the voice of the LORD your God, and the LORD will repent him of the evil. And then consent to the "
  "verdict with a warning attached to it, as for me, behold, I am in your hand, do with me as seemeth "
  "good and meet unto you, but know ye for certain, that if ye put me to death, ye shall surely bring "
  "innocent blood upon yourselves."),
 ("The Verdict, and the Micah Precedent (vv.16-19)",
  "The acquittal is one sentence, this man is not worthy to die, for he hath spoken to us in the name "
  "of the LORD our God. Then the elders produce a precedent, and it is a genuine piece of legal "
  "argument from scripture: Micah the Morasthite prophesied in the days of Hezekiah, and they quote "
  "him, Zion shall be plowed like a field, which is Micah 3:12 word for word. This is the only place in "
  "the Old Testament where one prophetic book is cited by name in argument inside another. And their "
  "point is not the prophecy but the response to it, did he not fear the LORD, and the LORD repented "
  "him of the evil."),
 ("Urijah, Who Was Not Spared (vv.20-24)",
  "The chapter refuses to end on the acquittal, and that refusal is the most important thing in it. "
  "Urijah the son of Shemaiah prophesied in the same words, and Jehoiakim sought to put him to death, "
  "and he fled to Egypt, and was fetched back, and was killed with the sword, and his body thrown "
  "into the graves of the common people. It is one of only two extraditions recorded in the Old "
  "Testament. The legal argument had been won, and a man still died for the same sermon. Jeremiah "
  "lived because Ahikam the son of Shaphan happened to protect him, so the verdict did not make him "
  "safe. A patron did."),
],
"jeremiah27": [
 ("Make Thee Bonds and Yokes (vv.1-2)",
  "Thus saith the LORD to me, Make thee bonds and yokes, and put them upon thy neck. This sign is not "
  "performed and finished like the smashed bottle, it is worn, and worn continuously in public. That "
  "detail is what makes chapter 28 possible: a symbol you carry on your body is a symbol somebody else "
  "can take off you."),
 ("Send Them to the Kings (vv.3-11)",
  "The message goes out by the hand of the ambassadors which come to Jerusalem, to the kings of Edom, "
  "Moab, Ammon, Tyre and Zidon. What that describes is a summit: five states with delegations in "
  "Jerusalem negotiating a coalition against Babylon, and a prophet walking into the middle of it "
  "wearing a yoke. The argument put to them starts from creation rather than from politics, I have "
  "made the earth, the man and the beast, and have given it unto whom it seemed meet unto me, and now "
  "I have given all these lands into the hand of Nebuchadnezzar the king of Babylon, my servant. And "
  "the practical counsel is survival, bring your neck under the yoke of the king of Babylon, and serve "
  "him and his people, and live."),
 ("To Zedekiah, Serve Him and Live (vv.12-15)",
  "The same counsel is given to the king of Judah in the same words, and then the warning about the "
  "advice competing with it, hearken not to the words of your prophets that speak unto you, saying, Ye "
  "shall not serve the king of Babylon, for they prophesy a lie unto you. What is being urged looks "
  "like collaboration and is presented as the only policy anyone survives, which is the position that "
  "makes Jeremiah hated by the war party and useful to nobody."),
 ("To the Priests, the Vessels Will Not Come Back Yet (vv.16-22)",
  "The specific claim circulating in Jerusalem is quoted, behold, the vessels of the LORD's house "
  "shall now shortly be brought again from Babylon, that is, the deportation of 597 was temporary and "
  "the temple furniture would be home within the year. The reply is that the remaining vessels will "
  "follow the first lot, and then a clause that is easy to miss, and there shall they be until the day "
  "that I visit them, then will I bring them up, and restore them to this place. Ezra 1 records them "
  "brought back and inventoried, seventy years later. So the prophecy agreed with the peace-prophets "
  "about the eventual return and disagreed with them only about when, which was the whole of the "
  "argument."),
],
"jeremiah28": [
 ("Hananiah's Two Years (vv.1-4)",
  "In the fourth year of Zedekiah, Hananiah the son of Azur the prophet spake in the house of the LORD "
  "in the presence of the priests and of all the people. He uses the standard formula, thus speaketh "
  "the LORD of hosts, and the content is unusually specific: I have broken the yoke of the king of "
  "Babylon, and within two full years will I bring again into this place all the vessels of the LORD's "
  "house, and Jeconiah, and all the captives of Judah. Precise, dated and therefore falsifiable, and "
  "that is what destroys him."),
 ("Amen, the LORD Do So (vv.5-9)",
  "Jeremiah's first answer is the most gracious thing he says to an opponent anywhere in the book, "
  "Amen, the LORD do so, the LORD perform thy words which thou hast prophesied. Then the argument, and "
  "it is historical rather than theological: the prophets that have been before me prophesied both "
  "against many nations and against great kingdoms, of war, and of evil, and of pestilence. The burden "
  "of proof therefore lies with the man promising peace, because the tradition runs the other way. And "
  "the test offered is the one Deuteronomy 18 lays down, the prophet which prophesieth of peace, when "
  "the word of the prophet shall come to pass, then shall the prophet be known."),
 ("Hananiah Breaks the Yoke (vv.10-11)",
  "Then Hananiah the prophet took the yoke from off the prophet Jeremiah's neck, and brake it, and "
  "said before all the people, Even so will I break the yoke of Nebuchadnezzar from the neck of all "
  "nations within the space of two full years. And then the clause that says more about Jeremiah than "
  "any of his prayers do: and the prophet Jeremiah went his way. He does not answer, he does not "
  "resist the assault on his own sign, and he leaves. Whatever he had at that moment, he did not have "
  "a reply."),
 ("Iron Instead of Wood (vv.12-14)",
  "The word comes afterwards, which explains the previous verse: he left because there was nothing to "
  "say yet. Thou hast broken the yokes of wood, but I will make for them yokes of iron. The escalation "
  "is exact and it is presented as a consequence of the interference rather than as a punishment for "
  "it. Breaking the sign made the thing signified heavier, which is a claim about what signs are."),
 ("Hananiah Died the Same Year (vv.15-17)",
  "The LORD hath not sent thee, but thou makest this people to trust in a lie, and the charge given is "
  "not error but sedition, because thou hast taught rebellion against the LORD. Then the sentence, "
  "this year thou shalt die. And the record closes in one clause with no comment attached, so Hananiah "
  "the prophet died the same year in the seventh month. His two-year prophecy was answered in about "
  "two months."),
],
"jeremiah29": [
 ("The Letter (vv.1-3)",
  "These are the words of the letter that Jeremiah the prophet sent from Jerusalem unto the residue of "
  "the elders which were carried away captives. It is the only prophetic letter preserved in the Old "
  "Testament, and the delivery arrangement is worth noticing: it goes by the hand of Elasah the son of "
  "Shaphan and Gemariah the son of Hilkiah, whom Zedekiah sent unto Nebuchadnezzar. A private pastoral "
  "letter travelling to Babylon in the diplomatic bag of a state embassy."),
 ("Build Houses, Plant Gardens, Seek the Peace of the City (vv.4-7)",
  "Build ye houses, and dwell in them, and plant gardens, and eat the fruit of them, take ye wives, "
  "and beget sons and daughters. It is an instruction to settle, which is the opposite of what the "
  "exiles wanted to hear and the opposite of what their own prophets were telling them. Then the "
  "sentence that has shaped the politics of religious minorities ever since, and seek the peace of the "
  "city whither I have caused you to be carried away captive, and pray unto the LORD for it. They are "
  "told to pray for Babylon, and the reason given is not piety but enlightened self-interest, for in "
  "the peace thereof shall ye have peace."),
 ("Let Not Your Prophets Deceive You (vv.8-9)",
  "Let not your prophets and your diviners, that be in the midst of you, deceive you, neither hearken "
  "to your dreams which ye cause to be dreamed. That last clause is unexpectedly sharp about how the "
  "trade worked, because it puts the dreaming on the audience rather than on the prophets: the demand "
  "was creating the supply."),
 ("Seventy Years, and the Thoughts of Peace (vv.10-14)",
  "After seventy years be accomplished at Babylon I will visit you, and perform my good word toward "
  "you, in causing you to return to this place. Then the verse quoted more often than any other in "
  "Jeremiah and almost always without its address, for I know the thoughts that I think toward you, "
  "saith the LORD, thoughts of peace, and not of evil, to give you an expected end. It is written to "
  "people who have just been told to build houses because they are not going home for seventy years, "
  "which means most of the original readers would die in Babylon. The promise is made to the community "
  "rather than to the individuals holding the letter, and it costs the first generation everything. "
  "The condition follows immediately, ye shall seek me, and find me, when ye shall search for me with "
  "all your heart."),
 ("Ahab and Zedekiah (vv.15-23)",
  "The letter turns to two named prophets operating among the exiles, Ahab the son of Kolaiah and "
  "Zedekiah the son of Maaseiah, and their sentence is specific and grim, he shall slay them before "
  "your eyes, and of them shall be taken up a curse, saying, The LORD make thee like Zedekiah and like "
  "Ahab, whom the king of Babylon roasted in the fire. Being made into a proverbial curse is treated "
  "as part of the penalty. The charge against them is in two parts, and have committed adultery with "
  "their neighbours' wives, and have spoken lying words in my name, which is the same pairing of "
  "conduct and falsehood as 23:14."),
 ("Shemaiah's Counter-Letter (vv.24-32)",
  "Shemaiah the Nehelamite writes back from Babylon to Jerusalem, to Zephaniah the priest, and the "
  "complaint is administrative: nobody has disciplined Jeremiah. He reminds the priest of his duties "
  "in the priest's own language, the LORD hath made thee priest, that ye should be officers in the "
  "house of the LORD, for every man that is mad, and maketh himself a prophet, that thou shouldest put "
  "him in prison, and in the stocks. And he quotes the offending sentence back as evidence, Babylon, "
  "your captivity is long, build ye houses. Zephaniah reads the letter aloud to Jeremiah, which is how "
  "it survives, and the reply is a sentence on the writer, he shall not have a man to dwell among this "
  "people, neither shall he behold the good that I will do for my people. The chapter is therefore a "
  "complete exchange of correspondence in both directions, which nothing else in the prophets is."),
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
