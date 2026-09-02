#!/usr/bin/env python3
"""
Folds Hosea, all 14 chapters.

Cleanest input of the remaining books. Every page already carries Author,
Classification, Key Themes and Historical Context, and every page carries an
outline sublist whose items all end in a verse range, with no gaps and no
overlaps. So the four existing fields are preserved untouched apart from the
capital fixes below, the sublist is dropped, and each outline item becomes a
prose section written from the text.

Emphatic capitals in the inherited Historical Context are repaired one at a
time, never by a blanket pass: ALLURING, GOD (used for emphasis, not as part of
LORD GOD), PURCHASED, SHALLOWNESS, RELATIONSHIP, WANTED, FATHER/ CHILD, DIVINE,
WARNING, MODEL, CONCLUSION, RETURN, WORDS. Each was checked against the five
cases a blanket pass would have destroyed elsewhere in the corpus.

Two other inherited defects are fixed here: 'Beth- aven' in hosea10, a broken
hyphenation, and the exclamation mark in hosea13's 'Death Defeated!', which
would have been the only '!' in 2908 section labels.

Usage:
    python3 fold_hosea.py [--check]
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
           "AM", "II"}
VERSES = {1: 11, 2: 23, 3: 5, 4: 19, 5: 15, 6: 11, 7: 16, 8: 14,
          9: 17, 10: 15, 11: 12, 12: 14, 13: 16, 14: 9}

# Repairs to the inherited Historical Context, exact strings, applied per page.
FIXES = {
    2: [("all things GOD provided", "all things God provided"),
        ("God instead speaks of ALLURING her back", "God instead speaks of alluring her back")],
    3: [("she must be PURCHASED back", "she must be purchased back")],
    6: [("not the absence of religious feeling, but its SHALLOWNESS",
         "not the absence of religious feeling but its shallowness"),
        ("God&#x27;s primary desire is not ritual but RELATIONSHIP",
         "God&#x27;s primary desire is not ritual but relationship")],
    7: [("God WANTED to heal them", "God wanted to heal them")],
    10: [("Beth- aven", "Beth-aven")],
    11: [("from husband/wife imagery to FATHER/ CHILD",
          "from husband and wife imagery to father and child"),
         ("His compassion is DIVINE, not human", "His compassion is divine, not human")],
    12: [("as both WARNING and MODEL", "as both warning and model")],
    14: [("Chapter 14 is the CONCLUSION and climax",
          "Chapter 14 is the conclusion and climax"),
         ("God gives the final invitation: RETURN",
          "God gives the final invitation, return"),
         ("He even provides the WORDS of repentance",
          "He even provides the words of repentance")],
}

SECTIONS = {
1: [
 ("The Prophetic Commission: Hosea's Marriage (vv.1-3)",
  "The book opens by dating itself to four Judean kings and one Israelite one, then "
  "immediately does something no other prophetic book does: the first command God gives "
  "the prophet is not to speak but to marry. Go, take unto thee a wife of whoredoms. The "
  "message will not be delivered from a distance, it will be lived at the prophet's own "
  "cost, and the reason is given in the same breath, for the land hath committed great "
  "whoredom, departing from the LORD. Hosea obeys and marries Gomer, and the marriage "
  "itself becomes the sermon."),
 ("First Child: Jezreel, Judgment on Jehu's House (vv.4-5)",
  "The children are named as pronouncements, and the first name is a place. Jezreel is "
  "where Jehu carried out the massacre that founded his dynasty, and God now says He will "
  "avenge that blood on the house that profited from it. The point is uncomfortable: the "
  "purge Jehu performed had divine sanction in 2 Kings, but the zeal in it was his own, "
  "and the dynasty built on it is about to end. God adds that He will break the bow of "
  "Israel in the valley of Jezreel, the same ground, the same name, judgment landing where "
  "the dynasty began."),
 ("Second Child: Lo-ruhamah, No Mercy (vv.6-7)",
  "The daughter's name means she shall not have mercy, and the sentence attached to it is "
  "that God will no more have mercy upon the house of Israel. Then comes a distinction "
  "that matters for the rest of the book: Judah is exempted, and exempted in a particular "
  "way. I will save them by the LORD their God, and will not save them by bow, nor by "
  "sword, nor by battle. Judah's deliverance, when it comes at Sennacherib's siege, will "
  "have no military explanation at all."),
 ("Third Child: Lo-ammi, Not My People (vv.8-9)",
  "The third name is the harshest because it undoes the covenant formula itself. Ye are "
  "not my people, and I will not be your God. Every earlier promise had run the other "
  "way, I will be your God and ye shall be my people, and here the words are reversed and "
  "handed to a child to carry through life. Naming a child this is not rhetoric, it is a "
  "man calling his son by a sentence of divorce every day for years."),
 ("The Promise of Future Restoration (vv.10-11)",
  "Then the chapter turns without transition. The children of Israel shall be as the sand "
  "of the sea, which is Abraham's promise restated, and in the place where it was said "
  "unto them, Ye are not my people, there it shall be said unto them, Ye are the sons of "
  "the living God. The judgment names are not merely lifted, they are reversed on the same "
  "ground where they were given. Judah and Israel are gathered under one head, which is "
  "the reunion of a kingdom split for two centuries. Paul quotes this passage in Romans 9 "
  "of Gentiles brought in."),
],
2: [
 ("The Accusation Against the Unfaithful Wife (vv.1-5)",
  "The oracle opens by handing the reversal of chapter 1 to the hearers as an instruction, "
  "say ye unto your brethren, Ammi, and to your sisters, Ruhamah, and then turns straight "
  "to the charge. Plead with your mother, for she is not my wife. The wife credits her "
  "lovers with bread and water, wool and flax, oil and drink, and the threat is exposure, "
  "she will be stripped and set as a wilderness. The language is domestic and the target "
  "is national: Baal worship promised fertility, and Israel took the promise."),
 ("God's Discipline: Hedging Her Way with Thorns (vv.6-13)",
  "The response is not abandonment but obstruction. I will hedge up her way with thorns, "
  "and make a wall, that she shall not find her paths. She will chase her lovers and not "
  "overtake them, and only then say, I will go and return to my first husband, for then "
  "was it better with me than now. Then the sentence God has been withholding: she did not "
  "know that I gave her the corn and the wine and the oil, and the silver and gold she "
  "made into images of Baal. The blessings she credited to Baal were the evidence against "
  "her. So they are taken back, the feast days cease, the vines are laid waste."),
 ("The Stunning Reversal: Alluring Love (vv.14-15)",
  "The therefore of verse 14 is the hinge of the whole book. Everything before it builds "
  "toward a final judgment, and the word arrives and turns the other way. Therefore, "
  "behold, I will allure her, and bring her into the wilderness, and speak comfortably "
  "unto her. The wilderness is not the punishment here, it is the courtship, the place "
  "where the relationship began. The valley of Achor, whose name means trouble and which "
  "was Israel's first failure in the land under Joshua, is given back as a door of hope."),
 ("The New Covenant: Betrothal Forever (vv.16-20)",
  "The vocabulary of the relationship is rebuilt. She will call Him Ishi, my husband, and "
  "no longer Baali, my master, and the names of the Baals will be taken out of her mouth "
  "so that she does not remember them. Then the betrothal, and it is stated three times, I "
  "will betroth thee unto me for ever, in righteousness and judgment, in lovingkindness "
  "and mercies, in faithfulness. These are the qualities the marriage lacked, supplied by "
  "the husband rather than demanded of the wife, and the outcome is knowledge, thou shalt "
  "know the LORD. Jewish weddings still recite these verses."),
 ("The Great Restoration: Reversal of Judgment Names (vv.21-23)",
  "The close runs the whole chain of provision backwards into blessing. The heavens answer "
  "the earth, the earth the corn and wine and oil, and they answer Jezreel, whose name "
  "means God sows and is now used for planting rather than scattering. Then the two "
  "remaining names are turned: I will have mercy upon Lo-ruhamah, and I will say to "
  "Lo-ammi, Thou art my people. Every sentence pronounced over the children in chapter 1 "
  "is revoked by name."),
],
3: [
 ("God's Command: Love Her Again (v.1)",
  "Five verses, and the first is a second command harder than the first. Go yet, love a "
  "woman beloved of her friend, an adulteress. The word is love, not merely take, and it "
  "is a command to feel as well as act. The reason is stated plainly, according to the "
  "love of the LORD toward the children of Israel, who look to other gods. Hosea is being "
  "asked to demonstrate what he cannot argue: that this kind of love is possible, because "
  "God is doing it."),
 ("The Purchase: Buying Back the Adulterous Wife (v.2)",
  "So I bought her to me for fifteen pieces of silver, and for an homer of barley, and an "
  "half homer of barley. The precision is the point. Fifteen shekels is half the thirty of "
  "Exodus 21:32, the price set for a slave gored by an ox, and the barley makes up the "
  "rest in grain, the cheapest of the grain offerings. She has fallen to the value of a "
  "damaged slave, and her husband pays it. Restoration in this book is never free and "
  "never described as easy."),
 ("The Condition: Faithful Waiting (v.3)",
  "Thou shalt abide for me many days, thou shalt not play the harlot, and thou shalt not "
  "be for another man, so will I also be for thee. The purchase does not end in immediate "
  "restoration of the marriage, it ends in a period of waiting imposed on both of them. He "
  "binds himself by the same terms he sets for her. The relationship is real but suspended, "
  "and the suspension is deliberate."),
 ("The Prophetic Parallel: Israel's Long Exile (v.4)",
  "The waiting is then interpreted, and the interpretation reaches far past the exile. "
  "Israel shall abide many days without a king, and without a prince, and without a "
  "sacrifice, and without an image, and without an ephod, and without teraphim. The list "
  "strips out both legitimate institutions and illegitimate ones, monarchy and sacrifice "
  "alongside idol and household god. It is a description of a people kept in existence "
  "with none of the machinery of a nation or a cult."),
 ("The Promise: Return in the Latter Days (v.5)",
  "Afterward shall the children of Israel return, and seek the LORD their God, and David "
  "their king, and shall fear the LORD and his goodness in the latter days. David has been "
  "dead for two centuries when this is written, so the name is being used for the line and "
  "the one who comes from it. Note also which kingdom is speaking: Hosea prophesies to the "
  "north, which rejected David's house at the schism, and the restoration he promises "
  "brings them back to it."),
],
4: [
 ("God's Lawsuit: The Charges (vv.1-3)",
  "Chapter 4 opens the second half of the book and changes genre. The marriage is behind "
  "us, and what stands in its place is a courtroom, the LORD hath a controversy with the "
  "inhabitants of the land. The Hebrew is a legal term for a formal suit. The indictment "
  "is a list of absences followed by a list of acts: no truth, no mercy, no knowledge of "
  "God in the land, then swearing, lying, killing, stealing, adultery. Read in order it "
  "tracks the second table of the Ten Commandments. The verdict extends past the guilty, "
  "the land itself mourns and the fish of the sea are taken away."),
 ("Indictment of the Priesthood (vv.4-9)",
  "The charge narrows to those paid to prevent this. My people are destroyed for lack of "
  "knowledge, and the next clause identifies who withheld it, because thou hast rejected "
  "knowledge, I will also reject thee. The priests were the teaching office, and they had "
  "an interest in the sin they were meant to correct, they eat up the sin of my people, "
  "because the offerings brought them food. Then the sentence that names the whole "
  "problem, like people, like priest. A nation does not rise above those who instruct it."),
 ("The Futility of Idolatry (vv.10-14)",
  "The fertility religion is measured against its own promises and fails them. They shall "
  "eat and not have enough, they shall commit whoredom and shall not increase. Baal was "
  "worshipped for exactly the increase it does not deliver. The chapter describes the "
  "hilltop shrines under oak and poplar and elm, and then refuses to single out the women, "
  "I will not punish your daughters when they commit whoredom, because the fathers were "
  "doing the same thing at the same shrines. The line about wine and new wine taking away "
  "the heart is offered as diagnosis rather than insult."),
 ("Warning to Judah: Do Not Follow Israel (vv.15-19)",
  "The oracle turns aside to speak to the southern kingdom, which is still standing. "
  "Though thou, Israel, play the harlot, yet let not Judah offend. The place names carry "
  "the argument: do not come to Gilgal, nor go up to Beth-aven, which means house of "
  "vanity and is Hosea's renaming of Bethel, house of God. The site of Jacob's ladder now "
  "houses a calf. Israel is called a backsliding heifer and Ephraim is left to its idols, "
  "and the chapter ends with the wind carrying them off, ashamed of their own devices."),
],
5: [
 ("Triple Indictment: Priests, Israel, Royal House (vv.1-7)",
  "Three groups are summoned at once, hear ye this, O priests, and hearken, ye house of "
  "Israel, and give ye ear, O house of the king. No class is exempt, and the images are of "
  "trapping, a snare on Mizpah and a net spread upon Tabor, both of them high places used "
  "for worship. The reason judgment is certain is a matter of character, not circumstance: "
  "they will not frame their doings to turn unto their God, for the spirit of whoredoms is "
  "in the midst of them. Their sacrifices cannot reach Him, they shall not find him, "
  "because the offering is not the problem."),
 ("The Alarm: War is Coming (vv.8-9)",
  "Blow ye the cornet in Gibeah, and the trumpet in Ramah. The towns named are on the "
  "border between the two kingdoms, and the alarm is being raised across it, which fixes "
  "the setting: this is the Syro-Ephraimite war of around 735 BC, when Israel and Syria "
  "attacked Judah and Judah called Assyria in. Ephraim shall be desolate in the day of "
  "rebuke, and the desolation is announced as settled."),
 ("Judah Also Condemned (v.10)",
  "The princes of Judah were like them that remove the bound. Moving a boundary stone is "
  "the quiet theft the law singles out in Deuteronomy 19 and 27, a crime committed at "
  "night against a neighbour who cannot prove it. Judah has just been warned not to follow "
  "Israel, and this is the charge that lands against it, not idolatry but the deliberate "
  "shifting of a line."),
 ("God as Moth and Lion (vv.11-14)",
  "Two images of how judgment arrives, and the pairing is the point. I will be unto "
  "Ephraim as a moth, and to the house of Judah as rottenness, decay so slow it is only "
  "noticed when the garment tears. Between them sits the diagnosis, when Ephraim saw his "
  "sickness he went to Assyria, treating the symptom with the empire that would destroy "
  "him. Then the second image, I will be unto Ephraim as a lion, and there shall be none "
  "to deliver. The moth is what they have not noticed, the lion is what they will not "
  "survive."),
 ("God Withdraws Until Repentance (v.15)",
  "I will go and return to my place, till they acknowledge their offence, and seek my face. "
  "The most severe thing in the chapter is not an act but a withdrawal, and it is stated "
  "with a condition attached and an expectation of the outcome, in their affliction they "
  "will seek me early. Absence is the instrument here, and it is temporary by design."),
],
6: [
 ("Israel's Call to Repentance (vv.1-3)",
  "Come, and let us return unto the LORD. Taken by itself this is the best thing said in "
  "the book by anyone other than God. He hath torn and he will heal us, after two days he "
  "will revive us, in the third day he will raise us up. It is confident, well phrased, "
  "and correct in its theology, and the phrase about the third day has been read as "
  "resurrection language ever since. It reads as the answer the previous chapter was "
  "waiting for."),
 ("God's Lament: Your Love is Like Morning Dew (v.4)",
  "God's reply exposes it. O Ephraim, what shall I do unto thee? your goodness is as a "
  "morning cloud, and as the early dew it goeth away. The word rendered goodness is hesed, "
  "covenant loyalty, the very quality God is looking for, and the complaint is not that "
  "they lack feeling but that the feeling does not last past the morning. This is the "
  "hardest verse in the chapter because the prayer it answers sounded sincere. Repentance "
  "that evaporates is the specific failure named here."),
 ("God's True Desire: Mercy, Not Sacrifice (vv.5-6)",
  "Therefore have I hewed them by the prophets, and my judgments are as the light that "
  "goeth forth. Then the verse that outlasts the book: I desired mercy, and not sacrifice, "
  "and the knowledge of God more than burnt offerings. It is not an abolition of the "
  "sacrificial system, which God commanded, it is a statement of priority inside it. Jesus "
  "quotes it twice, at Matthew 9:13 over eating with tax collectors and at Matthew 12:7 "
  "over the Sabbath, both times against people who had the ritual right and the mercy "
  "wrong."),
 ("The Catalogue of Crimes (vv.7-11)",
  "The evidence follows the principle. They like men have transgressed the covenant, which "
  "can also be read as they have transgressed like Adam, the first covenant broken in a "
  "garden. Then place by place: Gilead a city of workers of iniquity, Shechem a road where "
  "priests murder travellers, Bethel the site of lewdness. The priesthood appears here as "
  "a gang. Judah is named at the end, with a harvest set for it too."),
],
7: [
 ("God's Frustrated Healing: Iniquity Exposed (vv.1-2)",
  "When I would have healed Israel, then the iniquity of Ephraim was discovered. The "
  "sequence matters, the intention to heal is stated first and the corruption surfaces "
  "against it. What is exposed is theft and organized violence, the thief cometh in, and "
  "troops of robbers spoil without. Then the observation that explains the whole chapter: "
  "they consider not in their hearts that I remember all their wickedness. The problem is "
  "not defiance, it is that the thought never occurs to them."),
 ("The Oven: Political Conspiracy and Regicide (vv.3-7)",
  "They make the king glad with their lies, and then the baker's imagery begins. The "
  "conspirators are an oven left overnight, the baker sleeping while the dough rises, and "
  "in the morning it burneth as a flaming fire. This is not metaphor for its own sake, it "
  "is a description of Israel's last decades: between about 746 and 732 BC four of the "
  "final six kings were murdered by the men who replaced them. The chapter says the "
  "princes were drunk on the night of the killing. And the verdict on all of it, there is "
  "none among them that calleth unto me."),
 ("The Half-Baked Cake: Unaware Decay (vv.8-10)",
  "Ephraim hath mixed himself among the people, Ephraim is a cake not turned. A flatbread "
  "left on one side is burnt where it touches the stone and raw on top, useless either "
  "way, and the fault is inattention rather than malice. The application is stated "
  "directly, strangers have devoured his strength and he knoweth it not. The decay is real "
  "and unnoticed, and pride is what keeps it unnoticed, the pride of Israel testifieth to "
  "his face."),
 ("The Silly Dove: Flitting Between Empires (vv.11-12)",
  "Ephraim also is like a silly dove without heart, they go to Assyria. The bird chosen is "
  "one that panics and flies straight into the net, and the flight described is Israel's "
  "foreign policy, calling on Egypt against Assyria and Assyria against Egypt by turns, "
  "with no settled loyalty to either or to God. When they shall go, I will spread my net "
  "upon them. The instinct that looks like escape is what catches them."),
 ("God's Lament: I Would Redeem, But They Rebel (vv.13-16)",
  "The chapter ends in the first person and reads as grievance rather than sentence. "
  "Though I have redeemed them, yet they have spoken lies against me. They howled upon "
  "their beds rather than cried unto God, meaning the distress was real and never turned "
  "into prayer. I have bound them, though they have spoken lies against me, and the "
  "closing image is a deceitful bow, a weapon that looks serviceable and sends the arrow "
  "somewhere other than where it was aimed."),
],
8: [
 ("The Trumpet Alarm: Judgment Approaches (vv.1-3)",
  "Set the trumpet to thy mouth. He shall come as an eagle against the house of the LORD. "
  "The bird is a carrion bird as much as a raptor, and it is Assyria. The stated ground is "
  "covenant, they have transgressed my covenant, and trespassed against my law. Then the "
  "chapter records what Israel will say when the alarm sounds, My God, we know thee, and "
  "answers it in the next breath, Israel hath cast off the thing that is good. The claim "
  "to know God is not disputed as a feeling, it is disputed as a fact."),
 ("Self-Made Kings and Self-Made Gods (vv.4-6)",
  "They have set up kings, but not by me. The northern monarchy had begun in a divinely "
  "announced schism and then continued through nine dynasties of coup and counter-coup, "
  "and Hosea treats the whole succession as unauthorized. The same verb governs their "
  "religion, of their silver and their gold have they made them idols. Then the calf of "
  "Samaria, and the flattest sentence available about it, the workman made it, therefore "
  "it is not God. An object that required a craftsman cannot be the one who made the "
  "craftsman."),
 ("Sowing the Wind, Reaping the Whirlwind (vv.7-8)",
  "For they have sown the wind, and they shall reap the whirlwind. The proverb has "
  "outlived its context, and what it says here is precise: the harvest is the same "
  "substance as the seed and vastly larger. Nothing new is introduced by the judgment, it "
  "is their own act at scale. Israel is swallowed up, now shall they be among the Gentiles "
  "as a vessel wherein is no pleasure, a pot nobody wants."),
 ("A Wild Donkey: Hiring Lovers (vv.9-10)",
  "They are gone up to Assyria, a wild ass alone by himself, Ephraim hath hired lovers. "
  "The tribute paid to Assyria for protection is described as a payment for sex, which "
  "reverses the ordinary picture, the prostitute is the one paying. Though they have hired "
  "among the nations, now will I gather them, and the gathering is not rescue, it is "
  "arrest."),
 ("Multiplied Altars, Multiplied Sin (vv.11-13)",
  "Ephraim hath made many altars to sin. More worship, more guilt, because the altars were "
  "never commanded and the multiplication is itself the offence. I wrote to him the great "
  "things of my law, but they were counted as a strange thing, a written revelation "
  "treated as foreign. The sacrifices continue, and the verdict on them is that God does "
  "not accept them, and the destination is named, they shall return to Egypt, the house "
  "they were brought out of."),
 ("Israel Has Forgotten His Maker (v.14)",
  "For Israel hath forgotten his Maker, and buildeth temples. The chapter has listed "
  "kings, idols, altars, alliances and sacrifices, and the closing verse puts one cause "
  "under all of them, and it is not rebellion but forgetting. The building continues, more "
  "of it than before, which is why forgetting is the harder charge, there is no gap in the "
  "religious activity to give it away."),
],
9: [
 ("No Joy for Israel: The Harvest Will Fail (vv.1-6)",
  "Rejoice not, O Israel, for joy, as other people. The setting appears to be a harvest "
  "festival, and the prophet interrupts it, because the celebration was patterned on the "
  "neighbours and the credit was going to Baal, thou hast gone a whoring from thy God, thou "
  "hast loved a reward upon every cornfloor. The floor and the winepress shall fail them. "
  "Then the exile, they shall not dwell in the LORD's land, with the detail that their "
  "bread shall be unclean and their sacrifices unacceptable because they will be offered on "
  "foreign ground. Egypt and Assyria are both named as destinations."),
 ("The Days of Punishment Are Here (vv.7-9)",
  "The days of visitation are come. It is stated in the perfect, as accomplished. The "
  "chapter then records what the people say about the prophet, the prophet is a fool, the "
  "spiritual man is mad, which is the crowd's reply quoted back at them rather than the "
  "prophet's complaint. The comparison that closes it is the worst available in Israel's "
  "memory, they have deeply corrupted themselves, as in the days of Gibeah, the atrocity "
  "of Judges 19 that nearly destroyed a tribe."),
 ("God's Memory: Once Beloved, Now Corrupt (v.10)",
  "I found Israel like grapes in the wilderness, I saw your fathers as the firstripe in "
  "the fig tree at her first time. Both images are of unexpected sweetness in a place that "
  "does not produce it, and both are about delight rather than duty. Then the turn in the "
  "same verse, but they went to Baal-peor, and separated themselves unto that shame, the "
  "episode of Numbers 25 on the very edge of the promised land. The pattern was set before "
  "they entered."),
 ("Ephraim's Glory Flies Away: Barrenness (vv.11-14)",
  "Ephraim, their glory shall fly away like a bird. The judgment is aimed at fertility, "
  "which is precisely what Baal was worshipped to secure, no birth, no pregnancy, no "
  "conception. Though they bring up children, yet will I bereave them. Then the prophet "
  "prays, and the prayer is the most difficult sentence in the chapter, give them a "
  "miscarrying womb and dry breasts. He is asking for the lesser of two judgments, that "
  "children not be born into what is coming."),
 ("Driven Out of God's House (vv.15-17)",
  "All their wickedness is in Gilgal, the place where the monarchy was confirmed, and the "
  "sentence is expulsion, I will drive them out of mine house. The house is the land. Then "
  "the botanical image, their root is dried up, they shall bear no fruit, and the final "
  "line, they shall be wanderers among the nations. The book has moved from a woman driven "
  "out of a marriage to a people driven out of a land, and the vocabulary is deliberately "
  "the same."),
],
10: [
 ("The Luxuriant Vine: Prosperity Breeds Idolatry (vv.1-2)",
  "Israel is an empty vine, he bringeth forth fruit unto himself. The Hebrew supports both "
  "the older rendering and the modern luxuriant vine, and the ambiguity is useful, because "
  "the chapter's point is that the two states are the same state, materially full and "
  "producing nothing for God. According to the multitude of his fruit he hath increased "
  "the altars. Prosperity did not reduce the idolatry, it financed it. Their heart is "
  "divided, and a divided heart is the diagnosis, not a compromise."),
 ("Kingless and Helpless (vv.3-4)",
  "We have no king, because we feared not the LORD. The monarchy is spoken of as already "
  "gone, and the loss is traced to the fear of God rather than to Assyrian policy. What "
  "governs in its place is talk, they have spoken words, swearing falsely in making a "
  "covenant. The image is agricultural and ironic, judgment springeth up as hemlock in the "
  "furrows, the field is producing, and what it produces is poison."),
 ("The Calf Departs: Idols Carried Away (vv.5-8)",
  "The inhabitants of Samaria shall fear because of the calves of Beth-aven. The object of "
  "worship is now the object of anxiety, and then it is freight, it shall be also carried "
  "unto Assyria for a present to king Jareb. The god goes into exile as tribute. The high "
  "places are to be overgrown with thorn and thistle, and the people will address the "
  "terrain, they shall say to the mountains, Cover us, and to the hills, Fall on us, a "
  "line Jesus applies to Jerusalem in Luke 23 and John repeats in Revelation 6."),
 ("The Call: Sow Righteousness, Seek the LORD (vv.9-12)",
  "Gibeah is invoked again as the measure of how long this has run. Then, in the middle of "
  "a judgment oracle, the imperative that the whole chapter is remembered for. Sow to "
  "yourselves in righteousness, reap in mercy, break up your fallow ground, for it is time "
  "to seek the LORD, till he come and rain righteousness upon you. Fallow ground is not "
  "barren ground, it is good ground gone hard through disuse, which is the accurate "
  "description of Israel here, and breaking it is work done before there is any sign of "
  "rain."),
 ("The Harvest of Wickedness (vv.13-15)",
  "Ye have plowed wickedness, ye have reaped iniquity, ye have eaten the fruit of lies. "
  "The same agricultural frame, turned back on them, with the cause named: because thou "
  "didst trust in thy chariots and in the multitude of thy mighty men. Then Shalman's "
  "destruction of Beth-arbel is held up as the pattern, the mother dashed in pieces upon "
  "her children, and Bethel is told this is what will be done to it. The chapter that "
  "offered rain ends with a morning in which the king is cut off."),
],
11: [
 ("God's Fatherly Love Recalled (vv.1-4)",
  "The metaphor changes here from husband to father, and the tone changes with it. When "
  "Israel was a child, then I loved him, and called my son out of Egypt. What follows is "
  "domestic and physical: I taught Ephraim to go, taking them by their arms, I drew them "
  "with cords of a man, I laid meat unto them. This is a parent teaching a toddler to "
  "walk and lifting the feeding trough so the animal can reach, and against it stands the "
  "refusal, they knew not that I healed them. Matthew 2:15 takes the phrase about Egypt "
  "and applies it to Jesus."),
 ("The Consequence: Exile Under Assyria (vv.5-7)",
  "He shall not return into the land of Egypt, but the Assyrian shall be his king, because "
  "they refused to return. The refusal and the exile are set side by side using the same "
  "verb, they would not turn back, so they will be taken away. The sword shall abide on "
  "his cities. My people are bent to backsliding, and they called on the idols rather than "
  "on the one who was healing them, though they called him to the most High none at all "
  "would exalt him."),
 ("God's Heart Torn: How Can I Give You Up (vv.8-9)",
  "How shall I give thee up, Ephraim? how shall I deliver thee, Israel? Judgment has been "
  "pronounced and the pronouncer is now arguing against it, and the cities named, Admah "
  "and Zeboim, were destroyed with Sodom and Gomorrah, so what is being refused is that "
  "precedent. Mine heart is turned within me, my repentings are kindled together. Then the "
  "reason, and it is not Israel's improvement: I will not execute the fierceness of mine "
  "anger, for I am God, and not man. The difference between divine and human love is "
  "offered as the explanation, a man at the end of his patience is at the end of it, and "
  "God is not."),
 ("Future Restoration: The Lion Roars (vv.10-11)",
  "They shall walk after the LORD, he shall roar like a lion. The lion appeared in chapter "
  "5 as the predator none could escape, and here the same roar is a summons the scattered "
  "come toward, the children shall tremble from the west. They come as birds out of Egypt "
  "and as a dove out of Assyria, the two empires that had taken them, and the dove is the "
  "same bird that was silly and heartless in chapter 7, now flying home."),
 ("Ephraim's Current State: Lies (v.12)",
  "Ephraim compasseth me about with lies, and the house of Israel with deceit. After the "
  "most tender passage in the book, the chapter closes on the present tense and nothing "
  "has changed on the ground. Judah is mentioned in the same verse, and the Hebrew is "
  "difficult enough that translations split over whether it is being commended or accused. "
  "The restoration in verses 10 and 11 is real and it is not yet."),
],
12: [
 ("Ephraim Feeds on Wind: Useless Alliances (v.1)",
  "Ephraim feedeth on wind, and followeth after the east wind. Wind is what chapter 8 said "
  "they had sown, and here it is what they eat, a diet that cannot sustain anyone. The "
  "specific folly is named at once, they do make a covenant with the Assyrians, and oil is "
  "carried into Egypt. Olive oil was a serious export and it is going out as diplomatic "
  "payment to one empire while a treaty is signed with the other."),
 ("God's Case Against Jacob and Judah (vv.2-6)",
  "The LORD hath also a controversy with Judah, and the legal language of chapter 4 "
  "returns, but the evidence is a family history. He took his brother by the heel in the "
  "womb, and by his strength he had power with God. Jacob is presented twice over, as the "
  "grasper and as the wrestler, and the chapter is interested in the second, he wept, and "
  "made supplication unto him, he found him in Bethel. Then the application, therefore turn "
  "thou to thy God, wait on thy God continually. The ancestor is offered as the route "
  "back."),
 ("The Dishonest Merchant: Self-Deceived (vv.7-8)",
  "He is a merchant, in his hand are the balances of deceit. The heel-grabbing came down "
  "the generations and turned into a rigged scale. What makes it worse than fraud is the "
  "self-assessment that follows, Ephraim said, Yet I am become rich, I have found me out "
  "substance. The profit is read as proof of favor, and the sentence about all his labours "
  "not being found in him is the answer to that reading."),
 ("God's Consistency: Prophets and Visions (vv.9-11)",
  "I am the LORD thy God from the land of Egypt, and the method has not changed either, I "
  "have also spoken by the prophets, I have multiplied visions. God's side of the "
  "relationship is described as continuous where Israel's is described as intermittent. "
  "The tabernacles clause points at the feast that made them live in booths and remember "
  "the wilderness. Gilead and Gilgal are named again, their altars are as heaps in the "
  "furrows of the fields."),
 ("The Jacob Parallel: Served for a Wife (vv.12-13)",
  "Jacob fled into Syria, and served for a wife, and for a wife he kept sheep. The two "
  "verses set fourteen years of shepherding beside the exodus, and by a prophet the LORD "
  "brought Israel out of Egypt, and by a prophet was he preserved. The parallel is between "
  "Jacob serving to gain a wife and God working through Moses to gain a people, and the "
  "prophetic office is the thread. It also answers the merchant of verse 7, the ancestor "
  "worked years for what Ephraim now weighs on a false balance."),
 ("Ephraim's Bitter Provocation (v.14)",
  "Ephraim provoked him to anger with their high places, therefore shall he leave their "
  "blood upon them, and his reproach shall he return unto him. The chapter has offered "
  "Jacob as a model, the prophets as evidence, and turn thou to thy God as an instruction, "
  "and it closes with none of it taken up. The blood clause means responsibility stays "
  "where it was incurred."),
],
13: [
 ("Ephraim's Death Through Baal (vv.1-3)",
  "When Ephraim spake trembling, he was exalted, when he offended in Baal, he died. A "
  "whole history in one verse, and the death is dated to the worship rather than to the "
  "Assyrian army. What follows is the manufacture, they say of the calves, Kiss them, "
  "which is a devotional act performed toward an object someone cast. Then four images of "
  "how fast this disappears, morning cloud, early dew, chaff from the threshing floor, "
  "smoke out of a chimney. Nothing about it holds."),
 ("God's Exclusive Claim: No Saviour Beside Me (vv.4-6)",
  "I am the LORD thy God from the land of Egypt, and thou shalt know no god but me, for "
  "there is no saviour beside me. The claim is exclusive and it is grounded in history "
  "rather than argument. Then the mechanism of the failure, and it is not hardship: I did "
  "know thee in the wilderness, in the land of great drought. According to their pasture, "
  "so were they filled, they were filled, and their heart was exalted, therefore have they "
  "forgotten me. Scarcity kept them attentive and plenty did not."),
 ("God as Predator: Lion, Leopard, Bear (vv.7-8)",
  "I will be unto them as a lion, as a leopard by the way will I observe them. Three "
  "predators in two verses, and the bear is specified as bereaved of her whelps, which is "
  "the most dangerous animal in the list for a reason the book has already established, "
  "the loss is personal. The lion of chapter 5 was judgment and the lion of chapter 11 was "
  "a summons home, and here it is neither, it is simply the end of the hunt."),
 ("Self-Destruction and Divine Help (vv.9-11)",
  "O Israel, thou hast destroyed thyself, but in me is thine help. Both halves are in one "
  "verse, and the second half is offered while the first is being executed. Then the "
  "monarchy is settled with, I will be thy king, where is any other that may save thee? "
  "and the history recalled, I gave thee a king in mine anger, and took him away in my "
  "wrath. The kingship they demanded in 1 Samuel 8 is described as a concession given in "
  "displeasure, not a gift."),
 ("Sin Stored Up and Birth Pangs Coming (vv.12-13)",
  "The iniquity of Ephraim is bound up, his sin is hid. The language is of a document "
  "filed and sealed rather than forgotten, kept on record against a day of reckoning. Then "
  "the second image, the sorrows of a travailing woman shall come upon him, he is an "
  "unwise son who will not come to the birth. A labour that stops halfway kills both, and "
  "the chapter uses it for a nation that has begun a crisis it will not carry through to "
  "anything new."),
 ("Death Defeated (v.14)",
  "I will ransom them from the power of the grave, I will redeem them from death: O death, "
  "I will be thy plagues, O grave, I will be thy destruction. In the darkest chapter of "
  "the book, this. Translators divide over whether the last clause, repentance shall be hid "
  "from mine eyes, keeps it as promise or turns it to challenge, and the Hebrew allows "
  "both. Paul settles the reading he wants at 1 Corinthians 15:55, taking the taunt "
  "against death as answered in the resurrection."),
 ("The East Wind of Judgment on Samaria (vv.15-16)",
  "An east wind shall come, and his spring shall become dry. The wind off the desert is "
  "the one that kills crops, and it is applied to Ephraim, whose name means fruitful. Then "
  "the plainest statement of what is coming, Samaria shall become desolate, and the atrocity "
  "described in the last line, their infants shall be dashed in pieces, and their women "
  "with child shall be ripped up. This is what the Assyrian conquest of 722 BC did, and the "
  "chapter that promised victory over death ends by refusing to soften it."),
],
14: [
 ("The Final Call: Return to the LORD (vv.1-3)",
  "O Israel, return unto the LORD thy God, for thou hast fallen by thine iniquity. The book "
  "that opened with a marriage to a prostitute closes with an invitation, and it comes with "
  "the wording supplied. Take with you words, and say unto him, Take away all iniquity, and "
  "receive us graciously. The prayer given includes what has to be renounced to pray it, "
  "Asshur shall not save us, we will not ride upon horses, neither will we say any more to "
  "the work of our hands, Ye are our gods. Alliance, army and idol, the three things the "
  "book has been arguing about, dropped in one sentence, and the ground of appeal is that "
  "in thee the fatherless findeth mercy."),
 ("God's Seven I Will Promises (vv.4-8)",
  "The answer is a run of first-person commitments. I will heal their backsliding, I will "
  "love them freely, for mine anger is turned away from him. Then the imagery reverses "
  "everything the judgment oracles used: he shall grow as the lily, cast forth his roots as "
  "Lebanon, his beauty as the olive tree, they shall revive as the corn and grow as the "
  "vine. The vine was empty in chapter 10 and the root was dried in chapter 9. God says I "
  "am like a green fir tree, taking the fertility language Baal was worshipped for and "
  "claiming it, and asks Ephraim what he still has to do with idols."),
 ("The Wisdom Conclusion (v.9)",
  "Who is wise, and he shall understand these things? prudent, and he shall know them? for "
  "the ways of the LORD are right, and the just shall walk in them, but the transgressors "
  "shall fall therein. The book ends by stepping out of prophecy into the vocabulary of "
  "Proverbs and handing the reader a test. The same road is walked by one and stumbled over "
  "by the other, which is the point, nothing changes about the way, and everything depends "
  "on who is on it."),
],
}


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for ch in range(1, 15):
        page = f"hosea{ch}"
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
        if extra:
            problems.append(f"{page}: unexpected field(s) {extra[:1]}")
            continue
        for old_s, new_s in FIXES.get(ch, []):
            if old_s not in fields["Historical Context:"]:
                problems.append(f"{page}: fix target absent {old_s!r}")
                continue
            fields["Historical Context:"] = fields["Historical Context:"].replace(
                old_s, new_s)
            notes.append(f"{page}: repaired {old_s[:40]!r}")
        sections = SECTIONS[ch]
        covered = set()
        for label, text in [(w, fields[w]) for w in KEEP] + \
                           [(f"section {h!r}", p) for h, p in sections]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
            if " -- " in text:
                problems.append(f"{page}: double hyphen in {label}")
            if "\u2013" in text:
                problems.append(f"{page}: en-dash in {label}")
            if re.search(r"\b([A-Za-z]{2,})- ([a-z]{2,})\b", text):
                problems.append(f"{page}: broken hyphenation in {label}")
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
