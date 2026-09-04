#!/usr/bin/env python3
"""Batch 26: Proverbs 1-31, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch26.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Wisdom Literature"

DATA = {
    "proverbs1": (CLS,
        "a prologue that states six separate purposes before offering "
        "a single proverb, the fear of the LORD is the beginning of "
        "knowledge set as the motto the entire book hangs on, "
        "sinners' own invitation to violence quoted at length "
        "precisely because it sounds like belonging rather than "
        "crime, Wisdom personified crying aloud in the streets and "
        "city gates rather than hidden in any secret place, and a "
        "chilling reversal of roles promised to those who refuse her, "
        "I also will laugh at your calamity, mirroring the very "
        "mockery once aimed at wisdom itself"),
    "proverbs2": (CLS,
        "an entire chapter built as one twenty-two-verse conditional "
        "sentence, four verses of effortful verbs, receive, hide, "
        "incline, cry, before a single promise is given, wisdom "
        "described as both a gift God gives and a treasure a man must "
        "dig for like silver, protection offered against two dangers "
        "in turn, men who delight in evil for its own pleasure and a "
        "woman whose speech flatters while her feet forsake the "
        "covenant, and a closing verdict phrased in terms of land "
        "tenure rather than reward, the upright shall dwell in the "
        "land, the wicked shall be rooted out of it"),
    "proverbs3": (CLS,
        "five of the most quoted sentences in the book packed into "
        "ten opening verses, each pairing an instruction with a "
        "promise, trust in the LORD with all thine heart tied "
        "directly to having thy paths directed, divine discipline "
        "reframed as evidence of love rather than of rejection, for "
        "whom the LORD loveth he correcteth, wisdom valued entirely "
        "through commercial comparison, more precious than rubies, "
        "before being called a tree of life, the first return to "
        "Eden's imagery in the book, and neighborly duties closing "
        "the chapter in specific, mostly negative instructions like "
        "say not unto thy neighbour, go, and come again tomorrow"),
    "proverbs4": (CLS,
        "wisdom passed down three explicit generations, David to "
        "Solomon to Solomon's own son, quoted directly rather than "
        "merely asserted, a road pictured as the central image of the "
        "chapter, four separate commands to avoid the same wicked "
        "path, avoid it, pass not by it, turn from it, pass away, two "
        "paths contrasted purely by visibility, one shining more and "
        "more unto the perfect day, the other unable to see what "
        "makes them stumble, and a closing anatomy of the body "
        "working outward from a single organ nobody else can see, "
        "keep thy heart with all diligence, for out of it are the "
        "issues of life"),
    "proverbs5": (CLS,
        "a warning whose entire logic rests on the gap between how "
        "something sounds and where it actually ends, her lips drop "
        "as an honeycomb, but her end is bitter as wormwood, a "
        "command that is purely spatial and admits no negotiation, "
        "remove thy way far from her, and come not nigh the door of "
        "her house, a public confession put in the mouth of a man who "
        "did not listen, how have I hated instruction, marital love "
        "celebrated with unembarrassed water imagery, drink waters "
        "out of thine own cistern, and a closing statement that moves "
        "the whole matter out of discretion entirely, for the ways of "
        "man are before the eyes of the LORD"),
    "proverbs6": (CLS,
        "four separate dangers gathered into a single varied chapter, "
        "foolish loan pledges urged to be escaped through the same "
        "verbs used to describe fleeing a hunter or a fowler, an ant "
        "sent as the sole teacher of diligence, having no guide, "
        "overseer, or ruler, provideth her meat in the summer, a "
        "numerical list of seven things the LORD hates that works "
        "methodically through the body, a proud look, a lying tongue, "
        "feet swift to mischief, before naming a seventh that is not "
        "a body part at all, one who soweth discord among brethren, "
        "and an adultery warning made physical rather than merely "
        "moral, can a man take fire in his bosom, and his clothes not "
        "be burned"),
    "proverbs7": (CLS,
        "the longest continuous narrative in the entire book of "
        "Proverbs told from a window at twilight, wisdom urged to be "
        "held as close as family, thou art my sister, and "
        "understanding my kinswoman, specifically as protection "
        "against what follows, a seduction narrated in unhurried, "
        "cinematic detail down to the woman's dress and her "
        "religious-sounding speech, a young man described as void of "
        "understanding not for lack of intelligence but for standing "
        "in the wrong place, and a closing body count naming him one "
        "casualty among many, many strong men have been slain by her"),
    "proverbs8": (CLS,
        "Wisdom speaking for herself in an extended first-person "
        "address unlike anywhere else in the book, a public call "
        "issued from the very gates and crossroads where business is "
        "actually done rather than from anywhere hidden, a claim "
        "placed underneath government itself, by me kings reign, and "
        "princes decree justice, an account of her own age that "
        "reaches back before the mountains were settled and before "
        "the depths had fountains, present at creation while never "
        "claiming to have done the creating, and a closing appeal "
        "that puts the alternative in terms of self-harm rather than "
        "external punishment, he that sinneth against me wrongeth his "
        "own soul"),
    "proverbs9": (CLS,
        "two women, Wisdom and Folly, each building a house and each "
        "calling out from the highest places of the city using nearly "
        "identical words, whoso is simple, let him turn in hither, a "
        "banquet fully prepared, animals killed, wine mingled, "
        "servants sent, set against a banquet built on nothing but "
        "theft, stolen waters are sweet, an interlude on correction "
        "distinguishing not intelligence but response, reprove not a "
        "scorner, lest he hate thee, rebuke a wise man, and he will "
        "love thee, the book's motto restated a second time, the fear "
        "of the LORD is the beginning of wisdom, and a closing detail "
        "that separates the two invitations completely, he knoweth "
        "not that the dead are there"),
    "proverbs10": (CLS,
        "a literary transition marked cleanly in its own opening "
        "verse, the proverbs of Solomon, moving from nine chapters of "
        "discourse into individual two-line contrasts built almost "
        "entirely on the word but, the tongue appearing in eleven of "
        "thirty-two verses, from the mouth of the righteous as a well "
        "of life to a froward tongue that shall be cut out in the "
        "chapter's very last line, love covereth all sins arriving as "
        "the one proverb later quoted directly in the New Testament, "
        "wealth handled two ways at once, the rich man's own strong "
        "city set against a single verse crediting increase entirely "
        "to the blessing of the LORD, and a closing run built on "
        "duration, the righteous never removed, the years of the "
        "wicked shortened"),
    "proverbs11": (CLS,
        "commerce opened with a specific business practice named "
        "outright, a false balance is abomination to the LORD, but a "
        "just weight is his delight, a civic claim unusual for the "
        "collection, by the blessing of the upright the city is "
        "exalted, treating private virtue as having public effect, in "
        "the multitude of counsellors there is safety standing beside "
        "a warning against becoming surety for a stranger, the "
        "paradox the chapter is remembered for, there is that "
        "scattereth, and yet increaseth, and a closing image of the "
        "righteous as a tree of life, ending on the man who winneth "
        "souls being called wise"),
    "proverbs12": (CLS,
        "correction opened directly, whoso loveth instruction loveth "
        "knowledge, but he that hateth reproof is brutish, a "
        "virtuous woman called a crown to her husband while her "
        "opposite is named rottenness in his bones, speech pictured "
        "as both weapon and rescue, the words of the wicked lie in "
        "wait for blood while the mouth of the upright delivers, "
        "lying lips called an abomination to the LORD in the verse "
        "the chapter itself turns on, and a closing line that states "
        "the whole collection's premise in eight words, in the way of "
        "righteousness is life"),
    "proverbs13": (CLS,
        "a son who hears instruction set against a scorner who will "
        "not from the very first verse, two observations about money "
        "placed deliberately against each other, the ransom of a "
        "man's life are his riches, and there is that maketh himself "
        "rich, yet hath nothing, hope deferred maketh the heart sick, "
        "but when the desire cometh, it is a tree of life, offered as "
        "the chapter's most quoted line, a plain sentence on "
        "companionship, he that walketh with wise men shall be wise, "
        "but a companion of fools shall be destroyed, and a "
        "much-argued verse on discipline, he that spareth his rod "
        "hateth his son, closing on sufficiency rather than plenty"),
    "proverbs14": (CLS,
        "building and demolition opening the chapter, every wise "
        "woman buildeth her house, but the foolish plucketh it down "
        "with her hands, a warning against self-assurance repeated "
        "twice in the whole book, there is a way which seemeth right "
        "unto a man, but the end thereof are the ways of death, a "
        "loneliest sentence placed right beside it, the heart knoweth "
        "his own bitterness, and a stranger doth not intermeddle "
        "therewith, poverty and friendship set side by side without "
        "comment, the poor is hated even of his own neighbour, and "
        "the rich hath many friends, and a closing widening from "
        "household to nation, righteousness exalteth a nation, but "
        "sin is a reproach to any people"),
    "proverbs15": (CLS,
        "the best-known verse in the whole collection opening the "
        "chapter, a soft answer turneth away wrath, but grievous "
        "words stir up anger, God named as the watching observer "
        "rather than only the judge, the eyes of the LORD are in "
        "every place, beholding the evil and the good, two "
        "better-than sayings that both prefer the smaller portion, "
        "better is a dinner of herbs where love is, than a stalled ox "
        "and hatred therewith, planning entrusted to counsel rather "
        "than to solitary confidence, and a closing pair that puts "
        "the argument in strict order, the fear of the LORD is the "
        "instruction of wisdom, and before honour is humility"),
    "proverbs16": (CLS,
        "the densest theological cluster in the whole collection, "
        "six of nine opening verses naming the LORD directly, a "
        "man's heart deviseth his way, but the LORD directeth his "
        "steps, court wisdom assuming a reader near power, the wrath "
        "of a king is as messengers of death, the single most quoted "
        "verse in the chapter, pride goeth before destruction, and an "
        "haughty spirit before a fall, strength measured by restraint "
        "rather than conquest, he that is slow to anger is better "
        "than the mighty, and he that ruleth his spirit than he that "
        "taketh a city, and a closing verse that hands the outcome "
        "entirely to God, the lot is cast into the lap, but the whole "
        "disposing thereof is of the LORD"),
    "proverbs17": (CLS,
        "an opening preference for less rather than more, better is "
        "a dry morsel, and quietness therewith, than an house full of "
        "sacrifices with strife, the fining pot for silver and the "
        "furnace for gold set beside the LORD who trieth the hearts, "
        "one of Scripture's great friendship verses, a friend loveth "
        "at all times, and a brother is born for adversity, quarrels "
        "described physically, the beginning of strife is as when one "
        "letteth out water, and a closing pair that makes silence "
        "itself the test of wisdom rather than eloquence, even a "
        "fool, when he holdeth his peace, is counted wise"),
    "proverbs18": (CLS,
        "a man who has withdrawn from community pursuing his own "
        "desire against all sound wisdom, judging a matter before "
        "hearing it named outright as folly and shame, two images of "
        "refuge placed deliberately unequal, the name of the LORD is "
        "a strong tower, and the rich man's wealth is his strong "
        "city, one of the most quoted lines in the whole collection, "
        "death and life are in the power of the tongue, and a closing "
        "distinction between quantity and quality of friendship, a "
        "man that hath friends must shew himself friendly, and there "
        "is a friend that sticketh closer than a brother"),
    "proverbs19": (CLS,
        "integrity preferred over cleverness from the opening verse, "
        "better is the poor that walketh in his integrity, than he "
        "that is perverse in his lips, poverty's effect on friendship "
        "stated without any moralizing, wealth maketh many friends, "
        "but the poor is separated from his neighbour, the "
        "collection's boldest statement on charity, he that hath pity "
        "upon the poor lendeth unto the LORD, discipline urged while "
        "there is still hope, chasten thy son while there is hope, "
        "and a closing pair naming the fear of the LORD as tending to "
        "life while judgment waits for scorners"),
    "proverbs20": (CLS,
        "a warning about alcohol stated without any softening, wine "
        "is a mocker, strong drink is raging, a question that comes "
        "as near to a doctrine of universal guilt as the collection "
        "gets, who can say, I have made my heart clean, I am pure "
        "from my sin, the sharpest piece of market observation in the "
        "whole book, it is naught, it is naught, saith the buyer, "
        "when he is gone his way, then he boasteth, a prohibition the "
        "New Testament later takes up directly, say not thou, I will "
        "recompense evil, but wait on the LORD, and a closing pair "
        "contrasting the glory of young men's strength with the "
        "beauty of old men's gray hair"),
    "proverbs21": (CLS,
        "the boldest sovereignty claim in the whole collection "
        "opening the chapter, the king's heart is in the hand of the "
        "LORD, as the rivers of water, he turneth it whithersoever he "
        "will, a priority the prophets spent entire books arguing, to "
        "do justice and judgment is more acceptable to the LORD than "
        "sacrifice, a saying about a brawling wife repeated almost "
        "word for word twice in the same chapter, evidence the "
        "collection was assembled rather than composed in one "
        "sitting, guarded speech named as guarding the soul itself, "
        "and a closing image of a horse prepared for battle set "
        "against the plain admission that safety belongs to the LORD "
        "alone"),
    "proverbs22": (CLS,
        "the final sixteen verses of the first great Solomonic "
        "collection weighted heavily toward money and class, the rich "
        "and poor meet together, the LORD is the maker of them all, "
        "a sentence that has described debt ever since it was "
        "written, the borrower is servant to the lender, the single "
        "most quoted and most argued verse in the whole book, train "
        "up a child in the way he should go, and when he is old, he "
        "will not depart from it, and a clean break at verse "
        "seventeen into an entirely new collection, the words of the "
        "wise, whose form and content closely track an ancient "
        "Egyptian instruction text centuries older than Solomon "
        "himself"),
    "proverbs23": (CLS,
        "a meal at a ruler's table treated as a test rather than a "
        "courtesy, riches said to make themselves wings and fly away "
        "as an eagle toward heaven the moment a man labours to be "
        "rich, correction offered from a father's own hope of being "
        "gladdened rather than from mere enforcement, a request that "
        "becomes the emotional center of the whole chapter, my son, "
        "give me thine heart, and the longest sustained scene in all "
        "the collected sayings, the drunkard observed from the "
        "inside, swimming eyes, an unfelt beating, and a closing line "
        "naming the whole point of the portrait, I will seek it yet "
        "again"),
    "proverbs24": (CLS,
        "wisdom's own house-building language from chapter nine "
        "reused for human strength, through wisdom is an house "
        "builded, and by understanding it is established, character "
        "measured in the shortest sentence in the book, if thou faint "
        "in the day of adversity, thy strength is small, an "
        "obligation to rescue the condemned that refuses in advance "
        "any excuse of not having known, a verse describing "
        "resilience that has outlived its original setting, a just "
        "man falleth seven times, and riseth up again, and the "
        "collection's only piece of first-person reportage, a walk "
        "past an overgrown, broken-down field belonging to the "
        "slothful, closing the entire Words of the Wise section"),
    "proverbs25": (CLS,
        "an editorial note found nowhere else quite like it in the "
        "Old Testament, these are also proverbs of Solomon, which the "
        "men of Hezekiah king of Judah copied out roughly two and a "
        "half centuries after they were first spoken, court material "
        "built around the glory of concealing versus the honour of "
        "searching out a matter, similes almost entirely organized "
        "around knowing when to stop, hast thou found honey, eat so "
        "much as is sufficient for thee, an instruction Paul later "
        "quotes directly in Romans, if thine enemy be hungry, give "
        "him bread to eat, and a closing observation that even "
        "careful speech eventually fails against a whispering tongue"),
    "proverbs26": (CLS,
        "three character types organized into deliberate blocks, the "
        "fool, the sluggard and the troublemaker, rather than "
        "scattered individually, two verses placed side by side that "
        "appear to contradict each other on purpose, answer not a "
        "fool according to his folly and immediately answer a fool "
        "according to his folly, a lazy man's excuse elaborate enough "
        "to be its own kind of labor, there is a lion in the way, "
        "damage done through gossip pictured as fire that goes out "
        "for lack of wood, and a closing image naming flattery as "
        "concealment, a potsherd covered with silver dross"),
    "proverbs27": (CLS,
        "a limit on planning stated outright, boast not thyself of "
        "tomorrow, for thou knowest not what a day may bring forth, "
        "the fullest and most unsentimental treatment of friendship "
        "anywhere in the book, faithful are the wounds of a friend, "
        "but the kisses of an enemy are deceitful, character "
        "described as formed in company rather than in isolation, "
        "iron sharpeneth iron, so a man sharpeneth the countenance of "
        "his friend, praise named as a test alongside the fining pot "
        "that tries silver, and a closing turn into an unexpected "
        "setting for a wisdom collection, a farmyard, urging "
        "diligence in knowing the state of one's own flocks"),
    "proverbs28": (CLS,
        "bearing contrasted rather than outcome from the opening "
        "verse, the wicked flee when no man pursueth, but the "
        "righteous are bold as a lion, governance and money woven "
        "through nearly every antithetical couplet, a condition the "
        "rest of the Bible builds a whole doctrine on, he that "
        "covereth his sins shall not prosper, but whoso confesseth "
        "and forsaketh them shall have mercy, hasty riches condemned "
        "as inevitably corrupting, he that maketh haste to be rich "
        "shall not be innocent, and a closing verse that repeats the "
        "opening image from the opposite direction, when the wicked "
        "rise, men hide themselves"),
    "proverbs29": (CLS,
        "the single point past which correction stops working named "
        "outright, he that being often reproved hardeneth his neck "
        "shall suddenly be destroyed, and that without remedy, public "
        "life running through the chapter more than any other in the "
        "collection, when the righteous are in authority, the people "
        "rejoice, but when the wicked beareth rule, the people mourn, "
        "the most quoted and most misused line in the chapter, where "
        "there is no vision, the people perish, referring to "
        "prophetic revelation rather than ambition, discipline urged "
        "again in the household, and a closing verse naming where "
        "fear of man leads compared with trust in the LORD"),
    "proverbs30": (CLS,
        "an unknown author, Agur son of Jakeh, opening not with "
        "instruction but with a confession of ignorance, surely I am "
        "more brutish than any man, questions no answer in the "
        "collection has actually addressed, who hath gathered the "
        "wind in his fists, the only prayer in the entire book, give "
        "me neither poverty nor riches, feed me with food convenient "
        "for me, a run of numerical sayings admiring ants, conies, "
        "locusts and spiders for competence that outruns their size, "
        "and a closing image of pressure producing what it must, the "
        "churning of milk bringeth forth butter, so the forcing of "
        "wrath bringeth forth strife"),
    "proverbs31": (CLS,
        "the book's final chapter attributed entirely to a mother "
        "instructing her son the king, three times naming their "
        "relationship before a single piece of advice is given, what, "
        "my son, and what, the son of my womb, wine withheld "
        "specifically from a ruler who might forget the law and "
        "pervert judgment for the afflicted, an oracle that closes by "
        "reducing itself to advocacy, open thy mouth for the dumb, "
        "plead the cause of the poor and needy, and an acrostic poem "
        "describing a wife whose strength is explicitly commercial, "
        "she considereth a field, and buyeth it, closing the whole "
        "book on the very motto it opened with, but a woman that "
        "feareth the LORD, she shall be praised"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
