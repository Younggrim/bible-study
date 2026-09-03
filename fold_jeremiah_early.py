#!/usr/bin/env python3
"""
Jeremiah 1 to 10: the call, the temple sermon, and the idol satire. Ten pages,
276 verses.

All 52 Jeremiah pages carry gapless outlines, measured against each chapter's own
verse count, so the whole book folds rather than needing new divisions. The
inherited divisions are kept, the labels are rewritten into the corpus's nominal
style, and prose exposition is written for each.

Three places in this block need a note that says what the difficulty is rather
than smoothing it over. At 4:10 the prophet says God has greatly deceived this
people, and the Hebrew permits both a bitter quotation of the peace-prophets and a
direct accusation; translators have divided over it for centuries. At 7:22 God says
he commanded nothing about burnt offerings, which read flatly contradicts
Leviticus and is normally taken as the Hebrew idiom of relative emphasis. And at
7:16 the office of intercession is withdrawn from Jeremiah, which is the sharpest
thing said to him anywhere in the book.

Usage:
    python3 fold_jeremiah_early.py [--check]
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
"jeremiah1": [
 ("The Priest's Son from Anathoth, and Forty Years of Kings (vv.1-3)",
  "The words of Jeremiah the son of Hilkiah, of the priests that were in Anathoth in the land of "
  "Benjamin. Anathoth was a priestly town about three miles north-east of Jerusalem, and it is where "
  "1 Kings 2:26 records Solomon banishing Abiathar, which may make Jeremiah a descendant of the "
  "deposed priestly line. The dating covers the whole collapse in two verses: the thirteenth year of "
  "Josiah, which is 627 BC, then Jehoiakim, then the eleventh year of Zedekiah, unto the carrying "
  "away of Jerusalem captive in the fifth month. Forty years of preaching are summarised before the "
  "first oracle, so the reader is told the outcome in advance."),
 ("Known Before He Was Formed (vv.4-5)",
  "Before I formed thee in the belly I knew thee, and before thou camest forth out of the womb I "
  "sanctified thee, and I ordained thee a prophet unto the nations. Four verbs, all of them God's, "
  "and all of them complete before the man existed. The last phrase reaches wider than the book "
  "appears to: a prophet unto the nations, which is why chapters 46 to 51 belong in it rather than "
  "sitting as an appendix. Paul uses this verse's language of his own call in Galatians 1."),
 ("The Objection Overruled (vv.6-10)",
  "Then said I, Ah, Lord GOD, behold, I cannot speak, for I am a child. Moses had objected at the "
  "burning bush in almost the same terms and received the same kind of answer, say not, I am a "
  "child, for thou shalt go to all that I shall send thee. What is supplied is not eloquence but "
  "content, and it is described physically, the LORD put forth his hand, and touched my mouth, and "
  "said, Behold, I have put my words in thy mouth. The commission itself is six verbs, and the "
  "proportion holds for most of the book: to root out, and to pull down, and to destroy, and to throw "
  "down, and then to build, and to plant."),
 ("The Almond Rod (vv.11-12)",
  "What seest thou, and I said, I see a rod of an almond tree. The sign turns on a pun that only "
  "works in Hebrew, shaqed for almond against shoqed for watching, so the answer follows from the "
  "object, thou hast well seen, for I will hasten my word to perform it. There is a second reason "
  "for the almond. It is the first tree in the country to blossom, often in January, so the sign is "
  "about being early as much as about being watched."),
 ("The Seething Pot Facing North (vv.13-16)",
  "I see a seething pot, and the face thereof is toward the north, and the interpretation follows the "
  "direction, out of the north an evil shall break forth upon all the inhabitants of the land. Babylon "
  "lies east of Judah, but armies came from the north because the desert closed the direct route, so "
  "north is where invasion arrives from regardless of where the invader lives. The charge is stated "
  "once and briefly, because of all their wickedness, who have forsaken me, and have burned incense "
  "unto other gods, and worshipped the works of their own hands."),
 ("A Defenced City, an Iron Pillar (vv.17-19)",
  "Gird up thy loins, and arise, and speak unto them all that I command thee, be not dismayed at "
  "their faces, lest I confound thee before them. Then the promise, and it is about durability rather "
  "than about safety, I have made thee this day a defenced city, and an iron pillar, and brasen walls "
  "against the whole land. The opposition is itemised so he knows the scope of it, against the kings "
  "of Judah, against the princes thereof, against the priests thereof, and against the people of the "
  "land. And the terms are exact, they shall fight against thee, but they shall not prevail against "
  "thee. He is promised survival, not success, and the book is the record of both halves."),
],
"jeremiah2": [
 ("The Kindness of Thy Youth (vv.1-3)",
  "I remember thee, the kindness of thy youth, the love of thine espousals, when thou wentest after "
  "me in the wilderness, in a land that was not sown. The wilderness is remembered here as a "
  "honeymoon, which is a striking reading of a period the Pentateuch records mostly as complaint, and "
  "the point of remembering it that way is to establish that there was something to fall from. Israel "
  "was holiness unto the LORD, and the firstfruits of his increase, and firstfruits are protected "
  "property, all that devour him shall offend, evil shall come upon them."),
 ("What Iniquity Have Your Fathers Found in Me (vv.4-8)",
  "The charge is put as a legal challenge with the burden reversed, what iniquity have your fathers "
  "found in me, that they are gone far from me, and have walked after vanity, and are become vain. "
  "Then the omission this book returns to again and again, neither said they, Where is the LORD that "
  "brought us up out of the land of Egypt. Nobody asked. And the failure is distributed by office so "
  "that no group is left out: the priests said not, Where is the LORD, they that handle the law knew "
  "me not, the pastors also transgressed against me, and the prophets prophesied by Baal."),
 ("Two Evils, and the Broken Cisterns (vv.9-13)",
  "The argument is comparative and it is put as fieldwork, pass over to Chittim and to Kedar and see "
  "whether any nation has changed its gods, and my people have changed their glory for that which "
  "doth not profit. Then the sentence the chapter is remembered for, my people have committed two "
  "evils, they have forsaken me the fountain of living waters, and hewed them out cisterns, broken "
  "cisterns, that can hold no water. In a country where water was either a spring or a plastered pit "
  "cut in rock, the distinction is between something that keeps arriving on its own and something you "
  "have to fill, that cracks, and that then holds nothing at all."),
 ("Egypt and Assyria, and Wickedness That Corrects Itself (vv.14-19)",
  "Is Israel a servant, is he a homeborn slave, why is he spoiled. The foreign policy is then put as "
  "thirst, what hast thou to do in the way of Egypt, to drink the waters of Sihor, or in the way of "
  "Assyria, to drink the waters of the river, and the unstated answer is that both wells belong to "
  "somebody else. The section closes on a judgment that needs no external agent, thine own wickedness "
  "shall correct thee, and thy backslidings shall reprove thee, know and see that it is an evil thing "
  "that thou hast forsaken the LORD thy God."),
 ("The Noble Vine, and the Wild Ass (vv.20-25)",
  "I had planted thee a noble vine, wholly a right seed, how then art thou turned into the degenerate "
  "plant of a strange vine. The stain will not come out, though thou wash thee with nitre, and take "
  "thee much soap, yet thine iniquity is marked before me. Then two animals, chosen for the same "
  "quality: a wild ass used to the wilderness that snuffeth up the wind, and a dromedary traversing "
  "her ways, both of them following an appetite wherever it leads. And the block ends with the "
  "quotation the whole chapter has been working toward, thou saidst, I will not serve."),
 ("Trees, Stones, and the Number of Thy Cities (vv.26-37)",
  "Saying to a stock, Thou art my father, and to a stone, Thou hast brought me forth, and then the "
  "clause that exposes the arrangement for what it is, but in the time of their trouble they will "
  "say, Arise, and save us. The gods are for the good years. According to the number of thy cities "
  "are thy gods, O Judah, which counts the shrines and works out one per town. The chapter closes on "
  "the alliances failing in sequence, thou shalt be ashamed of Egypt, as thou wast ashamed of "
  "Assyria, and thou shalt go forth from him with thine hands upon thine head, which is the posture "
  "of a prisoner being led away."),
],
"jeremiah3": [
 ("Can a Divorced Wife Return (vv.1-5)",
  "The chapter opens by citing a law and then overriding it. Deuteronomy 24 forbids a man to take "
  "back a wife he divorced who has since married another, and the question here is put in exactly "
  "those terms, shall he return unto her again, shall not that land be polluted. And then, yet return "
  "again to me, saith the LORD. The impossibility is not resolved. It is stated and set aside, which "
  "is the argument of the whole chapter. The quoted piety at the end is part of the problem, wilt "
  "thou not from this time cry unto me, My father, thou art the guide of my youth, behold, thou hast "
  "spoken and done evil things as thou couldest."),
 ("Backsliding Israel and Treacherous Judah (vv.6-11)",
  "Dated in the days of Josiah, so during the most thorough reform the kingdom ever had. The northern "
  "kingdom went up upon every high mountain and played the harlot, and I gave her a bill of divorce, "
  "which is the exile of 722 BC described as a legal proceeding. And Judah watched it happen and "
  "feared not, but went and played the harlot also. The verdict would have been unwelcome in "
  "Jerusalem, the backsliding Israel hath justified herself more than treacherous Judah, and the "
  "reason it stands is that Israel had never had the temple, or Hezekiah, or Josiah."),
 ("Return, for I Am Merciful (vv.12-14)",
  "Go and proclaim these words toward the north, and the audience is the kingdom that had ceased to "
  "exist a century earlier. Return, thou backsliding Israel, and I will not cause mine anger to fall "
  "upon you, for I am merciful, saith the LORD, and I will not keep anger for ever. What is asked is "
  "minimal and is stated as a single condition, only acknowledge thine iniquity, that thou hast "
  "transgressed against the LORD thy God."),
 ("Shepherds, and the Ark Not Missed (vv.15-18)",
  "I will give you pastors according to mine heart, which shall feed you with knowledge and "
  "understanding. Then a sentence that is remarkable coming from a priest's son, they shall say no "
  "more, The ark of the covenant of the LORD, neither shall it come to mind, neither shall they "
  "remember it, neither shall they visit it. The ark vanishes from the record at the fall of "
  "Jerusalem and no biblical text says what became of it, and this verse says in advance that it will "
  "not be missed. The section ends with the reunion Ezekiel 37 signs with two sticks, in those days "
  "the house of Judah shall walk with the house of Israel."),
 ("Why Do You Not Call Me Father (vv.19-25)",
  "I said, thou shalt call me, My father, and shalt not turn away from me, and the disappointment is "
  "put in domestic terms rather than legal ones. Surely as a wife treacherously departeth from her "
  "husband, so have ye dealt treacherously with me. Then a sound from the hills, a voice was heard "
  "upon the high places, weeping and supplications of the children of Israel, which puts mourning "
  "where the idolatry had been. The chapter ends by supplying the words of a confession, we lie down "
  "in our shame, and our confusion covereth us, for we have sinned against the LORD our God. Whether "
  "that is a report or a script being handed to them is left open."),
],
"jeremiah4": [
 ("Circumcise Yourselves to the LORD (vv.1-4)",
  "If thou wilt return, O Israel, return unto me, and put away thine abominations out of my sight. "
  "The demands are then put in two agricultural and one bodily image: break up your fallow ground, "
  "sow not among thorns, and circumcise yourselves to the LORD, and take away the foreskins of your "
  "heart. Turning the covenant sign into a demand about the interior is not new here, Deuteronomy 10 "
  "had done it, and Paul takes it up in Romans 2, but the reason given is immediate and practical, "
  "lest my fury come forth like fire, because of the evil of your doings."),
 ("Blow the Trumpet, the Lion Is Come Up (vv.5-9)",
  "Declare ye in Judah, blow the trumpet, and say, Assemble yourselves, and let us go into the "
  "defenced cities. The invader is introduced by two figures rather than a name, the lion is come up "
  "from his thicket, and the destroyer of the Gentiles is on his way. And the collapse is described "
  "by office, the way this book usually does it, the heart of the king shall perish, and the heart of "
  "the princes, and the priests shall be astonished, and the prophets shall wonder."),
 ("Thou Hast Greatly Deceived This People (v.10)",
  "One verse, and it is the first of the passages that made this book a byword for candour. Then said "
  "I, Ah, Lord GOD, surely thou hast greatly deceived this people and Jerusalem, saying, Ye shall "
  "have peace, whereas the sword reacheth unto the soul. It can be read as the prophet bitterly "
  "quoting what the peace-prophets have been saying in God's name, and it can be read as an "
  "accusation aimed straight at God. The Hebrew allows both and translators have divided over it for "
  "centuries. The book leaves it standing without a gloss, and a note on it should do the same."),
 ("A Dry Wind, Not to Fan (vv.11-18)",
  "A dry wind of the high places toward the daughter of my people, not to fan, nor to cleanse. The "
  "qualification is the whole image: the wind of a threshing floor separates grain from chaff and is "
  "useful, and this one is the desert sirocco, which only strips. Then the speed of the thing, he "
  "shall come up as clouds, and his chariots as a whirlwind, his horses are swifter than eagles. An "
  "offer is still made in the middle of it, wash thine heart from wickedness, that thou mayest be "
  "saved, and the section closes with the diagnosis, this is thy wickedness, because it is bitter, "
  "because it reacheth unto thine heart."),
 ("My Bowels, My Bowels (vv.19-22)",
  "The prophet's own reaction, and it is reported as a physical symptom rather than as an opinion, my "
  "bowels, my bowels, I am pained at my very heart, my heart maketh a noise in me, I cannot hold my "
  "peace. What set it off is a sound, the sound of the trumpet, the alarm of war. Then the verdict he "
  "is grieving over, and it is not gentle, for my people is foolish, they have not known me, they are "
  "sottish children, and they have none understanding, they are wise to do evil, but to do good they "
  "have no knowledge."),
 ("Creation Reversed (vv.23-26)",
  "Four verses, each beginning I beheld, and each one taking something back out of Genesis 1. I "
  "beheld the earth, and lo, it was without form, and void, which is the phrase from the second verse "
  "of the Bible. And the heavens, and they had no light. The mountains trembled and all the hills "
  "moved lightly. I beheld, and lo, there was no man, and all the birds of the heavens were fled. And "
  "the fruitful place was a wilderness. It is the most sustained un-creation passage in the prophets, "
  "and it works by running the first chapter of scripture backwards."),
 ("Yet Not a Full End (vv.27-31)",
  "The whole land shall be desolate, yet will I not make a full end. That qualification is "
  "characteristic of Jeremiah and it is worth noticing how often it is attached: the sentence is "
  "always severe and almost never final. Then the futility of appearances, though thou clothest "
  "thyself with crimson, though thou deckest thee with ornaments of gold, in vain shalt thou make "
  "thyself fair, thy lovers will despise thee. And the chapter's last image, chosen because it is "
  "both agony and the beginning of something, I have heard a voice as of a woman in travail, the "
  "voice of the daughter of Zion."),
],
"jeremiah5": [
 ("Find One Man (vv.1-6)",
  "Run ye to and fro through the streets of Jerusalem, and see now, and know, and seek in the broad "
  "places thereof, if ye can find a man, if there be any that executeth judgment, that seeketh the "
  "truth, and I will pardon it. Abraham's bargaining over Sodom got down to ten. This gets to one, "
  "and the search fails. The prophet's first move is to excuse them by class, surely these are poor, "
  "they are foolish, for they know not the way of the LORD, so he goes to the great men instead, and "
  "reports that these have altogether broken the yoke, and burst the bonds. The excuse does not "
  "survive the second attempt."),
 ("How Shall I Pardon Thee (vv.7-9)",
  "How shall I pardon thee for this, thy children have forsaken me, and sworn by them that are no "
  "gods. The aggravation named is provision rather than neglect, when I had fed them to the full, "
  "then they committed adultery. And the section ends with the refrain that closes each stage of this "
  "chapter, shall I not visit for these things, saith the LORD, and shall not my soul be avenged on "
  "such a nation as this."),
 ("It Is Not He (vv.10-14)",
  "Go ye up upon her walls, and destroy, but not utterly, which is the same restraint as 4:27. Then "
  "the denial that gives the section its point, quoted in the people's own words, they have belied "
  "the LORD, and said, It is not he, neither shall evil come upon us, neither shall we see sword nor "
  "famine. The prophets who supplied that line get a sentence built on their own trade, the prophets "
  "shall become wind, and the word is not in them. And Jeremiah gets the opposite, behold, I will "
  "make my words in thy mouth fire, and this people wood, and it shall devour them."),
 ("A Nation Whose Language You Do Not Know (vv.15-19)",
  "I will bring a nation upon you from far, a mighty nation, a nation whose language thou knowest "
  "not, neither understandest what they say. The detail about language is the frightening one: not "
  "just an army but an army you cannot negotiate with. Their quiver is as an open sepulchre, and what "
  "they consume is listed as a household inventory, thine harvest, and thy bread, thy flocks and thy "
  "herds, thy vines and thy fig trees. The exile is then explained as an exchange in kind, like as ye "
  "have forsaken me, and served strange gods in your land, so shall ye serve strangers in a land that "
  "is not yours."),
 ("The Sand and the Sea (vv.20-25)",
  "Declare this in the house of Jacob, which have eyes, and see not, which have ears, and hear not. "
  "The argument is from the reliability of the natural order, which have placed the sand for the "
  "bound of the sea by a perpetual decree, that it cannot pass it, and though the waves toss "
  "themselves, yet can they not prevail. Something with no obedience in it keeps its limit. Then the "
  "same argument applied to weather, neither say they in their heart, Let us now fear the LORD our "
  "God, that giveth rain, both the former and the latter, in his season. And the consequence, your "
  "iniquities have turned away these things, and your sins have withholden good things from you."),
 ("A Wonderful Thing in the Land (vv.26-31)",
  "As a cage is full of birds, so are their houses full of deceit, they are waxen fat and shine, they "
  "judge not the cause of the fatherless, yet they prosper. The chapter closes on four clauses that "
  "describe an entire society and then place the blame in an unexpected quarter: the prophets prophesy "
  "falsely, and the priests bear rule by their means, and my people love to have it so, and what will "
  "ye do in the end thereof. The last clause is the only question in the chapter that is not "
  "answered."),
],
"jeremiah6": [
 ("Flee, and the Mount Cast Against the City (vv.1-8)",
  "Blow the trumpet in Tekoa, and set up a sign of fire in Beth-haccerem, for evil appeareth out of "
  "the north. The invaders are then allowed to speak, and what they say is the ordinary shop talk of "
  "a siege, arise, and let us go up at noon, and then, woe unto us, for the day goeth away, arise, "
  "and let us go by night. The engineering follows, hew ye down trees, and cast a mount against "
  "Jerusalem. And in the middle of it a plea that is entirely practical, be thou instructed, O "
  "Jerusalem, lest I make thee desolate, a land not inhabited."),
 ("Glean Thoroughly, and Ears That Cannot Hear (vv.9-12)",
  "They shall thoroughly glean the rest of Israel as a grapegatherer, turn back thine hand as a "
  "grapegatherer into the baskets, which is a picture of a second pass over ground already stripped. "
  "Then the prophet's difficulty stated as a question about audience, to whom shall I speak, and give "
  "warning, that they may hear, behold, their ear is uncircumcised, they cannot hearken, the word of "
  "the LORD is unto them a reproach, they have no delight in it. And his own condition, I am full of "
  "the fury of the LORD, I am weary with holding in."),
 ("Peace, Peace, When There Is No Peace (vv.13-15)",
  "From the least of them even unto the greatest of them, every one is given to covetousness, and "
  "from the prophet even unto the priest, every one dealeth falsely. The charge against the "
  "peace-prophets is put as medical malpractice, they have healed also the hurt of the daughter of my "
  "people slightly, saying, Peace, peace, when there is no peace. A wound closed over without being "
  "cleaned. These three verses appear again almost word for word at 8:11, which is worth noticing "
  "rather than explaining: the same diagnosis is repeated because nothing had changed."),
 ("Ask for the Old Paths (v.16)",
  "One verse, and the best known in the chapter. Thus saith the LORD, Stand ye in the ways, and see, "
  "and ask for the old paths, where is the good way, and walk therein, and ye shall find rest for "
  "your souls. It is quoted on its own often enough that the second half is usually lost, and the "
  "second half is why it sits here, but they said, We will not walk therein. The verse is not an "
  "invitation in this chapter. It is an invitation together with its refusal, recorded in the same "
  "breath."),
 ("Watchmen Set, and Frankincense Refused (vv.17-21)",
  "Also I set watchmen over you, saying, Hearken to the sound of the trumpet, but they said, We will "
  "not hearken, which repeats the previous verse's refusal in a different setting. Then the offerings "
  "dismissed with a question about purpose, to what purpose cometh there to me incense from Sheba, "
  "and the sweet cane from a far country, your burnt offerings are not acceptable. Frankincense from "
  "southern Arabia was among the most costly commodities traded in the ancient world, and naming it "
  "makes the point precisely: expense is not the currency being asked for."),
 ("A People from the North Country (vv.22-26)",
  "Behold, a people cometh from the north country, and the description is of soldiers who cannot be "
  "appealed to, they shall lay hold on bow and spear, they are cruel, and have no mercy, their voice "
  "roareth like the sea. The response commanded is not defence but mourning, O daughter of my people, "
  "gird thee with sackcloth, and wallow thyself in ashes, make thee mourning as for an only son, most "
  "bitter lamentation."),
 ("Reprobate Silver (vv.27-30)",
  "The chapter ends with the prophet described as an assayer rather than a preacher, I have set thee "
  "for a tower and a fortress among my people, that thou mayest know and try their way. The result of "
  "the assay is a complete failure of the process, and every stage of it is named, the bellows are "
  "burned, the lead is consumed of the fire, the founder melteth in vain. Reprobate silver shall men "
  "call them, because the LORD hath rejected them. Reprobate is the technical term for metal that "
  "went through the fire and came out worthless, and the pun on rejected is in the Hebrew as well."),
],
"jeremiah7": [
 ("The Temple Sermon (vv.1-7)",
  "Stand in the gate of the LORD's house, and proclaim there this word. What he says at the door is "
  "an attack on a slogan, trust ye not in lying words, saying, The temple of the LORD, The temple of "
  "the LORD, The temple of the LORD are these. The threefold repetition is the chant being quoted "
  "back. What is offered in its place is a list of things to do, amend your ways and your doings, "
  "execute judgment between a man and his neighbour, oppress not the stranger, the fatherless, and "
  "the widow, and shed not innocent blood, and then will I cause you to dwell in this place. Chapter "
  "26 records what this sermon cost: he was arrested for it and came close to being executed."),
 ("A Den of Robbers (vv.8-11)",
  "Will ye steal, murder, and commit adultery, and swear falsely, and burn incense unto Baal, and "
  "come and stand before me in this house. The building is being described as a place where stolen "
  "goods are safe, is this house, which is called by my name, become a den of robbers in your eyes. "
  "Jesus quotes that clause, joined to Isaiah 56, when he clears the temple courts, which means the "
  "sentence was still doing the same work six centuries later in the same location."),
 ("The Shiloh Precedent (vv.12-15)",
  "But go ye now unto my place which was in Shiloh, where I set my name at the first, and see what I "
  "did to it for the wickedness of my people Israel. Shiloh had housed the tabernacle and the ark "
  "through the whole period of the judges and was destroyed, most likely by the Philistines around "
  "1050 BC. The argument is an argument from precedent and it is hard to answer: a sanctuary God had "
  "put his own name on has already been abandoned once. Therefore will I do unto this house, which is "
  "called by my name, as I have done to Shiloh."),
 ("Pray Not for This People (vv.16-20)",
  "Therefore pray not thou for this people, neither lift up cry nor prayer for them, neither make "
  "intercession to me, for I will not hear thee. It is the sharpest thing said to Jeremiah anywhere "
  "in the book, and it is repeated at 11:14 and 14:11. The office of intercession, which Abraham "
  "exercised over Sodom and Moses over Israel at Sinai, is withdrawn from him. The reason follows as "
  "a domestic scene, which is what makes it land, the children gather wood, and the fathers kindle "
  "the fire, and the women knead their dough, to make cakes to the queen of heaven. A whole household "
  "cooperating on it."),
 ("Obedience Before Burnt Offerings (vv.21-28)",
  "Put your burnt offerings and sacrifices together, and eat them, for I spake not unto your fathers, "
  "nor commanded them in the day that I brought them out of the land of Egypt, concerning burnt "
  "offerings or sacrifices, but this thing commanded I them, saying, Obey my voice. Read flatly that "
  "contradicts Leviticus, and the standard reading is the Hebrew idiom of relative emphasis, where "
  "not this but that means this rather than that, as at Hosea 6:6 and Amos 5:21-25. What follows is "
  "the pattern of the whole history in one sentence, I sent unto you all my servants the prophets, "
  "daily rising up early and sending them, yet they hearkened not unto me."),
 ("Topheth, and the Valley of Slaughter (vv.29-34)",
  "Cut off thine hair, O Jerusalem, and cast it away, and take up a lamentation on high places. Then "
  "the specific practice, they have built the high places of Topheth, which is in the valley of the "
  "son of Hinnom, to burn their sons and their daughters in the fire, with a clause attached that is "
  "as close as this book comes to disowning something entirely, which I commanded them not, neither "
  "came it into my heart. The place is renamed the valley of slaughter, and the graveyard overflows "
  "into it, they shall bury in Topheth, because there is no place. The valley of the son of Hinnom is "
  "ge-hinnom in Hebrew, which becomes Gehenna in the New Testament and the standard word there for "
  "hell. This chapter is where that reputation begins."),
],
"jeremiah8": [
 ("Bones Brought Out of the Graves (vv.1-3)",
  "They shall bring out the bones of the kings of Judah, and the bones of his princes, and the bones "
  "of the priests, and the bones of the prophets, out of their graves. And the reason the bones are "
  "left where they are put is an exact match to the offence, they shall spread them before the sun, "
  "and the moon, and all the host of heaven, whom they have loved, and whom they have served, and "
  "after whom they have walked. People who worshipped the sky are left lying under it unburied, which "
  "in that culture was the worst indignity available. And death shall be chosen rather than life by "
  "all the residue of them that remain."),
 ("The Stork Knows Her Times (vv.4-7)",
  "Shall they fall, and not arise, shall he turn away, and not return. The argument is then made from "
  "birds, and it is made carefully: the stork in the heaven knoweth her appointed times, and the "
  "turtle and the crane and the swallow observe the time of their coming, but my people know not the "
  "judgment of the LORD. Migratory birds keep an appointed schedule with no instruction at all, and "
  "the people who were given the instruction do not. The word appointed is doing the work, because it "
  "is the same word used of the festivals."),
 ("The Lying Pen of the Scribes (vv.8-9)",
  "How do ye say, We are wise, and the law of the LORD is with us, lo, certainly in vain made he it, "
  "the pen of the scribes is in vain. This is the one place in the prophets that turns on scribal "
  "work specifically, and the charge is that possession and copying of the law had become a "
  "substitute for keeping it. The consequence is stated in terms of the wisdom claimed, the wise men "
  "are ashamed, they are dismayed and taken, lo, they have rejected the word of the LORD, and what "
  "wisdom is in them."),
 ("Peace, Peace, Repeated (vv.10-12)",
  "This block is 6:13-15 said again, almost word for word: from the least even unto the greatest "
  "every one is given to covetousness, and they have healed the hurt of the daughter of my people "
  "slightly, saying, Peace, peace, when there is no peace. The repetition is deliberate and should be "
  "read as such rather than treated as an editorial accident. The same sentences come back because "
  "the same wound was still being dressed the same way, and the second time they carry the added "
  "weight of having been said before and ignored."),
 ("No Grapes, and Serpents That Will Not Be Charmed (vv.13-17)",
  "There shall be no grapes on the vine, nor figs on the fig tree, and the leaf shall fade. The "
  "people are then quoted taking cover, why do we sit still, assemble yourselves, and let us enter "
  "into the defenced cities, and quoted again giving their own verdict, we looked for peace, but no "
  "good came, and for a time of health, and behold trouble. The section closes with an image drawn "
  "from a working trade, I will send serpents, cockatrices, among you, which will not be charmed. A "
  "snake a professional cannot handle."),
 ("Is There No Balm in Gilead (vv.18-22)",
  "The prophet speaks for himself again, and the sentence that opens it has become proverbial, the "
  "harvest is past, the summer is ended, and we are not saved. For the hurt of the daughter of my "
  "people am I hurt, I am black, astonishment hath taken hold on me. Then the question the chapter is "
  "known by, is there no balm in Gilead, is there no physician there, why then is not the health of "
  "the daughter of my people recovered. Gilead's balsam was the region's recognised medicinal export, "
  "so this is not a question about supply. The medicine existed and was near at hand. It was not "
  "applied."),
],
"jeremiah9": [
 ("A Fountain of Tears, and a Lodge in the Wilderness (vv.1-2)",
  "Oh that my head were waters, and mine eyes a fountain of tears, that I might weep day and night "
  "for the slain of the daughter of my people. That verse is the reason he is called the weeping "
  "prophet. The verse immediately after it is quoted far less often and belongs with it, oh that I "
  "had in the wilderness a lodging place of wayfaring men, that I might leave my people, and go from "
  "them. Grief for them and the wish to be away from them, in consecutive verses, with neither "
  "cancelling the other. The book records both without apologising for the second."),
 ("Take Heed of Thy Neighbour (vv.3-6)",
  "They bend their tongues like their bow for lies. What is described here is not the collapse of "
  "national religion but the collapse of ordinary trust, and the advice given is correspondingly "
  "bleak, take ye heed every one of his neighbour, and trust ye not in any brother, for every brother "
  "will utterly supplant, and every neighbour will walk with slanders. The verb in the next line is "
  "the one that matters, they have taught their tongues to speak lies, so this is a trained skill and "
  "an inherited one, and weary themselves to commit iniquity."),
 ("I Will Melt Them (vv.7-9)",
  "Behold, I will melt them, and try them, for how shall I do for the daughter of my people. The "
  "middle clause is a question about method, not a threat, and it reads as genuine difficulty. Then "
  "the speech again, their tongue is as an arrow shot out, one speaketh peaceably to his neighbour "
  "with his mouth, but in heart he layeth his wait. And the chapter's refrain, shall I not visit them "
  "for these things."),
 ("A Lamentation for the Pastures (vv.10-11)",
  "For the mountains will I take up a weeping and wailing, and for the habitations of the wilderness "
  "a lamentation, because they are burned up, so that none can pass through them. The loss is "
  "measured by a sound that has stopped, neither can men hear the voice of the cattle, both the fowl "
  "of the heavens and the beast are fled. And the city with them, I will make Jerusalem heaps, and a "
  "den of dragons."),
 ("Why Is the Land Desolate (vv.12-16)",
  "Who is the wise man, that may understand this, and who is he to whom the mouth of the LORD hath "
  "spoken, that he may declare it, for what the land perisheth. The question is asked of the wise and "
  "then answered by God instead, because they have forsaken my law which I set before them, and have "
  "walked after the imagination of their own heart. The sentence uses two bitter substances for what "
  "is normally hospitality, I will feed them with wormwood, and give them water of gall to drink, and "
  "ends with the scattering, I will scatter them also among the heathen."),
 ("Call for the Mourning Women (vv.17-22)",
  "Call for the mourning women, that they may come, and let them make haste, and take up a wailing "
  "for us. Professional mourners were a recognised trade, and sending for them says that the grief "
  "has outrun what a family can produce on its own. The reason is then given in a sentence that makes "
  "the danger domestic, for death is come up into our windows, and is entered into our palaces, to "
  "cut off the children from without, and the young men from the streets. And the closing image is "
  "agricultural and careless, they shall fall as the handful after the harvestman, and none shall "
  "gather them."),
 ("Let Not the Wise Man Glory (vv.23-24)",
  "Let not the wise man glory in his wisdom, neither let the mighty man glory in his might, let not "
  "the rich man glory in his riches. Three of the four things anyone in that world could be proud of "
  "are named and removed, and the fourth is substituted, but let him that glorieth glory in this, "
  "that he understandeth and knoweth me. And what is to be known is specified rather than left "
  "abstract, that I am the LORD which exercise lovingkindness, judgment, and righteousness, in the "
  "earth, for in these things I delight. Paul quotes this passage twice, at 1 Corinthians 1 and "
  "2 Corinthians 10."),
 ("Circumcised and Yet Uncircumcised (vv.25-26)",
  "I will punish all them which are circumcised with the uncircumcised, and then the list, which is "
  "the argument: Egypt, and Judah, and Edom, and the children of Ammon, and Moab, and all that are in "
  "the utmost corners. Judah is placed in a list of neighbouring nations that also practised "
  "circumcision, which shows the mark to be shared and therefore not by itself a distinction. The "
  "conclusion is stated in a sentence that only works because of the paradox in it, for all these "
  "nations are uncircumcised, and all the house of Israel are uncircumcised in the heart."),
],
"jeremiah10": [
 ("Learn Not the Way of the Heathen (vv.1-2)",
  "Learn not the way of the heathen, and be not dismayed at the signs of heaven, for the heathen are "
  "dismayed at them. Babylonian astronomy was the most accurate in the world and its astrology came "
  "with it, so this is specific advice rather than a general warning: people about to be deported to "
  "the culture that produced the omen literature are told not to be frightened of eclipses and "
  "conjunctions."),
 ("The Idol That Has to Be Fastened Down (vv.3-5)",
  "The satire is entirely procedural and works by describing the manufacture in order: one cutteth a "
  "tree out of the forest, the work of the hands of the workman with the axe, they deck it with silver "
  "and with gold, they fasten it with nails and with hammers, that it move not. A god that has to be "
  "nailed in place so it does not fall over. Then the summary, they are upright as the palm tree, but "
  "speak not, they must needs be borne, for they cannot go. And the conclusion drawn is not that "
  "idols are wicked but that they are beside the point, be not afraid of them, for they cannot do "
  "evil, neither also is it in them to do good."),
 ("There Is None Like Thee (vv.6-7)",
  "The satire breaks off into direct address, forasmuch as there is none like unto thee, O LORD, thou "
  "art great, and thy name is great in might, who would not fear thee, O King of nations. The chapter "
  "alternates between mocking the manufactured gods and speaking to God, and the alternation is "
  "itself the argument. The contrast is made by putting the two side by side and letting the reader "
  "hear the change of register, rather than by explaining what the difference is."),
 ("Silver from Tarshish, Gold from Uphaz (vv.8-9)",
  "They are altogether brutish and foolish, the stock is a doctrine of vanities. Then the imports are "
  "itemised with their sources, silver is brought from Tarshish, and gold from Uphaz, the work of the "
  "workman, and of the hands of the founder, blue and purple is their clothing. It makes the same "
  "point as the axe and the nails from the other end: every component of the god arrived on a ship, "
  "was paid for, and was finished by a tradesman."),
 ("The Living God, and the One Verse in Aramaic (vv.10-16)",
  "But the LORD is the true God, he is the living God, and an everlasting king. Verse 11 is the only "
  "verse in the whole book of Jeremiah written in Aramaic rather than Hebrew, and it is addressed "
  "outward, thus shall ye say unto them, The gods that have not made the heavens and the earth, even "
  "they shall perish from the earth. Aramaic was the international language of the region, so the one "
  "sentence the exiles are handed to say to their neighbours is written in the language the "
  "neighbours actually spoke. What follows is a creation doxology, he hath made the earth by his "
  "power, he hath established the world by his wisdom, and it closes on the covenant name, the "
  "portion of Jacob, the LORD of hosts is his name."),
 ("Gather Up Thy Wares (vv.17-18)",
  "Gather up thy wares out of the land, O inhabitant of the fortress, which is the instruction given "
  "to someone with an hour to pack. And the reason, behold, I will sling out the inhabitants of the "
  "land at this once. The verb is the point of the two verses. Not led away, not carried, slung, as "
  "from a sling, which is a picture of being thrown a long distance by someone who is aiming."),
 ("The Shepherds Have Become Brutish (vv.19-22)",
  "The voice here is the city's rather than the prophet's, woe is me for my hurt, my tabernacle is "
  "spoiled, and all my cords are broken, my children are gone forth of me, and are not. Then the "
  "cause is assigned, and it is assigned upward, for the pastors are become brutish, and have not "
  "sought the LORD, therefore they shall not prosper, and all their flocks shall be scattered. The "
  "section ends with the noise of the thing arriving, behold, the noise of the bruit is come, and a "
  "great commotion out of the north country."),
 ("Correct Me, but with Judgment (vv.23-25)",
  "O LORD, I know that the way of man is not in himself, it is not in man that walketh to direct his "
  "steps. Then the request, and it is carefully worded, O LORD, correct me, but with judgment, not in "
  "thine anger, lest thou bring me to nothing. He is not asking to be spared the correction, he is "
  "asking about the measure of it, which is a different prayer and a harder one. The last verse turns "
  "outward, pour out thy fury upon the heathen that know thee not, which Psalm 79 says in almost "
  "identical words."),
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
