#!/usr/bin/env python3
"""Batch 22: Numbers 1-22, 24-36 (chapter 23 already has Key Themes).

    python3 add_key_themes_batch22.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "numbers1": (CLS,
        "a census confined to men twenty and older able to go to war, "
        "the largest tribe Judah counted first among the twelve even "
        "though the order follows something other than birth, Levites "
        "deliberately excluded from the military count and assigned "
        "instead to guard the Tabernacle itself, a death penalty "
        "attached to any outsider who comes too near the holy things, "
        "and a running total of over six hundred thousand fighting "
        "men taken exactly one month after the Tabernacle first "
        "stood"),
    "numbers2": (CLS,
        "four camps of three tribes each arranged on the four sides "
        "of a Tabernacle that never moves from the center, Judah "
        "given the position of honor facing the sunrise and the order "
        "to set out first, Reuben's camp marching second despite "
        "Reuben's own birthright long since forfeited, the Tabernacle "
        "and its Levites explicitly placed in the very middle of the "
        "formation, and a closing note that Israel did according to "
        "all that the LORD commanded, camp and march alike"),
    "numbers3": (CLS,
        "a priestly genealogy that opens by naming two sons and then "
        "removing them in the same breath, Nadab and Abihu dead "
        "without children, an entire tribe of Levites handed over to "
        "Aaron as a gift rather than hired as staff, redemption of "
        "the firstborn grounded explicitly in the night the LORD "
        "spared Israel's own firstborn in Egypt, three Levite clans "
        "assigned three different regions of the camp and three "
        "different sets of Tabernacle furniture to guard, and a "
        "public headcount that comes up two hundred seventy-three "
        "short, redeemed at five shekels a head rather than simply "
        "waived"),
    "numbers4": (CLS,
        "holy objects wrapped in a fixed sequence of coverings before "
        "the men assigned to carry them are even allowed to approach, "
        "a repeated warning that seeing or touching what is uncovered "
        "brings death even to the Levites entrusted with carrying it, "
        "tent pegs and frame pieces inventoried by name rather than "
        "merely by count, service age set uniformly at thirty to "
        "fifty across all three Levitical clans, and a total "
        "workforce of 8,580 each assigned according to his own "
        "burden"),
    "numbers5": (CLS,
        "three categories of uncleanness ordered entirely outside the "
        "camp because God himself dwells in its midst, restitution "
        "for wrongdoing requiring both confession and a payment "
        "increased by a fifth, sin against a person treated as sin "
        "against the LORD, an unusual test involving bitter water for "
        "a wife suspected but never caught, and a ritual that leaves "
        "the outcome entirely in God's hands rather than in any human "
        "witness's testimony"),
    "numbers6": (CLS,
        "a vow of consecration open to any Israelite of either sex "
        "rather than reserved to priest or Levite, three "
        "restrictions, no wine or anything from the grapevine, no "
        "razor, no contact with the dead, matching in severity what "
        "is normally expected only of the high priest, a defilement "
        "that resets the entire vow to its starting point rather than "
        "merely pausing it, hair grown throughout the vow finally "
        "burned as an offering at its completion, and a three-line "
        "blessing whose words the priests speak while God himself "
        "does the actual blessing"),
    "numbers7": (CLS,
        "the longest chapter in the book built around twelve "
        "offerings that are, deliberately, all identical, six wagons "
        "and twelve oxen distributed unevenly to Gershon and Merari "
        "for the loads they actually carry while the Kohathites "
        "receive none because their burden must be borne on the "
        "shoulder, one tribal leader presenting his gifts on each of "
        "twelve consecutive days in the same order the camp itself is "
        "arranged, silver plates, golden dishes and enough animals to "
        "run into the hundreds recorded in exhaustive, repetitive "
        "detail, and a closing verse in which Moses hears God's voice "
        "speaking from between the two cherubim once the dedication "
        "is complete"),
    "numbers8": (CLS,
        "seven lamps lit facing forward so the Holy Place is never "
        "served in darkness, a Levite cleansing ceremony involving "
        "sprinkled water, a full shave and washed clothes before a "
        "single duty is performed, the whole congregation laying "
        "hands on the Levites so the nation's own obligation is "
        "transferred to them, an age bracket running from twenty-five "
        "to fifty that narrows again after fifty into lighter guard "
        "duty rather than full retirement, and a repeated statement "
        "that the Levites exist to keep a plague from striking the "
        "people who come too near the sanctuary"),
    "numbers9": (CLS,
        "a second Passover kept exactly one year after the first, "
        "ceremonially unclean men who ask to be included rather than "
        "accepting exclusion, a provision built for the genuinely "
        "prevented and fenced against anyone merely unwilling, a "
        "cloud settling over the Tabernacle from the very day it is "
        "first raised, and a pattern repeated regardless of duration, "
        "whether the cloud lingers a night, a month or a year, they "
        "camp or march at the LORD's word and no other"),
    "numbers10": (CLS,
        "two silver trumpets whose different blasts distinguish a "
        "full assembly from a leaders' meeting and one tribal "
        "division's departure from another's, a strict rule that only "
        "Aaron's sons may sound them, a departure carried out in the "
        "exact camp order fixed two chapters earlier, an invitation "
        "to Hobab to serve as guide even while the cloud itself "
        "already leads the way, and a marching prayer Moses speaks "
        "each time the ark sets forward and each time it comes to "
        "rest"),
    "numbers11": (CLS,
        "a first complaint met with fire at the very edge of the "
        "camp, a craving for meat that turns nostalgic about food "
        "eaten as slaves, Moses pouring out a burden so heavy he asks "
        "to be killed rather than carry it, seventy elders suddenly "
        "prophesying once God's Spirit is distributed from what "
        "already rested on Moses, and quail piled so deep that the "
        "very craving that demanded them becomes the reason for a "
        "grave"),
    "numbers12": (CLS,
        "a challenge to Moses' authority disguised as a complaint "
        "about his marriage, a parenthetical statement calling Moses "
        "the meekest man on the face of the earth right where he "
        "might be expected to defend himself, God distinguishing "
        "Moses from every other prophet by speaking to him mouth to "
        "mouth rather than in visions, Miriam alone struck with "
        "leprosy while Aaron is spared, and the entire camp waiting "
        "seven days rather than leaving her outside it alone"),
    "numbers13": (CLS,
        "twelve tribal leaders sent to spy out a land already "
        "promised rather than merely rumored, a single cluster of "
        "grapes so large it takes two men on a pole to carry it back "
        "as evidence, an honest report of walled cities and giant "
        "inhabitants delivered alongside an evil report that slanders "
        "the land itself, Caleb alone silencing the crowd with we are "
        "well able to overcome it, and a self-description, we were in "
        "our own sight as grasshoppers, that determines the nation's "
        "theology more than anything actually seen in Canaan"),
    "numbers14": (CLS,
        "an entire congregation weeping all night and proposing to "
        "elect a new leader back to Egypt, Joshua and Caleb tearing "
        "their clothes and nearly stoned for insisting the land is "
        "good, an offer to make of Moses a greater nation refused by "
        "an intercessor arguing God's own reputation and God's own "
        "words back to him, a pardon granted that still leaves every "
        "numbered adult to die in the wilderness over the next forty "
        "years, and a presumptuous march into Canaan the very next "
        "day that fails precisely because it is attempted without the "
        "ark and without God"),
    "numbers15": (CLS,
        "a sentence of forty years' death opened, in its very next "
        "breath, with when ye be come into the land, grain and drink "
        "offerings scaled to whichever animal accompanies them, a "
        "single law repeated for native Israelite and resident "
        "stranger alike, a stark distinction drawn between "
        "unintentional sin that can be atoned for and a high-handed "
        "sin that cannot, a man stoned for gathering sticks on the "
        "Sabbath as the chapter's own illustration of that "
        "high-handed sin, and blue-corded tassels commanded on every "
        "garment's corner as a permanent visual reminder against the "
        "wandering heart"),
    "numbers16": (CLS,
        "a Kohathite Levite already entrusted with the holiest "
        "objects in Israel demanding the priesthood on top of it, a "
        "theology of all the congregation are holy twisted into a "
        "denial that God appoints specific leaders at all, Dathan and "
        "Abiram calling Egypt itself a land flowing with milk and "
        "honey rather than the slavery it was, the ground opening "
        "beneath three men's tents while fire consumes two hundred "
        "fifty more the very next moment, and censers salvaged from "
        "the dead and hammered into an altar covering that stands as "
        "a permanent warning rather than being discarded"),
    "numbers17": (CLS,
        "twelve rods laid before the ark overnight with each leader's "
        "own name carved into his, one rod alone sprouting, budding, "
        "blossoming and bearing ripe almonds in stages a living tree "
        "normally takes months to complete, eleven dead sticks "
        "returned to their owners beside the one that came alive, a "
        "rod preserved permanently as a token against the very rebels "
        "who no longer exist to see it, and a terrified people crying "
        "we die, we perish, we all perish after witnessing exactly "
        "what unauthorized approach costs"),
    "numbers18": (CLS,
        "an entire chapter addressed to Aaron directly rather than to "
        "Moses, priests and Levites literally bearing the iniquity of "
        "the sanctuary so ordinary Israelites do not, provisions "
        "listed in such detail, firstfruits, firstborn redemption, "
        "devoted things, that the priesthood's abundance is "
        "impossible to overlook, a declaration that God himself, not "
        "land, is Aaron's portion and inheritance, and a tithe of the "
        "tithe required even from the Levites who already live off "
        "everyone else's tithe"),
    "numbers19": (CLS,
        "a red heifer never yoked and without blemish burned entirely "
        "outside the camp rather than on the altar, ashes mixed with "
        "running water into what the text calls the water of "
        "separation, contact with a corpse, a bone or even a grave in "
        "an open field all defiling for seven days, the very act of "
        "sprinkling the purifying water leaving the one who sprinkles "
        "unclean until evening, and a refusal to be purified carrying "
        "the same penalty as defiling the sanctuary itself, being cut "
        "off"),
    "numbers20": (CLS,
        "Miriam's death recorded in a single unadorned sentence after "
        "decades of leading Israel in worship, water struck twice "
        "from a rock God had only commanded to be spoken to, a leader "
        "barred from the very land he has led an entire nation toward "
        "because of one act of disbelief before their eyes, a brother "
        "nation, Edom, refusing safe passage and turning the "
        "wilderness route into another delay, and Aaron's priestly "
        "garments stripped from him and placed on his son on a "
        "mountaintop before Aaron himself dies there"),
    "numbers21": (CLS,
        "the same battlefield, Hormah, that swallowed Israel's "
        "presumptuous attack in chapter fourteen now delivering its "
        "first real victory, fiery serpents sent in judgment for a "
        "complaint almost identical to complaints already judged a "
        "generation earlier, a bronze serpent lifted on a pole that "
        "Jesus himself later cites as his own pattern, a well-song "
        "breaking out the moment grumbling gives way to faith, and "
        "two kings, Sihon and Og, defeated in succession by the very "
        "generation once too frightened by giants to attempt it"),
    "numbers22": (CLS,
        "a Moabite king too frightened to fight Israel by the sword "
        "turning instead to a diviner four hundred miles away to "
        "curse it by words, a foreign prophet consulting the LORD not "
        "once but repeatedly in hope of a different answer, God's "
        "outward permission to go granted even while his anger burns "
        "at the reason Balaam wants to, a donkey seeing what her "
        "rider cannot and turning aside from an angel with a drawn "
        "sword three separate times, and a warning delivered through "
        "the donkey's own mouth before Balaam ever reaches the king "
        "who summoned him"),
    "numbers24": (CLS,
        "divination abandoned entirely as the Spirit of God comes "
        "upon Balaam directly for his third oracle, an oracle that "
        "pronounces Israel's own encampment beautiful before "
        "repeating the Abrahamic promise nearly word for word, a "
        "furious king dismissing the very prophet he paid, a final "
        "oracle offered unpaid that reaches past the immediate moment "
        "to a star out of Jacob and a sceptre out of Israel, and a "
        "prophet who departs having failed to curse Israel by word "
        "while already turning, unseen, toward the seduction chapter "
        "twenty-five will describe"),
    "numbers25": (CLS,
        "seduction succeeding at Baal-Peor where three chapters of "
        "failed curses could not, Israelite men yoking themselves to "
        "a local god through Moabite women's invitation to "
        "sacrificial feasts, a plague spreading through the camp even "
        "while the people weep openly at the Tabernacle entrance, a "
        "single spear thrust by Phinehas stopping the plague after "
        "twenty-four thousand have already died, and a covenant of "
        "peace and of an everlasting priesthood granted, "
        "paradoxically, to the man who acted with a spear rather than "
        "a word"),
    "numbers26": (CLS,
        "a second census taken only after the entire generation "
        "counted in the first has died exactly as decreed, a total of "
        "six hundred one thousand seven hundred thirty men landing "
        "within two thousand of the number counted thirty-eight years "
        "earlier, one tribe, Simeon, collapsing by well over half "
        "while others grow by tens of thousands, a parenthetical note "
        "that Korah's own sons did not die with their father, and a "
        "closing statement that of everyone once numbered only Caleb "
        "and Joshua remain alive to see it"),
    "numbers27": (CLS,
        "five sisters petitioning publicly for their dead father's "
        "inheritance because he left no son, a divine ruling that "
        "reshapes the law of inheritance rather than simply denying "
        "their claim, Moses told to view the promised land from a "
        "mountain he will never descend into, a request for a "
        "successor that asks only for a shepherd rather than for any "
        "concession to himself, and Joshua invested with some, not "
        "all, of Moses' authority, left dependent on the priest's "
        "oracle where Moses spoke with God face to face"),
    "numbers28": (CLS,
        "a daily offering called God's own bread offered morning and "
        "evening as the framework around which every other sacrifice "
        "is added, a Sabbath offering that doubles the daily rather "
        "than replacing it, a new moon offering scaled by exact "
        "fractions of an ephah and hin per animal, Passover and "
        "Unleavened Bread requiring seven straight days of the same "
        "enlarged offering while the household Passover lamb itself "
        "goes unmentioned, and Pentecost's new grain offering marking "
        "the wheat harvest as belonging first to God"),
    "numbers29": (CLS,
        "a first day of the seventh month set apart specifically for "
        "trumpet blasts, a tenth day requiring souls afflicted and no "
        "work at all, its public offerings kept explicitly separate "
        "from the more elaborate atonement ritual already given in "
        "Leviticus, a seven-day feast of booths whose bull count "
        "decreases by one each day, thirteen down to seven, for "
        "reasons the text never explains, an eighth day of quiet "
        "assembly following that abundance with a single bull, ram "
        "and seven lambs, and a total of one hundred eighty-nine "
        "animals accumulated across Sukkot's seven days alone"),
    "numbers30": (CLS,
        "vow law addressed to tribal leaders as a matter of communal "
        "governance rather than only private devotion, a man's own "
        "vow left with no possibility of annulment by anyone, a "
        "father or husband able to void a daughter's or wife's vow "
        "only on the very day he first hears of it, silence "
        "functioning as confirmation just as much as speech would, a "
        "widow or divorced woman's vow standing on its own with no "
        "household authority left to override it, and a husband who "
        "waits and then annuls late bearing her guilt himself rather "
        "than voiding anything"),
    "numbers31": (CLS,
        "a war explicitly named the LORD's vengeance on Midian rather "
        "than Israel's own, a force of only twelve thousand men sent "
        "under a priest rather than a general, Balaam found among the "
        "Midianite dead despite never having cursed Israel by a "
        "single word, Moses' fury at officers who spared the very "
        "women identified as the architects of Baal-Peor, plunder "
        "divided by a fixed ratio that gives the Levites ten times "
        "the priests' proportional share, and a report that not one "
        "Israelite soldier is missing, answered with a freewill "
        "offering of gold given in thanksgiving rather than atonement "
        "for sin"),
    "numbers32": (CLS,
        "Reuben and Gad requesting land east of the Jordan for the "
        "sake of their livestock before a single tribe west of the "
        "river has received its own inheritance, Moses drawing a "
        "direct line back to the ten spies and the forty years their "
        "unbelief cost the nation, a compromise in which the two "
        "tribes agree to cross armed and fight until every other "
        "tribe is settled before returning home, a warning that sin, "
        "even when it looks like a reasonable request, will find you "
        "out, and Manasseh entering the narrative only at the "
        "settlement itself, splitting a tribe already counted as one"),
    "numbers33": (CLS,
        "forty-two stations written down by Moses at God's own "
        "command rather than left to memory, an itinerary from Egypt "
        "to Sinai covering roughly two months while the following "
        "thirty-eight years of wandering are compressed into a bare "
        "list of names, Aaron's death recorded here a second time "
        "with his exact age given, one hundred twenty-three, an "
        "instruction to destroy every carved and molten image in "
        "Canaan rather than merely displace its people, and a warning "
        "that whatever inhabitants Israel fails to drive out will "
        "become thorns in their sides and eventually draw down on "
        "Israel the very judgment intended for them"),
    "numbers34": (CLS,
        "precise borders drawn by God rather than left to conquest to "
        "define, a southern line running through the Wilderness of "
        "Zin and the Brook of Egypt to the Mediterranean, a western "
        "border stated in a single phrase, the Great Sea, a northern "
        "extent reaching to Lebo-hamath that later becomes the "
        "standard measure of Israel's ideal territory, and named "
        "overseers, Caleb among them, appointed to divide land he "
        "first believed in as a young spy forty years before he ever "
        "gets to allot it"),
    "numbers35": (CLS,
        "forty-eight Levitical cities distributed proportionally by "
        "every tribe rather than granted as a single inheritance, six "
        "of those forty-eight set apart specifically as cities of "
        "refuge, three on each side of the Jordan, murder "
        "distinguished from manslaughter by weapon, motive and "
        "premeditation rather than by outcome alone, a manslayer's "
        "confinement bound not to a fixed term of years but to the "
        "unpredictable death of the high priest, and a closing "
        "rationale that ties every safeguard in the chapter to the "
        "single fact that the LORD himself dwells among the people"),
    "numbers36": (CLS,
        "tribal leaders raising a problem chapter twenty-seven's "
        "ruling left unresolved, land passing permanently out of a "
        "tribe if an inheriting daughter marries outside it, God "
        "affirming the concern exactly as he had affirmed the "
        "daughters' own claim two chapters earlier, a solution that "
        "grants freedom to choose a husband while still requiring the "
        "choice fall within the father's own tribe, and a closing "
        "verse that names itself as the summary not only of this "
        "chapter but of everything commanded on the plains of Moab"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
