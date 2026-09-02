#!/usr/bin/env python3
"""
Completes two books: Lamentations (4 chapters left) and 1 Corinthians (2 left).

    lamentations1 lamentations2 lamentations3 lamentations5
    1corinthians1 1corinthians13

Why Historical Context is rewritten rather than merged. These pages carry content
in three places besides the labelled fields: headless continuation paragraphs, and
on four of them a field whose label is a sentence fragment -- "Chapter 1 is an
ACROSTIC poem:", "The chapter's movement is profound:", "Structure:", "The
Corinthian Context:". All of it is worth keeping, but the source text is full of
emphatic capitals that WORKFLOW.md rules out: ACROSTIC, ORDERED, WIDOW, UNCLEAN,
DIVINE, TRIPLE, CHOICE, RUINS, UNLESS, NOTHING.

Lowercasing those automatically is not safe here. Lamentations 2 legitimately
capitalises the Hebrew letter names PE and AYIN when noting that chapters 2 to 4
reverse them, and that is exactly the kind of word an automatic pass would ruin.
So the Historical Context body is written out in full for each page, folding in the
absorbed material by hand, and everything written is then checked against an
allow-list of capitalised words.

Skeleton corrections:
  lamentations2   10 sections consolidated to 6
  lamentations3   9 to 7, and the overlap fixed: the inherited outline had both
                  vv.21-24 and vv.22-23, so verses 22 and 23 sat in two sections.
                  Also "this I Recall" was lowercase mid-heading
  lamentations5   8 to 5
  1corinthians13  the labelled Structure: field was a three-part outline of
                  vv.1-3 / 4-7 / 8-13, which the sections restate

1 Corinthians 1 keeps its book-opening fields, including the page-specific
"Corinth:" and "Chapter 1 Content:".

Usage:
    python3 fold_lamentations_1corinthians.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"lamentations1": 22, "lamentations2": 22, "lamentations3": 66,
          "lamentations5": 22, "1corinthians1": 31, "1corinthians13": 13}

# Capitalised runs that are allowed to stand.
CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "NET", "WEB", "BSB", "PE", "AYIN", "III", "II"}

# Existing labels preserved above the sections, in this order. Historical Context
# is replaced by CONTEXT below where a page has one.
KEEP = {
    "lamentations1": ["Author:", "Classification:", "Key Themes:", "Historical Context:"],
    "lamentations2": ["Author:", "Classification:", "Key Themes:", "Historical Context:"],
    "lamentations3": ["Author:", "Classification:", "Key Themes:", "Historical Context:"],
    "lamentations5": ["Author:", "Classification:", "Key Themes:", "Historical Context:"],
    "1corinthians1": ["Author:", "Audience:", "Corinth:", "Purpose:",
                      "Chapter 1 Content:"],
    "1corinthians13": ["Author:", "Historical Context:"],
}

# Fields dropped because the sections or the rewritten context carry them.
DROP = {
    "lamentations1": ["Chapter 1 is an ACROSTIC poem:"],
    "lamentations3": ["The chapter&#x27;s movement is profound:"],
    "1corinthians13": ["Structure:", "The Corinthian Context:"],
}

# Added where the page has none.
ADD = {
    "1corinthians1": ("Epistle \u2014 Pauline",
      "Called saints in a divided church, factions named after their favourite "
      "teacher, baptism as a side issue, the cross as folly to those perishing, "
      "and God choosing what the world counts as nothing"),
    "1corinthians13": ("Epistle \u2014 Pauline",
      "Gifts without love reduced to nothing, love defined by what it does rather "
      "than what it feels, patience and kindness listed before anything "
      "impressive, prophecy and knowledge described as temporary, and seeing face "
      "to face rather than in a mirror"),
}

# Historical Context, rewritten to absorb the headless paragraphs and the
# fragment-labelled fields without their emphatic capitals.
CONTEXT = {
"lamentations1":
  "Jerusalem fell to Nebuchadnezzar in 586 BC after an eighteen-month siege. The "
  "temple was burned, the walls demolished, and the population killed, starved or "
  "deported. Lamentations was likely written in the immediate aftermath, while the "
  "ruins were still smoking, and the emotion in it is raw rather than reflective. "
  "Chapter 1 is an acrostic: each of its 22 verses begins with a successive letter "
  "of the Hebrew alphabet, aleph through tav. That form suggests crafted grief "
  "rather than random wailing \u2014 mourning ordered from one end of the alphabet "
  "to the other, structured enough to be written as poetry and honest enough to "
  "hold nothing back. The city is personified throughout as a woman, specifically a "
  "widow (v.1) and an unclean woman (vv.8-9). She who was great among the nations "
  "and a princess among the provinces now sits alone and pays tribute. The nations "
  "she trusted instead of God are called her lovers, and every one of them has "
  "betrayed her. The refrain that she has no comforter runs through the chapter.",
"lamentations2":
  "Chapter 2 shifts the focus from Jerusalem's grief to God's action, and the "
  "theological shock is deliberate. In the first eight verses God is repeatedly the "
  "subject of destructive verbs: he swallowed up, destroyed, cut off, burned, bent "
  "his bow, killed, poured out his fury. What chapter 1 described as catastrophe, "
  "chapter 2 attributes to God rather than to the Babylonians. This chapter is also "
  "an acrostic of 22 verses, with one notable variation: in chapters 2 to 4 the "
  "letters PE and AYIN are reversed from their usual order, which some read as the "
  "disorder of judgment reaching even the alphabet. The false prophets draw "
  "particular condemnation in v.14 \u2014 they saw false and deceptive visions and "
  "did not expose the people's iniquity, telling them what they wanted to hear "
  "rather than what they needed to. Jeremiah had warned for decades and been "
  "ignored.",
"lamentations3":
  "Chapter 3 is the structural centre of Lamentations. The book's five chapters "
  "form an A-B-C-B-A pattern with this chapter as the pivot, and it is also the "
  "longest \u2014 a triple acrostic of 66 verses, three to each Hebrew letter. "
  "That elaborate construction at the exact centre marks where the weight of the "
  "book falls: the hope is the focal point, not an afterthought. The movement "
  "within the chapter is its argument. Verses 1-18 are unrelieved despair, God "
  "having walled the speaker in and made him desolate. Verses 19-24 turn on a "
  "deliberate act of memory, \u201cthis I recall to mind, therefore have I "
  "hope\u201d. Verses 25-39 reflect on God's goodness, patience and sovereignty. "
  "Verses 40-54 call for self-examination and return, and the chapter closes in "
  "vv.55-66 with a cry for justice. The turn is not a change of circumstances but a "
  "choice about what to dwell on.",
"lamentations5":
  "Unlike chapters 1 to 4, chapter 5 is not an acrostic, though it still runs to 22 "
  "verses. Abandoning the strict form may represent a final dissolution of order: "
  "the people have lost even the capacity for structured grief, and what is left is "
  "unadorned pleading. The chapter catalogues the specific losses of the community "
  "left after the destruction \u2014 their inheritance, with land handed to "
  "foreigners; their families, fatherless and widowed; their basic resources, "
  "paying for water and wood that had been free; their labour, grinding like "
  "slaves; and their dignity, with women raped, princes hanged and elders shown no "
  "respect. The ending is one of the most debated conclusions in Scripture. "
  "\u201cTurn thou us unto thee... unless thou hast utterly rejected us\u201d can "
  "be read as a condition or as an emphatic denial, and the Hebrew supports either. "
  "Jewish liturgical practice repeats v.21 after v.22 when the book is read aloud, "
  "so that it does not end on the harder line.",
}

SECTIONS = {
"lamentations1": [
  ("Jerusalem the Widow: Alone and Weeping (vv.1-7)",
   "The book opens on a single word of grief and then a picture: the city that was "
   "full of people sits solitary, the princess become a tributary. She weeps in the "
   "night with tears on her cheeks and among all her lovers there is none to comfort "
   "her. The roads to Zion mourn because nobody walks them to the feasts, the gates "
   "are desolate, the priests sigh. The detail is civic rather than military \u2014 "
   "empty roads and quiet gates \u2014 which is how a siege looks after it ends."),
  ("Her Sin Exposed, and No Comforter (vv.8-11)",
   "The poem does not present the city only as a victim. \u201cJerusalem hath "
   "grievously sinned; therefore she is removed\u201d, and the imagery turns to "
   "uncleanness and exposure, her skirts lifted and her nakedness seen. Verse 9's "
   "\u201cshe remembereth not her last end\u201d names the failure as a refusal to "
   "think ahead. By v.11 the concern is food: the people give their treasures for "
   "meat to keep themselves alive."),
  ("The City Speaks: Is It Nothing to You? (vv.12-16)",
   "Here Jerusalem addresses passers-by directly, and the question is the most "
   "quoted line in the chapter: is it nothing to you, all ye that pass by? Behold "
   "and see if there be any sorrow like unto my sorrow. What follows is not a "
   "complaint against the Babylonians but against God \u2014 fire sent into her "
   "bones, a net spread for her feet, a yoke bound on her neck. She weeps because "
   "the comforter is far off, which is the same refrain from a different mouth."),
  ("God Is Righteous; I Have Rebelled (vv.17-22)",
   "The chapter ends with the concession that makes it more than grief: \u201cthe "
   "LORD is righteous; for I have rebelled against his commandment.\u201d The city "
   "asks to be heard rather than excused, calls her sorrow deserved, and then asks "
   "that the same day come on those who did this to her. Lament and self-accusation "
   "and a request for justice sit in the same breath, and the chapter closes with "
   "the heart faint rather than resolved."),
],
"lamentations2": [
  ("God as the Destroyer: He Hath Swallowed Up (vv.1-8)",
   "The opening verses stack up divine action without relief: he covered the "
   "daughter of Zion with a cloud, cast down his footstool, swallowed up the "
   "habitations, bent his bow like an enemy. The phrase \u201cas an enemy\u201d in "
   "v.5 is the hardest in the book \u2014 not that God permitted an enemy, but that "
   "he acted as one. Verse 8 has him stretching out a measuring line, which is a "
   "builder's tool used here for demolition."),
  ("The Silence: No Vision, No Law, No King (vv.9-10)",
   "The institutions fail one after another. The gates have sunk into the ground, "
   "the king and princes are among the Gentiles, the law is no more, and the "
   "prophets find no vision from the LORD. Every channel through which Israel "
   "expected to hear from God is closed at once. Verse 10 leaves the elders sitting "
   "on the ground in silence with dust on their heads, and the silence is the point "
   "\u2014 there is nothing left to say from any office."),
  ("Children Fainting in the Streets (vv.11-12)",
   "The poet's own body registers what he is describing: eyes failing with tears, "
   "bowels troubled, liver poured out. The cause is named without softening \u2014 "
   "the children and sucklings swoon in the streets of the city. Verse 12 records "
   "them asking their mothers for corn and wine and pouring out their souls in her "
   "bosom. It is the plainest description of famine in Scripture and it is put in "
   "the children's own words."),
  ("What Can I Say? Ruin Beyond Comparison (vv.13-14)",
   "\u201cWhat thing shall I take to witness for thee? what thing shall I liken to "
   "thee?\u201d The poet admits he has no comparison available, and calls the breach "
   "great like the sea, so that no one can heal it. Then the verdict on the "
   "prophets: they saw vanity and foolishness, and did not discover the people's "
   "iniquity. Their failure to name sin is treated as a cause of the ruin rather "
   "than a separate failing."),
  ("Enemies Mocking, and the LORD Has Done It (vv.15-17)",
   "Passers-by clap and hiss and wag their heads, quoting back the city's own "
   "reputation \u2014 is this the city that men called the perfection of beauty, the "
   "joy of the whole earth? The enemies then say plainly that they have swallowed "
   "her up. Verse 17 answers them without contradicting them: the LORD hath done "
   "that which he had devised, and fulfilled the word he commanded long ago. What "
   "the enemy claims as conquest the poet reads as prophecy kept."),
  ("Cry Out in the Night: Mothers and Children (vv.18-22)",
   "The chapter ends in instruction: let tears run down like a river, give thyself "
   "no rest, arise and cry out in the night, pour out thine heart like water before "
   "the Lord. Grief is being directed rather than merely expressed. The final verses "
   "put the worst of it into the prayer itself \u2014 women eating their children, "
   "priest and prophet slain in the sanctuary, young and old lying in the streets. "
   "The book does not look away, and it does not resolve here."),
],
"lamentations3": [
  ("The Man of Affliction: God's Rod (vv.1-18)",
   "The voice changes to a single \u201cI\u201d, and the chapter's first third is "
   "unrelieved. He has been led into darkness, his flesh and skin worn out, his "
   "bones broken, walled about so his prayer cannot pass. God is described as a bear "
   "lying in wait and a lion in secret places, and as an archer using the speaker "
   "for a target. Verse 18's \u201cmy strength and my hope is perished from the "
   "LORD\u201d is the lowest point of the book, and it is spoken by the man who is "
   "about to say the opposite."),
  ("This I Recall, Therefore Have I Hope (vv.19-24)",
   "The turn is deliberate and mechanical: remembering the affliction pushes the "
   "soul down, and then \u201cthis I recall to mind, therefore have I hope\u201d. "
   "Nothing outside has changed. What follows is the passage the book is known for "
   "\u2014 his compassions fail not, they are new every morning, great is thy "
   "faithfulness \u2014 and the point easily missed is where it is spoken from. "
   "Thomas Chisholm's 1923 hymn takes its title from v.23, but the words were first "
   "said in the ruins rather than in prosperity."),
  ("Good to Wait Quietly (vv.25-30)",
   "A short series on waiting: the LORD is good to them that wait for him and to "
   "the soul that seeks him, and it is good to bear the yoke while young. The "
   "instructions that follow are physical and unheroic \u2014 sit alone and keep "
   "silence, put the mouth in the dust, give the cheek to the one who strikes. "
   "Quietness is presented as an active posture rather than resignation, and v.29's "
   "\u201cif so be there may be hope\u201d keeps it honest."),
  ("He Does Not Afflict Willingly (vv.31-39)",
   "The theological centre of the chapter. God does not cast off for ever; though "
   "he cause grief he will have compassion; \u201che doth not afflict willingly nor "
   "grieve the children of men\u201d. The word rendered willingly is closer to from "
   "the heart, so affliction is described as something God does without it being "
   "what he delights in. Verses 37-39 press the consequence: since good and evil "
   "both come from His hand, why should a living man complain for the punishment of "
   "his sins?"),
  ("Let Us Search and Turn Again (vv.40-42)",
   "Three verses that turn from reflection to action, and the pronouns go plural "
   "for the first time in the chapter. Let us search and try our ways, and turn "
   "again to the LORD; let us lift up our heart with our hands. Then the confession "
   "without qualification: we have transgressed and rebelled, thou hast not "
   "pardoned. The self-examination is corporate, which is what makes the chapter "
   "more than a personal testimony."),
  ("Covered with a Cloud: Continuing Lament (vv.43-54)",
   "The lament resumes rather than ending, which is worth noticing \u2014 the hope "
   "of vv.22-23 does not close the subject. God has covered himself with a cloud so "
   "prayer cannot pass through, and the people are made offscouring in the midst of "
   "the nations. The images grow personal again: eyes running with rivers of water, "
   "hunted like a bird, cast into a dungeon, waters flowing over the head. Verse "
   "54's \u201cI said, I am cut off\u201d sits fifty verses after the same "
   "sentiment."),
  ("Thou Drewest Near: The Cry for Justice (vv.55-66)",
   "The last section is answered prayer reported in the past tense: I called upon "
   "thy name out of the low dungeon, thou heardest my voice, thou drewest near in "
   "the day that I called, thou saidst fear not. On the strength of that the speaker "
   "asks God to judge his cause and to repay those who devised against him. The "
   "chapter ends on a request for justice rather than on comfort, which keeps the "
   "hope in it from being sentimental."),
],
"lamentations5": [
  ("Remember, O LORD, What Is Come Upon Us (vv.1-3)",
   "The final chapter is a communal prayer and it opens with a request to be seen: "
   "remember, consider, behold our reproach. The losses named first are inheritance "
   "and family \u2014 the land turned over to strangers, the houses to aliens, and "
   "a community describing itself as fatherless, with mothers as widows. The "
   "\u201cwe\u201d is unbroken through the chapter, which is what distinguishes it "
   "from the personal voice of chapter 3."),
  ("Paying for Water and Wood (vv.4-7)",
   "The detail is deliberately mundane and therefore effective: they buy their own "
   "water and pay for their own wood. Things that had been free in their own land "
   "now cost money in it. They give the hand to Egypt and Assyria to get bread, "
   "returning to the alliances the prophets had condemned. Verse 7 states the "
   "grievance that runs under the whole chapter \u2014 our fathers have sinned and "
   "are not, and we have borne their iniquities."),
  ("Servants Rule Over Us (vv.8-10)",
   "\u201cServants have ruled over us: there is none that doth deliver us out of "
   "their hand.\u201d The complaint is about order inverted rather than only about "
   "hardship. Getting bread means risking their lives because of the sword of the "
   "wilderness, so the countryside is no longer safe to cross. Verse 10's skin "
   "black like an oven describes the physical effect of prolonged hunger."),
  ("Women Ravished, Elders Dishonoured (vv.11-18)",
   "The catalogue of indignity is specific: women ravished in Zion, princes hanged, "
   "elders shown no respect, young men grinding at the mill, children falling under "
   "wood they are made to carry. The elders have left the gate and the young their "
   "music, so both justice and joy have stopped. Verse 16's \u201cthe crown is "
   "fallen from our head\u201d is followed immediately by \u201cwoe unto us, that "
   "we have sinned\u201d, and the chapter ends this section with foxes walking on "
   "the desolate mountain of Zion."),
  ("Thou Remainest For Ever: Turn Us Again (vv.19-22)",
   "Against everything listed, one fixed point: thou, O LORD, remainest for ever, "
   "thy throne from generation to generation. The prayer that follows asks why God "
   "would forget for ever, and then makes its request \u2014 turn thou us unto "
   "thee, and we shall be turned; renew our days as of old. The restoration asked "
   "for is something God must do to them rather than something they undertake. The "
   "book then ends on its unresolved final line, which is why readers have argued "
   "about it ever since."),
],
"1corinthians1": [
  ("Greeting: Called to Be Saints (vv.1-3)",
   "Paul addresses a church he is about to spend sixteen chapters correcting as "
   "\u201cthe church of God which is at Corinth\u201d, sanctified and called to be "
   "saints. The status is stated before any of the problems, and it is not "
   "presented as flattery or as something they have earned. He also links them with "
   "all who call on the name of Jesus in every place, which quietly answers a "
   "congregation inclined to think of itself as its own centre."),
  ("Thanksgiving: Enriched in Everything (vv.4-9)",
   "The thanksgiving is genuine and specific: they come behind in no gift, they are "
   "enriched in all utterance and knowledge. Given what chapters 12 to 14 will say "
   "about how those gifts were being used, the commendation is striking \u2014 Paul "
   "does not dispute that they are gifted. Verse 9 grounds their standing in God's "
   "faithfulness rather than their own, which is the assumption the rest of the "
   "letter argues from."),
  ("The Divisions: I Am of Paul (vv.10-17)",
   "The first problem, reported by Chloe's household: factions naming themselves "
   "after Paul, Apollos, Cephas and Christ. Paul's questions in v.13 refuse to take "
   "the flattery \u2014 is Christ divided, was Paul crucified for you, were you "
   "baptized in Paul's name? He is glad he baptized almost none of them, which is a "
   "deliberate deflation of a status contest. Verse 17 states his commission as "
   "preaching rather than baptizing, and \u201cnot with wisdom of words\u201d opens "
   "the argument that follows."),
  ("The Preaching of the Cross Is Foolishness (vv.18-21)",
   "The cross divides its hearers into two groups by their response to it: "
   "foolishness to them that perish, the power of God to those being saved. Paul "
   "quotes Isaiah on destroying the wisdom of the wise, then asks where the scribe "
   "and the disputer are now. Verse 21's claim is that God chose the method "
   "deliberately \u2014 since the world by wisdom did not know Him, it pleased God "
   "to save by what preaching looks like from outside, which is foolishness."),
  ("Christ Crucified: Stumbling Block and Foolishness (vv.22-25)",
   "The two audiences are named with what each wants: Jews require a sign, Greeks "
   "seek wisdom. A crucified messiah fails both tests at once, being an offence to "
   "the first and absurd to the second. To those called it is the power and wisdom "
   "of God. Verse 25's \u201cthe foolishness of God is wiser than men\u201d is "
   "rhetorical rather than literal \u2014 there is no foolishness in God, and the "
   "comparison concedes the world's terms in order to overturn them."),
  ("God Chooses the Weak Things (vv.26-29)",
   "\u201cBehold your calling\u201d is an argument from the congregation's own "
   "membership: not many wise, not many mighty, not many noble. Paul is pointing at "
   "the room. God chose the foolish, the weak, the base and despised, and things "
   "which are not, to bring to nothing the things that are. The stated purpose in "
   "v.29 is that no flesh should glory in His presence, which returns to the "
   "factions the chapter began with."),
  ("Christ Made unto Us Wisdom (vv.30-31)",
   "The chapter closes by relocating everything the Corinthians had been competing "
   "over: Christ is made unto us wisdom, righteousness, sanctification and "
   "redemption. All four are received rather than achieved. The quotation that ends "
   "it \u2014 he that glorieth, let him glory in the Lord \u2014 leaves the "
   "boasting instinct intact while changing its object."),
],
"1corinthians13": [
  ("Without Love I Am Nothing (vv.1-3)",
   "The chapter opens by pricing the gifts the Corinthians most admired and finding "
   "them worthless on their own. Tongues of men and angels without love is sounding "
   "brass. Prophecy, all mysteries, all knowledge, faith to move mountains "
   "\u2014 without love, \u201cI am nothing\u201d. Giving away all his goods and "
   "giving his body to be burned still profits nothing. The Corinthians were "
   "preoccupied with spectacular gifts, especially tongues, while treating one "
   "another with contempt, and Paul's answer is not to rank the gifts but to say "
   "what they amount to without love."),
  ("What Love Does and Does Not Do (vv.4-7)",
   "Love is defined by verbs rather than feelings, and the list is unromantic. It "
   "suffers long, is kind, envies not, vaunts not itself, is not puffed up, does not "
   "behave itself unseemly, seeks not her own, is not easily provoked, thinks no "
   "evil. Read against the letter, nearly every item names something Corinth was "
   "doing wrong \u2014 the boasting, the self-seeking at the Lord's table, the "
   "lawsuits. Verse 7's four clauses all begin with \u201call things\u201d, which is "
   "where the definition stops being a checklist."),
  ("Love Never Fails; Gifts Cease (vv.8-10)",
   "Charity never fails, and then three things that do: prophecies fail, tongues "
   "cease, knowledge vanishes away. They are described as temporary by nature rather "
   "than as defective. The reason given is partiality \u2014 we know in part and "
   "prophesy in part \u2014 and when that which is perfect is come, the partial is "
   "done away. Whether that refers to the return of Christ or to something earlier "
   "has been argued for centuries; the argument itself does not depend on which."),
  ("When I Became a Man (v.11)",
   "A single verse of illustration, and it is pointed. Speaking, understanding and "
   "thinking as a child were appropriate then and are not now. Paul has already "
   "called the Corinthians babes in 3:1, so the analogy is not neutral. Growing up "
   "is presented as putting away rather than adding on, which is what he is asking "
   "of a church proud of what it had accumulated."),
  ("Through a Glass, Darkly (vv.12-13)",
   "The mirror image describes present knowledge, and ancient mirrors were polished "
   "metal giving a real but imperfect reflection. Now we see in a riddle; then face "
   "to face. \u201cThen shall I know even as also I am known\u201d makes the future "
   "knowing mutual. The chapter ends by naming three things that remain \u2014 "
   "faith, hope, charity \u2014 and then ranking them, which after two chapters "
   "about gifts is the only ranking Paul is willing to make."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def check_caps(page, where, text):
    bad = {w for w in CAPS.findall(text) if w not in CAPS_OK}
    return [f"{page}: emphatic capitals {sorted(bad)} in {where}"] if bad else []


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        keep_order = KEEP[page]
        dropped_want = DROP.get(page, [])
        fields, dropped, headless = {}, [], 0
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in keep_order:
                fields[name] = rest
            elif name is not None and name in dropped_want:
                dropped.append(name)
            elif name is None:
                headless += 1
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in keep_order:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in dropped_want:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")

        if page in CONTEXT:
            fields["Historical Context:"] = CONTEXT[page]
            notes.append(f"{page}: Historical Context rewritten, absorbing "
                         f"{headless} headless paragraph(s)"
                         + (f" and {len(dropped)} fragment field(s)" if dropped else ""))
        elif headless:
            problems.append(f"{page}: {headless} headless item(s) with nowhere to go")

        sections = SECTIONS[page]
        covered = set()
        for head, prose in sections:
            problems += check_caps(page, f"section {head!r}", prose)
            if "*" in prose:
                problems.append(f"{page}: markdown asterisk in {head!r}")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps an earlier section "
                                    f"at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for want in keep_order:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        if page in ADD:
            genre, themes = ADD[page]
            problems += check_caps(page, "Key Themes", themes)
            parts.append(ITEM.format(label="Classification:", body=genre) + "\n")
            parts.append(ITEM.format(label="Key Themes:", body=themes) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if "auth-sublist" in new:
            problems.append(f"{page}: sublist survived")
            continue
        planned[path] = new

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
