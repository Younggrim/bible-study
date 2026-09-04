#!/usr/bin/env python3
"""Batch 24: Genesis 2-50, the rest of the book (chapter 1 already has Key Themes).

    python3 add_key_themes_batch24.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "genesis2": (CLS,
        "a seventh day of rest that celebrates completion rather than "
        "recovery from exhaustion, man formed from dust and then "
        "animated by a breath breathed directly into his nostrils, "
        "two named trees standing at the center of a garden otherwise "
        "left open to every other tree, the first not good in all of "
        "creation spoken over a solitary man before any sin has "
        "occurred, and marriage instituted in a single sentence, bone "
        "of my bones and flesh of my flesh, before the chapter closes "
        "on nakedness without shame"),
    "genesis3": (CLS,
        "a serpent's opening question already reframing what God "
        "actually said rather than denying it outright, three appeals "
        "landing at once, food, beauty and wisdom, in the instant "
        "before the fruit is eaten, a couple who hide from the very "
        "God who has been walking with them and then blame each other "
        "the moment they are found, a curse on the serpent that "
        "doubles as the first promise of a deliverer, her seed shall "
        "bruise thy head, and coats of skin sewn by God himself as "
        "the first sacrifice covering the first shame"),
    "genesis4": (CLS,
        "two offerings brought side by side with only one accepted, "
        "and no stated difference except the unrecorded difference of "
        "heart behind each, a warning that sin crouches at the door "
        "before it ever actually pounces, the first murder answered "
        "by a question, where is thy brother, that Cain deflects "
        "rather than answers, a mark placed on a murderer for his own "
        "protection rather than his punishment, and two divergent "
        "lines, Cain's producing cities, music and metalwork alongside "
        "boastful violence, Seth's producing nothing recorded except "
        "that men began to call on the name of the LORD"),
    "genesis5": (CLS,
        "ten generations from Adam to Noah spanning over sixteen "
        "centuries by their own recorded ages, a repeated closing "
        "clause, and he died, tolling eight separate times like a "
        "bell across the chapter, one man alone breaking the pattern, "
        "Enoch walked with God, and he was not, for God took him, a "
        "genealogy built entirely around the same formula of living, "
        "begetting and dying, and a final birth named Noah in the "
        "explicit hope that he might bring comfort from the very "
        "ground God had cursed"),
    "genesis6": (CLS,
        "an obscure union between the sons of God and the daughters "
        "of men producing giants and a corruption so total that every "
        "imagination of the heart is described as only evil "
        "continually, God's own grief at having made humanity at "
        "all, one man found to have grace in the eyes of the LORD "
        "before the word grace is ever used anywhere else in the "
        "text, exact dimensions given for an ark large enough to "
        "preserve two of every kind, and a closing note that Noah did "
        "according to all that God commanded him, so did he"),
    "genesis7": (CLS,
        "an invitation to come rather than go into the ark, God "
        "already present there awaiting Noah's family, clean animals "
        "gathered by sevens and unclean by twos, a flood traced to "
        "two separate sources, the fountains of the great deep and "
        "the windows of heaven, opening on the very same day, forty "
        "days of rain followed by a hundred fifty days of prevailing "
        "water, and a single line noting that the LORD himself shut "
        "the door once everyone was inside"),
    "genesis8": (CLS,
        "God remembering Noah not because he had forgotten him but "
        "because the moment has come to act on his behalf, a wind "
        "sent over the waters using the same Hebrew word elsewhere "
        "translated Spirit, a raven that never returns set against a "
        "dove that comes back twice before finally staying away for "
        "good, an olive leaf carried back as the first physical "
        "evidence of dry land, and the first altar in Scripture built "
        "the moment Noah steps off the ark, its sweet savour "
        "prompting God's promise never again to curse the ground or "
        "destroy every living thing"),
    "genesis9": (CLS,
        "the same command once given in Eden, be fruitful and "
        "multiply, reissued to Noah but paired now with a fear and "
        "dread of man that never existed in the garden, permission to "
        "eat meat granted for the first time alongside a strict "
        "prohibition on blood, murder answered with a formula, by man "
        "shall his blood be shed, that ties capital punishment "
        "directly to the image of God in every human being, a rainbow "
        "set as a sign whose remembering is explicitly assigned to "
        "God rather than to Noah, and a drunken failure in a vineyard "
        "producing a prophecy that shapes the destiny of three "
        "separate lines of nations"),
    "genesis10": (CLS,
        "seventy nations traced back through Noah's three sons in a "
        "genealogical table with no parallel anywhere else in ancient "
        "literature, an order that lists Japheth first and Shem last "
        "even though the heading names them the other way, because "
        "the line the book actually follows is saved for the end, "
        "Nimrod singled out among Ham's descendants as a mighty "
        "hunter who founds Babel and Nineveh, Canaan's descendants "
        "listed as the very nations Israel will later displace, and "
        "a closing verse insisting all humanity divided from this "
        "single family after the flood"),
    "genesis11": (CLS,
        "one language and one people building not to fill the earth "
        "as commanded but to make a name and avoid being scattered, a "
        "tower so small God must, ironically, come down merely to see "
        "it, a confusion of language and a scattering that turns "
        "humanity's own act of defiance into the mechanism of its "
        "judgment, ten generations from Shem to Abram in which "
        "recorded lifespans fall dramatically from six hundred years "
        "to two hundred five, and a family that stops short of Canaan "
        "at Haran, leaving the story poised exactly where God's call "
        "in chapter twelve will pick it up"),
    "genesis12": (CLS,
        "a call to leave country, kindred and father's house answered "
        "before a single promise has actually been fulfilled, seven "
        "promises stacked one after another culminating in all the "
        "families of the earth being blessed through this one man, an "
        "altar built at both Shechem and Bethel marking obedience "
        "with worship rather than merely with movement, a famine "
        "driving Abram into Egypt where he lies about his own wife, "
        "and a rebuke from a pagan king that leaves the father of "
        "faith sent away in disgrace even as God protects the promise "
        "despite him"),
    "genesis13": (CLS,
        "a return from Egyptian failure that leads Abram straight "
        "back to the altar at Bethel rather than anywhere else, "
        "herdsmen's strife settled by Abram offering Lot first choice "
        "of the land rather than claiming it himself, Lot lifting up "
        "his own eyes to choose the well-watered plain by sight, God "
        "then telling Abram to lift up his eyes and receive land by "
        "promise instead, and a single ominous clause noting the men "
        "of Sodom were wicked and sinners before the LORD exceedingly, "
        "planted right where Lot pitches his tent toward the city"),
    "genesis14": (CLS,
        "the Bible's first recorded battle narrative arising out of a "
        "rebellion against tribute paid to four eastern kings, Abram "
        "arming exactly three hundred eighteen trained servants of "
        "his own household rather than assembling an army, a night "
        "pursuit reaching as far as Dan and beyond Damascus to "
        "recover Lot along with everyone else's goods, two kings "
        "meeting Abram on his return, one offering a transaction and "
        "one offering bread, wine and a blessing, and a tithe given "
        "to Melchizedek before Abram refuses to take so much as a "
        "thread from the king of Sodom"),
    "genesis15": (CLS,
        "God identifying himself to a still-childless man as both "
        "shield and exceeding great reward, a promise of countless "
        "offspring illustrated by stars rather than by any nearer, "
        "more countable thing, a single verse, he believed in the "
        "LORD, and he counted it to him for righteousness, that "
        "becomes the foundational text for justification by faith "
        "throughout the New Testament, a covenant ceremony in which a "
        "smoking furnace and a burning lamp alone pass between the "
        "divided pieces while Abram sleeps, and four hundred years of "
        "coming slavery and deliverance revealed to him well before "
        "Israel exists to experience either"),
    "genesis16": (CLS,
        "Sarai's own plan to build a family through her Egyptian maid "
        "rather than through God's stated timing, Abram's agreement "
        "to a solution both culturally legal and spiritually "
        "mistaken, a pregnant Hagar despising the mistress who "
        "arranged the whole plan, Abram washing his hands of the "
        "resulting conflict with thy maid is in thy hand, and the "
        "first appearance in Scripture of the angel of the LORD, who "
        "finds a fleeing servant in the wilderness and gives her a "
        "name for God, thou God seest me, that no one else in the "
        "text ever uses"),
    "genesis17": (CLS,
        "a new divine name, El Shaddai, introduced thirteen years "
        "after Ishmael's birth alongside new names for both Abram and "
        "Sarai, circumcision instituted as a sign cut into the flesh "
        "of every male at eight days old, Abraham's own laughter at "
        "the promise of a hundred-year-old father and a ninety-year-"
        "old mother met not with rebuke but with a name, Isaac, that "
        "means laughter itself, Ishmael blessed and made into a "
        "nation while the covenant itself is reserved specifically "
        "for a son not yet conceived, and every male in the household "
        "circumcised that same day with no recorded delay"),
    "genesis18": (CLS,
        "three visitors arriving at Mamre, one of them the LORD "
        "himself, met with lavish and immediate hospitality before "
        "anyone identifies who they are, a promise that Sarah will "
        "have a son within the year met by her own private laughter, "
        "a rhetorical question that answers the very doubt just "
        "raised, is any thing too hard for the LORD, God choosing to "
        "tell Abraham his plan for Sodom rather than hide it from "
        "him, and an intercession that talks God down from fifty "
        "righteous to ten without ever finding even that many in the "
        "city"),
    "genesis19": (CLS,
        "two angels welcomed into Lot's house at the very gate where "
        "he now sits as a man of civic standing, a mob demanding the "
        "visitors answered by Lot's own shocking offer of his "
        "daughters instead, a rescue in which the angels must "
        "physically drag a hesitating Lot out of the city, brimstone "
        "and fire raining from the LORD out of heaven in a judgment "
        "total enough to leave nothing standing, and Lot's wife "
        "turned to a pillar of salt for a single backward glance "
        "while his own daughters later draw him into the very "
        "disgrace that produces Moab and Ammon"),
    "genesis20": (CLS,
        "the same she is my sister deception repeated with Abimelech "
        "that Abraham already used on Pharaoh, this time coming after "
        "God has already promised Isaac through Sarah by name, a "
        "pagan king protected from sin in a dream even while "
        "Abraham's own household created the danger, Abraham's excuse "
        "that he assumed no fear of God existed in this place proven "
        "wrong by the king's own innocence, and a half-truth admitted "
        "outright, Sarah is in fact his half-sister, revealing the "
        "deception as a long-standing arrangement rather than a "
        "single lapse"),
    "genesis21": (CLS,
        "a promise twenty-five years in the making finally fulfilled "
        "at the set time exactly as God had said, a name, Isaac, "
        "meaning laughter, turning what was once the laughter of "
        "disbelief into the laughter of joy, Ishmael's mockery at a "
        "weaning feast triggering Sarah's demand that he and Hagar be "
        "sent away entirely, God confirming a promise for Ishmael "
        "even while confirming that the covenant runs through Isaac "
        "alone, and a covenant sworn with Abimelech at a well named "
        "for the very oath exchanged there, Beer-sheba"),
    "genesis22": (CLS,
        "a command to sacrifice the son of promise stacked with four "
        "separate intensifiers, thy son, thine only son, Isaac, whom "
        "thou lovest, before a single reason is given, three days' "
        "journey undertaken without any recorded hesitation or delay, "
        "a son's own question, where is the lamb, answered with a "
        "sentence that turns out to be literally true before the "
        "chapter ends, an angel's interruption at the very moment the "
        "knife is raised and a ram caught in a thicket offered in "
        "Isaac's place, and a place named Jehovah-jireh, the LORD "
        "will provide, standing as the chapter's own summary of "
        "everything that just happened"),
    "genesis23": (CLS,
        "the only woman in Scripture whose age at death is explicitly "
        "recorded, a burial cave purchased at full price from "
        "Hittites who offer it freely at first, a transaction "
        "insisted on and witnessed publicly rather than accepted as a "
        "gift, four hundred shekels of silver paid for the only land "
        "Abraham ever owns in the country God had promised him "
        "entirely, and a grave secured as legal possession standing "
        "as an act of faith that his family belongs there "
        "permanently"),
    "genesis24": (CLS,
        "the longest chapter in Genesis built entirely around finding "
        "a bride for a son who never leaves the land himself, a "
        "servant's prayer for a very specific sign answered before he "
        "has even finished speaking it, a young woman who does "
        "exactly what was prayed for without knowing she is being "
        "tested, a family's swift agreement that the thing proceeded "
        "from the LORD, and Isaac meditating in a field at evening "
        "before he ever sees the woman who will comfort him after his "
        "mother's death"),
    "genesis25": (CLS,
        "Abraham's death recorded at a hundred seventy-five in a good "
        "old age, an old man, and full of years, with Isaac and "
        "Ishmael burying him together despite the family's earlier "
        "rupture, twins struggling inside Rebekah before either is "
        "even born, a divine oracle declaring the elder shall serve "
        "the younger well before either child has done anything to "
        "deserve it, and a birthright traded away for a bowl of stew "
        "in a single sentence that calls it Esau's own despising of "
        "what he sold"),
    "genesis26": (CLS,
        "an entire chapter devoted to the quietest of the three "
        "patriarchs, a famine and a warning specifically not to go "
        "down into Egypt this time, Isaac repeating word for word his "
        "father's own she is my sister deception about the very same "
        "threat, wells re-dug and renamed exactly as Abraham had "
        "named them, contention and opposition finally giving way to "
        "a well called room because the LORD hath made room for us, "
        "and Esau's Hittite wives described as nothing but grief of "
        "mind to both his parents"),
    "genesis27": (CLS,
        "a blind and aging father planning to bless his firstborn in "
        "direct contradiction of an oracle given before either son "
        "was born, a mother's scheme disguising one son as another "
        "down to smell and touch, a lie repeated using God's own name "
        "to cover the deception, a blessing that trembles its way out "
        "of Isaac once he realizes what has happened and still cannot "
        "be recalled, and a family so fractured by the end of the "
        "chapter that a mother's few days apart from her favored son "
        "becomes twenty years she never sees him again"),
    "genesis28": (CLS,
        "a fugitive fleeing his own brother's murderous anger "
        "receiving, of all things, his father's deliberate blessing "
        "before he even leaves, a stairway reaching from earth to "
        "heaven with angels ascending and descending witnessed in a "
        "dream on a stone pillow, the Abrahamic promises repeated to "
        "a man who has done nothing yet to earn them, a startled "
        "confession, surely the LORD is in this place, and I knew it "
        "not, and a vow that is still conditional, phrased as if "
        "God's faithfulness were somehow still in question"),
    "genesis29": (CLS,
        "the deceiver who tricked his own father with a disguise now "
        "tricked himself by a veiled bride under cover of darkness, "
        "Laban's excuse that the younger is never given before the "
        "firstborn landing as an unmistakable echo of what Jacob did "
        "to Esau, fourteen years of service that felt to Jacob like "
        "only a few days because of his love for Rachel, an unloved "
        "wife whose womb God opens while her sister's remains closed, "
        "and Judah, the future tribe of David and of Christ, born "
        "specifically to the wife who was never the one Jacob "
        "wanted"),
    "genesis30": (CLS,
        "two sisters competing for children through their own maids "
        "as much as through themselves, mandrakes traded for a night "
        "with Jacob as though love itself had become a commodity, "
        "four more sons and a daughter born before God finally "
        "remembers Rachel and opens her own womb for Joseph, Jacob's "
        "wages negotiated around speckled and spotted animals only "
        "for Laban to strip the flock of them first, and selective "
        "breeding that leaves Jacob increasing exceedingly despite "
        "his father-in-law's repeated manipulation"),
    "genesis31": (CLS,
        "God's own command to return home arriving only after Laban's "
        "sons begin resenting Jacob's prosperity and Laban's own "
        "attitude visibly changes, twenty years of service recounted "
        "with wages changed ten separate times, a dream revealing it "
        "was God rather than any breeding trick that multiplied the "
        "flocks, Rachel's theft of her father's household gods left "
        "unexplained and undiscovered even during a direct search, "
        "and a covenant at Mizpah that settles into peace only after "
        "Jacob's own passionate defense of two decades of faithful, "
        "sacrificial labor"),
    "genesis32": (CLS,
        "angels meeting Jacob at the very moment he is about to face "
        "the brother he wronged twenty years earlier, a report that "
        "Esau is approaching with four hundred men driving Jacob to "
        "divide his own camp in fear, one of Scripture's finest "
        "prayers built on God's own command, Jacob's confessed "
        "unworthiness and a direct claim on God's promise, waves of "
        "gifts sent ahead in careful stages to appease a brother who "
        "has not yet spoken a word, and a nightlong wrestling match "
        "that leaves Jacob limping away with a new name, Israel, and "
        "a hip permanently marked by the encounter"),
    "genesis33": (CLS,
        "a long-dreaded reunion resolved not in violence but in an "
        "embrace, Esau running to meet the very brother who once "
        "stole his blessing, Jacob arranging his family by rank and "
        "then bowing seven times before a brother he still fears, "
        "both men independently declaring I have enough in the very "
        "same conversation, and an altar built at Shechem under a new "
        "name, El-elohe-Israel, the first time Jacob claims God "
        "specifically as his own rather than only as his father's"),
    "genesis34": (CLS,
        "a daughter violated by a prince who only afterward claims to "
        "love her, a father who hears of it and simply holds his "
        "peace rather than acting, sons who answer the negotiation "
        "deceitfully by demanding circumcision as the price of "
        "intermarriage, a massacre carried out on the very day the "
        "men of the city are most vulnerable from that same "
        "circumcision, and a chapter that closes with no resolution, "
        "Jacob rebuking his sons only for the danger they have "
        "created rather than for the wrong itself"),
    "genesis35": (CLS,
        "a twenty-year-old vow at last fulfilled when God commands "
        "Jacob back to Bethel, foreign idols and earrings surrendered "
        "and buried under an oak before the household even sets out, "
        "God's covenant and Jacob's new name, Israel, formally "
        "reaffirmed at the very place it was first given in a dream, "
        "Rachel dying in hard labor on the road and naming her son "
        "son of my sorrow before Jacob renames him son of my right "
        "hand, and Isaac's death closing the chapter with Esau and "
        "Jacob burying their father together despite everything that "
        "came between them"),
    "genesis36": (CLS,
        "an entire genealogical chapter devoted to Esau's line before "
        "the narrative turns permanently to Jacob's family, two "
        "brothers separating because the land cannot support both "
        "households' wealth just as Abraham and Lot once separated, "
        "fourteen chiefs of Edom listed by name, the earlier Horite "
        "inhabitants of Seir recorded before Esau's own line "
        "displaces them, and eight kings of Edom noted as reigning "
        "before Israel ever had a king of its own"),
    "genesis37": (CLS,
        "a coat of many colors given openly enough that every brother "
        "notices the favoritism behind it, two dreams of sheaves and "
        "stars that the brothers hear as a direct claim to rule over "
        "them, a father who rebukes the second dream yet quietly "
        "keeps turning it over in his mind, a pit and a rope of "
        "Ishmaelite traders substituted for the murder the brothers "
        "first planned, and a bloodied coat brought home to a father "
        "who is deceived into mourning a son who is still alive"),
    "genesis38": (CLS,
        "Judah separating from his brothers and marrying a Canaanite "
        "in the very chapter that interrupts Joseph's own story, two "
        "sons struck dead by God in succession for refusing the duty "
        "owed to their brother's widow, a father who withholds his "
        "third son out of fear and leaves Tamar without recourse, a "
        "disguise as a prostitute that succeeds where an honest "
        "request had already failed, and a signet, cord and staff "
        "produced as evidence that turns Judah's threat to burn her "
        "into a confession, she hath been more righteous than I"),
    "genesis39": (CLS,
        "a repeated refrain, the LORD was with Joseph, marking every "
        "stage of his rise in Potiphar's house and his fall into "
        "prison alike, total authority handed to a slave because his "
        "master can see whose blessing is on him, a temptation "
        "refused not for fear of consequences but because it would be "
        "sin against God, a garment left behind in flight that "
        "becomes the very evidence used to convict him falsely, and a "
        "prison sentence that somehow becomes another platform for "
        "the same blessing that built Potiphar's house"),
    "genesis40": (CLS,
        "a butler and a baker imprisoned together and troubled by "
        "dreams on the very same night, Joseph crediting God with "
        "interpretation before he has even heard what either man "
        "dreamed, three branches and three baskets both meaning three "
        "days but pointing toward opposite fates, an honest "
        "interpretation delivered even when the news is a hanging "
        "rather than a restoration, and a request to be remembered "
        "met, in the chapter's final line, with being simply "
        "forgotten"),
    "genesis41": (CLS,
        "thirteen years passing between a coat torn from Joseph's "
        "back and a ring placed on his hand, Pharaoh's magicians "
        "failing where a forgotten prisoner will soon succeed, a "
        "butler's sudden memory of his own fault reopening the door "
        "Joseph had been shut behind, an interpretation Joseph "
        "insists is not his own but God's, and two sons named "
        "Manasseh and Ephraim whose names together summarize "
        "forgetting the toil and being made fruitful in the very land "
        "of Joseph's affliction"),
    "genesis42": (CLS,
        "ten brothers bowing before a ruler they do not recognize, "
        "fulfilling a dream they mocked twenty years earlier, an "
        "accusation of spying that forces the very confession the "
        "brothers have avoided for two decades, we are verily guilty "
        "concerning our brother spoken while the accused stands "
        "listening in a language they think he cannot understand, "
        "money secretly returned to their sacks that terrifies rather "
        "than relieves them, and a father who refuses to risk his "
        "last favored son even as the family's survival depends on "
        "it"),
    "genesis43": (CLS,
        "a famine that finally forces Jacob's hand where fear alone "
        "could not, Judah offering himself as surety for Benjamin in "
        "the same breath that proves how far he has come from the "
        "brother who sold Joseph for silver, a steward's casual "
        "mention of the God of Israel as the source of the money's "
        "mysterious return, Joseph excusing himself to weep alone at "
        "the sight of his mother's other son, and brothers seated in "
        "the exact order of their birth by a host whose knowledge "
        "they cannot begin to explain"),
    "genesis44": (CLS,
        "a silver cup deliberately planted in the youngest brother's "
        "sack as the final test of whether these men have actually "
        "changed, a rash vow that whoever has it shall die spoken "
        "before anyone knows the cup will be found on Benjamin, torn "
        "clothes and a return to the city rather than the abandonment "
        "Joseph is testing for, Judah's extraordinary speech offering "
        "himself as a bondman in Benjamin's place, and a substitution "
        "that answers, without anyone realizing it, the very crime "
        "the brothers committed against Joseph himself twenty years "
        "earlier"),
    "genesis45": (CLS,
        "a revelation that comes only after Joseph can no longer "
        "restrain himself, weeping loudly enough that the Egyptians "
        "outside the room can hear it, three separate statements "
        "crediting God rather than the brothers for sending Joseph to "
        "Egypt, an invitation for the whole family to come down and "
        "be nourished through five more years of famine, a warning "
        "not to quarrel on the journey home tucked into an otherwise "
        "joyful sending-off, and a father whose spirit revives, the "
        "text switching his name from Jacob to Israel in the very "
        "same verse, at the news his son is alive"),
    "genesis46": (CLS,
        "a stop at Beer-sheba, the same place Abraham and Isaac once "
        "worshipped, before Jacob will take a single step further "
        "toward Egypt, God's doubled call, Jacob, Jacob, promising "
        "both to go down with him and to bring him back up again, a "
        "genealogy totaling exactly seventy souls entering Egypt, a "
        "number that echoes the seventy nations of chapter ten, and a "
        "reunion in which Joseph weeps on his father's neck a good "
        "while while Jacob says he can now die having seen his son's "
        "face"),
    "genesis47": (CLS,
        "five brothers coached to present themselves specifically as "
        "shepherds so Pharaoh will settle them apart in Goshen, Jacob "
        "blessing Pharaoh twice in an audience where the lesser is "
        "technically blessing the greater, a famine administration in "
        "which Joseph systematically buys up money, livestock, land "
        "and finally the people themselves for Pharaoh, a fixed "
        "twenty percent tax established afterward that leaves the "
        "people grateful rather than resentful, and a dying man's "
        "oath extracted from Joseph, hand under the thigh, to bury "
        "him in Canaan rather than in the land that saved his "
        "family's life"),
    "genesis48": (CLS,
        "two grandsons formally adopted as Jacob's own sons, "
        "elevating Joseph to a double portion no other son receives, "
        "a dying man's eyes too dim to see clearly yet his hands "
        "crossed deliberately rather than by accident, Joseph's "
        "protest at the crossed hands met with Jacob's own "
        "insistence, I know it, my son, I know it, a blessing "
        "formula, God make thee as Ephraim and as Manasseh, that "
        "becomes the standard blessing spoken over children for "
        "generations afterward, and the younger again placed above "
        "the elder in a pattern this book has repeated since Isaac "
        "and Ishmael"),
    "genesis49": (CLS,
        "twelve sons gathered to hear not farewells but futures, that "
        "which shall befall you in the last days, Reuben's birthright "
        "forfeited in a single sentence for defiling his father's "
        "bed, Simeon and Levi's violence at Shechem answered with a "
        "scattering that becomes judgment for one and blessing for "
        "the other, the Shiloh prophecy naming a coming ruler for "
        "whom the scepter will never actually depart from Judah, and "
        "a peaceful death described in its own quiet language, he "
        "gathered up his feet into the bed, and yielded up the "
        "ghost"),
    "genesis50": (CLS,
        "a father embalmed for forty days and mourned for seventy "
        "before a funeral procession of Egyptian officials, chariots "
        "and horsemen escorts his body all the way back to Canaan, "
        "brothers newly afraid of revenge the moment their father is "
        "gone, inventing or recalling a deathbed instruction to plead "
        "for mercy, Joseph's own theological summary of the entire "
        "book, ye thought evil against me, but God meant it unto "
        "good, a death at a hundred ten years old considered in "
        "Egyptian culture itself to be the ideal lifespan, and a "
        "coffin left waiting in Egypt on the strength of an oath that "
        "Genesis leaves entirely unresolved for four hundred years"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
