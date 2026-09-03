#!/usr/bin/env python3
"""
Jeremiah 46 to 52: the oracles against the nations, and the appendix. Seven pages,
225 verses. All seven sublists are gapless outlines and are folded.

Two things are worth setting out before the sections. Babylon gets a hundred and ten
verses across chapters 50 and 51, more than any other nation receives in any prophetic
book, and the reason is that this is the empire Jeremiah had spent forty years telling
Judah to submit to. Submission was never approval, and 51:20-26 states the difficulty
without resolving it: Babylon is my battle axe, and I will render unto Babylon all the
evil that they have done in Zion. The instrument is held accountable for the work it
was used for, and the book does not untie that knot.

And the pattern of these oracles is judgment followed by a future. Moab, Ammon and
Elam each close on a promise to bring again their captivity. Edom and Damascus do not,
and neither does Babylon.

The last thing in the book before the appendix is a filing instruction: the scroll
describing Babylon's fall is to be read aloud in Babylon, weighted with a stone, and
sunk in the Euphrates.

Usage:
    python3 fold_jeremiah_nations.py [--check]
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
"jeremiah46": [
 ("Egypt at Carchemish (vv.1-12)",
  "Dated against Pharaoh-necho at the river Euphrates in Carchemish, which Nebuchadrezzar smote in the "
  "fourth year of Jehoiakim, so 605 BC. The battle is described from inside the Egyptian army and "
  "largely in its own orders, order ye the buckler and shield, harness the horses, furbish the spears, "
  "put on the brigandines. Then the rout, wherefore have I seen them dismayed and turned away back, "
  "they are fled apace, and looked not back. The mocking image is drawn from the Nile itself, Egypt "
  "riseth up like a flood, and his waters are moved like the rivers, because a flood that rises every "
  "year also goes down every year. Carchemish is the battle that settled who would rule the Near East "
  "for the next seventy years, and everything that happens to Judah in this book follows from it."),
 ("Nebuchadrezzar Comes to Egypt (vv.13-26)",
  "A second oracle, and this one reaches the delta towns where the refugees of chapter 43 had settled, "
  "declare ye in Egypt, publish in Migdol, publish in Noph and in Tahpanhes. The mercenaries are "
  "described leaving, the hired men in the midst of her are like fatted bullocks, for they also are "
  "turned back, and are fled away together, they did not stand. Egypt is a very fair heifer, but "
  "destruction cometh out of the north. The invaders are described as loggers, they shall cut down her "
  "forest, because they are more than the grasshoppers. The gods are named in the sentence alongside "
  "the government, I will punish Amon of No, and Pharaoh, and Egypt, with their gods, and their kings. "
  "And then a clause that is easy to miss, and afterward they shall dwell as in the days of old. Egypt "
  "is sentenced and not ended, which is the same restraint Ezekiel 29 shows."),
 ("Fear Not, O My Servant Jacob (vv.27-28)",
  "Two verses lifted almost word for word out of 30:10-11 and set at the end of the first foreign "
  "oracle. The placement is deliberate. The moment the book turns outward to the nations, it stops to "
  "distinguish the two cases, for I will make a full end of all the nations whither I have driven thee, "
  "but I will not make a full end of thee. And the qualification travels with the comfort as it always "
  "does in this book, but I will correct thee in measure."),
],
"jeremiah47": [
 ("Waters Rise Out of the North (vv.1-4)",
  "Against the Philistines, before that Pharaoh smote Gaza. The invasion is a flood, behold, waters "
  "rise up out of the north, and shall be an overflowing flood, and shall overflow the land. Then a "
  "detail about what the noise of it does, at the noise of the stamping of the hoofs of his strong "
  "horses, the fathers shall not look back to their children for feebleness of hands. A parent who "
  "does not turn round for a child is the measure of the panic, and it is a more exact one than any "
  "casualty figure. The oracle reaches past Philistia to the Phoenician ports, to cut off Tyrus and "
  "Zidon, and names the Philistines' place of origin, the remnant of the country of Caphtor, which is "
  "Crete."),
 ("How Long Wilt Thou Be Quiet (vv.5-7)",
  "Baldness is come upon Gaza, Ashkelon is cut off with the remnant of their valley. Then the prophet "
  "turns and addresses the sword itself, and it is the most humane note in these chapters, O thou sword "
  "of the LORD, how long will it be ere thou be quiet, put up thyself into thy scabbard, rest, and be "
  "still. And the answer refuses the request, how can it be quiet, seeing the LORD hath given it a "
  "charge. The oracle asks for the violence to stop and then explains why it cannot, which is the shape "
  "of a great deal of this book."),
],
"jeremiah48": [
 ("Woe unto Nebo, City by City (vv.1-10)",
  "The oracle opens as a gazetteer, and the names come faster than any commentary can follow, Nebo, "
  "Kiriathaim, Misgab, Heshbon, Madmen, Horonaim. What Moab loses is named specifically and it is the "
  "trade the nation was known for, the plains also shall be destroyed, and the vine of Sibmah. And in "
  "the middle of it a verse that has troubled readers for centuries, cursed be he that keepeth back his "
  "sword from blood, which places a curse on restraint in carrying out the sentence."),
 ("Never Emptied from Vessel to Vessel (vv.11-13)",
  "Moab hath been at ease from his youth, and hath settled on his lees, and hath not been emptied from "
  "vessel to vessel, neither hath he gone into captivity, therefore his taste remained in him, and his "
  "scent is not changed. The image is winemaking: wine left undisturbed on its sediment holds its "
  "character and never improves, and Moab has never been decanted. What is charged against it is never "
  "having been deported. It is the most original accusation in these chapters, and it is brought "
  "against a nation whose only offence in this section is having been comfortable."),
 ("Moab's Strength Broken (vv.14-20)",
  "How say ye, We are mighty, and strong men for the war. The fall is reported with an eye on the "
  "audience for it, all ye that are about him, bemoan him, and all ye that know his name, say, How is "
  "the strong staff broken. Then an instruction that reads strangely in a judgment oracle, ask her that "
  "fleeth, and her that escapeth, and say, What is done. Interview the refugees. The oracle sends people "
  "to get the account from the survivors rather than delivering it itself."),
 ("The Cities of the Plain (vv.21-28)",
  "A second gazetteer, Holon, Jahazah, Dibon, Beth-diblathaim, Beth-gamul, Beth-meon, Kerioth, Bozrah, "
  "and the charge underneath all of them stated once, because he magnified himself against the LORD. "
  "Then advice drawn from the terrain, O ye that dwell in Moab, leave the cities, and dwell in the rock, "
  "and be like the dove that maketh her nest in the sides of the hole's mouth. Moab is limestone gorge "
  "country, and what is being recommended is to live in it like a bird."),
 ("The Pride of Moab (vv.29-30)",
  "Two verses that work by piling the words up, we have heard the pride of Moab, his loftiness, and his "
  "arrogancy, and his pride, and the haughtiness of his heart. Five terms for one thing inside a single "
  "verse. The chapter's diagnosis is delivered by repetition rather than by argument, which is a device "
  "it uses again in the next section for the opposite emotion."),
 ("I Will Cry for Moab (vv.31-39)",
  "This is what makes the chapter unusual among the foreign oracles. Therefore will I howl for Moab, and "
  "I will cry out for all Moab, mine heart shall mourn for the men of Kir-heres. The grief is God's own, "
  "not merely the prophet's. What is mourned is a specific sound going quiet, I have caused wine to fail "
  "from the winepresses, none shall tread with shouting, their shouting shall be no shouting, that is, "
  "the harvest songs stopping. Mine heart shall sound for Moab like pipes. A judgment oracle in which "
  "the judge laments at greater length than he threatens."),
 ("The Eagle Spread over Moab (vv.40-44)",
  "He shall fly as an eagle, and shall spread his wings over Moab. Then a verse taken almost exactly "
  "from Isaiah 24, he that fleeth from the fear shall fall into the pit, and he that getteth up out of "
  "the pit shall be taken in the snare. Each escape opens onto the next trap, which describes the "
  "structure of the sentence rather than the sequence of one battle."),
 ("Yet Will I Bring Again the Captivity of Moab (vv.45-47)",
  "A fire is gone out of Heshbon, and a flame from the midst of Sihon, and woe be unto thee, O Moab, the "
  "people of Chemosh perisheth. And then the last verse turns entirely, yet will I bring again the "
  "captivity of Moab in the latter days, saith the LORD. Forty-six verses of judgment on a hostile "
  "neighbour, closing on restoration. The same clause is given to Ammon at 49:6 and to Elam at 49:39, so "
  "the pattern in these chapters is judgment and then a future, and it is worth noticing which nations "
  "do not get it."),
],
"jeremiah49": [
 ("Against Ammon (vv.1-6)",
  "Hath Israel no sons, hath he no heir, why then doth their king inherit Gad. The charge is territorial "
  "and precise: Ammon had moved into the land of Gad after the northern tribes were deported, which is "
  "opportunism at a neighbour's funeral, the same offence Edom is charged with at 49:7 and Ammon itself "
  "at 25:1. Wherefore gloriest thou in the valleys. And the oracle closes with the reversal, and "
  "afterward I will bring again the captivity of the children of Ammon."),
 ("Against Edom (vv.7-22)",
  "The longest of these oracles after Moab's, and much of it runs parallel to Obadiah closely enough "
  "that both are usually taken to draw on a common source. Is wisdom no more in Teman, is their counsel "
  "perished. The taunt about thoroughness is the memorable part, if grapegatherers came to thee, would "
  "they not leave some gleaning grapes, if thieves by night, they will destroy till they have enough, "
  "but I have made Esau bare. Then the charge, which is Obadiah's charge, thy terribleness hath "
  "deceived thee, and the pride of thine heart, O thou that dwellest in the clefts of the rock, that "
  "holdest the height of the hill. The cliff city behind that line is the site later known as Petra. "
  "Though thou shouldest make thy nest as high as the eagle, I will bring thee down from thence. Edom "
  "gets no closing promise of restoration."),
 ("Against Damascus (vv.23-27)",
  "Hamath is confounded, and Arpad, for they have heard evil tidings, they are fainthearted. The city is "
  "described as a person losing composure rather than as a fortress falling, how is the city of praise "
  "not left, the city of my joy, and then sorrows have taken her, as a woman in travail. Five verses for "
  "one of the oldest continuously inhabited cities in the world, and no restoration clause attached to "
  "them."),
 ("Against Kedar and Hazor (vv.28-33)",
  "The target here is a way of life rather than a city. Arise ye, go up to the wealthy nation, that "
  "dwelleth without care, which have neither gates nor bars, which dwell alone. Nomads with no walls "
  "are described as straightforward plunder, their tents and their flocks shall they take away. What "
  "they lose is the thing that had kept them safe, and the phrase used of their security, they dwell "
  "without care, is the same phrase Ezekiel 38 uses of restored Israel when Gog decides it is worth "
  "attacking."),
 ("Against Elam (vv.34-39)",
  "Dated in the beginning of the reign of Zedekiah. Behold, I will break the bow of Elam, the chief of "
  "their might. Elam's archers were the one thing the nation was militarily known for, so the sentence "
  "removes its reputation rather than its territory. And the oracle ends as Moab's and Ammon's did, but "
  "it shall come to pass in the latter days, that I will bring again the captivity of Elam."),
],
"jeremiah50": [
 ("Babylon Is Taken, Bel Is Confounded (vv.1-3)",
  "Declare ye among the nations, and publish, and say, Babylon is taken, Bel is confounded, Merodach is "
  "broken in pieces. What follows over two chapters is a hundred and ten verses, more than any other "
  "nation receives in any prophetic book, and the reason is the position this book has held for forty "
  "years. Jeremiah had told Judah to submit to Babylon, had called Nebuchadrezzar God's servant three "
  "times, and had been called a traitor for it. These two chapters are where the book makes clear that "
  "submission was never approval."),
 ("Israel and Judah Come Weeping (vv.4-7)",
  "In those days the children of Israel shall come, they and the children of Judah together, going and "
  "weeping, and they shall ask the way to Zion. Both kingdoms again, travelling together. Then the "
  "diagnosis of how they were lost, my people hath been lost sheep, their shepherds have caused them to "
  "go astray. And a sentence quoted from their captors which the oracle lets stand without correcting "
  "it, all that found them have devoured them, and their adversaries said, We offend not, because they "
  "have sinned against the LORD. The enemies were right about that. It does not make them innocent, and "
  "the next section is why."),
 ("Flee Out of the Midst of Babylon (vv.8-10)",
  "Remove out of the land of the Chaldeans, and be as the he goats before the flocks, that is, go out "
  "in front rather than waiting to be driven. The instruction to leave is repeated through both "
  "chapters and is quoted in Revelation 18 of a different Babylon. The agent is described as a "
  "coalition, I will raise and cause to come up against Babylon an assembly of great nations from the "
  "north country."),
 ("Because Thou Rejoicedst (vv.11-16)",
  "Because thou wast glad, because thou rejoicedst, O ye destroyers of mine heritage. That is the "
  "charge, and it is worth reading carefully, because it is not the conquest. The conquest had been "
  "commissioned. What is charged is the pleasure taken in it, which is precisely the charge brought "
  "against Edom at 49:7 and against Ammon and Moab at 48:27. Then the reversal of the mother image, "
  "your mother shall be sore confounded, and a practical instruction to the attackers, all ye that bend "
  "the bow, shoot at her, spare no arrows."),
 ("Israel Is a Scattered Sheep (vv.17-20)",
  "Israel is a scattered sheep, the lions have driven him away, first the king of Assyria hath devoured "
  "him, and last this king of Babylon hath broken his bones. Two empires named as two predators in "
  "sequence, which is the whole political history of the nation in one sentence. Then a restoration "
  "stated in extravagant terms, in those days, and in that time, the iniquity of Israel shall be sought "
  "for, and there shall be none, and the sins of Judah, and they shall not be found, for I will pardon "
  "them whom I reserve. Not forgiven so much as unfindable."),
 ("Go Up Against the Land of Merathaim (vv.21-32)",
  "A long summons to the attackers, and in the middle of it the hammer image of 23:29 is taken off "
  "God's word and applied to the empire, how is the hammer of the whole earth cut asunder and broken. "
  "The charge is compressed into one clause, because thou hast striven against the LORD, and the reply "
  "into another, behold, I am against thee, O thou most proud, and thy day is come."),
 ("Their Redeemer Is Strong (vv.33-34)",
  "Two verses, and they turn on a legal term. The children of Israel and the children of Judah were "
  "oppressed together, and all that took them captives held them fast, they refused to let them go. "
  "Then, their Redeemer is strong, the LORD of hosts is his name, he shall throughly plead their cause. "
  "A redeemer in Israelite law is the relative obliged to buy a family member out of debt or slavery, "
  "the office Boaz performs in Ruth, and it is applied here to God as the party bringing the suit."),
 ("A Sword upon the Chaldeans (vv.35-40)",
  "A sword is called for against each institution in turn, the princes, the wise men, the liars, the "
  "mighty men, the horses and the chariots, the treasures, and the waters. The list takes a nation "
  "apart by function rather than by geography. And the comparison the section closes on is the strongest "
  "available, as God overthrew Sodom and Gomorrah, so shall no man dwell there, neither shall any son "
  "of man dwell therein."),
 ("A People Shall Come from the North (vv.41-46)",
  "These verses are taken almost word for word from 6:22-24, where they described the enemy coming "
  "against Jerusalem. Here they describe the enemy coming against Babylon. The same sentences, the same "
  "cruelty, the same terror, with the direction reversed: behold, a people shall come from the north, "
  "they are cruel, and will not shew mercy. The book's last word on empire is to reuse its own language "
  "about the invasion of Judah, unaltered, against the invader."),
],
"jeremiah51": [
 ("A Destroying Wind (vv.1-10)",
  "I will raise up against Babylon a destroying wind, and will send unto Babylon fanners, that shall fan "
  "her. Then the reason for all of it stated as a matter of record, for Israel hath not been forsaken, "
  "nor Judah of his God. And a verse that reads as an epitaph on an entire civilisation, we would have "
  "healed Babylon, but she is not healed, forsake her, and let us go every one into his own country."),
 ("The Kings of the Medes (vv.11-14)",
  "The LORD hath raised up the spirit of the kings of the Medes, for his device is against Babylon, to "
  "destroy it, because it is the vengeance of the LORD, the vengeance of his temple. Naming the Medes is "
  "a specific claim, and Babylon did fall to a Medo-Persian force in 539 BC. The oath behind it is sworn "
  "on nothing external, the LORD of hosts hath sworn by himself, saying, Surely I will fill thee with "
  "men, as with caterpillars."),
 ("He Hath Made the Earth by His Power (vv.15-19)",
  "The creation doxology from 10:12-16 repeated word for word, including the workshop satire, every "
  "founder is confounded by the graven image, and closing on the covenant name, the portion of Jacob, "
  "the LORD of hosts is his name. Repeating it here does the same work it did in chapter 10 and it "
  "does it against a bigger target: the empire's gods are set beside the maker of the world and the "
  "comparison is left to argue for itself."),
 ("My Battle Axe, Now Broken (vv.20-26)",
  "Thou art my battle axe and weapons of war, for with thee will I break in pieces the nations. The "
  "phrase with thee will I break in pieces is then repeated down a list of everything a country "
  "contains, horse and rider, chariot and driver, man and woman, old and young, shepherd and "
  "husbandman. And then the turn, and I will render unto Babylon all the evil that they have done in "
  "Zion. The instrument is held to account for the work it was used to do. That is the hardest "
  "theological knot in the book, and it is not untied here or anywhere else. It is stated twice and "
  "left standing."),
 ("Set Up a Standard (vv.27-33)",
  "Call together against her the kingdoms of Ararat, Minni, and Ashchenaz. The defenders are described "
  "as having given up before the engagement, the mighty men of Babylon have forborn to fight, they have "
  "remained in their holds, their might hath failed. And there is a detail about how the news reaches "
  "the palace, one post shall run to meet another, to shew the king of Babylon that his city is taken at "
  "one end. The couriers overtake each other."),
 ("Nebuchadrezzar Hath Swallowed Me Up (vv.34-40)",
  "The voice becomes Zion's and the metaphor is digestion, Nebuchadrezzar the king of Babylon hath "
  "devoured me, he hath crushed me, he hath swallowed me up like a dragon. The reply is in the same "
  "terms, I will punish Bel in Babylon, and I will bring forth out of his mouth that which he hath "
  "swallowed up. And then a banquet that is not one, I will make them drunken, that they may rejoice, "
  "and sleep a perpetual sleep, and not wake."),
 ("How Is Sheshach Taken (vv.41-44)",
  "Sheshach is the cipher for Babylon already used at 25:26. The sea is come up upon Babylon, she is "
  "covered with the multitude of the waves thereof, which is metaphor rather than geography, since "
  "Babylon sat on a plain. The reversal is in the last verse and it answers the swallowing of the "
  "previous section, and the nations shall not flow together any more unto him."),
 ("My People, Go Ye Out (vv.45-48)",
  "My people, go ye out of the midst of her, and deliver ye every man his soul from the fierce anger of "
  "the LORD. Then some unusually practical advice about how to live through a long collapse, and lest "
  "your heart faint, and ye fear for the rumour that shall be heard in the land, for a rumour shall "
  "come one year, and after that in another year a rumour. The fall of an empire takes years and "
  "arrives as a series of conflicting reports, and they are told in advance not to read each year's "
  "rumour as the end of the story."),
 ("As Babylon Hath Caused the Slain (vv.49-53)",
  "As Babylon hath caused the slain of Israel to fall, so shall all the earth be slain at Babylon. Then "
  "a word to the exiles about where their attention should be, ye that have escaped the sword, go away, "
  "stand not still, remember the LORD afar off, and let Jerusalem come into your mind. And the futility "
  "of fortification, though Babylon should mount up to heaven, and though she should fortify the height "
  "of her strength, yet from me shall spoilers come unto her."),
 ("The Broad Walls Shall Be Utterly Broken (vv.54-58)",
  "A sound of a cry cometh from Babylon, and great destruction from the land of the Chaldeans. Then the "
  "specific claim, the broad walls of Babylon shall be utterly broken, and her high gates shall be "
  "burned with fire. Herodotus describes those walls as wide enough to turn a four-horse chariot on the "
  "top, and they were the most famous fortification in the world when this was written. The section "
  "closes on a proverb about wasted effort, the people shall labour in vain."),
 ("The Book Cast into the Euphrates (vv.59-64)",
  "The last thing in the book before the appendix, and it is a filing instruction. Seraiah the son of "
  "Neriah, who is Baruch's brother, is travelling to Babylon with Zedekiah in the fourth year, and "
  "Jeremiah writes all this evil in a book and hands it to him with orders: when thou comest to "
  "Babylon, read all these words, then bind a stone to it, and cast it into the midst of Euphrates, and "
  "say, Thus shall Babylon sink, and shall not rise. The final sign-act in the book is the destruction "
  "of the document that describes it, performed in the enemy capital by a man who had to carry it there "
  "to do it. And then the editorial seam, thus far are the words of Jeremiah."),
],
"jeremiah52": [
 ("Zedekiah's Reign (vv.1-3)",
  "Zedekiah was one and twenty years old when he began to reign, and he reigned eleven years in "
  "Jerusalem, and he did that which was evil in the eyes of the LORD. This chapter is an appendix. It "
  "comes from the same source as 2 Kings 24 and 25 and is largely identical to it, and it is here "
  "because the words of Jeremiah ended at 51:64 and somebody thought the reader should still be told "
  "how it came out."),
 ("The Siege (vv.4-5)",
  "The ninth year, tenth month, tenth day, Nebuchadrezzar came, and all his army, and pitched against "
  "it, and built forts against it round about. So the city was besieged unto the eleventh year of king "
  "Zedekiah. Eighteen months in two verses, which is the proportion a chronicle keeps and the reverse "
  "of the proportion the rest of this book keeps."),
 ("The Breach, the Flight and the Capture (vv.6-11)",
  "In the fourth month, the ninth day of the month, the famine was sore in the city, so that there was "
  "no bread for the people of the land. Then the flight by night through the gate between the two walls, "
  "the capture in the plains of Jericho, and the sentence at Riblah, they slew the sons of Zedekiah "
  "before his eyes, then he put out the eyes of Zedekiah, and bound him in chains, and carried him to "
  "Babylon, and put him in prison till the day of his death."),
 ("The Temple Burned (vv.12-14)",
  "In the fifth month, in the tenth day of the month, came Nebuzar-adan, and burned the house of the "
  "LORD, and the king's house, and all the houses of Jerusalem, and all the walls of Jerusalem round "
  "about were broken down. That date is the one the Jewish calendar still keeps as the ninth of Av, the "
  "fast for the destruction of both temples, and it is fixed by this verse and its parallel in Kings."),
 ("The Deportation (vv.15-16)",
  "The poor of the people, and the residue, and the fugitives, and the rest of the multitude, carried "
  "away captive. And then the same clause that starts chapter 40's whole story, but Nebuzar-adan left "
  "certain of the poor of the land for vinedressers and for husbandmen. The people at the bottom stay, "
  "and are given the vineyards."),
 ("The Vessels Catalogued (vv.17-23)",
  "The longest passage in the chapter is an inventory, and the disproportion is worth asking about. The "
  "pillars, the bases, the brasen sea, the pots, the shovels, the snuffers, the bowls and the spoons, "
  "and then the two pillars measured to the cubit with the pomegranates counted, ninety and six on a "
  "side and a hundred on the network. A chronicle that gave eighteen months of siege two verses gives "
  "the temple furniture seven. The reason is at the other end of the exile: Ezra 1 records these objects "
  "being brought back and counted again. Somebody kept the list."),
 ("Executed at Riblah (vv.24-27)",
  "Seraiah the chief priest, Zephaniah the second priest, three door keepers, the officer set over the "
  "men of war, and threescore men of the people of the land, taken to Riblah and killed there. This is "
  "the event Ezekiel 11:10 had described in advance in one clause, I will judge you in the border of "
  "Israel, and Riblah is on the northern border."),
 ("The Deportation Numbers (vv.28-30)",
  "Three deportations counted separately, three thousand and twenty and three in the seventh year, eight "
  "hundred thirty and two in the eighteenth, seven hundred forty and five in the twenty-third, all the "
  "persons were four thousand and six hundred. The figures are much lower than the totals in 2 Kings and "
  "are generally taken to count adult men only. A book of this length ends its history with an audit "
  "total."),
 ("Jehoiachin at the King's Table (vv.31-34)",
  "The book ends on a meal. In the seven and thirtieth year of the captivity, Evil-merodach king of "
  "Babylon brought Jehoiachin out of prison, and spake kindly to him, and set his throne above the "
  "throne of the kings that were with him, and changed his prison garments, and he did continually eat "
  "bread before him all the days of his life. Babylonian administrative tablets excavated at the city "
  "record rations issued to Yaukin, king of the land of Yahud, which is this man under his own name, so "
  "the last scene in the book has independent documentation. It is not a restoration. Nothing is given "
  "back and nobody goes home. What it establishes is that the line Jeremiah had said would lose the "
  "throne was still alive, out of prison, and eating at the emperor's table, which for a book that ends "
  "in exile is as much of an ending as it is prepared to give."),
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
