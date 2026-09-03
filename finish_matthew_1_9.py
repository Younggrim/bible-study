#!/usr/bin/env python3
"""
Matthew, first pass: chapters 1 to 9.

Matthew is the last book with any inherited verse-range sections at all, and they are
a strange sample. What has a heading tends to be a single famous verse or a point of
interpretation rather than a passage: 'Galilee of the Gentiles (v.15)', 'The Rock
(v.18)', 'Corban (vv.5-6)', 'The Veil Torn (v.51)', 'The Unforgivable Sin (vv.31-32)'.
Five of these nine pages had nothing at all, including the genealogy, the birth, the
Sermon on the Mount and its conclusion.

Where sections do exist they are kept and worked around. matthew4's 'Galilee of the
Gentiles (v.15)' sits inside the move to Capernaum, so the surrounding section is
written as vv.12-14 and vv.16-17 rather than displacing it. matthew9 keeps
'Matthew's Calling (v.9)' and 'New Wine in New Wineskins (vv.16-17)' the same way.

The inherited topical notes without ranges stay as they are: 'Herod the Great:',
'The Magi:', 'John the Baptist:', 'The Baptism of Jesus:', 'The Temptation:',
'The Six Antitheses:', 'The central theme:'.

Usage:
    python3 finish_matthew_1_9.py [--check]
"""
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
ITEM_RE = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

