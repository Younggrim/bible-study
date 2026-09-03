#!/usr/bin/env python3
"""
Psalms 37 to 48. Twelve pages, 208 verses.

Ten of the twelve outlines fold as they stand. psalms45 and psalms46 have no sublist at
all, so their sections are written from scratch, divided where each psalm divides: the
wedding song at the address to the king and then to the bride, and psalms46 at its two
refrains, which is the structure the Selah markings already indicate.

Psalms 42 and 43 belong together. They share a refrain that appears three times, at 42:5,
42:11 and 43:5, psalms43 has no superscription of its own, and many Hebrew manuscripts
treat them as one poem. The sections label the refrain consistently across both pages so
a reader following it can see that it crosses the break.

psalms41 closes Book I of the psalter, and its last verse is the doxology that marks the
division rather than part of the psalm's argument. The section says so.

Usage:
    python3 fold_psalms_037_048.py [--check]
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
"psalms37": [
 ("Fret Not Thyself (vv.1-11)",
  "Fret not thyself because of evildoers, neither be thou envious against the workers of iniquity. The "
  "psalm is an acrostic and a wisdom poem rather than a prayer, and its subject is the specific temptation "
  "of watching the wrong people prosper. The instruction fret not is given three times in the first eight "
  "verses. What is offered instead is a set of verbs, trust in the LORD, and do good, delight thyself also "
  "in the LORD, commit thy way unto the LORD, rest in the LORD, and wait patiently for him. And verse 11 "
  "is the beatitude Jesus quotes in Matthew 5:5, but the meek shall inherit the earth."),
 ("The Wicked Have Drawn Out the Sword (vv.12-15)",
  "The wicked plotteth against the just, and gnasheth upon him with his teeth. Then the same laughter as "
  "Psalm 2:4, the Lord shall laugh at him, for he seeth that his day is coming. And the outcome is stated "
  "as equipment turning back on its owner, their sword shall enter into their own heart, and their bows "
  "shall be broken, which is the self-defeating pattern of Psalm 7:15."),
 ("A Little That a Righteous Man Hath (vv.16-22)",
  "A little that a righteous man hath is better than the riches of many wicked. The section is a run of "
  "comparisons and every one of them turns on duration rather than on quantity, the LORD knoweth the days "
  "of the upright, and their inheritance shall be for ever. Then a picture of debt that measures a whole "
  "life, the wicked borroweth, and payeth not again, but the righteous sheweth mercy, and giveth."),
 ("I Have Been Young, and Now Am Old (vv.23-26)",
  "The steps of a good man are ordered by the LORD, and he delighteth in his way. Then a promise about "
  "falling that concedes the fall, though he fall, he shall not be utterly cast down, for the LORD "
  "upholdeth him with his hand. And the evidence offered is the poet's own age, which is the most personal "
  "claim in the psalm, I have been young, and now am old, yet have I not seen the righteous forsaken, nor "
  "his seed begging bread."),
 ("Depart from Evil, and Do Good (vv.27-31)",
  "Depart from evil, and do good, and dwell for evermore. The instruction is put in the same terms as "
  "34:14. Then the reason it is possible rather than merely required, and it is internal, the law of his "
  "God is in his heart, none of his steps shall slide, which is the promise Jeremiah 31:33 makes of the "
  "new covenant."),
 ("I Have Seen the Wicked in Great Power (vv.32-36)",
  "The wicked watcheth the righteous, and seeketh to slay him. Then the psalm's most honest concession, "
  "which is that the problem it addresses is real and visible, I have seen the wicked in great power, and "
  "spreading himself like a green bay tree. And the reversal is reported as an absence rather than an "
  "event, yet he passed away, and lo, he was not, yea, I sought him, but he could not be found."),
 ("Mark the Perfect Man (vv.37-40)",
  "Mark the perfect man, and behold the upright, for the end of that man is peace. The psalm closes by "
  "asking the reader to look at the end rather than the middle, which is what forty verses of comparison "
  "have been arguing for. And the last word is on where the help comes from, but the salvation of the "
  "righteous is of the LORD, he is their strength in the time of trouble."),
],
"psalms38": [
 ("Rebuke Me Not in Thy Wrath (vv.1-2)",
  "O LORD, rebuke me not in thy wrath, neither chasten me in thy hot displeasure. The same request as "
  "Psalm 6:1, word for word, and it asks for the manner to change rather than the discipline to stop. And "
  "the second verse names what it feels like, for thine arrows stick fast in me, and thy hand presseth me "
  "sore."),
 ("There Is No Soundness in My Flesh (vv.3-8)",
  "Six verses of physical description and they do not spare the reader, mine iniquities are gone over mine "
  "head, my wounds stink and are corrupt, I am troubled, I am bowed down greatly, I go mourning all the "
  "day long. What is unusual is the causation the psalm assigns, because of my sin and because of my "
  "foolishness, so the illness and the guilt are not separated. And the sound it ends on is animal, I have "
  "roared by reason of the disquietness of my heart."),
 ("My Groaning Is Not Hid from Thee (vv.9-10)",
  "Lord, all my desire is before thee, and my groaning is not hid from thee. Two verses that stop "
  "describing and simply note that the description was unnecessary. And the physical detail continues in "
  "the second, my heart panteth, my strength faileth me, as for the light of mine eyes, it also is gone "
  "from me."),
 ("My Lovers and My Friends Stand Aloof (v.11)",
  "One verse, and it is the loneliest in the psalm. My lovers and my friends stand aloof from my sore, and "
  "my kinsmen stand afar off. In a culture where illness carried ritual consequences the distance may have "
  "been required of them, which does not make it easier, and Psalm 31:11 and Job's friends describe the "
  "same withdrawal."),
 ("They Also That Seek My Hurt (v.12)",
  "One verse on the opposite behaviour: while the friends move away, they also that seek my hurt speak "
  "mischievous things, and imagine deceits all the day long. The two verses are placed side by side so "
  "that the absence of one group and the attention of the other are read together."),
 ("I Was as a Man That Heareth Not (vv.13-14)",
  "But I, as a deaf man, heard not, and I was as a dumb man that openeth not his mouth. The response to "
  "both the abandonment and the slander is deliberate silence, and it is described as a chosen condition "
  "rather than an inability. Isaiah 53:7 uses the same silence of the servant."),
 ("In Thee, O LORD, Do I Hope (vv.15-16)",
  "For in thee, O LORD, do I hope, thou wilt hear, O Lord my God. The reason for the silence of the "
  "previous section is given here: he is not answering because he is waiting for someone else to. And the "
  "concern named is the same as Psalm 13:4, lest they should rejoice over me, when my foot slippeth."),
 ("Forsake Me Not, O LORD (vv.17-22)",
  "For I am ready to halt, and my sorrow is continually before me. Then the confession, which the psalm "
  "has been circling since verse 3, for I will declare mine iniquity, I will be sorry for my sin. And the "
  "closing petitions are three and they are urgent rather than eloquent, forsake me not, O LORD, O my God, "
  "be not far from me, make haste to help me."),
],
"psalms39": [
 ("I Will Keep My Mouth with a Bridle (vv.1-3)",
  "I said, I will take heed to my ways, that I sin not with my tongue, I will keep my mouth with a bridle, "
  "while the wicked is before me. The silence here is a policy rather than a symptom, and the psalm records "
  "that it did not work, I was dumb with silence, I held my peace, even from good, and my sorrow was "
  "stirred. Then the pressure building, my heart was hot within me, while I was musing the fire burned, "
  "then spake I with my tongue. The rest of the psalm is what came out."),
 ("Make Me to Know Mine End (vv.4-6)",
  "LORD, make me to know mine end, and the measure of my days, what it is, that I may know how frail I am. "
  "What he asks for, after three verses of trying not to speak, is a lifespan. The measurements are all "
  "diminishing, behold, thou hast made my days as an handbreadth, and mine age is as nothing before thee. "
  "And the closing image is the psalter's bleakest assessment of accumulation, he heapeth up riches, and "
  "knoweth not who shall gather them, which is the observation Ecclesiastes builds a book on."),
 ("My Hope Is in Thee (vv.7-8)",
  "And now, Lord, what wait I for, my hope is in thee. Two verses, and the first is a question the psalm "
  "answers by elimination: given everything in the previous section, there is nothing else left to be "
  "waiting for. Then a petition about reputation, deliver me from all my transgressions, make me not the "
  "reproach of the foolish."),
 ("Remove Thy Stroke Away from Me (vv.9-11)",
  "I was dumb, I opened not my mouth, because thou didst it. The silence of the opening returns and is "
  "given a different reason: not discipline but recognition of the source. Then the request, remove thy "
  "stroke away from me, and an image of erosion, thou makest his beauty to consume away like a moth."),
 ("I Am a Stranger with Thee (vv.12-13)",
  "Hear my prayer, O LORD, and give ear unto my cry, hold not thy peace at my tears. Then the phrase the "
  "psalm is remembered for and it is a claim about status, for I am a stranger with thee, and a sojourner, "
  "as all my fathers were. A resident alien had rights of protection but no land. And the psalm ends on a "
  "request that no other psalm makes, O spare me, that I may recover strength, before I go hence, and be "
  "no more. He asks God to look away."),
],
"psalms40": [
 ("He Brought Me Up out of an Horrible Pit (vv.1-3)",
  "I waited patiently for the LORD, and he inclined unto me, and heard my cry. The rescue is described as "
  "extraction and then as engineering, he brought me up also out of an horrible pit, out of the miry clay, "
  "and set my feet upon a rock, and established my goings. Mud and rock, in one sentence. And the result is "
  "public rather than private, he hath put a new song in my mouth, and many shall see it, and fear, and "
  "shall trust in the LORD."),
 ("Many, O LORD, Are Thy Wonderful Works (vv.4-5)",
  "Blessed is that man that maketh the LORD his trust, and respecteth not the proud. Then a sentence that "
  "gives up on counting, many, O LORD my God, are thy wonderful works, they are more than can be numbered. "
  "The psalm's confidence in this section is arithmetic: the works outnumber the troubles of the section "
  "that will follow."),
 ("Mine Ears Hast Thou Opened (vv.6-8)",
  "Sacrifice and offering thou didst not desire, mine ears hast thou opened. The rejection of sacrifice in "
  "favour of obedience is the same argument as 1 Samuel 15:22 and Jeremiah 7:22. Then, then said I, Lo, I "
  "come, in the volume of the book it is written of me, I delight to do thy will, O my God. Hebrews 10:5-7 "
  "quotes the passage of Christ and follows the Septuagint, which reads a body hast thou prepared me where "
  "the Hebrew has mine ears hast thou opened, a difference the epistle's argument turns on."),
 ("I Have Not Hid Thy Righteousness (vv.9-10)",
  "I have preached righteousness in the great congregation, lo, I have not refrained my lips. Two verses "
  "of testimony that are all negatives, I have not hid thy righteousness within my heart, I have not "
  "concealed thy lovingkindness and thy truth from the great congregation. What is claimed is that nothing "
  "was withheld."),
 ("Let Thy Lovingkindness Preserve Me (v.11)",
  "One verse, and it is the hinge of the psalm. Withhold not thou thy mercy from me, O LORD, let thy "
  "lovingkindness and thy truth continually preserve me. The verb withhold answers the two verses above "
  "it, where the singer withheld nothing, and everything after it is trouble rather than testimony."),
 ("Mine Iniquities Have Taken Hold upon Me (vv.12-17)",
  "For innumerable evils have compassed me about. The word innumerable is the same claim made about God's "
  "works in verse 5, now made about troubles, and the accounting is honest about the source, mine "
  "iniquities have taken hold upon me, so that I am not able to look up. These six verses appear again "
  "almost word for word as Psalm 70. And the psalm ends without resolution, on need and a request for "
  "speed, but I am poor and needy, make no tarrying, O my God."),
],
"psalms41": [
 ("Blessed Is He That Considereth the Poor (vv.1-3)",
  "Blessed is he that considereth the poor, the LORD will deliver him in time of trouble. The psalm opens "
  "with a beatitude about attention to other people's need, and what is promised in return is nursing "
  "care, the LORD will strengthen him upon the bed of languishing, thou wilt make all his bed in his "
  "sickness. The promise fits the psalm, since the singer is himself ill."),
 ("Heal My Soul, for I Have Sinned (v.4)",
  "I said, LORD, be merciful unto me, heal my soul, for I have sinned against thee. One verse, and it puts "
  "the request and the admission in the same sentence without arranging them into an argument. Unlike "
  "Psalm 38 the psalm does not dwell on the connection; it states it once and moves to the people around "
  "the sickbed."),
 ("Mine Enemies Speak Evil of Me (vv.5-8)",
  "Mine enemies speak evil of me, When shall he die, and his name perish. The visitors are quoted, and the "
  "detail that makes the section work is the double behaviour, if he come to see me, he speaketh vanity, "
  "his heart gathereth iniquity, when he goeth abroad, he telleth it. Sympathy at the bedside and gossip "
  "outside the door. And their verdict is quoted as a diagnosis, an evil disease cleaveth unto him."),
 ("Mine Own Familiar Friend (v.9)",
  "One verse, and it is the sharpest in the psalm. Yea, mine own familiar friend, in whom I trusted, which "
  "did eat of my bread, hath lifted up his heel against me. Sharing bread put a man under obligation, "
  "which is what makes the betrayal a breach rather than a disappointment. Jesus quotes this verse in "
  "John 13:18 at the last supper, of Judas, and stops before the second half."),
 ("Raise Me Up, That I May Requite Them (vv.10-12)",
  "But thou, O LORD, be merciful unto me, and raise me up, that I may requite them. The psalm does not "
  "pretend to a magnanimity it has not got. And the evidence that God is on his side is put as a negative, "
  "by this I know that thou favourest me, because mine enemy doth not triumph over me, which is a modest "
  "test and the only one available to a man still in bed."),
 ("Blessed Be the LORD God of Israel (v.13)",
  "Blessed be the LORD God of Israel from everlasting, and to everlasting, Amen, and Amen. This verse is "
  "not part of the psalm's argument. It is the doxology that closes Book I of the psalter, which runs from "
  "Psalm 1 to Psalm 41, and the same formula closes Books II, III and IV at 72:19, 89:52 and 106:48. The "
  "five-book division is ancient and the doxologies are how it is marked in the text itself."),
],
"psalms42": [
 ("As the Hart Panteth (vv.1-2)",
  "As the hart panteth after the water brooks, so panteth my soul after thee, O God. The comparison is "
  "with an animal in drought rather than with ordinary thirst, so what is described is need rather than "
  "preference. And the question that follows names what is actually missing, when shall I come and appear "
  "before God, which is about access to the sanctuary. This psalm opens Book II of the psalter and is "
  "attributed to the sons of Korah rather than to David."),
 ("Where Is Thy God (v.3)",
  "My tears have been my meat day and night, while they continually say unto me, Where is thy God. One "
  "verse, and the taunt in it is the same one Psalm 3:2 reports: not a denial that God exists but a claim "
  "that he has not turned up. It is the question the whole psalm is answering, and the answer it gives is "
  "a refrain rather than an argument."),
 ("I Went with the Multitude (v.4)",
  "When I remember these things, I pour out my soul in me, for I had gone with the multitude, I went with "
  "them to the house of God, with the voice of joy and praise. The grief here is specifically the memory "
  "of having been in the crowd, which is worse than never having been. And the phrase with a multitude "
  "that kept holyday dates it to a festival he is now missing."),
 ("The First Refrain (v.5)",
  "Why art thou cast down, O my soul, and why art thou disquieted in me, hope thou in God, for I shall yet "
  "praise him. The verse is spoken by the singer to himself, which is unusual in the psalter and is the "
  "device this psalm is known for. It appears three times, here, at 42:11 and at 43:5, which is one of the "
  "reasons Psalms 42 and 43 are widely read as a single poem split in two."),
 ("Deep Calleth unto Deep (vv.6-7)",
  "O my God, my soul is cast down within me, therefore will I remember thee from the land of Jordan, and "
  "of the Hermonites, from the hill Mizar. The geography puts him in the far north, away from Jerusalem, "
  "which explains the whole complaint. Then the image the section is remembered for, and it is drawn from "
  "that landscape of gorges and waterfalls, deep calleth unto deep at the noise of thy waterspouts, all "
  "thy waves and thy billows are gone over me."),
 ("The LORD Will Command His Lovingkindness (v.8)",
  "Yet the LORD will command his lovingkindness in the daytime, and in the night his song shall be with "
  "me, and my prayer unto the God of my life. One verse of confidence in the middle of the complaint, "
  "divided between day and night, and the psalm does not stay there: the next section goes back to the "
  "question."),
 ("Why Hast Thou Forgotten Me (vv.9-10)",
  "I will say unto God my rock, Why hast thou forgotten me. The complaint is addressed to the title, which "
  "is the sharpest thing about it: a rock that has forgotten. And the taunt of verse 3 is quoted again "
  "word for word, mine enemies reproach me, while they say daily unto me, Where is thy God. The psalm is "
  "circling rather than progressing, which is what its refrain is for."),
 ("The Second Refrain (v.11)",
  "Why art thou cast down, O my soul, and why art thou disquieted within me, hope thou in God, for I shall "
  "yet praise him, who is the health of my countenance, and my God. The refrain returns unchanged except "
  "for one addition at the end, my God, which is the first time in the psalm the possessive is used without "
  "a question attached to it."),
],
"psalms43": [
 ("Plead My Cause (vv.1-2)",
  "Judge me, O God, and plead my cause against an ungodly nation. This psalm has no superscription of its "
  "own, which is rare in this part of the psalter, and it shares Psalm 42's refrain, so many Hebrew "
  "manuscripts join the two as one poem. The complaint continues from there without a break, why go I "
  "mourning because of the oppression of the enemy, and the question put to God is the same, why dost thou "
  "cast me off."),
 ("Send Out Thy Light and Thy Truth (v.3)",
  "O send out thy light and thy truth, let them lead me, let them bring me unto thy holy hill, and to thy "
  "tabernacles. One verse, and the two qualities are asked for as guides on a journey with a destination. "
  "What the whole of Psalm 42 was mourning was distance from the sanctuary, and this is the petition that "
  "names it directly."),
 ("Then Will I Go unto the Altar of God (v.4)",
  "Then will I go unto the altar of God, unto God my exceeding joy, yea, upon the harp will I praise thee. "
  "The verse follows from the previous one as a consequence rather than a hope, and what he intends to do "
  "on arrival is play. After two psalms of thirst and tears the destination is described as exceeding joy, "
  "which is the strongest phrase available."),
 ("The Third Refrain (v.5)",
  "Why art thou cast down, O my soul, and why art thou disquieted within me, hope in God, for I shall yet "
  "praise him, who is the health of my countenance, and my God. The refrain for the third and last time, "
  "and it closes the pair of psalms. Nothing has changed in the singer's circumstances between 42:5 and "
  "here: he is still in the north, still taunted, still away from the temple. What the refrain does is "
  "put the same sentence to himself three times, which the psalm evidently regards as the work."),
],
"psalms44": [
 ("We Have Heard with Our Ears (vv.1-3)",
  "We have heard with our ears, O God, our fathers have told us, what work thou didst in their days. The "
  "psalm opens with inherited testimony rather than personal experience, which is the position the whole "
  "poem argues from. And the conquest is described with the credit carefully assigned, they got not the "
  "land in possession by their own sword, but thy right hand, and thine arm, and the light of thy "
  "countenance, because thou hadst a favour unto them."),
 ("Through Thee Will We Push Down Our Enemies (vv.4-8)",
  "Thou art my King, O God, command deliverances for Jacob. Then the confession that makes the next "
  "section a genuine difficulty, for I will not trust in my bow, neither shall my sword save me. The "
  "congregation states that it has done exactly what the psalter recommends, and in God we boast all the "
  "day long, and praise thy name for ever."),
 ("Thou Hast Cast Us Off (vv.9-16)",
  "But thou hast cast off, and put us to shame, and goest not forth with our armies. Eight verses of "
  "military disaster described as God's own doing, and the verbs are all second person: thou makest us to "
  "turn back, thou hast given us like sheep appointed for meat, thou hast scattered us among the heathen, "
  "thou sellest thy people for nought. And the humiliation is measured in reputation, thou makest us a "
  "byword among the heathen, a shaking of the head among the people."),
 ("All This Is Come upon Us, Yet Have We Not Forgotten Thee (vv.17-22)",
  "All this is come upon us, yet have we not forgotten thee, neither have we dealt falsely in thy "
  "covenant. This is the section that makes the psalm unusual: it denies the standard explanation. Most "
  "national laments confess sin, and this one refuses to, our heart is not turned back, neither have our "
  "steps declined from thy way. And verse 22 is quoted by Paul in Romans 8:36 in the middle of his "
  "argument that nothing separates us from the love of Christ, for thy sake are we killed all the day "
  "long, we are counted as sheep for the slaughter. He quotes it as a description of the situation, not as "
  "a problem to be solved."),
 ("Awake, Why Sleepest Thou (vv.23-26)",
  "Awake, why sleepest thou, O Lord, arise, cast us not off for ever. The boldness of addressing God as "
  "asleep is not softened anywhere in the psalm, and Isaiah 51:9 uses the same imperative. The complaint "
  "is put once more as a question about attention, wherefore hidest thou thy face, and forgettest our "
  "affliction. And the psalm ends with no answer given and no reason offered, only a request and a ground "
  "for it that has nothing to do with deserving, arise for our help, and redeem us for thy mercies' sake."),
],
"psalms45": [
 ("My Heart Is Inditing a Good Matter (vv.1-2)",
  "My heart is inditing a good matter, I speak of the things touching the king, my tongue is the pen of a "
  "ready writer. The psalm announces itself as a composition and names its occasion, and the "
  "superscription calls it a song of loves, which is a wedding song for a royal marriage. What it says "
  "about the king begins with appearance and speech, thou art fairer than the children of men, grace is "
  "poured into thy lips."),
 ("Gird Thy Sword upon Thy Thigh (vv.3-5)",
  "Gird thy sword upon thy thigh, O most mighty, with thy glory and thy majesty. A wedding song that "
  "arms the bridegroom is startling to a modern reader and was ordinary in the ancient Near East, where a "
  "king's marriage and his military standing were the same subject. And what the sword is said to be for "
  "is stated in moral terms, ride prosperously because of truth and meekness and righteousness."),
 ("Thy Throne, O God, Is For Ever (vv.6-9)",
  "Thy throne, O God, is for ever and ever, the sceptre of thy kingdom is a right sceptre. These are the "
  "verses Hebrews 1:8-9 quotes and applies directly to the Son, and they are the reason this psalm is "
  "read messianically rather than only as court poetry: the king is addressed as God, and then in the next "
  "breath is said to have a God, therefore God, thy God, hath anointed thee with the oil of gladness above "
  "thy fellows. The Hebrew permits more than one construction and the tension is in the text rather than "
  "in the translation. Then the wedding itself, all thy garments smell of myrrh, and aloes, and cassia, "
  "and the queen standing at the right hand in gold of Ophir."),
 ("Hearken, O Daughter (vv.10-15)",
  "Hearken, O daughter, and consider, and incline thine ear, forget also thine own people, and thy "
  "father's house. The address turns to the bride and what is asked of her is emigration: a foreign "
  "princess marrying into Jerusalem leaves her own house behind, which is a real cost and is named as one. "
  "Then the promise, so shall the king greatly desire thy beauty. And the procession is described as she "
  "arrives, the king's daughter is all glorious within, her clothing is of wrought gold, she shall be "
  "brought unto the king with gladness and rejoicing."),
 ("Instead of Thy Fathers Shall Be Thy Children (vv.16-17)",
  "Instead of thy fathers shall be thy children, whom thou mayest make princes in all the earth. The "
  "answer to what she was asked to give up in verse 10 is given here: the family she leaves is replaced by "
  "the family she founds. And the psalm ends on the composer's own promise rather than the couple's, I "
  "will make thy name to be remembered in all generations, therefore shall the people praise thee for ever "
  "and ever."),
],
"psalms46": [
 ("God Is Our Refuge and Strength (vv.1-3)",
  "God is our refuge and strength, a very present help in trouble. Then the conditions under which that is "
  "claimed, and they are deliberately extreme, therefore will not we fear, though the earth be removed, "
  "and though the mountains be carried into the midst of the sea. Mountains were the standard image of "
  "permanence, so what is described is the failure of the most reliable things there are. And the section "
  "closes with a Selah, one of three in this psalm, which is a musical or liturgical marking whose exact "
  "sense is not recoverable but which here falls at each turn of the poem."),
 ("There Is a River (vv.4-7)",
  "There is a river, the streams whereof shall make glad the city of God. The contrast with the roaring "
  "sea of the previous section is the point, and it is geographical as well as poetic: Jerusalem has no "
  "river, only the Gihon spring, so the river here is a promise rather than a description. Ezekiel 47 and "
  "Revelation 22 both take up the image. Then the timing of the help, God shall help her, and that right "
  "early, and the refrain that closes the section, the LORD of hosts is with us, the God of Jacob is our "
  "refuge."),
 ("Be Still, and Know (vv.8-11)",
  "Come, behold the works of the LORD, what desolations he hath made in the earth. The invitation is to "
  "look at wreckage, and what is being wrecked is named in the next verse, he breaketh the bow, and "
  "cutteth the spear in sunder, he burneth the chariot in the fire. Disarmament rather than victory. Then "
  "the sentence the psalm is known by, be still, and know that I am God, and the stillness asked for is "
  "the opposite of the raging nations of verse 6 rather than a recommendation about quiet devotion. And "
  "the refrain returns to close the psalm, the LORD of hosts is with us, the God of Jacob is our refuge. "
  "Luther's Ein feste Burg is based on this psalm."),
],
"psalms47": [
 ("Clap Your Hands, All Ye People (vv.1-4)",
  "O clap your hands, all ye people, shout unto God with the voice of triumph. The address is to the "
  "nations rather than to Israel, which is the psalm's characteristic move, and the reason given is scale, "
  "for the LORD most high is terrible, he is a great King over all the earth. Then the land is described as "
  "a gift chosen rather than won, he shall choose our inheritance for us, the excellency of Jacob whom he "
  "loved."),
 ("God Is Gone Up with a Shout (vv.5-7)",
  "God is gone up with a shout, the LORD with the sound of a trumpet. The verse is most likely liturgical, "
  "describing the ark being carried up into the sanctuary, and Christian tradition has read it of the "
  "ascension. Then four imperatives to sing in a single verse, and the instruction that follows them is "
  "about manner, sing ye praises with understanding, which asks for attention rather than volume."),
 ("God Reigneth over the Heathen (vv.8-9)",
  "God reigneth over the heathen, God sitteth upon the throne of his holiness. And the last verse is the "
  "widest in the psalm, the princes of the people are gathered together, the people of the God of Abraham. "
  "Foreign rulers are described as belonging to Abraham's God, which is the promise of Genesis 12:3 read as "
  "already happening, and the closing clause makes the ownership explicit, for the shields of the earth "
  "belong unto God."),
],
"psalms48": [
 ("Great Is the LORD (vv.1-3)",
  "Great is the LORD, and greatly to be praised in the city of our God, in the mountain of his holiness. "
  "The psalm's subject is a place, and the geography is described in terms borrowed from the mythology of "
  "the region, beautiful for situation, the joy of the whole earth, is mount Zion, on the sides of the "
  "north. Zion is not in the north and is not a notable mountain; the phrase belongs to the divine "
  "dwelling of Canaanite poetry, and the psalm assigns it to Jerusalem."),
 ("The Kings Were Troubled (vv.4-7)",
  "For lo, the kings were assembled, they passed by together. The defeat is described entirely as a "
  "reaction, with no battle reported, they saw it, and so they marvelled, they were troubled, and hasted "
  "away. Then the physical description, fear took hold upon them there, and pain, as of a woman in "
  "travail. And the comparison the section ends on is naval, thou breakest the ships of Tarshish with an "
  "east wind, which for an inland city is a borrowed image of unstoppable loss."),
 ("As We Have Heard, So Have We Seen (v.8)",
  "As we have heard, so have we seen in the city of the LORD of hosts. One verse, and it is the exact "
  "counterpart of Psalm 44:1, where the congregation had heard from its fathers and was now losing. Here "
  "the inherited report and the present experience agree. The psalter puts both claims in its collection "
  "without harmonising them."),
 ("We Have Thought of Thy Lovingkindness (vv.9-11)",
  "We have thought of thy lovingkindness, O God, in the midst of thy temple. The word is meditated, and "
  "the location is the building, so what is described is deliberate reflection in a particular place. Then "
  "the reach of the reputation, according to thy name, O God, so is thy praise unto the ends of the earth. "
  "And the response asked for is regional, let mount Zion rejoice, let the daughters of Judah be glad."),
 ("Walk About Zion (vv.12-14)",
  "Walk about Zion, and go round about her, tell the towers thereof. The instruction is a survey, and it "
  "is oddly practical for a hymn: count the towers, mark the bulwarks, consider the palaces. The purpose "
  "is given in the next clause and it is educational, that ye may tell it to the generation following. And "
  "the closing verse moves from the fortifications to the one who is not among them, for this God is our "
  "God for ever and ever, he will be our guide even unto death."),
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
