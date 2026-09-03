#!/usr/bin/env python3
"""
Isaiah 13 to 23: the oracles against the nations. Eleven pages, 189 verses.

Ten of the eleven outlines fold as they stand. isaiah15's does not: it carried a section
at verse 5 and another at verses 5 to 7, so verse 5 was described twice. The two are
merged into one section covering 5 to 7, which is where the flight south is described
and where the prophet's own cry sits inside it.

These chapters are usually read as a block of foreign judgment, and the striking thing
about them is how often they end somewhere else. Isaiah 19 finishes with an altar to the
LORD in Egypt and a highway joining Egypt, Assyria and Israel, with Egypt called my
people. Isaiah 18 has Cush bringing tribute to Zion. Isaiah 23 gives Tyre seventy years
and then a restoration. Judgment on the nations in this book is repeatedly a route into
something else, and the sections say so where the text does.

isaiah14:12-15 is the passage behind the name Lucifer, which is the Latin translation of
a Hebrew phrase meaning shining one, son of the morning. The section says what the words
mean and what the passage is addressed to, and leaves the later identification as later.

Usage:
    python3 fold_isaiah_nations.py [--check]
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
"isaiah13": [
 ("The Mustered Army (vv.1-5)",
  "The burden of Babylon, which Isaiah the son of Amoz did see, and the heading matters because Babylon "
  "was not yet the threat when Isaiah wrote; Assyria was. Lift ye up a banner upon the high mountain, "
  "exalt the voice unto them. The troops are described in an unexpected way, I have commanded my "
  "sanctified ones, I have also called my mighty ones for mine anger, so a foreign army is spoken of as "
  "consecrated for the purpose. And the muster is drawn from a great distance, the LORD of hosts "
  "mustereth the host of the battle, they come from a far country, from the end of heaven."),
 ("The Day of the LORD (vv.6-13)",
  "Howl ye, for the day of the LORD is at hand, it shall come as a destruction from the Almighty. The "
  "physical description is of a body in shock, all hands shall be faint, and every man's heart shall "
  "melt, and they shall be afraid, pangs and sorrows shall take hold of them. Then the sky goes out, "
  "the stars of heaven and the constellations thereof shall not give their light, the sun shall be "
  "darkened in his going forth, and the moon shall not cause her light to shine. That vocabulary "
  "becomes standard, running through Joel, Ezekiel 32 and the Gospels. And the target is named as a "
  "quality rather than a nation, I will cause the arrogancy of the proud to cease."),
 ("The Slaughter (vv.14-18)",
  "They shall be as a chased roe, and as a sheep that no man taketh up, every man shall turn to his own "
  "people, and flee every one into his own land. What follows is the ugliest passage in these chapters "
  "and it is not softened, their children also shall be dashed to pieces before their eyes. The Medes "
  "are named as the agent, and the detail given about them is commercial rather than military, they "
  "shall not regard silver, and as for gold, they shall not delight in it. An army that cannot be "
  "bought off is the specific horror being described."),
 ("Babylon's Permanent Desolation (vv.19-22)",
  "And Babylon, the glory of kingdoms, the beauty of the Chaldees' excellency, shall be as when God "
  "overthrew Sodom and Gomorrah. What is promised is not conquest but abandonment, and it is measured "
  "by who moves in: it shall never be inhabited, neither shall the Arabian pitch tent there, neither "
  "shall the shepherds make their fold there, but wild beasts of the desert shall lie there, and owls "
  "shall dwell there, and satyrs shall dance there. Even nomads will not camp on the site. The city was "
  "in fact taken intact by Cyrus in 539 BC and declined slowly over centuries, which is the shape most "
  "of these oracles' fulfilment takes."),
],
"isaiah14": [
 ("The LORD Will Have Mercy on Jacob (vv.1-2)",
  "Before the taunt-song begins, two verses establish why it is being sung. For the LORD will have mercy "
  "on Jacob, and will yet choose Israel, and set them in their own land. Then a clause that is easy to "
  "read past, and the strangers shall be joined with them, and they shall cleave to the house of Jacob. "
  "The restoration is not exclusive even here, in the middle of the harshest oracles in the book."),
 ("The Taunt-Song Against the King of Babylon (vv.3-11)",
  "Thou shalt take up this proverb against the king of Babylon, and the word rendered proverb is mashal, "
  "which here means a taunt-song. It opens with a question rather than a curse, how hath the oppressor "
  "ceased, the golden city ceased. Then the reaction of the natural world, which is relief, the whole "
  "earth is at rest, and is quiet, they break forth into singing, yea, the fir trees rejoice at thee. "
  "And then the arrival in the underworld, which is the most theatrical scene in the book: hell from "
  "beneath is moved for thee, it stirreth up the dead for thee, and the kings of the nations rise from "
  "their thrones to greet him with one line, art thou also become weak as we, art thou become like unto "
  "us. And the last detail is bedding, the worm is spread under thee, and the worms cover thee."),
 ("How Art Thou Fallen from Heaven (vv.12-15)",
  "How art thou fallen from heaven, O Lucifer, son of the morning. The name is not in the Hebrew. The "
  "phrase there is helel ben shachar, shining one, son of the dawn, and Lucifer is the Latin the "
  "Vulgate used for it, light-bearer, which was the ordinary Latin word for the morning star. What "
  "follows is five sentences all beginning I will, I will ascend into heaven, I will exalt my throne "
  "above the stars of God, I will sit also upon the mount of the congregation, I will ascend above the "
  "heights of the clouds, I will be like the most High. And the reply is one line, yet thou shalt be "
  "brought down to hell. From the church fathers onward this has been read as an account of Satan's "
  "fall, partly because Jesus speaks of Satan falling as lightning from heaven in Luke 10. What the "
  "passage itself is addressed to, at verse 4, is the king of Babylon."),
 ("The King's Shameful End (vv.16-23)",
  "The scene returns to the surface and to onlookers examining a corpse, they that see thee shall "
  "narrowly look upon thee, and say, Is this the man that made the earth to tremble. The specific "
  "indignity is burial, and it is stated by contrast, all the kings of the nations lie in glory, every "
  "one in his own house, but thou art cast out of thy grave like an abominable branch. Then the sentence "
  "on the dynasty rather than the man, I will cut off from Babylon the name, and remnant, and son, and "
  "nephew. And the city is left to the water, I will make it a possession for the bittern, and pools of "
  "water."),
 ("Oracle Against Assyria (vv.24-27)",
  "Four verses, and they are the ones that mattered most to the original audience, since Assyria was the "
  "power actually at the door. The LORD of hosts hath sworn, saying, Surely as I have thought, so shall "
  "it come to pass. I will break the Assyrian in my land, and upon my mountains tread him under foot. "
  "And the closing question makes the point of the whole chapter, for the LORD of hosts hath purposed, "
  "and who shall disannul it, and his hand is stretched out, and who shall turn it back."),
 ("Oracle Against Philistia (vv.28-32)",
  "Dated in the year that king Ahaz died. Rejoice not thou, whole Palestina, because the rod of him that "
  "smote thee is broken, which warns against celebrating the death of an oppressor on the grounds that "
  "the replacement will be worse, out of the serpent's root shall come forth a cockatrice. And the "
  "chapter closes with a question and an answer that turn the whole block of oracles back toward Judah, "
  "what shall one answer the messengers of the nations, that the LORD hath founded Zion, and the poor of "
  "his people shall trust in it."),
],
"isaiah15": [
 ("Overnight Destruction (vv.1-4)",
  "The burden of Moab, and the speed is the first thing stated, in the night Ar of Moab is laid waste. "
  "The mourning is described town by town and posture by posture: on the tops of the houses, and in the "
  "streets thereof, every one shall howl, weeping abundantly. Every head shall be baldness, and every "
  "beard cut off, which are the customary signs and also, under Israelite law, forbidden ones. And the "
  "soldiers are named as mourners rather than as casualties, therefore the armed soldiers of Moab shall "
  "cry out, his life shall be grievous unto him."),
 ("The Flight South (vv.5-7)",
  "My heart shall cry out for Moab. That is the prophet's own voice inside an oracle of judgment against "
  "a hostile neighbour, and it is the same instinct Jeremiah 48 shows at greater length. Then the "
  "refugees are tracked along a road, his fugitives shall flee unto Zoar, they shall go it up with "
  "weeping, and by the way of Horonaim they shall raise up a cry of destruction. And what they are "
  "carrying is itemised, therefore the abundance they have gotten shall they carry away to the brook of "
  "the willows, which is a picture of a whole population moving with what it can lift."),
 ("Weeping Everywhere (vv.8-9)",
  "For the cry is gone round about the borders of Moab, the howling thereof unto Eglaim, and the howling "
  "thereof unto Beer-elim. The oracle measures the disaster by how far the sound travels rather than by "
  "casualties. And the last verse takes what was already bad and adds to it, for the waters of Dimon "
  "shall be full of blood, for I will bring more upon Dimon, lions upon him that escapeth of Moab. Even "
  "the survivors are given something further to survive."),
],
"isaiah16": [
 ("Send the Lamb, and Hide the Outcasts (vv.1-5)",
  "Send ye the lamb to the ruler of the land, which is an instruction to Moab to resume paying the "
  "tribute 2 Kings 3 records it once paying to Israel. Then a request put in Moab's mouth, and it is a "
  "request for asylum, hide the outcasts, bewray not him that wandereth, let mine outcasts dwell with "
  "thee, Moab, be thou a covert to them from the face of the spoiler. And the ground offered for "
  "granting it is a promise about the throne in Jerusalem, and in mercy shall the throne be established, "
  "and he shall sit upon it in truth, judging, and seeking judgment. A hostile neighbour is invited to "
  "shelter refugees on the strength of what David's line is going to be."),
 ("Moab's Pride Prevents Mercy (vv.6-7)",
  "We have heard of the pride of Moab, he is very proud, even of his haughtiness, and his pride, and his "
  "wrath, but his lies shall not be so. The stacked synonyms are the same device Jeremiah 48:29 uses on "
  "the same nation. And then the consequence, therefore shall Moab howl for Moab, every one shall howl. "
  "The asylum offered in the previous section is not withdrawn; what is stated is that Moab will not be "
  "in a position to grant it."),
 ("The Vineyards of Sibmah (vv.8-12)",
  "Moab's economy was wine, and what is mourned is the vine, for the fields of Heshbon languish, and the "
  "vine of Sibmah, the lords of the heathen have broken down the principal plants thereof. Then the "
  "prophet again puts himself in it, therefore I will bewail with the weeping of Jazer the vine of "
  "Sibmah, I will water thee with my tears. The specific loss named is a sound, the shouting for thy "
  "summer fruits is fallen, and I have made the vintage shouting to cease. And the last verse is about "
  "exhausted religion, when it is seen that Moab is weary on the high place, he shall come to his "
  "sanctuary to pray, but he shall not prevail."),
 ("The Three-Year Countdown (vv.13-14)",
  "This is the word that the LORD hath spoken concerning Moab since that time. Then a dated addendum "
  "that converts a poem into a forecast, but now the LORD hath spoken, saying, Within three years, as "
  "the years of an hireling, and the glory of Moab shall be contemned. The comparison with a hired man's "
  "contract is doing precise work: a hireling counts his term exactly and does not extend it, so three "
  "years means three years."),
],
"isaiah17": [
 ("The Ruin of Damascus (vv.1-3)",
  "Behold, Damascus is taken away from being a city, and it shall be a ruinous heap. Damascus fell to "
  "Assyria in 732 BC, so this oracle concerns the northern half of the coalition that had frightened "
  "Ahaz in chapter 7. And the fortress of Ephraim is put in the same sentence as the Syrian capital, "
  "the fortress also shall cease from Ephraim, and the kingdom from Damascus, because the two had made "
  "themselves one policy and are given one sentence."),
 ("The Decline of Jacob (vv.4-6)",
  "In that day the glory of Jacob shall be made thin, and the fatness of his flesh shall wax lean. Then "
  "two agricultural pictures of what a remnant actually looks like. The first is harvest, and it shall "
  "be as when the harvestman gathereth the corn, in the valley of Rephaim, that is, a field stripped "
  "clean. The second is more exact, yet gleaning grapes shall be left in it, as the shaking of an olive "
  "tree, two or three berries in the top of the uppermost bough, four or five in the outmost fruitful "
  "branches. A counted handful in the parts of the tree the pickers could not reach."),
 ("The Remnant Turns to Their Maker (vv.7-8)",
  "In that day shall a man look to his Maker, and his eyes shall have respect to the Holy One of Israel. "
  "And what he stops looking at is named specifically, he shall not look to the altars, the work of his "
  "hands, neither shall respect that which his fingers have made. The phrase the work of his hands is "
  "the whole argument compressed: what disqualifies the altars is that he built them."),
 ("Because Thou Hast Forgotten (vv.9-11)",
  "His strong cities shall be as a forsaken bough, and the cause is stated flatly, because thou hast "
  "forgotten the God of thy salvation. Then an image drawn from horticulture that is probably a "
  "reference to the fertility gardens of the period, thou shalt plant pleasant plants, and shalt set it "
  "with strange slips, in the day shalt thou make thy plant to grow, and in the morning shalt thou make "
  "thy seed to flourish. Forced growth, and then the result, but the harvest shall be a heap in the day "
  "of grief and of desperate sorrow."),
 ("The Rushing of Many Waters (vv.12-14)",
  "Woe to the multitude of many people, which make a noise like the noise of the seas. The nations are "
  "described entirely by sound and then dismissed with two similes about how quickly noise stops, God "
  "shall rebuke them, and they shall flee far off, and shall be chased as the chaff of the mountains "
  "before the wind, and like a rolling thing before the whirlwind. And the timing is the point of the "
  "last verse, and behold at eveningtide trouble, and before the morning he is not. Overnight."),
],
"isaiah18": [
 ("The Land Beyond the Rivers of Cush (vv.1-2)",
  "Woe to the land shadowing with wings, which is beyond the rivers of Ethiopia, that sendeth "
  "ambassadors by the sea, even in vessels of bulrushes upon the waters. Papyrus boats on the Nile are "
  "being described, and the ambassadors are almost certainly recruiting for an anti-Assyrian alliance, "
  "which is the diplomacy Isaiah spends these chapters opposing. The people are described respectfully, "
  "which is unusual in an oracle, a nation meted out and trodden down, terrible from their beginning."),
 ("The World Summoned to Watch (v.3)",
  "One verse, and it turns the audience from an embassy into everybody, all ye inhabitants of the world, "
  "see ye, when he lifteth up an ensign on the mountains, and when he bloweth a trumpet, hear ye. What "
  "is being arranged is not a private judgment on one nation but something staged to be watched, which "
  "is why the verse stands on its own between the address and the action."),
 ("God Waits Quietly, Then Prunes (vv.4-6)",
  "For so the LORD said unto me, I will take my rest, and I will consider in my dwelling place like a "
  "clear heat upon herbs, and like a cloud of dew in the heat of harvest. The stillness is deliberate "
  "and it is the most interesting thing in the chapter: what is described is not inactivity but the "
  "quiet of a grower waiting for exactly the right moment. And the moment is horticultural, for afore "
  "the harvest, when the bud is perfect, and the sour grape is ripening in the flower, he shall both cut "
  "off the sprigs with pruning hooks. The intervention comes just before the crop matures, which is when "
  "cutting costs most."),
 ("Cush Brings Tribute to Zion (v.7)",
  "In that time shall the present be brought unto the LORD of hosts of a people scattered and peeled, to "
  "the place of the name of the LORD of hosts, the mount Zion. The chapter that opened with woe closes "
  "with the same nation arriving with a gift, and Psalm 68:31 and Acts 8, where an Ethiopian official is "
  "found reading this very book, both belong in the same line of thought."),
],
"isaiah19": [
 ("Civil War and Chaos (vv.1-4)",
  "Behold, the LORD rideth upon a swift cloud, and shall come into Egypt, and the idols of Egypt shall "
  "be moved at his presence. What is predicted first is internal rather than external, and I will set "
  "the Egyptians against the Egyptians, and they shall fight every one against his brother, city against "
  "city, and kingdom against kingdom. Then the failure of the country's information systems, and they "
  "shall seek to the idols, and to the charmers, and to them that have familiar spirits, and to the "
  "wizards. A state that cannot get a straight answer from anyone it consults."),
 ("The Nile Fails (vv.5-10)",
  "And the waters shall fail from the sea, and the river shall be wasted and dried up. For Egypt that "
  "is not one calamity among several, it is the whole economy, and the chapter follows the consequences "
  "down the supply chain: the reeds and flags shall wither, the paper reeds by the brooks shall wither, "
  "the fishers also shall mourn, and all they that cast angle into the brooks shall lament. Then the "
  "textile trade, they that work in fine flax, and they that weave networks, shall be confounded. Every "
  "trade named depends on water and every one of them stops."),
 ("Egypt's Wisdom Fails (vv.11-15)",
  "Surely the princes of Zoan are fools, the counsel of the wise counsellors of Pharaoh is become "
  "brutish. Egypt's reputation for wisdom was ancient and international, so this is an attack on the "
  "thing the country was most confident about, how say ye unto Pharaoh, I am the son of the wise. The "
  "image used is drunkenness, the LORD hath mingled a perverse spirit in the midst thereof, and they "
  "shall be as a drunken man staggereth in his vomit. And the summary is the same as at 9:14, there "
  "shall be no work for Egypt, which the head or tail may do."),
 ("Five Cities Speak the Language of Canaan (vv.16-18)",
  "In that day shall Egypt be afraid because of the LORD of hosts, and the fear is directed at Judah of "
  "all places, and the land of Judah shall be a terror unto Egypt. Then a specific and quietly "
  "extraordinary claim, in that day shall five cities in the land of Egypt speak the language of Canaan, "
  "and swear to the LORD of hosts. Five Egyptian cities keeping the covenant in Hebrew. A Jewish "
  "military colony did later exist at Elephantine with its own temple, and papyri from it survive, which "
  "is the nearest historical anchor for a verse like this."),
 ("An Altar to the LORD in Egypt (vv.19-22)",
  "In that day shall there be an altar to the LORD in the midst of the land of Egypt, and a pillar at "
  "the border thereof to the LORD. Given that Deuteronomy insists on one sanctuary in one place, an "
  "authorised altar in Egypt is a remarkable thing for this book to promise. And the pattern that "
  "follows is the pattern of Judges applied to a foreign nation, they shall cry unto the LORD because of "
  "the oppressors, and he shall send them a saviour, and he shall deliver them. Egypt gets the cycle "
  "Israel got."),
 ("The Highway, and Egypt My People (vv.23-25)",
  "In that day shall there be a highway out of Egypt to Assyria, and the Assyrian shall come into Egypt, "
  "and the Egyptian into Assyria, and they shall serve with one accord. The two superpowers that had "
  "ground Israel between them for two centuries are pictured using a road rather than an army. Then "
  "Israel is placed between them not as a buffer but as a third party of equal standing, and Israel "
  "shall be the third with Egypt and with Assyria, even a blessing in the midst of the land. And the "
  "closing blessing gives each of them a title previously reserved for Israel, blessed be Egypt my "
  "people, and Assyria the work of my hands, and Israel mine inheritance. It is the widest sentence in "
  "the first half of the book."),
],
"isaiah20": [
 ("Ashdod Falls (v.1)",
  "In the year that Tartan came unto Ashdod, when Sargon the king of Assyria sent him, and fought "
  "against Ashdod, and took it. This is one of the most precisely datable verses in the prophets. "
  "Sargon II is named, which is the only occurrence of his name in the Bible, and the campaign against "
  "Ashdod is recorded in his own annals, placing it at 711 BC. Ashdod had led a Philistine revolt "
  "counting on Egyptian support, and the support did not arrive."),
 ("Walk Naked and Barefoot (v.2)",
  "At the same time spake the LORD by Isaiah, saying, Go and loose the sackcloth from off thy loins, and "
  "put off thy shoe from thy foot. And the verse ends with the flattest report of obedience in the "
  "prophets, and he did so, walking naked and barefoot. The word probably means stripped to an "
  "undergarment rather than wholly unclothed, which is how prisoners were marched. It is the longest "
  "sign-act in scripture and the next verse gives its duration."),
 ("Three Years as a Sign (vv.3-4)",
  "Like as my servant Isaiah hath walked naked and barefoot three years for a sign and wonder upon Egypt "
  "and upon Ethiopia. Three years. The interpretation is given in the same terms as the act, so shall "
  "the king of Assyria lead away the Egyptians prisoners, and the Ethiopians captives, young and old, "
  "naked and barefoot, even with their buttocks uncovered. He was not illustrating a defeat, he was "
  "wearing the deportation for three years in public before it happened."),
 ("Their Expectation Ashamed (vv.5-6)",
  "And they shall be afraid and ashamed of Ethiopia their expectation, and of Egypt their glory. The "
  "audience for the sign was never Egypt. It was the party in Jerusalem arguing for an Egyptian "
  "alliance, and the last verse puts their conclusion in their own mouths, behold, such is our "
  "expectation, whither we flee for help, and how shall we escape. Three years of a prophet walking "
  "about half-dressed to make one point about foreign policy."),
],
"isaiah21": [
 ("The Desert of the Sea (vv.1-10)",
  "The burden of the desert of the sea, and the oracle is deliberately disorienting from its title "
  "onward. The prophet reports his own distress at receiving it, therefore are my loins filled with "
  "pain, pangs have taken hold upon me, my heart panted, the night of my pleasure hath he turned into "
  "fear unto me. Then a watchman is posted, set a watchman, let him declare what he seeth, and what he "
  "sees is a chariot with two riders. And the report he brings back is the line the passage is known "
  "for, Babylon is fallen, is fallen, which Revelation 18 takes up word for word. Prepare the table, "
  "watch in the watchtower, eat, drink, arise, ye princes, anoint the shield, which reads as a feast "
  "interrupted."),
 ("The Burden of Dumah (vv.11-12)",
  "Two verses, and they are the most compressed exchange in the book. He calleth to me out of Seir, "
  "Watchman, what of the night, watchman, what of the night. The watchman said, The morning cometh, and "
  "also the night, if ye will enquire, enquire ye, return, come. The question is asked twice and the "
  "answer refuses to be either good news or bad, morning and night together, followed by an invitation "
  "to come back and ask again. It is the least resolved oracle in the collection and it is left that "
  "way."),
 ("The Burden upon Arabia (vv.13-17)",
  "The burden upon Arabia, and it opens with an instruction to the local population to do something "
  "concrete, the inhabitants of the land of Tema brought water to him that was thirsty, they prevented "
  "with their bread him that fled. Caravan traders sheltering refugees from a war. Then the same "
  "hireling's contract that dated the Moab oracle, within a year, according to the years of an "
  "hireling, and all the glory of Kedar shall fail. And the survivors are counted as a small number, "
  "the residue of the number of archers shall be diminished."),
],
"isaiah22": [
 ("The Valley of Vision (vv.1-4)",
  "The burden of the valley of vision, which is Jerusalem itself, and this is the one oracle in the "
  "block aimed at the city rather than at a foreign nation. What is wrong is a mood, thou that art full "
  "of stirs, a tumultuous city, a joyous city, and the population is on the roofs celebrating something. "
  "The prophet's reaction is to refuse consolation, therefore said I, Look away from me, I will weep "
  "bitterly, labour not to comfort me. The reason is in the same verse, for the spoiling of the daughter "
  "of my people."),
 ("The Day of Trouble (vv.5-8a)",
  "For it is a day of treading down, and of perplexity by the Lord of hosts in the valley of vision, "
  "breaking down the walls. Then the coalition arriving, and Elam bare the quiver, with chariots of men "
  "and horsemen, and Kir uncovered the shield, so troops from the far side of Mesopotamia are on Judean "
  "roads. The section stops mid-verse at verse 8 because the sentence turns there from what is done to "
  "Jerusalem to what Jerusalem does about it."),
 ("Ye Looked to the Armour, Not to the Maker (vv.8b-11)",
  "What follows is a list of entirely sensible emergency measures, and the list is the indictment. Thou "
  "didst look in that day to the armour of the house of the forest. Ye have seen also the breaches of "
  "the city of David, that they are many, and ye gathered together the waters of the lower pool, and ye "
  "made a ditch between the two walls for the water of the old pool. That is Hezekiah's tunnel and the "
  "reservoir work of 2 Chronicles 32, real engineering that saved the city. And the charge is not that "
  "they did it but what they left out, but ye have not looked unto the maker thereof, neither had "
  "respect unto him that fashioned it long ago."),
 ("Let Us Eat and Drink (vv.12-14)",
  "And in that day did the Lord God of hosts call to weeping, and to mourning, and to baldness, and to "
  "girding with sackcloth. What he got instead is quoted, and it is the most famous sentence in the "
  "chapter, let us eat and drink, for tomorrow we shall die. Paul quotes it in 1 Corinthians 15 as the "
  "logical position of a man who does not expect a resurrection. And the response here is unusually "
  "final for this book, surely this iniquity shall not be purged from you till ye die."),
 ("The Demotion of Shebna (vv.15-19)",
  "The only oracle in Isaiah addressed to a named civil servant. Go unto this treasurer, even unto "
  "Shebna, which is over the house, and the charge is a tomb, what hast thou here, and whom hast thou "
  "here, that thou hast hewed thee out a sepulchre here, as he that heweth him out a sepulchre on high. "
  "A rock-cut tomb in Jerusalem was a claim to permanence and to standing. The sentence uses two verbs "
  "of throwing, behold, the LORD will carry thee away with a mighty captivity, and will surely violently "
  "turn and toss thee like a ball into a large country."),
 ("The Elevation of Eliakim (vv.20-25)",
  "And it shall come to pass in that day, that I will call my servant Eliakim the son of Hilkiah, and I "
  "will clothe him with thy robe, and strengthen him with thy girdle. Then the phrase that the New "
  "Testament picks up, and the key of the house of David will I lay upon his shoulder, so he shall open, "
  "and none shall shut, and he shall shut, and none shall open, which Revelation 3:7 applies to Christ. "
  "The chapter does not end on the promotion, though. The last verse takes it back, in that day shall "
  "the nail that is fastened in the sure place be removed, and the burden that was upon it shall be cut "
  "off. Even the good appointment is temporary, which is the point of putting the two officials in one "
  "oracle."),
],
"isaiah23": [
 ("Howl, Ye Ships of Tarshish (vv.1-5)",
  "The burden of Tyre, and the news reaches the fleet before it reaches the city, howl, ye ships of "
  "Tarshish, for it is laid waste. Merchant crews arriving from Cyprus find there is no port to unload "
  "at. What Tyre was is stated as commerce rather than conquest, whose merchants are princes, whose "
  "traffickers are the honourable of the earth, and the grain trade is named, the harvest of the river "
  "is her revenue. And Egypt is included in the mourning, because the loss of Tyre's shipping is a loss "
  "to everyone who sold through it."),
 ("Pass Over to Tarshish (vv.6-7)",
  "Pass ye over to Tarshish, howl, ye inhabitants of the isle. Tarshish is at the far western end of "
  "the Mediterranean, so what is being recommended is emigration to the other end of the known world. "
  "Then the question that measures how far the city has come down, is this your joyous city, whose "
  "antiquity is of ancient days. Tyre was old when Jerusalem was young, and the oracle uses its age "
  "against it."),
 ("Who Hath Taken This Counsel (vv.8-9)",
  "Who hath taken this counsel against Tyre, the crowning city, whose merchants are princes. The "
  "question is asked and then answered in the next verse, the LORD of hosts hath purposed it, to stain "
  "the pride of all glory, and to bring into contempt all the honourable of the earth. The stated "
  "purpose is not punishment for a particular crime. It is the deflation of standing as such, which is "
  "the same argument chapter 2 made about everything tall."),
 ("The Colonies Cannot Help (vv.10-12)",
  "Pass through thy land as a river, O daughter of Tarshish, there is no more strength. Tyre's power "
  "rested on a network of colonies and trading partners around the Mediterranean, and the oracle "
  "removes them one clause at a time, he stretched out his hand over the sea, he shook the kingdoms, he "
  "hath given a commandment against the merchant city. And Cyprus is closed as a refuge, pass over to "
  "Chittim, there also shalt thou have no rest."),
 ("Behold the Land of the Chaldeans (vv.13-14)",
  "Behold the land of the Chaldeans, and the verse points at a precedent, he brought it to ruin. The "
  "argument is that what happened once to a great power can happen again, and the section closes by "
  "returning to the opening line so the oracle is framed by it, howl, ye ships of Tarshish, for your "
  "strength is laid waste."),
 ("Seventy Years, and the Hire Made Holy (vv.15-18)",
  "And it shall come to pass in that day, that Tyre shall be forgotten seventy years, according to the "
  "days of one king. Seventy years is the same span Jeremiah gives Babylon, and here it is a lifetime "
  "rather than a symbol. What follows is a strange and rather bleak picture of recovery, the city "
  "described as an aging singer taking up her harp again to be remembered, and its trade called hire. "
  "And then the turn, which is the last thing anybody would expect from these chapters, her merchandise "
  "shall be holiness to the LORD, it shall not be treasured nor laid up, for her merchandise shall be "
  "for them that dwell before the LORD, to eat sufficiently, and for durable clothing. The profits of "
  "the greatest trading city in the world end up as food and clothing for people who serve at the "
  "temple."),
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
