#!/usr/bin/env python3
"""Batch 20: Exodus 1-7, 11-30 (chapters 8-10 and 31-40 already have Key Themes).

    python3 add_key_themes_batch20.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "exodus1": (CLS,
        "five verbs of growth in one verse echoing both the creation "
        "mandate and the promise to Abraham, a dynasty change "
        "introduced as a king who did not know Joseph, oppression "
        "that backfires so badly that affliction only multiplies the "
        "people further, two midwives who fear God enough to lie to a "
        "king and are given houses for it, and a decree escalating "
        "from forced labor to a river-drowning order for every son "
        "born"),
    "exodus2": (CLS,
        "eighty years of a life compressed into twenty-five verses, an "
        "ark built for a baby using the same word Genesis used for "
        "Noah's vessel, a rescue engineered by a sister who positions "
        "her own mother to be hired as the nurse, a premature "
        "deliverance by the sword answered by a countryman's question "
        "of who made him judge, and a cry that goes unanswered until "
        "four verbs in two verses record God hearing, remembering, "
        "looking and having respect"),
    "exodus3": (CLS,
        "a bush that burns without being consumed, ground made holy "
        "by presence rather than by any quality of the dirt itself, a "
        "name whose form deflects definition back onto God's own "
        "self-existence, a first objection about identity answered "
        "not with reassurance about Moses but with a promise of "
        "accompaniment, and instructions for a request Pharaoh is "
        "already expected to refuse"),
    "exodus4": (CLS,
        "three signs matched to three objections, a rod, a hand and "
        "river water, a question about who made the mouth thrown back "
        "at a man who says he cannot speak, an anger kindled only "
        "after the plain request to send someone else, a firstborn "
        "son named as Israel's identity before a single plague has "
        "fallen on Egypt's own firstborn, and a night attack turned "
        "back only when a wife performs the circumcision her husband "
        "had neglected"),
    "exodus5": (CLS,
        "a first audience with Pharaoh answered by the question of "
        "who the LORD even is, a labor quota left standing while the "
        "raw material for meeting it is withdrawn, foremen beaten for "
        "a shortfall created by the order itself, the very people who "
        "had bowed in worship two chapters earlier now cursing the "
        "man sent to deliver them, and a prayer that accuses God of "
        "making things worse rather than better"),
    "exodus6": (CLS,
        "a name given a fuller unveiling than the patriarchs "
        "themselves received, seven first-person promises stacked one "
        "after another as though redemption were a single continuous "
        "sentence, a people too crushed by their own bondage to hear "
        "good news when it is spoken to them, a lineage inserted "
        "mid-narrative to certify exactly who this Moses and this "
        "Aaron are, and an objection recycled almost word for word "
        "from a few verses earlier as though nothing had changed at "
        "all"),
    "exodus7": (CLS,
        "a relationship defined in terms of authority before a single "
        "word is spoken to Pharaoh, a rod that becomes a serpent and "
        "then swallows the serpents produced by rival magic, "
        "imitation power that can reproduce a plague but not reverse "
        "it, a river turned to blood on the very site where Hebrew "
        "infants were once drowned, and a hardening named as both "
        "Pharaoh's own act and God's declared intention beforehand"),
    "exodus11": (CLS,
        "one plague announced as the last, back wages requested in "
        "silver and gold for four centuries of unpaid labor, a coming "
        "distinction so exact that not even a dog barks on Israel's "
        "side of it, a warning delivered and then a departure made in "
        "great anger, and a hardening reaffirmed as the reason the "
        "wonders had to be multiplied at all"),
    "exodus12": (CLS,
        "a calendar reset so that redemption itself becomes Israel's "
        "new starting point, a lamb selected on the tenth and killed "
        "on the fourteenth without a bone broken, blood applied to a "
        "doorframe as the one thing that turns judgment aside, a meal "
        "eaten in traveling clothes with a staff already in hand, and "
        "an exodus of some six hundred thousand men executed to the "
        "very day four hundred thirty years after the sojourn began"),
    "exodus13": (CLS,
        "a firstborn claimed as God's own on the strength of "
        "firstborns once spared, a longer road chosen deliberately "
        "because the shorter one led past a war the people were not "
        "ready to face, a coffin carried the length of a wilderness "
        "journey to answer a four-hundred-year-old oath, a father "
        "instructed to answer his son's question with the whole story "
        "rather than a short answer, and a pillar of cloud and fire "
        "that never once leaves its post"),
    "exodus14": (CLS,
        "a camp positioned to look trapped so that a king's "
        "confidence would be his own undoing, a command to stop "
        "crying out and start marching forward, a wind that blows all "
        "night to open what a hand merely gestures toward, chariot "
        "wheels that come off mid-pursuit as the army realizes too "
        "late whom it is actually fighting, and a shoreline left with "
        "not so much as one soldier surviving"),
    "exodus15": (CLS,
        "a song sung on a shore still littered with the wreckage of "
        "an army, praise moving from a single victory outward to "
        "nations who have not yet even heard the news, water made "
        "undrinkable three days after the greatest deliverance in the "
        "nation's history, a tree shown by God turning bitterness "
        "sweet, and a conditional promise attaching Israel's health "
        "to nothing more complicated than listening"),
    "exodus16": (CLS,
        "a month out from slavery and already the flesh pots of Egypt "
        "remembered more fondly than the whip, bread provided daily "
        "as both gift and test of whether the law will be walked in, "
        "a portion doubled on the sixth day so the seventh can be "
        "kept without gathering, manna spoiling overnight for the "
        "greedy but keeping perfectly for the obedient, and a jar of "
        "it preserved before the LORD long after the taste itself is "
        "gone"),
    "exodus17": (CLS,
        "water struck from a rock that God says he will be standing "
        "on when it is struck, a place named twice for the same "
        "complaint, once for testing and once for quarreling, a "
        "battle whose outcome tracks not the sword in the valley but "
        "a pair of raised hands on the hill, arms grown too heavy to "
        "hold up without two men bracing them on a stone, and an "
        "altar named the LORD is my banner over an enemy marked for a "
        "hostility God intends to outlast the generation"),
    "exodus18": (CLS,
        "a father-in-law's visit turning into the clearest lesson in "
        "Scripture on delegation, a whole nation waiting from morning "
        "to evening for one man's judgment, an outsider's blunt "
        "diagnosis that the thing Moses is doing is not good and will "
        "wear him away, a fourfold qualification for leaders, able, "
        "God-fearing, truthful and free of covetousness, and a tiered "
        "structure of judges over thousands, hundreds, fifties and "
        "tens that Moses adopts without argument"),
    "exodus19": (CLS,
        "an arrival at the very mountain where the bush once burned, "
        "fulfilling a promise made to Moses before he ever returned "
        "to Egypt, an offer framed as identity before it is framed as "
        "obligation, eagles' wings before commandments, a people's "
        "unanimous yes given before they have heard a single specific "
        "term, boundaries set around the mountain making nearness "
        "lethal rather than casual, and thunder, fire and trumpet "
        "turning what had been a private vision into a whole camp's "
        "trembling"),
    "exodus20": (CLS,
        "words spoken audibly to an entire nation rather than "
        "delivered through an intermediary, a preamble of rescue "
        "placed before a single command is given, four commandments "
        "ordering the relationship with God followed by six ordering "
        "relationships with neighbors, prohibitions reduced in places "
        "to two or three words with no case law attached to soften "
        "them, and a request from the people themselves to let Moses "
        "stand between them and a voice too terrifying to hear "
        "directly"),
    "exodus21": (CLS,
        "case law applying the commandments to disputes an agrarian "
        "society would actually face, a servant who may choose "
        "permanent bondage marked by a pierced ear at the doorpost, a "
        "sharp line drawn between premeditated murder and accidental "
        "killing by whether a city of refuge is available, eye for "
        "eye and tooth for tooth set as a ceiling on retaliation "
        "rather than a floor, and an ox's owner made liable only once "
        "negligence has already been demonstrated before"),
    "exodus22": (CLS,
        "restitution scaled to the animal and its recoverability, "
        "four-fold for a sheep and five-fold for an ox already sold, "
        "capital penalties reserved for sorcery, bestiality and "
        "sacrifice to other gods, a repeated appeal to Israel's own "
        "memory of being strangers as the reason to treat strangers "
        "well, a widow's or orphan's cry promised a direct hearing "
        "from God himself, and a cloak taken in pledge required back "
        "by sunset because it is the only covering its owner has"),
    "exodus23": (CLS,
        "false witness and majority pressure treated as equally "
        "corrupting to justice, an obligation to help even an "
        "enemy's struggling animal, a sabbath year that lets the land "
        "itself rest while the poor eat what grows unattended, three "
        "annual pilgrimage feasts marking the agricultural and "
        "redemptive calendar, and a conquest promised gradually, "
        "little by little, so the land is not left desolate faster "
        "than the people can fill it"),
    "exodus24": (CLS,
        "a covenant sealed with blood divided between an altar and a "
        "crowd, half on one and half thrown on the other, tying both "
        "parties into a single agreement, seventy-four elders who see "
        "God and are simply not struck down for it, a pavement like "
        "sapphire described beneath his feet, a book of the covenant "
        "read aloud and answered a second time with the same pledge "
        "to obey, and a forty-day ascent into a cloud that from below "
        "looks like devouring fire"),
    "exodus25": (CLS,
        "a sanctuary requested only from those who give willingly, "
        "materials from gold to acacia wood listed before a single "
        "instruction on assembly, an ark whose two cherubim face each "
        "other and look down at the very spot God promises to meet "
        "Moses, bread kept perpetually before God's presence "
        "representing all twelve tribes at once, and a lampstand "
        "hammered from one solid piece of gold rather than assembled "
        "from parts"),
    "exodus26": (CLS,
        "ten inner curtains joined by fifty gold clasps into what the "
        "text insists on calling one tabernacle, four successive "
        "layers of covering moving from woven cherubim inward to "
        "weatherproof skins outward, a framework of gilded acacia "
        "standing in silver sockets on three sides, a veil separating "
        "the holy place from the most holy strong enough that its "
        "tearing at the crucifixion carries the weight the Gospels "
        "give it, and an entrance screen embroidered in the same "
        "three colors as the veil it stands apart from"),
    "exodus27": (CLS,
        "a bronze altar with horns on each corner positioned as the "
        "very first thing anyone entering the courtyard would meet, a "
        "courtyard whose linen walls run a hundred fifty feet by "
        "seventy-five and stand only shoulder height, a single gate "
        "on the east side as the only way in, oil kept burning from "
        "evening to morning as a standing statute rather than an "
        "occasional observance, and every measurement repeatedly tied "
        "back to the pattern shown to Moses on the mountain rather "
        "than to any craftsman's own design"),
    "exodus28": (CLS,
        "garments made for glory and for beauty rather than for "
        "utility alone, two shoulder stones and twelve breastplate "
        "stones carrying the whole nation's names into the priest's "
        "presence with God, bells and pomegranates alternating on a "
        "robe's hem so the priest's movement inside the holy place is "
        "literally audible, a gold plate reading HOLINESS TO THE LORD "
        "worn on the forehead, and an admission built into the "
        "garments themselves that even Israel's worship needs a "
        "priest to bear its guilt"),
    "exodus29": (CLS,
        "a seven-day ordination built from washing, clothing, "
        "anointing and three distinct sacrifices, blood applied to an "
        "ear, a thumb and a big toe so that hearing, doing and "
        "walking are each separately consecrated, a sin offering "
        "whose flesh is burned outside the camp while its fat alone "
        "goes to the altar, a daily offering of two lambs established "
        "as perpetual rather than one-time, and a closing promise "
        "that ties the entire ceremony to nothing less than God "
        "dwelling among his people"),
    "exodus30": (CLS,
        "an incense altar kept so small it is easy to miss beside the "
        "ark it stands nearest to, a ransom of exactly half a shekel "
        "charged alike to rich and poor at every census, a bronze "
        "laver positioned between altar and tent so that cleansing "
        "always follows atonement and precedes service, an anointing "
        "oil compounded to a fixed recipe and forbidden from any "
        "common use, and an incense recipe carrying the same "
        "prohibition, its formula reserved for God alone under "
        "penalty of being cut off"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
