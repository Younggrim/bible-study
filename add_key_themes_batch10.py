#!/usr/bin/env python3
"""Batch 10: Romans 1-11, 13-16 (chapter 12 already had the pair; this is
otherwise the whole book, including chapter 1). See add_key_themes_batch1.py.

    python3 add_key_themes_batch10.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Epistle — Pauline"

DATA = {
    "romans1": (CLS,
        "A one-sentence introduction that names the gospel before Paul "
        "names himself, an obligation felt toward Greeks and Barbarians "
        "before Rome has ever been visited, the just shall live by faith "
        "set down as the thesis before the letter argues for it, idols "
        "exchanged for the glory of an incorruptible God, and God giving "
        "people up three times to exactly what they had already chosen"),
    "romans2": (CLS,
        "A moralist condemned by the same standard he uses to condemn "
        "pagans, judging another named a way of confessing the same "
        "guilt rather than escaping it, the Law's possession shown "
        "worthless the moment it is broken, circumcision relocated to "
        "the heart and the spirit rather than the flesh, and no "
        "partiality promised between Jew and Gentile before the same "
        "judgment"),
    "romans3": (CLS,
        "Objections raised by Paul himself before anyone else can raise "
        "them, a string of Old Testament quotations stopping every mouth "
        "at once, but now marking the hinge of the whole letter after "
        "three chapters of indictment, justification, redemption and "
        "propitiation drawn from three different worlds in one sentence, "
        "and boasting excluded rather than merely redirected"),
    "romans4": (CLS,
        "Abraham believing God and having it counted for righteousness "
        "before circumcision or law existed, David's forgiveness cited "
        "as proof that works were never the ground even for Israel's own "
        "king, a date made to carry the whole argument about "
        "circumcision as sign rather than cause, hope believed against "
        "hope while the difficulty is fully conceded rather than denied, "
        "and a promise secured to all the seed rather than to the "
        "law-keepers only"),
    "romans5": (CLS,
        "Peace with God named first among five results that flow from "
        "justification, access into grace and hope of glory listed "
        "alongside a purpose found even in suffering, Adam and Christ "
        "set up as two representative heads for the whole of humanity, "
        "condemnation through one traced against justification through "
        "one, and grace declared to abound much more wherever sin "
        "abounded"),
    "romans6": (CLS,
        "An objection about grace and continued sin answered before it "
        "can even be finished, union with Christ's death offered as "
        "identity rather than willpower, reckon named as the first "
        "imperative and treated as arithmetic rather than effort, a "
        "slave metaphor apologized for even as it is used, and wages of "
        "death set against a gift of eternal life in a deliberately "
        "asymmetric sentence"),
    "romans7": (CLS,
        "Marriage law used to argue that death dissolves an obligation "
        "the living cannot escape, the law called holy and just and good "
        "even as sin uses it as a weapon, coveting aroused by the very "
        "command that forbids it, a war between wanting the good and "
        "doing the evil described from the inside, and a cry of "
        "wretchedness left unanswered until the next chapter"),
    "romans8": (CLS,
        "No condemnation declared as a relocation of judgment rather "
        "than its cancellation, nineteen mentions of the Spirit "
        "answering a struggle that had only one in the chapter before, "
        "Abba, Father left standing in Aramaic inside a Greek letter to "
        "a Latin city, a golden chain of five links all spoken of in the "
        "past tense, and five courtroom questions that each expect a "
        "person rather than an argument for an answer"),
    "romans9": (CLS,
        "Paul's willingness to be accursed for brothers he has just "
        "finished grieving over, Isaac chosen over Ishmael and Jacob "
        "over Esau before either had done good or evil, a potter's "
        "authority over clay answering an objection about fairness "
        "before it is fully raised, Hosea and Isaiah both quoted to "
        "include Gentiles among vessels of mercy, and Israel stumbling "
        "at a stumblingstone it sought by works rather than by faith"),
    "romans10": (CLS,
        "Zeal without knowledge diagnosed as Israel's problem rather "
        "than a lack of sincerity, Moses quoted for both ways of "
        "righteousness he is used to argue, no ascent to heaven or "
        "descent to the deep required because the word is already near, "
        "a chain of necessity running backward from calling to being "
        "sent, and God's arms described as stretched out all day toward "
        "a disobedient people"),
    "romans11": (CLS,
        "Paul's own believing as the proof Israel has not been cast "
        "away entirely, an indirect strategy that provokes jealousy "
        "through Gentile salvation rather than bypassing Israel, an "
        "olive tree with natural branches broken off and wild branches "
        "grafted in, a mystery revealed so the Gentiles will not be wise "
        "in their own conceits, and a doxology that answers unanswerable "
        "questions with worship instead of resolution"),
    "romans13": (CLS,
        "Governing authorities named ministers of God ordained to "
        "restrain evil, submission taught as the general principle "
        "rather than an absolute overriding obedience to God, love named "
        "the only debt that never finishes being paid, an ethic given an "
        "actual deadline with the night far spent, and clothing imagery "
        "closing on putting on the Lord Jesus Christ, the verses that "
        "stopped Augustine's argument with himself in a Milan garden"),
    "romans14": (CLS,
        "Strong and weak believers commanded not to judge or despise "
        "each other over disputable matters, a day and a meal both "
        "referred to the Lord rather than argued to a single correct "
        "practice, none of us living to himself grounded in an "
        "accounting each believer gives for themselves alone, liberty "
        "limited by love rather than by rule when a weaker brother could "
        "stumble, and a doxology some manuscripts place here rather "
        "than at the letter's actual end"),
    "romans15": (CLS,
        "The strong asked to bear the weak by Christ's own example of "
        "not pleasing himself, Christ named a minister to the "
        "circumcision and a mercy to the Gentiles in the same careful "
        "sentence, four Old Testament quotations stacked from every part "
        "of the Hebrew Bible to put Jew and Gentile in one sentence, "
        "Spain named as the next frontier for a man who refused to build "
        "on another's foundation, and prayer requested as a wrestling "
        "match over a collection Paul fears will be refused"),
    "romans16": (CLS,
        "Twenty-six people greeted by name in a church Paul had never "
        "visited, women named prominently including a deacon, a couple "
        "where the wife is listed first, and an apostle called Junia, a "
        "warning against smooth talkers slipped into a chapter otherwise "
        "made of greetings, a secretary who signs his own name inside "
        "the letter he is writing, and a doxology that ends the letter "
        "exactly where it began, with the gospel"),
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
