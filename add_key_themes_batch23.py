#!/usr/bin/env python3
"""Batch 23: Deuteronomy 1-34, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch23.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "deuteronomy1": (CLS,
        "an eleven-day journey remembered as a forty-year one before "
        "the address even properly begins, a whole land already "
        "described in its fullness, hill country, coast, Lebanon, "
        "before a single step toward it is described, judges "
        "appointed the same way Jethro once counseled but retold now "
        "as Moses' own decision, a rebellion at Kadesh-barnea blamed "
        "on brothers who melted the people's hearts with reports of "
        "giants, and a presumptuous attack the morning after "
        "repentance that fails precisely because God says I am not "
        "among you"),
    "deuteronomy2": (CLS,
        "thirty-eight years of wandering compressed into a handful of "
        "verses ending at a single named brook, three separate "
        "nations, Edom, Moab and Ammon, that Israel is explicitly "
        "forbidden to attack because God gave their land to someone "
        "else first, parenthetical notes about vanished giants "
        "elsewhere proving God has displaced whole peoples before, a "
        "chilling statement that the hand of the LORD was actively "
        "against the old generation rather than merely letting them "
        "die, and a hardened Sihon whose refusal to grant passage is "
        "credited directly to God rather than to the king's own "
        "stubbornness alone"),
    "deuteronomy3": (CLS,
        "a giant king's iron bed preserved as physical evidence long "
        "after the giant himself is gone, sixty fortified cities "
        "taken from Bashan in a single campaign, land distributed to "
        "two and a half tribes on the explicit condition that their "
        "warriors first help conquer everyone else's, a charge to "
        "Joshua grounded entirely in what his own eyes have already "
        "witnessed done to two kings, and Moses' plea to cross over "
        "refused so completely that God tells him not to raise the "
        "subject again"),
    "deuteronomy4": (CLS,
        "a covenant explained rather than merely repeated for a "
        "generation that mostly never heard it delivered at Horeb, a "
        "nation asked whether any other people has a god so near or "
        "laws so righteous, no image permitted of anything because "
        "Israel heard only a voice at the mountain and saw no form to "
        "copy, exile foretold for a generation not yet born alongside "
        "a promise that seeking God with all the heart will still "
        "find him even there, and three cities of refuge set apart "
        "east of the Jordan in the very middle of an otherwise "
        "theological address"),
    "deuteronomy5": (CLS,
        "a covenant Moses insists was made not with the dead fathers "
        "but with the very people standing there that day, the Ten "
        "Commandments restated nearly word for word from Sinai with "
        "the Sabbath's reason changed to remembering slavery in "
        "Egypt, God adding no more once the ten words are spoken, a "
        "people who beg Moses to mediate rather than hear the voice "
        "directly a second time, and God's own longing, spoken aloud, "
        "that the heart behind their promise could actually keep it"),
    "deuteronomy6": (CLS,
        "the Shema, hear O Israel, the LORD our God is one, standing "
        "as the single sentence Jesus later calls the first and "
        "greatest commandment, God's words commanded into every "
        "posture of daily life, sitting, walking, lying down, rising, "
        "cities and vineyards and wells Israel will inherit without "
        "having built any of them, a specific warning that a full "
        "stomach breeds a forgetful heart, and a father's answer to a "
        "child's question about the law told entirely as the story of "
        "slavery and rescue rather than as abstract instruction"),
    "deuteronomy7": (CLS,
        "seven named nations marked for complete destruction not from "
        "ethnic hatred but to prevent Israel's own children being "
        "turned to other gods, Israel's election traced to nothing in "
        "Israel itself, they were the fewest of all peoples, but to "
        "God's own love and an oath sworn long before, blessing "
        "promised on flocks, children and harvest with no barrenness "
        "among them, a command not to fear because the same God who "
        "plagued Egypt is the one going ahead of them, and gold "
        "stripped from idols specifically forbidden because desiring "
        "it risks becoming devoted to destruction along with the "
        "image itself"),
    "deuteronomy8": (CLS,
        "forty years of wilderness reinterpreted as education rather "
        "than punishment, hunger deliberately allowed before manna is "
        "given so the lesson of dependence can land, a good land "
        "described in such lavish detail, brooks, wheat, honey, iron "
        "in the stones, that its abundance itself becomes the coming "
        "danger, a warning that a full stomach and a lifted heart "
        "tend to forget the God who filled it, and a reminder that "
        "even the power to get wealth is itself God's gift rather "
        "than a man's own achievement"),
    "deuteronomy9": (CLS,
        "a warning issued in advance against ever crediting the "
        "conquest to Israel's own righteousness, the same claim "
        "demolished three times in three consecutive verses, a golden "
        "calf built at the very base of the mountain where the law "
        "was still being written above them, an offer to make of "
        "Moses a greater nation refused by an intercessor who appeals "
        "only to God's own reputation among the nations, and a "
        "catalog of rebellion, Taberah, Massah, Kibroth-hattaavah, "
        "Kadesh-barnea, summarized bluntly as a pattern rather than a "
        "series of isolated lapses"),
    "deuteronomy10": (CLS,
        "new tablets cut and carried up the mountain a second time "
        "after Moses himself broke the first pair, Levi set apart at "
        "this point in the story specifically to carry the ark rather "
        "than to inherit land, five requirements condensed into a "
        "single rhetorical question, what doth the LORD thy God "
        "require of thee, a demand to circumcise the heart itself "
        "rather than only the flesh, and God's own impartiality "
        "toward the fatherless, the widow and the stranger offered as "
        "the direct model for how Israel is to treat the stranger "
        "among them"),
    "deuteronomy11": (CLS,
        "an appeal addressed specifically to those who personally "
        "witnessed the plagues and the Red Sea rather than to their "
        "children, a land explicitly contrasted with Egypt because it "
        "depends on rain from heaven rather than on foot-worked "
        "irrigation canals, blessing and rain tied to obedience so "
        "directly that the same God who sends one can withhold the "
        "other, teaching commands nearly repeated word for word from "
        "chapter six's Shema, and a blessing and a curse set on two "
        "facing mountains before Israel has even crossed the river to "
        "reach them"),
    "deuteronomy12": (CLS,
        "every pagan worship site marked for total destruction, "
        "altars torn down, pillars broken, names erased, before a "
        "single word is said about how Israel itself should worship, "
        "a single chosen place established in deliberate contrast to "
        "every man doing what is right in his own eyes, ordinary meat "
        "permitted to be slaughtered locally for food while tithes, "
        "firstlings and vows are reserved strictly for the chosen "
        "place, a warning not to forsake the Levite repeated inside "
        "the very laws that seem to make room for eating apart from "
        "him, and a prohibition on drinking blood stated three times "
        "in eleven verses as though it were the instruction most "
        "often broken"),
    "deuteronomy13": (CLS,
        "a prophet whose predicted sign actually comes true still to "
        "be rejected if it leads toward another god, five separate "
        "negatives, no consent, no listening, no pity, no sparing, no "
        "concealing, aimed at the very closest relationships, a "
        "brother, a child, a wife, a friend as one's own soul, an "
        "entire city subject to complete destruction only after "
        "diligent inquiry and confirmed proof, plunder burned rather "
        "than kept so the city becomes a permanent heap never "
        "rebuilt, and a stated purpose in every case that God's own "
        "fierce anger be turned away from the whole nation"),
    "deuteronomy14": (CLS,
        "an identity, ye are the children of the LORD your God, given "
        "before a single food law is stated, pagan mourning "
        "practices, cutting the body and shaving the head for the "
        "dead, forbidden specifically because Israel belongs to God "
        "rather than to grief's usual customs, the same clean and "
        "unclean animal categories from Leviticus repeated for a new "
        "generation, a tithe eaten joyfully before the LORD at the "
        "chosen place or converted to money and spent there on "
        "whatever the soul desires, and a third-year tithe that stays "
        "entirely local, feeding the Levite, the stranger, the "
        "fatherless and the widow until they are satisfied"),
    "deuteronomy15": (CLS,
        "a debt release every seven years described as belonging to "
        "the LORD rather than merely to the calendar, an ideal of no "
        "poor among you made explicitly conditional on obedience "
        "rather than promised outright, a warning against the wicked "
        "thought that calculates the release year before deciding "
        "whether to lend, a Hebrew servant sent away in the seventh "
        "year not empty-handed but liberally furnished from flock, "
        "floor and winepress, and a firstling animal that belongs to "
        "God unless blemished, in which case it becomes ordinary food "
        "rather than an acceptable offering"),
    "deuteronomy16": (CLS,
        "three pilgrimage feasts, Passover, Weeks and Tabernacles, "
        "each requiring every male to appear at the one chosen place "
        "rather than nowhere in particular, unleavened bread eaten "
        "specifically because Israel left Egypt in haste, giving "
        "scaled proportionally to each man's own blessing rather than "
        "fixed to a flat amount, judges commanded three times over, "
        "no perverted judgment, no partiality, no bribes, in "
        "successive clauses, and a closing prohibition on planting "
        "any tree or setting up any pillar beside the altar of the "
        "LORD"),
    "deuteronomy17": (CLS,
        "a blemished sacrifice called an abomination before a single "
        "word is said about human justice, idolaters prosecuted only "
        "after diligent inquiry and only on the testimony of two or "
        "three witnesses rather than one, the accusing witnesses "
        "required to throw the first stones themselves, a supreme "
        "court at the chosen place binding local judges who otherwise "
        "face a case too hard for them, and a king permitted only on "
        "the condition that he neither multiply horses, nor wives, "
        "nor silver and gold to himself"),
    "deuteronomy18": (CLS,
        "an entire tribe left with no land inheritance because the "
        "LORD himself is stated to be their inheritance, a list of "
        "forbidden occult practices, divination, sorcery, necromancy "
        "and child sacrifice, running to eight distinct terms in two "
        "verses, a promised prophet like Moses raised up from among "
        "Israel's own brethren rather than from any foreign source, "
        "that promise traced directly back to the people's own "
        "request at Horeb not to hear God's voice again, and a test "
        "for any prophet's claim resting entirely on whether the word "
        "actually comes to pass"),
    "deuteronomy19": (CLS,
        "roads and equal spacing commanded to the cities of refuge so "
        "that distance itself never determines a man's guilt, the "
        "same refuge explicitly denied to anyone who lies in wait out "
        "of hatred rather than kills by accident, a boundary stone "
        "protected by law as though moving it were theft of land "
        "itself, a rule that no one may be convicted of any offense "
        "on a single witness's word alone, and a false witness "
        "sentenced to suffer exactly what he intended for his victim "
        "rather than any lesser penalty"),
    "deuteronomy20": (CLS,
        "a priest, not a general, addressing the army before battle "
        "with a fourfold command against fear, four separate "
        "exemptions sending home the man with an undedicated house, "
        "an unharvested vineyard, an unconsummated betrothal or a "
        "fearful heart, peace offered to distant cities before any "
        "siege begins, total destruction reserved specifically for "
        "the Canaanite nations so their example cannot teach Israel "
        "their abominations, and a prohibition on cutting down fruit "
        "trees during a siege framed as a question, are the trees of "
        "the field human, that they should be attacked"),
    "deuteronomy21": (CLS,
        "an unsolved murder answered by a heifer ceremony performed "
        "by the nearest city's elders rather than left unaddressed, a "
        "captive woman granted a full month to mourn her parents "
        "before any marriage and, if later unwanted, released rather "
        "than sold, a firstborn son's double portion protected from a "
        "father's favoritism toward a more beloved wife's child, a "
        "rebellious son brought to public elders only after both "
        "parents agree and prior discipline has already failed, and "
        "an executed body required to be buried the same day rather "
        "than left hanging overnight"),
    "deuteronomy22": (CLS,
        "a neighbor's stray ox or lost garment that cannot simply be "
        "ignored, an active duty to help lift a fallen animal rather "
        "than merely avoiding harm, a roof railing required "
        "specifically so a fall does not bring blood on the builder's "
        "own house, mixed seed, mixed plowing animals and mixed "
        "fabric all forbidden as a single teaching in maintaining "
        "distinctions, and a betrothed woman's cry in the city "
        "weighed against her silence in the open field to determine "
        "guilt in a case of assault"),
    "deuteronomy23": (CLS,
        "emasculated men, those of illegitimate birth, and Ammonites "
        "and Moabites permanently barred from the assembly while "
        "Edomites and Egyptians are readmitted after only three "
        "generations, camp sanitation regulated down to a tool for "
        "covering waste because the LORD himself is said to walk in "
        "the camp, an escaped slave deliberately protected from being "
        "returned to his master rather than handed back, a vow left "
        "optional to make but binding the moment it is spoken, and "
        "hunger in a neighbor's field permitted to be satisfied by "
        "hand while a sickle or a container crosses the line into "
        "theft"),
    "deuteronomy24": (CLS,
        "a divorce law that regulates rather than commands the "
        "practice, forbidding a woman's return to her first husband "
        "once she has remarried, a full year exempted from war and "
        "public duty for a newly married man so he can, in the "
        "text's own words, cheer up his wife, a millstone forbidden "
        "as collateral because taking it takes a man's very "
        "livelihood, kidnapping for sale punished by death as one of "
        "the sternest anti-slavery statements in the entire law, and "
        "gleanings from grain, olives and grapes left deliberately "
        "unharvested a second time for the stranger, the fatherless "
        "and the widow"),
    "deuteronomy25": (CLS,
        "a limit of forty stripes on corporal punishment specifically "
        "so the punished man is not degraded beyond recognition as a "
        "brother, an ox permitted to eat while it treads the grain "
        "rather than being muzzled through its labor, levirate "
        "marriage requiring a surviving brother to raise up his dead "
        "brother's name, a refusal met with public shame, a sandal "
        "removed and spit in the face, honest weights tied directly "
        "to how long the nation itself will endure in the land, and a "
        "command to remember Amalek's attack on the weak stragglers "
        "specifically so that memory can be blotted out"),
    "deuteronomy26": (CLS,
        "a firstfruits ceremony that only begins once Israel is "
        "actually settled in the land, a worshipper's confession "
        "opening with a Syrian ready to perish was my father and "
        "moving through slavery, deliverance and gift in a handful of "
        "verses, a third-year tithe declaration built around three "
        "negatives affirming the offering was never touched in "
        "mourning or given for the dead, God and Israel described as "
        "mutually avouching each other on the very same day, and a "
        "closing promise that Israel will be set high above all "
        "nations in praise, name and honor"),
    "deuteronomy27": (CLS,
        "great stones plastered and inscribed with the entire law set "
        "up specifically on Ebal, the mountain of cursing, rather "
        "than Gerizim, an altar of uncut stones built alongside those "
        "inscribed stones with no iron tool ever lifted against them, "
        "a formal declaration that this very day Israel has become "
        "the people of the LORD, six tribes standing on each of two "
        "facing mountains for blessing and for cursing, and twelve "
        "curses pronounced one after another with the whole people "
        "answering Amen to each in turn"),
    "deuteronomy28": (CLS,
        "fourteen verses of blessing set against fifty-four verses of "
        "curse, a structural imbalance that already forecasts which "
        "path Moses expects Israel to take, blessing promised in the "
        "city and the field, coming in and going out, everywhere "
        "without exception, a siege prophecy specific enough to name "
        "a nation from the end of the earth whose language Israel "
        "will not understand, cannibalism during that siege described "
        "in language too graphic to soften, and curses that mirror "
        "the blessings point for point, reversing every promise of "
        "the chapter's opening verses"),
    "deuteronomy29": (CLS,
        "a covenant explicitly distinguished from the one made at "
        "Horeb rather than a mere repetition of it, evidence for that "
        "covenant drawn from forty years of clothes and shoes that "
        "never wore out rather than from any new miracle, an "
        "admission that Israel saw everything yet was given no heart "
        "to perceive, no eyes to see, no ears to hear until this very "
        "day, a covenant scope stretching from tribal leaders down to "
        "the hewer of wood and the drawer of water and reaching "
        "forward to those not yet born, and a boundary drawn between "
        "secret things that belong to God alone and revealed things "
        "that belong to Israel and its children forever"),
    "deuteronomy30": (CLS,
        "restoration promised even from the outmost parts of heaven "
        "once a scattered people calls the blessing and the curse to "
        "mind and returns with all the heart, a commandment described "
        "as neither too high to reach nor too far across the sea to "
        "fetch but already near, in the mouth and in the heart, a "
        "stark binary set before the nation, life and good against "
        "death and evil, heaven and earth called formally to witness "
        "the choice being offered, and a final appeal reduced to two "
        "words, choose life, addressed to the seed as much as to the "
        "generation actually listening"),
    "deuteronomy31": (CLS,
        "a leader at one hundred twenty admitting plainly that he can "
        "no longer go out and come in, the same charge, be strong and "
        "of a good courage, given first to the whole nation and then "
        "to Joshua personally, a written law entrusted to the priests "
        "with instructions for public reading every seven years to "
        "men, women, children and the stranger alike, a divine "
        "forecast of apostasy delivered in the tabernacle before "
        "Moses has even finished speaking to the people, and a song "
        "commanded specifically as a witness because a nation can "
        "always claim it forgot a law but never so easily forget a "
        "song"),
    "deuteronomy32": (CLS,
        "heaven and earth summoned as witnesses that will outlast the "
        "audience actually listening, God pictured first as a "
        "faithful rock of perfect work before Israel is ever called a "
        "perverse and crooked generation, an eagle stirring her nest "
        "as the image for how God found and carried Israel through "
        "the wilderness, Jeshurun growing fat and kicking against the "
        "very God who fed it, and a closing declaration, see now that "
        "I, even I, am he, that leaves no room for any rival power to "
        "claim credit for either wound or healing"),
    "deuteronomy33": (CLS,
        "a dying leader's blessing on all twelve tribes given as his "
        "very last recorded words, Reuben's blessing reduced to bare "
        "survival rather than the prominence his birthright once "
        "promised, Levi praised specifically for choosing covenant "
        "loyalty over family ties at the golden calf, Joseph "
        "receiving by far the longest and most lavish blessing of "
        "precious things from heaven and earth alike, and a closing "
        "hymn calling Israel happy above every other nation precisely "
        "because no other people has a God who rides to their help "
        "across the sky"),
    "deuteronomy34": (CLS,
        "a single mountain vantage point from which God shows Moses "
        "the entire land he will never set foot in, a death described "
        "as happening according to the word of the LORD and a burial "
        "performed by God himself in a grave no one has ever located, "
        "an old man whose eye was not dim nor his strength abated "
        "even at the moment of death, Joshua's authority established "
        "through the laying on of Moses' own hands, and a closing "
        "obituary insisting no prophet since has known the LORD face "
        "to face the way Moses did"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
