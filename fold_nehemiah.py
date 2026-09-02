#!/usr/bin/env python3
"""
Completes Nehemiah: all thirteen chapters.

No sublists, so sections are written from the text. Nehemiah is largely a first-person
memoir and divides by episode, which makes the breaks clear.

Two chapters are registers. nehemiah7 is a 73-verse census that nearly duplicates
Ezra 2, and nehemiah11 and 12 carry settlement and genealogical lists, so those are
sectioned by the list's own organising principle rather than forced into narrative.

Two fragment-labelled fields folded into the sections covering the same material:
"The commitments are remarkably specific:" and "Nehemiah's responses are
characteristically direct:".

Usage:
    python3 fold_nehemiah.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"nehemiah1": 11, "nehemiah2": 20, "nehemiah3": 32, "nehemiah4": 23,
          "nehemiah5": 19, "nehemiah6": 19, "nehemiah7": 73, "nehemiah8": 18,
          "nehemiah9": 38, "nehemiah10": 39, "nehemiah11": 36, "nehemiah12": 47,
          "nehemiah13": 31}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Historical Context:"]

DROP = {
    "nehemiah10": ["The commitments are remarkably specific:"],
    "nehemiah13": ["Nehemiah&#x27;s responses are characteristically direct:"],
}

GENRE = "Historical Narrative \u2014 Post-Exilic Memoir"

THEMES = {
"nehemiah1": "A cupbearer with daily access to a king, news that arrives four months "
  "before anything is said about it, mourning before petition, and a prayer that quotes "
  "God's own promise back to him",
"nehemiah2": "Sadness shown before a king at personal risk, a prayer lifted between a "
  "question and its answer, requests specific enough to prove months of planning, and a "
  "wall inspected at night before anyone is told",
"nehemiah3": "Forty teams named with the section each built, a high priest working "
  "alongside goldsmiths and perfumers, daughters recorded among the builders, men "
  "building opposite their own houses, and one group who would not work",
"nehemiah4": "Opposition escalating from mockery to conspiracy to discouragement from "
  "within, prayer paired with a posted guard at every stage, families stationed by their "
  "own gaps, and a trowel in one hand with a weapon in the other",
"nehemiah5": "Exploitation found inside the community while enemies waited outside, "
  "usury and debt-slavery among brothers, an assembly called against the nobles, and a "
  "governor who declined his allowance for twelve years",
"nehemiah6": "Four invitations to a meeting that was an ambush, an open letter designed "
  "to be read by others, a prophet paid to give bad counsel, a refusal that names the "
  "work as the reason, and fifty-two days",
"nehemiah7": "A wall finished and a city still empty, command delegated to two men, a "
  "register recovered rather than compiled, descent that some could not prove, and "
  "giving recorded by household",
"nehemiah8": "A book asked for rather than imposed, six hours of reading from a wooden "
  "platform, Levites who gave the sense, weeping redirected into feasting, and a feast "
  "kept as it had not been since Joshua",
"nehemiah9": "The longest prayer in the Old Testament, history recited as a cycle of "
  "faithfulness against rebellion, God called ready to pardon in the middle of the "
  "indictment, justice conceded to be on God's side, and a covenant proposed at the end",
"nehemiah10": "A covenant signed rather than felt, eighty-four names beginning with the "
  "governor, commitments itemised down to firewood, nothing new legislated, and a motto "
  "that closes the document",
"nehemiah11": "A fortified city that nobody wanted to live in, one household in ten "
  "brought by lot, volunteers blessed publicly, inhabitants recorded by role, and a "
  "survey of the countryside from Beersheba northward",
"nehemiah12": "Genealogies establishing unbroken service across generations, two choirs "
  "marching opposite ways along the top of the wall, a rampart once dismissed as fox-work "
  "carrying processions, joy audible at a distance, and storerooms organised for what "
  "comes after",
"nehemiah13": "A return that finds every commitment broken, an enemy housed in the "
  "temple storeroom, Levites gone back to their fields for lack of support, gates shut "
  "before the Sabbath, and a book that ends asking to be remembered",
}

SECTIONS = {
"nehemiah1": [
  ("News from Jerusalem (vv.1-3)",
   "The month is Chislev in the twentieth year of Artaxerxes, 445 BC, some thirteen "
   "years after Ezra reached Jerusalem. Nehemiah is cupbearer at Susa, which meant "
   "tasting the king's wine against poison and therefore daily personal access to the "
   "monarch -- a position of unusual trust for a Jew in exile. His brother Hanani brings "
   "the report: the wall broken down and the gates burned, the survivors in great "
   "affliction and reproach. This is probably the forced demolition of Ezra 4:23 rather "
   "than the destruction of 586 BC."),
  ("Four Months of Prayer (vv.4-7)",
   "The response is not a plan but a collapse: he sat down and wept and mourned certain "
   "days, and fasted and prayed. Comparing 1:1 with 2:1 shows the interval was about four "
   "months, so nothing is said to the king for a third of a year. The prayer confesses "
   "\u201cI and my father's house have sinned\u201d, putting himself inside the failure "
   "rather than reporting on it."),
  ("Remember the Word Thou Commandedst (vv.8-11)",
   "The petition's argument is God's own word quoted back -- the promise from "
   "Deuteronomy that if they return, he will gather them from the uttermost parts. He "
   "asks for mercy in the sight of \u201cthis man\u201d, and only in the last clause of "
   "the chapter does the reader learn who he is: for I was the king's cupbearer. The "
   "detail is withheld until the prayer is finished, which is a deliberate order."),
],
"nehemiah2": [
  ("Sadness Before the King (vv.1-3)",
   "In Nisan, four months on, Nehemiah appears with a visibly heavy face, and his own "
   "aside says how dangerous that was: then I was very sore afraid. A servant's sorrow "
   "in the royal presence could be read as disloyalty or plotting. He answers carefully, "
   "naming the city of his fathers' sepulchres rather than Jerusalem, which is a "
   "sentiment a Persian king could respect without political overtones."),
  ("So I Prayed to the God of Heaven (vv.4-8)",
   "The king asks what he wants, and between the question and the reply sits the "
   "shortest prayer in Scripture -- so I prayed to the God of heaven. Then the requests "
   "come out fully formed: leave, a time set, letters to the governors beyond the river, "
   "and timber from the king's forest. Nobody improvises that list. Four months of "
   "praying had also been four months of planning."),
  ("The Night Inspection (vv.9-16)",
   "He arrives, and does nothing for three days. Then he rides out by night with a few "
   "men and tells no one what God has put in his heart, surveying the broken wall and the "
   "burned gates before anyone knows he is assessing them. The rulers, the priests and "
   "the nobles are all left uninformed. Verse 14 notes a place where the beast could not "
   "pass, so the damage was worse in some sections than others -- exactly what an "
   "inspection is for."),
  ("Let Us Rise Up and Build (vv.17-20)",
   "Only now does he speak, and the appeal is first person plural throughout: ye see the "
   "distress we are in, come and let us build. He tells them about the hand of God and "
   "the king's words, and they answer let us rise up and build. Sanballat, Tobiah and "
   "Geshem appear at once with mockery and the charge of rebellion, and his reply draws a "
   "boundary -- ye have no portion nor right nor memorial in Jerusalem."),
],
"nehemiah3": [
  ("Beginning at the Sheep Gate (vv.1-5)",
   "The construction record starts at the northeast corner near the temple and moves "
   "counterclockwise, and it opens with Eliashib the high priest and his fellow priests "
   "laying beams themselves. Roughly forty teams are named with the section each took. "
   "Verse 5 records the one refusal in the chapter: the nobles of Tekoa would not put "
   "their necks to the work of their Lord, a sentence left in the register without "
   "comment."),
  ("Round the City, Gate by Gate (vv.6-15)",
   "The list proceeds gate by gate -- the old gate, the valley gate, the dung gate, the "
   "gate of the fountain -- with the length repaired sometimes specified in cubits. Among "
   "the builders are goldsmiths and apothecaries, trades with no obvious relevance to "
   "masonry. Verse 12 names Shallum repairing with his daughters, the only mention of "
   "women in the record and included without remark."),
  ("Every Man Opposite His House (vv.16-27)",
   "A phrase recurs through this stretch: each repaired the section over against his own "
   "house. The organising principle was proximity and self-interest at once, which is why "
   "a wall of that length went up in under two months. Priests, Levites and temple "
   "servants are all placed, and the section by the water gate and the tower of Ophel is "
   "assigned to the Nethinim."),
  ("Priests, Goldsmiths and Merchants (vv.28-32)",
   "The circuit closes back at the sheep gate where it began. The final assignments go to "
   "priests above the horse gate, a goldsmith, and the merchants. The chapter has named "
   "the high priest, district rulers, tradesmen, temple servants, women and people from "
   "Jericho, Tekoa, Gibeon and Zanoah -- a wall built by the whole community rather than "
   "by builders, which is the point of listing them all."),
],
"nehemiah4": [
  ("Mockery: Even a Fox Would Break It (vv.1-6)",
   "The first weapon is ridicule. Sanballat asks what these feeble Jews are doing, and "
   "Tobiah adds that a fox going up would break the wall down. Nehemiah's response is two "
   "things at once and stays that way for the whole chapter: he prays, and then v.6 says "
   "so built we the wall. The prayer in vv.4-5 is unguardedly hostile, which the book "
   "records rather than tidies."),
  ("Conspiracy, and a Watch Set (vv.7-9)",
   "Mockery becomes conspiracy when the wall reaches half its height. The coalition now "
   "surrounds the city on every side -- Samaria to the north, Ammon east, the Arabs "
   "south, Ashdod west. Verse 9 is the chapter's method in one sentence: nevertheless we "
   "made our prayer unto our God, and set a watch against them day and night. Neither "
   "half is presented as sufficient alone."),
  ("The Strength of the Bearers Is Decayed (vv.10-14)",
   "The third attack comes from inside. Judah says the strength of the bearers of "
   "burdens is decayed and there is much rubbish, and the Jews living near the enemies "
   "report the threats ten times over. Nehemiah's answer is to station families by "
   "households at the lowest and most exposed places, with their swords and bows, and to "
   "tell them to remember the Lord and fight for their brethren, sons, daughters, wives "
   "and houses. He gives them something concrete to defend."),
  ("A Trowel in One Hand (vv.15-23)",
   "The arrangement that follows is the book's most quoted image: those who built worked "
   "with one hand and held a weapon with the other, and the load-bearers were armed too. "
   "A trumpeter stayed beside Nehemiah because the work was spread far apart along the "
   "wall. Nobody removed their clothes, and they used the night for a guard and the day "
   "for work. The chapter ends in exhaustion rather than triumph."),
],
"nehemiah5": [
  ("A Great Cry Against Their Brethren (vv.1-5)",
   "The crisis shifts from outside to inside, and it interrupts the building narrative "
   "deliberately. The poor are mortgaging fields and selling children into servitude to "
   "fellow Jews, under pressure from famine and the Persian tax and the unpaid labour of "
   "the wall itself. The complaint is not against the enemy but against brothers, and "
   "v.5 puts it plainly: our flesh is as the flesh of our brethren, our children as "
   "their children."),
  ("I Rebuked the Nobles (vv.6-13)",
   "Nehemiah is angry and says so, then consults with himself before acting -- a pause "
   "the text bothers to record. He calls a great assembly and confronts the nobles "
   "publicly, and his argument is the practice's absurdity: they had been redeeming Jews "
   "from foreign owners while selling them to each other. Usury among Israelites is "
   "forbidden outright in Exodus 22, Leviticus 25 and Deuteronomy 23. He demands "
   "restitution the same day, takes an oath from them, and shakes out his lap as a sign."),
  ("Twelve Years Without the Governor's Allowance (vv.14-18)",
   "The chapter's second half is Nehemiah's own record of practice. For twelve years as "
   "governor he did not take the food allowance the office entitled him to, because the "
   "bondage was heavy on the people -- and he notes that former governors had taken it. "
   "He fed a hundred and fifty at his own table daily and still bought no land. The "
   "reason given is not policy but the fear of God."),
  ("Think Upon Me, My God, for Good (v.19)",
   "One verse, and it is the first of several such prayers that punctuate the memoir. "
   "Think upon me, my God, for good, according to all that I have done for this people. "
   "It sits oddly beside the modesty of the previous verses, and the book leaves it "
   "there. The same request closes the whole work at 13:31."),
],
"nehemiah6": [
  ("Four Invitations to the Plain of Ono (vv.1-4)",
   "With the wall standing and only the doors left to hang, the attack becomes personal. "
   "Sanballat and Geshem invite him to meet in the plain of Ono, and Nehemiah says "
   "outright that they thought to do him mischief. His reply is the same four times: I am "
   "doing a great work, so that I cannot come down. Why should the work cease while I "
   "come down to you? He does not argue with the premise, he declines the meeting."),
  ("An Open Letter (vv.5-9)",
   "The fifth approach comes as an open letter, unsealed so anyone could read it on the "
   "way. It alleges that Nehemiah plans rebellion and has hired prophets to proclaim him "
   "king, and suggests the report will reach Artaxerxes. Publishing an accusation is the "
   "point of leaving it open. Nehemiah denies it flatly, says they invented it out of "
   "their own heart, and prays strengthen my hands."),
  ("A Hired Prophet (vv.10-14)",
   "The subtlest attempt. Shemaiah urges him to shut himself in the temple to escape "
   "assassination, which would have meant a layman entering where he had no right and "
   "discrediting himself. Nehemiah's answer is a question -- should such a man as I flee? "
   "-- and then his judgement: I perceived that God had not sent him, for Tobiah and "
   "Sanballat had hired him. Noadiah and other prophets are named as involved."),
  ("Fifty-Two Days (vv.15-19)",
   "The wall is finished in fifty-two days, and the effect on the surrounding nations is "
   "recorded as recognition rather than defeat: they perceived this work was wrought of "
   "our God. The chapter's last verses are less triumphant, noting that nobles in Judah "
   "were corresponding with Tobiah, who had married into their families. The opposition "
   "outside is beaten and the compromise inside remains, which sets up chapter 13."),
],
"nehemiah7": [
  ("Gatekeepers, Singers and a Delegated Command (vv.1-4)",
   "With the doors hung, Nehemiah turns to administration and hands the city to two "
   "men -- Hanani his brother and Hananiah, described as one who feared God above many, "
   "which is the qualification given. The security instruction is specific: the gates are "
   "not to be opened until the sun is hot. Verse 4 states the next problem plainly. The "
   "city is large and great and the people few, and the houses are not built."),
  ("The Register Found (vv.5-38)",
   "God puts it in his heart to number the people, and what he finds is not a new census "
   "but the register of those who first came up with Zerubbabel -- the same list as Ezra "
   "2, with small numerical differences that copyists have argued over ever since. He "
   "reproduces it rather than replacing it. Using the founding roll to solve a present "
   "problem ties the repopulation to the original return."),
  ("Priests, Levites and Unproven Descent (vv.39-65)",
   "The temple personnel are counted, and the Levite shortage familiar from Ezra 2 is "
   "there again. Then those who could not show their father's house, including priests "
   "whose names were sought and not found: they are put from the priesthood as polluted, "
   "and barred from the holy things until a priest should stand up with Urim and Thummim. "
   "A suspension with no stated end, recorded without softening."),
  ("The Totals and the Giving (vv.66-73)",
   "The totals close the register at 42,360, with servants, singers and animals counted "
   "separately. The last verses record what the heads of families gave to the work -- "
   "gold, silver, priests' garments -- and then the people settling in their cities. The "
   "chapter ends on the seventh month, which is where chapter 8 begins, so the register "
   "hands directly into the reading of the law."),
],
"nehemiah8": [
  ("Bring the Book: The People Ask (vv.1-6)",
   "On the first day of the seventh month the people gather as one man and ask Ezra to "
   "bring the book of the law. The initiative is theirs, which is the detail that makes "
   "this chapter unusual -- nobody imposes a reading. Ezra reads from morning until "
   "midday, five or six hours, from a wooden pulpit made for the purpose, and the people "
   "stand. When he blesses God they answer amen with lifted hands and bow their faces to "
   "the ground."),
  ("They Gave the Sense (vv.7-8)",
   "Thirteen Levites are named as moving among the people, and v.8 describes what they "
   "did: they read distinctly, and gave the sense, and caused them to understand the "
   "reading. Hebrew was no longer the everyday language after the exile, so this was "
   "probably translation as well as explanation. Two verses that describe teaching as a "
   "separate task from reading."),
  ("The Joy of the LORD Is Your Strength (vv.9-12)",
   "The people weep when they hear the law, and the leaders stop them. This day is holy, "
   "mourn not nor weep -- go your way, eat the fat and drink the sweet, send portions to "
   "those for whom nothing is prepared. The grief was appropriate and is redirected "
   "rather than validated. \u201cThe joy of the LORD is your strength\u201d is spoken to "
   "people who have just been convicted, not to people already cheerful."),
  ("Tabernacles as Not Since Joshua (vv.13-18)",
   "The next day the heads of families come back for more, and reading further they find "
   "the feast of booths and keep it. Verse 17 makes a striking claim -- since the days of "
   "Joshua the son of Nun it had not been done so. Centuries of the festival kept "
   "partially or not at all, corrected by people reading the instructions for themselves. "
   "The reading continued daily through the seven days."),
],
"nehemiah9": [
  ("Sackcloth and Separation (vv.1-4)",
   "Two days after the feast ends, the mood changes completely: fasting, sackcloth and "
   "earth on their heads. They read the law a quarter of the day and confess for another "
   "quarter, so the confession is as long as the reading. The separation from strangers "
   "is covenantal rather than ethnic, the same concern as Ezra 9. Levites are named as "
   "leading the cry."),
  ("Thou Art LORD Alone (vv.5-15)",
   "The longest prayer in the Old Testament begins with creation and moves to Abraham, "
   "the exodus, the Red Sea, Sinai and the manna. The recital is not decorative -- each "
   "act of God becomes a premise for what follows. Verse 8's \u201cthou hast performed "
   "thy words, for thou art righteous\u201d sets up the contrast the rest of the prayer "
   "runs on."),
  ("But They Dealt Proudly (vv.16-31)",
   "The history is retold as a cycle: God gives, Israel rebels, God disciplines, Israel "
   "cries out, God delivers. The failures are named without euphemism -- the golden calf, "
   "refusing to hear, killing the prophets, stiff necks. And in the middle of the "
   "indictment sits v.17, God described as ready to pardon, gracious and merciful, slow "
   "to anger and of great kindness. The mercy is stated at the point where the offence "
   "is worst."),
  ("Now Therefore, Our God (vv.32-37)",
   "The prayer turns to the present. Verse 33 concedes the whole argument: thou art just "
   "in all that is brought upon us, for thou hast done right, but we have done wickedly. "
   "Then the description of their condition -- servants in the land God gave their "
   "fathers, its increase going to kings set over them because of their sins. No excuse "
   "is offered and no request is made yet."),
  ("We Make a Sure Covenant (v.38)",
   "One verse turns the confession into a document: because of all this we make a sure "
   "covenant and write it, and our princes, Levites and priests seal it. Repentance is "
   "committed to paper rather than left as feeling, and chapter 10 is the signature "
   "list. The prayer produces an obligation instead of a resolution."),
],
"nehemiah10": [
  ("Nehemiah Signs First (vv.1-8)",
   "The document opens with the governor's name, which sets the pattern for everything "
   "in it: the leader is bound before anyone else is. The priests follow. This is a legal "
   "instrument -- signed, sealed and witnessed -- rather than a statement of intent, and "
   "the eighty-four names across the section represent the whole community by "
   "office."),
  ("Levites and Chiefs of the People (vv.9-27)",
   "The Levites are listed, then the chiefs of the people, and the length of the roll is "
   "part of its function. Anyone could later check who had signed. Naming the signatories "
   "in a book that will record the covenant being broken three chapters later gives the "
   "list a weight nobody intended at the time."),
  ("Entering into a Curse and an Oath (vv.28-31)",
   "The commitments begin, and they are specific: no intermarriage with the peoples of "
   "the land, no trading on the sabbath or holy days when neighbours bring wares, and the "
   "seventh year left and debts released. None of this is new legislation. Every clause "
   "restates Mosaic law that had lapsed, which is why the document is a recommitment "
   "rather than a reform."),
  ("We Will Not Forsake the House of Our God (vv.32-39)",
   "The remaining clauses are administrative and unglamorous: a third of a shekel yearly "
   "for the service, lots cast for who supplies wood for the altar, firstfruits, "
   "firstborn and tithes brought to the chambers. Firewood rotas are the kind of detail "
   "that shows a community intending to function rather than to feel. The last clause is "
   "the motto the whole document serves -- and we will not forsake the house of our God."),
],
"nehemiah11": [
  ("One in Ten by Lot (vv.1-2)",
   "The problem is that a walled city with no inhabitants is an empty fortress. The "
   "leaders already lived in Jerusalem; everyone else preferred the villages where they "
   "had land and houses. The solution combines compulsion and choice -- lots bring one "
   "household in ten, and others volunteer. Verse 2 records that the people blessed those "
   "who willingly offered themselves, so the sacrifice was publicly honoured rather than "
   "assumed."),
  ("The Chief of the Province in Jerusalem (vv.3-19)",
   "The new inhabitants are recorded by descent and role: men of Judah, of Benjamin, "
   "priests, Levites, gatekeepers. Numbers are given for each group. Some individuals get "
   "a phrase of description -- a mighty man of valour, one who was over the business of "
   "the house of God -- so the register is not purely statistical. Repopulation is being "
   "organised rather than left to drift."),
  ("Overseers and Officers (vv.20-24)",
   "A short section on administration: the Nethinim on the hill of Ophel, the overseer of "
   "the Levites and the singers, and a man at the king's hand in all matters concerning "
   "the people. The mention of the king's commandment concerning the singers shows the "
   "Persian arrangement still framing everything, even in the details of worship."),
  ("The Villages of Judah and Benjamin (vv.25-36)",
   "The chapter closes with a survey of where everyone else settled -- Kirjath-arba, "
   "Dibon, Beersheba and its villages in the south, Geba and Michmash and Bethel "
   "northward for Benjamin. The geography traces the extent of the territory actually "
   "occupied. The city was being filled and the land was being inhabited, which is the "
   "point of listing places nobody would otherwise record."),
],
"nehemiah12": [
  ("Priests and Levites with Zerubbabel (vv.1-11)",
   "The chapter opens with the list of priests and Levites who came up in the first "
   "return, roughly a century before Nehemiah. Establishing that line matters because the "
   "dedication about to happen is being performed by the same families who started. The "
   "high priestly succession is traced from Jeshua down to Jaddua."),
  ("The Generations of Joiakim (vv.12-26)",
   "The record continues through the next generations -- heads of the priestly houses in "
   "Joiakim's day, then the Levites, singers and gatekeepers down to Nehemiah's own time. "
   "It is dry reading and it is doing something: proving continuity of service across "
   "three generations and two returns, which is the institutional claim behind the "
   "ceremony."),
  ("Two Companies on the Wall (vv.27-39)",
   "The dedication. Levites and singers are brought in from the villages, and priests, "
   "people, gates and wall are all purified. Then two great companies of thanksgiving are "
   "sent in opposite directions along the top of the wall, with Ezra leading one and "
   "Nehemiah following the other, until they meet at the temple. The structure Tobiah "
   "said a fox would break down is now carrying two processions with instruments."),
  ("The Joy of Jerusalem Heard Afar Off (vv.40-43)",
   "The companies meet, the sacrifices are offered, and the wives and children rejoice "
   "with them -- the text specifies that the celebration was not confined to the men or "
   "the officials. Verse 43 measures the joy by its range: the joy of Jerusalem was heard "
   "even afar off. A city mocked for its rubble is now audible at a distance for a "
   "different reason."),
  ("Storerooms and Portions (vv.44-47)",
   "The chapter ends in logistics, which is the honest sequel to a festival. Men are "
   "appointed over the chambers for the treasures, offerings, firstfruits and tithes, and "
   "the portions for singers and gatekeepers are set. The dedication is being turned into "
   "a standing arrangement, since a ceremony does not feed anyone the following week."),
],
"nehemiah13": [
  ("Read in the Book of Moses (vv.1-3)",
   "The final chapter opens with a public reading that produces immediate action: they "
   "find the provision about Ammonites and Moabites and separate the mixed multitude. "
   "Reading followed by change is the pattern of chapter 8 repeated in miniature, and it "
   "sets up everything that follows by showing what the community was capable of when the "
   "law was actually read to it."),
  ("Tobiah's Furniture Thrown Out (vv.4-9)",
   "Nehemiah returns from the Persian court after an absence -- he had gone back in "
   "Artaxerxes' thirty-second year, around 433 BC -- and finds that Eliashib the priest "
   "has given Tobiah a chamber in the temple itself, the room used for grain offerings, "
   "frankincense and tithes. His response is physical: it grieved me sore, and I cast "
   "forth all the household stuff of Tobiah out of the chamber. Then he has the rooms "
   "cleansed and the vessels brought back."),
  ("The Levites Gone to Their Fields (vv.10-14)",
   "The portions had not been given, so the Levites and singers had left the temple for "
   "their farms -- an entirely rational response to not being paid. Nehemiah contends "
   "with the rulers and asks the question that answers itself: why is the house of God "
   "forsaken? He restores the officers and the tithes, and adds another remember me, O my "
   "God, concerning this."),
  ("Shut the Gates Before the Sabbath (vv.15-22)",
   "The sabbath is being openly ignored -- winepresses trodden, loads brought in, "
   "Tyrians selling fish. Nehemiah's remedy is administrative and physical: he orders the "
   "gates shut as darkness falls before the sabbath and keeps them shut, and when "
   "merchants camp outside he threatens to lay hands on them. They came no more. Then he "
   "sets Levites to guard the gates, which turns a personal intervention into a "
   "procedure."),
  ("Remember Me, O My God (vv.23-31)",
   "The last abuse is intermarriage resumed, with children who could not speak the "
   "language of Judah. Nehemiah's reaction is the most violent in the book -- he contends "
   "with them, curses them, strikes some and pulls out their hair -- and he cites Solomon "
   "as the precedent for where it leads. The book then simply stops, with the priesthood "
   "cleansed, the offerings arranged, and one more prayer: remember me, O my God, for "
   "good. A wall built in fifty-two days needed constant maintenance afterwards, and the "
   "ending refuses to pretend otherwise."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[8:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        want_drop = DROP.get(page, [])
        fields, dropped, extra = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")
        if dropped:
            notes.append(f"{page}: fragment label folded into prose")

        sections = SECTIONS[page]
        covered = set()
        for label, text in [("Key Themes", THEMES[page])] + \
                           [(f"section {h!r}", p) for h, p in sections] + \
                           [(w, fields[w]) for w in KEEP]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
            if "\u2013" in head:
                problems.append(f"{page}: en-dash in {head!r}")
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        parts.append(ITEM.format(label="Author:", body=fields["Author:"]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=GENRE) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=THEMES[page]) + "\n")
        parts.append(ITEM.format(label="Historical Context:",
                                 body=fields["Historical Context:"]) + "\n")
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
