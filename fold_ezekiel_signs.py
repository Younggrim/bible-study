#!/usr/bin/env python3
"""
Ezekiel 12 to 19: the signs, the false prophets, and the parables of the vine. Eight
pages, 210 verses. The inherited sublists on all eight are gapless outlines, so they
are folded rather than preserved, and the labels are rewritten into the corpus's
nominal style.

Two of these chapters answer objections rather than announce judgment, and that is
worth noticing because it tells us what the exiles were actually saying. At 12:21-28 the
complaint is not that the prophet is wrong but that he is not urgent, every vision
faileth and the vision that he seeth is for many days to come. At 18:2 and 18:25 the
complaint is that the arrangement is unjust, the fathers have eaten sour grapes, and
the way of the Lord is not equal. Jeremiah 31 records the same proverb being answered
the same way at the same time.

ezekiel16 is the longest chapter in the book and carries its most sustained metaphor.
The section on verses 15 to 34 says plainly that the sexual imagery is meant to shock,
because a note that does not say so leaves a reader wondering whether the page has
misread the text.

Usage:
    python3 fold_ezekiel_signs.py [--check]
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
"ezekiel12": [
 ("The Exile's Baggage, and the Hole in the Wall (vv.1-7)",
  "The audience is described before the sign is given, and the description explains why a sign is "
  "needed at all, thou dwellest in the midst of a rebellious house, which have eyes to see, and see "
  "not, they have ears to hear, and hear not. So he is told to act it out. Prepare stuff for "
  "removing, and remove by day in their sight, then dig through the wall and carry the bundle out "
  "through the hole at evening, with his face covered so that he cannot see the ground. Every detail "
  "will be decoded in the next section, and the point of doing it in public over two days is that "
  "people who will not listen to a sentence may still watch a man move house."),
 ("The Prince Shall Not See the Land (vv.8-16)",
  "In the morning the interpretation comes, and it begins by naming the prophet himself as the sign, "
  "I am your sign. The decoding is exact: the prince that is among them shall bear upon his shoulder "
  "in the twilight, and shall go forth, they shall dig through the wall to carry out thereby. Then "
  "the clause that looks like a contradiction, I will bring him to Babylon, yet shall he not see it, "
  "though he shall die there. Both halves are literal. 2 Kings 25 records Zedekiah captured near "
  "Jericho, his sons killed in front of him, his eyes put out at Riblah, and then the journey to "
  "Babylon in chains. He reached the city and never saw it."),
 ("Eating Bread with Quaking (vv.17-20)",
  "A second and much shorter sign, and this one is about manner rather than about action. Eat thy "
  "bread with quaking, and drink thy water with trembling and with carefulness. The interpretation "
  "applies it to the people still in Jerusalem, who will eat their bread with carefulness and drink "
  "their water with astonishment, and it states the reason in terms of the land rather than of the "
  "diners, that the land may be desolate from all that is therein."),
 ("The Proverb About Vision Failing (vv.21-25)",
  "What is that proverb that ye have in the land of Israel, saying, The days are prolonged, and "
  "every vision faileth. It is the complaint of people who have heard warnings for a generation and "
  "watched nothing happen, and it is answered by cancelling the saying rather than by arguing with "
  "it, I will make this proverb to cease. Against it stands a promise about timing in the second "
  "person, the days are at hand, and the effect of every vision, and for I am the LORD, I will "
  "speak, and the word that I shall speak shall come to pass."),
 ("The Other Proverb, About the Distant Future (vv.26-28)",
  "The second objection is subtler than the first and harder to refute, the vision that he seeth is "
  "for many days to come, and he prophesieth of the times that are far off. Nobody is calling the "
  "prophet a liar. They are agreeing with him in a way that costs nothing. The reply is a single "
  "clause repeated for emphasis, there shall none of my words be deferred, but the word which I have "
  "spoken shall be done. What makes the exchange striking is where it sits: two chapters after the "
  "glory has been described leaving the temple, the question being argued is still whether any of "
  "this is urgent."),
],
"ezekiel13": [
 ("Prophets Who Follow Their Own Spirit (vv.1-7)",
  "Woe unto the foolish prophets, that follow their own spirit, and have seen nothing. The charge is "
  "not corruption but emptiness, and the images are of scavenging and of neglected structural work: "
  "they are like the foxes in the deserts, and ye have not gone up into the gaps, neither made up the "
  "hedge for the house of Israel to stand in the battle. The formula they use is quoted against "
  "them, saying, The LORD saith, and the LORD hath not sent them. What they are accused of is "
  "supplying a sentence in God's name to fill a silence."),
 ("The Untempered Mortar, and the Wall That Falls (vv.8-16)",
  "The metaphor is builders' work. One party puts up a wall and the prophets daub it with untempered "
  "mortar, a coating that hides the joints and holds nothing. The weather is then described in three "
  "stages, an overflowing shower, great hailstones, and a stormy wind to rend it, and the outcome "
  "includes the decorators, it shall fall, and ye shall be consumed in the midst thereof. The charge "
  "is stated in one clause and it is the most quoted line in the chapter, they have seen visions of "
  "peace for her, and there is no peace. Cosmetic work on a structure that will not stand is the "
  "specific offence."),
 ("The Women with Pillows and Kerchiefs (vv.17-23)",
  "The oracle turns to the daughters of thy people, which prophesy out of their own heart, and "
  "describes a practice the Old Testament nowhere else mentions: sewing pillows to all armholes and "
  "making kerchiefs upon the head of every stature, to hunt souls. What the articles were and how "
  "they were used is not recoverable, and honest commentary says so. Two things about the trade are "
  "clear from the text itself. It was paid, and cheaply, ye have polluted me among my people for "
  "handfuls of barley and for pieces of bread. And its effect was to reverse who felt safe, to slay "
  "the souls that should not die, and to save the souls alive that should not live, so it was "
  "producing confidence in the wrong people."),
],
"ezekiel14": [
 ("Elders with Idols in Their Hearts (vv.1-5)",
  "Certain of the elders of Israel come and sit before the prophet, which is the posture of men "
  "seeking a word, and the reply is about where their idolatry is located, these men have set up "
  "their idols in their heart, and put the stumblingblock of their iniquity before their face. There "
  "is no shrine to point at. They have come to consult a prophet of the LORD while carrying "
  "something else internally, and the question put back is a refusal, should I be enquired of at all "
  "by them. What follows is more unsettling than a refusal, I the LORD will answer him that cometh "
  "according to the multitude of his idols."),
 ("Turn Yourselves from Your Idols (vv.6-8)",
  "The call is given in the plainest form it takes in this book, repent, and turn yourselves from "
  "your idols, and turn away your faces from all your abominations. The alternative is stated in "
  "terms of visibility, I will set my face against that man, and will make him a sign and a proverb, "
  "and I will cut him off from the midst of my people. Being made into a cautionary saying is "
  "treated as part of the penalty."),
 ("The Prophet Who Is Deceived (vv.9-11)",
  "And if the prophet be deceived when he hath spoken a thing, I the LORD have deceived that "
  "prophet. It is one of the hardest sentences in the prophets and it belongs beside the lying "
  "spirit of 1 Kings 22 and 2 Chronicles 18. Two things keep it from being arbitrary. The liability "
  "is shared and stated, they shall bear the punishment of their iniquity, the punishment of the "
  "prophet shall be even as the punishment of him that seeketh unto him, so the man who went looking "
  "for the answer he wanted is not a victim. And the purpose given is corrective rather than "
  "punitive, that the house of Israel may go no more astray from me."),
 ("Noah, Daniel and Job Could Not Deliver Them (vv.12-20)",
  "Four judgments are put as cases in turn, famine, evil beasts, the sword, pestilence, and each one "
  "carries the same clause, though Noah, Daniel, and Job were in it, they should deliver but their "
  "own souls by their righteousness. The three names are chosen carefully. Each man is remembered for "
  "coming through a catastrophe, one by ark, one in a foreign court, one in his own body, and each "
  "is from a different era, and not one of them can extend that survival to another person, they "
  "shall deliver neither son nor daughter. The mention of Daniel is one of the very few outside his "
  "own book and shows the name was already proverbial for righteousness under pressure."),
 ("Yet a Remnant Brought Forth (vv.21-23)",
  "How much more when I send my four sore judgments upon Jerusalem, and then the turn, yet, behold, "
  "therein shall be left a remnant that shall be brought forth, both sons and daughters. The comfort "
  "offered is of an unusual kind. It is not that the survivors will prosper but that seeing them "
  "will explain the judgment, ye shall see their way and their doings, and ye shall be comforted "
  "concerning the evil that I have brought upon Jerusalem, and ye shall know that I have not done "
  "without cause all that I have done. What is promised to the exiles is understanding."),
],
"ezekiel15": [
 ("What Is the Vine Branch Good For (vv.1-3)",
  "The oracle opens as a question about timber, and the shift is the whole point. Israel is the vine "
  "in Isaiah 5 and Psalm 80, where the question is always about fruit. Here it is about the wood, "
  "what is the vine tree more than any tree, shall wood be taken thereof to do any work, or will men "
  "make a pin of it to hang any vessel thereon. Vine wood is crooked, soft and useless for building, "
  "and everyone hearing this knew it. A vine that is not bearing has no fallback value."),
 ("Only Fit for Burning (vv.4-5)",
  "The answer follows from the question, it is cast into the fire for fuel, and the description of "
  "the burning is deliberately thorough, the fire devoureth both the ends of it, and the midst of it "
  "is burned. Then the argument closes on itself, when it was whole, it was meet for no work, how "
  "much less shall it be meet yet for any work, when the fire hath devoured it. Something already "
  "useless does not become useful by being damaged."),
 ("Jerusalem as the Burnt Wood (vv.6-8)",
  "As the vine tree among the trees of the forest, so will I give the inhabitants of Jerusalem, and "
  "then a sentence about repeated judgment, they shall go out from one fire, and another fire shall "
  "devour them. The reason is given once, because they have committed a trespass. Eight verses, one "
  "image, no promise attached and no remnant mentioned: this is the shortest oracle in the book and "
  "the one with the least relief in it, and its placement between the intercession chapters on "
  "either side is what makes it land."),
],
"ezekiel16": [
 ("The Abandoned Infant, and Canaanite Parentage (vv.1-5)",
  "The chapter opens with an insult that has a legal point inside it, thy birth and thy nativity is "
  "of the land of Canaan, thy father was an Amorite, and thy mother an Hittite. Jerusalem is being "
  "told it has no claim by descent, which cuts against the whole argument from ancestry that the "
  "city was relying on. Then the condition it was found in, described in the vocabulary of "
  "midwifery: the navel not cut, not washed, not salted, not swaddled, and cast out in the open field "
  "to the loathing of thy person. No eye pitied thee."),
 ("Live, in Thy Blood (vv.6-7)",
  "Two verses, and the operative word is repeated, I said unto thee when thou wast in thy blood, "
  "Live, yea, I said unto thee when thou wast in thy blood, Live. Nothing is done for the child "
  "except that it is told to survive, and it does, I have caused thee to multiply as the bud of the "
  "field, and thou art come to excellent ornaments. The last clause keeps the scene from turning "
  "sentimental, thou wast naked and bare."),
 ("The Covenant, the Clothing and the Renown (vv.8-14)",
  "The imagery moves from rescue to marriage, I spread my skirt over thee, and covered thy "
  "nakedness, yea, I sware unto thee, and entered into a covenant with thee. What follows is an "
  "inventory of gifts, and it is detailed because the detail will be reversed later: the washing and "
  "anointing, broidered work, shoes of badgers' skins, fine linen and silk, bracelets, a chain, a "
  "jewel on the forehead, earrings and a beautiful crown. Then reputation, thy renown went forth "
  "among the heathen for thy beauty, with the source of it named in the same sentence, for it was "
  "perfect through my comeliness which I had put upon thee. Every item in the list arrived as a "
  "present."),
 ("The Gifts Turned into Payment (vv.15-34)",
  "The turn is stated in one clause, but thou didst trust in thine own beauty, and playedst the "
  "harlot because of thy renown, and then the gifts of the previous section are traced item by item "
  "into their new use: the garments become hangings for high places, the jewels become images, the "
  "oil and incense are set before them, and worst, the children are given, thou hast slain my "
  "children, and delivered them to cause them to pass through the fire. The foreign alliances with "
  "Egypt, Assyria and Chaldea are described in the same terms as the idolatry, because the book "
  "treats them as the same act of dependence. The block ends on an inversion that is the sharpest "
  "thing in it, she pays instead of being paid, thou hast given thy gifts to all thy lovers, "
  "therefore contrary is it in thee from other women. This is the most sustained metaphor in the "
  "prophets and the most brutal, and the sexual language is meant to shock rather than to titillate; "
  "some Jewish tradition restricted the chapter's public reading for exactly that reason."),
 ("The Sentence, Carried Out by Those She Paid (vv.35-43)",
  "The judgment is constructed as an undoing. I will gather all thy lovers, and will discover thy "
  "nakedness unto them, so the instruments of the sentence are the partners of the offence. Then the "
  "gifts are taken back in reverse order, they shall break down thine eminent place, and strip thee "
  "also of thy clothes, and shall take thy fair jewels, and leave thee naked and bare, which returns "
  "her precisely to the condition of verse 7. The legal frame is stated too, I will judge thee as "
  "women that break wedlock and shed blood are judged. The reason given at the end is not anger "
  "alone, because thou hast not remembered the days of thy youth."),
 ("Worse Than Samaria, Worse Than Sodom (vv.44-52)",
  "The proverb is quoted first, As is the mother, so is her daughter, and then the family is drawn "
  "out: the elder sister is Samaria, the younger is Sodom. This section contains the definition of "
  "Sodom's guilt that gets cited most often and is most often overlooked, this was the iniquity of "
  "thy sister Sodom, pride, fulness of bread, and abundance of idleness was in her and in her "
  "daughters, neither did she strengthen the hand of the poor and needy. And the comparison is "
  "pressed to its limit, thou hast justified thy sisters in all thine abominations, that is, "
  "Jerusalem's conduct has made the two byword cities look defensible."),
 ("The Everlasting Covenant, and Remembering with Shame (vv.53-63)",
  "The restoration is stated with the sisters included, when I shall bring again their captivity, "
  "the captivity of Sodom and her daughters, and the captivity of Samaria and her daughters, then "
  "will I bring again the captivity of thy captives. The purpose attached to it is not celebration, "
  "that thou mayest bear thine own shame, and mayest be confounded. And then the ground of the whole "
  "thing, which owes nothing to the preceding sixty verses, nevertheless I will remember my covenant "
  "with thee in the days of thy youth, and I will establish unto thee an everlasting covenant. The "
  "phrase not by thy covenant makes the asymmetry explicit. A chapter that opened by denying "
  "Jerusalem any claim of descent ends by giving her a promise she has no claim to either, and the "
  "last note is about memory, that thou mayest remember, and be confounded, and never open thy mouth "
  "any more."),
],
"ezekiel17": [
 ("The Riddle of the Two Eagles and the Vine (vv.1-10)",
  "Put forth a riddle, and speak a parable, and the story is told before it is explained, which is "
  "how a riddle works. A great eagle comes to Lebanon, crops the highest branch of the cedar and "
  "carries it to a land of traffick. Then it takes seed of the land and plants it in a fruitful "
  "field, and it grows into a spreading vine of low stature whose branches turn toward the eagle "
  "that planted it. A second eagle appears, and the vine bends her roots toward him and shoots out "
  "her branches for him to water. The riddle ends in questions rather than statements, shall it "
  "prosper, shall he not pull up the roots thereof."),
 ("The Interpretation, and the Broken Oath (vv.11-21)",
  "The decoding is historical and specific. The first eagle is the king of Babylon, who took "
  "Jerusalem's king and princes in 597, and installed a man of the king's seed under a covenant and "
  "an oath. The second eagle is Egypt, and the offence is diplomatic, he rebelled against him in "
  "sending his ambassadors into Egypt, that they might give him horses and much people. What makes "
  "this more than a policy error is the way the oath is treated: it was sworn by a Judean king to a "
  "pagan emperor, and God calls it mine oath that he hath despised, and my covenant that he hath "
  "broken. Zedekiah's Egyptian negotiations are a matter of record, and Jeremiah 37 describes the "
  "Egyptian force that briefly lifted the siege and then withdrew."),
 ("The Tender Twig Planted on the Mountain (vv.22-24)",
  "The last three verses repeat the eagles' action with a different actor, I will also take of the "
  "highest branch of the high cedar, and will set it, I will plant it upon an high mountain and "
  "eminent. What grows is not a low vine but a goodly cedar, and the point of it is shelter, under "
  "it shall dwell all fowl of every wing, in the shadow of the branches thereof shall they dwell. "
  "Jesus uses the same image of a tree that the birds lodge in for the kingdom in Matthew 13. The "
  "closing line states the principle the whole parable has been arguing, I the LORD have brought "
  "down the high tree, have exalted the low tree."),
],
"ezekiel18": [
 ("The Proverb About Sour Grapes Withdrawn (vv.1-4)",
  "What mean ye, that ye use this proverb concerning the land of Israel, saying, The fathers have "
  "eaten sour grapes, and the children's teeth are set on edge. It is a complaint about inherited "
  "liability, and it was in wide enough circulation that Jeremiah 31 quotes it and answers it the "
  "same way at the same period. The reply cancels the saying, ye shall not have occasion any more to "
  "use this proverb, and replaces it with two clauses, all souls are mine, and the soul that "
  "sinneth, it shall die."),
 ("The Righteous Man Lives (vv.5-9)",
  "The first of three test cases, and the definition of a just man is given entirely as conduct, "
  "with no reference to office, descent or belief: has not eaten upon the mountains, has not defiled "
  "his neighbour's wife, has not oppressed anyone, has restored the debtor's pledge, has given his "
  "bread to the hungry and covered the naked, has not lent upon usury nor taken increase, has "
  "executed true judgment between man and man. He is just, he shall surely live."),
 ("The Wicked Son Dies (vv.10-13)",
  "The second case reverses the first, a son that is a robber, a shedder of blood, who has eaten "
  "upon the mountains, defiled his neighbour's wife, oppressed the poor and needy, and given forth "
  "upon usury. The question is put and answered in the same breath, shall he then live, he shall not "
  "live, he shall surely die, his blood shall be upon him. The father's record does not carry "
  "forward, which is the half of the principle the audience was less interested in."),
 ("The Righteous Grandson Lives (vv.14-18)",
  "The third case turns it the other way, and the crucial word is a verb of attention, if he beget a "
  "son that seeth all his father's sins which he hath done, and considereth, and doeth not such like. "
  "He shall not die for the iniquity of his father, he shall surely live. And the last clause of the "
  "section closes the door the other way as well, as for his father, he shall die in his iniquity. "
  "The three cases together rule out inherited guilt and inherited merit."),
 ("The Principle Stated (vv.19-20)",
  "The objection is anticipated, yet say ye, Why doth not the son bear the iniquity of the father, "
  "and the answer is given as a rule rather than as a case, the son shall not bear the iniquity of "
  "the father, neither shall the father bear the iniquity of the son. The righteousness of the "
  "righteous shall be upon him, and the wickedness of the wicked shall be upon him. Stated this "
  "flatly, it also rules out the comfort of borrowing someone else's standing."),
 ("The Wicked Who Turns Shall Live (vv.21-23)",
  "If the wicked will turn from all his sins that he hath committed, and keep all my statutes, he "
  "shall surely live, he shall not die. The clause that follows is more generous than the rule "
  "requires, all his transgressions that he hath committed, they shall not be mentioned unto him. "
  "And then the question that supplies the chapter's motive and is easy to read past, have I any "
  "pleasure at all that the wicked should die, saith the Lord GOD, and not that he should return "
  "from his ways, and live."),
 ("The Righteous Who Turns Shall Die (v.24)",
  "One verse for the other direction, and it is as unqualified as the previous section, when the "
  "righteous turneth away from his righteousness, and committeth iniquity, in his sin that he hath "
  "sinned, in them shall he die. Taken with verses 21 to 23 it establishes what the chapter is "
  "really arguing: the account is settled on the present state and not on the accumulated record, "
  "and that cuts both ways with the same edge."),
 ("Whose Way Is Unequal (vv.25-29)",
  "The second objection is quoted, yet ye say, The way of the Lord is not equal, which is to say not "
  "fair, and it is answered with the charge turned around, are not your ways unequal. The reasoning "
  "in between simply restates the two turnings of the preceding sections. What is worth noticing is "
  "that the objection is quoted twice, at verse 25 and again at verse 29, and answered the same way "
  "both times. The book's habit of repeating rather than developing is doing something specific "
  "here: the complaint was not going to be argued out of existence."),
 ("Turn, and Live (vv.30-32)",
  "The chapter closes on imperatives, repent, and turn yourselves from all your transgressions, and "
  "then the demand that sits in tension with the rest of the book, cast away from you all your "
  "transgressions, and make you a new heart and a new spirit. At 11:19 and again at 36:26 it is God "
  "who gives the new heart and removes the stony one. Here the same thing is commanded. Ezekiel "
  "holds both without reconciling them, which is what a preacher does rather than what a systematic "
  "theologian does, and the final line explains why it is put as an appeal, for I have no pleasure "
  "in the death of him that dieth, wherefore turn yourselves, and live ye."),
],
"ezekiel19": [
 ("The Lioness and Her First Whelp (vv.1-4)",
  "The genre is announced, take thou up a lamentation for the princes of Israel, and the funeral song "
  "opens on a question, what is thy mother, a lioness. The first cub learns to catch the prey and "
  "devours men, and then the hunt reverses, the nations also heard of him, he was taken in their pit, "
  "and they brought him with chains unto the land of Egypt. That is Jehoahaz, who reigned three "
  "months in 609 BC before Necho deposed him and took him to Egypt, as 2 Kings 23 records. The "
  "lament is being sung over a dynasty while it is still on the throne."),
 ("The Lioness and Her Second Whelp (vv.5-9)",
  "The mother waits, sees that her hope is lost, and takes another of her whelps and makes him a "
  "young lion. The pattern repeats with the same verbs, he devoured men, he knew their desolate "
  "palaces, and then the nations set against him on every side and spread their net over him, and he "
  "is taken in chains to the king of Babylon. Most read this as Jehoiachin, deported in 597, and "
  "some as Zedekiah. The purpose stated for the capture is about silence rather than about "
  "punishment, that his voice should no more be heard upon the mountains of Israel."),
 ("The Vine Plucked Up and Planted in the Wilderness (vv.10-14)",
  "The image changes from lions to a vine and the subject does not, thy mother is like a vine in thy "
  "blood, planted by the waters, fruitful and full of branches, and she had strong rods for the "
  "sceptres of them that bare rule. The reversal is described as a series of removals, plucked up in "
  "fury, cast down to the ground, the east wind drying up her fruit, the strong rods broken and "
  "withered, and the fire consuming them. Where she ends is the last detail, and now she is planted "
  "in the wilderness, in a dry and thirsty ground. Then the closing line, which repeats the opening "
  "announcement so that the chapter is framed by its own genre, this is a lamentation, and shall be "
  "for a lamentation."),
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
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if not keep:
            problems.append(f"{page}: no book fields found to preserve")
            continue
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