OPS = {
"matthew1": [
 ("", "The Genealogy (vv.1-17)",
  "The book opens with a legal document rather than a story, and its first line states the two "
  "claims the whole Gospel rests on, the son of David, the son of Abraham. The list is arranged in "
  "three groups of fourteen, from Abraham to David, David to the exile, the exile to Christ, which "
  "is a structure imposed on the record rather than found in it. Four women are named and the "
  "choice of them is deliberate: Thamar, who posed as a prostitute, Rachab, who was one, Ruth, a "
  "Moabitess, and her that had been the wife of Urias, unnamed. Then the last link breaks the "
  "pattern of the whole list. Every other entry says begat. This one says Joseph the husband of "
  "Mary, of whom was born Jesus."),
 ("The Genealogy", "The Birth of Jesus Christ (vv.18-25)",
  "The account is told from Joseph's side throughout, and his first decision is a decent one made "
  "in the wrong direction, being a just man, and not willing to make her a publick example, was "
  "minded to put her away privily. The angel's instruction reverses it and gives the child's name "
  "with its meaning attached, for he shall save his people from their sins. Then the first of "
  "Matthew's fulfilment formulas, quoting Isaiah on the virgin and the name Emmanuel, which "
  "Matthew translates for a reader who might not have Hebrew, God with us. The chapter ends with "
  "obedience described in two flat clauses, he did as the angel of the Lord had bidden him, and "
  "called his name JESUS."),
],
"matthew2": [
 ("", "The Wise Men from the East (vv.1-12)",
  "The visitors are astrologers from outside Israel who read a star correctly and then ask the "
  "wrong man for directions. Herod's court supplies the answer from Micah, and Matthew lets the "
  "irony stand: the scholars know exactly where the Messiah is to be born and none of them travels "
  "the five miles to look. Herod's request for a report is described by Matthew as a lie before it "
  "is one, he sent them, saying, that I may come and worship him also. The gifts are gold, "
  "frankincense and myrrh, and the chapter does not interpret them. The men go home another way, "
  "being warned of God in a dream."),
 ("The Wise Men from the East", "The Flight into Egypt (vv.13-15)",
  "The instruction comes at night and is urgent, arise, and take the young child and his mother, "
  "and flee into Egypt, and Joseph leaves the same night. Matthew attaches Hosea 11:1 to it, out "
  "of Egypt have I called my son, which in Hosea is about the nation coming out of slavery. Matthew "
  "reads the child as retracing Israel's route, which is the pattern the next two chapters keep: "
  "Egypt, then the water, then the wilderness, then the mountain."),
 ("The Flight into Egypt", "Herod Slew the Children (vv.16-18)",
  "Three verses, and Matthew gives the reason for the massacre as wounded pride, when Herod saw "
  "that he was mocked of the wise men, he was exceeding wroth. The order covers all the children "
  "in Bethlehem and the coasts thereof from two years old and under, and the two years is worked "
  "out from what the astrologers told him. Then Jeremiah is quoted, Rachel weeping for her "
  "children, and would not be comforted, because they are not. Matthew offers no consolation with "
  "it."),
 ("Herod Slew the Children", "Return, and Nazareth (vv.19-23)",
  "Three dreams in one chapter guide the family, and the last one changes their destination. "
  "Joseph is told Herod is dead and sets out for Judaea, then hears that Archelaus reigns there and "
  "is warned off, so he turns aside into Galilee and settles at Nazareth. Matthew's closing "
  "fulfilment note has no clear source text and he says so vaguely himself, spoken by the prophets, "
  "he shall be called a Nazarene, which readers have been arguing about ever since. The family "
  "ends up in an obscure town because of a political risk."),
],
"matthew3": [
 ("", "John in the Wilderness (vv.1-6)",
  "The message is two words in the Greek, repent ye, with a reason attached, for the kingdom of "
  "heaven is at hand. Isaiah is quoted, the voice of one crying in the wilderness, and then Matthew "
  "describes the man rather than the doctrine: raiment of camel's hair, a leathern girdle, and his "
  "meat was locusts and wild honey. The clothing is Elijah's, deliberately. The response is a mass "
  "movement, Jerusalem and all Judaea going out to a river to be baptized, confessing their sins."),
 ("John in the Wilderness", "Fruits Worthy of Repentance (vv.7-12)",
  "The Pharisees and Sadducees get a different sermon from the crowd, and it opens O generation of "
  "vipers, who hath warned you to flee from the wrath to come? The demand is for evidence, bring "
  "forth therefore fruits meet for repentance, and the defence he expects is closed off in "
  "advance, think not to say within yourselves, We have Abraham to our father. Then the comparison "
  "with the one coming after, whose shoes I am not worthy to bear, and the two baptisms set side by "
  "side, with the Holy Ghost, and with fire. The threshing floor image at the end has the wheat and "
  "the chaff separated by the same wind."),
 ("Fruits Worthy of Repentance", "The Baptism of Jesus (vv.13-17)",
  "John refuses, and Matthew is the only Gospel to record the exchange, I have need to be baptized "
  "of thee, and comest thou to me? The answer is a reason rather than an order, suffer it to be so "
  "now, for thus it becometh us to fulfil all righteousness. Then the three things that happen at "
  "once: the heavens opened, the Spirit of God descending like a dove, and a voice. Matthew's "
  "wording of the voice is addressed to the onlookers rather than to Jesus, this is my beloved Son, "
  "in whom I am well pleased, which is how Matthew tends to handle the disclosures."),
],
"matthew4": [
 ("", "The Temptation in the Wilderness (vv.1-11)",
  "He is led up of the Spirit into the wilderness to be tempted, so the testing is commissioned "
  "rather than accidental. Forty days and forty nights of fasting sets the parallel with Israel's "
  "forty years and Moses' forty days. Three temptations, and all three are answered from "
  "Deuteronomy, from the same part of the law that describes the wilderness generation failing the "
  "same tests. Bread, answered with man shall not live by bread alone. The temple pinnacle, where "
  "scripture is quoted at him and he answers thou shalt not tempt the Lord thy God. Then all the "
  "kingdoms of the world for one act of worship, refused with get thee hence, Satan. Then angels "
  "came and ministered unto him."),
 ("Galilee of the Gentiles", "He Dwelt in Capernaum (vv.12-14,16-17)",
  "The move is prompted by John's arrest, and Matthew notes the geography carefully because he "
  "wants Isaiah's prophecy to land on it: he leaves Nazareth and settles in Capernaum, on the "
  "border of Zabulon and Nephthalim. Then the quotation about a great light shining on people that "
  "sat in darkness. And the ministry opens with exactly the words John was using, from that time "
  "Jesus began to preach, and to say, Repent, for the kingdom of heaven is at hand. The message "
  "does not change when the messenger does."),
 ("He Dwelt in Capernaum", "Fishers of Men (vv.18-22)",
  "Two pairs of brothers, called in the middle of a working day. Simon and Andrew are casting a "
  "net, James and John are mending theirs with their father in the boat. The call is four words and "
  "a promise, follow me, and I will make you fishers of men, and Matthew records no discussion "
  "either time. What he records is speed, they straightway left their nets, and immediately they "
  "left the ship and their father. The second detail is the costly one: Zebedee is left sitting in "
  "the boat."),
 ("Fishers of Men", "All Galilee, and the Great Multitudes (vv.23-25)",
  "Three verses summarising a whole campaign, and the summary has three verbs, teaching in their "
  "synagogues, preaching the gospel of the kingdom, and healing all manner of sickness. The list of "
  "who came is geographic and reaches outside Israel, from Galilee, Decapolis, Jerusalem, Judaea, "
  "and from beyond Jordan. The crowd assembled in these verses is the audience for the sermon that "
  "begins in the next, which is why Matthew puts the summary here rather than after it."),
],
"matthew5": [
 ("", "The Beatitudes (vv.1-12)",
  "He goes up into a mountain and sits down, which is a teacher's posture, and the disciples come "
  "to him. Nine blessings, and the pattern is consistent: a condition nobody would choose, and a "
  "promise attached to it. Poor in spirit, mourning, meek, hungering after righteousness, merciful, "
  "pure in heart, peacemakers, persecuted. The kingdom is promised twice, at the beginning and at "
  "the eighth, which closes the set. Then the last one changes person from they to ye and gets "
  "three verses instead of one, blessed are ye, when men shall revile you, with a reason that puts "
  "the hearers in a line, for so persecuted they the prophets which were before you."),
 ("The Beatitudes", "Salt and Light (vv.13-16)",
  "Two images for the same thing and both are useless if withheld. Salt that has lost its savour is "
  "good for nothing but to be trodden under foot. A candle is not lit to be put under a bushel, and "
  "a city set on an hill cannot be hid. Then the instruction, and the object of it is not the "
  "reputation of the person shining, let your light so shine before men, that they may see your "
  "good works, and glorify your Father which is in heaven."),
 ("Salt and Light", "Not to Destroy, But to Fulfil (vv.17-20)",
  "Think not that I am come to destroy the law, or the prophets. The denial is emphatic and the "
  "positive claim is stronger than the objection it answers, I am not come to destroy, but to "
  "fulfil, with a guarantee attached about the smallest written mark, one jot or one tittle. Then "
  "the sentence that governs everything after it and would have startled the audience most: except "
  "your righteousness shall exceed the righteousness of the scribes and Pharisees, ye shall in no "
  "case enter into the kingdom of heaven. The standard is being raised, not relaxed."),
 ("Not to Destroy, But to Fulfil", "Anger, Lust, Divorce and Oaths (vv.21-37)",
  "Four of the six antitheses, and each follows the same form: ye have heard that it was said, but "
  "I say unto you. Killing is traced back to anger and to contempt, and the illustration is about "
  "worship, leave there thy gift before the altar, and go thy way, first be reconciled to thy "
  "brother. Adultery is traced to the look. The remedies proposed are deliberately extreme, if thy "
  "right eye offend thee, pluck it out. Divorce is restricted to one ground. And oaths are removed "
  "altogether in favour of plain speech, let your communication be, Yea, yea, Nay, nay, with the "
  "reasoning that a man who swears by heaven or earth or his own head is pledging things he does "
  "not own."),
 ("Anger, Lust, Divorce and Oaths", "Love Your Enemies (vv.38-48)",
  "The last two antitheses. An eye for an eye is replaced not by pacifism in the abstract but by "
  "four specific responses, the other cheek, the cloak as well as the coat, the second mile, and "
  "lending without turning away. Then love your enemies, bless them that curse you, and the reason "
  "given is imitation rather than results, for he maketh his sun to rise on the evil and on the "
  "good, and sendeth rain on the just and on the unjust. The argument closes by pointing out that "
  "loving people who love you back is not distinctive, do not even the publicans the same? And then "
  "the sentence the whole chapter has been building toward, be ye therefore perfect, even as your "
  "Father which is in heaven is perfect."),
],
"matthew6": [
 ("", "Do Not Your Alms Before Men (vv.1-8)",
  "Three religious duties are treated in the same shape, and the shape is the point: alms, prayer "
  "and fasting each done for men, with a reward already received, or done in secret, with a reward "
  "from the Father which seeth in secret. The illustrations are physical and slightly comic, a "
  "trumpet sounded before a donation, prayer performed standing in the corners of the streets. The "
  "instruction about prayer is spatial, enter into thy closet, and shut thy door. And the warning "
  "against long prayers is about the assumption behind them, be not ye therefore like unto them, "
  "for your Father knoweth what things ye have need of, before ye ask him."),
 ("The Lord's Prayer", "Forgiveness, Fasting, and Treasure (vv.14-24)",
  "The one petition of the prayer that gets an expansion is the one about forgiveness, and the "
  "expansion runs both ways, if ye forgive not men their trespasses, neither will your Father "
  "forgive your trespasses. Then fasting, with the same secrecy rule and a practical instruction, "
  "anoint thine head, and wash thy face. Then treasure, and the argument is about durability first, "
  "where moth and rust doth corrupt, and about the heart second, for where your treasure is, there "
  "will your heart be also. The single eye follows, and then the sentence that closes the section "
  "with no middle option offered, ye cannot serve God and mammon."),
],
"matthew7": [
 ("", "Judge Not (vv.1-6)",
  "Judge not, that ye be not judged, and the reason given is reciprocity rather than relativism, "
  "with what measure ye mete, it shall be measured to you again. Then the mote and the beam, which "
  "is a joke with a serious end: the objection is not to correcting a brother but to correcting him "
  "while unable to see. The instruction is sequential, first cast out the beam out of thine own "
  "eye, and then shalt thou see clearly to cast out the mote. And immediately after it a saying "
  "that limits the whole passage, give not that which is holy unto the dogs, so this is not a "
  "prohibition on discernment."),
 ("Judge Not", "Ask, Seek, Knock (vv.7-12)",
  "Three imperatives with three promises, and then the argument from ordinary fatherhood, what man "
  "is there of you, whom if his son ask bread, will he give him a stone? The premise about human "
  "nature is conceded in passing, if ye then, being evil, know how to give good gifts unto your "
  "children. Then the sentence Matthew places as the summary of the whole sermon so far, all things "
  "whatsoever ye would that men should do to you, do ye even so to them, with the note that this is "
  "the law and the prophets. The rule is stated positively, which is what distinguishes it from its "
  "many negative predecessors."),
 ("Ask, Seek, Knock", "The Strait Gate and the False Prophets (vv.13-23)",
  "Two gates, two ways, and the numbers are given, many there be which go in thereat, and few there "
  "be that find it. Then false prophets, and the test offered is not doctrine but produce, ye shall "
  "know them by their fruits, with the observation that grapes do not come off thorns. The section "
  "ends on the most disquieting passage in the sermon: people who called him Lord, prophesied, cast "
  "out devils and did many wonderful works, and are told I never knew you. Not their works but "
  "their knowledge of him is what is at issue, and the sentence between the two is the criterion, "
  "he that doeth the will of my Father which is in heaven."),
 ("The Strait Gate and the False Prophets", "The House on the Rock (vv.24-29)",
  "The closing parable has two builders and one storm, and the difference between them is not effort "
  "or materials but foundation. Whosoever heareth these sayings of mine, and doeth them, is likened "
  "unto a wise man which built his house upon a rock. Both houses face the same rain, floods and "
  "wind. Then Matthew's own note on the effect, and it is about authority rather than content, the "
  "people were astonished at his doctrine, for he taught them as one having authority, and not as "
  "the scribes."),
],
"matthew8": [
 ("The Centurion", "Peter's Wife's Mother, and the Cost (vv.14-22)",
  "The healing is domestic and brief, he touched her hand, and the fever left her, and she arose, "
  "and ministered unto them. Then a summary of an evening's work with a quotation attached, Isaiah "
  "on bearing our sicknesses. What follows is the passage that gives the section its edge. A scribe "
  "offers to follow him anywhere and is warned about accommodation, the Son of man hath not where "
  "to lay his head. Another asks to bury his father first and receives the hardest answer in the "
  "chapter, follow me, and let the dead bury their dead. Matthew places both immediately before a "
  "boat trip into a storm."),
 ("The Storm", "The Two Possessed of Devils (vv.28-34)",
  "Matthew has two men rather than one, and describes them as exceeding fierce, so that no man "
  "might pass that way. Their question is the one the demons ask throughout this Gospel, art thou "
  "come hither to torment us before the time? which concedes the outcome and disputes the "
  "timetable. The herd of swine runs into the sea. Then the reaction, which is the point of the "
  "episode: the keepers go and tell the city, and the whole city comes out, and what they ask for "
  "is his departure. Two men are restored and a town would rather have its livestock."),
],
"matthew9": [
 ("Matthew's Calling", "Why Eateth Your Master with Publicans (vv.10-15)",
  "The dinner at Matthew's house draws two separate objections, and Jesus answers both with "
  "quotations. To the Pharisees asking why he eats with publicans and sinners, he cites Hosea, I "
  "will have mercy, and not sacrifice, with the medical proverb before it, they that be whole need "
  "not a physician, but they that are sick. To John's disciples asking about fasting, the answer is "
  "a wedding, can the children of the bridechamber mourn, as long as the bridegroom is with them? "
  "and then the clause that darkens it, the days will come, when the bridegroom shall be taken from "
  "them, and then shall they fast."),
 ("New Wine in New Wineskins", "The Ruler's Daughter and the Woman (vv.18-26)",
  "Matthew's version is the shortest of the three and keeps the structure: a request interrupted by "
  "a healing. The ruler's statement is more absolute here than in Mark, my daughter is even now "
  "dead, come and lay thy hand upon her, and she shall live. The woman with the issue of blood "
  "twelve years touches the hem of his garment and is told her faith hath made her whole. At the "
  "house the minstrels are already in and the crowd is put out with a sentence they laugh at, the "
  "maid is not dead, but sleepeth. He took her by the hand, and the maid arose."),
 ("The Ruler's Daughter and the Woman", "Two Blind Men, and a Dumb Man (vv.27-34)",
  "Two blind men follow him calling him thou son of David, which is the first time anyone in "
  "Matthew uses the title in public. The question put to them is about belief rather than need, "
  "believe ye that I am able to do this? and the healing is according to your faith be it unto you. "
  "He charges them strictly to tell no one and they spread it abroad in all that country. Then a "
  "dumb man possessed with a devil, and the two reactions Matthew sets against each other: the "
  "multitudes marvelled, saying, It was never so seen in Israel, and the Pharisees said, He casteth "
  "out devils through the prince of the devils."),
 ("Two Blind Men, and a Dumb Man", "The Harvest Is Plenteous (vv.35-38)",
  "The chapter closes with the same three-verb summary that opened the ministry, teaching, "
  "preaching and healing, and then the sentence that explains the whole section: when he saw the "
  "multitudes, he was moved with compassion on them, because they fainted, and were scattered "
  "abroad, as sheep having no shepherd. The diagnosis is a leadership failure. Then the harvest "
  "image, the harvest truly is plenteous, but the labourers are few, and an instruction that is "
  "not to go but to ask, pray ye therefore the Lord of the harvest, that he will send forth "
  "labourers. The men who pray it are sent in the first verse of the next chapter."),
],
}


def find(items, prefix):
    for i, (label, _) in enumerate(items):
        if H.unescape(label).strip().startswith(prefix):
            return i
    return -1


def first_section(items):
    for i, (label, _) in enumerate(items):
        if re.search(r"\(vv?\.[^)]*\)\s*:?\s*$", H.unescape(label).strip()):
            return i
    return len(items)


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, ops in OPS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        for after, label, prose in ops:
            at = first_section(items) if after == "" else find(items, after) + 1
            if after and at == 0:
                problems.append(f"{page}: insert anchor {after!r} not found")
                continue
            items.insert(at, [label + ":", prose])
            notes.append(f"{page}: inserted {label!r}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    for n in notes:
        print(f"    {n}")
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would touch' if check else 'touched'} {len(planned)} pages, "
          f"{len(notes)} change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
