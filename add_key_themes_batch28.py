#!/usr/bin/env python3
"""Batch 28: Acts 2-28 (chapter 1 already has Key Themes).

    python3 add_key_themes_batch28.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "acts2": (CLS,
        "three signs marking the Spirit's arrival at once, sound, "
        "sight and speech, real languages heard by every nation "
        "gathered in Jerusalem rather than any ecstatic babble, a "
        "deliberate reversal of Babel centuries after the fact, "
        "Peter's first sermon preached seven weeks after denying "
        "Jesus three times, a response recorded as physical before it "
        "becomes a decision, pricked in their heart, and a promise "
        "extended past the room itself, unto you, and to your "
        "children, and to all that are afar off, closing on a "
        "description of church life built around four steady "
        "priorities"),
    "acts3": (CLS,
        "a lame man over forty years old carried daily to beg at a "
        "temple gate that Peter and John pass with no money but a "
        "name instead, a healing instant and complete enough that the "
        "man leaps and holds onto his healers as a crowd gathers, "
        "Peter's first move being to refuse the credit, why look ye "
        "so earnestly on us, as though by our own power we had made "
        "this man to walk, a call to repentance offered to the very "
        "people who had Jesus killed weeks earlier, and Moses' "
        "prophecy of a coming prophet tied directly to Abraham's "
        "covenant blessing for all nations"),
    "acts4": (CLS,
        "an arrest triggered specifically by preaching the "
        "resurrection to a council of Sadducees who denied it "
        "existed, a healed man standing in the room as evidence the "
        "council cannot argue away, an exclusive claim stated as "
        "plainly as anywhere in Scripture, neither is there salvation "
        "in any other, unlearned men recognized only by having been "
        "with Jesus, a threatened church praying not for safety but "
        "for boldness, and a community so united that Luke can say "
        "plainly, neither was there any among them that lacked"),
    "acts5": (CLS,
        "the first recorded sin inside the church answered by "
        "immediate and severe judgment, a lie not about withholding "
        "money but about pretending to have given all of it, an angel "
        "opening a prison at night only to send the apostles straight "
        "back to the very place that got them arrested, baffled "
        "officers reporting doors shut with all safety and no man "
        "found within, a sentence the whole chapter turns on, we "
        "ought to obey God rather than men, and a beating followed "
        "immediately by rejoicing that they were counted worthy to "
        "suffer shame for his name"),
    "acts6": (CLS,
        "a complaint from Greek-speaking believers that their widows "
        "were being overlooked in daily food distribution, a solution "
        "that hands the selection of seven men entirely to the "
        "congregation rather than to the apostles themselves, seven "
        "chosen with Greek names drawn directly from the community "
        "that felt neglected, growth recorded as the direct outcome "
        "of settling an internal dispute, and Stephen introduced as "
        "full of faith and power, his opponents unable to resist his "
        "wisdom and forced to resort to false witnesses instead"),
    "acts7": (CLS,
        "the longest chapter in the whole book built as an answer to "
        "a single question, are these things so, Stephen surveying "
        "Israel's history from Abraham through Moses to Solomon to "
        "argue that God has always worked outside the established "
        "structures, a repeated pattern of Israel rejecting its own "
        "chosen deliverers, Joseph, Moses, the prophets and now "
        "Jesus, a claim that the Most High dwelleth not in temples "
        "made with hands, and a martyrdom that mirrors Jesus' own "
        "death point for point, heaven opened, a spirit committed to "
        "God, and a prayer for the killers' forgiveness with a young "
        "man named Saul watching approvingly"),
    "acts8": (CLS,
        "Saul introduced first by consent and then by violence, "
        "entering house after house to commit men and women to "
        "prison, a scattering meant to destroy the church instead "
        "becoming the very mechanism the book uses to spread it, "
        "Philip preaching in Samaria, enemy territory for Jews, and "
        "Simon the sorcerer revealing a wrong heart by trying to buy "
        "the Spirit's power with money, and an Ethiopian official "
        "reading Isaiah's suffering servant in his own chariot, "
        "believing and being baptized the moment Philip explains who "
        "it describes, carrying the gospel to Africa"),
    "acts9": (CLS,
        "a man breathing out threatenings and slaughter struck blind "
        "by a light on the road to Damascus, a question that "
        "identifies persecuting the church with persecuting Christ "
        "himself, Saul, Saul, why persecutest thou me, Ananias sent "
        "to the very man coming to arrest him and greeting him first "
        "with a single word, brother, before he has proven anything, "
        "no probation period before the persecutor begins preaching, "
        "straightway he preached Christ, and Peter's own two miracles "
        "at Lydda and Joppa closing the chapter, an eight-year "
        "illness healed in two sentences and a widow raised with two "
        "words, Tabitha, arise"),
    "acts10": (CLS,
        "a devout Roman centurion who prays and gives alms yet still "
        "needs to hear and believe the gospel to be saved, a sheet of "
        "unclean animals lowered three times with a command Peter "
        "refuses three times, kill, and eat, a vision about people "
        "rather than food, what God hath cleansed, that call not thou "
        "common, timing made explicit as three men knock while Peter "
        "still puzzles over what he saw, and a sermon that opens with "
        "the very conclusion Peter has just been forced to accept, "
        "God is no respecter of persons, the Spirit falling on "
        "Gentiles in the middle of the preaching itself"),
    "acts11": (CLS,
        "Peter defending his ministry to uncircumcised Gentiles "
        "before a critical Jerusalem church by simply recounting what "
        "happened rather than arguing theology, a conclusion nobody "
        "in the room can refute, what was I, that I could withstand "
        "God, believers scattered by persecution reaching Antioch and "
        "beginning to preach to Greeks as well as Jews, disciples "
        "called Christians for the first time in that very city, and "
        "a famine relief collection stated in a single clause, every "
        "man according to his ability, sending money from a Gentile "
        "congregation back to the Jewish believers who first sent the "
        "gospel out"),
    "acts12": (CLS,
        "a king killing one apostle and arresting a second "
        "specifically to gain favor with Jewish leaders, a church "
        "praying without ceasing while chains fall off Peter unnoticed "
        "by the very guards chained to him, a prayer meeting that "
        "refuses to believe its own prayer has been answered when "
        "Peter actually knocks at the door, Herod accepting worship "
        "as a god and immediately struck down for withholding the "
        "glory that belonged to God alone, and a sentence placed "
        "deliberately right after his death, the word of God grew and "
        "multiplied, letting the contrast make the point without "
        "comment"),
    "acts13": (CLS,
        "a diverse leadership team fasting and worshipping when the "
        "Holy Spirit names two men by name, separate me Barnabas and "
        "Saul, a name change marked at the exact moment Saul "
        "confronts a sorcerer on Cyprus, then Saul, who also is "
        "called Paul, a sermon at Pisidian Antioch following the same "
        "shape as Peter's earlier sermons before landing on "
        "justification by faith rather than the law of Moses, envy "
        "named outright as the motive when the whole city turns out "
        "to hear the word the next week, and an expulsion answered "
        "not with despair but with joy, the disciples were filled "
        "with joy, and with the Holy Ghost"),
    "acts14": (CLS,
        "the same pattern repeating at Iconium as at Antioch, a "
        "divided city and a planned assault the missionaries simply "
        "leave rather than confront, a lame man healed at Lystra "
        "prompting a pagan crowd to try to worship Paul and Barnabas "
        "as Zeus and Hermes, a sermon to a purely pagan audience built "
        "entirely on creation rather than on Israel's history, Paul "
        "stoned and left for dead by the very crowd that tried to "
        "worship him and getting up to return to the city the next "
        "day, and a return journey retracing every town they were "
        "driven out of, warning new believers that it is through much "
        "tribulation we must enter the kingdom of God"),
    "acts15": (CLS,
        "a controversy striking at the heart of the gospel itself, "
        "whether Gentile believers must be circumcised to be saved, "
        "three testimonies settling the matter in turn, Peter's "
        "account of Gentiles receiving the Spirit without "
        "circumcision, Paul and Barnabas's miracles, and James's "
        "citation of Amos, a letter carried by named men so Gentile "
        "churches hear the decision from Jerusalem's own "
        "representatives rather than from Paul alone, a burden "
        "deliberately kept light, no greater burden than these "
        "necessary things, and a sharp split between Paul and "
        "Barnabas over John Mark that produces two missionary teams "
        "instead of one"),
    "acts16": (CLS,
        "Timothy circumcised by Paul, of all people, right after the "
        "Jerusalem council settled that circumcision cannot be "
        "required, a tactic rather than a principle chosen to remove "
        "an obstacle among local Jews, the Spirit blocking Asia and "
        "Bithynia twice before a vision finally redirects Paul toward "
        "Macedonia, a businesswoman named Lydia becoming the first "
        "convert in Europe, her heart opened by the Lord rather than "
        "by the argument itself, a slave girl's true but unbearable "
        "shouting leading to a beating whose real cause is economic "
        "loss rather than religious objection, and a midnight "
        "earthquake answered by a jailer's question, what must I do "
        "to be saved, met with the simplest gospel statement in the "
        "whole book"),
    "acts17": (CLS,
        "a habitual method stated outright, three sabbaths of "
        "reasoning from the scriptures, an accusation the opposition "
        "itself supplies rather than Luke, these that have turned the "
        "world upside down are come hither also, Bereans held up as "
        "the model for every believer, receiving the word eagerly "
        "while still searching the scriptures daily to test it, and a "
        "sermon at Athens that never once quotes the Old Testament, "
        "starting instead from the city's own altar to an unknown "
        "God and its own poets before arguing toward a Creator who "
        "will judge the world through a man he raised from the dead"),
    "acts18": (CLS,
        "a synagogue turned away with a gesture and a sentence, your "
        "blood be upon your own heads, from henceforth I will go unto "
        "the Gentiles, the very next convert being the synagogue's "
        "own chief ruler, a vision promising safety and a reason for "
        "it, for I have much people in this city, a year and six "
        "months of settled teaching ended by a Roman official who "
        "declines outright to judge a question of Jewish law, a "
        "personal vow kept at Cenchrea by the same man who fought the "
        "circumcision party in chapter fifteen, and Apollos discipled "
        "privately rather than corrected publicly by a married couple "
        "who expound the way of God more perfectly to him"),
    "acts19": (CLS,
        "twelve disciples found who know only John's baptism and are "
        "given the rest of the gospel rather than being rejected for "
        "their incomplete knowledge, two years of daily teaching in a "
        "lecture hall producing the report that all who dwelt in Asia "
        "heard the word, a demon that recognizes Jesus and Paul by "
        "name but not the seven Jewish exorcists trying to use the "
        "name as a formula, occult books worth fifty thousand pieces "
        "of silver burned publicly as the visible fruit of genuine "
        "repentance, both of Paul's eventual destinations, Jerusalem "
        "and Rome, named together in a single verse of planning, and "
        "a riot whose real motive, a silversmith admits outright, is "
        "money rather than religion"),
    "acts20": (CLS,
        "a change of route explained in a single clause, when the "
        "Jews laid wait for him, seven named traveling companions "
        "carrying the collection two entire letters were written to "
        "organize, a young man named Eutychus falling asleep in a "
        "window during a midnight sermon and falling three stories to "
        "his death before being raised and Paul simply going back "
        "upstairs to keep talking, a farewell delivered thirty miles "
        "from Ephesus because Paul refuses to lose time reaching "
        "Jerusalem by Pentecost, and the only speech in the whole "
        "book addressed specifically to Christian leaders, reviewing "
        "his ministry, declaring his readiness to suffer and warning "
        "of dangers still to come"),
    "acts21": (CLS,
        "cargo details and coastline names surviving only because "
        "Luke writes this whole section in the first person as an "
        "eyewitness, repeated warnings from believers along the way "
        "that bonds and afflictions await Paul in Jerusalem, an "
        "answer that refuses the premise that this is only about "
        "danger, what mean ye to weep and to break mine heart, a "
        "company that stops arguing not because they agree but "
        "because the argument is over, the will of the Lord be done, "
        "James proposing a public demonstration involving four men "
        "under a vow to answer a rumor about Paul, and an arrest "
        "triggered by a false accusation that ends, unexpectedly, "
        "with Paul asking permission to address the very mob that "
        "just tried to kill him"),
    "acts22": (CLS,
        "a defense won a hearing simply by being spoken in Hebrew, a "
        "speech built entirely on common ground, Tarsus, Gamaliel, "
        "zeal for the law, before the crowd erupts the instant the "
        "word Gentiles is spoken, a chief captain who cannot follow "
        "the Hebrew ordering an examination by scourging simply to "
        "learn what the shouting was about, Roman citizenship "
        "revealed only at the last possible moment, not to escape "
        "suffering but to secure a proper process, and an officer "
        "convening the Sanhedrin himself the next morning purely as a "
        "fact-finding exercise, setting up the scene chapter "
        "twenty-three opens with"),
    "acts23": (CLS,
        "a council split in two by a single sentence declaring "
        "himself on trial for the hope and resurrection of the dead, "
        "Pharisees and Sadducees turning on each other instead of on "
        "Paul, a personal appearance by the Lord at Paul's darkest "
        "moment naming the destination that guarantees his survival "
        "until then, so must thou bear witness also at Rome, over "
        "forty men bound by an oath not to eat or drink until Paul is "
        "dead, a plot uncovered by a nephew's courage rather than by "
        "any dramatic intervention, and a military transfer numbering "
        "four hundred seventy soldiers to move a single prisoner, "
        "alongside a letter that quietly improves the officer's own "
        "account of what actually happened"),
    "acts24": (CLS,
        "a professional orator hired to prosecute Paul opening with "
        "three verses of flattery before three charges, only one of "
        "which anyone can actually prove, a defense that insists "
        "Christianity is the fulfillment of Judaism rather than a "
        "departure from it, a governor deferring judgment for a "
        "reason Luke states plainly, having more perfect knowledge of "
        "that way, a private audience in which Paul reasons about "
        "righteousness, temperance and judgment to come until Felix "
        "trembles and postpones, when I have a convenient season, I "
        "will call for thee, and two years explained by two motives, "
        "money hoped for and a political favor, with neither one "
        "legal"),
    "acts25": (CLS,
        "a new governor waiting only three days before the "
        "prosecution raises Paul's case again, a proposed transfer to "
        "Jerusalem that Festus does not realize is actually an "
        "ambush, repeated hearings producing the same result as "
        "before, no accusation of the things that were supposed, an "
        "appeal that removes the case from every court in Judaea in "
        "eight words, hast thou appealed unto Caesar, unto Caesar "
        "shalt thou go, and a king brought in specifically because "
        "Festus needs a coherent charge to send Rome and cannot find "
        "one on his own"),
    "acts26": (CLS,
        "the third and fullest account of the Damascus road in the "
        "whole book, shaped deliberately for a king already expert in "
        "Jewish affairs, a past stated without any softening, many of "
        "the saints did I shut up in prison, a commission summarized "
        "in a single sentence covering the entire gospel, to open "
        "their eyes, and to turn them from darkness to light, an "
        "interruption from Festus, much learning doth make thee mad, "
        "answered with courteous and unmoved composure, a wish "
        "extended to everyone listening except for the chains "
        "themselves, and a private, unanimous verdict of innocence "
        "that comes too late to matter because Paul has already "
        "appealed to Caesar"),
    "acts27": (CLS,
        "the longest sustained eyewitness passage in the whole book, "
        "full of the kind of detail only a passenger would keep, "
        "Paul's warning against sailing overruled because the "
        "centurion trusts the ship's master and owner more than the "
        "prisoner, fourteen days without sun or stars and all hope of "
        "survival gone before Paul stands to declare a promise nobody "
        "but him still believes, two hundred seventy-six souls "
        "counted precisely at the moment the number matters most, "
        "soldiers proposing to kill the prisoners to prevent escape, "
        "and a centurion who overrules them specifically to save "
        "Paul"),
    "acts28": (CLS,
        "an island's kindness met with a viper bite the locals read "
        "first as guilt and then, when Paul survives it, as divinity, "
        "believers walking out thirty and forty miles from Rome to "
        "meet a prisoner who has been shipwrecked and held two years "
        "without ever being formally charged, six words recording the "
        "effect on him, he thanked God, and took courage, a rented "
        "house and a soldier guard becoming the setting for preaching "
        "rather than for confinement, Isaiah's own words about a "
        "hardened people quoted to explain why the gospel now turns "
        "fully toward the Gentiles, and an ending that resolves "
        "nothing, no verdict, no death, only two years of preaching "
        "with all confidence, no man forbidding him"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
