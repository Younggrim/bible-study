#!/usr/bin/env python3
"""
Psalms 49 to 60. Twelve pages, 171 verses.

Eleven of the twelve outlines fold as they stand. psalms49 has no sublist, so its sections
are written from scratch and divided at the psalm's own joints: the summons, the two
observations about wealth, and the refrain, which appears at verses 12 and 20 in slightly
different form and gives the poem its shape.

psalms53 is Psalm 14 again with small variations, and psalms70 will be part of Psalm 40.
The psalter preserves duplicates rather than tidying them, and where a psalm is a second
version of another the section says so, because a reader who notices the repetition should
not be left wondering whether the page has made a mistake.

Psalms 51 to 60 carry the fullest set of historical superscriptions in the psalter, tying
them to named episodes in 1 and 2 Samuel. The sections use them where they explain the
poem and do not press them where the connection is loose.

Usage:
    python3 fold_psalms_049_060.py [--check]
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
"psalms49": [
 ("Hear This, All Ye People (vv.1-4)",
  "Hear this, all ye people, give ear, all ye inhabitants of the world. The address is universal and the "
  "psalm identifies itself as wisdom rather than prayer, my mouth shall speak of wisdom, and the "
  "meditation of my heart shall be of understanding. Then a clause that treats the poem as a puzzle to be "
  "worked at, I will incline mine ear to a parable, I will open my dark saying upon the harp. Nothing is "
  "addressed to God anywhere in this psalm; it is addressed to everybody else."),
 ("They That Trust in Their Wealth (vv.5-9)",
  "Wherefore should I fear in the days of evil. The question is answered by an observation about what money "
  "cannot buy, and it is put as a transaction that fails, none of them can by any means redeem his brother, "
  "nor give to God a ransom for him. Then the reason the price cannot be met, for the redemption of their "
  "soul is precious, and it ceaseth for ever. The wealthy are not being condemned here for cruelty but "
  "measured against one specific purchase they cannot make."),
 ("Their Inward Thought (vv.10-14)",
  "For he seeth that wise men die, likewise the fool and the brutish person perish. The psalm's argument is "
  "from a fact anyone can check. Then what the rich actually believe is quoted as an inner assumption, "
  "their inward thought is, that their houses shall continue for ever, and it is met with the practice of "
  "the age, they call their lands after their own names. Naming an estate after yourself is offered as "
  "evidence of the thought. And the last image is agricultural and bleak, like sheep they are laid in the "
  "grave, death shall feed on them."),
 ("God Will Redeem My Soul (v.15)",
  "One verse, and it is the psalm's answer to itself. But God will redeem my soul from the power of the "
  "grave, for he shall receive me. What the rich man could not purchase at any price in verse 7 is here "
  "described as given. The verb receive is the one used of Enoch being taken in Genesis 5:24, and the psalm "
  "does not develop the thought further."),
 ("Be Not Thou Afraid When One Is Made Rich (vv.16-20)",
  "Be not thou afraid when one is made rich, when the glory of his house is increased. The instruction is "
  "the practical conclusion, and the reason is given in a sentence that has become proverbial, for when he "
  "dieth he shall carry nothing away, his glory shall not descend after him. Then the self-congratulation "
  "quoted once more, though while he lived he blessed his soul. And the psalm closes on its refrain in "
  "sharper form than at verse 12, man that is in honour, and understandeth not, is like the beasts that "
  "perish. The fault named at the end is not wealth but not understanding."),
],
"psalms50": [
 ("The Mighty God Hath Spoken (vv.1-6)",
  "The mighty God, even the LORD, hath spoken, and called the earth, from the rising of the sun unto the "
  "going down thereof. The psalm opens as a court being convened and the imagery is Sinai, our God shall "
  "come, and shall not keep silence, a fire shall devour before him. Then the summons, gather my saints "
  "together unto me, those that have made a covenant with me by sacrifice, so the defendants are the "
  "faithful rather than the pagans. And the heavens are called as witnesses, which is how Deuteronomy 32 "
  "and Isaiah 1 both open."),
 ("I Will Take No Bullock out of Thy House (vv.7-15)",
  "Hear, O my people, and I will testify against thee. The charge is not neglect of the sacrifices, and the "
  "psalm says so plainly, I will not reprove thee for thy sacrifices or thy burnt offerings, to have been "
  "continually before me. What is disputed is what they were thought to accomplish, and the argument is "
  "put as a question about supply, for every beast of the forest is mine, and the cattle upon a thousand "
  "hills. If I were hungry, I would not tell thee. Then what is asked instead, offer unto God thanksgiving, "
  "and pay thy vows unto the most High, and call upon me in the day of trouble."),
 ("Thou Hatest Instruction (vv.16-21)",
  "But unto the wicked God saith, What hast thou to do to declare my statutes. The second address is to "
  "people inside the covenant community who recite it and live otherwise, thou castest my words behind "
  "thee. The charges are specific and social, consenting with a thief, partnership with adulterers, and "
  "then family, thou speakest against thy brother, thou slanderest thine own mother's son. And the reason "
  "for the delay is stated as a misreading, these things hast thou done, and I kept silence, thou "
  "thoughtest that I was altogether such an one as thyself."),
 ("Whoso Offereth Praise Glorifieth Me (vv.22-23)",
  "Now consider this, ye that forget God, lest I tear you in pieces, and there be none to deliver. Then the "
  "psalm's conclusion, and it puts the two halves of its argument together, whoso offereth praise "
  "glorifieth me, and to him that ordereth his conversation aright will I shew the salvation of God. Praise "
  "and conduct, named as one requirement."),
],
"psalms51": [
 ("Have Mercy upon Me, O God (vv.1-6)",
  "Have mercy upon me, O God, according to thy lovingkindness. The superscription puts this psalm after "
  "Nathan came to him, when he had gone in to Bath-sheba, which is 2 Samuel 12. Three words for sin and "
  "three for its removal appear in the first two verses, blot out, wash me, cleanse me. Then the "
  "confession is put in a form that has troubled readers, against thee, thee only, have I sinned, in a "
  "case that had two other victims, and the point being made is about who defines the offence rather than "
  "who suffered it. Paul quotes verse 4 in Romans 3:4."),
 ("Purge Me with Hyssop (vv.7-9)",
  "Purge me with hyssop, and I shall be clean, wash me, and I shall be whiter than snow. Hyssop was the "
  "sprinkling implement of the purification rituals of Leviticus 14 and Numbers 19, so the request borrows "
  "a priestly procedure. Then a petition about hearing rather than about guilt, make me to hear joy and "
  "gladness, that the bones which thou hast broken may rejoice. And the last verse asks God to look away, "
  "hide thy face from my sins, which is the reverse of the request most psalms make."),
 ("Create in Me a Clean Heart (vv.10-12)",
  "Create in me a clean heart, O God, and renew a right spirit within me. The verb create is the one used "
  "in Genesis 1:1, reserved in Hebrew for what only God does, so what is asked for is not repair. Then the "
  "petition that reads differently after 1 Samuel 16:14, cast me not away from thy presence, and take not "
  "thy holy spirit from me: David had watched exactly that happen to Saul. And the request is for the "
  "return of something specific, restore unto me the joy of thy salvation."),
 ("The Sacrifices of God Are a Broken Spirit (vv.13-17)",
  "Then will I teach transgressors thy ways, and sinners shall be converted unto thee. The intended use of "
  "the forgiveness is instruction, which is a striking thing to promise in the middle of a confession. "
  "Then the psalm's most quoted claim, for thou desirest not sacrifice, else would I give it, thou "
  "delightest not in burnt offering, which for adultery and murder was true in a legal sense as well: the "
  "law provided no sacrifice for either. And what is offered instead, the sacrifices of God are a broken "
  "spirit, a broken and a contrite heart, O God, thou wilt not despise."),
 ("Build Thou the Walls of Jerusalem (vv.18-19)",
  "Do good in thy good pleasure unto Zion, build thou the walls of Jerusalem. The two closing verses widen "
  "from one man to a city and appear to assume walls that need building, which has led many to read them "
  "as added when the psalm entered congregational use after the exile. And they end by putting the "
  "sacrifices back, then shall they offer bullocks upon thine altar, which sits in tension with verse 16 "
  "and is left standing."),
],
"psalms52": [
 ("Why Boastest Thou Thyself (vv.1-4)",
  "Why boastest thou thyself in mischief, O mighty man. The superscription attaches the psalm to Doeg the "
  "Edomite's report to Saul, which led to the massacre of the priests at Nob in 1 Samuel 22, and the "
  "offence in the psalm is speech throughout: thy tongue deviseth mischiefs, like a sharp razor, thou "
  "lovest evil more than good, thou lovest all devouring words."),
 ("God Shall Destroy Thee (v.5)",
  "One verse of sentence, and its verbs come in a sequence of removal, God shall likewise destroy thee for "
  "ever, he shall take thee away, and pluck thee out of thy dwelling place, and root thee out of the land "
  "of the living. Four actions, each more final than the last, ending with the same word Jeremiah's "
  "commission uses for what God does to nations."),
 ("The Righteous Also Shall See (vv.6-7)",
  "The righteous also shall see, and fear, and shall laugh at him. The reaction is described in three "
  "verbs and the middle one is the interesting one: they are frightened before they are amused. And what "
  "they say is quoted as a summary of the whole psalm, lo, this is the man that made not God his strength, "
  "but trusted in the abundance of his riches."),
 ("I Am Like a Green Olive Tree (vv.8-9)",
  "But I am like a green olive tree in the house of God. The contrast is with the man rooted out of the "
  "land of the living in verse 5: an olive is the slowest-growing and longest-lived tree a household owned, "
  "and it is planted rather than plucked. And the psalm ends on waiting rather than on triumph, I will "
  "wait on thy name, for it is good before thy saints."),
],
"psalms53": [
 ("The Fool Hath Said in His Heart (v.1)",
  "This psalm is Psalm 14 again, with small variations, and the psalter keeps both rather than choosing. "
  "The most visible difference is the divine name: Psalm 14 uses the LORD and this one uses God "
  "throughout, which is a feature of the whole of Book II. The fool hath said in his heart, There is no "
  "God, and the word is nabal, a moral rather than an intellectual failure."),
 ("God Looked Down from Heaven (vv.2-3)",
  "God looked down from heaven upon the children of men, to see if there were any that did understand, "
  "that did seek God. The survey and its result are as total here as in Psalm 14, every one of them is "
  "gone back, they are altogether become filthy, there is none that doeth good, no, not one. Paul quotes "
  "the passage in Romans 3."),
 ("Have the Workers of Iniquity No Knowledge (v.4)",
  "Have the workers of iniquity no knowledge, who eat up my people as they eat bread. The comparison with "
  "bread describes the oppression as routine rather than exceptional, and the last clause names what is "
  "not happening, they have not called upon God."),
 ("There Were They in Great Fear (v.5)",
  "There were they in great fear, where no fear was. This is where the two psalms differ most: Psalm 14:5 "
  "has the same opening and then goes a different way, while this version adds a picture of scattered "
  "bones, for God hath scattered the bones of him that encampeth against thee. The military language has "
  "led many to think this version was adapted for a particular battle."),
 ("Oh That the Salvation of Israel (v.6)",
  "Oh that the salvation of Israel were come out of Zion. The closing verse is Psalm 14:7 with God for the "
  "LORD, and it turns a poem about universal corruption into a request for one nation's rescue, when God "
  "bringeth back the captivity of his people, Jacob shall rejoice, and Israel shall be glad."),
],
"psalms54": [
 ("Save Me, O God, by Thy Name (vv.1-2)",
  "Save me, O God, by thy name, and judge me by thy strength. The superscription places the psalm when the "
  "Ziphims came and said to Saul, Doth not David hide himself with us, which is 1 Samuel 23, so the "
  "betrayal is by people of his own tribe's territory. And the petition is for hearing before anything "
  "else, hear my prayer, O God, give ear to the words of my mouth."),
 ("Strangers Are Risen Up Against Me (v.3)",
  "For strangers are risen up against me, and oppressors seek after my soul, they have not set God before "
  "them. One verse, and the word strangers is the difficulty in it: the Ziphites were Judeans, so either "
  "the term is being used of conduct rather than nationality or the psalm has a different occasion than "
  "the superscription supposes. The last clause is the same diagnosis as Psalm 10:4."),
 ("God Is Mine Helper (vv.4-5)",
  "Behold, God is mine helper, the Lord is with them that uphold my soul. The turn comes early in this "
  "psalm, at the halfway point of seven verses, and it is stated as an observation rather than a hope. "
  "Then the request against the enemies is brief and rests on God's character rather than on their deserts, "
  "cut them off in thy truth."),
 ("I Will Praise Thy Name (vv.6-7)",
  "I will freely sacrifice unto thee, I will praise thy name, O LORD, for it is good. The word freely is "
  "the technical term for a freewill offering, one nobody was required to bring. And the psalm ends in the "
  "perfect tense although the danger of verse 3 has not been described as lifting, for he hath delivered "
  "me out of all trouble, which is the psalter's habitual way of speaking about an answer before it "
  "arrives."),
],
"psalms55": [
 ("Give Ear to My Prayer (vv.1-3)",
  "Give ear to my prayer, O God, and hide not thyself from my supplication. The state described is "
  "agitation rather than danger, I mourn in my complaint, and make a noise, and the cause is given as "
  "pressure from two directions, because of the voice of the enemy, because of the oppression of the "
  "wicked."),
 ("Oh That I Had Wings Like a Dove (vv.4-8)",
  "My heart is sore pained within me, and the terrors of death are fallen upon me. Then the psalm's most "
  "human sentence, and it is a wish to be somewhere else, oh that I had wings like a dove, for then would "
  "I fly away, and be at rest. What he would do with the wings is stated plainly, lo, then would I wander "
  "far off, and remain in the wilderness. Escape rather than victory, and the psalter records the wish "
  "without correcting it."),
 ("I Have Seen Violence and Strife in the City (vv.9-11)",
  "Destroy, O Lord, and divide their tongues, for I have seen violence and strife in the city. The request "
  "for divided speech is the Babel remedy applied to a conspiracy. Then the city is described as patrolled "
  "by what has gone wrong in it, day and night they go about it upon the walls, mischief also and sorrow "
  "are in the midst of it, so the trouble is on the walls where the watchmen should be."),
 ("It Was Not an Enemy (vv.12-14)",
  "For it was not an enemy that reproached me, then I could have borne it. The distinction is the point of "
  "the psalm: an enemy would have been manageable. But it was thou, a man mine equal, my guide, and mine "
  "acquaintance. And the intimacy is specified in the detail that makes it worst, we took sweet counsel "
  "together, and walked unto the house of God in company. They had gone to worship together."),
 ("Let Death Seize upon Them (v.15)",
  "One verse of imprecation, and it is unrestrained, let death seize upon them, and let them go down quick "
  "into hell, for wickedness is in their dwellings. The psalter places it immediately after the "
  "recollection of walking to the temple with the man, and does not soften either verse on account of the "
  "other."),
 ("Evening, and Morning, and at Noon (vv.16-19)",
  "As for me, I will call upon God, and the LORD shall save me. Then the schedule, evening, and morning, "
  "and at noon, will I pray, and cry aloud, which is the earliest indication in scripture of prayer three "
  "times a day, the practice Daniel 6:10 records him keeping. And the confidence is stated as something "
  "already received, he hath delivered my soul in peace from the battle that was against me."),
 ("He Hath Broken His Covenant (vv.20-21)",
  "He hath put forth his hands against such as be at peace with him, he hath broken his covenant. The "
  "betrayer of verses 12 to 14 is described again, and the description turns entirely on the gap between "
  "manner and intent, his words were smoother than oil, yet were they drawn swords."),
 ("Cast Thy Burden upon the LORD (vv.22-23)",
  "Cast thy burden upon the LORD, and he shall sustain thee, he shall never suffer the righteous to be "
  "moved. The instruction is addressed outward to a reader rather than upward, which is how several of "
  "these psalms end, and 1 Peter 5:7 takes up the same idea. And the last clause returns to the singer's "
  "own position with nothing resolved except his intention, but I will trust in thee."),
],
"psalms56": [
 ("Be Merciful unto Me, O God (vv.1-2)",
  "Be merciful unto me, O God, for man would swallow me up. The superscription places the psalm when the "
  "Philistines took him in Gath, which is the episode of 1 Samuel 21 where David feigned madness to "
  "escape. And the pressure is described as constant rather than acute, mine enemies would daily swallow "
  "me up, he fighting daily oppresseth me."),
 ("In God I Will Praise His Word (vv.3-4)",
  "What time I am afraid, I will trust in thee. The verse concedes the fear and does not treat it as a "
  "failure, which is why it is quoted more than anything else in the psalm. Then the refrain, in God I "
  "will praise his word, in God I have put my trust, I will not fear what flesh can do unto me, and the "
  "word flesh is doing the work: the threat is real and is bounded by mortality."),
 ("They Mark My Steps (vv.5-7)",
  "Every day they wrest my words, all their thoughts are against me for evil. The surveillance is described "
  "in hunting terms, they mark my steps, when they wait for my soul. And the petition against them is "
  "brief and uses the exile as its measure, in thine anger cast down the people."),
 ("Put My Tears into Thy Bottle (v.8)",
  "Thou tellest my wanderings, put thou my tears into thy bottle, are they not in thy book. One verse, and "
  "it is the most tender image in the psalter. Tellest means counts, and what is being asked for is that "
  "the tears be collected and kept rather than that the trouble be removed. Three records are named in one "
  "verse: a tally of journeys, a container, and a book."),
 ("God Is For Me (vv.9-11)",
  "When I cry unto thee, then shall mine enemies turn back, this I know, for God is for me. The clause "
  "this I know is the psalm's turning point and Paul's argument in Romans 8:31 rests on the same claim. "
  "Then the refrain of verse 4 repeated almost exactly, in God have I put my trust, I will not be afraid "
  "what man can do unto me, with flesh replaced by man."),
 ("I Will Walk Before God (vv.12-13)",
  "Thy vows are upon me, O God, I will render praises unto thee. The obligation is described as already "
  "incurred. And the reason given is stated as a completed rescue, for thou hast delivered my soul from "
  "death, wilt thou not deliver my feet from falling, that I may walk before God in the light of the "
  "living."),
],
"psalms57": [
 ("Be Merciful unto Me (vv.1-3)",
  "Be merciful unto me, O God, be merciful unto me, for my soul trusteth in thee. The superscription "
  "places the psalm when he fled from Saul in the cave, which is either 1 Samuel 22 or 24, and the shelter "
  "imagery fits it, in the shadow of thy wings will I make my refuge, until these calamities be overpast. "
  "The last clause is about duration: the refuge is described as temporary because the trouble is."),
 ("My Soul Is Among Lions (v.4)",
  "My soul is among lions, I lie among them that are set on fire, even the sons of men, whose teeth are "
  "spears and arrows, and their tongue a sharp sword. One verse, and the animal and the weapon imagery are "
  "mixed deliberately: what makes the men dangerous turns out on inspection to be their speech."),
 ("The First Refrain (v.5)",
  "Be thou exalted, O God, above the heavens, let thy glory be above all the earth. The refrain appears "
  "twice, here and at verse 11, and it divides the psalm into a half about danger and a half about praise. "
  "What is asked for in it has nothing to do with the singer's situation, which is the point of putting it "
  "in the middle."),
 ("They Are Fallen Themselves (v.6)",
  "They have prepared a net for my steps, they have digged a pit before me, into the midst whereof they "
  "are fallen themselves. The self-defeating pattern of Psalm 7:15 and 9:15, stated in a single verse, and "
  "the psalm reports it as done rather than requested."),
 ("My Heart Is Fixed (vv.7-10)",
  "My heart is fixed, O God, my heart is fixed, I will sing and give praise. The word fixed means settled "
  "or established, and repeating it is the psalm's way of contrasting with the agitation of verse 4. Then "
  "the singer wakes the instruments and himself, awake, psaltery and harp, I myself will awake early. And "
  "the reach of the praise is deliberately wider than the cave, I will praise thee, O Lord, among the "
  "people, I will sing unto thee among the nations."),
 ("The Second Refrain (v.11)",
  "Be thou exalted, O God, above the heavens, let thy glory be above all the earth. The refrain again, "
  "unchanged, closing the psalm. Verses 7 to 11 appear again as the opening of Psalm 108, which is "
  "assembled out of parts of this psalm and Psalm 60."),
],
"psalms58": [
 ("Do Ye Judge Uprightly (vv.1-2)",
  "Do ye indeed speak righteousness, O congregation, do ye judge uprightly, O ye sons of men. The address "
  "is to judges and the first word of the Hebrew is difficult, read either as a congregation of rulers or "
  "as silent gods, which is why translations differ here. The charge is that the corruption is deliberate, "
  "yea, in heart ye work wickedness, ye weigh the violence of your hands in the earth."),
 ("Like the Deaf Adder (vv.3-5)",
  "The wicked are estranged from the womb, they go astray as soon as they be born, speaking lies. The claim "
  "is about origin rather than upbringing, which is as strong a statement of inherited fault as the "
  "psalter makes. Then an image from a working trade, they are like the deaf adder that stoppeth her ear, "
  "which will not hearken to the voice of charmers. A snake that cannot be handled by the usual method, "
  "which is the same figure Jeremiah 8:17 uses."),
 ("Break Their Teeth, O God (vv.6-9)",
  "Break their teeth, O God, in their mouth, break out the great teeth of the young lions. This is among "
  "the harshest passages in the psalter and the images come in a run: water running away, a snail melting, "
  "a stillbirth, thorns under a pot. What is being asked for in each is that the thing simply cease to "
  "be effective rather than be punished, let them melt away as waters which run continually."),
 ("Verily There Is a Reward (vv.10-11)",
  "The righteous shall rejoice when he seeth the vengeance, he shall wash his feet in the blood of the "
  "wicked. The image is deliberately shocking and the psalm makes no attempt to soften it. What it is "
  "arguing for is stated in the last verse and it is a conclusion about the world rather than a taste for "
  "revenge, so that a man shall say, Verily there is a reward for the righteous, verily he is a God that "
  "judgeth in the earth. The psalm exists because that had come into doubt."),
],
"psalms59": [
 ("Deliver Me from Mine Enemies (vv.1-5)",
  "Deliver me from mine enemies, O my God, defend me from them that rise up against me. The superscription "
  "places the psalm when Saul sent messengers to watch the house and kill him, which is 1 Samuel 19, and "
  "the psalm's imagery of a house being watched fits. And the claim is that the surveillance is unearned, "
  "not for my transgression, nor for my sin, O LORD."),
 ("They Go About the City (vv.6-7)",
  "They return at evening, they make a noise like a dog, and go round about the city. Two verses that "
  "describe the watchers as scavenging animals working a beat, and the detail about their speech is what "
  "makes it worse, behold, they belch out with their mouth, swords are in their lips, for who, say they, "
  "doth hear."),
 ("Thou, O LORD, Shalt Laugh at Them (vv.8-10)",
  "But thou, O LORD, shalt laugh at them, thou shalt have all the heathen in derision. The same laughter as "
  "Psalm 2:4 and 37:13. Then a title repeated twice in this psalm and nowhere else in quite this form, "
  "because of his strength will I wait upon thee, for God is my defence, and the last clause is the "
  "psalm's most confident line, the God of my mercy shall prevent me, that is, shall go before me."),
 ("Consume Them Not (vv.11-13)",
  "Slay them not, lest my people forget, scatter them by thy power. The petition is unusual because it "
  "asks for a slower judgment rather than a quicker one, and the reason given is educational: a sudden end "
  "would teach nobody. Then the purpose stated, and let them know that God ruleth in Jacob unto the ends "
  "of the earth."),
 ("They Go About the City Again (vv.14-15)",
  "And at evening let them return, and let them make a noise like a dog, and go round about the city. The "
  "two verses from earlier in the psalm repeated almost word for word, with one addition that changes "
  "their sense entirely, let them wander up and down for meat, and grudge if they be not satisfied. The "
  "watchers are now scavengers who go hungry, and the repetition is the psalm's way of showing the same "
  "scene after the answer of the middle section."),
 ("I Will Sing of Thy Power (vv.16-17)",
  "But I will sing of thy power, yea, I will sing aloud of thy mercy in the morning. Morning is set against "
  "the evening the watchers keep returning at, so the two halves of the day belong to different parties. "
  "And the psalm ends on the title from verse 9 repeated, unto thee, O my strength, will I sing, for God "
  "is my defence, and the God of my mercy."),
],
"psalms60": [
 ("O God, Thou Hast Cast Us Off (vv.1-3)",
  "O God, thou hast cast us off, thou hast scattered us, thou hast been displeased. The superscription "
  "attaches the psalm to a campaign in Aram and Edom recorded in 2 Samuel 8, which was a victory, and the "
  "psalm is a lament, so the connection is loose and the psalm may have been used after a reverse in the "
  "same war. The imagery is geological, thou hast made the earth to tremble, thou hast broken it. And the "
  "closing figure is drink, thou hast made us to drink the wine of astonishment."),
 ("A Banner Because of the Truth (vv.4-5)",
  "Thou hast given a banner to them that fear thee, that it may be displayed because of the truth. A "
  "banner was the rallying point in a battle and the phrase because of the truth explains what the "
  "rallying is for. Then the petition that follows from it, that thy beloved may be delivered, save with "
  "thy right hand, and hear me."),
 ("Gilead Is Mine, and Manasseh Is Mine (vv.6-8)",
  "God hath spoken in his holiness, I will rejoice, I will divide Shechem, and mete out the valley of "
  "Succoth. An oracle is quoted, and it is a survey of territory claimed by name, Gilead is mine, and "
  "Manasseh is mine, Ephraim also is the strength of mine head, Judah is my lawgiver. Then the "
  "neighbouring states are named in deliberately menial terms, Moab is my washpot, over Edom will I cast "
  "out my shoe, which is the language of a householder assigning chores."),
 ("Who Will Bring Me into the Strong City (vv.9-10)",
  "Who will bring me into the strong city, who will lead me into Edom. The question follows the confident "
  "oracle and undercuts it, and the answer is given as a complaint, wilt not thou, O God, which hadst cast "
  "us off, and thou, O God, which didst not go out with our armies. The psalm holds the promise and the "
  "present defeat in consecutive verses without reconciling them, which is what Psalm 44 also does."),
 ("Through God We Shall Do Valiantly (vv.11-12)",
  "Give us help from trouble, for vain is the help of man. The conclusion is the psalter's standing "
  "political judgment, stated here in four words. And the last verse is the answer to the question of "
  "verse 9, through God we shall do valiantly, for he it is that shall tread down our enemies. These two "
  "verses appear again as the close of Psalm 108."),
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
