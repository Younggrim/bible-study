#!/usr/bin/env python3
"""Batch 25: Job 1-42, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch25.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Wisdom Literature"

DATA = {
    "job1": (CLS,
        "four descriptive words, perfect, upright, God-fearing and "
        "evil-avoiding, applied at once to introduce a man before a "
        "single event happens to him, a heavenly council convened "
        "where God himself raises Job's name to Satan rather than the "
        "reverse, an accusation reduced to a single transactional "
        "question, doth Job fear God for nought, four catastrophes "
        "arriving in such rapid succession that each messenger's "
        "report overlaps the next, and a response of worship rather "
        "than curse, the LORD gave, and the LORD hath taken away, "
        "blessed be the name of the LORD"),
    "job2": (CLS,
        "the same heavenly council convened a second time with God "
        "adding that Job was destroyed without cause, a proverb, skin "
        "for skin, used to argue that a man will trade anything "
        "external to save his own body, boils covering Job from the "
        "sole of his foot to his crown so completely his own friends "
        "fail to recognize him, a wife's counsel to curse God and die "
        "met with a rebuke that still refuses to call her foolish "
        "outright, and three friends who travel from a distance and, "
        "before speaking a single word, simply sit with him in "
        "silence for seven days"),
    "job3": (CLS,
        "a curse aimed deliberately at the day of Job's birth rather "
        "than at God himself, language that inverts the words of "
        "creation, let there be light answered point for point by let "
        "that day be darkness, death portrayed not as punishment but "
        "as the great equalizer where kings and prisoners alike find "
        "rest, a question that will not be answered until chapter "
        "thirty-eight, why is light given to him that is in misery, "
        "and an unmistakable echo of Satan's own word hedge, now "
        "turned against the very man it once protected"),
    "job4": (CLS,
        "Eliphaz opening gently by reminding Job of the same counsel "
        "Job once gave to others now struggling to take it himself, a "
        "theology built on a single observed claim, who ever perished "
        "being innocent, a lion's fate used as proof that even the "
        "mightiest wicked eventually fall, a terrifying night vision "
        "in which a spirit passes before his face and a voice asks "
        "whether mortal man can be more just than God, and a valid "
        "theological point, no human is perfectly righteous, quietly "
        "repurposed into a false accusation against Job specifically"),
    "job5": (CLS,
        "a proverb offered as settled fact, man is born unto trouble, "
        "as the sparks fly upward, used to minimize rather than "
        "acknowledge Job's grief, a hymn to God's power and justice "
        "that is true in every line yet aimed to imply Job simply "
        "hasn't sought God properly, suffering reframed entirely as "
        "beneficial discipline, happy is the man whom God correcteth, "
        "six troubles and a seventh promised deliverance if only Job "
        "will repent, and a closing claim of authority, lo this, we "
        "have searched it, so it is, that presents theory as though "
        "it were verified fact"),
    "job6": (CLS,
        "grief measured against the sand of the sea and found "
        "immeasurably heavier, a donkey and an ox that only cry out "
        "when something is genuinely lacking, offered as proof that "
        "Job's own outcry is proportional rather than dramatic, "
        "friends compared to seasonal desert streams that run dry "
        "precisely when travelers need them most, a direct challenge, "
        "teach me, and I will hold my tongue, that no friend actually "
        "answers with anything specific, and a closing plea to be "
        "looked at again with fresh eyes because my righteousness is "
        "in it"),
    "job7": (CLS,
        "human life compared to hired labor and hard military "
        "service, endless nights of tossing set against days that fly "
        "by swifter than a weaver's shuttle, Job turning from his "
        "friends to address God directly for the first time in the "
        "book, Psalm eight's wonder, what is man, that thou art "
        "mindful of him, inverted here into a complaint that God's "
        "constant attention feels like surveillance rather than "
        "grace, and a closing challenge asking what harm his sin, if "
        "it exists, could possibly do to God at all"),
    "job8": (CLS,
        "an opening that dismisses Job's own words as a strong wind "
        "before offering a single argument, a foundational premise, "
        "doth God pervert judgment, used to conclude that Job's dead "
        "children must have deserved their fate, an appeal to "
        "inherited tradition on the grounds that we are but of "
        "yesterday and know nothing ourselves, papyrus that cannot "
        "grow without water and a spider's web too fragile to bear "
        "weight offered as pictures of a godless life collapsing, and "
        "a conditional restoration promised only if Job turns out, "
        "after all, to be blameless"),
    "job9": (CLS,
        "Job agreeing with Bildad's premise that God is just while "
        "drawing from it a far more terrifying conclusion, an "
        "inventory of divine power, moving mountains, shaking the "
        "earth, commanding the sun, that outstrips anything the "
        "friends have said about God, a confession that even "
        "innocence would not help him, if I justify myself, mine own "
        "mouth shall condemn me, a bold accusation that God "
        "destroyeth the perfect and the wicked alike, and a longing "
        "for a daysman, an arbiter able to lay a hand on both God and "
        "man, that the rest of Scripture will eventually answer"),
    "job10": (CLS,
        "a demand to know why God contends with him rather than "
        "simply naming the charge, one of the most intimate "
        "descriptions of creation in Scripture, fashioned like clay, "
        "poured like milk, curdled like cheese, fenced with bones and "
        "sinews, a paradox in which Job cannot win either way, if I "
        "be wicked, woe unto me, and if I be righteous, yet will I "
        "not lift up my head, God pictured hunting him like a fierce "
        "lion through repeated waves of attack, and the same death "
        "wish from chapter three returning, better never to have left "
        "the womb at all"),
    "job11": (CLS,
        "the harshest of the three friends opening not with sympathy "
        "but with a direct accusation of lying, a wish that God "
        "himself would speak against Job and a claim that God "
        "exacteth of thee less than thine iniquity deserveth, a "
        "genuinely exalted description of God's unsearchable wisdom, "
        "higher than heaven, deeper than hell, turned immediately "
        "into a weapon to silence questions rather than answer them, "
        "a comparison of Job to a wild ass's colt that drips with "
        "open contempt, and a conditional prescription, repent and be "
        "restored, that assumes the very guilt it never actually "
        "proves"),
    "job12": (CLS,
        "sarcasm opening the reply, no doubt but ye are the people, "
        "and wisdom shall die with you, before Job claims equal "
        "standing with his accusers, the tabernacles of robbers "
        "prosper named as an observation that directly undercuts the "
        "friends' whole theology, creation itself called on as a "
        "witness, ask now the beasts, and they shall teach thee, a "
        "hymn to divine sovereignty stretching from kings to "
        "counselors to nations that actually exceeds anything the "
        "friends themselves have offered, and the same theology of "
        "God's absolute control turned to precisely the opposite "
        "conclusion the friends drew from it"),
    "job13": (CLS,
        "friends dismissed outright as forgers of lies and physicians "
        "of no value, a direct challenge that their silence would be "
        "wiser than their speech, one of the most famous verses in "
        "all of Scripture, though he slay me, yet will I trust in "
        "him, spoken in the very breath that insists on maintaining "
        "his own innocence before God, a bold request for genuine "
        "two-way dialogue rather than a one-sided assault, then call "
        "thou, and I will answer, and a closing image asking whether "
        "God would really break a leaf driven to and fro"),
    "job14": (CLS,
        "man that is born of a woman is of few days, and full of "
        "trouble, opening one of Scripture's most quoted meditations "
        "on mortality, a tree's capacity to sprout again after being "
        "cut down set bitterly against a man who lies down and riseth "
        "not, a sudden flash of resurrection hope, if a man die, "
        "shall he live again, imagining God hiding him in the grave "
        "until wrath passes, that hope collapsing again by the "
        "chapter's end as mountains fall and water wears away stone, "
        "and a closing image of pain and mourning that belongs to the "
        "man's own flesh and soul even in death"),
    "job15": (CLS,
        "a second speech opening with open accusation rather than "
        "gentle counsel, thine own mouth condemneth thee, and not I, "
        "turning Job's own protests of innocence into further proof "
        "of guilt, rhetorical questions demanding whether Job "
        "predates Adam or sat in God's secret council, angels "
        "themselves called impure before God as the foundation for "
        "calling man abominable and filthy, and an extended, vivid "
        "portrait of the wicked man's torment, terror, wandering, "
        "fruitlessness, aimed at Job without ever naming him "
        "directly"),
    "job16": (CLS,
        "a verdict on his friends that has become proverbial, "
        "miserable comforters are ye all, an offer of what real "
        "comfort would have looked like, I would strengthen you with "
        "my mouth, delivered as a rebuke of what they actually "
        "provide, some of Scripture's most violent imagery describing "
        "God tearing him in wrath and setting him up as a target for "
        "archers, an appeal to the earth itself not to cover his "
        "blood, and a sudden declaration in the very midst of that "
        "violence, my witness is in heaven, and my record is on "
        "high"),
    "job17": (CLS,
        "a spirit broken enough to say the graves are ready for me, a "
        "request for God himself to stand as surety since no human "
        "friend will vouch for him, Job reduced to a public byword "
        "even as he insists the righteous shall hold on his way and "
        "grow stronger, corruption and the worm addressed as father, "
        "mother and sister in place of the family that has abandoned "
        "him, and hope itself asked after in despair, where is now my "
        "hope, as for my hope, who shall see it"),
    "job18": (CLS,
        "Bildad offended enough by Job's earlier comment about "
        "animals to open with open irritation rather than argument, "
        "an accusation that Job tears himself in anger and expects "
        "the earth to be forsaken for his sake, an elaborate, "
        "unbroken poem describing the wicked man's destruction with "
        "no conditional and no offer of restoration this time, "
        "disease called the firstborn of death devouring his skin, "
        "and a portrait so detailed, snares, terrors, a scattered "
        "dwelling, a vanished name, that it can only be read as aimed "
        "directly at Job"),
    "job19": (CLS,
        "friends accused of vexing his soul and breaking him in "
        "pieces with words ten times over, total abandonment "
        "catalogued in devastating detail, brothers estranged, "
        "servants unresponsive, his own breath offensive to his wife, "
        "young children despising him, a request that his words be "
        "engraved with an iron pen and lead in the rock forever "
        "because he expects to lose the argument, one of Scripture's "
        "most remarkable declarations of faith, I know that my "
        "redeemer liveth, spoken at the very depth of that isolation, "
        "and a warning to the friends that a coming judgment will "
        "vindicate him and condemn them"),
    "job20": (CLS,
        "Zophar visibly agitated by Job's warning about a coming "
        "judgment and rushing to answer defensively, a thesis stated "
        "as ancient and self-evident, the triumphing of the wicked is "
        "short, and the joy of the hypocrite but for a moment, "
        "wickedness pictured as sweet food that turns to the gall of "
        "asps once swallowed, riches consumed greedily and then "
        "forced back up, God shall cast them out of his belly, and a "
        "closing verdict naming this the heritage appointed unto him "
        "by God as though the matter were settled beyond appeal"),
    "job21": (CLS,
        "a request simply to be listened to before being mocked, let "
        "this be your consolations, a single demolishing question, "
        "wherefore do the wicked live, become old, yea, are mighty in "
        "power, answered with an inventory of the wicked's actual "
        "observable prosperity, established children, safe houses, "
        "music and celebration, a rebuttal of delayed punishment on "
        "descendants as no punishment at all to the man who already "
        "does not care what happens after his death, and a final, "
        "chilling observation that death itself draws no moral "
        "distinction, they shall lie down alike in the dust, and the "
        "worms shall cover them"),
    "job22": (CLS,
        "a final speech that abandons theory for outright "
        "fabrication, specific crimes invented against a man God "
        "himself has already called blameless, taking pledges from "
        "brothers, stripping the naked, withholding water from the "
        "hungry, an accusation that Job believes thick clouds hide "
        "him from God's sight, the generation of the flood cited as "
        "precedent for what happens to those who tell God to depart "
        "from them, and a genuinely beautiful call to repentance, "
        "acquaint now thyself with him, and be at peace, aimed "
        "tragically at a man who already knows God intimately"),
    "job23": (CLS,
        "a longing that has nothing to do with relief from pain and "
        "everything to do with reaching God himself, oh that I knew "
        "where I might find him, a search in every direction, "
        "forward, backward, left, right, that turns up nothing, one "
        "of the Bible's purest statements of faith without sight, "
        "when he hath tried me, I shall come forth as gold, a "
        "specific claim that his own foot has held God's steps and "
        "not declined from them, and a trembling before the very "
        "unchangeableness that both refines and terrifies at once"),
    "job24": (CLS,
        "a single opening question that names the whole problem of "
        "unpunished evil, why, seeing times are not hidden from the "
        "Almighty, do they that know him not see his days, boundary "
        "stones moved and a widow's ox taken while the poor are "
        "reduced to gleaning others' fields and sleeping naked in the "
        "cold, murderers, adulterers and thieves who operate "
        "specifically because darkness suits them better than light, "
        "and a debated closing section in which the wicked's eventual "
        "fall is conceded even as their prolonged security in the "
        "meantime remains the real complaint"),
    "job25": (CLS,
        "the shortest speech in the entire book, six verses, marking "
        "the visible exhaustion of the friends' theology, an argument "
        "reduced to a single point, God's greatness against man's "
        "smallness, even the moon and stars called impure before him "
        "and man himself called a worm, a kernel of real truth about "
        "human unworthiness used to avoid Job's specific question "
        "rather than answer it, and Zophar's total silence in this "
        "final round left conspicuously unremarked"),
    "job26": (CLS,
        "sarcasm opening the reply to a six-verse speech, how hast "
        "thou helped him that is without power, before Job delivers a "
        "hymn to God's majesty that outstrips anything his accusers "
        "have managed, God's dominion extending even into Sheol where "
        "the dead themselves tremble, the earth described as hanging "
        "upon nothing centuries before that cosmology could be "
        "verified, and a closing line naming everything just "
        "described as merely the outskirts of his ways, how little a "
        "portion is heard of him"),
    "job27": (CLS,
        "an oath of integrity sworn by the very God Job believes has "
        "wronged him, till I die I will not remove mine integrity "
        "from me, a refusal to concede his friends' accusations even "
        "under continued suffering, a description of the wicked man's "
        "fate, children by the sword, houses fragile as a moth's web, "
        "that sounds almost identical to what the friends themselves "
        "have argued, and Job turning that very theology back on his "
        "accusers as evidence of his own innocence rather than his "
        "guilt"),
    "job28": (CLS,
        "an extended survey of human mining technology, silver found, "
        "gold refined, iron extracted, mountains overturned, offered "
        "as proof of nearly limitless human ingenuity, a central "
        "question that all that ingenuity cannot answer, but where "
        "shall wisdom be found, the deep and the sea both denying "
        "they contain it, wisdom placed beyond purchase by gold, "
        "onyx, coral or pearls, and a closing answer that locates "
        "true wisdom not in achievement but in reverence, the fear of "
        "the Lord, that is wisdom, and to depart from evil is "
        "understanding"),
    "job29": (CLS,
        "an elegy for a vanished life opening with when God preserved "
        "me and his candle shined upon my head, elders rising to "
        "their feet and princes falling silent the moment Job "
        "appeared at the city gate, righteousness described entirely "
        "in terms of active advocacy for the poor, the widow, the "
        "blind, the lame, directly refuting accusations Eliphaz has "
        "not yet even made, an expectation of dying peacefully in his "
        "own nest with days multiplied like the sand, and a closing "
        "image of Job living as a king among his people, one who "
        "comforted mourners rather than needing comfort himself"),
    "job30": (CLS,
        "a chapter of pure reversal answering chapter twenty-nine "
        "point for point, mocked now by the very outcasts whose "
        "fathers he would once have disdained to set with his "
        "sheepdogs, a body in open revolt, bones pierced at night, "
        "skin disfigured, pain that never rests, a cry that goes "
        "specifically unanswered, I cry unto thee, and thou dost not "
        "hear me, a God once experienced as near now felt only as "
        "cruel, lifting Job up merely to toss him into the storm, and "
        "a closing image of kinship with jackals and owls where honor "
        "once stood"),
    "job31": (CLS,
        "sexual purity governed at the level of the eyes themselves, "
        "I made a covenant with mine eyes, before any outward act is "
        "even addressed, servants treated with justice on the "
        "explicit ground that master and servant were made in the "
        "same womb, generosity toward the poor, the fatherless and "
        "the naked itemized point by point as a direct answer to "
        "accusations never actually leveled at him until now, worship "
        "of neither gold nor sun nor moon offered as proof against "
        "idolatry, and a closing legal challenge, oh that one would "
        "hear me, behold, my desire is that the Almighty would answer "
        "me, that Job says he would carry as a crown rather than "
        "fear"),
    "job32": (CLS,
        "a fourth voice introduced abruptly and never mentioned again "
        "after this speech or in the book's epilogue, anger described "
        "as kindled four times in five verses, once at Job for "
        "justifying himself over God and three times at the friends "
        "for condemning him without a real answer, a long deferral to "
        "age now abandoned with the observation that great men are "
        "not always wise, an appeal to the spirit in man and the "
        "inspiration of the Almighty as the source of genuine "
        "understanding, and a self-introduction so extended that an "
        "entire chapter passes before a single argument is actually "
        "made"),
    "job33": (CLS,
        "Elihu positioning himself as Job's equal, made by the same "
        "Spirit and formed from the same clay, rather than as another "
        "distant accuser, Job's own words quoted back to him with "
        "apparent accuracy, I am clean without transgression, he "
        "counteth me for his enemy, a claim that God does in fact "
        "speak, just not the way Job expects, through dreams, through "
        "pain and through a mediating angel, one of the most "
        "Christological passages in the book naming a ransom found "
        "and a soul brought back from the pit, and an open invitation "
        "for Job to answer, the only one of the four speakers who "
        "actually offers him the floor"),
    "job34": (CLS,
        "Job's positions paraphrased once more, I am righteous, and "
        "God hath taken away my judgment, before Elihu turns to "
        "defend God's justice as inherent rather than delegated, an "
        "argument that God cannot answer to anyone because no one "
        "appointed him over the earth in the first place, an "
        "insistence that God shows no partiality to prince or pauper "
        "because both are equally the work of his hands, a model "
        "confession put into a hypothetical repentant man's mouth as "
        "what Job himself has failed to say, and a harsh closing "
        "verdict that Job speaks without knowledge and adds rebellion "
        "to his sin"),
    "job35": (CLS,
        "a question attributed to Job, what advantage have I, how am "
        "I better off than if I had sinned, answered first by "
        "insisting human conduct affects other humans rather than "
        "diminishing or enriching God at all, a distinction drawn "
        "between crying out in raw pain, which anyone does, and "
        "genuinely seeking God, which requires real intentionality, "
        "none saith, where is God my maker, who giveth songs in the "
        "night, an instruction to trust even when Job cannot see the "
        "judgment Elihu insists is still before him, and a closing "
        "accusation, in words that anticipate God's own rebuke two "
        "chapters later, that Job multiplies words without knowledge"),
    "job36": (CLS,
        "a claim to speak on God's behalf with perfect knowledge that "
        "borders on presumption even as its content proves genuinely "
        "insightful, a direct challenge to Job's complaint of divine "
        "inattention, he withdraweth not his eyes from the righteous, "
        "Elihu's most original idea, suffering as discipline that "
        "opens the ears rather than punishment for a hidden past sin, "
        "a warning not to turn toward iniquity rather than simply "
        "accepting affliction as it comes, and a transition into "
        "nature poetry, the water cycle, thunder and lightning, that "
        "begins building directly toward God's own appearance from "
        "the whirlwind"),
    "job37": (CLS,
        "a heart trembling at the sound of God's own thunder before a "
        "single further argument is made, weather itself, snow, "
        "frost, whirlwind, described as serving multiple purposes at "
        "once, whether for correction, or for his land, or for mercy, "
        "a repeated challenge to Job, stand still, and consider the "
        "wondrous works of God, that anticipates almost exactly the "
        "questions God himself will soon ask, an admission that human "
        "speech cannot even be properly ordered before God because of "
        "sheer human darkness, and a closing description of terrible "
        "majesty that functions as the herald's announcement just "
        "before the King himself finally speaks"),
    "job38": (CLS,
        "God breaking thirty-seven chapters of human argument by "
        "speaking out of a whirlwind, an opening rebuke that names "
        "Job's words as without knowledge rather than sinful, where "
        "wast thou when I laid the foundations of the earth answered "
        "by the detail that morning stars sang and sons of God "
        "shouted for joy while Job did not yet exist, boundaries set "
        "on the sea itself, hitherto shalt thou come, but no further, "
        "used as the model for boundaries God alone can set on "
        "suffering, and a relentless sequence of questions about "
        "snow, stars and weather that Job is never expected to "
        "answer, only to feel the weight of"),
    "job39": (CLS,
        "God's interrogation shifting from cosmic phenomena to "
        "animals that live entirely outside human control, mountain "
        "goats and wild donkeys whose reproductive cycles God "
        "oversees without any need of human awareness, a wild ox too "
        "powerful and untameable to ever serve a man's field, an "
        "ostrich called foolish and deprived of wisdom yet able to "
        "outrun a horse, one of the most magnificent animal "
        "descriptions in literature given to a war horse that laughs "
        "at fear and smells battle from afar, and hawks and eagles "
        "that nest on unreachable crags governed entirely by instinct "
        "rather than instruction"),
    "job40": (CLS,
        "a direct challenge to answer, shall he that contendeth with "
        "the Almighty instruct him, met by Job's first brief and "
        "still incomplete submission, I am vile, what shall I answer "
        "thee, a second speech that turns the question from "
        "intellectual to moral, wilt thou condemn me, that thou "
        "mayest be righteous, exposing that Job's insistence on his "
        "own innocence had implicitly indicted God's justice, and "
        "Behemoth introduced as a creature Job cannot even capture, "
        "let alone control, offered as proof that only the one who "
        "governs all creation has any right to question its Ruler"),
    "job41": (CLS,
        "an entire chapter devoted to a single terrifying creature no "
        "hook, rope, covenant or weapon can subdue, a cumulative "
        "catalogue of invulnerability, scales sealed like armor, fire "
        "from the mouth, a heart hard as stone, that leaves Leviathan "
        "entirely beyond any human power to touch, a theological "
        "pivot at the chapter's center, who then is able to stand "
        "before me, arguing from the creature's terror to the far "
        "greater terror owed its Creator, a declaration that God owes "
        "nothing to anyone because whatsoever is under the whole "
        "heaven is his, and a closing title, king over all the "
        "children of pride, that names exactly the posture the whole "
        "book has been correcting"),
    "job42": (CLS,
        "a confession that moves from secondhand hearing to direct "
        "sight, I have heard of thee by the hearing of the ear, but "
        "now mine eye seeth thee, repentance expressed not over "
        "specific invented sins but over speaking of things too "
        "wonderful to understand, God's own astonishing verdict that "
        "Job, who accused him of cruelty, spoke rightly, while the "
        "friends, who defended him with orthodox theology, spoke "
        "wrongly, restoration arriving specifically when Job prays "
        "for the very friends who wronged him, and a doubled "
        "inheritance, fourteen thousand sheep, six thousand camels, "
        "exactly twice what Job had before, closing a book that never "
        "once explains why any of it happened"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
