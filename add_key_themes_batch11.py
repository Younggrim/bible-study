#!/usr/bin/env python3
"""Batch 11: 1 Corinthians 2-12, 14-16 (chapters 1, 13 already had the
pair). See add_key_themes_batch1.py.

    python3 add_key_themes_batch11.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Epistle — Pauline"

DATA = {
    "1corinthians2": (CLS,
        "Paul's own arrival described in weakness and fear so that "
        "faith would rest in power rather than eloquence, a hidden "
        "wisdom eye has not seen and ear has not heard, the Spirit named "
        "as the only means by which the things of God can be received, "
        "a natural man unable to know what is spiritually discerned, and "
        "a closing claim to the mind of Christ resting on the Spirit "
        "rather than on ability"),
    "1corinthians3": (CLS,
        "Envying and strife diagnosed as evidence of spiritual infancy "
        "rather than sophistication, Paul planting and Apollos watering "
        "while only God gives the increase, Christ named the only "
        "foundation before any building material is judged, fire "
        "testing every man's work with loss possible even where "
        "salvation is not, and party slogans turned inside out so that "
        "the teachers belong to the church rather than the church to "
        "the teachers"),
    "1corinthians4": (CLS,
        "Apostles described as stewards managing what belongs to "
        "someone else, Paul declining to judge even himself and leaving "
        "that to the Lord, a devastating irony set between the "
        "Corinthians reigning as kings and the apostles going hungry "
        "and despised, fatherhood claimed on grounds no other teacher "
        "in Corinth can claim, and a question left open whether Paul "
        "should come with a rod or in a spirit of meekness"),
    "1corinthians5": (CLS,
        "A sin not even named among the Gentiles met with pride instead "
        "of mourning, deliverance to Satan aimed at saving the spirit "
        "rather than merely punishing the flesh, a little leaven argued "
        "to leaven the whole lump, an earlier instruction corrected and "
        "narrowed to a brother rather than the world outside, and "
        "jurisdiction fixed firmly on those within the church rather "
        "than those without"),
    "1corinthians6": (CLS,
        "Lawsuits between believers taken to pagan courts when saints "
        "will one day judge the world and angels, being wronged "
        "preferred to wronging a brother, a vice list ending in a "
        "reminder that this is what some of them used to be, all "
        "things lawful answered by not all things being profitable, and "
        "the body named a temple of the Holy Ghost bought with a price "
        "rather than a possession to use as one likes"),
    "1corinthians7": (CLS,
        "Marriage and singleness both named gifts rather than one "
        "ranked above the other, divorce addressed separately for two "
        "believers and for a believer married to an unbeliever, "
        "remaining in the calling one was called in argued twice from "
        "circumcision and once from slavery, advice about virgins "
        "offered as judgment rather than commandment because of the "
        "present distress, and a closing decision handed back to the "
        "reader between good and better rather than right and wrong"),
    "1corinthians8": (CLS,
        "Knowledge that puffs up set against love that builds up, one "
        "God and one Lord confessed before any question about meat is "
        "settled, an idol declared nothing at all in the world while a "
        "weaker conscience is still taken seriously, a strong "
        "believer's freedom capable of emboldening a weak one toward "
        "their own destruction, and a vow to eat no flesh at all rather "
        "than risk offending a brother"),
    "1corinthians9": (CLS,
        "Real rights established from common sense, the Law and Jesus' "
        "own command before any of them are surrendered, none of those "
        "rights actually used so no accusation of financial motive "
        "could stick, becoming all things to all men kept inside a "
        "chapter about surrendering rights rather than convictions, and "
        "an athlete's discipline applied to Paul's own body lest he "
        "himself be disqualified after preaching to others"),
    "1corinthians10": (CLS,
        "Israel's wilderness privileges shown insufficient to prevent "
        "its wilderness failures, let him that thinketh he standeth "
        "take heed lest he fall, a way of escape promised through "
        "temptation rather than around it, one loaf making many eaters "
        "one body used to argue what sharing an idol's table also "
        "does, and liberty limited by another man's conscience rather "
        "than by the eater's own"),
    "1corinthians11": (CLS,
        "Imitation of Paul as he imitates Christ governing a passage "
        "about coverings that follows, a cultural sign of married "
        "status read as either respectability or rebellion depending "
        "on whether it is worn, the Lord's Supper turned into a "
        "divisive meal where the wealthy eat while the poor go hungry, "
        "the institution of the Supper recounted to correct how it was "
        "being kept, and self-examination commanded before eating and "
        "drinking rather than left to instinct"),
    "1corinthians12": (CLS,
        "A test for spiritual utterance stated by its content, Jesus is "
        "Lord, rather than its intensity, the same Spirit, Lord and God "
        "behind gifts, ministries and workings that differ, a body with "
        "many members none of which may say it does not belong, less "
        "honourable parts given more abundant honour rather than less, "
        "and a numbered list that stops numbering exactly where the "
        "church's argument about rank needed it to"),
    "1corinthians14": (CLS,
        "Prophecy preferred over tongues in corporate worship because "
        "it edifies the whole church rather than only the speaker, five "
        "words with understanding weighed against ten thousand in an "
        "unknown tongue, tongues limited to two or three speakers and "
        "required to be interpreted, God named not the author of "
        "confusion but of peace, and everything ordered under one "
        "governing rule, let all things be done unto edifying"),
    "1corinthians15": (CLS,
        "The gospel reduced to three facts and two scripture-anchored "
        "qualifiers, a chain of consequences traced out fully if Christ "
        "is not risen, Christ named firstfruits so that His "
        "resurrection is the beginning of the harvest rather than a "
        "separate event, a resurrection body compared to a seed sown in "
        "weakness and raised in power, and death's sting and victory "
        "both declared already answered before the chapter's last "
        "word"),
    "1corinthians16": (CLS,
        "A collection organized as systematic and weekly giving rather "
        "than a single impulsive gift, a great door opened at Ephesus "
        "in the same breath as many adversaries, Apollos declining an "
        "invitation from the very church that had formed a party around "
        "him, five imperatives gathered under one that governs them, "
        "let all your things be done with charity, and a closing "
        "signature in Paul's own hand marking everything before it as "
        "dictated"),
}


def main():
    check = "--check" in sys.argv
    bad = 0
    for book, (classification, themes) in DATA.items():
        status = process(book, classification, themes, check)
        print(f"{book}: {status}")
        if status not in ("ok", "already-has"):
            bad += 1
    print(f"\n{'checked' if check else 'wrote'} {len(DATA)} pages, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
