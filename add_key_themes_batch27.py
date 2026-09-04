#!/usr/bin/env python3
"""Batch 27: Matthew 1-28, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch27.py [--check]
"""
import sys

from add_key_themes_batch1 import process

NARR = "Gospel — Narrative"
DISC = "Gospel — Narrative and Discourse"

DATA = {
    "matthew1": (NARR,
        "a genealogy opening the entire Gospel as a legal document "
        "rather than a story, three groups of fourteen imposed "
        "deliberately on the record rather than found in it, four "
        "women named by choice, Tamar, Rahab, Ruth and the wife of "
        "Uriah, before Mary breaks the pattern of the whole list "
        "entirely, a decent man's decision to divorce quietly "
        "reversed by an angel who names the child before he is born, "
        "for he shall save his people from their sins, and the first "
        "of Matthew's fulfilment formulas, quoting Isaiah on a virgin "
        "and a name Matthew stops to translate, God with us"),
    "matthew2": (NARR,
        "astrologers from outside Israel reading a star correctly and "
        "then asking the wrong man for directions, Herod's own "
        "scholars naming the exact town of Bethlehem from Micah "
        "without a single one of them making the five-mile trip, a "
        "request for a report that Matthew frames as a lie before it "
        "is even carried out, a flight to Egypt attached to Hosea's "
        "out of Egypt have I called my son so the child retraces the "
        "nation's own route, and a massacre answered only with "
        "Jeremiah's Rachel weeping for her children, Matthew offering "
        "no consolation alongside it"),
    "matthew3": (NARR,
        "a two-word message translated with its reason attached, "
        "repent, for the kingdom of heaven is at hand, a wilderness "
        "prophet dressed deliberately like Elijah drawing crowds out "
        "of Jerusalem and all Judaea, Pharisees and Sadducees met "
        "with a different sermon than the crowd, O generation of "
        "vipers, a demand for fruit that closes off the excuse of "
        "ancestry in advance, we have Abraham to our father, and "
        "John's own refusal at the Jordan answered not with an order "
        "but with a reason, thus it becometh us to fulfil all "
        "righteousness, before heaven opens, a dove descends and a "
        "voice speaks"),
    "matthew4": (NARR,
        "temptation following baptism not by accident but by the "
        "Spirit's own leading, forty days of fasting deliberately "
        "echoing Israel's forty years in the wilderness, three "
        "temptations answered every time from the very book of "
        "Deuteronomy that once described Israel failing the same "
        "tests, two pairs of brothers called mid-workday with four "
        "words and no recorded discussion, straightway left their "
        "nets, and a costly detail left almost unremarked, Zebedee "
        "left sitting alone in the boat"),
    "matthew5": (DISC,
        "nine blessings delivered from a mountain in a teacher's "
        "posture, each pairing a condition nobody would choose with a "
        "promise attached to it, salt and light offered as two images "
        "for the same uselessness if withheld, a claim stronger than "
        "the objection it answers, I am not come to destroy, but to "
        "fulfil, a standard raised rather than relaxed, except your "
        "righteousness shall exceed the righteousness of the scribes "
        "and Pharisees, and six antitheses that trace commandments "
        "back to the heart, murder to anger, adultery to a look, "
        "ending on love your enemies and an imitation argument rather "
        "than a results-based one, for he maketh his sun to rise on "
        "the evil and on the good"),
    "matthew6": (DISC,
        "three religious duties, alms, prayer and fasting, each given "
        "the identical choice between a reward already received "
        "before men and a reward from the Father who seeth in secret, "
        "a model prayer covering worship, submission, dependence, "
        "forgiveness and protection in a single short pattern, the "
        "one petition Jesus chooses to expand being the one about "
        "forgiveness, running both directions, treasure argued first "
        "from durability and then from the heart, for where your "
        "treasure is, there will your heart be also, and anxiety "
        "about food and clothing answered by pointing to birds fed "
        "and flowers clothed without a single day of work"),
    "matthew7": (DISC,
        "judging forbidden on the ground of reciprocity rather than "
        "relativism, with what measure ye mete, it shall be measured "
        "to you again, a mote and a beam turned into a joke with a "
        "serious end, a rule stated positively for once rather than "
        "negatively, all things whatsoever ye would that men should "
        "do to you, do ye even so to them, a test for false prophets "
        "based on produce rather than doctrine, ye shall know them by "
        "their fruits, and a closing parable of two builders facing "
        "the identical storm, the difference between them lying "
        "entirely in the foundation rather than the effort"),
    "matthew8": (NARR,
        "a leper touched despite every social and religious barrier "
        "that made him untouchable, a Roman centurion whose "
        "understanding of authority produces the only faith in the "
        "Gospels that makes Jesus marvel, a mother-in-law healed with "
        "a touch and rising immediately to serve, two would-be "
        "followers answered with warnings about cost rather than "
        "encouragement, the Son of man hath not where to lay his "
        "head, a storm slept through and then rebuked with the same "
        "authority just claimed in the Sermon on the Mount, and a "
        "town that, faced with two restored men and a drowned herd of "
        "swine, asks Jesus to leave rather than to stay"),
    "matthew9": (NARR,
        "sins forgiven before legs are healed, addressing the deeper "
        "need first and proving the authority to do either, Matthew "
        "himself called from a tax booth with two words and answering "
        "with an immediate dinner party, two objections answered with "
        "two quotations, mercy and not sacrifice for the Pharisees, a "
        "bridegroom taken away for John's disciples, new wine refused "
        "a home in old wineskins as the chapter's own image for what "
        "is happening, a woman healed by touching a hem while a "
        "ruler's daughter waits, and a diagnosis offered for the "
        "whole crowd's condition, sheep having no shepherd, that "
        "turns immediately into a call to pray for laborers"),
    "matthew10": (DISC,
        "twelve named in pairs, one labeled by his old job and one by "
        "his eventual betrayal, a mission deliberately narrowed at "
        "this stage to the lost sheep of the house of Israel that "
        "Matthew will later reverse entirely, dependence commanded "
        "down to the smallest detail, no gold, no scrip, no second "
        "coat, a warning delivered as sheep among wolves paired with "
        "an instruction that sounds almost self-contradictory, wise "
        "as serpents, and harmless as doves, fear repeated three "
        "times with three different reasons, and a closing turn to "
        "something unexpectedly gentle, a cup of cold water given to "
        "a little one, coming right after talk of a sword dividing "
        "households"),
    "matthew11": (DISC,
        "a formula that closes every one of Matthew's five discourses "
        "used here for the first time, a bold prophet now imprisoned "
        "and doubting whether he had gotten it right, three questions "
        "about what the crowds went out to see building to an "
        "unqualified verdict on John immediately relativized in the "
        "very next clause, unrepentant cities warned that greater "
        "privilege brings greater accountability, and an invitation "
        "that turns from judgment to rest in a single verse, come "
        "unto me, all ye that labour and are heavy laden, offering "
        "not the removal of a yoke but a different one entirely"),
    "matthew12": (NARR,
        "two sabbath disputes both answered from precedent rather "
        "than principle, David eating the showbread and priests "
        "working in the temple, before two claims are made that are "
        "larger than either argument requires, one greater than the "
        "temple and Lord even of the sabbath, the longest Old "
        "Testament quotation in the whole Gospel placed deliberately "
        "between a murder plot and an accusation of demonic power, a "
        "warning about the unforgivable sin arising from a permanent, "
        "willful hardening rather than a momentary lapse, and family "
        "redefined in the chapter's final verse, whosoever shall do "
        "the will of my Father which is in heaven, the same is my "
        "brother, and sister, and mother"),
    "matthew13": (DISC,
        "a sower parable told from a boat without a word of "
        "interpretation, four soils and four outcomes closing on who "
        "hath ears to hear, let him hear, parables explained as an "
        "act of both grace and judgment, revealing to the open and "
        "confirming the blindness of those already closed, a private "
        "interpretation naming each soil as a way of hearing rather "
        "than a class of person, wheat and tares left deliberately "
        "growing together until the harvest, small-beginning parables "
        "of mustard seed and leaven set beside treasure and pearl "
        "parables about response rather than size, and a closing "
        "scene at Nazareth where the only objection raised against "
        "Jesus is his own ordinariness"),
    "matthew14": (NARR,
        "John's death told as a flashback triggered by Herod's guilty "
        "conscience, a rash oath at a birthday party sealing a "
        "prophet's fate that Herod himself lacked the will to order "
        "sooner, five thousand men fed from five loaves and two "
        "fishes after Jesus is moved with compassion rather than "
        "sending the hungry crowd away, a storm at the fourth watch "
        "met by three short clauses, be of good cheer, it is I, be "
        "not afraid, Peter's bold request to walk on water recorded "
        "only in Matthew, and a first united confession from the "
        "disciples, of a truth thou art the Son of God, closing the "
        "chapter at Gennesaret in a scene of pressing crowds rather "
        "than teaching"),
    "matthew15": (NARR,
        "a hand-washing dispute turned into a countercharge that the "
        "Pharisees' own tradition voids God's actual commandment, "
        "corban exposed as a loophole that lets religious devotion "
        "excuse abandoning aging parents, a principle announced to "
        "the crowd, not that which goeth into the mouth defileth a "
        "man, but that which cometh out, a Canaanite woman answered "
        "first with silence and then with a proverb about children "
        "and dogs that she turns back on him, one of only two times "
        "in the Gospel that faith is called great, and both times the "
        "person is a Gentile, and a second feeding, four thousand men "
        "beside women and children, recorded without any apology for "
        "repeating the first"),
    "matthew16": (NARR,
        "Pharisees and Sadducees together demanding a sign answered "
        "by mocking their own competence at reading weather, a "
        "warning about leaven that the disciples take as a comment on "
        "forgotten bread until Matthew supplies what they missed, a "
        "question asked in two stages at a city built around pagan "
        "worship, first what men say and then whom say ye, an answer "
        "that goes further than any rumor, thou art the Christ, the "
        "Son of the living God, credited immediately to revelation "
        "rather than insight, and a rebuke within minutes of that "
        "same confession, get thee behind me, Satan, the harshest "
        "thing said to any disciple in the whole Gospel"),
    "matthew17": (NARR,
        "three disciples taken up a mountain and shown a glory "
        "breaking through ordinary human form, his face did shine as "
        "the sun, Moses and Elijah appearing beside him before a "
        "voice repeats the words from the baptism with one addition, "
        "hear ye him, a boy the disciples cannot heal met first with "
        "exasperation and then with an explanation of size, faith as "
        "a grain of mustard seed, a second passion prediction "
        "answered in four words, they were exceeding sorry, and an "
        "episode found only in this Gospel, a temple tax paid though "
        "Jesus argues the sons of the king are exempt from it, the "
        "coin pulled from a fish's mouth"),
    "matthew18": (DISC,
        "a child called into the middle of the room to answer a "
        "question about greatness, the most violent language in the "
        "whole Gospel aimed at anyone who causes one of these little "
        "ones to offend, a shepherd's arithmetic applied to a single "
        "lost sheep out of ninety-nine, an explicit three-step "
        "process for confronting sin within the community that aims "
        "at restoration rather than punishment, Peter's generous "
        "offer of seven times answered with seventy times seven, not "
        "a larger number but the abolition of counting, and a parable "
        "pairing an unpayable debt of ten thousand talents against a "
        "manageable debt of a hundred pence to explain exactly why"),
    "matthew19": (NARR,
        "a test question about divorce answered by going behind Moses "
        "to Genesis itself, what therefore God hath joined together, "
        "let not man put asunder, Moses' provision named a concession "
        "to hardness of heart rather than a permission, disciples "
        "rebuking people who bring children to Jesus for the second "
        "time in three chapters and being corrected again, a rich "
        "young man who alone in the Gospels asks what lack I yet and "
        "alone walks away sorrowful for his great possessions, and an "
        "answer that removes the whole matter from human capacity "
        "entirely, with God all things are possible"),
    "matthew20": (NARR,
        "a parable found only in Matthew existing specifically to "
        "unsettle the promise Peter has just been given, laborers "
        "hired at dawn and at the eleventh hour all paid the same "
        "penny, a complaint answered not by denying unfairness but by "
        "asking is thine eye evil, because I am good, the most "
        "detailed passion prediction yet followed immediately by a "
        "mother's request for thrones for her sons, a correction "
        "aimed at all twelve disciples at once, it shall not be so "
        "among you, the Son of man came not to be ministered unto, "
        "but to minister, and two blind men near Jericho who ask only "
        "that their eyes may be opened, set deliberately against the "
        "mother's request for status"),
    "matthew21": (NARR,
        "detailed arrangements given in advance for a donkey and "
        "colt, fulfilling Zechariah's prophecy of a king who comes in "
        "peace rather than in war, a crowd shouting Hosanna to the "
        "son of David, a royal acclamation the city itself cannot "
        "quite explain, calling him only Jesus the prophet of "
        "Nazareth of Galilee, a temple cleared with two quotations "
        "paired together, a house of prayer turned into a den of "
        "thieves, a fig tree cursed and withered as a sign against "
        "fruitless religion, and two parables of judgment, two sons "
        "and wicked tenants, that force the religious leaders to "
        "pronounce sentence on themselves before they even realize "
        "what they have done"),
    "matthew22": (NARR,
        "a wedding feast parable ending in a detail unique to "
        "Matthew, a guest without a wedding garment cast out even "
        "after the doors were thrown open to bad and good alike, an "
        "unnatural alliance between Pharisees and Herodians setting a "
        "tax trap with no safe answer, a coin's image drawn out to "
        "produce the answer itself, render therefore unto Caesar the "
        "things which are Caesar's, and unto God the things that are "
        "God's, the Sadducees corrected on two counts at once, "
        "scripture and the power of God, two commandments given in "
        "place of one, love God and love thy neighbour as thyself, "
        "and a closing question about David's son and David's Lord "
        "that ends all further questioning for the rest of the week"),
    "matthew23": (DISC,
        "instruction to obey the scribes and Pharisees paired "
        "immediately with a warning not to imitate their works, the "
        "charge being inconsistency rather than error, three titles "
        "forbidden to the disciples, Rabbi, father and master, seven "
        "specific woes rather than general abuse, straining a gnat "
        "and swallowing a camel while whited sepulchres are named "
        "beautiful outward and full of dead men's bones, and a "
        "closing lament that shifts entirely from prosecution to "
        "grief, how often would I have gathered thy children "
        "together, even as a hen gathereth her chickens under her "
        "wings, and ye would not"),
    "matthew24": (DISC,
        "a prediction that not one stone shall be left upon another "
        "answered by three joined questions about timing and signs, "
        "wars, famines and earthquakes named explicitly as only the "
        "beginning of sorrows rather than the end, a specific sign, "
        "the abomination of desolation, triggering practical "
        "instructions for a single day, flee to the mountains, a fig "
        "tree's season readable while the day and hour remain unknown "
        "to anyone but the Father, Noah's flood used as a pattern "
        "stressing ordinary normality rather than open wickedness, "
        "and a servant's fate turning entirely on how he treats a "
        "delay rather than on whether he believes a return is "
        "coming"),
    "matthew25": (DISC,
        "five wise and five foolish virgins differing only in oil "
        "kept in reserve, all ten having slept, the failure being "
        "unpreparedness for delay rather than wakefulness itself, "
        "three servants given unequal sums and judged identically for "
        "what they do with them rather than how much they receive, a "
        "buried talent justified by an accusation about the master "
        "that is turned back against the servant who made it, and a "
        "final judgment in which both sheep and goats ask the "
        "identical surprised question, when did we see thee, because "
        "neither group did anything for credit, inasmuch as ye have "
        "done it unto one of the least of these my brethren, ye have "
        "done it unto me"),
    "matthew26": (NARR,
        "the longest chapter in the whole Gospel opening with a plot "
        "dated carefully to avoid an uproar during the feast, an "
        "anointing at Bethany defended as preparation for burial "
        "against an objection costed in exact terms, thirty pieces of "
        "silver recorded only by Matthew as the price of betrayal, "
        "the same question asked around the table by every disciple "
        "in turn, Lord, is it I, including, uniquely in this Gospel, "
        "Judas himself, three prayers in Gethsemane whose wording "
        "shifts from if it be possible to thy will be done, and "
        "Peter's three denials escalating from simple denial to an "
        "oath and finally to a curse before he goes out and weeps "
        "bitterly"),
    "matthew27": (NARR,
        "Judas's fate told only in this Gospel, a confession offered "
        "and refused, see thou to that, before silver bought a field, "
        "Pilate's own wife sending a warning during the hearing that "
        "he chooses to ignore, hands washed in front of the crowd "
        "changing nothing about the verdict already decided, a "
        "crucifixion recorded almost in passing, one clause, while "
        "mockery is quoted in full from three separate groups using "
        "the identical argument, he saved others, himself he cannot "
        "save, and three details reported only by Matthew at the "
        "moment of death, an earthquake, split rocks, and graves "
        "opened with saints appearing in the city"),
    "matthew28": (NARR,
        "an earthquake and a descending angel recorded only in this "
        "Gospel, guards left shaking and as dead men, a message "
        "reduced to four short clauses, fear not, he is not here, he "
        "is risen, come see the place, women leaving with fear and "
        "great joy held together rather than resolved into one, "
        "worship and doubt placed inside the very same sentence with "
        "no explanation offered for either, but some doubted, and a "
        "closing commission built on four parts, authority, command, "
        "method and promise, given to the same group that had just "
        "worshipped and doubted at once"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
