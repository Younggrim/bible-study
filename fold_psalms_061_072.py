#!/usr/bin/env python3
"""
Psalms 61 to 72. Twelve pages, 201 verses. All twelve outlines are gapless and are folded.

This block closes Book II of the psalter. psalms72 ends with the doxology that marks the
division, and with a colophon, the prayers of David the son of Jesse are ended, which is an
editorial note rather than part of the psalm. The section says so, because a reader who
takes it as the poem's last line will read it as a claim about authorship that the rest of
the psalter contradicts.

psalms70 is Psalm 40:13-17 repeated almost word for word, and psalms67 carries a refrain at
verses 3 and 5. Both are handled the way the earlier duplicates and refrains were: the
repetition is named rather than smoothed over.

Usage:
    python3 fold_psalms_061_072.py [--check]
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
KEEP = ("Author:", "Date:", "Attributed Author:", "Classification:", "Key Themes:",
        "Historical Context:")
REPAIRS = {}

SECTIONS = {
"psalms61": [
 ("From the End of the Earth (vv.1-2)",
  "Hear my cry, O God, attend unto my prayer. The location given is deliberately vague and deliberately "
  "far, from the end of the earth will I cry unto thee, when my heart is overwhelmed. And the petition "
  "that follows admits it needs help to get anywhere, lead me to the rock that is higher than I."),
 ("A Shelter and a Strong Tower (vv.3-4)",
  "For thou hast been a shelter for me, and a strong tower from the enemy. The claim is made in the "
  "perfect tense, so the confidence rests on a record. Then two images side by side, one architectural and "
  "one avian, I will abide in thy tabernacle for ever, I will trust in the covert of thy wings, which is "
  "the same pairing as Psalm 27:5."),
 ("The Heritage of Them That Fear Thy Name (v.5)",
  "For thou, O God, hast heard my vows, thou hast given me the heritage of those that fear thy name. One "
  "verse, and the word heritage is the land-allotment term Psalm 16:6 uses, so what is claimed is a "
  "portion held in common with others rather than a private answer."),
 ("Thou Wilt Prolong the King's Life (vv.6-7)",
  "Thou wilt prolong the king's life, and his years as many generations. The switch to the third person is "
  "why many read the psalm as a royal one prayed on the king's behalf, and the request is for something "
  "longer than a lifetime. He shall abide before God for ever, O prepare mercy and truth, which may "
  "preserve him."),
 ("So Will I Sing Praise (v.8)",
  "So will I sing praise unto thy name for ever, that I may daily perform my vows. One verse, and it pairs "
  "for ever with daily, which is the psalm's way of making a large promise practical: the perpetual praise "
  "is to be delivered in instalments."),
],
"psalms62": [
 ("My Soul Waiteth upon God (vv.1-2)",
  "Truly my soul waiteth upon God, from him cometh my salvation. The Hebrew word behind waiteth carries "
  "silence in it, so what is described is a deliberate quiet rather than patience. Then the titles, he only "
  "is my rock and my salvation, he is my defence, I shall not be greatly moved, and the qualifier greatly "
  "is honest rather than triumphant."),
 ("How Long Will Ye Imagine Mischief (vv.3-4)",
  "How long will ye imagine mischief against a man, ye shall be slain all of you, as a bowing wall shall "
  "ye be, and as a tottering fence. The images are of structures about to fall. And the charge against them "
  "is the gap between speech and intent, they bless with their mouth, but they curse inwardly."),
 ("He Only Is My Rock (vv.5-7)",
  "My soul, wait thou only upon God, for my expectation is from him. The psalm turns and addresses itself, "
  "as Psalm 42 does, and then repeats the titles of verse 2 with one change: I shall not be moved, without "
  "the greatly. Between the two statements the opponents have been described, and the confidence has gone "
  "up rather than down."),
 ("Pour Out Your Heart Before Him (v.8)",
  "Trust in him at all times, ye people, pour out your heart before him, God is a refuge for us. One verse, "
  "addressed outward to a congregation rather than upward, and the instruction to pour out the heart is the "
  "psalter's plainest invitation to pray badly if necessary."),
 ("Men of Low Degree Are Vanity (vv.9-10)",
  "Surely men of low degree are vanity, and men of high degree are a lie, when laid in the balance, they "
  "are altogether lighter than vanity. Both ends of the social scale are weighed and both come up light. "
  "Then the practical warning, trust not in oppression, and become not vain in robbery, if riches increase, "
  "set not your heart upon them, which concedes that the riches may in fact increase."),
 ("Power Belongeth unto God (vv.11-12)",
  "God hath spoken once, twice have I heard this, that power belongeth unto God. The formula is a wisdom "
  "device for emphasis, and what is heard is put in two halves that the psalm holds together, power and "
  "mercy, also unto thee, O Lord, belongeth mercy. And the closing clause is the one Paul quotes in "
  "Romans 2:6, for thou renderest to every man according to his work."),
],
"psalms63": [
 ("My Soul Thirsteth for Thee (vv.1-2)",
  "O God, thou art my God, early will I seek thee. The superscription places the psalm in the wilderness of "
  "Judah, and the imagery matches, my soul thirsteth for thee, my flesh longeth for thee, in a dry and "
  "thirsty land, where no water is. Then what is missed is named and it is not water, to see thy power and "
  "thy glory, so as I have seen thee in the sanctuary."),
 ("Thy Lovingkindness Is Better Than Life (vv.3-5)",
  "Because thy lovingkindness is better than life, my lips shall praise thee. It is the strongest "
  "comparative in the psalter and it is made by a man in a desert, which is what gives it weight. Then the "
  "imagery turns from thirst to a meal, my soul shall be satisfied as with marrow and fatness, which were "
  "the richest parts of an animal and were normally the portion burned on the altar."),
 ("In the Night Watches (vv.6-8)",
  "When I remember thee upon my bed, and meditate on thee in the night watches. The night watches are the "
  "divisions the sentries kept, so the psalm is describing wakeful hours put to a use. Then the wings again, "
  "in the shadow of thy wings will I rejoice. And the last verse pairs two verbs that describe the same "
  "act from both sides, my soul followeth hard after thee, thy right hand upholdeth me."),
 ("They Shall Go into the Lower Parts of the Earth (vv.9-10)",
  "But those that seek my soul, to destroy it, shall go into the lower parts of the earth. Two verses of "
  "reversal, and the fate described is battlefield exposure, they shall fall by the sword, they shall be a "
  "portion for foxes, which for that culture was the worst end available because it left no burial."),
 ("The King Shall Rejoice in God (v.11)",
  "But the king shall rejoice in God, every one that sweareth by him shall glory. The switch to the third "
  "person at the end is the same move as Psalm 61:6 and is why both are read as royal. And the psalm ends "
  "on the mouths it began with, the mouth of them that speak lies shall be stopped."),
],
"psalms64": [
 ("Hear My Voice, O God (vv.1-2)",
  "Hear my voice, O God, in my prayer, preserve my life from fear of the enemy. What is asked for is "
  "protection from the fear as much as from the man. And the danger is described as organised, hide me from "
  "the secret counsel of the wicked, from the insurrection of the workers of iniquity."),
 ("They Whet Their Tongue Like a Sword (vv.3-6)",
  "Who whet their tongue like a sword, and bend their bows to shoot their arrows, even bitter words. The "
  "weapons named turn out on inspection to be speech, which is the psalm's method throughout. Then the "
  "confidence of the plotters is quoted, they say, Who shall see them. And the last verse credits their "
  "effort, they search out iniquities, they accomplish a diligent search, so the psalm concedes they are "
  "working hard."),
 ("God Shall Shoot at Them (vv.7-8)",
  "But God shall shoot at them with an arrow, suddenly shall they be wounded. The reply uses the weapon of "
  "verse 3 and the word suddenly answers their diligent search: the effort was long and the answer is "
  "quick. And the reversal is complete in the next clause, their own tongue shall fall upon themselves."),
 ("All Men Shall Fear (vv.9-10)",
  "And all men shall fear, and shall declare the work of God. The outcome is public understanding rather "
  "than the singer's relief, which is where several of these psalms land. And the last verse is a general "
  "invitation, the righteous shall be glad in the LORD, and shall trust in him, and all the upright in "
  "heart shall glory."),
],
"psalms65": [
 ("Praise Waiteth for Thee in Zion (vv.1-2)",
  "Praise waiteth for thee, O God, in Sion, and unto thee shall the vow be performed. The psalm opens at "
  "the temple with obligations being discharged. And the second verse gives the reason anyone comes at all, "
  "O thou that hearest prayer, unto thee shall all flesh come, which widens the congregation past Israel "
  "in the psalm's second sentence."),
 ("Iniquities Prevail Against Me (v.3)",
  "Iniquities prevail against me, as for our transgressions, thou shalt purge them away. One verse, and it "
  "moves from the singular to the plural inside itself, so a personal admission becomes a national one. "
  "The verb purge is the atonement word of Leviticus."),
 ("Blessed Is the Man Whom Thou Choosest (v.4)",
  "Blessed is the man whom thou choosest, and causest to approach unto thee, that he may dwell in thy "
  "courts. One verse, and the two verbs are both God's: chosen and caused to approach. What follows is "
  "satisfaction rather than status, we shall be satisfied with the goodness of thy house."),
 ("By Terrible Things Wilt Thou Answer Us (vv.5-8)",
  "By terrible things in righteousness wilt thou answer us, O God of our salvation. The answer is described "
  "as awe-inspiring rather than gentle, and the reach of the confidence is stated geographically, who art "
  "the confidence of all the ends of the earth, and of them that are afar off upon the sea. Then the sea "
  "and the nations are handled with one verb, which stilleth the noise of the seas, and the tumult of the "
  "people, which is the same pairing as Psalm 46."),
 ("Thou Visitest the Earth (vv.9-13)",
  "Thou visitest the earth, and waterest it, thou greatly enrichest it with the river of God. The last "
  "five verses are the finest agricultural writing in the psalter and they follow a growing season in "
  "order: the furrows watered, the ridges settled, the showers, the increase blessed. Then the image the "
  "psalm is remembered for, thou crownest the year with thy goodness, and thy paths drop fatness. And the "
  "closing verse gives the fields a voice, the pastures are clothed with flocks, the valleys also are "
  "covered over with corn, they shout for joy, they also sing."),
],
"psalms66": [
 ("Make a Joyful Noise unto God (vv.1-4)",
  "Make a joyful noise unto God, all ye lands. The address is to everybody, and what is asked for is volume "
  "before content, sing forth the honour of his name, make his praise glorious. Then a note about the "
  "quality of some of the praise being offered, through the greatness of thy power shall thine enemies "
  "submit themselves unto thee, where the verb suggests feigned or cringing submission."),
 ("He Turned the Sea into Dry Land (vv.5-7)",
  "Come and see the works of God, he is terrible in his doings toward the children of men. The example "
  "cited is the exodus and it is put in the first person plural although it happened centuries earlier, he "
  "turned the sea into dry land, they went through the flood on foot, there did we rejoice in him. The "
  "congregation places itself at the crossing."),
 ("Thou Hast Tried Us, as Silver Is Tried (vv.8-12)",
  "Bless our God, ye people, and make the voice of his praise to be heard. Then a passage that assigns the "
  "recent trouble to God without complaint, for thou, O God, hast proved us, thou hast tried us, as silver "
  "is tried. The images are of livestock and of traffic, thou laidst affliction upon our loins, thou hast "
  "caused men to ride over our heads, we went through fire and through water. And the destination is stated "
  "in three words that make the whole psalm a thanksgiving, but thou broughtest us out into a wealthy "
  "place."),
 ("I Will Pay Thee My Vows (vv.13-15)",
  "I will go into thy house with burnt offerings, I will pay thee my vows, which my lips have uttered, and "
  "my mouth hath spoken, when I was in trouble. The vows are described as made under pressure and paid "
  "afterwards, which is the ordinary honest sequence. And the offering listed is extravagant, burnt "
  "sacrifices of fatlings, with the incense of rams, bullocks with goats."),
 ("Come and Hear, All Ye That Fear God (vv.16-20)",
  "Come and hear, all ye that fear God, and I will declare what he hath done for my soul. The psalm turns "
  "from national to personal in its last section, which is the reverse of the usual direction. Then a "
  "condition stated with unusual candour, if I regard iniquity in my heart, the Lord will not hear me. And "
  "the closing verse is the psalm's whole argument in one line, blessed be God, which hath not turned away "
  "my prayer, nor his mercy from me."),
],
"psalms67": [
 ("God Be Merciful unto Us (vv.1-2)",
  "God be merciful unto us, and bless us, and cause his face to shine upon us. The wording borrows the "
  "priestly blessing of Numbers 6:24-26, and then does something with it the blessing does not: it attaches "
  "a purpose clause, that thy way may be known upon earth, thy saving health among all nations. The "
  "blessing is asked for in order to be visible to somebody else."),
 ("The First Refrain (v.3)",
  "Let the people praise thee, O God, let all the people praise thee. The refrain appears twice, here and "
  "at verse 5, and it divides a seven-verse psalm into three parts. What it asks for is not Israel's praise "
  "but everyone's, which is the psalm's single subject."),
 ("Let the Nations Be Glad (v.4)",
  "O let the nations be glad and sing for joy, for thou shalt judge the people righteously, and govern the "
  "nations upon earth. One verse, and the reason given for the gladness is judgment, which is the psalter's "
  "consistent position: reliable government is good news to those who have not had any."),
 ("The Second Refrain (v.5)",
  "Let the people praise thee, O God, let all the people praise thee. The refrain unchanged, closing the "
  "middle section, and its repetition is what makes the psalm's structure symmetrical around verse 4."),
 ("Then Shall the Earth Yield Her Increase (vv.6-7)",
  "Then shall the earth yield her increase, and God, even our own God, shall bless us. The harvest is "
  "mentioned only at the end and only briefly, which suggests the psalm was sung at a festival without "
  "being about one. And the closing verse repeats the purpose of verse 2, God shall bless us, that all the "
  "ends of the earth may fear him, so the psalm ends where it began: the blessing is for export."),
],
"psalms68": [
 ("Let God Arise (vv.1-6)",
  "Let God arise, let his enemies be scattered. The opening line is the formula spoken when the ark set out "
  "in Numbers 10:35, so the psalm begins as a marching song. Then a turn nobody would predict from that "
  "opening: after the smoke and the melting wax, God is described as a father of the fatherless, and a "
  "judge of the widows, God setteth the solitary in families, he bringeth out those which are bound. The "
  "same verse names the alternative, but the rebellious dwell in a dry land."),
 ("Thou, O God, Didst Send a Plentiful Rain (vv.7-14)",
  "O God, when thou wentest forth before thy people, when thou didst march through the wilderness. The "
  "history is recited as weather and geology, the earth shook, the heavens also dropped at the presence of "
  "God, and Sinai is named. Then the detail that has puzzled every commentator, a company of women "
  "announcing victory, the Lord gave the word, great was the company of those that published it, and an "
  "image of a dove with silver wings whose sense is not recoverable."),
 ("The Hill of Bashan (vv.15-18)",
  "The hill of God is as the hill of Bashan, an high hill as the hill of Bashan. Then a question put to the "
  "larger mountains, why leap ye, ye high hills, this is the hill which God desireth to dwell in. Zion is "
  "not an impressive mountain and the psalm makes the choice of it the point. And verse 18 is the one Paul "
  "quotes in Ephesians 4:8, thou hast ascended on high, thou hast led captivity captive, thou hast received "
  "gifts for men, where Paul's version has gave gifts rather than received them, following a reading the "
  "Targum also has."),
 ("Who Daily Loadeth Us with Benefits (vv.19-23)",
  "Blessed be the Lord, who daily loadeth us with benefits, even the God of our salvation. Then a sentence "
  "about death that is unusually direct for the psalter, unto God the Lord belong the issues from death. "
  "And the section closes with battlefield imagery that is not softened, that thy foot may be dipped in the "
  "blood of thine enemies."),
 ("The Singers Went Before (vv.24-27)",
  "They have seen thy goings, O God, the goings of my God, my King, in the sanctuary. What is described is "
  "a procession and the order of march is given, the singers went before, the players on instruments "
  "followed after, among them were the damsels playing with timbrels. Then the tribes are named as they "
  "pass, little Benjamin, the princes of Judah, Zebulun and Naphtali, which puts the smallest tribe at the "
  "head of the column."),
 ("Ascribe Ye Strength unto God (vv.28-35)",
  "Thy God hath commanded thy strength, strengthen thou that which thou hast wrought for us. The horizon "
  "widens to the nations bringing tribute, princes shall come out of Egypt, Ethiopia shall soon stretch out "
  "her hands unto God, a verse Acts 8 has often been read against. And the psalm closes on a paradox it "
  "does not resolve, O God, thou art terrible out of thy holy places, and then, he giveth strength and "
  "power unto his people."),
],
"psalms69": [
 ("Save Me, O God, for the Waters Are Come In (vv.1-4)",
  "Save me, O God, for the waters are come in unto my soul. The distress is described as drowning in mud "
  "rather than in water, I sink in deep mire, where there is no standing, which is the same figure Psalm "
  "40:2 uses of the rescue. Then the arithmetic of the opposition, they that hate me without a cause are "
  "more than the hairs of mine head, and John 15:25 quotes the phrase without a cause of Jesus."),
 ("My Sins Are Not Hid from Thee (vv.5-6)",
  "O God, thou knowest my foolishness, and my sins are not hid from thee. The admission sits oddly with the "
  "claim of innocence in verse 4, and the psalm makes no attempt to reconcile them. What follows is a "
  "concern for other people rather than for himself, let not them that wait on thee be ashamed for my sake."),
 ("The Zeal of Thine House Hath Eaten Me Up (vv.7-12)",
  "Because for thy sake I have borne reproach, shame hath covered my face. Then the two verses the Gospels "
  "use: I am become a stranger unto my brethren, which John 7:5 echoes of Jesus' own family, and the zeal "
  "of thine house hath eaten me up, which John 2:17 quotes when he clears the temple. And the reach of the "
  "mockery is stated at the end, I was the song of the drunkards."),
 ("Hear Me, O LORD, for Thy Mercy Is Good (vv.13-18)",
  "But as for me, my prayer is unto thee, O LORD, in an acceptable time. The petition returns to the water "
  "and mud of the opening, deliver me out of the mire, and let me not sink, let not the waterflood overflow "
  "me. And the reason offered is God's disposition rather than the singer's case, hear me, O LORD, for thy "
  "lovingkindness is good."),
 ("Reproach Hath Broken My Heart (vv.19-21)",
  "Reproach hath broken mine heart, and I am full of heaviness. Then the loneliness stated as a failed "
  "search, I looked for some to take pity, but there was none, and for comforters, but I found none. And "
  "verse 21 is the one all four Gospels stand behind at the crucifixion, they gave me also gall for my "
  "meat, and in my thirst they gave me vinegar to drink."),
 ("Let Their Table Become a Snare (vv.22-28)",
  "Let their table become a snare before them. This is the longest imprecation in the psalter and it asks "
  "for blindness, a bowed back, desolate houses and a name struck out of the book of the living. Paul "
  "quotes verses 22 and 23 in Romans 11:9-10 of Israel's hardening, and Acts 1:20 uses verse 25 of Judas, "
  "let their habitation be desolate. The psalter records the prayer as it was prayed and does not gloss it."),
 ("I Will Praise the Name of God with a Song (vv.29-36)",
  "But I am poor and sorrowful, let thy salvation, O God, set me up on high. The turn comes with nothing "
  "having changed, and what is promised is song rather than sacrifice, which the next verse makes explicit, "
  "this also shall please the LORD better than an ox or bullock. Then the audience widens to the humble and "
  "the imprisoned, and the psalm ends at the scale of a nation, for God will save Zion, and will build the "
  "cities of Judah, which suggests the poem was taken into use after the exile."),
],
"psalms70": [
 ("Make Haste, O God (v.1)",
  "Make haste, O God, to deliver me, make haste to help me, O LORD. This psalm is Psalm 40:13-17 repeated "
  "with small changes, chiefly the substitution of God for the LORD, which is characteristic of Book II. "
  "The psalter keeps both and the duplication is deliberate rather than accidental, since the shorter "
  "version has its own superscription marking it as a separate liturgical piece."),
 ("Let Them Be Ashamed (vv.2-3)",
  "Let them be ashamed and confounded that seek after my soul. What is asked is reversal rather than "
  "destruction, let them be turned backward. And the quoted taunt is a single syllable of satisfaction, "
  "let them be turned back for a reward of their shame that say, Aha, aha, which is the same word Psalm "
  "35:21 and Ezekiel 25:3 report."),
 ("Let God Be Magnified (v.4)",
  "Let all those that seek thee rejoice and be glad in thee, and let such as love thy salvation say "
  "continually, Let God be magnified. One verse set against the previous two: the same verb, let them say, "
  "with a different sentence in the mouth."),
 ("I Am Poor and Needy (v.5)",
  "But I am poor and needy, make haste unto me, O God, thou art my help and my deliverer, O LORD, make no "
  "tarrying. The psalm ends where it began, asking for speed, and the five verses contain no report of an "
  "answer. It is the shortest complete lament in the psalter and it is left open."),
],
"psalms71": [
 ("In Thee, O LORD, Do I Put My Trust (vv.1-4)",
  "In thee, O LORD, do I put my trust, let me never be put to confusion. The opening borrows from Psalm "
  "31:1-3 almost word for word, and this psalm is assembled from phrases found elsewhere in the psalter "
  "more than any other, which suits a poem about a long life of praying. And the petition is for a place "
  "to go, be thou my strong habitation, whereunto I may continually resort."),
 ("Thou Art My Trust from My Youth (vv.5-8)",
  "For thou art my hope, O Lord GOD, thou art my trust from my youth. The claim reaches back as far as it "
  "can, by thee have I been holden up from the womb, thou art he that took me out of my mother's bowels, "
  "which is the same argument Psalm 22:9 makes. And the result of a long record is stated as a habit, my "
  "praise shall be continually of thee."),
 ("Cast Me Not Off in the Time of Old Age (vv.9-13)",
  "Cast me not off in the time of old age, forsake me not when my strength faileth. This is the only psalm "
  "in the psalter whose subject is being old, and the specific fear is that the record of verses 5 to 8 "
  "will not carry him through the last stretch. Then the opponents are quoted taking the failing strength "
  "as evidence, God hath forsaken him, persecute and take him, for there is none to deliver him."),
 ("I Will Go in the Strength of the Lord GOD (vv.14-16)",
  "But I will hope continually, and will yet praise thee more and more. The response to declining strength "
  "is an increase in praise rather than a reduction. Then an admission that the praise has outrun his "
  "capacity to organise it, I know not the numbers thereof, which is a rare thing for a psalm to concede."),
 ("Now Also When I Am Old (vv.17-21)",
  "O God, thou hast taught me from my youth, and hitherto have I declared thy wondrous works. Then the "
  "petition the psalm exists for, and its motive is not comfort but transmission, now also when I am old "
  "and greyheaded, O God, forsake me not, until I have shewed thy strength unto this generation. He wants "
  "to live long enough to finish telling the next lot. And the psalm's boldest claim follows, thou shalt "
  "quicken me again, and shalt bring me up again from the depths of the earth."),
 ("My Tongue Shall Talk of Thy Righteousness (vv.22-24)",
  "I will also praise thee with the psaltery, O my God, unto thee will I sing with the harp. The old man "
  "ends with instruments, which after fifteen verses about failing strength is the psalm's quiet answer to "
  "itself. And the last verse reports the opposition of verses 10 to 13 as finished, for they are "
  "confounded, for they are brought unto shame, that seek my hurt."),
],
"psalms72": [
 ("Give the King Thy Judgments (vv.1-4)",
  "Give the king thy judgments, O God, and thy righteousness unto the king's son. The psalm is a prayer for "
  "a reign and what it asks for first is a judiciary rather than an army. Then who the government is "
  "measured by, and it is not the powerful, he shall judge thy people with righteousness, and thy poor with "
  "judgment. And the first thing he is asked to do is stated twice, he shall judge the poor of the people, "
  "he shall save the children of the needy, and shall break in pieces the oppressor."),
 ("He Shall Have Dominion from Sea to Sea (vv.5-11)",
  "They shall fear thee as long as the sun and moon endure, throughout all generations. The imagery for "
  "the reign is rainfall rather than conquest, he shall come down like rain upon the mown grass, as showers "
  "that water the earth. Then the extent, and he shall have dominion also from sea to sea, and from the "
  "river unto the ends of the earth, with the nations named as bringing tribute, the kings of Tarshish and "
  "of the isles, the kings of Sheba and Seba shall offer gifts. Matthew 2 has often been read against these "
  "verses."),
 ("He Shall Deliver the Needy (vv.12-14)",
  "For he shall deliver the needy when he crieth, the poor also, and him that hath no helper. The reason "
  "for the dominion of the previous section is given here and it is the poor, which is why the section "
  "belongs on its own: the empire is justified by the welfare. And the valuation is stated plainly, "
  "precious shall their blood be in his sight."),
 ("His Name Shall Endure for Ever (vv.15-17)",
  "And he shall live, and to him shall be given of the gold of Sheba. Then an agricultural promise on a "
  "scale that is deliberately improbable, there shall be an handful of corn in the earth upon the top of "
  "the mountains, the fruit thereof shall shake like Lebanon. And the last verse returns to Genesis 12:3, "
  "men shall be blessed in him, all nations shall call him blessed, which is why this psalm has always been "
  "read past Solomon."),
 ("The Doxology and the Colophon (vv.18-20)",
  "Blessed be the LORD God of Israel, who only doeth wondrous things, and blessed be his glorious name for "
  "ever, let the whole earth be filled with his glory, Amen, and Amen. That is the doxology closing Book II "
  "of the psalter, matching 41:13 at the end of Book I. Then verse 20, and it is not part of the psalm at "
  "all, the prayers of David the son of Jesse are ended. It is an editorial colophon marking the end of a "
  "collection, and it is worth knowing what it is: taken as the poem's last line it reads as a claim about "
  "authorship, and psalms attributed to David appear again at 86, 101, 103 and throughout Book V, so the "
  "note marks the close of one gathering rather than the end of his contributions."),
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
        if len(set(labels)) != len(labels):
            dup = sorted({l for l in labels if labels.count(l) > 1})
            found.append(f"{page}: duplicate label(s) {dup}")
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
                notes.append(f"{page}: dropped inherited item {label!r}")
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
