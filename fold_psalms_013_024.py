#!/usr/bin/env python3
"""
Psalms 13 to 24. Twelve pages, 177 verses. All twelve outlines are gapless and are folded.

psalms15's outline divides at a half verse, 2-5a and 5b, and the split is kept because
the psalm turns there: ten qualifications end and the promise begins inside verse 5.

Four of these psalms are quoted heavily in the New Testament and the sections say where
rather than leaving the reader to find out: 14:1-3 in Romans 3, 16:8-11 in Acts 2 and 13,
19:4 in Romans 10, and 22 throughout the crucifixion accounts.

Usage:
    python3 fold_psalms_013_024.py [--check]
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
"psalms13": [
 ("How Long (vv.1-2)",
  "How long wilt thou forget me, O LORD, for ever, how long wilt thou hide thy face from me. The question "
  "is asked four times in two verses, which is the whole structure of the complaint: not an argument but "
  "a repetition. And the four are not identical in target, two are about God, one about the singer's own "
  "state, how long shall I take counsel in my soul, having sorrow in my heart daily, and one about the "
  "enemy."),
 ("Consider and Hear Me (vv.3-4)",
  "Consider and hear me, O LORD my God, lighten mine eyes, lest I sleep the sleep of death. Three "
  "petitions after four questions, and the reason offered is the one the psalter uses repeatedly, which is "
  "reputational rather than personal, lest mine enemy say, I have prevailed against him. Sleep here is "
  "death rather than rest, which is the reverse of its use in Psalms 3 and 4."),
 ("I Will Sing unto the LORD (vv.5-6)",
  "But I have trusted in thy mercy, my heart shall rejoice in thy salvation. Six verses is the whole "
  "psalm, and the turn happens with no event in between: nothing is reported as having changed except the "
  "tense. And the last verse commits to something not yet true, I will sing unto the LORD, because he "
  "hath dealt bountifully with me."),
],
"psalms14": [
 ("The Fool Hath Said (v.1)",
  "The fool hath said in his heart, There is no God. The denial is located in the heart rather than in "
  "argument, and the word for fool in Hebrew is moral rather than intellectual: nabal is a person whose "
  "judgment is corrupt, not one who has reasoned badly. And the consequence follows in the same verse, "
  "they are corrupt, they have done abominable works, there is none that doeth good."),
 ("There Is None That Doeth Good (vv.2-3)",
  "The LORD looked down from heaven upon the children of men, to see if there were any that did "
  "understand, and seek God. The search is described as a survey and its result is total, they are all "
  "gone aside, they are all together become filthy, there is none that doeth good, no, not one. Paul "
  "quotes these verses at length in Romans 3:10-12 as the centre of his case that the charge falls on "
  "everybody."),
 ("Have All the Workers of Iniquity No Knowledge (vv.4-6)",
  "Have all the workers of iniquity no knowledge, who eat up my people as they eat bread. The oppression "
  "is described as routine, which is the force of the comparison with bread: not an atrocity but a meal. "
  "Then a fear that comes from nowhere, there were they in great fear, for God is in the generation of "
  "the righteous. And the closing line names who was being counted on, ye have shamed the counsel of the "
  "poor, because the LORD is his refuge."),
 ("Oh That the Salvation of Israel Were Come (v.7)",
  "Oh that the salvation of Israel were come out of Zion. One verse, and it turns a psalm about universal "
  "corruption into a request for a specific rescue from a specific place. And the outcome is stated as an "
  "emotion rather than a victory, when the LORD bringeth back the captivity of his people, Jacob shall "
  "rejoice, and Israel shall be glad."),
],
"psalms15": [
 ("Who Shall Abide in Thy Tabernacle (v.1)",
  "LORD, who shall abide in thy tabernacle, who shall dwell in thy holy hill. One verse, and it is a "
  "question of the kind a pilgrim arriving at the sanctuary gate would ask, which is probably its original "
  "setting. Psalm 24:3 asks the same question in almost the same words and answers it more briefly."),
 ("He That Walketh Uprightly (vv.2-5a)",
  "The answer is a list and every item is conduct rather than belief, which is the point of it: he that "
  "walketh uprightly, and worketh righteousness, and speaketh the truth in his heart. Then the negatives, "
  "he that backbiteth not with his tongue, nor doeth evil to his neighbour, nor taketh up a reproach "
  "against his neighbour. Three of the ten concern speech about other people. Two are unexpectedly "
  "specific and costly, he that sweareth to his own hurt, and changeth not, that is, keeps a bargain that "
  "turns out badly for him, and he that putteth not out his money to usury. The section stops in the "
  "middle of verse 5 because the qualifications end there."),
 ("He That Doeth These Things Shall Never Be Moved (v.5b)",
  "Half a verse, and it is the answer to the question in verse 1. He that doeth these things shall never "
  "be moved. Nothing is promised about prosperity or long life, only stability, and it is attached to the "
  "list rather than to the temple: the person described is secure whether or not he is standing on the "
  "holy hill."),
],
"psalms16": [
 ("Preserve Me, O God (vv.1-2)",
  "Preserve me, O God, for in thee do I put my trust. Then a confession that concedes something most "
  "religious language avoids, thou art my Lord, my goodness extendeth not to thee. Whatever good the "
  "singer has is of no use to God, which removes the transaction from the relationship before the psalm "
  "goes any further."),
 ("Their Sorrows Shall Be Multiplied (vv.3-4)",
  "My goodness extends instead to other people, and the saints that are in the earth are named as the "
  "excellent, in whom is all my delight. Against that, the alternative is refused in the plainest terms "
  "available, their drink offerings of blood will I not offer, nor take up their names into my lips. "
  "Refusing to say the names is the strongest form of dissociation that culture had."),
 ("The Lines Are Fallen unto Me in Pleasant Places (vv.5-6)",
  "The LORD is the portion of mine inheritance and of my cup, thou maintainest my lot. The vocabulary is "
  "the land allotment of Joshua, where each tribe received a portion measured out by line, except that "
  "Levi received no land and was told that the LORD was its inheritance. The singer applies the Levite's "
  "arrangement to himself and calls it a good deal, the lines are fallen unto me in pleasant places, yea, "
  "I have a goodly heritage."),
 ("I Have Set the LORD Always Before Me (vv.7-8)",
  "I will bless the LORD, who hath given me counsel, my reins also instruct me in the night seasons. Then "
  "the sentence Peter quotes in Acts 2:25 at Pentecost, I have set the LORD always before me, because he "
  "is at my right hand, I shall not be moved. The posture described is deliberate attention rather than "
  "feeling, and the conclusion drawn from it is stability."),
 ("Thou Wilt Not Leave My Soul in Hell (vv.9-11)",
  "Therefore my heart is glad, and my glory rejoiceth, my flesh also shall rest in hope. Then the verse "
  "the New Testament makes most use of in this psalm, for thou wilt not leave my soul in hell, neither "
  "wilt thou suffer thine Holy One to see corruption. Peter quotes it in Acts 2 and Paul in Acts 13, and "
  "both argue the same way: David died and was buried, so the verse was not finally about him. And the "
  "psalm closes on a phrase about direction, thou wilt shew me the path of life, in thy presence is "
  "fulness of joy."),
],
"psalms17": [
 ("Hear the Right, O LORD (vv.1-5)",
  "Hear the right, O LORD, attend unto my cry, give ear unto my prayer, that goeth not out of feigned "
  "lips. The claim is not general innocence but honesty in this particular petition. Then the test "
  "invited, thou hast proved mine heart, thou hast visited me in the night, thou hast tried me, and shalt "
  "find nothing. And the ground of the claim is stated as restraint rather than achievement, concerning "
  "the works of men, by the word of thy lips I have kept me from the paths of the destroyer."),
 ("Keep Me as the Apple of the Eye (vv.6-9)",
  "I have called upon thee, for thou wilt hear me, O God, incline thine ear unto me. Then two images that "
  "have both passed into ordinary English, keep me as the apple of the eye, hide me under the shadow of "
  "thy wings. The first is the pupil, the most instinctively protected part of the body, and the second is "
  "a bird sheltering its young, which is the same figure Jesus uses of Jerusalem in Matthew 23:37."),
 ("Like a Lion Greedy of His Prey (vv.10-12)",
  "They are inclosed in their own fat, with their mouth they speak proudly. The description moves from "
  "arrogance to hunting, they have now compassed us in our steps, they have set their eyes bowing down to "
  "the earth. And the comparison is doubled to cover both danger and patience, like as a lion that is "
  "greedy of his prey, and as it were a young lion lurking in secret places."),
 ("Deliver My Soul from the Wicked (vv.13-14)",
  "Arise, O LORD, disappoint him, cast him down, deliver my soul from the wicked. Then a description of "
  "the opponents by what they have, men of the world, which have their portion in this life, and the phrase "
  "is doing careful work: their portion is real and it is bounded. And the last clause notes that it "
  "extends beyond them, they leave the rest of their substance to their babes, so the psalm concedes their "
  "prosperity is durable and still calls it a portion in this life."),
 ("I Shall Be Satisfied, When I Awake (v.15)",
  "As for me, I will behold thy face in righteousness, I shall be satisfied, when I awake, with thy "
  "likeness. One verse set against the previous one, and every term in it is the counterpart of something "
  "there: their portion against his satisfaction, this life against waking, and possessions against a "
  "face. Whether awake means morning or something further is left open by the Hebrew, and the psalm does "
  "not press it."),
],
"psalms18": [
 ("The LORD Is My Rock (vv.1-3)",
  "I will love thee, O LORD, my strength, and what follows is a stack of titles rather than a sentence, "
  "my rock, and my fortress, and my deliverer, my God, my strength, my buckler, the horn of my salvation, "
  "and my high tower. Seven of them, all defensive, and most of them geological or architectural. This "
  "psalm appears almost word for word as 2 Samuel 22, which makes it one of only a handful of texts "
  "preserved twice in the Old Testament."),
 ("The Sorrows of Death Compassed Me (vv.4-6)",
  "The sorrows of death compassed me, and the floods of ungodly men made me afraid. The danger is put in "
  "water and rope imagery, the sorrows of hell compassed me about, the snares of death prevented me. Then "
  "the one action taken, in my distress I called upon the LORD, and the answer is located, he heard my "
  "voice out of his temple, and my cry came before him, even into his ears."),
 ("He Bowed the Heavens (vv.7-15)",
  "Nine verses of theophany, and it is the longest sustained storm description in the psalter. Then the "
  "earth shook and trembled, the foundations also of the hills moved. The imagery is drawn from every "
  "element at once, smoke out of his nostrils, coals of fire, darkness under his feet, a cherub as a "
  "vehicle, thick clouds as a pavilion, hail and coals of fire, arrows and lightnings. And the last verse "
  "strips the world back to bedrock, then the channels of waters were seen, and the foundations of the "
  "world were discovered. All of this is the answer to one man calling from distress."),
 ("He Drew Me Out of Many Waters (vv.16-19)",
  "He sent from above, he took me, he drew me out of many waters. After nine verses of cosmic disturbance "
  "the rescue itself is four verbs and one man being lifted. And the reason given is unexpected in a "
  "passage this violent, he delivered me, because he delighted in me. The last verse names where he was "
  "put, he brought me forth also into a large place, which is the opposite of the snares and floods of "
  "verse 5."),
 ("I Have Kept the Ways of the LORD (vv.20-24)",
  "The LORD rewarded me according to my righteousness, according to the cleanness of my hands hath he "
  "recompensed me. The claim is uncomfortable to modern readers and the psalm makes it without "
  "qualification, I was also upright before him, and I kept myself from mine iniquity. What it is "
  "claiming is loyalty in a specific conflict rather than sinlessness, which is how the same claim works "
  "in Psalm 7."),
 ("With the Merciful Thou Wilt Shew Thyself Merciful (vv.25-29)",
  "With the merciful thou wilt shew thyself merciful, with an upright man thou wilt shew thyself upright, "
  "with the pure thou wilt shew thyself pure, and with the froward thou wilt shew thyself froward. Four "
  "clauses on one principle: God is met in the manner he is approached. Then two images of scale, thou "
  "wilt save the afflicted people, but wilt bring down high looks, and one of personal capability, by my "
  "God have I leaped over a wall."),
 ("He Teacheth My Hands to War (vv.30-42)",
  "Thirteen verses on equipment and training, and the striking thing is how much of it is instruction "
  "rather than protection, he teacheth my hands to war, so that a bow of steel is broken by mine arms. "
  "The physical detail is specific, he maketh my feet like hinds' feet, thou hast enlarged my steps under "
  "me, that my feet did not slip, thou hast girded me with strength unto the battle. And the outcome is "
  "reported without decoration, I have pursued mine enemies, and overtaken them, neither did I turn again "
  "till they were consumed."),
 ("A People Whom I Have Not Known (vv.43-45)",
  "Thou hast made me the head of the heathen, a people whom I have not known shall serve me. The horizon "
  "widens from the battlefield to an empire, and the submission is described as coming before contact, as "
  "soon as they hear of me, they shall obey me. Paul quotes verse 49 from the next section in Romans 15:9 "
  "as evidence that the Gentiles were always in view."),
 ("The LORD Liveth (vv.46-50)",
  "The LORD liveth, and blessed be my rock, and let the God of my salvation be exalted. The psalm returns "
  "to the titles it opened with, which closes a frame across fifty verses. And the last verse names the "
  "reach of the promise beyond the singer, great deliverance giveth he to his king, and sheweth mercy to "
  "his anointed, to David, and to his seed for evermore."),
],
"psalms19": [
 ("The Heavens Declare (vv.1-6)",
  "The heavens declare the glory of God, and the firmament sheweth his handywork. What the passage is "
  "careful about is the manner of the speech, and the paradox is stated outright, there is no speech nor "
  "language, where their voice is not heard. A wordless communication with universal range, and Paul takes "
  "up verse 4 in Romans 10:18. Then the sun is described as a runner and a bridegroom, which rejoiceth as "
  "a strong man to run a race, and its circuit is total, from the end of the heaven, and there is nothing "
  "hid from the heat thereof."),
 ("The Law of the LORD Is Perfect (vv.7-11)",
  "The subject changes from the sky to the scriptures and the form changes with it: six lines, each naming "
  "the law with a different word and pairing it with an adjective and an effect. The law is perfect, "
  "converting the soul, the testimony is sure, making wise the simple, the statutes are right, rejoicing "
  "the heart, the commandment is pure, enlightening the eyes, the fear is clean, enduring for ever, the "
  "judgments are true and righteous altogether. Then two comparisons, more to be desired are they than "
  "gold, sweeter also than honey and the honeycomb, so value and pleasure are both claimed."),
 ("Cleanse Thou Me from Secret Faults (vv.12-14)",
  "Who can understand his errors, cleanse thou me from secret faults. The turn to the first person is the "
  "third movement of the psalm, and the sins named are the ones the previous section's clear law cannot "
  "reach: the ones the singer cannot see. Then a request for restraint, keep back thy servant also from "
  "presumptuous sins. And the closing verse asks for something unusual, that the words of my mouth, and "
  "the meditation of my heart, be acceptable in thy sight, which puts speech and thought forward as an "
  "offering after eleven verses about other people's."),
],
"psalms20": [
 ("The LORD Hear Thee in the Day of Trouble (vv.1-5)",
  "The LORD hear thee in the day of trouble, the name of the God of Jacob defend thee. The whole section "
  "is in the second person singular and it is a congregation praying for a king before a campaign, which "
  "the references to offerings and to the sanctuary make clear, send thee help from the sanctuary, and "
  "strengthen thee out of Zion. And what is asked is specific to the occasion, grant thee according to "
  "thine own heart, and fulfil all thy counsel."),
 ("Now Know I That the LORD Saveth His Anointed (v.6)",
  "Now know I that the LORD saveth his anointed, he will hear him from his holy heaven with the saving "
  "strength of his right hand. One verse, and the change from the plural prayer to a single confident "
  "voice suggests a moment in the liturgy, possibly an answer given at the sanctuary. Whatever prompted "
  "it, the verb is now know rather than hope."),
 ("Some Trust in Chariots (vv.7-8)",
  "Some trust in chariots, and some in horses, but we will remember the name of the LORD our God. It is "
  "the sharpest single contrast in the psalter's political theology, and it is the same argument Isaiah "
  "makes at 31:1. Chariots were the decisive military technology of the age. And the outcome is put in the "
  "perfect tense, they are brought down and fallen, but we are risen, and stand upright."),
 ("Save, LORD (v.9)",
  "Save, LORD, let the king hear us when we call. The psalm ends as it began, with the congregation asking "
  "rather than declaring, and the last clause is ambiguous in the Hebrew as to who is being asked to hear. "
  "The English follows one reading; the Septuagint takes it the other way, save the king and hear us."),
],
"psalms21": [
 ("The King Shall Joy in Thy Strength (vv.1-7)",
  "The king shall joy in thy strength, O LORD, and in thy salvation how greatly shall he rejoice. This is "
  "the answer to the previous psalm: there the congregation prayed before a campaign, here it celebrates "
  "afterwards, and the granting is stated in the same words the prayer used, thou hast given him his "
  "heart's desire. What was given is listed, a crown of pure gold, length of days, honour and majesty, and "
  "the last verse names the mechanism the whole psalm rests on, for the king trusteth in the LORD."),
 ("Thine Hand Shall Find Out Thine Enemies (vv.8-12)",
  "Thine hand shall find out thine enemies, thy right hand shall find out those that hate thee. The "
  "address shifts and the language becomes hard, thou shalt make them as a fiery oven in thine anger, and "
  "the fire shall devour them. What is threatened extends past the men, and their fruit shalt thou destroy "
  "from the earth, which is the standard ancient concern with a dynasty rather than an individual. And the "
  "reason is stated as intent, for they intended evil against thee."),
 ("Be Thou Exalted (v.13)",
  "Be thou exalted, LORD, in thine own strength, so will we sing and praise thy power. One verse, and it "
  "moves the exaltation from the king, who has occupied twelve verses, onto God. The last word of a royal "
  "psalm is about somebody else's strength."),
],
"psalms22": [
 ("My God, Why Hast Thou Forsaken Me (vv.1-2)",
  "My God, my God, why hast thou forsaken me. Jesus quotes this line from the cross in Matthew 27:46 and "
  "Mark 15:34, in Aramaic, and it is the only one of the seven sayings that is a question. The complaint "
  "is not only about absence but about distance from help, why art thou so far from helping me. And the "
  "second verse adds the duration, I cry in the daytime, but thou hearest not, and in the night season, "
  "and am not silent."),
 ("Our Fathers Trusted in Thee (vv.3-5)",
  "But thou art holy, O thou that inhabitest the praises of Israel. The turn is immediate and it is an "
  "argument rather than a consolation: our fathers trusted in thee, they trusted, and thou didst deliver "
  "them. Three times in two verses the verb trusted is used of previous generations, and the point being "
  "made is that the pattern is well established, which is precisely what makes the present silence a "
  "problem."),
 ("A Worm, and No Man (vv.6-8)",
  "But I am a worm, and no man, a reproach of men, and despised of the people. Then the mockery is quoted, "
  "they shoot out the lip, they shake the head, saying, He trusted in the LORD, let him deliver him. "
  "Matthew 27:43 records almost those words being said at the cross, and the mockery works by turning the "
  "argument of the previous section against the sufferer: the fathers trusted and were delivered, so the "
  "absence of a rescue is taken as evidence."),
 ("Thou Art He That Took Me Out of the Womb (vv.9-11)",
  "But thou art he that took me out of the womb, thou didst make me hope when I was upon my mother's "
  "breasts. Against the taunt of verse 8 the psalm offers a longer history than the fathers' and a more "
  "personal one, thou art my God from my mother's belly. And the petition follows from the loneliness "
  "rather than from the danger, be not far from me, for there is none to help."),
 ("Bulls of Bashan (vv.12-13)",
  "Many bulls have compassed me, strong bulls of Bashan have beset me round. Bashan was the region known "
  "for its cattle, so the comparison is with the largest and best-fed animals anybody had seen. And the "
  "second verse changes species without warning, they gaped upon me with their mouths, as a ravening and a "
  "roaring lion."),
 ("They Pierced My Hands and My Feet (vv.14-18)",
  "I am poured out like water, and all my bones are out of joint, my heart is like wax. The physical "
  "description is the most detailed in the psalter and several of its lines are quoted or echoed in the "
  "crucifixion accounts: my tongue cleaveth to my jaws, which John 19:28 answers with I thirst; they "
  "pierced my hands and my feet, where the Hebrew is difficult and the Septuagint reads pierced; I may "
  "tell all my bones, and John 19:36 notes that none were broken; and they part my garments among them, "
  "and cast lots upon my vesture, which all four Gospels record as done at the foot of the cross."),
 ("Deliver My Soul from the Sword (vv.19-21)",
  "But be not thou far from me, O LORD, O my strength, haste thee to help me. The petitions come in a rush "
  "and the animals of the previous sections are gathered into them, deliver my soul from the sword, my "
  "darling from the power of the dog, save me from the lion's mouth, from the horns of the unicorns. And "
  "the last clause of verse 21 in the Hebrew is a bare statement that the answer came, which is where the "
  "psalm turns."),
 ("I Will Declare Thy Name unto My Brethren (vv.22-26)",
  "I will declare thy name unto my brethren, in the midst of the congregation will I praise thee. Hebrews "
  "2:12 quotes this verse and puts it in Christ's mouth. Nothing in the psalm explains the change of tone; "
  "the deliverance is not described, only its effect, for he hath not despised nor abhorred the affliction "
  "of the afflicted. And the closing line is a meal, the meek shall eat and be satisfied, so a public "
  "thanksgiving offering is being shared out."),
 ("All the Ends of the World Shall Remember (vv.27-31)",
  "All the ends of the world shall remember and turn unto the LORD. The psalm's final movement widens from "
  "one sufferer to the whole earth and then to time, and all the kindreds of the nations shall worship "
  "before thee. Two groups are named that are usually left out, they that go down to the dust and a seed "
  "that shall serve him, so the dead and the unborn are both included. And the last three words in the "
  "Hebrew are a single perfect verb, he hath done it, which John 19:30 answers with it is finished."),
],
"psalms23": [
 ("The LORD Is My Shepherd (vv.1-3)",
  "The LORD is my shepherd, I shall not want. Shepherd was a royal title across the ancient Near East, so "
  "the opening claim is political as well as pastoral. What follows is a working description of good "
  "husbandry rather than a sentiment: he maketh me to lie down in green pastures, he leadeth me beside the "
  "still waters. Sheep will not drink from moving water and will not lie down while anxious, so both "
  "details are statements about the competence of the shepherd. And the last clause names the motive, he "
  "leadeth me in the paths of righteousness for his name's sake."),
 ("The Valley of the Shadow of Death (v.4)",
  "Yea, though I walk through the valley of the shadow of death, I will fear no evil, for thou art with "
  "me. The grammar changes here and it is the hinge of the psalm: the first three verses speak of God in "
  "the third person, and from this verse on it is thou. The shift to direct address happens in the valley "
  "rather than in the pasture. And the equipment named is the shepherd's two tools, thy rod and thy staff, "
  "one for driving off predators and one for guiding."),
 ("Thou Preparest a Table (v.5)",
  "Thou preparest a table before me in the presence of mine enemies. The imagery changes from pasture to "
  "hospitality and the enemies are not removed, only outlasted: the meal happens in front of them. Then "
  "two marks of a host's honour, thou anointest my head with oil, my cup runneth over, and the overflowing "
  "cup is the psalter's picture of provision beyond requirement."),
 ("I Will Dwell in the House of the LORD (v.6)",
  "Surely goodness and mercy shall follow me all the days of my life. The verb is stronger than follow "
  "suggests; it is the word used of pursuit, so the two qualities are described as chasing him rather than "
  "trailing behind. And the last clause moves from tent to house, and I will dwell in the house of the LORD "
  "for ever, which ends a psalm about travelling with an address."),
],
"psalms24": [
 ("The Earth Is the LORD's (vv.1-2)",
  "The earth is the LORD's, and the fulness thereof, the world, and they that dwell therein. Paul quotes "
  "the verse twice in 1 Corinthians 10 to settle a question about food. The ground of the claim is given "
  "as construction, for he hath founded it upon the seas, and established it upon the floods, which uses "
  "the imagery of the surrounding creation stories and assigns the outcome to one builder."),
 ("Who Shall Ascend into the Hill of the LORD (vv.3-6)",
  "Who shall ascend into the hill of the LORD, or who shall stand in his holy place. The question of "
  "Psalm 15:1 asked again, and the answer here is shorter and arranged by body part, he that hath clean "
  "hands, and a pure heart, who hath not lifted up his soul unto vanity. Then the promise, he shall "
  "receive the blessing from the LORD, and righteousness from the God of his salvation, so what the "
  "qualified person receives is described as given rather than earned."),
 ("Lift Up Your Heads, O Ye Gates (vv.7-10)",
  "Lift up your heads, O ye gates, and be ye lift up, ye everlasting doors, and the King of glory shall "
  "come in. The passage is built as an exchange, almost certainly sung antiphonally as a procession "
  "arrived at the sanctuary: a summons, then a challenge from inside, who is this King of glory, then an "
  "answer, the LORD strong and mighty, the LORD mighty in battle. The whole thing repeats with a different "
  "answer the second time, the LORD of hosts, he is the King of glory, so the question is asked twice and "
  "answered twice, and the psalm ends on the title rather than on the entry."),
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
