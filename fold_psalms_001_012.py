#!/usr/bin/env python3
"""
Psalms 1 to 12. Twelve pages, 135 verses. All twelve outlines are gapless and are folded.

Psalms needs one addition to the preserved fields. Every page in the book carries five
of them, Author, Classification, Attributed Author, Key Themes and Historical Context,
and Attributed Author appears nowhere else in the corpus. It is kept, because on these
pages Author holds the compiler and Attributed Author holds the superscription's claim,
which are genuinely different facts.

Sections here are shorter than in the narrative books, and deliberately so. A psalm of
six verses does not support the exposition a chapter of Mark does, and padding it would
misdescribe the page. That is the same measurement already applied to the couplet
chapters of Proverbs.

psalms8's inherited outline used one label twice, God's Majestic Name, for verse 1 and
verse 9. The repetition is the psalm's own device, an inclusio, but two identical labels
on one page read as an error, so the second is renamed to say what it is doing.

Usage:
    python3 fold_psalms_001_012.py [--check]
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
"psalms1": [
 ("The Blessed Man (vv.1-3)",
  "The psalter opens on a single figure and describes him first by what he avoids, and the three verbs "
  "descend by stages, walketh not in the counsel of the ungodly, nor standeth in the way of sinners, nor "
  "sitteth in the seat of the scornful. Walking, standing, sitting: casual company becomes settled "
  "residence. What he does instead is stated as a habit rather than an achievement, his delight is in the "
  "law of the LORD, and in his law doth he meditate day and night. And the image is a planted tree with a "
  "water supply, not a wild one, he shall be like a tree planted by the rivers of water, whose leaf also "
  "shall not wither."),
 ("The Wicked Contrasted (vv.4-5)",
  "The ungodly are not like unto chaff, they are chaff, and the comparison is agricultural and dismissive: "
  "chaff is what the threshing floor throws away, weightless and rootless, the exact opposite of a tree "
  "with its roots in a stream. The consequence is judicial, therefore the ungodly shall not stand in the "
  "judgment, nor sinners in the congregation of the righteous, and the verb stand picks up the second of "
  "the three postures from verse 1."),
 ("The Two Ways (v.6)",
  "One verse closes the psalm and states the whole of it in two clauses, for the LORD knoweth the way of "
  "the righteous, but the way of the ungodly shall perish. The word knoweth carries more than "
  "information; it is the verb of acknowledgement and care. And the two ways set out here are the frame "
  "the entire psalter is read through, which is why this psalm has no title and functions as an "
  "introduction rather than as a song."),
],
"psalms2": [
 ("Why Do the Heathen Rage (vv.1-3)",
  "Why do the heathen rage, and the people imagine a vain thing. The psalm opens with a question about "
  "futility rather than about danger, and then quotes the conspirators directly, let us break their bands "
  "asunder, and cast away their cords from us. What they describe as bondage is God's rule, and the "
  "coalition is stated as universal, the kings of the earth set themselves, and the rulers take counsel "
  "together. Acts 4:25-26 quotes these verses of the alliance against Jesus."),
 ("He That Sitteth in the Heavens Shall Laugh (vv.4-6)",
  "He that sitteth in the heavens shall laugh, the Lord shall have them in derision. It is the only place "
  "in the psalter where God is described as laughing, and it is laughter at a plan rather than at people. "
  "Then the register changes without warning, then shall he speak unto them in his wrath. And the answer "
  "to the whole rebellion is not an argument but an appointment already made, yet have I set my king upon "
  "my holy hill of Zion."),
 ("Thou Art My Son (vv.7-9)",
  "The king speaks and quotes his own commission, I will declare the decree, the LORD hath said unto me, "
  "Thou art my Son, this day have I begotten thee. The formula belongs to a coronation, where the new "
  "king was declared God's son, and the New Testament applies it to Christ at Acts 13:33 and Hebrews 1:5 "
  "and 5:5. What is offered is territorial, ask of me, and I shall give thee the heathen for thine "
  "inheritance, and the instruments are a rod of iron and a potter's vessel, which Revelation 2:27 takes "
  "up."),
 ("Kiss the Son (vv.10-12)",
  "Be wise now therefore, O ye kings, be instructed, ye judges of the earth. The psalm ends not in triumph "
  "but in an invitation addressed to the rebels of verse 2, and its terms are a paradox held in one "
  "sentence, serve the LORD with fear, and rejoice with trembling. Then the gesture of submission, kiss "
  "the Son, lest he be angry. And the last clause is the psalm's only beatitude and it answers the first "
  "psalm, blessed are all they that put their trust in him."),
],
"psalms3": [
 ("Many Are They That Rise Up (vv.1-2)",
  "The superscription puts this psalm when David fled from Absalom his son, which is the rebellion of "
  "2 Samuel 15, and the arithmetic in the opening lines is the point, LORD, how are they increased that "
  "trouble me. What the enemies say is quoted, and it is theological rather than military, many there be "
  "which say of my soul, There is no help for him in God. The taunt is that God has taken a side and it "
  "is not his."),
 ("Thou, O LORD, Art a Shield (vv.3-4)",
  "But thou, O LORD, art a shield for me, my glory, and the lifter up of mine head. The three titles "
  "answer the taunt point by point: protection against the many, glory against the shame of flight, and a "
  "lifted head against a man leaving his own capital on foot. And the answer is reported as already "
  "received, I cried unto the LORD with my voice, and he heard me out of his holy hill."),
 ("I Laid Me Down and Slept (vv.5-6)",
  "I laid me down and slept, I awaked, for the LORD sustained me. Sleep is the evidence offered, and for a "
  "king in the open with an army behind him it is a stronger claim than courage would be. The conclusion "
  "drawn is proportional, I will not be afraid of ten thousands of people, that have set themselves "
  "against me round about."),
 ("Salvation Belongeth unto the LORD (vv.7-8)",
  "Arise, O LORD, save me, O my God, and the petition is followed by an image of enemies disarmed rather "
  "than destroyed, thou hast smitten all mine enemies upon the cheek bone, thou hast broken the teeth of "
  "the ungodly. And the psalm closes by widening from the singer to everyone, salvation belongeth unto the "
  "LORD, thy blessing is upon thy people."),
],
"psalms4": [
 ("Hear Me When I Call (v.1)",
  "Hear me when I call, O God of my righteousness, thou hast enlarged me when I was in distress. The "
  "petition is grounded in a past deliverance rather than in present need, and the verb enlarged is "
  "spatial: the previous trouble is described as a narrow place he was brought out of into room."),
 ("How Long Will Ye Love Vanity (vv.2-3)",
  "O ye sons of men, how long will ye turn my glory into shame, how long will ye love vanity, and seek "
  "after leasing. The psalm turns aside from prayer to address the opponents directly, which is unusual, "
  "and what it says to them is a statement of fact rather than a threat, but know that the LORD hath set "
  "apart him that is godly for himself."),
 ("Stand in Awe, and Sin Not (vv.4-5)",
  "Stand in awe, and sin not, commune with your own heart upon your bed, and be still. The instruction is "
  "to spend the night thinking rather than plotting, and Paul quotes the first clause in Ephesians 4:26 in "
  "the Greek form, be ye angry, and sin not, which is how the Septuagint rendered it. The pairing of "
  "sacrifice with trust in the next verse is characteristic of the psalter, offer the sacrifices of "
  "righteousness, and put your trust in the LORD."),
 ("More Than in the Time That Their Corn Increased (vv.6-7)",
  "There be many that say, Who will shew us any good. The complaint is quoted and then answered with a "
  "request for something other than the good being asked for, LORD, lift thou up the light of thy "
  "countenance upon us. And the comparison drawn is agricultural and exact, thou hast put gladness in my "
  "heart, more than in the time that their corn and their wine increased. Harvest gladness was the "
  "highest ordinary joy that culture knew, and it is used here as the thing being exceeded."),
 ("I Will Both Lay Me Down in Peace (v.8)",
  "I will both lay me down in peace, and sleep, for thou, LORD, only makest me dwell in safety. The psalm "
  "closes as Psalm 3 did, with sleep offered as the evidence, and the word only is doing the work: the "
  "safety is not the absence of the opponents addressed in verse 2 but something held independently of "
  "them."),
],
"psalms5": [
 ("In the Morning Will I Direct My Prayer (vv.1-3)",
  "Give ear to my words, O LORD, consider my meditation. The time of day is stated twice, my voice shalt "
  "thou hear in the morning, in the morning will I direct my prayer unto thee, and the verb direct is the "
  "one used of laying out a sacrifice on the altar, so the morning prayer is being described as the "
  "morning offering. And the last clause is about expectation rather than petition, and will look up."),
 ("Thou Hatest All Workers of Iniquity (vv.4-6)",
  "For thou art not a God that hath pleasure in wickedness, neither shall evil dwell with thee. The "
  "language is stronger than most readers expect from a psalm, thou hatest all workers of iniquity, thou "
  "shalt destroy them that speak leasing. What the passage is doing is establishing that the singer's "
  "case rests on God's character rather than on his own standing, which is why it comes before the "
  "request."),
 ("I Will Come into Thy House (vv.7-8)",
  "But as for me, I will come into thy house in the multitude of thy mercy. The contrast with the previous "
  "section turns on the ground of access, which is named as mercy rather than merit, and the posture is "
  "specified, and in thy fear will I worship toward thy holy temple. Then the petition, lead me, O LORD, "
  "in thy righteousness, make thy way straight before my face."),
 ("There Is No Faithfulness in Their Mouth (vv.9-10)",
  "For there is no faithfulness in their mouth, their inward part is very wickedness, their throat is an "
  "open sepulchre, they flatter with their tongue. Paul quotes the open sepulchre in Romans 3:13 in his "
  "chain of texts on universal guilt. And the petition against them is put as a request for consistency, "
  "cast them out in the multitude of their transgressions, for they have rebelled against thee, so the "
  "offence named is against God rather than against the singer."),
 ("Let All Those That Put Their Trust in Thee Rejoice (vv.11-12)",
  "But let all those that put their trust in thee rejoice, let them ever shout for joy, because thou "
  "defendest them. The psalm closes by widening from the individual to a category, and the last image is "
  "military equipment used as weather, for thou, LORD, wilt bless the righteous, with favour wilt thou "
  "compass him as with a shield. The shield surrounds rather than being carried."),
],
"psalms6": [
 ("O LORD, Rebuke Me Not in Thine Anger (vv.1-3)",
  "O LORD, rebuke me not in thine anger, neither chasten me in thy hot displeasure. The request is not to "
  "be spared the correction but to have its temperature changed, which is the same prayer Jeremiah makes "
  "for himself at 10:24. Then the physical state, have mercy upon me, O LORD, for I am weak, O LORD, heal "
  "me, for my bones are vexed. And the question that ends the section is left open, but thou, O LORD, how "
  "long."),
 ("In the Grave Who Shall Give Thee Thanks (vv.4-5)",
  "Return, O LORD, deliver my soul, oh save me for thy mercies' sake. The argument offered is one the "
  "psalter uses more than once and it is unsentimental about death, for in death there is no remembrance "
  "of thee, in the grave who shall give thee thanks. The reason for wanting to live is stated as the loss "
  "of a worshipper, which is the same case Hezekiah makes in Isaiah 38 and which the Old Testament "
  "generally leaves standing without the later hope attached."),
 ("All the Night Make I My Bed to Swim (vv.6-7)",
  "I am weary with my groaning, all the night make I my bed to swim, I water my couch with my tears. The "
  "exaggeration is deliberate and it is the psalter's normal way of measuring grief, by what it does to "
  "sleep and to the body, mine eye is consumed because of grief. Two verses on insomnia, and no relief "
  "offered inside them."),
 ("The LORD Hath Heard the Voice of My Weeping (vv.8-10)",
  "Depart from me, all ye workers of iniquity, for the LORD hath heard the voice of my weeping. The turn "
  "is abrupt and nothing in the psalm explains it, which is characteristic: the change is reported rather "
  "than accounted for. And the tense shifts to the perfect, the LORD hath heard my supplication, the LORD "
  "will receive my prayer, so what was asked for in verse 4 is spoken of as done by verse 9."),
],
"psalms7": [
 ("Save Me from All Them That Persecute Me (vv.1-2)",
  "O LORD my God, in thee do I put my trust, save me from all them that persecute me. The danger is put "
  "in a single image and it is a predator without a rescuer, lest he tear my soul like a lion, rending it "
  "in pieces, while there is none to deliver. The superscription attaches the psalm to words of Cush the "
  "Benjamite, an episode recorded nowhere else."),
 ("If I Have Done This (vv.3-5)",
  "O LORD my God, if I have done this, if there be iniquity in my hands. What follows is a self-imposed "
  "curse of the kind used in a legal oath, let the enemy persecute my soul, and take it, yea, let him "
  "tread down my life upon the earth. The singer is not claiming general innocence but submitting to a "
  "specific test on a specific charge, which is how such oaths worked."),
 ("Arise, O LORD, in Thine Anger (vv.6-9)",
  "Arise, O LORD, in thine anger, lift up thyself because of the rage of mine enemies. The request is for "
  "a court to be convened, and the jurisdiction claimed is universal, the LORD shall judge the people. "
  "Then the standard he asks to be measured by, judge me, O LORD, according to my righteousness, followed "
  "immediately by a clause that removes any thought of appearances, for the righteous God trieth the "
  "hearts and reins."),
 ("God Judgeth the Righteous (vv.10-13)",
  "My defence is of God, which saveth the upright in heart. Then a sentence about patience that is easy to "
  "read past, God judgeth the righteous, and God is angry with the wicked every day. And the imagery is "
  "of a weapon being prepared with time taken over it, he hath bent his bow, and made it ready, and the "
  "conditional in the middle of it is the point, if he turn not."),
 ("He Is Fallen into the Ditch (vv.14-16)",
  "Behold, he travaileth with iniquity, and hath conceived mischief, and brought forth falsehood. The "
  "wickedness is described as a pregnancy carried to term. Then the outcome is stated three ways, all of "
  "them self-inflicted, he made a pit, and is fallen into the ditch which he made, his mischief shall "
  "return upon his own head, and his violent dealing shall come down upon his own pate. No external "
  "agency is required."),
 ("I Will Praise the LORD (v.17)",
  "One verse, I will praise the LORD according to his righteousness, and will sing praise to the name of "
  "the LORD most high. The psalm that opened with a lion and a self-imposed curse ends in a single line of "
  "praise, and what is praised is the righteousness the singer had asked to be judged by."),
],
"psalms8": [
 ("How Excellent Is Thy Name (v.1)",
  "O LORD our Lord, how excellent is thy name in all the earth, who hast set thy glory above the heavens. "
  "The psalm opens and closes with the same line, which is a frame the Hebrew poets used to say that "
  "everything inside is contained by the thought. And the two prepositions are doing the work: the name "
  "is in all the earth, and the glory is above the heavens."),
 ("Out of the Mouth of Babes (v.2)",
  "Out of the mouth of babes and sucklings hast thou ordained strength because of thine enemies. One "
  "verse, and its logic is the reverse of what a hymn to majesty would be expected to say: the answer to "
  "the enemy is the smallest and least articulate voice available. Jesus quotes it in Matthew 21:16 when "
  "children are shouting in the temple courts and the authorities object."),
 ("When I Consider Thy Heavens (vv.3-4)",
  "When I consider thy heavens, the work of thy fingers, the moon and the stars, which thou hast ordained. "
  "The work of thy fingers is a deliberately small phrase for an enormous object. Then the question the "
  "psalm exists to ask, what is man, that thou art mindful of him, and the son of man, that thou visitest "
  "him. It is asked at night, looking up, which is why the scale of it lands."),
 ("Thou Hast Put All Things Under His Feet (vv.5-8)",
  "For thou hast made him a little lower than the angels, and hast crowned him with glory and honour. The "
  "answer to the question is not reassurance about God's kindness but a statement about human office, and "
  "it quotes Genesis 1 in its own words, thou madest him to have dominion over the works of thy hands, "
  "thou hast put all things under his feet. The list that follows descends from sheep and oxen to the "
  "fish of the sea, and whatsoever passeth through the paths of the seas. Hebrews 2:6-8 quotes the whole "
  "passage and observes that we do not yet see it happening."),
 ("The Refrain Returns (v.9)",
  "O LORD our Lord, how excellent is thy name in all the earth. Verse 1 repeated exactly, which closes the "
  "frame. Nothing has been added to the sentence, and after the intervening verses about the night sky "
  "and human dominion it is not the same sentence: the psalm has spent seven verses establishing what the "
  "name is excellent in comparison with."),
],
"psalms9": [
 ("I Will Praise Thee with My Whole Heart (vv.1-6)",
  "I will praise thee, O LORD, with my whole heart, I will shew forth all thy marvellous works. The psalm "
  "opens in the first person and with four verbs of intention, praise, shew forth, be glad, sing. Then the "
  "reason moves to the past tense and to a court, when mine enemies are turned back, they shall fall and "
  "perish at thy presence, for thou hast maintained my right. And the closing image is of a record "
  "erased, thou hast destroyed cities, their memorial is perished with them, which in that world was the "
  "most complete defeat available."),
 ("A Refuge in Times of Trouble (vv.7-10)",
  "But the LORD shall endure for ever, he hath prepared his throne for judgment. The contrast is with the "
  "perished memorials of the previous verse: what lasts is a court rather than a city. Then the two verses "
  "the psalm is best known for, and the LORD will be a refuge for the oppressed, a refuge in times of "
  "trouble, and they that know thy name will put their trust in thee, for thou, LORD, hast not forsaken "
  "them that seek thee."),
 ("Sing Praises to the LORD, Which Dwelleth in Zion (vv.11-14)",
  "Sing praises to the LORD, which dwelleth in Zion, declare among the people his doings. Then a clause "
  "about what God keeps track of, for he forgetteth not the cry of the humble, and the petition returns "
  "with an image of a threshold, thou that liftest me up from the gates of death. And the purpose given "
  "for the deliverance is public, that I may shew forth all thy praise in the gates of the daughter of "
  "Zion, so the gates of death are answered by the gates of the city."),
 ("The Heathen Is Sunk in the Pit (vv.15-16)",
  "The heathen is sunk down in the pit that they made, in the net which they hid is their own foot taken. "
  "The same principle as 7:15, and the psalm pauses over it, the LORD is known by the judgment which he "
  "executeth, the wicked is snared in the work of his own hands. The word Higgaion is attached here, a "
  "musical or reflective direction whose sense is not recoverable."),
 ("Put Them in Fear (vv.17-20)",
  "The wicked shall be turned into hell, and all the nations that forget God. Then the promise the psalm "
  "has been building toward, and it is about patience rather than reversal, for the needy shall not alway "
  "be forgotten, the expectation of the poor shall not perish for ever. And the closing petition asks for "
  "a specific and modest thing, put them in fear, O LORD, that the nations may know themselves to be but "
  "men."),
],
"psalms10": [
 ("Why Standest Thou Afar Off (v.1)",
  "Why standest thou afar off, O LORD, why hidest thou thyself in times of trouble. One verse, and it is "
  "a complaint rather than a petition. The psalm is left without a superscription in the Hebrew, and the "
  "Septuagint joins it to Psalm 9 as one composition, which is why the numbering of the psalter differs "
  "between the Hebrew and Greek traditions from here until Psalm 147."),
 ("The Wicked Boasteth (vv.2-11)",
  "Ten verses on one subject, which is unusually sustained for the psalter, and the portrait is built out "
  "of things the man says. He is quoted four times: God hath forgotten, he hideth his face, he will never "
  "see it, and I shall not be moved, and I shall never be in adversity. Then the method described, he "
  "lieth in wait secretly as a lion in his den, he doth catch the poor. And the diagnosis in verse 4 is "
  "the sharpest line in the psalm, God is not in all his thoughts, which is not denial but absence of the "
  "question."),
 ("Arise, O LORD, Lift Up Thine Hand (vv.12-15)",
  "Arise, O LORD, O God, lift up thine hand, forget not the humble. The petition answers the boast word "
  "for word: the man said God had forgotten, and the prayer asks him not to forget. Then a claim against "
  "the man's own reasoning, thou hast seen it, for thou beholdest mischief and spite, to requite it with "
  "thy hand. And the closing line names the poor's actual position, the poor committeth himself unto thee, "
  "thou art the helper of the fatherless."),
 ("The LORD Is King for Ever (vv.16-18)",
  "The LORD is King for ever and ever, the heathen are perished out of the land. The complaint of verse 1 "
  "is not answered with an explanation but with a statement about who is on the throne. Then hearing, LORD, "
  "thou hast heard the desire of the humble. And the psalm's last purpose clause is the most concrete in "
  "it, to judge the fatherless and the oppressed, that the man of the earth may no more oppress."),
],
"psalms11": [
 ("How Say Ye to My Soul, Flee (vv.1-3)",
  "In the LORD put I my trust, how say ye to my soul, Flee as a bird to your mountain. The psalm opens by "
  "quoting advice and refusing it, and the advice is not cowardly but sensible, since the reason given is "
  "military, for lo, the wicked bend their bow, they make ready their arrow upon the string. And the "
  "counsellors' closing argument is the strongest thing in the psalm, if the foundations be destroyed, "
  "what can the righteous do."),
 ("The LORD Is in His Holy Temple (vv.4-5)",
  "The answer does not address the arrows. The LORD is in his holy temple, the LORD's throne is in heaven, "
  "his eyes behold, his eyelids try, the children of men. The reply to the collapse of the foundations is "
  "a statement about where the throne is, which is not where the fighting is. And what the watching is "
  "for is stated in the next verse, the LORD trieth the righteous, so the observation includes the singer "
  "and is not only surveillance of the enemy."),
 ("Fire and Brimstone (v.6)",
  "Upon the wicked he shall rain fire and brimstone, and an horrible tempest, this shall be the portion of "
  "their cup. One verse, and the vocabulary is Sodom's, which is the psalter's shorthand for a judgment "
  "that comes from outside the human situation altogether. The cup as a measure of allotted fate runs "
  "from here through Jeremiah 25 to Gethsemane."),
 ("The Upright Shall Behold His Face (v.7)",
  "For the righteous LORD loveth righteousness, his countenance doth behold the upright. The psalm that "
  "began with an instruction to run away ends with a face rather than a fortress, and the reversal of the "
  "opening image is deliberate: the advice was to flee to a mountain, and what is offered instead is "
  "being looked at."),
],
"psalms12": [
 ("Help, LORD, for the Godly Man Ceaseth (v.1)",
  "Help, LORD, for the godly man ceaseth, for the faithful fail from among the children of men. One verse "
  "of assessment, and it is the same complaint as Isaiah 57:1 and Micah 7:2: not that the wicked are "
  "strong but that the good are running out. The verb is one of numbers dwindling rather than of defeat."),
 ("They Speak with a Double Heart (vv.2-4)",
  "They speak vanity every one with his neighbour, with flattering lips and with a double heart. The "
  "problem this psalm is about is speech, and the petition against it is specific to the organ, the LORD "
  "shall cut off all flattering lips, and the tongue that speaketh proud things. Then the boast is quoted "
  "and it is a claim of independence, with our tongue will we prevail, our lips are our own, who is lord "
  "over us."),
 ("Now Will I Arise, Saith the LORD (v.5)",
  "For the oppression of the poor, for the sighing of the needy, now will I arise, saith the LORD. One "
  "verse, and it is the only place in the psalm where God speaks. What moves him is named as a sound "
  "rather than an argument, the sighing of the needy, and what he promises is stated in their own terms, "
  "I will set him in safety from him that puffeth at him."),
 ("The Words of the LORD Are Pure Words (v.6)",
  "The words of the LORD are pure words, as silver tried in a furnace of earth, purified seven times. The "
  "verse is placed immediately after God's one speech in the psalm and immediately after four verses about "
  "human speech that cannot be trusted, so the comparison is the argument. And the image is technical: "
  "silver refined seven times is a specification, not a flourish."),
 ("Thou Shalt Preserve Them (vv.7-8)",
  "Thou shalt keep them, O LORD, thou shalt preserve them from this generation for ever. The promise is "
  "made without any claim that the conditions will improve, and the last verse of the psalm says so, the "
  "wicked walk on every side, when the vilest men are exalted. The psalm ends where it began, with the "
  "faithful in a minority, and what has changed in between is that God has been quoted."),
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
