#!/usr/bin/env python3
"""Batch 30: Luke 2-4, 7-9, 11-24 (chapters 1, 5, 6, 10 already have Key Themes).

    python3 add_key_themes_batch30.py [--check]
"""
import sys

from add_key_themes_batch1 import process

NARR = "Gospel — Narrative"
DISC = "Gospel — Narrative and Discourse"

DATA = {
    "luke2": (NARR,
        "a birth dated by an administrative decree rather than by any "
        "angel or star, a couple traveling only because a government "
        "required it and a firstborn laid in a feeding trough for "
        "lack of room, an announcement made not to kings or scholars "
        "but to shepherds working a night shift, a sign they can "
        "actually go check for themselves, ye shall find the babe "
        "wrapped in swaddling clothes, lying in a manger, an offering "
        "of two turtledoves at the purification, the very provision "
        "Leviticus allows for those who cannot afford a lamb, "
        "Simeon's prophecy naming both a light for the Gentiles and a "
        "sword through Mary's own soul, and the only glimpse of Jesus "
        "between infancy and his baptism, a twelve-year-old telling "
        "his parents he must be about his Father's business"),
    "luke3": (NARR,
        "a historian's precision naming seven office-holders from "
        "Caesar down to the high priests before saying the word of "
        "God came to none of them but to John, Isaiah quoted at "
        "greater length than any other Gospel keeps, all flesh shall "
        "see the salvation of God, practical instructions unique to "
        "Luke given to specific groups, crowds, tax collectors, "
        "soldiers, each told exactly what repentance looks like in "
        "their own work, John's story finished, including his "
        "imprisonment, before Luke ever records the baptism itself, "
        "and a genealogy traced backward all the way to Adam and to "
        "God rather than forward from Abraham"),
    "luke4": (DISC,
        "temptation following the Spirit's own leading rather than "
        "any accident, three temptations ending with the temple "
        "rather than the kingdoms, Jerusalem left as the last word "
        "because Jerusalem is where this whole Gospel is heading, a "
        "homecoming sermon at Nazareth that reads Isaiah aloud and "
        "stops mid-sentence, deliberately omitting the day of "
        "vengeance, admiration turning to attempted murder the moment "
        "Jesus mentions God's grace reaching Gentiles, and healings "
        "moving from private, a fever rebuked rather than treated, to "
        "public, a whole town's sick brought at sunset and healed one "
        "by one before he leaves the next morning because he must "
        "preach the kingdom to other cities too"),
    "luke7": (NARR,
        "a centurion who never appears in person, reasoning from "
        "military chain of command rather than personal merit, say in "
        "a word, and my servant shall be healed, drawing the "
        "strongest compliment Jesus pays anyone in the Gospels, a "
        "widow's only son raised at Nain without anyone even asking, "
        "compassion recorded before the miracle rather than after it, "
        "weep not, John sending a question from prison that concedes "
        "real doubt, art thou he that should come, or look we for "
        "another, answered with a list of fulfilled signs rather than "
        "reassurance, and a sinful woman weeping at Jesus' feet in a "
        "Pharisee's house, provoking a lesson that those forgiven "
        "much love much"),
    "luke8": (DISC,
        "women named outright as financial supporters of the "
        "ministry, Mary Magdalene, Joanna and Susanna, a sower "
        "parable interpreted soil by soil in terms of what happens to "
        "the word rather than to the ground, a family unable to reach "
        "Jesus through the crowd answered with a redefinition of "
        "family itself, my mother and my brethren are these which "
        "hear the word of God, and do it, a storm calmed by two words "
        "followed by a question harder than the storm itself, where "
        "is your faith, a demon-possessed man named Legion healed and "
        "found sitting clothed and in his right mind while the "
        "townspeople ask Jesus to leave rather than stay, and two "
        "healings interleaved, a woman healed by a touch she cannot "
        "hide and a girl raised after a delay that seemed, for a "
        "moment, to have cost her life"),
    "luke9": (DISC,
        "the twelve sent out with a deliberately empty packing list, "
        "no staff, no bag, no bread, no money, Herod's own question "
        "left hanging unanswered, who is this of whom I hear such "
        "things, five thousand fed with twelve baskets left over, one "
        "for each disciple who said it could not be done, a question "
        "asked while Jesus is praying alone, whom say ye that I am, "
        "answered by Peter and immediately followed by the first "
        "prediction of suffering, an added word found only in Luke, "
        "take up his cross daily, a transfiguration in which only "
        "Luke reports what Moses and Elijah were actually discussing, "
        "his decease which he should accomplish at Jerusalem, and "
        "three consecutive attempts by the disciples to make the "
        "movement smaller, arguing over who is greatest, forbidding "
        "an outside exorcist and wanting to call down fire on a "
        "village"),
    "luke11": (DISC,
        "a disciple's request prompted simply by watching Jesus pray, "
        "Lord, teach us to pray, a shorter version of the same model "
        "prayer Matthew records, a persistent friend parable arguing "
        "not that God is reluctant but that shameless boldness in "
        "prayer is rewarded, three imperatives and three promises "
        "ending, in Luke's version, not on good things but "
        "specifically on the Holy Spirit, an accusation of casting "
        "out demons by Satan's own power demolished by pointing out a "
        "divided kingdom cannot stand, two Gentile examples, Nineveh "
        "and the queen of the south, offered as proof that less "
        "evidence produced more response, and a dinner invitation "
        "that turns into six woes, three on Pharisees and three on "
        "lawyers, the harshest passage in the whole Gospel"),
    "luke12": (DISC,
        "a crowd so thick people trample each other while Jesus "
        "addresses his disciples over their heads about the leaven of "
        "hypocrisy, fear repeated deliberately three times, "
        "persecution, insignificance and provision, each answered by "
        "a different aspect of God's own character, an inheritance "
        "dispute refused outright, who made me a judge or a divider "
        "over you, and turned instead into a parable about a rich "
        "fool who builds bigger barns the very night his soul is "
        "required of him, ravens and lilies offered as arguments from "
        "lesser to greater against worry, and a stunning denial near "
        "the chapter's end, suppose ye that I am come to give peace "
        "on earth, I tell you, nay, but rather division"),
    "luke13": (DISC,
        "two recent tragedies, Galileans killed by Pilate and "
        "eighteen crushed by a falling tower, used not to explain "
        "suffering but to press the urgency of repentance, a barren "
        "fig tree granted one more year of grace by an interceding "
        "vinedresser before judgment falls, a woman bent double for "
        "eighteen years healed unasked, called to him rather than "
        "begging, a synagogue ruler's objection answered by the "
        "congregation's own Sabbath practice of watering their "
        "animals, two small parables of a mustard seed and hidden "
        "leaven kept moving steadily toward Jerusalem, and a lament "
        "addressed to that very city by name, O Jerusalem, Jerusalem, "
        "which killest the prophets, how often would I have gathered "
        "thy children together, and ye would not"),
    "luke14": (DISC,
        "a man with dropsy healed at a Sabbath dinner after Jesus "
        "asks the lawfulness question himself before anyone else can "
        "raise it, seating advice built entirely around status, sit "
        "not down in the highest room, paired with an instruction to "
        "the host to invite guests who can never repay the favor, the "
        "poor, the maimed, the lame, the blind, a great banquet "
        "parable in which excuses about land, oxen and a new wife "
        "lose out to servants sent compelling strangers in from the "
        "highways and hedges, and three separate uses of the phrase "
        "cannot be my disciple aimed at a crowd Jesus never tries to "
        "make comfortable, illustrated by a builder and a king who "
        "both count the cost before they commit to anything"),
    "luke15": (DISC,
        "three parables told in direct response to a single "
        "complaint, this man receiveth sinners, and eateth with them, "
        "a shepherd who leaves ninety-nine to search for one lost "
        "sheep and a woman who sweeps her whole house for one lost "
        "coin, both stories ending in the same near-identical "
        "interpretation, joy shall be in heaven over one sinner that "
        "repenteth, a younger son's rebellion and return met by a "
        "father who runs rather than waits, and an elder son's "
        "resentment left as the parable's real unresolved question, "
        "the story closing not on the celebration but on an "
        "invitation extended to the very brother still standing "
        "outside"),
    "luke16": (DISC,
        "a dishonest manager commended not for his dishonesty but for "
        "his shrewdness in securing his own future before it is too "
        "late, Pharisees derided for their love of money answered "
        "with a single word explaining their contempt, covetous, a "
        "warning that what is highly esteemed among men is "
        "abomination in the sight of God, a beggar given a name, "
        "Lazarus, the only named character in any of Jesus' parables, "
        "and a rich man in torment asking that Lazarus warn his "
        "brothers, refused on the ground that if they will not hear "
        "Moses and the prophets, neither will they be persuaded "
        "though one rose from the dead"),
    "luke17": (DISC,
        "a millstone warning against causing a little one to stumble "
        "followed immediately by forgiveness given no limit at all, "
        "seven times in a day, the only recorded request in the "
        "Gospels for more faith answered not with a bigger portion "
        "but with a mustard seed's worth properly used, a servant's "
        "obedience named baseline rather than bonus, we are "
        "unprofitable servants, ten lepers healed on the way to the "
        "priests and only one returning to give thanks, a Samaritan, "
        "prompting the question where are the nine, and a kingdom "
        "said to come not with observation but already among them, "
        "set against a Son of man's return as visible and sudden as "
        "lightning across the sky"),
    "luke18": (DISC,
        "an unjust judge who fears neither God nor man finally "
        "granting justice purely because a widow will not stop "
        "asking, a Pharisee praying about his own accomplishments set "
        "against a tax collector who cannot even lift his eyes, God "
        "be merciful to me a sinner, children brought and rebuked by "
        "the disciples before being named the very standard for "
        "entering the kingdom, a rich ruler who has kept every "
        "commandment from his youth walking away sorrowful over the "
        "one thing he will not sell, a third passion prediction so "
        "plain that Luke still records the disciples understanding "
        "none of it, and a blind beggar near Jericho crying out so "
        "much the more despite being told to be quiet, finally asked "
        "the question nobody usually asks a beggar, what wilt thou "
        "that I shall do unto thee"),
    "luke19": (NARR,
        "a wealthy, hated tax collector climbing a tree in a "
        "humiliating act just to see Jesus, an immediate "
        "self-invitation followed by radical, voluntary restitution, "
        "half my goods to the poor and fourfold to anyone I have "
        "cheated, a nobleman parable explained in advance as an "
        "answer to a mistaken expectation that the kingdom would "
        "appear immediately, citizens who send a message after their "
        "king, we will not have this man to reign over us, a "
        "triumphal entry whose crowd shout answers the angels' own "
        "song at the nativity, peace in heaven, and glory in the "
        "highest, weeping over a city that cannot see what he already "
        "sees coming, and a temple cleared of merchants with no whip "
        "and no overturned tables recorded, only a quotation and a "
        "standoff that a listening crowd is what keeps alive for the "
        "rest of the week"),
    "luke20": (NARR,
        "a counter-question about John's baptism that traps the very "
        "men demanding to know Jesus' own authority, a parable of "
        "wicked tenants who beat the servants and finally kill the "
        "son, aimed unmistakably at the leaders listening to it, a "
        "tax question with no safe answer resolved by transcending "
        "the trap entirely, render unto Caesar, an argument from the "
        "burning bush answering the Sadducees on resurrection with a "
        "clause Luke alone adds, for all live unto him, scribes "
        "conceding the point out loud and then daring to ask no more "
        "questions at all, and a warning against men who devour "
        "widows' houses placed immediately before the very widow who "
        "gives her last two mites in the next chapter"),
    "luke21": (DISC,
        "a poor widow's two small coins named worth more than every "
        "large gift given from abundance, admiration for the temple's "
        "stonework answered flatly, not one stone shall be left upon "
        "another, wars, earthquakes and famines named explicitly as "
        "things that must happen without yet being the end, a "
        "promised mouth and wisdom for anyone delivered up to "
        "synagogues and prisons that their adversaries cannot resist "
        "or gainsay, a specific and literal warning about armies "
        "compassing Jerusalem that believers would remember and flee "
        "by decades later, and an instruction that inverts ordinary "
        "fear into anticipation, when these things begin to come to "
        "pass, then look up, and lift up your heads, for your "
        "redemption draweth nigh"),
    "luke22": (NARR,
        "Satan entering Judas at the very moment the plot against "
        "Jesus finds an insider, an insider whose betrayal is "
        "arranged with money mentioned but not yet counted, two cups "
        "over a Passover meal Jesus says he has desired with desire "
        "to eat, a betrayal announced after the meal rather than "
        "before so the traitor is served alongside everyone else, "
        "disciples arguing over greatness within hours of the cross "
        "answered by Jesus defining himself as one who serves, a "
        "specific prayer for Peter that his faith not fail rather "
        "than that he not fall at all, sweat like great drops of "
        "blood and an angel sent to strengthen him in Gethsemane, an "
        "ear severed and healed by Jesus even during his own arrest, "
        "and a single unrecorded-elsewhere detail, the Lord turned, "
        "and looked upon Peter, the moment the cock crows a third "
        "time"),
    "luke23": (NARR,
        "three political charges brought before Pilate, one of them "
        "demonstrably false, answered with a verdict delivered in the "
        "trial's first five verses, I find no fault in this man, a "
        "trial before Herod found only in Luke in which Jesus simply "
        "refuses to perform or even speak, three separate "
        "declarations of innocence from Pilate followed by handing "
        "Jesus over anyway, Barabbas named specifically as guilty of "
        "the very crimes Jesus was charged with, women weeping on the "
        "road answered not with comfort but with a warning about the "
        "city itself, the first of the seven sayings from the cross "
        "recorded only in Luke, Father, forgive them, for they know "
        "not what they do, a dying criminal's simple request answered "
        "with today shalt thou be with me in paradise, and last words "
        "drawn from a child's own bedtime prayer, Father, into thy "
        "hands I commend my spirit"),
    "luke24": (NARR,
        "women arriving with spices to find the stone already rolled "
        "away, two men in shining garments answering with a question "
        "rather than an announcement, why seek ye the living among "
        "the dead, the eleven dismissing the report as idle tales "
        "while Peter alone goes to check for himself, two disciples "
        "on the road to Emmaus walking beside the risen Jesus for "
        "miles without recognizing him until bread is broken, a "
        "resurrection insisted on as thoroughly physical, hands and "
        "feet shown, broiled fish eaten, rather than any vision or "
        "ghost, an opened understanding named as the real turning "
        "point rather than any new piece of evidence, then opened he "
        "their understanding, that they might understand the "
        "scriptures, and a Gospel that ends exactly where it began, "
        "in the temple, with a blessing rather than with fear"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
