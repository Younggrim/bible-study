#!/usr/bin/env python3
"""
Jeremiah 30 to 36: the Book of Consolation, the field at Anathoth, and the burned
scroll. Seven pages, 207 verses. All seven sublists are gapless outlines and are
folded.

The inherited outline on jeremiah31 carried a broken label, the new COVENANT, with a
lowercase article and an emphatic capital. It is rewritten as The New Covenant, which
is the only label in this block that needed correcting rather than restyling.

Chapters 30 to 33 are marked off from the rest of the book by an instruction inside
them: write thee all the words that I have spoken unto thee in a book. They are the
most sustained stretch of hope in Jeremiah, and 31:31-34 is the longest Old Testament
passage quoted anywhere in the New, at Hebrews 8.

Chapter 36 is the closest thing in the Old Testament to an account of how a prophetic
book came to exist, and its last clause matters for anyone reading this one: the
replacement scroll was longer than the one Jehoiakim burned, and there were added
besides unto them many like words.

Usage:
    python3 fold_jeremiah_consolation.py [--check]
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
"jeremiah30": [
 ("Write All the Words in a Book (vv.1-3)",
  "Write thee all the words that I have spoken unto thee in a book, and that instruction is what marks "
  "chapters 30 to 33 off from everything around them. This is material composed as a document rather "
  "than delivered as a sermon, and it is the most sustained stretch of hope in the book. The promise "
  "names both kingdoms, I will bring again the captivity of my people Israel and Judah, which is the "
  "note the whole section keeps returning to: the reunion of a nation that had been split for three "
  "and a half centuries."),
 ("The Day of Jacob's Trouble (vv.4-9)",
  "A voice of trembling, of fear, and not of peace, and then the phrase that occurs nowhere else in "
  "scripture, alas, for that day is great, so that none is like it, it is even the time of Jacob's "
  "trouble, but he shall be saved out of it. A great deal of later interpretation has been built on "
  "those words; what the verse itself claims is a severity without parallel and a rescue that comes "
  "through it rather than instead of it. Then the yoke of chapters 27 and 28 reversed, I will break his "
  "yoke from off thy neck, and burst thy bonds, and the promise of a ruler, they shall serve the LORD "
  "their God, and David their king, whom I will raise up unto them."),
 ("Fear Thou Not, O My Servant Jacob (vv.10-11)",
  "Fear thou not, O my servant Jacob, neither be dismayed, O Israel, for I am with thee to save thee. "
  "Isaiah 41 and 43 use this formula in almost identical words. What is characteristic of Jeremiah is "
  "the clause that is not withdrawn even here, I will correct thee in measure, and will not leave thee "
  "altogether unpunished. That is the very request Jeremiah made for himself at 10:24, correct me, but "
  "with judgment, now granted to the nation. Consolation in this book always keeps the correction and "
  "argues about its size."),
 ("Thy Wound Is Incurable, and I Will Heal It (vv.12-17)",
  "The diagnosis is delivered as hopeless before anything else is said, thy bruise is incurable, and "
  "thy wound is grievous, there is none to plead thy cause, thou hast no healing medicines, all thy "
  "lovers have forgotten thee. And the cause is named, because thy sins were increased, I have wounded "
  "thee. Then the reversal comes in the same medical vocabulary, for I will restore health unto thee, "
  "and I will heal thy wounds. Notice that incurable is never retracted. A cure is supplied from "
  "outside the category rather than the prognosis being revised. And the grievance being answered is "
  "quoted, because they called thee an outcast, saying, This is Zion, whom no man seeketh after."),
 ("The City Builded Upon Her Own Heap (vv.18-22)",
  "The city shall be builded upon her own heap, and the palace shall remain after the manner thereof, "
  "which promises rebuilding on the same rubble rather than a fresh start somewhere easier. Out of them "
  "shall proceed thanksgiving, and the voice of them that make merry. Then a political clause that is "
  "easy to read past, their nobles shall be of themselves, and their governor shall proceed from the "
  "midst of them, so the restored community is to be governed from inside rather than by an imperial "
  "appointment. And the covenant formula closes it, ye shall be my people, and I will be your God."),
 ("The Whirlwind of the LORD (vv.23-24)",
  "Two verses that repeat 23:19-20 almost word for word, the whirlwind of the LORD goeth forth with "
  "fury, a continuing whirlwind, it shall fall with pain upon the head of the wicked. Ending a chapter "
  "of consolation with a storm oracle is deliberate, and it is the same instinct as 4:27 and 30:11: "
  "this book will not let comfort stand entirely by itself. The last clause is about duration rather "
  "than about fear, in the latter days ye shall consider it."),
],
"jeremiah31": [
 ("An Everlasting Love (vv.1-6)",
  "Yea, I have loved thee with an everlasting love, therefore with lovingkindness have I drawn thee. "
  "What follows is not exalted language but ordinary life resumed, thou shalt again be adorned with thy "
  "tabrets, and shalt go forth in the dances of them that make merry, thou shalt yet plant vines upon "
  "the mountains of Samaria. The mountains of Samaria are the point. This is addressed to the northern "
  "kingdom, gone for a century, and what it offers them is farming. And the last verse puts watchmen on "
  "mount Ephraim calling people up to Zion, which reunites the two kingdoms in a single sentence."),
 ("Sing with Gladness for Jacob (vv.7-14)",
  "Publish ye, praise ye, and say, O LORD, save thy people. The composition of the returning company is "
  "the substance of the passage, and the list is put together so as to exclude nobody who would "
  "normally be left behind: I will gather them from the coasts of the earth, and with them the blind "
  "and the lame, the woman with child and her that travaileth with child together, a great company "
  "shall return. The road is described accordingly, I will cause them to walk by the rivers of waters, "
  "in a straight way, wherein they shall not stumble. Then the relationship claimed, for I am a father "
  "to Israel, and Ephraim is my firstborn, and the shepherd image, he that scattered Israel will gather "
  "him. The section ends past survival, their soul shall be as a watered garden."),
 ("Rachel Weeping (vv.15-17)",
  "A voice was heard in Ramah, lamentation, and bitter weeping, Rachel weeping for her children, "
  "refused to be comforted for her children, because they were not. Rachel is the mother of Joseph and "
  "Benjamin and was buried near Bethlehem, so she stands here for the deported north, and Matthew 2 "
  "quotes the verse of the children killed at Bethlehem. What this passage does with grief is unusual "
  "and worth noticing: it does not correct the weeping or explain it away, it answers it with a reason "
  "to stop, refrain thy voice from weeping, for thy work shall be rewarded, and they shall come again "
  "from the land of the enemy."),
 ("Is Ephraim My Dear Son (vv.18-20)",
  "Ephraim is quoted repenting, and the wording of the request is careful, turn thou me, and I shall be "
  "turned, for thou art the LORD my God. He asks to be turned rather than promising to turn. Then the "
  "reply, which is the most affectionate sentence in the book, is Ephraim my dear son, is he a pleasant "
  "child, for since I spake against him, I do earnestly remember him still, therefore my bowels are "
  "troubled for him, I will surely have mercy upon him. The kingdom that began the idolatry and had "
  "been gone for a hundred and forty years is called a pleasant child."),
 ("A Woman Shall Compass a Man (vv.21-22)",
  "Set thee up waymarks, make thee high heaps, set thine heart toward the highway, that is, mark the "
  "route on the way out so it can be found on the way back. Then a clause nobody has explained "
  "satisfactorily, the LORD hath created a new thing in the earth, a woman shall compass a man. It has "
  "been read as a virgin conception, as a reversal of the usual courtship, and as the weak protecting "
  "the strong, and the honest position is that its sense is not now recoverable. What is clear is the "
  "question framing it, how long wilt thou go about, O thou backsliding daughter."),
 ("Then I Awaked (vv.23-26)",
  "The LORD bless thee, O habitation of justice, and mountain of holiness, quoted as the greeting "
  "people will use in Judah again. I have satiated the weary soul, and I have replenished every "
  "sorrowful soul. And then one line unlike anything else in the prophets, upon this I awaked, and "
  "beheld, and my sleep was sweet unto me. The prophet reports having slept well. It is the only such "
  "note in the book and it stands out in a collection this full of insomniac grief."),
 ("No More Sour Grapes (vv.27-30)",
  "I will sow them with the seed of man, and with the seed of beast. Then the six verbs of the "
  "commission in chapter 1 are quoted back with the proportion changed, like as I have watched over "
  "them, to pluck up, and to break down, and to throw down, and to destroy, and to afflict, so will I "
  "watch over them, to build, and to plant. And the proverb Ezekiel 18 deals with at length is settled "
  "here in two verses, they shall say no more, The fathers have eaten a sour grape, and the children's "
  "teeth are set on edge, but every one shall die for his own iniquity. Two prophets working at the "
  "same time, answering the same saying, the same way."),
 ("The New Covenant (vv.31-34)",
  "The passage the book is best known for, and the longest single Old Testament text quoted in the New "
  "Testament, at Hebrews 8. Behold, the days come, that I will make a new covenant with the house of "
  "Israel, and with the house of Judah, not according to the covenant that I made with their fathers, "
  "which my covenant they brake. Four things are promised and the order of them matters. A new "
  "location for the law, I will put my law in their inward parts, and write it in their hearts. The "
  "relationship formula, I will be their God, and they shall be my people. The end of an entire "
  "profession, they shall teach no more every man his neighbour, saying, Know the LORD, for they shall "
  "all know me, from the least of them unto the greatest of them. And the ground of all three, placed "
  "last so that it carries the weight, for I will forgive their iniquity, and I will remember their sin "
  "no more. Jesus uses the phrase over the cup at the last supper."),
 ("As Long as Sun and Moon (vv.35-37)",
  "The guarantee is put in cosmological terms, and the argument runs from something nobody doubts to "
  "something everybody did: the LORD which giveth the sun for a light by day, and the ordinances of the "
  "moon and of the stars for a light by night, if those ordinances depart from before me, then the seed "
  "of Israel shall also cease. Then a second guarantee framed as a task nobody can perform, if heaven "
  "above can be measured, and the foundations of the earth searched out beneath, then will I cast off "
  "all the seed of Israel. The covenant is being made as secure as the physical order, which is exactly "
  "the argument 33:20 makes about David."),
 ("The Whole Valley Shall Be Holy (vv.38-40)",
  "The last three verses are a survey, and the surveying is deliberate: the tower of Hananeel, the gate "
  "of the corner, the hill Gareb, Goath. What matters is what ends up inside the line. And the whole "
  "valley of the dead bodies, and of the ashes, and all the fields unto the brook of Kidron, shall be "
  "holy unto the LORD. That valley is Topheth, the ground chapters 7 and 19 renamed the valley of "
  "slaughter, where children had been burned. The book's most hopeful chapter ends by enclosing the "
  "worst place in the city inside the holy precinct, and it shall not be plucked up, nor thrown down "
  "any more for ever."),
],
"jeremiah32": [
 ("Siege and Imprisonment (vv.1-5)",
  "Dated the tenth year of Zedekiah, 587 BC, with the Babylonian army camped round the city and the "
  "prophet shut up in the court of the prison. The reason for the arrest is quoted from the king's own "
  "complaint and it names the offence precisely, wherefore dost thou prophesy and say, Behold, I will "
  "give this city into the hand of the king of Babylon. Everything in this chapter happens inside a "
  "prison inside a besieged city in its last months, and the setting is established first because it "
  "is what makes the transaction that follows look absurd."),
 ("The Field at Anathoth (vv.6-15)",
  "His cousin Hanameel arrives with a right of first refusal, buy thou my field that is in Anathoth, "
  "for the right of redemption is thine. Anathoth was in territory the Babylonians had already "
  "overrun, so the asset was worthless and the seller knew it. He buys it, and the conveyancing is "
  "recorded in more procedural detail than any other transaction in the Old Testament: seventeen "
  "shekels of silver, the deed sealed and a second copy left open, the witnesses, the money weighed in "
  "the balances, and the documents handed to Baruch to be put in an earthen vessel, that they may "
  "continue many days. The reason is given at the end, houses and fields and vineyards shall be "
  "possessed again in this land. It is the most expensive sermon in the book, and the only one filed "
  "with witnesses."),
 ("Nothing Too Hard for Thee (vv.16-25)",
  "The prayer after the purchase begins where these prayers usually begin, with creation, ah Lord GOD, "
  "behold, thou hast made the heaven and the earth by thy great power and stretched out arm, and there "
  "is nothing too hard for thee. It recites the exodus and the gift of the land, and states the "
  "principle of consequence without flinching, thou recompensest the iniquity of the fathers into the "
  "bosom of their children. Then it arrives at its actual subject, which is not a request but a "
  "difficulty, behold the mounts, they are come unto the city to take it, and the city is given into "
  "the hand of the Chaldeans, and thou hast said unto me, Buy thee the field for money. He has done "
  "what he was told and wants to know what it meant."),
 ("Is Any Thing Too Hard for Me (vv.26-35)",
  "The answer opens by turning his own sentence into a question, behold, I am the LORD, the God of all "
  "flesh, is there any thing too hard for me. What follows immediately is not comfort but the worst "
  "confirmed, this city shall be given into the hand of the Chaldeans, and they shall burn it with "
  "fire. Then a long recital of cause, closing on the practice this book will not stop naming, they "
  "built the high places of Baal, to cause their sons and their daughters to pass through the fire, "
  "which I commanded them not, neither came it into my mind. The rhetorical question is answered by "
  "conceding the whole catastrophe first."),
 ("Fields Shall Be Bought Again (vv.36-44)",
  "And now therefore, and the turn comes. Behold, I will gather them out of all countries, and I will "
  "bring them again unto this place, and I will cause them to dwell safely. The promises of chapter 31 "
  "are restated, they shall be my people, and I will be their God, and I will give them one heart, and "
  "one way, and I will make an everlasting covenant with them. And then the chapter comes back down to "
  "the deed in the jar, and the ordinary language of conveyancing is repeated on purpose, men shall "
  "buy fields for money, and subscribe evidences, and seal them, and take witnesses. What is being "
  "promised is not a vision. It is a functioning property market."),
],
"jeremiah33": [
 ("Call Unto Me (vv.1-3)",
  "The second word came to him while he was yet shut up in the court of the prison, which the text "
  "repeats so that the setting is not mislaid. Call unto me, and I will answer thee, and shew thee "
  "great and mighty things, which thou knowest not. The verse is usually quoted as a general promise "
  "about prayer, and its weight comes from where it was spoken: to a prisoner, in a city that had "
  "weeks left."),
 ("I Will Bring It Health and Cure (vv.4-9)",
  "It opens with the demolition already under way, houses thrown down to make defences against the "
  "mounts and the sword, and then turns, behold, I will bring it health and cure, and I will reveal "
  "unto them abundance of peace and truth. What is promised goes past restoration to reputation, and "
  "it shall be to me a name of joy, a praise and an honour before all the nations of the earth, which "
  "shall hear all the good that I do unto them, and they shall fear and tremble for all the goodness "
  "and for all the prosperity that I procure unto it. The nations are moved by the goodness rather than "
  "by the judgment, which is the reverse of the usual direction in these books."),
 ("The Voice of the Bridegroom Again (vv.10-13)",
  "The sounds cancelled at 7:34 and 16:9 are restored item by item, the voice of joy, and the voice of "
  "gladness, the voice of the bridegroom, and the voice of the bride, and one is added that was not on "
  "the original list, the voice of them that shall say, Praise the LORD of hosts, for he is good, for "
  "his mercy endureth for ever. Then the pastures fill again, and the closing image is a working "
  "detail rather than a poetic one, the flocks shall pass again under the hands of him that telleth "
  "them, which is a shepherd counting animals into the fold."),
 ("The Branch of Righteousness (vv.14-16)",
  "The promise of 23:5-6 repeated, with one change that is easy to miss. There the name The LORD Our "
  "Righteousness was given to the king. Here it is given to the city, and this is the name wherewith "
  "she shall be called, The LORD our righteousness. The title moves from the person to the place, which "
  "is the same movement Ezekiel makes in the last verse of his book when he names his city The LORD is "
  "there."),
 ("David and Levi (vv.17-22)",
  "David shall never want a man to sit upon the throne of the house of Israel, neither shall the priests "
  "the Levites want a man before me to offer burnt offerings. Then the guarantee, in the same form as "
  "31:35-37, if ye can break my covenant of the day, and my covenant of the night, then may my covenant "
  "be broken with David my servant. And the increase is measured against the two things nobody can "
  "count, as the host of heaven cannot be numbered, neither the sand of the sea measured, so will I "
  "multiply the seed of David my servant, and the Levites."),
 ("The Two Families (vv.23-26)",
  "The chapter ends by quoting something being said in the street, considerest thou not what this "
  "people have spoken, saying, The two families which the LORD hath chosen, he hath even cast them off. "
  "The two families are Israel and Judah, and the complaint is that the election has simply been "
  "cancelled. The reply is cosmological again, if my covenant be not with day and night, and if I have "
  "not appointed the ordinances of heaven and earth, then will I cast away the seed of Jacob. That is "
  "the third time in four chapters that the promise is anchored to the physical order, which is a fair "
  "measure of how badly it needed anchoring."),
],
"jeremiah34": [
 ("To Zedekiah, Thou Shalt Not Escape (vv.1-7)",
  "Dated during the siege, when the king of Babylon fought against Jerusalem and against all the cities "
  "thereof that were left, of which two are named, Lachish and Azekah. Those names are worth stopping "
  "on. The Lachish letters, ostraca excavated at the site in 1935, include a dispatch about watching "
  "for the fire signals of Azekah, written during this campaign, which puts a contemporary military "
  "message alongside this verse. The word to the king is specific and mixed, thou shalt not escape out "
  "of his hand, but shalt surely be taken, and thine eyes shall behold the eyes of the king of Babylon, "
  "and yet thou shalt die in peace, and they will burn odours for thee."),
 ("The Covenant to Release the Slaves (vv.8-11)",
  "Zedekiah had made a covenant with all the people to proclaim liberty unto them, that every man "
  "should let his manservant and his maidservant, being an Hebrew, go free. That is the law of Exodus "
  "21 and Deuteronomy 15, ignored for centuries and suddenly enforced in the middle of a siege. And "
  "then, but afterward they turned, and caused the servants and the handmaids, whom they had let go "
  "free, to return, and brought them into subjection. The reform lasted exactly as long as the danger "
  "did, and the likely trigger for the reversal is at 37:5, the Egyptian army coming north and the "
  "Babylonians briefly pulling back."),
 ("Ye Turned and Polluted My Name (vv.12-16)",
  "The charge is measured against the original statute and against the reason given for it, at the end "
  "of seven years let ye go every man his brother an Hebrew, commanded in the day that I brought them "
  "forth out of the land of Egypt, out of the house of bondmen. The parallel is the argument: people "
  "whose whole national story is being released from slavery were commanded to release slaves. Then the "
  "assessment of the recent covenant, and it credits it before condemning the reversal, ye were now "
  "turned, and had done right in my sight, in proclaiming liberty every man to his neighbour, but ye "
  "turned and polluted my name."),
 ("I Proclaim a Liberty for You (vv.17-22)",
  "The sentence is a pun and it is the bitterest in the book, behold, I proclaim a liberty for you, "
  "saith the LORD, to the sword, to the pestilence, and to the famine. They refused to release, so they "
  "are released, to three things. Then the ceremony itself is turned against them. The parties had cut "
  "a calf in two and passed between the pieces, which is the ritual behind the Hebrew idiom for cutting "
  "a covenant, so the men that have transgressed my covenant are made like that calf. And the last "
  "verse withdraws the reprieve they had been counting on, the Chaldeans shall return, and fight "
  "against this city, and take it, and burn it with fire."),
],
"jeremiah35": [
 ("Bring the Rechabites into the House of the LORD (vv.1-5)",
  "Dated in the days of Jehoiakim, which is earlier than the chapters on either side, so the "
  "arrangement here is thematic rather than chronological. Go unto the house of the Rechabites, and "
  "bring them into one of the chambers, and give them wine to drink. The Rechabites were a nomadic "
  "clan attached to Israel rather than descended from it, and they were inside Jerusalem at this point "
  "because the Babylonian advance had driven them off the land. The prophet sets out pots of wine and "
  "cups in a temple chamber and offers them a drink, which is a test dressed as hospitality."),
 ("We Will Drink No Wine (vv.6-11)",
  "They refuse, and the refusal is quoted at length with its reasoning intact: Jonadab the son of "
  "Rechab our father commanded us, saying, Ye shall drink no wine, neither ye, nor your sons for ever, "
  "neither shall ye build house, nor sow seed, nor plant vineyard, but all your days ye shall dwell in "
  "tents. Then they account for the fact that they are indoors in a city, in apparent breach of the "
  "last clause, when Nebuchadrezzar came up into the land, we said, Come, and let us go to Jerusalem "
  "for fear of the army of the Chaldeans. Two centuries and more of obedience to a family rule with no "
  "divine sanction behind it, and the one exception explained without being excused."),
 ("They Obeyed, and You Have Not (vv.12-17)",
  "The comparison is the whole point and it is stated without softening: the words of Jonadab, that he "
  "commanded his sons not to drink wine, are performed, for unto this day they drink none, but obey "
  "their father's commandment, notwithstanding I have spoken unto you, rising early and speaking, but "
  "ye hearkened not unto me. A dead ancestor's dietary rule outperformed a covenant with God. The "
  "sentence follows from it, because I have spoken unto them, but they have not heard, therefore will "
  "I bring upon Judah all the evil that I have pronounced against them."),
 ("Jonadab Shall Not Want a Man (vv.18-19)",
  "The Rechabites are given a promise in the exact wording used of the royal house three chapters "
  "earlier, because ye have obeyed the commandment of Jonadab your father, Jonadab the son of Rechab "
  "shall not want a man to stand before me for ever. A clan that was not Israelite by blood receives "
  "the formula reserved for David and for Levi, and the stated ground of it is nothing more than that "
  "they kept their word."),
],
"jeremiah36": [
 ("Write All the Words in a Roll (vv.1-4)",
  "Dated the fourth year of Jehoiakim. Take thee a roll of a book, and write therein all the words that "
  "I have spoken unto thee against Israel, and against Judah, from the days of Josiah, even unto this "
  "day. Twenty-three years of preaching to be compressed into one document, and the purpose given is "
  "not archival, it may be that the house of Judah will hear, that they may return every man from his "
  "evil way. Then the mechanism, and it is the reason this chapter matters so much, Jeremiah called "
  "Baruch the son of Neriah, and Baruch wrote from the mouth of Jeremiah all the words. This is the "
  "closest thing in the Old Testament to an account of how a prophetic book came to be a book."),
 ("Baruch Reads in the Temple (vv.5-10)",
  "I am shut up, I cannot go into the house of the LORD, therefore go thou. No reason is given for the "
  "restriction, which is characteristic of this book's reticence about its own author. Baruch reads on "
  "a fast day, from the chamber of Gemariah the son of Shaphan, in the higher court, in the ears of all "
  "the people. The timing is not incidental: a fast would have filled the courts with people in from "
  "the towns, so the reading is arranged for the largest possible audience."),
 ("The Officials Hear, and Advise Him to Hide (vv.11-19)",
  "Michaiah reports it to the princes sitting in the scribe's chamber, and they send for Baruch and "
  "have the whole thing read again. Their questions are the questions of men establishing provenance, "
  "tell us now, how didst thou write all these words at his mouth. Their reaction is fear and their "
  "conduct is protective, go, hide thee, thou and Jeremiah, let no man know where ye be. The civil "
  "officials come out of this chapter considerably better than the priests came out of chapter 26."),
 ("The King Cuts It Up and Burns It (vv.20-26)",
  "The scroll is read to Jehoiakim in the winterhouse, and the detail of the scene carries the whole "
  "judgment on him: there was a fire on the hearth burning before him, and when Jehudi had read three "
  "or four leaves, he cut it with the penknife, and cast it into the fire, until all the roll was "
  "consumed. Three or four columns at a time, methodically, with a scribe's own knife. And the contrast "
  "is stated outright, yet they were not afraid, nor rent their garments, neither the king, nor any of "
  "his servants. His father Josiah had torn his clothes on hearing a book read, at 2 Kings 22. Three "
  "men try to stop him and fail, and the arrest party sent after the author comes back "
  "empty-handed, but the LORD hid them."),
 ("Write It Again, and Add More (vv.27-32)",
  "Take thee again another roll, and write in it all the former words that were in the first roll. The "
  "sentence on Jehoiakim is precise about what he lost, he shall have none to sit upon the throne of "
  "David, and his dead body shall be cast out in the day to the heat, and in the night to the frost. "
  "And the last clause of the chapter is the one that matters most for anyone holding this book, and "
  "there were added besides unto them many like words. The replacement was longer than the original. "
  "Burning the document enlarged it, and what survives is the expanded second edition."),
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
