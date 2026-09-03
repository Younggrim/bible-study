#!/usr/bin/env python3
"""
Ezekiel 25 to 32: the oracles against the nations. Eight pages, 197 verses.

Four of these pages carry gapless outlines and are folded. Three have no sublist at all,
ezekiel26, ezekiel27 and ezekiel29, so their sections are written from scratch.

ezekiel26 also carries an inherited item, Tyre's sin (v.2), which is dropped as a field
because its whole substance is folded into the new sections: the commercial motive behind
Aha, she is broken, the thirteen-year Babylonian siege, and Alexander scraping the
mainland ruins into the sea in 332 BC to build his causeway. Nothing in it is lost, and
the script reports the drop so the change is visible rather than silent.

The block ends where the book turns. Chapter 32 closes the foreign oracles with a tour of
the underworld in which every fallen empire has its own plot, and chapter 33 opens the
second half with the news of Jerusalem's fall arriving in Babylonia.

Usage:
    python3 fold_ezekiel_nations.py [--check]
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
KEEP = ("Author:", "Date:", "Classification:", "Key Themes:", "Historical Context:",
        "Notable:")
REPAIRS = {}

SECTIONS = {
"ezekiel25": [
 ("Ammon, and the Word Aha (vv.1-7)",
  "The seven foreign oracles begin, and the charge in every one of the four in this chapter is "
  "something the neighbours said while Jerusalem burned. Ammon's is quoted: because thou saidst, "
  "Aha, against my sanctuary, when it was profaned, and against the land of Israel, when it was "
  "desolate, and against the house of Judah, when they went into captivity. The sentence is "
  "dispossession by desert tribes rather than by an empire, I will deliver thee to the men of the "
  "east, and they shall set their palaces in thee, with Rabbah reduced to a stable for camels. And "
  "each oracle ends the same way, ye shall know that I am the LORD."),
 ("Moab, and Judah Treated as One Nation Among Many (vv.8-11)",
  "Moab's offence is not an act but an assessment, and it is the most theological charge in the "
  "chapter: because Moab and Seir do say, Behold, the house of Judah is like unto all the heathen. "
  "That is, the fall of Jerusalem proved there was nothing to the claim that this people's God was "
  "different. It is exactly the argument the Assyrian officers made at Hezekiah's wall in 2 Chronicles "
  "32, and the reply here is the same, the sentence is passed so that they shall know that I am the "
  "LORD."),
 ("Edom, and Vengeance Against a Brother (vv.12-14)",
  "Because that Edom hath dealt against the house of Judah by taking vengeance, and hath greatly "
  "offended. What aggravates it is family: Edom is Esau's line, so this is a brother settling old "
  "accounts at the worst possible moment. Edom's conduct at the fall of Jerusalem is the whole "
  "subject of Obadiah and the sting in Psalm 137, and Ezekiel comes back to it at chapter 35. The "
  "sentence here is unusual in this section for naming the agent, I will lay my vengeance upon Edom "
  "by the hand of my people Israel."),
 ("Philistia, and the Old Hatred (vv.15-17)",
  "Because the Philistines have dealt by revenge, and have taken vengeance with a despiteful heart, "
  "to destroy it for the old hatred. The phrase is worth pausing on, because the hatred it names had "
  "by this date been running for something like six hundred years, since the period of the judges, "
  "and it outlasted every political arrangement in between. The sentence reaches the specialised "
  "troops and the coastal remnant, I will cut off the Cherethims, and destroy the remnant of the sea "
  "coast."),
],
"ezekiel26": [
 ("The Charge, and the Nations Like Waves (vv.1-6)",
  "The date formula is defective and worth noting, the eleventh year, in the first day of the month, "
  "with no month named, which is the only such gap in the book's fourteen dated oracles. The charge "
  "is again quoted speech, and its motive is commercial: she is broken that was the gates of the "
  "people, she is turned unto me, I shall be replenished, now she is laid waste. Tyre traded by sea "
  "and Jerusalem sat on the inland caravan routes, so the destruction of Judah looked to a Phoenician "
  "merchant like the removal of a competitor and the redirection of traffic. The sentence turns Tyre's "
  "own element against it, I will cause many nations to come up against thee, as the sea causeth his "
  "waves to come up, and states for the first time the detail this chapter is known for, I will also "
  "scrape her dust from her, and make her like the top of a rock."),
 ("Nebuchadnezzar, and the Bare Rock (vv.7-14)",
  "The named agent comes first, I will bring upon Tyrus Nebuchadrezzar king of Babylon, a king of "
  "kings, from the north, with horses and with chariots, and the siege is described in technical "
  "terms, a fort, a mount, engines of war and axes against the towers. Then the pronoun changes at "
  "verse 12, from he to they, and so does the action, they shall lay thy stones and thy timber and "
  "thy dust in the midst of the water. The two halves match two events separated by two and a half "
  "centuries. Nebuchadnezzar besieged the mainland city for thirteen years, from about 585 to 572 BC, "
  "wrecked it, and never took the island fortress half a mile offshore. In 332 BC Alexander took the "
  "island by demolishing the mainland ruins and carrying the stone, timber and rubble into the sea to "
  "build a causeway out to it. That causeway silted up and is now the neck of land the modern town "
  "stands on, and the site of the old mainland city is bare rock, thou shalt be a place for the "
  "spreading of nets."),
 ("The Lament of the Coastland Princes (vv.15-18)",
  "Shall not the isles shake at the sound of thy fall. The mourners are described by what they take "
  "off, which is how rank is registered in this book: the princes of the sea come down from their "
  "thrones, lay away their robes, put off their broidered garments and clothe themselves with "
  "trembling, and sit upon the ground. Their lament is quoted, how art thou destroyed, that wast "
  "inhabited of seafaring men, the renowned city, which wast strong in the sea. They are trading "
  "partners rather than allies, and what frightens them is the precedent rather than the loss."),
 ("Down to the Pit, and Never Found Again (vv.19-21)",
  "The last three verses move from history to the underworld, when I shall bring up the deep upon "
  "thee, and great waters shall cover thee, and then I shall bring thee down with them that descend "
  "into the pit, with the people of old time. The sentence the whole chapter has been working toward "
  "is the final clause, and it is about erasure rather than destruction, thou shalt be no more, "
  "though thou be sought for, yet shalt thou never be found again. For a city whose entire identity "
  "was its name in every port on the Mediterranean, that is the precise reversal of what it had."),
],
"ezekiel27": [
 ("The Ship Built Out of the Whole World (vv.1-11)",
  "The lament for Tyre is built on a single conceit, and it is carried through with unusual "
  "discipline: the city is a ship, and every part of the ship is an import. Fir trees of Senir for "
  "the boards, a cedar of Lebanon for the mast, oaks of Bashan for the oars, benches of ivory out of "
  "Chittim, fine linen with broidered work from Egypt for the sail, blue and purple from the isles of "
  "Elishah for the awning. The crew is foreign in the same way, mariners from Zidon and Arvad, "
  "caulkers from Gebal, soldiers from Persia, Lud and Phut, and Gammadims in the towers. Nothing in "
  "the vessel comes from Tyre. That is the argument, made structurally before it is made in words: a "
  "trading power is an assembly of other people's goods, and the assembly is what can be taken "
  "apart."),
 ("The Trading List (vv.12-25)",
  "Fourteen verses of manifest, and it is the longest commercial inventory in the Bible and a "
  "genuinely useful record of Iron Age Mediterranean and Near Eastern trade. Tarshish brings silver, "
  "iron, tin and lead. Javan, Tubal and Meshech bring slaves and vessels of brass. Togarmah brings "
  "horses and mules, Dedan ivory and ebony, Syria emeralds, purple, embroidery, fine linen, coral and "
  "agate. Damascus sends wine and white wool, Arabia and Kedar send lambs, rams and goats, Sheba and "
  "Raamah send spices, precious stones and gold. Judah and Israel appear in the list too, and what "
  "they supply is worth noticing beside the previous chapter's rivalry: wheat of Minnith, honey, oil "
  "and balm, that is, farm produce. The section closes on reputation, the ships of Tarshish did sing "
  "of thee in thy market."),
 ("The Ship Broken in the East Wind (vv.26-36)",
  "Thy rowers have brought thee into great waters, the east wind hath broken thee in the midst of the "
  "seas. The wreck is itemised in the same manner as the cargo, which is the point of having "
  "itemised the cargo: thy riches, and thy fairs, thy merchandise, thy mariners, and thy pilots, thy "
  "caulkers, and all thy men of war shall fall into the midst of the seas in the day of thy ruin. "
  "Everything the ship was made of goes down at once. The coastlands hear the cry of the pilots and "
  "come out to mourn with dust on their heads and ashes to wallow in, and their lament asks a "
  "question a commercial city has no answer to, what city is like Tyrus, like the destroyed in the "
  "midst of the sea. The closing line is deliberately flat, thou shalt be a terror, and never shalt "
  "be any more."),
],
"ezekiel28": [
 ("The Prince of Tyre, Who Said I Am a God (vv.1-10)",
  "The charge is a quotation, thine heart is lifted up, and thou hast said, I am a God, I sit in the "
  "seat of God, in the midst of the seas, and the refutation is immediate and repeated, yet thou art "
  "a man, and not God. What produced the claim is named precisely, and it is not military conquest, "
  "with thy wisdom and with thine understanding thou hast gotten thee riches, by thy great wisdom and "
  "by thy traffick hast thou increased thy riches. Commercial genius is the specific form the pride "
  "takes. The reigning king of Tyre in this period was Ithobaal III. The sentence ends with the claim "
  "turned into a question at the worst moment for answering it, wilt thou then be a man, and no God, "
  "in the hand of him that slayeth thee."),
 ("The King of Tyre, and the Anointed Cherub (vv.11-19)",
  "A second lament, and its language goes well beyond anything that can be said of a Phoenician "
  "monarch. Thou hast been in Eden the garden of God, with nine precious stones named as a covering; "
  "thou art the anointed cherub that covereth, and I have set thee so; thou wast upon the holy "
  "mountain of God; thou wast perfect in thy ways from the day that thou wast created, till iniquity "
  "was found in thee. How much of this is about a king and how much about a being behind him has been "
  "argued since the church fathers, and readers from Tertullian onward have taken it as a description "
  "of Satan's fall. Others read it as court poetry using the Eden story to describe royal hubris, "
  "which is what Isaiah 14 does with the king of Babylon. The text itself supplies both an unearthly "
  "vocabulary and an entirely commercial cause, by the multitude of thy merchandise they have filled "
  "the midst of thee with violence, and thou hast corrupted thy wisdom by reason of thy brightness."),
 ("Sidon (vv.20-23)",
  "Four verses for a city that had been Tyre's rival and senior partner by turns, and the "
  "disproportion against Tyre's three chapters is itself informative about who mattered "
  "commercially. No specific offence is named. What is stated instead is a purpose, and I will be "
  "glorified in the midst of thee, with pestilence and blood in her streets as the means, and the "
  "usual closing formula, and they shall know that I am the LORD."),
 ("No More a Pricking Brier for Israel (vv.24-26)",
  "The last three verses explain what the seven foreign oracles were for, and there shall be no more "
  "a pricking brier unto the house of Israel, nor any grieving thorn of all that are round about them, "
  "that despised them. The phrase is borrowed from Numbers 33:55, where the nations left unremoved in "
  "the land were warned of in exactly those words, so the oracles are presented as finishing an old "
  "piece of business. What they clear the ground for is described in ordinary terms, they shall dwell "
  "safely therein, and shall build houses, and plant vineyards, which is the subject of the second "
  "half of the book."),
],
"ezekiel29": [
 ("The Dragon in the River, and the Staff of Reed (vv.1-7)",
  "The tenth year, tenth month, twelfth day, and the address is to Pharaoh king of Egypt, the great "
  "dragon that lieth in the midst of his rivers. The charge is a claim of ownership and of authorship "
  "over the Nile, which hath said, My river is mine own, and I have made it for myself. The sentence "
  "is worked out in fishing imagery, I will put hooks in thy jaws, and cause the fish of thy rivers "
  "to stick unto thy scales, and I will bring thee up out of the midst of thy rivers. Then the reason "
  "Judah is implicated at all, described from the point of view of the man doing the leaning, thou "
  "hast been a staff of reed to the house of Israel, when they took hold of thee by thy hand, thou "
  "didst break, and rend all their shoulder. A reed does not merely fail to hold, it splinters and "
  "injures the hand that trusted it."),
 ("Forty Years, and a Base Kingdom (vv.8-16)",
  "The desolation is described from the tower of Syene even unto the border of Ethiopia, that is, the "
  "whole length of the country, and the term is forty years, the same span as Israel's wilderness. "
  "Then a restoration, and its terms are the most carefully limited in the prophets: I will bring "
  "again the captivity of Egypt, and they shall be there a base kingdom, it shall be the basest of "
  "the kingdoms, neither shall it exalt itself any more above the nations. Egypt is not destroyed and "
  "not restored to greatness. The purpose is stated in terms of Judah's politics rather than Egypt's "
  "deserts, and it shall be no more the confidence of the house of Israel, which is to say the "
  "temptation is removed by reducing the size of the thing tempting."),
 ("Egypt as Wages for the Army at Tyre (vv.17-21)",
  "Dated the twenty-seventh year, seventeen years after the oracle above it, which makes this the "
  "latest dated word in the book apart from the temple vision. It is also the one place where "
  "Ezekiel comments on how one of his own prophecies turned out. Nebuchadrezzar king of Babylon "
  "caused his army to serve a great service against Tyrus, and the cost is described physically, "
  "every head was made bald, and every shoulder was peeled, from thirteen years of hauling siege "
  "material. And yet had he no wages: the island held, and the plunder never came. So Egypt is "
  "assigned as compensation, I will give the land of Egypt unto Nebuchadrezzar, and it shall be the "
  "wages for his army. The chapter closes by turning back to Israel, in that day will I cause the "
  "horn of the house of Israel to bud."),
],
"ezekiel30": [
 ("The Day of the LORD Against Egypt (vv.1-5)",
  "Howl ye, Woe worth the day, for the day is near, even the day of the LORD is near, a cloudy day, "
  "it shall be the time of the heathen. The phrase the day of the LORD is used here of a foreign "
  "nation's collapse, which is how this book and Amos both use it: not one event at the end of "
  "history but a day of reckoning wherever it falls. Who goes down with Egypt is listed, Ethiopia, "
  "Libya, Lydia, all the mingled people, Chub, and the men of the league, that is, the mercenary and "
  "treaty forces an empire hires and cannot save."),
 ("The Allies Fall Together (vv.6-9)",
  "The pride of her strength shall come down, and the geography is repeated, from the tower of Syene "
  "shall they fall in it. The phrasing at verse 7 puts Egypt in company rather than alone, they shall "
  "be desolate in the midst of the countries that are desolate, so the point is that Egypt is not "
  "exceptional. The section ends with news travelling by water, messengers going forth in ships to "
  "make the careless Ethiopians afraid, and the adjective careless is doing the work: they are about "
  "to hear something they had no plans for."),
 ("Nebuchadnezzar as the Instrument (vv.10-12)",
  "I will make the multitude of Egypt to cease by the hand of Nebuchadrezzar king of Babylon, and the "
  "instrument is described without flattery, he and his people with him, the terrible of the nations, "
  "shall be brought to destroy the land. The final clause is the one that matters for Egypt "
  "specifically, and I will make the rivers dry. Everything Egyptian agriculture, transport and "
  "religion rested on was the annual behaviour of one river, so drying it is not one calamity among "
  "several."),
 ("City by City (vv.13-19)",
  "The judgment is itemised by place, and the list doubles as a map of Egyptian religion and "
  "administration. Noph is Memphis, the old capital, and its idols and its prince are named. No is "
  "Thebes, the great southern cult centre. Sin is Pelusium, which the text calls the strength of "
  "Egypt because it guarded the eastern approach. Aven is On, the Greek Heliopolis, centre of sun "
  "worship. Pibeseth is Bubastis, and Tehaphnehes is Daphnae, the frontier garrison town Jeremiah "
  "was taken to. Every name on the list is a fortress, a shrine, or both, which is the point of "
  "naming them rather than saying Egypt again."),
 ("Pharaoh's Arms Broken (vv.20-26)",
  "Dated the eleventh year, first month, seventh day, and it opens with something already done, I "
  "have broken the arm of Pharaoh king of Egypt. The reference is to a specific failure: Hophra "
  "marched out to relieve the siege of Jerusalem and withdrew, and Jeremiah 37 describes the brief "
  "lifting of the siege and the return of the Babylonians. Then the escalation, I will break his "
  "arms, the strong, and that which was broken, that is, both the sound arm and the one already "
  "broken, so that the sword shall fall out of his hand. And the transfer, I will strengthen the arms "
  "of the king of Babylon, and put my sword in his hand."),
],
"ezekiel31": [
 ("Whom Art Thou Like (vv.1-2)",
  "The eleventh year, third month, first day, and the oracle opens with a question put to Pharaoh and "
  "to his multitude, Whom art thou like in thy greatness. The chapter answers it with Assyria, and "
  "the choice is pointed. Assyria had dominated the entire Near East for three centuries and had "
  "collapsed within living memory, Nineveh falling in 612 BC. Egypt is being invited to compare "
  "itself with the largest thing anyone in the audience had watched disappear."),
 ("The Cedar in Lebanon (vv.3-9)",
  "Behold, the Assyrian was a cedar in Lebanon with fair branches, and with a shadowing shroud, and "
  "of an high stature. The description is of a tree that provides for everything under it, all the "
  "fowls of heaven made their nests in his boughs, and under his branches did all the beasts of the "
  "field bring forth their young, and under his shadow dwelt all great nations. Two details make it "
  "more than praise. His height came from somewhere else, the waters made him great, the deep set him "
  "up on high. And the comparison is drawn inside Eden, the cedars in the garden of God could not "
  "hide him. This is the same sheltering tree that chapter 17 ended on as a promise, used here as an "
  "obituary."),
 ("The Heart Lifted Up (vv.10-11)",
  "Because thou hast lifted up thyself in height, and his heart is lifted up in his height, therefore "
  "have I delivered him into the hand of the mighty one of the heathen. The diagnosis is word for word "
  "the one given to Tyre three chapters earlier and to Uzziah in 2 Chronicles 26, and the "
  "repetition is the argument: the same failure is being described in a Phoenician merchant, an "
  "Assyrian empire, an Egyptian pharaoh and a king of Judah, and the size of the subject makes no "
  "difference to it."),
 ("Cut Down, and the Nations Gone from Under It (vv.12-14)",
  "The terrible of the nations have cut him off, and have left him, and the felling is described by "
  "where the debris lands, upon the mountains and in all the valleys his branches are fallen. What "
  "happens to the tenants is stated separately and coldly, all the people of the earth are gone down "
  "from his shadow, and have left him. The purpose given for felling the largest tree is deterrence "
  "for the rest of the forest, to the end that none of all the trees by the waters exalt themselves "
  "for their height."),
 ("Sheol, and the Comfort of Company (vv.15-18)",
  "The descent is accompanied by mourning on a geological scale, I covered the deep for him, and the "
  "great waters were stayed, and Lebanon fainted for him. The dependents follow him down, they that "
  "be his arms, that dwelt under his shadow in the midst of the heathen, went down into hell with "
  "him. Then the last verse turns from Assyria to the reader it was aimed at from the beginning, this "
  "is Pharaoh and all his multitude, saith the Lord GOD. The consolation offered in these chapters is "
  "always the same and always bleak, and it is stated here as a fact rather than as an offer: he "
  "shall be comforted by finding out who else is down there."),
],
"ezekiel32": [
 ("The Dragon Taken in a Net (vv.1-10)",
  "The twelfth year, twelfth month, first day. The image is corrected in the opening line, thou art "
  "as a whale in the seas, not a lion among the nations, and the charge is disturbance, thou camest "
  "forth with thy rivers, and troubledst the waters. The capture is by net rather than by battle, I "
  "will spread out my net upon thee. What follows is the standard vocabulary of the day of the LORD "
  "applied to one national collapse, I will cover the heaven, and make the stars thereof dark, I will "
  "cover the sun with a cloud, and the moon shall not give her light, which is the language Joel and "
  "Amos use and which the Gospels take up. The effect described is political, their kings shall be "
  "horribly afraid for thee."),
 ("The Sword of Babylon, and the Waters Made Deep (vv.11-16)",
  "The sword of the king of Babylon shall come upon thee, and the destruction reaches the animals as "
  "well as the people, I will destroy all the beasts thereof from beside the great waters. Then an "
  "image of stillness that is more unsettling than the violence, then will I make their waters deep, "
  "and cause their rivers to run like oil. A river running like oil is a river with no traffic on it. "
  "The section closes by naming its own genre twice, this is the lamentation wherewith they shall "
  "lament her, the daughters of the nations shall lament her."),
 ("The Descent, and the Tour of the Pit (vv.17-21)",
  "Wail for the multitude of Egypt, and cast them down, her, and the daughters of the famous nations, "
  "unto the nether parts of the earth. What begins here is one of the strangest passages in the "
  "prophets: a guided walk through the underworld in which each fallen empire has its own plot and "
  "its own company, and the residents speak, the strong among the mighty shall speak to him out of "
  "the midst of hell. The instruction to Pharaoh is to take his place in it, go down, and be thou "
  "laid with the uncircumcised."),
 ("Assyria in the Pit (vv.22-23)",
  "Asshur is there and all her company, his graves are about him, all of them slain, fallen by the "
  "sword. The epitaph attached is repeated over almost every nation in the tour and is the only thing "
  "any of them is remembered for, which caused terror in the land of the living. Assyria is placed "
  "first because chapter 31 has just spent eighteen verses on it."),
 ("Elam in the Pit (vv.24-25)",
  "There is Elam and all her multitude round about her grave, all of them slain, gone down "
  "uncircumcised into the nether parts of the earth. Elam lay east of Babylonia and had been a power "
  "in its own right for over a thousand years. The clause added to its entry is about what it "
  "brought with it, yet have they borne their shame with them that go down to the pit."),
 ("Meshech and Tubal in the Pit (vv.26-28)",
  "There is Meshech, Tubal, and all her multitude, peoples of Anatolia who reappear at the head of "
  "Gog's coalition in chapters 38 and 39. Their entry carries a distinction that is easy to miss, "
  "and they shall not lie with the mighty that are fallen of the uncircumcised, which seems to "
  "concern honourable burial, since the mighty in the next clause are described as going down to hell "
  "with their weapons of war, and they have laid their swords under their heads."),
 ("Edom in the Pit (v.29)",
  "One verse, and it names the leadership rather than the population, there is Edom, her kings, and "
  "all her princes, which with their might are laid by them that were slain by the sword. Edom had "
  "been the subject of an oracle four chapters earlier and will get a full chapter at 35, so its "
  "single line here is a placement rather than a summary."),
 ("Sidon and the Princes of the North (v.30)",
  "There be the princes of the north, all of them, and all the Zidonians, which are gone down with "
  "the slain. The same clause that followed Elam follows them, they have borne their shame with them "
  "that go down to the pit, which is this passage's way of saying that a nation's reputation is "
  "buried with it and not before it."),
 ("Pharaoh Comforted Among Them (vv.31-32)",
  "Pharaoh shall see them, and shall be comforted over all his multitude, and the comfort is nothing "
  "more than the company: the largest surviving power in the region is consoled by discovering that "
  "everyone else is already there. The closing line ends the chapter and the whole section of "
  "oracles against the nations, and I will lay him with the slain, saith the Lord GOD. What comes "
  "next is chapter 33, where the watchman's commission is restated and a fugitive arrives in "
  "Babylonia with the news that Jerusalem has fallen."),
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
