#!/usr/bin/env python3
"""
Folds three more complete books: Joel, Zephaniah and Malachi. Ten chapters.

Each page already carries Author, Classification, Key Themes and Historical
Context, plus a Structure: sublist giving headings and verse ranges. Those
headings are carried over, consolidated where noted, and the bullets replaced with
exposition.

Headless continuation paragraphs are appended to Historical Context, matching the
reference pages which carry none.

Six fields across the four Malachi chapters have a sentence fragment for a label
rather than a field name -- "The disputation format is distinctive:", "The second
half addresses a widespread practice:", "The chapter closes with a contrast:", "The
chapter presents the ultimate contrast:", "The closing commands are significant:".
All hold real content and are folded into the relevant section prose. Their text
also carries emphatic capitals (HEALING, BACKWARD, FORWARD, WITHOUT), which
WORKFLOW.md rules out, so the substance is rewritten in sentence case.

Consolidated because WORKFLOW.md targets 4-5 sections under 20 verses and 5-7 for
20-40:
    zephaniah1  7 -> 5      malachi1  6 -> 5
    zephaniah3  8 -> 6      malachi2  7 -> 5
                            malachi3  11 -> 6
                            malachi4  6 -> 4   (a six-verse chapter)

Follows the format in WORKFLOW.md. Writes nothing if any page fails a check.

Usage:
    python3 fold_joel_zephaniah_malachi.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"joel1": 20, "joel2": 32, "joel3": 21,
          "zephaniah1": 18, "zephaniah2": 15, "zephaniah3": 20,
          "malachi1": 14, "malachi2": 17, "malachi3": 18, "malachi4": 6}

HEADER_ORDER = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

# Sentence-fragment labels whose content is folded into section prose instead.
ABSORB = {
    "malachi1": ["The disputation format is distinctive:"],
    "malachi2": ["The second half addresses a widespread practice:"],
    "malachi3": ["The chapter closes with a contrast:"],
    "malachi4": ["The chapter presents the ultimate contrast:",
                 "The closing commands are significant:"],
}

SECTIONS = {
"joel1": [
  ("The Unprecedented Plague: Tell Your Children (vv.1-4)",
   "Joel gives no king and no date, which is why the book is hard to place and easy "
   "to apply. He opens by asking the elders whether anything like this has happened "
   "in their days or their fathers', and instructs them to tell their children, so "
   "the event is being entered into memory as it happens. Verse 4 names four waves of "
   "locust in sequence, each finishing what the last left. Whether these are four "
   "species or four stages, the effect is a description of nothing remaining."),
  ("Call to Mourn: Drunkards, Priests, Farmers (vv.5-12)",
   "The summons goes out group by group, and each is addressed through what it has "
   "lost. The drinkers have no new wine. The farmers and vinedressers are told to be "
   "ashamed, their harvest gone. The priests are told to gird themselves and lament, "
   "because the grain and drink offerings are cut off from the house of God \u2014 "
   "the plague has stopped the sacrifices, so the disaster is liturgical as well as "
   "agricultural. The list of ruined crops in v.12 ends with joy itself withered."),
  ("Call to Fast and Cry Out (vv.13-14)",
   "The instruction moves from mourning to assembly: sanctify a fast, call a solemn "
   "meeting, gather the elders and all the inhabitants into the house of the LORD, "
   "and cry to Him. Nothing is promised at this point. The response asked for is "
   "corporate and public rather than private, which is how Israel handled catastrophe "
   "it understood as more than weather."),
  ("The Day of the LORD Is Near (vv.15-18)",
   "\u201cAlas for the day! for the day of the LORD is at hand\u201d turns the locust "
   "crisis into a lens. What is in front of them becomes a preview of something "
   "larger, and this is the theme the rest of the book develops. The detail in vv.17-18 "
   "stays close to the ground \u2014 seed rotting under the clods, barns broken down, "
   "cattle wandering because there is no pasture, flocks made desolate. The animals "
   "are described as groaning, which is the verse that most often stops a reader."),
  ("Joel's Prayer: Creation Cries to God (vv.19-20)",
   "The chapter ends with the prophet praying rather than preaching: \u201cO LORD, to "
   "thee will I cry.\u201d Fire has consumed the pastures and the watercourses are "
   "dried. Verse 20 puts the beasts of the field alongside him, crying to God as well. "
   "The chapter closes without an answer, which is left for chapter 2."),
],
"joel2": [
  ("The Terrifying Army of the LORD (vv.1-11)",
   "A trumpet is blown on Zion and the language shifts from insects to invasion "
   "\u2014 a people great and strong, the like of which has not been, running like "
   "horsemen, climbing walls, marching each in his path without breaking ranks. "
   "Whether Joel is describing the locusts in military terms or moving past them to a "
   "human army is genuinely open, and the ambiguity may be deliberate. Verse 11 "
   "settles the ownership: the LORD calls this \u201chis army\u201d, which is the most "
   "disquieting line in the chapter."),
  ("Rend Your Hearts, Not Your Garments (vv.12-17)",
   "\u201cTurn ye even to me with all your heart\u201d comes with fasting, weeping "
   "and mourning, and then the correction: rend your heart and not your garments. "
   "Tearing clothes was the visible sign, and Joel does not forbid it so much as "
   "refuse to accept it alone. Verse 14's \u201cwho knoweth if he will return and "
   "repent\u201d withholds any guarantee, which makes the call to repent rest on God's "
   "character rather than on a promised outcome. The assembly gathers everyone, down "
   "to nursing infants and newly married couples otherwise exempt."),
  ("God's Response: Jealousy, Pity, Restoration (vv.18-27)",
   "The turn comes without transition: the LORD was jealous for his land and pitied "
   "his people. Grain, wine and oil are promised back, the northern army driven off, "
   "the rains restored. Verse 25 is the line the chapter is remembered for \u2014 "
   "\u201cI will restore to you the years that the locust hath eaten\u201d \u2014 and "
   "the restoration is of years rather than crops. Verse 26 adds that they shall eat "
   "and be satisfied and never be ashamed, answering the shame of chapter 1 directly."),
  ("The Promise of the Spirit (vv.28-29)",
   "\u201cAfterward\u201d moves the horizon out. The Spirit is poured on all flesh, "
   "and the categories named are the ones usually passed over: sons and daughters, "
   "old men and young men, servants and handmaids. Prophecy, dreams and visions are "
   "distributed across age, sex and status without regard to any of them. Peter quotes "
   "this at Pentecost as the explanation for what the crowd is watching."),
  ("Signs Before the Day of the LORD (vv.30-31)",
   "Blood, fire and pillars of smoke, the sun darkened and the moon turned to blood, "
   "before the great and terrible day. The imagery is cosmic where the chapter began "
   "agricultural, and it is the same day Joel has been circling since 1:15. Peter "
   "quotes these verses too, which has kept the question of their timing open ever "
   "since."),
  ("Whosoever Shall Call (v.32)",
   "The chapter ends on a single condition rather than a threat: whosoever shall call "
   "on the name of the LORD shall be delivered. Paul quotes it in Romans 10 and "
   "presses the \u201cwhosoever\u201d. The verse also names a remnant in Zion whom the "
   "LORD shall call, so calling runs in both directions in the same sentence."),
],
"joel3": [
  ("God Gathers the Nations to Judgment (vv.1-3)",
   "The chapter opens with restoration as the setting for judgment: when God brings "
   "back the captivity of Judah, He will gather all nations into the valley of "
   "Jehoshaphat \u2014 a name meaning the LORD judges, and a place no one has "
   "identified. The charge is specific rather than general: they scattered His people, "
   "divided His land, cast lots for the people, and traded a boy for a prostitute and "
   "a girl for wine. Human trafficking is named as the offence."),
  ("Specific Charges: Tyre, Sidon, Philistia (vv.4-8)",
   "Named cities are addressed directly and asked what they have to do with God. The "
   "accusation is that they took silver and gold and carried the people of Judah and "
   "Jerusalem into the slave markets, selling them to the Greeks. The sentence is "
   "reversal in kind \u2014 their own sons and daughters sold to the Sabeans, a nation "
   "far off. Judgment in Joel repeatedly returns to people what they did to others."),
  ("The Call to War: Nations Against God (vv.9-12)",
   "The proclamation inverts a famous line: beat your plowshares into swords and your "
   "pruninghooks into spears, the reverse of Isaiah and Micah. The weak are told to "
   "say they are strong. It reads as a summons the nations are welcome to answer, and "
   "v.11 asks them to gather round, at which point the tone shifts \u2014 they are "
   "assembling for judgment, not battle. Verse 12 returns to the valley where the LORD "
   "sits to judge."),
  ("The Harvest of Judgment (vv.13-16)",
   "Two harvest images do the work: the sickle put in because the crop is ripe, and "
   "the winepress trodden because it is full. Both appear again in Revelation 14. "
   "Verse 14's \u201cmultitudes, multitudes in the valley of decision\u201d is often "
   "read as people deciding for God, but the decision here is the verdict being "
   "handed down. The sun and moon darken again, and the LORD roars out of Zion while "
   "being at the same time the hope of His people."),
  ("The Eternal Kingdom: Jerusalem Holy (vv.17-21)",
   "The book ends on permanence: God dwelling in Zion, the city holy, strangers no "
   "longer passing through it. The imagery turns wet after two chapters of drought "
   "\u2014 mountains dropping new wine, hills flowing with milk, a fountain from the "
   "house of the LORD watering the valley of Shittim. Egypt and Edom are named as "
   "desolate by contrast. The final clause is the book's resolution: the LORD dwells "
   "in Zion, which is what the locusts had interrupted."),
],
"zephaniah1": [
  ("Superscription and a Royal Genealogy (v.1)",
   "Zephaniah's lineage is traced back four generations to Hizkiah, which is unusual "
   "among the prophets and is generally taken to mean Hezekiah the king. If so, "
   "Zephaniah is of royal blood and speaking against the royal house, which explains "
   "the confidence with which chapter 1 addresses princes and the king's children. The "
   "date is Josiah's reign, so before or during the reform of 622 BC."),
  ("Universal Judgment: Creation Reversed (vv.2-6)",
   "The book opens at the largest possible scale: I will utterly consume all things "
   "from off the land. The order of what is swept away \u2014 man, beast, birds, fish "
   "\u2014 runs backwards through the creation account, which makes the threat an "
   "undoing rather than a punishment. Then it narrows to Judah and Jerusalem, naming "
   "Baal, the star worship on the rooftops, and Malcham, and adding those who have "
   "simply stopped looking for the LORD at all."),
  ("The Day of the LORD as Sacrifice (vv.7-11)",
   "\u201cHold thy peace at the presence of the Lord GOD\u201d introduces the day as a "
   "sacrifice at which God has invited guests \u2014 and the guests are the ones "
   "consumed. Princes, king's children, those in foreign clothing, and those leaping "
   "over the threshold are named in turn. Verses 10-11 name real districts, the fish "
   "gate and the second quarter and Maktesh, so the judgment is mapped onto the city's "
   "actual streets rather than described in general."),
  ("Searched with Candles (vv.12-13)",
   "The image is God going through Jerusalem with lamps, looking into corners for men "
   "\u201csettled on their lees\u201d \u2014 wine left undisturbed until it thickens. "
   "Their creed is quoted: the LORD will not do good, neither will he do evil. It is "
   "not atheism but the assumption that God is indifferent, and the answer is that "
   "they will build houses and not live in them, plant vineyards and not drink the "
   "wine. Complacency gets the most precise sentence in the chapter."),
  ("The Great Day: Near and Terrible (vv.14-18)",
   "The pace tightens into a hammering list: a day of wrath, trouble, distress, "
   "wasteness, desolation, darkness, gloominess, clouds, thick darkness, trumpet and "
   "alarm. The Latin of v.15 gave the medieval hymn Dies Irae its name. Verse 18 "
   "closes the chapter by making silver and gold useless for deliverance \u2014 the "
   "one resource the complacent had counted on, ruled out in the final line."),
],
"zephaniah2": [
  ("Seek the LORD Before the Day (vv.1-3)",
   "After chapter 1 the address turns to the people with three imperatives \u2014 "
   "seek the LORD, seek righteousness, seek meekness \u2014 and one qualified hope: "
   "\u201cit may be ye shall be hid in the day of the LORD's anger.\u201d The "
   "\u201cit may be\u201d is doing real work; nothing is guaranteed and the appeal is "
   "not softened into a promise. Those addressed are the meek of the earth who have "
   "kept His judgment, so this is a word to the ones already listening."),
  ("Against Philistia: The West (vv.4-7)",
   "The oracles that follow move round the compass, and the first goes west to the "
   "Philistine cities \u2014 Gaza, Ashkelon, Ashdod, Ekron. Their coastland becomes "
   "pasture with cottages for shepherds, which is a specific kind of ruin: not "
   "flattened but repurposed, the harbour towns turned into grazing. The remnant of "
   "Judah is named as inheriting it."),
  ("Against Moab and Ammon: The East (vv.8-11)",
   "East next, and the charge is the reproach and reviling they aimed at God's people "
   "\u2014 words rather than armies. The sentence is Sodom and Gomorrah, and the "
   "stated cause in v.10 is pride. Verse 11 widens unexpectedly: the LORD will famish "
   "all the gods of the earth, and men from every coast will worship Him, so an oracle "
   "of judgment turns for a moment into a promise about the nations."),
  ("Against Cush: The South (v.12)",
   "One verse, addressed to the Ethiopians, and the brevity is itself the point after "
   "the fuller treatment given to Philistia and Moab. \u201cYe shall be slain by my "
   "sword\u201d is spoken in the first person, which keeps the agent in view even "
   "where no invading empire is named."),
  ("Against Assyria and Nineveh: The North (vv.13-15)",
   "The last oracle goes north to the superpower of the day, and it is the longest. "
   "Nineveh will be made dry like a wilderness, with flocks and wild animals lodging "
   "in it and birds in the ruined windows. The quotation in v.15 is the city's own "
   "voice \u2014 \u201cI am, and there is none beside me\u201d \u2014 a claim close "
   "enough to God's own self-description to explain the sentence. Nineveh fell in 612 "
   "BC, within a generation."),
],
"zephaniah3": [
  ("Woe to the Oppressing City (vv.1-5)",
   "After going round the compass, the oracle comes home. The city is not named at "
   "first, which makes v.2 land harder: she obeyed not, received not correction, "
   "trusted not in the LORD, drew not near to her God. Then the four groups \u2014 "
   "princes as roaring lions, judges as evening wolves, prophets light and "
   "treacherous, priests who profane the sanctuary. Verse 5 sets the just LORD in the "
   "middle of it, bringing judgment to light every morning and not failing, which is "
   "the standard the four have fallen short of."),
  ("Patience Exhausted, and \u201cWait Ye Upon Me\u201d (vv.6-8)",
   "God recalls destroying nations and leaving their streets empty, and the stated "
   "purpose was instruction: surely thou wilt fear me, thou wilt receive instruction. "
   "The next clause records that it did not work \u2014 they rose early and corrupted "
   "their doings. Verse 8's \u201cwait ye upon me\u201d is the hinge of the book. The "
   "same waiting that has meant judgment throughout is about to mean something else, "
   "and everything after this verse is promise."),
  ("Pure Speech and United Worship (vv.9-10)",
   "The first promise concerns language: I will turn to the people a pure language, "
   "that they may all call on the name of the LORD and serve Him with one consent. "
   "Given that Babel scattered speech, this reads as a reversal of it, and the "
   "gathering that follows reaches beyond the rivers of Ethiopia. Worship is described "
   "as unified rather than merely resumed."),
  ("The Humble Remnant (vv.11-13)",
   "Shame is removed, and the specific thing taken away is the proud \u2014 God "
   "removes them from the middle of the city, so what is left is an afflicted and poor "
   "people who trust in the name of the LORD. Verse 13's description is domestic and "
   "small: they shall do no iniquity, speak no lies, feed and lie down with none to "
   "make them afraid. After two and a half chapters of terror, the promise is being "
   "able to sleep."),
  ("Sing, O Daughter of Zion, and the God Who Sings (vv.14-17)",
   "The command is to sing, shout and be glad, because the judgments are taken away "
   "and the LORD is in the midst. Then v.17 turns the singing round: \u201che will "
   "rejoice over thee with joy... he will joy over thee with singing.\u201d God is "
   "described as the one doing the singing, and the phrase \u201che will rest in his "
   "love\u201d sits between the two. It is the least expected verse in the Minor "
   "Prophets and the reason this chapter is loved."),
  ("Gathered, Healed, Renowned (vv.18-20)",
   "The book closes with a list of what God undertakes to do: gather those who "
   "sorrow, save the halt, drive out the enemy, deal with those who afflicted her, and "
   "turn her shame into praise and fame among all people. \u201cAt that time will I "
   "bring you again\u201d dates it without specifying when. A book that opened by "
   "unmaking creation ends with a name restored, and the last words are that the LORD "
   "has said it."),
],
"malachi1": [
  ("Superscription: The Burden of the Word (v.1)",
   "\u201cThe burden of the word of the LORD to Israel by Malachi.\u201d The name "
   "means my messenger, which has led some to read it as a title rather than a person. "
   "The book is the last of the Old Testament and is built as a series of disputes: "
   "God states something, the people answer with \u201cwherein?\u201d or \u201chow?\u201d, "
   "and God replies with evidence. That format tells you as much as the content \u2014 "
   "this is a community that has become argumentative with God, questioning His love, "
   "His justice and His requirements while bringing Him blind and lame animals."),
  ("First Disputation: I Have Loved You (vv.2-5)",
   "The opening statement is affection and the reply is a challenge: wherein hast thou "
   "loved us? The evidence offered is Jacob and Esau, and \u201cEsau have I "
   "hated\u201d is language of election and rejection between two nations rather than "
   "a report of feeling, as the reference to Edom's territory in the next verses shows. "
   "Edom's attempts to rebuild are answered by God tearing down. The question being "
   "settled is whether Judah's reduced circumstances prove they are unloved."),
  ("Second Disputation: A Table Despised (vv.6-9)",
   "The argument moves to worship, and the logic is ordinary: a son honours his "
   "father, a servant his master, so where is God's honour? The priests ask wherein "
   "they have despised His name, and the answer is the animals \u2014 blind, lame, "
   "sick. Verse 8's test is devastating in its simplicity: offer that to your governor "
   "and see whether he accepts it. What is being exposed is not unbelief but "
   "carelessness that would be unthinkable in any other transaction."),
  ("My Name Great Among the Nations (vv.10-11)",
   "\u201cWho is there even among you that would shut the doors for nought?\u201d "
   "\u2014 God would rather the temple were closed than run like this. Then a claim "
   "that sits oddly in a book about a failing priesthood: from the rising of the sun to "
   "its going down His name shall be great among the Gentiles, with incense and a pure "
   "offering in every place. The worship God is not receiving at the altar He will "
   "receive elsewhere."),
  ("Weariness, and a Curse on the Deceiver (vv.12-14)",
   "The priests are quoted calling the service wearisome and snuffing at it, the "
   "gesture of someone bored by their own job. The chapter ends with a curse aimed "
   "precisely: not at the poor man with nothing, but at the deceiver who has a sound "
   "animal in the flock and vows it, then substitutes a damaged one. The offence is "
   "having the good thing and choosing not to give it, and the closing line is that God "
   "is a great King and His name is dreadful among the heathen."),
],
"malachi2": [
  ("Warning to the Priests (vv.1-4)",
   "The commandment is addressed to the priests directly and the threat is specific: "
   "the blessings they pronounce will be cursed, and their offerings spread on their "
   "own faces. That the man who pronounces blessing should have his words turned is a "
   "targeted judgment rather than a general one. Verse 4 states the purpose \u2014 "
   "that the covenant with Levi might stand \u2014 so the warning is described as "
   "preserving something rather than only punishing."),
  ("The Covenant with Levi and the Ideal Priest (vv.5-7)",
   "What a priest was for is set out as a standard: the law of truth in his mouth, no "
   "iniquity found in his lips, walking with God in peace, and turning many away from "
   "iniquity. Verse 7 gives the definition \u2014 the priest's lips should keep "
   "knowledge, and people should seek the law at his mouth, for he is the messenger of "
   "the LORD of hosts. The word for messenger is the same as the prophet's own name."),
  ("Priests Who Cause Others to Stumble (vv.8-9)",
   "Against that standard: ye are departed out of the way, ye have caused many to "
   "stumble at the law, ye have corrupted the covenant of Levi. The charge is not "
   "personal failure alone but damage done to others through the office. The "
   "consequence given is contempt \u2014 God has made them contemptible before the "
   "people, which is presented as the outcome of partiality in handling the law rather "
   "than as an arbitrary humiliation."),
  ("Faithlessness to Brothers, and Foreign Marriage (vv.10-12)",
   "\u201cHave we not all one father?\u201d shifts from priests to the community and "
   "names dealing treacherously with a brother as a breach of covenant. Then the "
   "specific practice: Judah has married the daughter of a strange god. Nehemiah "
   "13:23-28 describes the same problem in the same period. It is treated as two "
   "offences at once, breaking a covenant and blurring the identity that made Israel "
   "distinct."),
  ("Faithlessness in Marriage, and Wearying the LORD (vv.13-17)",
   "The altar is covered with tears and God will not regard the offering, and the "
   "reason given is what is happening at home: men divorcing the wife of their youth "
   "to marry pagan women. Marriage is called a covenant and God a witness to it, which "
   "is the ground of the argument. Verse 16's \u201che hateth putting away\u201d is "
   "explained by the image beside it, covering violence with a garment \u2014 an act "
   "of aggression dressed in legal respectability. The chapter ends with the people "
   "wearying God with words and then asking how they have done it."),
],
"malachi3": [
  ("The Messenger, and the Lord Coming to His Temple (v.1)",
   "One verse holds two arrivals. A messenger is sent to prepare the way, and then the "
   "Lord himself comes suddenly to his temple \u2014 the one they are said to be "
   "seeking and delighting in. All four Gospels apply the first half to John the "
   "Baptist. The word rendered messenger is again the prophet's own name, and the "
   "coming is answered in the next verse with a question rather than a welcome."),
  ("The Refiner's Fire: Who Shall Stand? (vv.2-5)",
   "\u201cWho may abide the day of his coming?\u201d The images are a refiner's fire "
   "and fuller's soap, both of which work by removing rather than destroying, and the "
   "refiner is described as sitting \u2014 the posture of someone watching a crucible "
   "closely. The first to be purified are the sons of Levi, so judgment begins at the "
   "altar. Verse 5 lists who God will be a swift witness against, and sorcerers and "
   "adulterers stand beside those who oppress the hired worker, the widow, the "
   "fatherless and the stranger."),
  ("I Change Not, and Return to Me (vv.6-7)",
   "\u201cFor I am the LORD, I change not; therefore ye sons of Jacob are not "
   "consumed.\u201d Their survival is credited to God's constancy rather than to their "
   "own improvement. The invitation follows \u2014 return unto me, and I will return "
   "unto you \u2014 and so does the now-familiar reply: wherein shall we return? The "
   "question is asked in genuine puzzlement, which is the condition the whole book "
   "diagnoses."),
  ("Will a Man Rob God? (vv.8-9)",
   "The answer to \u201cwherein\u201d is put as a question of its own: will a man rob "
   "God? Yet ye have robbed me. Asked how, the reply is tithes and offerings. The "
   "charge is corporate \u2014 \u201cye have robbed me, even this whole nation\u201d "
   "\u2014 and it connects the shabby sacrifices of chapter 1 to something the whole "
   "community, not only the priests, was doing."),
  ("The Open Windows of Heaven (vv.10-12)",
   "\u201cProve me now herewith\u201d is the one place in Scripture where God invites "
   "a test of this kind, and what is promised is the windows of heaven opened and a "
   "blessing there is not room to receive. The context is agricultural and covenantal "
   "rather than a general principle of return on investment: the devourer is rebuked, "
   "the vine does not cast its fruit, and the nations call them blessed. The promise "
   "answers the ruined harvests the community had taken as evidence God did not care."),
  ("The Cynics and the Book of Remembrance (vv.13-18)",
   "The last dispute is the bleakest: it is vain to serve God, and the proud are "
   "called happy. Against that, v.16 records those who feared the LORD speaking to one "
   "another, and God listening and writing a book of remembrance. They are called His "
   "jewels, and the promise is that the difference between serving God and not will "
   "become visible. The chapter ends by stating that the distinction will be seen, "
   "which is precisely what the cynics said it never would be."),
],
"malachi4": [
  ("The Day Burning Like an Oven (v.1)",
   "The final chapter is six verses and opens on a furnace. The proud and the wicked "
   "are stubble, and what is left is neither root nor branch \u2014 an agricultural "
   "way of saying nothing remains to grow back. The same day that closes the chapter "
   "with healing begins it with burning, and the difference between the two outcomes "
   "is not the day but who is standing in it."),
  ("The Sun of Righteousness, with Healing (vv.2-3)",
   "For those who fear His name the same dawn brings the Sun of righteousness rising "
   "with healing in his wings, and the image that follows is oddly domestic: they go "
   "out and grow up like calves let out of a stall. It is a picture of release rather "
   "than triumph. Verse 3 does describe the wicked trodden as ashes underfoot, so the "
   "chapter holds both without softening either."),
  ("Remember the Law of Moses (v.4)",
   "The instruction looks backwards: remember the law of Moses my servant, commanded "
   "in Horeb. Nothing new is added. At the close of the Old Testament the community is "
   "pointed to what it already has, which fits a book whose complaint throughout has "
   "been neglect rather than ignorance."),
  ("Elijah Is Coming, and the Last Word (vv.5-6)",
   "Then the book looks forward: Elijah will be sent before the great and dreadful "
   "day, to turn the hearts of fathers to children and children to fathers. So the "
   "Old Testament ends suspended between memory and expectation, law and promise. Its "
   "final word is \u201ccurse\u201d, and it functions as a warning of what remains "
   "without that turning of hearts rather than as a threat \u2014 the closing note is "
   "of something unfinished. Jesus identifies John the Baptist with this Elijah, some "
   "four centuries later."),
],
}


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body = pane.group(2)

        absorb_labels = ABSORB.get(page, [])
        fields, extra, absorbed = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', body, re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in HEADER_ORDER:
                fields[name] = rest
            elif name is not None and name in absorb_labels:
                absorbed.append(name)
            elif name is None and rest == "Structure:":
                pass
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in HEADER_ORDER:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in absorb_labels:
            if want not in absorbed:
                problems.append(f"{page}: expected to absorb {want!r}, not found")

        if extra:
            fields["Historical Context:"] = " ".join(
                [fields.get("Historical Context:", "")] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged into "
                         f"Historical Context")
        if absorbed:
            notes.append(f"{page}: {len(absorbed)} fragment-labelled field(s) folded "
                         f"into section prose")

        sections = SECTIONS[page]
        covered = set()
        for head, prose in sections:
            if "*" in prose:
                problems.append(f"{page}: markdown asterisk in prose")
            if re.search(r"\b[A-Z]{3,}\b", re.sub(r"LORD|GOD|OT|NT|BC|AD", "", prose)):
                problems.append(f"{page}: emphatic capitals in {head!r}")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)",
                                 head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                covered |= set(range(a, z + 1))
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for want in HEADER_ORDER:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if "auth-sublist" in new:
            problems.append(f"{page}: sublist survived")
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
