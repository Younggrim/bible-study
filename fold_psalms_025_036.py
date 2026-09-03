#!/usr/bin/env python3
"""
Psalms 25 to 36. Twelve pages, 199 verses. All twelve outlines are gapless and are folded.

The inherited outlines on psalms31 through 36 wrote their ranges with a space, as (vv. 1-8)
rather than (vv.1-8), which no other page in the corpus does. The rewritten labels use the
compact form throughout.

Two of these are acrostics, 25 and 34, where each line begins with a successive letter of
the Hebrew alphabet. Neither is perfect: 25 is missing a letter and repeats another, and 34
omits one. The sections say so where it affects how the psalm reads, because an acrostic
explains why a poem moves from subject to subject without an argument connecting them.

Usage:
    python3 fold_psalms_025_036.py [--check]
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
"psalms25": [
 ("Unto Thee, O LORD, Do I Lift Up My Soul (vv.1-7)",
  "The psalm is an acrostic, each line beginning with the next letter of the Hebrew alphabet, which is why "
  "it moves between petition, instruction and confession without connecting arguments: the form is "
  "supplying the order. What is asked first is not rescue but instruction, shew me thy ways, O LORD, teach "
  "me thy paths. Then a request about memory that runs both ways, remember not the sins of my youth, and "
  "remember thou me for thy mercy's sake."),
 ("Good and Upright Is the LORD (vv.8-10)",
  "Good and upright is the LORD, therefore will he teach sinners in the way. The logic of that therefore "
  "is worth pausing on: God's goodness is given as the reason he instructs the guilty rather than as a "
  "reason to expect the opposite. And the meek are named as those who get the most out of it, the meek "
  "will he guide in judgment, and the meek will he teach his way."),
 ("For Thy Name's Sake, Pardon Mine Iniquity (vv.11-15)",
  "For thy name's sake, O LORD, pardon mine iniquity, for it is great. The reason offered for the pardon "
  "is the size of the debt, which is not the argument anyone would expect. Then a promise about "
  "instruction repeated a third time, him shall he teach in the way that he shall choose, and the phrase "
  "that gives the psalm its warmest line, the secret of the LORD is with them that fear him."),
 ("Turn Thee unto Me (vv.16-22)",
  "Turn thee unto me, and have mercy upon me, for I am desolate and afflicted. The troubles are listed "
  "without ranking, the troubles of my heart are enlarged, look upon mine affliction and my pain, and "
  "forgive all my sins. And the psalm ends by widening past the singer in a verse that falls outside the "
  "acrostic pattern, redeem Israel, O God, out of all his troubles, which suggests it was added when the "
  "psalm was taken into congregational use."),
],
"psalms26": [
 ("Judge Me, O LORD (vv.1-3)",
  "Judge me, O LORD, for I have walked in mine integrity. The request is for a verdict rather than for "
  "mercy, which is a different kind of prayer from Psalm 25 immediately before it, and the singer invites "
  "the examination, examine me, O LORD, and prove me, try my reins and my heart. What he offers as "
  "evidence is not achievement but attention, for thy lovingkindness is before mine eyes."),
 ("I Have Not Sat with Vain Persons (vv.4-5)",
  "I have not sat with vain persons, neither will I go in with dissemblers. The claim is made entirely in "
  "terms of company kept, which is the same measure Psalm 1 opens the psalter with, and it is stated as "
  "hatred rather than avoidance, I have hated the congregation of evil doers."),
 ("I Will Wash Mine Hands in Innocency (vv.6-8)",
  "I will wash mine hands in innocency, so will I compass thine altar, O LORD. Priests washed before "
  "approaching the altar, so the gesture is being borrowed and given a moral sense. Then the reason for "
  "wanting to be there, and it is affection rather than duty, LORD, I have loved the habitation of thy "
  "house, and the place where thine honour dwelleth."),
 ("Gather Not My Soul with Sinners (vv.9-10)",
  "Gather not my soul with sinners, nor my life with bloody men. The petition is about classification: "
  "not to be spared but not to be counted with a particular group. And the group is identified by one "
  "practice, in whose hands is mischief, and their right hand is full of bribes, which is the specific "
  "corruption the psalms return to most often in judicial contexts."),
 ("My Foot Standeth in an Even Place (vv.11-12)",
  "But as for me, I will walk in mine integrity, redeem me, and be merciful unto me. The two halves of "
  "that verse sit oddly together, since integrity is claimed and mercy is asked for in one breath, and the "
  "psalm does not reconcile them. And the last verse answers the psalm's own anxiety about where he will "
  "be placed, my foot standeth in an even place, in the congregations will I bless the LORD."),
],
"psalms27": [
 ("The LORD Is My Light and My Salvation (vv.1-6)",
  "The LORD is my light and my salvation, whom shall I fear. The first half of the psalm is confidence "
  "and it is expressed as a series of rhetorical questions and unlikely calm, though an host should "
  "encamp against me, in this will I be confident. What is asked for in the middle of a military "
  "situation is domestic, one thing have I desired of the LORD, that I may dwell in the house of the LORD "
  "all the days of my life. A man under threat asks for residence rather than for victory."),
 ("Hide Not Thy Face Far from Me (vv.7-12)",
  "Hear, O LORD, when I cry with my voice, have mercy also upon me, and answer me. The second half of the "
  "psalm is anxious and the change is abrupt enough that some have read the two halves as separate poems. "
  "The petition turns on a face, when thou saidst, Seek ye my face, my heart said unto thee, Thy face, "
  "LORD, will I seek, hide not thy face far from me. And the fear named is abandonment by the closest "
  "people, when my father and my mother forsake me, then the LORD will take me up."),
 ("Wait on the LORD (vv.13-14)",
  "I had fainted, unless I had believed to see the goodness of the LORD in the land of the living. The "
  "verse concedes how near collapse was, which is unusual for a psalm that opened as confidently as this "
  "one. And the last verse is addressed outward rather than upward, wait on the LORD, be of good courage, "
  "and he shall strengthen thine heart, with the instruction repeated at the end, wait, I say, on the "
  "LORD."),
],
"psalms28": [
 ("Be Not Silent to Me (vv.1-2)",
  "Unto thee will I cry, O LORD my rock, be not silent to me. The fear is not of judgment but of no answer "
  "at all, lest, if thou be silent to me, I become like them that go down into the pit. Then the posture, "
  "when I lift up my hands toward thy holy oracle, which is the standing gesture of prayer in the "
  "psalter and is directed at a place."),
 ("Draw Me Not Away with the Wicked (vv.3-5)",
  "Draw me not away with the wicked, and with the workers of iniquity, which speak peace to their "
  "neighbours, but mischief is in their hearts. The offence named is the gap between what is said and what "
  "is meant, and the petition against them asks for accuracy rather than severity, give them according to "
  "their deeds, and according to the wickedness of their endeavours. And the reason is a failure of "
  "attention, because they regard not the works of the LORD."),
 ("The LORD Hath Heard the Voice of My Supplications (vv.6-7)",
  "Blessed be the LORD, because he hath heard the voice of my supplications. The turn is sudden and "
  "unexplained, as in Psalms 6 and 13, and the tense changes to the perfect. Then a stack of titles, the "
  "LORD is my strength and my shield, my heart trusted in him, and I am helped, and the response is "
  "physical, therefore my heart greatly rejoiceth, and with my song will I praise him."),
 ("Save Thy People (vv.8-9)",
  "The LORD is their strength, and he is the saving strength of his anointed. The psalm widens from the "
  "individual to the nation in its last two verses, which is the pattern of Psalms 25 and 51 as well. And "
  "the closing petition uses the shepherd language of Psalm 23 in the plural, feed them also, and lift "
  "them up for ever."),
],
"psalms29": [
 ("Give unto the LORD the Glory (vv.1-2)",
  "Give unto the LORD, O ye mighty, give unto the LORD glory and strength. The address is not to Israel "
  "but to heavenly beings, sons of the mighty in the Hebrew, so the psalm opens above the world rather "
  "than in it. And what is asked for is worship in a specific manner, worship the LORD in the beauty of "
  "holiness."),
 ("The Voice of the LORD (vv.3-9)",
  "The phrase the voice of the LORD occurs seven times in these seven verses, which is the structure of "
  "the psalm and the reason it is read as a storm moving across the country. It begins over water, the "
  "voice of the LORD is upon the waters, then breaks the cedars of Lebanon in the north, shakes the "
  "wilderness of Kadesh in the south, and ends in the sanctuary. The physical detail is exact for a storm "
  "front, he maketh them also to skip like a calf, and the flames of fire are lightning. Scholars have "
  "long noted how closely the imagery matches Canaanite storm-god poetry, and what the psalm does with it "
  "is assign every one of those effects to one name."),
 ("The LORD Sitteth upon the Flood (vv.10-11)",
  "The LORD sitteth upon the flood, yea, the LORD sitteth King for ever. The verb is sitting, immediately "
  "after seven verses of noise and breakage, and the word for flood is the one used of Noah's, so what is "
  "described is a throne over the worst water there has been. And the last verse turns the whole storm "
  "toward a congregation, the LORD will give strength unto his people, the LORD will bless his people "
  "with peace."),
],
"psalms30": [
 ("Thou Hast Lifted Me Up (vv.1-3)",
  "I will extol thee, O LORD, for thou hast lifted me up, and hast not made my foes to rejoice over me. "
  "The verb lifted is the one used of drawing a bucket from a well, which fits what follows, O LORD, thou "
  "hast brought up my soul from the grave. The illness or danger is not described, only its depth and the "
  "fact that it is over."),
 ("Joy Cometh in the Morning (vv.4-5)",
  "Sing unto the LORD, O ye saints of his, and give thanks at the remembrance of his holiness. Then the "
  "two verses the psalm is remembered for, and they are a comparison of durations, for his anger endureth "
  "but a moment, in his favour is life, weeping may endure for a night, but joy cometh in the morning. "
  "Nothing in the psalm claims the night is short. It claims the morning comes."),
 ("I Shall Never Be Moved (vv.6-7)",
  "And in my prosperity I said, I shall never be moved. The singer quotes his own complacency, which is a "
  "rare thing for a psalm to do, and identifies what had actually been holding him up, LORD, by thy favour "
  "thou hast made my mountain to stand strong. Then the withdrawal in half a verse, thou didst hide thy "
  "face, and I was troubled."),
 ("What Profit Is There in My Blood (vv.8-10)",
  "I cried to thee, O LORD, and unto the LORD I made supplication. The argument used is the same one "
  "Psalm 6 and Isaiah 38 use and it is put as a question about usefulness, what profit is there in my "
  "blood, when I go down to the pit, shall the dust praise thee, shall it declare thy truth. The case for "
  "being kept alive is that a dead worshipper is no use to anybody."),
 ("Thou Hast Turned My Mourning into Dancing (vv.11-12)",
  "Thou hast turned for me my mourning into dancing, thou hast put off my sackcloth, and girded me with "
  "gladness. The change is described as a change of clothes, which makes it public rather than internal. "
  "And the purpose clause at the end answers the question of verse 9 directly, to the end that my glory "
  "may sing praise to thee, and not be silent."),
],
"psalms31": [
 ("In Thee, O LORD, Do I Put My Trust (vv.1-8)",
  "In thee, O LORD, do I put my trust, let me never be ashamed. The opening eight verses stack refuge "
  "images, be thou my strong rock, for an house of defence to save me, for thou art my rock and my "
  "fortress. And verse 5 is the sentence Jesus speaks as his last word from the cross in Luke 23:46, into "
  "thine hand I commit my spirit, which makes this psalm and Psalm 22 the two he quotes there. Stephen "
  "uses a version of it in Acts 7:59."),
 ("My Strength Faileth (vv.9-13)",
  "Have mercy upon me, O LORD, for I am in trouble, mine eye is consumed with grief. The distress is "
  "described physically and then socially, and the social part is worse: I was a reproach among my "
  "neighbours, and a fear to mine acquaintance, they that did see me without fled from me. Then the phrase "
  "Jeremiah adopts as his own nickname for a man at 20:10, I have heard the slander of many, fear was on "
  "every side."),
 ("But I Trusted in Thee (vv.14-18)",
  "But I trusted in thee, O LORD, I said, Thou art my God. The turn is marked by the word but and by a "
  "claim about time rather than about circumstances, my times are in thy hand. Then the petitions, make "
  "thy face to shine upon thy servant, and a request against the speech that had done the damage in the "
  "previous section, let the lying lips be put to silence."),
 ("Oh How Great Is Thy Goodness (vv.19-22)",
  "Oh how great is thy goodness, which thou hast laid up for them that fear thee. The image is of a store "
  "kept in reserve and then of a hiding place, thou shalt hide them in the secret of thy presence from the "
  "pride of man. And the singer then admits what he had said in the middle of it, for I said in my haste, "
  "I am cut off from before thine eyes, and reports that he was wrong, nevertheless thou heardest the "
  "voice of my supplications."),
 ("Be of Good Courage (vv.23-24)",
  "O love the LORD, all ye his saints, for the LORD preserveth the faithful. The psalm ends turned outward "
  "and giving instruction, which is where Psalm 27 also ends, and in almost the same words, be of good "
  "courage, and he shall strengthen your heart, all ye that hope in the LORD."),
],
"psalms32": [
 ("Blessed Is He Whose Transgression Is Forgiven (vv.1-2)",
  "Blessed is he whose transgression is forgiven, whose sin is covered. Three words for wrongdoing and "
  "three for its removal appear in these two verses, which is the psalm's way of being thorough. Paul "
  "quotes them in Romans 4:7-8 as his evidence that righteousness is reckoned rather than earned. And the "
  "last clause adds a condition that is about honesty rather than merit, in whose spirit there is no "
  "guile."),
 ("My Bones Waxed Old (vv.3-4)",
  "When I kept silence, my bones waxed old through my roaring all the day long. The silence described is "
  "not calm but concealment, and its effects are physical, thy hand was heavy upon me, my moisture is "
  "turned into the drought of summer. Two verses on what not saying it cost."),
 ("I Acknowledged My Sin (v.5)",
  "One verse, and it is the turn of the psalm. I acknowledged my sin unto thee, and mine iniquity have I "
  "not hid, I said, I will confess my transgressions unto the LORD, and thou forgavest the iniquity of my "
  "sin. The forgiveness arrives inside the same sentence as the confession, with nothing between them, "
  "which after two verses of wasting is the whole point of the arrangement."),
 ("Thou Art My Hiding Place (vv.6-7)",
  "For this shall every one that is godly pray unto thee in a time when thou mayest be found. The "
  "experience is turned into instruction, and the clause about timing implies a window, as Isaiah 55:6 "
  "does. Then the image the section is known for, thou art my hiding place, thou shalt preserve me from "
  "trouble, thou shalt compass me about with songs of deliverance."),
 ("I Will Guide Thee with Mine Eye (vv.8-9)",
  "I will instruct thee and teach thee in the way which thou shalt go, I will guide thee with mine eye. "
  "The voice changes to God's for two verses. And the warning attached is drawn from stable management, "
  "be ye not as the horse, or as the mule, which have no understanding, whose mouth must be held in with "
  "bit and bridle. Guidance by eye or guidance by bridle: the difference is whether the animal is paying "
  "attention."),
 ("Be Glad in the LORD (vv.10-11)",
  "Many sorrows shall be to the wicked, but he that trusteth in the LORD, mercy shall compass him about. "
  "The verb compass is the same one used of the songs in verse 7, so the psalm closes the circle it drew "
  "there. And the last verse is three imperatives of joy, be glad in the LORD, and rejoice, ye righteous, "
  "and shout for joy, all ye that are upright in heart."),
],
"psalms33": [
 ("Sing unto Him a New Song (vv.1-3)",
  "Rejoice in the LORD, O ye righteous, for praise is comely for the upright. The instruction is musical "
  "and specific, praise the LORD with harp, sing unto him with the psaltery and an instrument of ten "
  "strings. And the last clause asks for competence as well as enthusiasm, play skilfully with a loud "
  "noise, which is a rare thing for a hymn to specify."),
 ("He Loveth Righteousness and Judgment (vv.4-5)",
  "For the word of the LORD is right, and all his works are done in truth. Two verses that set the psalm's "
  "subject, and the last clause is a claim about quantity that the rest of the poem will argue for, the "
  "earth is full of the goodness of the LORD."),
 ("By the Word of the LORD Were the Heavens Made (vv.6-9)",
  "By the word of the LORD were the heavens made, and all the host of them by the breath of his mouth. The "
  "creation is described as speech rather than labour, which follows Genesis 1 closely, and the sea is "
  "handled without a struggle, he gathereth the waters of the sea together as an heap. Then the "
  "conclusion drawn is a demand for attention from everybody, let all the earth fear the LORD, and the "
  "reason is put in two clauses that leave no interval, for he spake, and it was done, he commanded, and "
  "it stood fast."),
 ("The Counsel of the LORD Standeth for Ever (vv.10-12)",
  "The LORD bringeth the counsel of the heathen to nothing, he maketh the devices of the people of none "
  "effect. Against that, the counsel of the LORD standeth for ever, the thoughts of his heart to all "
  "generations. The contrast is between plans that expire and one that does not. And the beatitude that "
  "closes the section is national, blessed is the nation whose God is the LORD."),
 ("He Fashioneth Their Hearts Alike (vv.13-15)",
  "The LORD looketh from heaven, he beholdeth all the sons of men. The observation is described as "
  "comprehensive and the reason given for its accuracy is unusual, he fashioneth their hearts alike, he "
  "considereth all their works. The maker of the instrument is the one reading it."),
 ("There Is No King Saved by the Multitude of an Host (vv.16-17)",
  "There is no king saved by the multitude of an host, a mighty man is not delivered by much strength. "
  "Two verses of military scepticism, and the second names the most expensive asset of the age, an horse "
  "is a vain thing for safety, neither shall he deliver any by his great strength. This is the same "
  "argument as Psalm 20:7 and Isaiah 31:1."),
 ("The Eye of the LORD Is upon Them That Fear Him (vv.18-19)",
  "Behold, the eye of the LORD is upon them that fear him, upon them that hope in his mercy. The general "
  "observation of verses 13 to 15 is here narrowed to a particular attention, and what it is for is stated "
  "in two plain outcomes, to deliver their soul from death, and to keep them alive in famine."),
 ("Our Soul Waiteth for the LORD (vv.20-22)",
  "Our soul waiteth for the LORD, he is our help and our shield. The psalm ends in the first person plural "
  "and in the posture the psalter recommends most often. And the last verse is a petition rather than a "
  "declaration, which is a modest ending for a poem about creation and empires, let thy mercy, O LORD, be "
  "upon us, according as we hope in thee."),
],
"psalms34": [
 ("I Will Bless the LORD at All Times (vv.1-7)",
  "The psalm is an acrostic, and one Hebrew letter is missing from the sequence, which is worth knowing "
  "because it explains the loose connection between its parts. It opens in the first person, I will bless "
  "the LORD at all times, and then invites company, O magnify the LORD with me. The testimony is specific "
  "about what was removed, I sought the LORD, and he heard me, and delivered me from all my fears. And the "
  "closing image is a garrison, the angel of the LORD encampeth round about them that fear him."),
 ("O Taste and See (vv.8-10)",
  "O taste and see that the LORD is good, blessed is the man that trusteth in him. The invitation is "
  "sensory rather than argumentative, which is unusual, and 1 Peter 2:3 takes it up. Then a comparison "
  "drawn from the top of the food chain, the young lions do lack, and suffer hunger, but they that seek "
  "the LORD shall not want any good thing."),
 ("Keep Thy Tongue from Evil (vv.11-14)",
  "Come, ye children, hearken unto me, I will teach you the fear of the LORD. The psalm turns into a "
  "lesson, and the question it poses is about wanting a good life, what man is he that desireth life, and "
  "loveth many days. The answer is four instructions and three of them concern speech, keep thy tongue "
  "from evil, and thy lips from speaking guile, depart from evil, and do good, seek peace, and pursue it. "
  "1 Peter 3:10-12 quotes the whole passage."),
 ("The Eyes of the LORD Are upon the Righteous (vv.15-18)",
  "The eyes of the LORD are upon the righteous, and his ears are open unto their cry. Then the two verses "
  "the psalm is best loved for, and they are about proximity rather than rescue, the LORD is nigh unto "
  "them that are of a broken heart, and saveth such as be of a contrite spirit. A broken heart is treated "
  "as a qualification."),
 ("Many Are the Afflictions of the Righteous (vv.19-22)",
  "Many are the afflictions of the righteous, but the LORD delivereth him out of them all. The verse "
  "concedes the number before it promises the outcome, which is the psalm's honesty. Then a clause John "
  "19:36 applies to the crucifixion, he keepeth all his bones, not one of them is broken. And the last "
  "verse ends on the same word the psalm has used throughout, none of them that trust in him shall be "
  "desolate."),
],
"psalms35": [
 ("Plead My Cause, O LORD (vv.1-10)",
  "Plead my cause, O LORD, with them that strive with me, fight against them that fight against me. The "
  "opening ten verses ask God to act as both advocate and soldier, take hold of shield and buckler, and "
  "stand up for mine help. And in the middle of it, a sentence addressed to the singer himself rather "
  "than about the enemy, say unto my soul, I am thy salvation. The imprecations are unrestrained, let them "
  "be as chaff before the wind, and let the angel of the LORD chase them, and the psalter does not "
  "apologise for them. What is asked is that the trap be turned, for without cause have they hid for me "
  "their net in a pit."),
 ("They Rewarded Me Evil for Good (vv.11-18)",
  "False witnesses did rise up against me, they laid to my charge things that I knew not. The grievance in "
  "this section is betrayal by people he had cared for, and the detail is what makes it sting: I behaved "
  "myself as though he had been my friend or brother, I bowed down heavily, as one that mourneth for his "
  "mother. He had fasted and worn sackcloth for the men now testifying against him. And the closing vow "
  "is public, I will give thee thanks in the great congregation, I will praise thee among much people."),
 ("Let Them Not Rejoice Over Me (vv.19-28)",
  "Let not them that are mine enemies wrongfully rejoice over me. The phrase without a cause occurs twice "
  "in this psalm, and John 15:25 quotes it of Jesus, they hated me without a cause. What is quoted from "
  "the opponents is a single syllable of satisfaction, they opened their mouth wide against me, and said, "
  "Aha, aha, our eye hath seen it. And the psalm ends on the opposite noise, let them shout for joy, and "
  "be glad, that favour my righteous cause, and my tongue shall speak of thy righteousness all the day "
  "long."),
],
"psalms36": [
 ("The Transgression of the Wicked (vv.1-4)",
  "The transgression of the wicked saith within my heart, that there is no fear of God before his eyes. "
  "The diagnosis is the same as Psalm 10:4 and it locates the fault in an absence rather than in an act. "
  "Then the mechanism of self-deception, for he flattereth himself in his own eyes, until his iniquity be "
  "found to be hateful, and Paul quotes the opening clause in Romans 3:18. The last verse tracks it "
  "through a day, he deviseth mischief upon his bed, so the planning happens where Psalm 4:4 recommends "
  "reflection."),
 ("Thy Mercy Is in the Heavens (vv.5-9)",
  "Thy mercy, O LORD, is in the heavens, and thy faithfulness reacheth unto the clouds. The change of "
  "subject is total and the measurements are all vertical or unfathomable, thy righteousness is like the "
  "great mountains, thy judgments are a great deep. Then a clause that widens further than most readers "
  "notice, O LORD, thou preservest man and beast. And the imagery becomes hospitality and then supply, "
  "they shall be abundantly satisfied with the fatness of thy house, for with thee is the fountain of "
  "life, in thy light shall we see light."),
 ("Let Not the Foot of Pride Come Against Me (vv.10-12)",
  "O continue thy lovingkindness unto them that know thee, and thy righteousness to the upright in heart. "
  "The petition is for continuation rather than for a new act. Then the specific danger named, let not the "
  "foot of pride come against me, and let not the hand of the wicked remove me, which returns to the man "
  "described in the first four verses. And the psalm closes on him in the perfect tense, there are the "
  "workers of iniquity fallen, they are cast down, and shall not be able to rise."),
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
