#!/usr/bin/env python3
"""
Proverbs 1 to 9, 30 and 31: the chapters that are continuous discourse rather than
collected sayings. Eleven pages.

These are the only Proverbs chapters whose inherited sublists are genuine outlines.
Measured against the text, chapters 1 to 9 and 31 cover every verse with no overlap,
and chapter 30 covers every verse but one. Chapters 10 to 29 are a different thing
entirely, a topical index with scattered and overlapping references, and they are
handled separately.

So the sublists here are folded into prose sections the way Hosea's were: outline
dropped, each item becoming a section written from the text.

Two repairs come with it. proverbs30 leaves v.17 uncovered, the eye that mocks a
father and is picked out by ravens, which sits between two numerical sayings and
belongs to neither, so it gets its own section. proverbs31's two outline items carry
their sub-points inside the same line separated by literal asterisks, which is the
last markdown left in the corpus. Those sub-points become the section divisions rather
than surviving as punctuation.

Usage:
    python3 fold_proverbs_discourses.py [--check]
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

OPS = {
"proverbs1": [
 ("Prologue: Purpose and Motto (vv.1-7)",
  "The book states its own purpose in six verses before saying anything wise, and the list of "
  "aims is broader than instruction: to know wisdom and instruction, to perceive the words of "
  "understanding, to receive the instruction of justice and judgment and equity, to give subtilty "
  "to the simple, to the young man knowledge and discretion. Two audiences are named, the simple "
  "and the young, and then a third that is easy to miss, a wise man will hear, and will increase "
  "learning. Then the motto the whole collection hangs on, the fear of the LORD is the beginning "
  "of knowledge, with its opposite in the same breath, but fools despise wisdom and instruction."),
 ("A Father's Warning Against Sinners (vv.8-19)",
  "The first instruction is about company rather than conduct, my son, if sinners entice thee, "
  "consent thou not. What follows is their invitation quoted at length, and it is quoted because "
  "it is attractive: come with us, let us lay wait for blood, we shall find all precious "
  "substance, cast in thy lot among us, let us all have one purse. The appeal is belonging as much "
  "as profit. The answer is not a moral argument but an observation about outcomes, they lay wait "
  "for their own blood, and the closing line generalises it, so are the ways of every one that is "
  "greedy of gain, which taketh away the life of the owners thereof."),
 ("Wisdom's Public Appeal and Warning (vv.20-33)",
  "Wisdom is personified for the first time and the setting is deliberately public, she crieth in "
  "the streets, in the chief place of concourse, in the openings of the gates. Nothing here is "
  "esoteric. The complaint is about refusal rather than ignorance, how long, ye simple ones, will "
  "ye love simplicity? and the offer is stated plainly, turn you at my reproof, behold, I will "
  "pour out my spirit unto you. Then the consequence, and it is the most chilling passage in the "
  "chapter because it describes a reversal of roles, I also will laugh at your calamity, then "
  "shall they call upon me, but I will not answer. The reason given is that they refused when "
  "asked, they would none of my counsel, therefore shall they eat of the fruit of their own way."),
],
"proverbs2": [
 ("The Conditions for Finding Wisdom (vv.1-4)",
  "Four verses of conditions before any promise, and they are all verbs of effort: receive, hide, "
  "incline, apply, cry, lift up thy voice. The last two images make the point about cost, if thou "
  "seekest her as silver, and searchest for her as for hid treasures. Mining and treasure hunting "
  "are both slow, dirty and uncertain. The chapter opens by refusing to suggest that wisdom "
  "arrives by being told things."),
 ("The Results: Knowing God (vv.5-8)",
  "The promise attached is not information but relationship, then shalt thou understand the fear "
  "of the LORD, and find the knowledge of God. The reason it works is put in the middle, for the "
  "LORD giveth wisdom, out of his mouth cometh knowledge and understanding, so the searching of "
  "the previous verses is answered by a gift rather than by discovery. Then two images of "
  "protection, he layeth up sound wisdom for the righteous, he is a buckler to them that walk "
  "uprightly."),
 ("Wisdom's Protection from Evil Men (vv.9-15)",
  "The first thing wisdom is said to protect against is company, to deliver thee from the way of "
  "the evil man, from the man that speaketh froward things. The description of them is about "
  "pleasure rather than profit, who rejoice to do evil, and delight in the frowardness of the "
  "wicked, which is a harder charge than greed. The closing image is geometric and hard to "
  "improve on, whose ways are crooked, and they froward in their paths."),
 ("Wisdom's Protection from the Adulteress (vv.16-19)",
  "The second protection is from the strange woman, and the specific danger named is her speech, "
  "which flattereth with her words. What is described as broken is not chiefly a marriage but two "
  "commitments, she forsaketh the guide of her youth, and forgetteth the covenant of her God. "
  "Then the closing verse, which is the bleakest sentence in the chapter, none that go unto her "
  "return again, neither take they hold of the paths of life."),
 ("Walking in the Way of the Good (vv.20-22)",
  "The chapter closes by putting both outcomes in terms of land tenure rather than reward: the "
  "upright shall dwell in the land, and the perfect shall remain in it, but the wicked shall be "
  "cut off from the earth, and the transgressors shall be rooted out of it. Staying put is the "
  "blessing. Being uprooted is the judgment, and both are agricultural rather than judicial."),
],
"proverbs3": [
 ("Blessings of Obedience: Life, Peace, Favour (vv.1-10)",
  "Ten verses containing five of the most quoted sentences in the book, and each pairs an "
  "instruction with a promise. Bind mercy and truth about thy neck, and thou shalt find favour. "
  "Trust in the LORD with all thine heart, and lean not unto thine own understanding, in all thy "
  "ways acknowledge him, and he shall direct thy paths. Be not wise in thine own eyes, and it "
  "shall be health to thy navel. And honour the LORD with thy substance, and with the firstfruits "
  "of all thine increase, which attaches the promise of full barns to a specific act of giving "
  "rather than to general piety."),
 ("God's Fatherly Discipline (vv.11-12)",
  "Two verses that reframe hardship as attention rather than rejection, my son, despise not the "
  "chastening of the LORD, neither be weary of his correction, for whom the LORD loveth he "
  "correcteth, even as a father the son in whom he delighteth. The argument is from analogy and "
  "the analogy is uncomfortable, because it makes the correction evidence of the delight. Hebrews "
  "12 quotes these verses and builds a chapter on them."),
 ("The Supreme Value of Wisdom (vv.13-20)",
  "The valuation is made by comparison and every comparison is commercial: better than the "
  "merchandise of silver, than fine gold, more precious than rubies, and all the things thou "
  "canst desire are not to be compared unto her. Then the images turn from price to what she "
  "holds, length of days in her right hand, riches and honour in her left. The famous line about "
  "manner rather than content follows, her ways are ways of pleasantness, and all her paths are "
  "peace, and then the tree of life, which is the first time Proverbs reaches back to Eden. The "
  "section closes on creation, the LORD by wisdom hath founded the earth."),
 ("Security Through Wisdom (vv.21-26)",
  "The promises here are all about the ordinary hours when nothing is happening. Then shalt thou "
  "walk safely, and thy foot shall not stumble. When thou liest down, thou shalt not be afraid, "
  "yea, thou shalt lie down, and thy sleep shall be sweet. Sleep is an unusual thing to promise "
  "and a precise one, because it is what fear takes away first. The reason given is presence "
  "rather than circumstance, for the LORD shall be thy confidence, and shall keep thy foot from "
  "being taken."),
 ("Duties Toward Neighbours (vv.27-35)",
  "The chapter ends with wisdom applied to the man next door, and the instructions are specific "
  "and mostly negative. Withhold not good from them to whom it is due, when it is in thine hand "
  "to do it. Say not unto thy neighbour, Go, and come again, and tomorrow I will give, which is a "
  "prohibition on delay rather than on refusal. Devise not evil against thy neighbour, seeing he "
  "dwelleth securely by thee, where the reason is his trust. Strive not without cause. Envy not "
  "the oppressor, choose none of his ways. And the closing pair of verdicts, the LORD scorneth the "
  "scorners, but he giveth grace unto the lowly."),
],
"proverbs4": [
 ("Three Generations of Wisdom (vv.1-9)",
  "The father teaching here says he was taught, and quotes his own father doing it: for I was my "
  "father's son, tender and only beloved in the sight of my mother, he taught me also, and said "
  "unto me, Let thine heart retain my words. Wisdom is presented as inherited instruction passed "
  "down three generations rather than as insight. The urgency is in the verbs, get wisdom, get "
  "understanding, forget it not, forsake her not, love her, exalt her, embrace her, and the "
  "closing promise is a coronation, she shall give to thine head an ornament of grace, a crown of "
  "glory shall she deliver to thee."),
 ("The Two Paths Contrasted (vv.10-19)",
  "The image is a road and the instruction is about which one to be on, enter not into the path of "
  "the wicked, avoid it, pass not by it, turn from it, and pass away. Four commands to do the same "
  "thing, which suggests the pull is real. The description of the other party is memorable for "
  "being about appetite, for they sleep not, except they have done mischief, and their sleep is "
  "taken away, unless they cause some to fall. They eat the bread of wickedness. Then the two "
  "closing images, and both are about visibility: the path of the just is as the shining light, "
  "that shineth more and more unto the perfect day, and the way of the wicked is as darkness, they "
  "know not at what they stumble."),
 ("Guard Your Heart and Walk Straight (vv.20-27)",
  "The last section works through the body part by part, and the order puts the heart first for a "
  "stated reason, keep thy heart with all diligence, for out of it are the issues of life. Then "
  "the mouth, put away from thee a froward mouth, and perverse lips put far from thee. Then the "
  "eyes, let thine eyes look right on, and let thine eyelids look straight before thee. Then the "
  "feet, ponder the path of thy feet, and let all thy ways be established, turn not to the right "
  "hand nor to the left. An anatomy of attention, working outward from the one organ nobody else "
  "can see."),
],
"proverbs5": [
 ("The Adulteress's Deception (vv.1-6)",
  "The warning is entirely about the gap between how something sounds and where it goes. Her lips "
  "drop as an honeycomb, and her mouth is smoother than oil, and then the reversal in the next "
  "verse, but her end is bitter as wormwood, sharp as a two-edged sword. The chapter is careful "
  "to say the deception is not chiefly a lie she tells, it is her own condition, she knoweth not "
  "the plain path, her ways are moveable, thou canst not know them."),
 ("Stay Far from Her (vv.7-14)",
  "The command is spatial and admits no negotiation, remove thy way far from her, and come not "
  "nigh the door of her house. Then the costs are itemised, and they are almost all social rather "
  "than moral: thine honour given unto others, thy years unto the cruel, thy labours in the house "
  "of a stranger. The closing lines are a speech put in the mouth of a man who did not listen, and "
  "the regret is about instruction rather than pleasure, how have I hated instruction, and my "
  "heart despised reproof, and have not obeyed the voice of my teachers. He says it in public, in "
  "the midst of the congregation and assembly."),
 ("Rejoice in Your Wife (vv.15-20)",
  "The alternative offered is not restraint but pleasure elsewhere, and the imagery is water in a "
  "dry country, drink waters out of thine own cistern, and running waters out of thine own well. "
  "The instruction is unembarrassed, let thy fountain be blessed, and rejoice with the wife of thy "
  "youth, and be thou ravished always with her love. Then the question that closes the section, "
  "and why wilt thou, my son, be ravished with a strange woman? The argument against adultery here "
  "is that it is a worse deal."),
 ("God Sees Everything (vv.21-23)",
  "Three verses that move the whole matter out of the realm of discretion, for the ways of man are "
  "before the eyes of the LORD, and he pondereth all his goings. Then the mechanism of ruin, and "
  "it is self-inflicted rather than imposed, he is holden with the cords of his sins. The chapter "
  "ends on the reason rather than the punishment, he shall die without instruction, and in the "
  "greatness of his folly he shall go astray."),
],
"proverbs6": [
 ("Warning Against Foolish Pledges (vv.1-5)",
  "Standing surety for a neighbour's debt is treated as an emergency to be escaped rather than a "
  "kindness to be honoured, and the urgency is in the verbs, deliver thyself, give not sleep to "
  "thine eyes, nor slumber to thine eyelids. Two animal images make the case, deliver thyself as a "
  "roe from the hand of the hunter, and as a bird from the hand of the fowler. The chapter offers "
  "no theology for it, only that the man has put himself in someone else's hand."),
 ("The Ant and the Sluggard (vv.6-11)",
  "Go to the ant, thou sluggard, consider her ways, and be wise. The argument is about "
  "self-direction rather than industry, which having no guide, overseer, or ruler, provideth her "
  "meat in the summer. Then the sluggard's own voice, yet a little sleep, a little slumber, a "
  "little folding of the hands to sleep, which is the most sympathetic line in the passage because "
  "it is exactly what anyone would say. The ending is abrupt on purpose, so shall thy poverty come "
  "as one that travelleth, and thy want as an armed man."),
 ("The Worthless Troublemaker (vv.12-15)",
  "The portrait is built entirely out of body language, and that is the point: he speaketh with "
  "his feet, he teacheth with his fingers, he winketh with his eyes. Nothing is said about what he "
  "says. The diagnosis is placed where nobody can see it, frowardness is in his heart, he deviseth "
  "mischief continually, he soweth discord, and the outcome is sudden and without warning, "
  "therefore shall his calamity come suddenly, suddenly shall he be broken without remedy."),
 ("Seven Things the LORD Hates (vv.16-19)",
  "A numerical saying, six things doth the LORD hate, yea, seven are an abomination unto him, and "
  "the list works through the body again: a proud look, a lying tongue, hands that shed innocent "
  "blood, a heart that deviseth wicked imaginations, feet that be swift in running to mischief, a "
  "false witness. The seventh is given the emphatic position and is the only one that is not a "
  "body part, and it names a result rather than an organ, he that soweth discord among brethren."),
 ("Warning Against Adultery (vv.20-35)",
  "The longest section in the chapter and the argument is economic before it is moral. A prostitute "
  "costs a piece of bread. Adultery costs everything, and the reason is the husband: jealousy is "
  "the rage of a man, therefore he will not spare in the day of vengeance, he will not regard any "
  "ransom, neither will he rest content, though thou givest many gifts. Two images make the "
  "impossibility physical, can a man take fire in his bosom, and his clothes not be burned? can "
  "one go upon hot coals, and his feet not be burned? The comparison with theft is deliberate: a "
  "thief who steals from hunger is despised but understood, and restitution is possible. Here it "
  "is not."),
],
"proverbs7": [
 ("Treasure Wisdom as Protection (vv.1-5)",
  "The instruction is to hold wisdom close enough that it functions as family, say unto wisdom, "
  "Thou art my sister, and call understanding thy kinswoman. The physical images are deliberately "
  "intimate, keep my commandments as the apple of thine eye, bind them upon thy fingers, write "
  "them upon the table of thine heart. And the stated purpose is defensive, that they may keep "
  "thee from the strange woman, from the stranger which flattereth with her words."),
 ("The Seduction Witnessed (vv.6-23)",
  "Eighteen verses of narrative, which is the longest continuous story in Proverbs, and it is told "
  "from a window: at the window of my house I looked through my casement, and beheld among the "
  "simple ones a young man void of understanding. The detail is unhurried and specific. It is "
  "twilight, in the evening, in the black and dark night. Her dress is noted, the attire of an "
  "harlot, and so is her manner, subtil of heart, loud and stubborn, now is she without, now in "
  "the streets, and lieth in wait at every corner. Her speech is quoted at length and it is "
  "religious in part, I have peace offerings with me, this day have I payed my vows, and practical "
  "in part, the goodman is not at home, he is gone a long journey. The closing images are all of "
  "animals that do not understand what is happening, he goeth as an ox to the slaughter, as a bird "
  "hasteth to the snare, and knoweth not that it is for his life."),
 ("Warning and Death Toll (vv.24-27)",
  "The narrator steps back out of the story and addresses the room, hearken unto me now therefore, "
  "O ye children, and the instruction is again about proximity rather than resistance, let not "
  "thine heart decline to her ways, go not astray in her paths. Then the arithmetic that ends the "
  "chapter, for she hath cast down many wounded, yea, many strong men have been slain by her. Her "
  "house is the way to hell, going down to the chambers of death. The young man of verse 7 is "
  "revealed as one of a series."),
],
"proverbs8": [
 ("Wisdom's Public Call (vv.1-11)",
  "Wisdom takes her stand in the places where business is done, in the top of high places, by the "
  "way in the places of the paths, at the gates, at the entry of the city. The audience she names "
  "is everybody, unto you, O men, I call, and my voice is to the sons of man. What she claims for "
  "her speech is straightforwardness rather than depth, there is nothing froward or perverse in "
  "them, they are all plain to him that understandeth. And the valuation is the same as chapter 3, "
  "receive my instruction, and not silver, for wisdom is better than rubies."),
 ("Wisdom's Nature and Gifts (vv.12-21)",
  "Wisdom describes her own company, I dwell with prudence, and I find out knowledge of witty "
  "inventions, and then what she is against, and the list is specific, pride, and arrogancy, and "
  "the evil way, and the froward mouth, do I hate. The claim that follows is political, by me "
  "kings reign, and princes decree justice, which puts wisdom underneath government rather than "
  "beside it. Then the terms of access, I love them that love me, and those that seek me early "
  "shall find me, and the reward described as durable riches and righteousness."),
 ("Wisdom's Origin and Role in Creation (vv.22-31)",
  "The most discussed passage in the book, and it is Wisdom speaking about her own age: the LORD "
  "possessed me in the beginning of his way, before his works of old. Then a run of clauses "
  "describing what did not yet exist, before the mountains were settled, before the hills, while "
  "as yet he had not made the earth, when there were no depths, when there were no fountains "
  "abounding with water. The verbs of the section are about presence rather than agency, when he "
  "prepared the heavens, I was there, when he set a compass upon the face of the depth. And the "
  "closing self-description is the surprise, then I was by him, as one brought up with him, and I "
  "was daily his delight, rejoicing always before him, rejoicing in the habitable part of his "
  "earth, and my delights were with the sons of men. Wisdom at the creation is described as "
  "playing."),
 ("Wisdom's Final Appeal (vv.32-36)",
  "The appeal is put in terms of attention, blessed is the man that heareth me, watching daily at "
  "my gates, waiting at the posts of my doors, which is the posture of a servant rather than a "
  "student. Then the stakes are raised as high as the chapter can take them, for whoso findeth me "
  "findeth life, and shall obtain favour of the LORD. And the closing verse states the alternative "
  "as self-harm rather than punishment, he that sinneth against me wrongeth his own soul, and all "
  "they that hate me love death."),
],
"proverbs9": [
 ("Lady Wisdom's Banquet (vv.1-6)",
  "Wisdom builds a house with seven pillars, kills her beasts, mingles her wine, furnishes her "
  "table, and then sends out invitations by servants, which is a considerable amount of "
  "preparation before anyone is asked. The invitation itself is shouted from the highest places of "
  "the city and is addressed to the least promising audience available, whoso is simple, let him "
  "turn in hither. The terms are two imperatives, come, eat of my bread, and drink of the wine "
  "which I have mingled, and one condition, forsake the foolish, and live."),
 ("The Wise and the Scoffer (vv.7-12)",
  "Six verses on who can be corrected, and the advice is unexpectedly practical, reprove not a "
  "scorner, lest he hate thee, rebuke a wise man, and he will love thee. The distinction is not "
  "intelligence but response, give instruction to a wise man, and he will be yet wiser. Then the "
  "book's motto restated with an addition, the fear of the LORD is the beginning of wisdom, and "
  "the knowledge of the holy is understanding. And a closing sentence that puts the whole matter "
  "back on the reader, if thou be wise, thou shalt be wise for thyself, but if thou scornest, thou "
  "alone shalt bear it."),
 ("Lady Folly's Banquet (vv.13-18)",
  "The mirror image, and the parallels are exact enough to be deliberate. Folly also has a house, "
  "also sits at the high places of the city, also calls to passengers, and uses the same words, "
  "whoso is simple, let him turn in hither. The differences are two. Her fare is stolen rather "
  "than prepared, stolen waters are sweet, and bread eaten in secret is pleasant. And she does not "
  "mention what the guests already are, but he knoweth not that the dead are there, and that her "
  "guests are in the depths of hell. The first nine chapters end with two invitations that sound "
  "identical and one detail the diner is not told."),
],
"proverbs30": [
 ("Agur's Confession of Ignorance (vv.1-4)",
  "The chapter changes author and the new one opens by disqualifying himself, surely I am more "
  "brutish than any man, and have not the understanding of a man. That is an odd thing to find in "
  "a wisdom book, and the questions that follow explain it: who hath gathered the wind in his "
  "fists? who hath bound the waters in a garment? who hath established all the ends of the earth? "
  "what is his name, and what is his son's name, if thou canst tell? A collection of answers is "
  "interrupted by a man listing what nobody knows."),
 ("The Sufficiency and Purity of Scripture (vv.5-6)",
  "Two verses that follow the confession directly and answer it. Every word of God is pure, he is "
  "a shield unto them that put their trust in him. If the previous section says human "
  "understanding cannot reach, this one says something else has come down. The instruction "
  "attached is about restraint, add thou not unto his words, lest he reprove thee, and thou be "
  "found a liar."),
 ("The Prayer for Contentment (vv.7-9)",
  "The only prayer in Proverbs, and it asks for two things and then explains both. Remove far from "
  "me vanity and lies, and give me neither poverty nor riches, feed me with food convenient for "
  "me. The reasons are symmetrical and both are about God rather than comfort: lest I be full, and "
  "deny thee, and say, Who is the LORD? or lest I be poor, and steal, and take the name of my God "
  "in vain. A request to be kept in the middle, on the grounds that either end is a spiritual "
  "risk."),
 ("Warnings Against Wickedness (vv.10-14)",
  "A short run of sayings about accusation and arrogance, beginning with an instruction not to "
  "inform on a servant to his master, lest he curse thee, and thou be found guilty. Then a "
  "generation described in four parallel verses, and the charges escalate: cursing father and "
  "mother, pure in their own eyes, lofty of eyelid, and finally a generation whose teeth are as "
  "swords, to devour the poor from off the earth, and the needy from among men."),
 ("Things Never Satisfied (vv.15-16)",
  "The first of the numerical sayings, and the form is a riddle rather than a lesson. The "
  "horseleach hath two daughters, crying, Give, give. Then four things that say not, It is enough: "
  "the grave, the barren womb, the earth that is not filled with water, and the fire. The list is "
  "not moral. It is an observation about appetite that has no bottom, and the reader is left to "
  "apply it."),
 ("The Eye That Mocks a Father (v.17)",
  "One verse standing between two numerical sayings and belonging to neither. The eye that mocketh "
  "at his father, and despiseth to obey his mother, the ravens of the valley shall pick it out, "
  "and the young eagles shall eat it. The punishment is aimed at the organ that did the mocking, "
  "and the picture is of a body left unburied in open country, which for the ancient reader is the "
  "worst end available. It is the harshest verse in the chapter and it is about contempt at home."),
 ("Things Too Wonderful (vv.18-19)",
  "Four things which I know not: the way of an eagle in the air, the way of a serpent upon a rock, "
  "the way of a ship in the midst of the sea, and the way of a man with a maid. Each of the first "
  "three leaves no track, which is what holds the list together, and the fourth is placed last so "
  "that the reader supplies the connection. The saying admires rather than explains."),
 ("The Adulterous Woman (v.20)",
  "A single verse appended to the previous saying and reading as a sour comment on it. Such is the "
  "way of an adulterous woman, she eateth, and wipeth her mouth, and saith, I have done no "
  "wickedness. The image is deliberately domestic and casual, and what it describes is not "
  "pleasure but the absence of any sense that anything happened."),
 ("Things the Earth Cannot Bear (vv.21-23)",
  "Four for which the earth is disquieted, and all four are inversions of status rather than "
  "crimes: a servant when he reigneth, a fool when he is filled with meat, an odious woman when "
  "she is married, and an handmaid that is heir to her mistress. The saying is about social order "
  "under strain and it does not pretend to be kind. It records what the writer thought "
  "insupportable."),
 ("The Four Small but Wise Creatures (vv.24-28)",
  "Four things which are little upon the earth, but they are exceeding wise, and each is credited "
  "with a competence that outruns its size. The ants are a people not strong, yet they prepare "
  "their meat in the summer. The conies are but a feeble folk, yet make they their houses in the "
  "rocks. The locusts have no king, yet go they forth all of them by bands. And the spider taketh "
  "hold with her hands, and is in kings' palaces. Preparation, shelter, organisation without "
  "leadership, and access to places above her station."),
 ("Things Stately in Going (vv.29-31)",
  "Three things which go well, yea, four are comely in going: a lion which is strongest among "
  "beasts and turneth not away for any, a greyhound, a he goat, and a king against whom there is "
  "no rising up. The saying is purely about bearing, and it is the only one in the chapter that "
  "admires something without qualifying it."),
 ("Final Warning Against Pride (vv.32-33)",
  "The chapter ends with an instruction that is physical, if thou hast thought evil, lay thine "
  "hand upon thy mouth. Then a proverb about process, and the three clauses run in parallel: "
  "surely the churning of milk bringeth forth butter, and the wringing of the nose bringeth forth "
  "blood, so the forcing of wrath bringeth forth strife. Each is a thing produced by pressure, and "
  "the third is offered as the same mechanism as the first two."),
],
"proverbs31": [
 ("A Mother's Oracle to a King (vv.1-2)",
  "The last chapter is attributed to a woman, the words of king Lemuel, the prophecy that his "
  "mother taught him, and it opens with the sound of somebody who has been waiting to speak: what, "
  "my son? and what, the son of my womb? and what, the son of my vows? Three times the "
  "relationship is named before any instruction is given, and the third names a vow, which "
  "suggests the child was asked for."),
 ("Give Not Thy Strength Unto Women (v.3)",
  "One verse, and the warning is put in terms of expenditure rather than morality, give not thy "
  "strength unto women, nor thy ways to that which destroyeth kings. The phrase that which "
  "destroyeth kings is doing the work: this is advice to a ruler about what has historically "
  "ended reigns, not general counsel about appetite."),
 ("It Is Not for Kings to Drink Wine (vv.4-7)",
  "The prohibition is occupational rather than absolute, and the reason is given plainly, lest "
  "they drink, and forget the law, and pervert the judgment of any of the afflicted. A judge who "
  "has been drinking is the specific danger. Then the verses that have made this passage awkward "
  "for temperance readers ever since: give strong drink unto him that is ready to perish, and wine "
  "unto those that be of heavy hearts, let him drink, and forget his poverty, and remember his "
  "misery no more. Wine is taken away from the man with power and offered to the man with nothing."),
 ("Plead the Cause of the Dumb (vv.8-9)",
  "The oracle ends in two verses of instruction that read as the point of the whole speech: open "
  "thy mouth for the dumb, in the cause of all such as are appointed to destruction, open thy "
  "mouth, judge righteously, and plead the cause of the poor and needy. The mouth that was told to "
  "refuse wine in the previous verses is told what to do instead. A mother's advice to a king "
  "reduces to advocacy for people who cannot speak for themselves."),
 ("Her Worth and Her Husband's Trust (vv.10-12)",
  "The poem that closes Proverbs is an acrostic, one verse for each of the twenty-two letters of "
  "the Hebrew alphabet, which is why it moves between topics without transitions. It opens with a "
  "question about scarcity, who can find a virtuous woman? for her price is far above rubies, and "
  "the phrase used of her is eshet chayil, where chayil is a military word for strength or "
  "capability. The husband's position is described in terms of confidence rather than authority, "
  "the heart of her husband doth safely trust in her, so that he shall have no need of spoil."),
 ("Her Industry and Enterprise (vv.13-19,24)",
  "The longest strand of the poem, and what it describes is a business. She seeketh wool and flax, "
  "she is like the merchants' ships, she riseth while it is yet night and giveth meat to her "
  "household. Then a transaction in her own name, she considereth a field, and buyeth it, with the "
  "profits of her hands she planteth a vineyard. Her arms are described as strong, she layeth her "
  "hands to the spindle, and the later verse in the same strand records her selling, she maketh "
  "fine linen and girdles, and delivereth them to the merchant. Nothing here is domestic in the "
  "sense of being confined to a house."),
 ("Her Generosity (v.20)",
  "One verse placed in the middle of the account of her trading, and the placing is the argument. "
  "She stretcheth out her hand to the poor, yea, she reacheth forth her hands to the needy. The "
  "same hands that hold the spindle and take the profit are described reaching outward, and the "
  "poem does not treat the two as separate virtues."),
 ("Her Preparation and Dignity (vv.21-23,25)",
  "Provision described as foresight rather than wealth, she is not afraid of the snow for her "
  "household, for all her household are clothed with scarlet. Then her own clothing, coverings of "
  "tapestry, silk and purple, which the poem states without apology. Her husband's standing in the "
  "gate is credited to her in the same strand. And the summary verse, strength and honour are her "
  "clothing, and she shall rejoice in time to come, which describes her wardrobe twice, once in "
  "fabric and once in character."),
 ("Her Wisdom and Kindness (vv.26-27)",
  "Two verses about speech and oversight. She openeth her mouth with wisdom, and in her tongue is "
  "the law of kindness, which is the only place in the poem she is described as teaching. Then she "
  "looketh well to the ways of her household, and eateth not the bread of idleness. The book that "
  "opened with a father's instruction ends by describing a woman whose speech carries law."),
 ("Her Praise and the Fear of the LORD (vv.28-31)",
  "The praise comes from inside the house first, her children arise up, and call her blessed, her "
  "husband also, and he praiseth her, and his words are quoted, many daughters have done "
  "virtuously, but thou excellest them all. Then the verse that reaches back to the motto of "
  "chapter 1 and closes the book on it, favour is deceitful, and beauty is vain, but a woman that "
  "feareth the LORD, she shall be praised. The last instruction is public rather than private, "
  "give her of the fruit of her hands, and let her own works praise her in the gates, which is the "
  "same city gate where wisdom was crying in chapter 1."),
],
}


def verify(planned):
    """Apply the audit's checks to the planned HTML without writing it.

    The working tree belongs to another session, so write-then-audit is unavailable.
    Running the same rules against the strings in memory is what makes --check mean
    anything here.
    """
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
            found.append(f"{page}: described twice {sorted({v for v, _ in repeated})}")
        if starts != sorted(starts):
            found.append(f"{page}: sections out of verse order")
        if "<li>" in pane:
            found.append(f"{page}: sublist survived the fold")
        if "*" in pane:
            found.append(f"{page}: markdown asterisk left in pane")
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label) if w not in A.CAPS_OK})
            if stray and A.TAIL.search(label):
                found.append(f"{page}: capitals {stray} in {label!r}")
    return found


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, sections in OPS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        keep = []
        for label, body in ITEM_RE.findall(pane.group(2)):
            if H.unescape(label).strip() in ("Author:", "Historical Context:"):
                keep.append([label, body.strip()])
        if len(keep) != 2:
            problems.append(f"{page}: expected Author and Historical Context, "
                            f"found {len(keep)}")
            continue
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
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
          f"{len(notes)} section(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
