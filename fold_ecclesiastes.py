#!/usr/bin/env python3
"""
Completes Ecclesiastes: all twelve chapters.

The skeletons here are the best inherited so far. Every chapter's Structure: sublist
uses compact verse ranges, covers the chapter completely, and has no overlaps -- the
first book where the checks found nothing to correct in the divisions. So the
headings are carried over as given and the bullets replaced with exposition.

One headless continuation paragraph per page, merged into Historical Context. No
emphatic capitals anywhere in the book.

Usage:
    python3 fold_ecclesiastes.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"ecclesiastes1": 18, "ecclesiastes2": 26, "ecclesiastes3": 22,
          "ecclesiastes4": 16, "ecclesiastes5": 20, "ecclesiastes6": 12,
          "ecclesiastes7": 29, "ecclesiastes8": 17, "ecclesiastes9": 18,
          "ecclesiastes10": 20, "ecclesiastes11": 10, "ecclesiastes12": 14}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Historical Context:"]

GENRE = "Wisdom Literature"

THEMES = {
"ecclesiastes1": "A thesis stated before any argument, life measured under the sun, "
  "cycles that go nowhere and are never full, and wisdom pursued to the point where it "
  "increases grief",
"ecclesiastes2": "Pleasure tested deliberately and found empty, works on a royal scale "
  "that still end in someone else's hands, wisdom conceded to be better than folly and "
  "still ending in the same grave, and a first conclusion that eating and drinking are "
  "a gift",
"ecclesiastes3": "Fourteen pairs of opposites nobody chooses, eternity set in the human "
  "heart without the ability to see the whole, injustice observed rather than explained, "
  "and death levelling man with beast",
"ecclesiastes4": "Oppression seen with no comforter, rivalry named as the engine of "
  "achievement, isolation described as misery, two better than one and three strands "
  "hard to break, and popularity that does not outlast a generation",
"ecclesiastes5": "Fewer words in God's house, vows better unmade than unkept, money "
  "that never satisfies the one who loves it, sleep as the labourer's advantage over the "
  "rich, and a portion received rather than earned",
"ecclesiastes6": "Wealth held without the capacity to enjoy it, a stillborn child called "
  "better off, appetite that outruns supply, and the question of who knows what is good "
  "left open",
"ecclesiastes7": "A funeral preferred to a feast, sorrow treated as more instructive "
  "than laughter, a warning against being either too righteous or too wicked, and a "
  "search that concludes people were made upright and have sought out inventions",
"ecclesiastes8": "Authority obeyed without illusions about it, sentences delayed until "
  "the heart is set on evil, the fear of God distinguished from outcomes, and God's work "
  "declared beyond finding out",
"ecclesiastes9": "One event happening to the righteous and the wicked alike, the living "
  "told to eat and drink and work because the dead cannot, time and chance overriding "
  "swiftness and strength, and a poor wise man whose city forgot him",
"ecclesiastes10": "A dead fly spoiling the ointment, composure recommended before a "
  "ruler's anger, hazards attached to ordinary work, a fool's own words consuming him, "
  "and a land judged by the character of its rulers",
"ecclesiastes11": "Bread cast on waters without knowing the return, sowing continued "
  "because the weather cannot be predicted, light called sweet, youth told to rejoice, "
  "and judgment named in the same breath",
"ecclesiastes12": "A creator to be remembered before the body fails, old age described "
  "through a failing household, words called goads and nails, many books declared "
  "wearying, and a whole duty stated in two clauses",
}

SECTIONS = {
"ecclesiastes1": [
  ("Title and Thesis: All Is Vanity (vv.1-2)",
   "The book announces its conclusion before making any argument. \u201cVanity of "
   "vanities\u201d is a Hebrew superlative like holy of holies, and the word is hebel -- "
   "vapour, breath, something real that cannot be held. Not worthlessness so much as "
   "insubstantiality. The speaker is called Qoheleth, the Assembler or Preacher, and "
   "identified as son of David, king in Jerusalem."),
  ("The Question: What Profit Hath a Man? (v.3)",
   "One verse frames the whole book as an accounting question: what profit hath a man of "
   "all his labour? The word is commercial, the language of a ledger. And the qualifier "
   "attached to it is the one that governs everything -- under the sun, a phrase used "
   "twenty-nine times in Ecclesiastes and nowhere else in Scripture. The investigation "
   "is deliberately conducted without appeal to what lies above it."),
  ("The Cycles of Nature (vv.4-7)",
   "Generations pass while the earth stays. The sun rises and goes down and hurries back "
   "to where it rose. The wind circles. The rivers run to the sea and the sea is not "
   "full. These are not images of reassuring order but of motion without arrival -- "
   "everything busy, nothing accumulating. The observation is accurate about the world "
   "and it is offered as a problem."),
  ("The Weariness of All Things (vv.8-11)",
   "The eye is not satisfied with seeing nor the ear with hearing, which is a statement "
   "about appetite rather than about beauty. Then the harder claim: there is no new thing "
   "under the sun, and what seems new has been forgotten rather than invented. Verse 11 "
   "says former things are not remembered and neither will these be, so the loss is of "
   "memory as much as of substance."),
  ("The Preacher's Experiment with Wisdom (vv.12-18)",
   "The method is stated plainly: he gave his heart to seek and search out by wisdom "
   "everything done under heaven. His qualifications were unmatched -- authority, wealth, "
   "and more wisdom than anyone before him in Jerusalem. The result is the verse the "
   "chapter closes on, and it is not what the pursuit promised: in much wisdom is much "
   "grief, and he that increaseth knowledge increaseth sorrow. Understanding more made "
   "it worse rather than better."),
],
"ecclesiastes2": [
  ("The Experiment with Pleasure and Works (vv.1-11)",
   "The second experiment is deliberate and well-funded: laughter, wine, houses, "
   "vineyards, gardens, pools, servants, herds, silver and gold, singers. He says he "
   "withheld nothing his eyes desired, so this is not a cautionary tale about excess "
   "half-attempted. The verdict in v.11 is delivered after looking at all of it: all was "
   "vanity and vexation of spirit, and there was no profit under the sun. The word "
   "\u201cprofit\u201d answers the ledger question of 1:3 with a nil return."),
  ("Wisdom's Advantage and Its Limit (vv.12-17)",
   "He concedes what most of the book is accused of denying: wisdom excelleth folly as "
   "light excelleth darkness. The advantage is real. Then the limit -- one event happeneth "
   "to them all, and the wise man dies as the fool does, and both are equally forgotten. "
   "Verse 17 records the effect on him: therefore I hated life. The passage is not "
   "cynicism about wisdom but grief that wisdom cannot solve the one problem that "
   "matters."),
  ("Leaving Labour to Others (vv.18-23)",
   "The complaint narrows to inheritance. Everything he built goes to a successor who did "
   "not build it and may be a fool, and he has no say in which. Verse 23 describes the "
   "cost in the meantime -- his days are sorrow and his travail grief, and his heart "
   "takes no rest in the night. A man who has everything is described as unable to "
   "sleep."),
  ("Eat, Drink, and Enjoy: from God (vv.24-26)",
   "The first of the book's enjoyment conclusions, and the turn is in the last clause "
   "rather than the advice. There is nothing better than to eat and drink and enjoy good "
   "in one's labour -- and then, this also I saw, that it was from the hand of God. What "
   "could not be extracted by effort is received as a gift. Nothing about the "
   "circumstances has changed, only where they are said to come from."),
],
"ecclesiastes3": [
  ("The Poem of Times and Seasons (vv.1-8)",
   "Fourteen pairs of opposites, the most quoted lines in the book and the most "
   "misread. Set to music in the 1960s as an anthem of variety, the poem is actually "
   "about helplessness -- nobody chooses their time to be born or die, and no one votes "
   "on when war comes. A time to kill and a time to heal sit in the same list as planting "
   "and harvest. The point is that the times are appointed and not by us."),
  ("Eternity in the Heart (vv.9-15)",
   "The question of 1:3 returns, and then the verse that most complicates the book: God "
   "hath made every thing beautiful in his time, and hath set the world -- or eternity -- "
   "in their heart, yet so that no man can find out the work of God from beginning to "
   "end. Humans are given a sense of the whole and denied the view of it. That gap is "
   "where the book's frustration actually lives, and it is described as God's doing."),
  ("The Problem of Injustice (vv.16-17)",
   "He looks at the place of judgment and finds wickedness there, which is the worst "
   "place to find it. His response is not a solution but a deferral: I said in mine "
   "heart, God shall judge the righteous and the wicked, for there is a time there for "
   "every purpose. The poem's logic of appointed times is applied to justice, which puts "
   "the resolution outside the observable world."),
  ("Man and Beast Alike (vv.18-22)",
   "The hardest passage in the chapter. Man and beast have one breath, both go to dust, "
   "and he asks who knows whether the spirit of man goes upward. The question is left "
   "open rather than answered, and the chapter's closing counsel follows from the "
   "openness rather than despite it: there is nothing better than that a man should "
   "rejoice in his own works, for that is his portion."),
],
"ecclesiastes4": [
  ("The Tears of the Oppressed (vv.1-3)",
   "He returns and considers the oppressions done under the sun, and the detail he "
   "repeats is that they had no comforter -- said twice in one verse. Power is on the "
   "side of the oppressors and nobody is on the other. His conclusion is the bleakest "
   "sentence in the book: he praised the dead more than the living, and better than both "
   "is the one never born. It is stated as an observation, not commended as a "
   "philosophy."),
  ("Rivalry and Envy (vv.4-6)",
   "Then a diagnosis of achievement itself: every work and skill comes from a man's envy "
   "of his neighbour. Excellence is credited to comparison rather than to craft. The "
   "chapter does not therefore recommend idleness -- v.5 says the fool folds his hands "
   "and eats his own flesh -- and lands instead on proportion in v.6: better a handful "
   "with quietness than both hands full with travail."),
  ("The Misery of Isolation (vv.7-8)",
   "A portrait of one man alone, without child or brother, whose eye is never satisfied "
   "and who does not ask for whom he is working. The question the passage puts is his own "
   "and he does not raise it: for whom do I labour, and bereave my soul of good? Wealth "
   "accumulated with no one to receive it is called vanity and a sore travail."),
  ("Two Are Better Than One (vv.9-12)",
   "The remedy to v.8, and it is practical rather than sentimental. If one falls the "
   "other lifts him. Two keep each other warm. One may be overpowered where two can "
   "stand. Then the line that outgrew its context: a threefold cord is not quickly "
   "broken. Read against the isolated man of the previous verses, this is the answer to "
   "a specific problem rather than a general saying about friendship."),
  ("The Vanity of Political Popularity (vv.13-16)",
   "A poor and wise child is better than an old and foolish king who will no longer be "
   "admonished. The prisoner rises to reign. And then the reversal that makes it "
   "Ecclesiastes rather than Proverbs: those who come after will not rejoice in him "
   "either. Popularity does not survive a generation, so even the good outcome is "
   "temporary."),
],
"ecclesiastes5": [
  ("Words Before God (vv.1-7)",
   "The counsel is about restraint in worship: keep thy foot, be more ready to hear than "
   "to sacrifice, and let thy words be few, for God is in heaven and thou upon earth. "
   "Vows get the sharpest treatment -- better not to vow than to vow and not pay, and do "
   "not tell the priest it was a mistake. Verse 7 closes with fear God, which is the "
   "book's own answer arriving early and briefly."),
  ("The Vanity of Wealth (vv.8-17)",
   "Oppression is traced up through the officials to the king and left there. Then the "
   "observations on money that have never needed updating: he that loveth silver shall "
   "not be satisfied with silver, and when goods increase so do those who eat them. "
   "Verse 12 is the sharpest -- the sleep of a labouring man is sweet whether he eats "
   "little or much, but abundance will not let a rich man sleep. He also notes riches "
   "lost by mishandling, and a man leaving as naked as he came."),
  ("Receive Your Portion from God (vv.18-20)",
   "The third enjoyment conclusion, and it goes further than the earlier two. Eating, "
   "drinking and finding good in labour is called a man's portion, and then both the "
   "wealth and the power to enjoy it are named as God's gift -- the capacity as well as "
   "the goods. Verse 20 is the most peaceful sentence in the book: God answereth him in "
   "the joy of his heart, so he shall not much remember the days of his life."),
],
"ecclesiastes6": [
  ("Wealth Without Enjoyment (vv.1-6)",
   "The evil described is specific and modern: a man given riches, wealth and honour who "
   "lacks nothing he desires, and God does not give him power to enjoy it, so a stranger "
   "eats it. The chapter says a stillborn child is better off, and argues it -- the child "
   "never saw the sun and has rest, while this man lived long and found no good. Longevity "
   "without enjoyment is counted as loss rather than gain."),
  ("The Insatiability of Desire (vv.7-9)",
   "All a man's labour is for his mouth, and yet the appetite is not filled. The wise "
   "have no advantage over the fool here, since hunger does not respect wisdom. Verse 9's "
   "counsel is characteristically modest: better is the sight of the eyes than the "
   "wandering of the desire -- what is in front of you rather than what you are reaching "
   "for."),
  ("Who Knows What Is Good? (vv.10-12)",
   "The chapter ends on limits. Whatever exists has already been named, and a man cannot "
   "contend with one mightier than he. Then the question the second half of the book keeps "
   "returning to: who knoweth what is good for man in this life? Nobody can tell him what "
   "shall be after him under the sun. The ignorance is not remedied, and the following "
   "chapters give counsel inside it rather than resolving it."),
],
"ecclesiastes7": [
  ("Better Than: The Value of Sorrow (vv.1-12)",
   "A run of comparisons that invert the obvious. The day of death is better than the day "
   "of birth, the house of mourning better than the house of feasting, rebuke better than "
   "a song, and sorrow better than laughter because by it the heart is made better. The "
   "argument is that a funeral tells the truth about the human condition and a party does "
   "not. Verse 10 warns against nostalgia -- do not ask why the former days were better -- "
   "which is unusual counsel in wisdom literature."),
  ("Balanced Living Under God's Sovereignty (vv.13-18)",
   "Consider the work of God: what he hath made crooked, no man can make straight. In the "
   "day of prosperity be joyful, in adversity consider, for God has set the one over "
   "against the other. Then the passage most often quoted out of context: be not righteous "
   "over much, and be not over much wicked. It is not counsel toward mediocrity but "
   "against self-righteous excess and reckless folly alike, and v.18 grounds it in the "
   "fear of God."),
  ("The Strength and Limits of Wisdom (vv.19-22)",
   "Wisdom strengthens the wise more than ten mighty men strengthen a city, which is a "
   "high claim. It sits immediately beside v.20 -- there is not a just man upon earth that "
   "doeth good and sinneth not. Then a practical note on hearing yourself criticised: do "
   "not listen for what servants say of you, for you have said the same of others."),
  ("Made Upright, Seeking Inventions (vv.23-29)",
   "He says he proved all this by wisdom and it was still far from him, and describes "
   "searching and not finding. The passage about the woman in vv.26-28 is the most "
   "difficult in the book, and it is reporting his search rather than issuing a doctrine "
   "-- he says he did not find what he was looking for. The conclusion he does reach is "
   "v.29: God hath made man upright, but they have sought out many inventions. The fault "
   "is located in human ingenuity rather than in the design."),
],
"ecclesiastes8": [
  ("Wisdom Under Authority (vv.1-9)",
   "Practical counsel for living near power without illusions about it. Keep the king's "
   "commandment, do not be hasty to leave his presence, and be aware that where the word "
   "of a king is there is power and no one can say to him what doest thou. Verse 8's four "
   "clauses widen it -- no man has power over the spirit, over the day of death, over "
   "war, or to be delivered by wickedness. Authority is real and also bounded."),
  ("The Problem of Delayed Justice (vv.10-14)",
   "The observation is exact and uncomfortable: because sentence against an evil work is "
   "not executed speedily, the heart of men is fully set in them to do evil. Delay is "
   "named as a cause of wickedness rather than merely a frustration. He then holds two "
   "things together without reconciling them -- it shall be well with them that fear God, "
   "and there are just men to whom it happens according to the work of the wicked. He "
   "calls the second one vanity and does not withdraw the first."),
  ("Eat, Drink, and Be Merry (v.15)",
   "The fourth enjoyment conclusion, and by now the refrain has weight behind it. Placed "
   "directly after the injustice he has just described, commending mirth is not evasion "
   "but the counsel of someone who has looked at the alternative and found nothing "
   "better under the sun."),
  ("God's Work Not Found Out (vv.16-17)",
   "He applied his heart to know wisdom and to see the business done on the earth, and "
   "records what the effort produced: that a man cannot find out the work of God, though "
   "he labour to seek it and go without sleep. Even if a wise man says he knows it, he "
   "cannot find it. The chapter ends by naming the limit rather than lamenting it."),
],
"ecclesiastes9": [
  ("One Event unto All (vv.1-6)",
   "The righteous and the wicked, the clean and the unclean, the one who sacrifices and "
   "the one who does not -- one event happeneth to them all, and he calls this an evil "
   "under the sun. Verse 4 offers the one advantage the living hold: a living dog is "
   "better than a dead lion. The dead know nothing and have no more portion in anything "
   "done under the sun, which is the premise the next section builds its counsel on."),
  ("Go Thy Way, Eat Thy Bread (vv.7-10)",
   "The most vigorous passage in the book. Eat with joy, drink with a merry heart, wear "
   "white, keep oil on your head, live joyfully with the wife you love, and whatever your "
   "hand finds to do, do it with your might. The reason given is the one from the "
   "previous section -- there is no work nor device nor knowledge in the grave where thou "
   "goest. Mortality is the argument for engagement rather than for withdrawal."),
  ("Time and Chance (vv.11-12)",
   "The race is not to the swift nor the battle to the strong, and bread does not "
   "reliably go to the wise. Time and chance happeneth to them all. The birds and fishes "
   "of v.12 are taken suddenly in a net, and men are said to be taken the same way. "
   "Competence improves the odds and does not settle them, which is a harder thing to say "
   "than either fatalism or confidence."),
  ("The Poor Wise Man (vv.13-18)",
   "A small city besieged by a great king is delivered by one poor wise man, and no man "
   "remembered him. That is the whole parable, and it is offered as an example of wisdom "
   "he says he saw. The closing lines hold the tension: wisdom is better than strength, "
   "and the poor man's words are not heard. Both are said to be true at once."),
],
"ecclesiastes10": [
  ("A Dead Fly in the Ointment (vv.1-3)",
   "The image is precise: dead flies cause the apothecary's ointment to stink, so a "
   "little folly ruins a reputation built on wisdom and honour. Proportion is the point -- "
   "the quantity of folly needed is small. Verse 3 adds that a fool's lack of sense "
   "announces itself as he walks, so the ruin is not even discreet."),
  ("Composure Before a Ruler (vv.4-7)",
   "If the ruler's spirit rises against you, do not leave your place, for yielding "
   "pacifies great offences. Then an observation on inverted order: servants on horseback "
   "and princes walking, folly set in high places. It is reported as something he saw "
   "rather than explained, which is the chapter's habit."),
  ("The Hazards of Work (vv.8-11)",
   "A run of occupational risks -- digging a pit and falling in, breaking a hedge and "
   "being bitten, cleaving wood and being hurt. Then the argument for skill: if the iron "
   "is blunt he must use more strength, therefore wisdom is profitable. Sharpening the "
   "axe is presented as wisdom in its most ordinary form, and the serpent charmer of v.11 "
   "shows that timing matters as much as technique."),
  ("The Fool's Words (vv.12-15)",
   "The words of a wise man's mouth are gracious, but a fool's lips swallow himself. His "
   "talk begins in foolishness and ends in mischievous madness, and he multiplies words "
   "about a future he cannot know. Verse 15 has him wearied by his own labour and unable "
   "to find the way to the city, which is folly failing at the simplest task."),
  ("Good and Bad Governance (vv.16-20)",
   "Woe to the land whose king is a child and whose princes eat in the morning; blessed "
   "is the land whose king is noble and whose princes eat in due season. Then slothfulness "
   "letting the building decay, and money answering all things. The chapter closes with a "
   "caution about speech that has outlived its era: curse not the king, no not in thy "
   "thought, for a bird of the air shall carry the voice."),
],
"ecclesiastes11": [
  ("Cast Thy Bread upon the Waters (vv.1-2)",
   "Two verses of counsel about acting under uncertainty. Cast thy bread upon the waters, "
   "for thou shalt find it after many days -- generosity or venture sent out without a "
   "guaranteed return. Then give portions to seven and also to eight, because you do not "
   "know what evil shall be upon the earth. Diversification argued from ignorance rather "
   "than from confidence."),
  ("He That Observeth the Wind Shall Not Sow (vv.3-6)",
   "The clouds empty themselves and the tree falls where it falls, and none of it waits "
   "for your understanding. The farmer who watches the weather too closely never sows and "
   "never reaps. Verse 5 makes the ignorance explicit -- you do not know the way of the "
   "spirit or how bones grow in the womb, so you will not know the works of God. The "
   "conclusion is to sow morning and evening, because you cannot tell which will prosper."),
  ("Rejoice, and Remember Judgment (vv.7-10)",
   "Light is sweet and it is pleasant to behold the sun. The young are told to rejoice, "
   "let the heart cheer, walk in the sight of the eyes -- and then, in the same sentence, "
   "know that God will bring it into judgment. The two are not set against each other. "
   "Verse 10's counsel to put away sorrow leads directly into chapter 12's remember now "
   "thy Creator, so the enjoyment and the accounting belong to the same instruction."),
],
"ecclesiastes12": [
  ("Remember Now Thy Creator (vv.1-2)",
   "The urgency is in the timing: remember now thy Creator in the days of thy youth, "
   "while the evil days are not yet come. It continues chapter 11's address to the young "
   "without a break. Verse 2's darkening of the sun, moon and stars, and clouds returning "
   "after the rain, begins the allegory -- these are not cosmic events but the "
   "description of a body starting to fail."),
  ("The Allegory of Aging (vv.3-7)",
   "One of the most sustained metaphors in Scripture, and every image is a body. The "
   "keepers of the house tremble, the strong men bow, the grinders cease because they are "
   "few, those that look out of the windows are darkened -- arms shaking, legs weakening, "
   "teeth lost, eyesight going. The almond tree flourishes as white hair, the grasshopper "
   "is a burden, mourners go about the streets. Then the silver cord loosed and the golden "
   "bowl broken, and dust returning to the earth while the spirit returns to God who gave "
   "it. The chapter names the destination as well as the decline."),
  ("The Epilogue (vv.8-12)",
   "The thesis of 1:2 returns unchanged -- vanity of vanities -- so the book does not "
   "revoke its own premise. Then a note on the writing itself: he sought out acceptable "
   "words and words of truth, and his sayings are goads and nails, things that prod and "
   "things that fasten. Verse 12's line about many books and weariness of the flesh has "
   "been quoted by readers ever since, usually with sympathy."),
  ("The Conclusion of the Whole Matter (vv.13-14)",
   "After twelve chapters of investigation the answer is two clauses: fear God, and keep "
   "his commandments, for this is the whole duty of man. Nothing about it depends on "
   "having solved the questions the book raised, which is why it functions as a "
   "conclusion rather than a resolution. Verse 14 adds the reason -- God shall bring "
   "every work into judgment, with every secret thing -- and the book that began by "
   "asking what profit there is under the sun ends by pointing above it."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[12:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        fields, extra = {}, []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is None and rest == "Structure:":
                pass
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")

        sections = SECTIONS[page]
        covered = set()
        for label, text in [("Key Themes", THEMES[page])] + \
                           [(f"section {h!r}", p) for h, p in sections] + \
                           [(w, fields[w]) for w in KEEP]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
            if "\u2013" in head:
                problems.append(f"{page}: en-dash in {head!r}")
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        parts.append(ITEM.format(label="Author:", body=fields["Author:"]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=GENRE) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=THEMES[page]) + "\n")
        parts.append(ITEM.format(label="Historical Context:",
                                 body=fields["Historical Context:"]) + "\n")
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
