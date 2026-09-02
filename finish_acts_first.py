#!/usr/bin/env python3
"""
Acts, first half: the eleven pages in chapters 2 to 16 that the audit flags.

The recurring failure here is that Luke's set pieces survived and the narrative
between them did not. acts5 kept Ananias and Sapphira and Gamaliel's counsel and lost
everything in between, which is the arrest, the angel opening the prison, and the
apostles found teaching in the temple the next morning by officers who had locked the
door themselves. acts10 kept Cornelius and the vision and the Gentile Pentecost and
lost the twenty-seven verses that join them, including Peter walking into a Gentile
house and the sermon he preaches once he is inside.

acts16 lost vv.11-24, which is Lydia, the girl with the spirit of divination, and the
beating that puts Paul in the cell where the earthquake finds him. Only the jailer's
conversion had a section, so the page described the rescue and not the imprisonment.

One structural repair: acts9 ran 'Saul's Conversion (vv.1-19)' with a nested 'Ananias'
Obedience (vv.10-19)' inside it, describing ten verses twice. The conversion becomes
vv.1-9, which is where the road to Damascus actually ends.

Usage:
    python3 finish_acts_first.py [--check]
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
RANGE_IN_LABEL = re.compile(r"\(vv?\.[^)]*\)(?=\s*:?\s*$)")

OPS = {
"acts2": [
 ("insert", "Peter's Sermon", "Pricked in Their Heart (vv.37-41)",
  "The response to the sermon is recorded as a physical reaction before it is a decision, now "
  "when they heard this, they were pricked in their heart, and said, Men and brethren, what "
  "shall we do? The answer is four things in one sentence: repent, be baptized every one of you "
  "in the name of Jesus Christ for the remission of sins, and ye shall receive the gift of the "
  "Holy Ghost. The promise is extended past the room in a clause that has kept commentators "
  "busy, unto you, and to your children, and to all that are afar off. Luke notes that Peter "
  "said much more than is recorded, with many other words did he testify, and gives the number, "
  "about three thousand souls."),
],
"acts4": [
 ("insert", "", "Peter and John Arrested (vv.1-4)",
  "The priests and the captain of the temple and the Sadducees come upon them being grieved, and "
  "Luke names the specific offence: that they taught the people, and preached through Jesus the "
  "resurrection from the dead. The Sadducees denied resurrection, so this is doctrinal as much "
  "as public order. They are put in hold until the next day because it was now eventide, and the "
  "verse that closes the paragraph makes the arrest look futile, howbeit many of them which "
  "heard the word believed, and the number of the men was about five thousand."),
 ("insert", "Peter Before the Sanhedrin", "We Cannot But Speak (vv.13-22)",
  "The council's first observation is about class rather than argument, they perceived that they "
  "were unlearned and ignorant men, and they took knowledge of them, that they had been with "
  "Jesus. The difficulty is the healed man standing there, we cannot deny it, so they confer "
  "privately and settle on suppression rather than refutation, that they speak henceforth to no "
  "man in this name. The answer is put as a question they cannot answer, whether it be right in "
  "the sight of God to hearken unto you more than unto God, judge ye, and then the flat refusal, "
  "we cannot but speak the things which we have seen and heard. They are released because of the "
  "crowd, and Luke adds the man's age, above forty years old, which rules out a temporary "
  "complaint."),
 ("insert", "The Church's Prayer", "All Things Common (vv.32-37)",
  "The community is described in one sentence that runs together conviction and property, the "
  "multitude of them that believed were of one heart and of one soul, neither said any of them "
  "that ought of the things which he possessed was his own. Luke is careful about the mechanism: "
  "sales were occasional and voluntary, as many as were possessors of lands or houses sold them, "
  "and laid them down at the apostles' feet, and distribution was according to need. The result "
  "is stated plainly, neither was there any among them that lacked. Then one man is named as the "
  "example, Barnabas, which is being interpreted, The son of consolation, and the naming sets up "
  "the contrast the next chapter opens with."),
],
"acts5": [
 ("insert", "Ananias and Sapphira", "Signs in Solomon's Porch (vv.12-16)",
  "Two things are recorded together and they sit oddly side by side. The apostles are performing "
  "signs in Solomon's porch and the people magnify them, and yet of the rest durst no man join "
  "himself to them. Fear and admiration at once, which is what chapter 5 has just produced. Then "
  "a detail Luke reports without comment, that they brought the sick into the streets so that "
  "the shadow of Peter passing by might overshadow some of them, and that people came from the "
  "cities round about and were healed every one."),
 ("insert", "Signs in Solomon's Porch", "The Angel Opens the Prison (vv.17-26)",
  "The high priest arrests them, and the escape is described with no drama at all: the angel of "
  "the Lord by night opened the prison doors, and brought them forth, and the instruction given "
  "is to go straight back and do the thing they were arrested for, go, stand and speak in the "
  "temple to the people all the words of this life. What Luke enjoys is the morning after. The "
  "council assembles, sends for the prisoners, and the officers return baffled, the prison truly "
  "found we shut with all safety, and the keepers standing without before the doors, but when we "
  "had opened, we found no man within. Then somebody comes in with the news, behold, the men "
  "whom ye put in prison are standing in the temple, and teaching the people."),
 ("insert", "The Angel Opens the Prison", "We Ought to Obey God (vv.27-33)",
  "The charge is that they filled Jerusalem with this doctrine, and it includes a phrase that "
  "gives away the council's real objection, ye intend to bring this man's blood upon us. The "
  "answer is the sentence the chapter is remembered for, we ought to obey God rather than men, "
  "and then the accusation is accepted and turned round, whom ye slew and hanged on a tree. The "
  "witnesses named are two, and we are his witnesses of these things, and so is also the Holy "
  "Ghost, whom God hath given to them that obey him. Luke records the effect in five words, "
  "they were cut to the heart, and took counsel to slay them."),
 ("insert", "Gamaliel's Counsel", "Beaten, and Rejoicing (vv.40-42)",
  "Gamaliel's advice is taken but only halfway: they agreed with him, and when they had called "
  "the apostles, and beaten them, they let them go. The council that decided not to kill them "
  "still had them flogged. Then the response that Luke sets against it, and they departed from "
  "the presence of the council, rejoicing that they were counted worthy to suffer shame for his "
  "name. The chapter closes on persistence rather than triumph, and daily in the temple, and in "
  "every house, they ceased not to teach and preach Jesus Christ."),
],
"acts8": [
 ("insert", "", "Scattered Abroad (vv.1-4)",
  "Saul is introduced by consent rather than action, and Saul was consenting unto his death, and "
  "then by violence, entering into every house, and haling men and women committed them to "
  "prison. The persecution scatters the church throughout the regions of Judaea and Samaria, "
  "except the apostles, who stay. Luke records the burial of Stephen with a phrase that carries "
  "the cost, devout men made great lamentation over him. Then the sentence that turns the "
  "disaster into the book's method, therefore they that were scattered abroad went every where "
  "preaching the word. The mission spreads because the church is broken up."),
],
"acts9": [
 ("retitle", "Saul's Conversion", "(vv.1-9)"),
 ("insert", "Saul's Immediate Ministry", "Peter at Lydda and Joppa (vv.31-43)",
  "The narrative leaves Saul and returns to Peter for two miracles that prepare for chapter 10. "
  "Aeneas at Lydda has kept his bed eight years, and the healing is two sentences long. Then "
  "Tabitha at Joppa, whose name Luke gives in both languages, and the scene is domestic and "
  "closely observed: the widows standing by weeping, showing the coats and garments which she "
  "made while she was with them. Peter puts them all out, kneels, and says two words, Tabitha, "
  "arise. The chapter ends with a detail that matters more than it looks, he tarried many days "
  "in Joppa with one Simon a tanner, a trade that made a man ceremonially unclean, which is "
  "where the messengers from Cornelius will find him."),
],
"acts10": [
 ("insert", "Peter's Vision", "The Men from Caesarea (vv.17-23)",
  "Peter is still puzzling over the vision when the knock comes, and Luke makes the timing "
  "explicit, while Peter thought on the vision, the Spirit said unto him, Behold, three men seek "
  "thee. The instruction removes his discretion, go with them, doubting nothing, for I have sent "
  "them. The men state their business and their master's rank, Cornelius the centurion, a just "
  "man, and one that feareth God, and of good report among all the nation of the Jews. Then the "
  "first breach: then called he them in, and lodged them. A Jewish man puts three Gentiles up "
  "for the night before he has worked out what the vision meant."),
 ("insert", "The Men from Caesarea", "Peter Enters a Gentile House (vv.24-33)",
  "Cornelius has called together his kinsmen and near friends, so a private enquiry has become a "
  "gathering. He falls at Peter's feet and is picked up with a correction, stand up, I myself "
  "also am a man. Then Peter states what everyone in the room already knows, ye know how that it "
  "is an unlawful thing for a man that is a Jew to keep company with one of another nation, and "
  "gives his reason for coming anyway, God hath shewed me that I should not call any man common "
  "or unclean. Cornelius recounts the angel, and the last line is a sentence any preacher would "
  "want to hear, now therefore are we all here present before God, to hear all things that are "
  "commanded thee of God."),
 ("insert", "Peter Enters a Gentile House", "God Is No Respecter of Persons (vv.34-43)",
  "The sermon opens with the conclusion Peter has just been forced to, of a truth I perceive that "
  "God is no respecter of persons, but in every nation he that feareth him is accepted with him. "
  "What follows is the shortest summary of the gospel in Acts and it is almost entirely "
  "biographical: baptized by John, anointed with the Holy Ghost and with power, went about doing "
  "good, hanged on a tree, raised up the third day. The witness clause is careful about who saw "
  "it, not to all the people, but unto witnesses chosen before of God, even to us, who did eat "
  "and drink with him after he rose from the dead. And the offer at the end is open, whosoever "
  "believeth in him shall receive remission of sins."),
],
"acts11": [
 ("insert", "The Church at Antioch", "Agabus and the Famine Relief (vv.27-30)",
  "A prophet named Agabus signifies by the Spirit that there shall be great dearth throughout all "
  "the world, and Luke dates it, which came to pass in the days of Claudius Caesar. The response "
  "is the first recorded collection in the church, and the principle is stated in one clause, "
  "every man according to his ability. Money goes from a Gentile congregation to the Jewish "
  "believers in Judaea, carried by Barnabas and Saul, which is the pattern Paul's later letters "
  "spend chapters arguing for."),
],
"acts13": [
 ("insert", "The Antioch Church", "Cyprus and Bar-jesus (vv.4-12)",
  "The first stop is Cyprus, Barnabas' home, and the confrontation there is with a Jewish "
  "sorcerer and false prophet named Bar-jesus, who is attached to the Roman governor. Luke marks "
  "the change of name at exactly this point, then Saul, who also is called Paul, and from here on "
  "uses the Roman one. The rebuke is fierce, O full of all subtilty and all mischief, thou child "
  "of the devil, and the judgement fits the offence, blindness for a season on a man who had been "
  "obscuring the way of the Lord. The governor believes, being astonished at the doctrine of the "
  "Lord."),
 ("insert", "Cyprus and Bar-jesus", "Into the Synagogue at Antioch (vv.13-15)",
  "Three verses of travel that carry two things worth noticing. John Mark departs from them and "
  "returns to Jerusalem, which Luke reports without explanation here and which will split Paul "
  "from Barnabas in chapter 15. Then the mechanics of the mission: they go into the synagogue on "
  "the sabbath and sit down, and the invitation to speak is extended by the rulers as ordinary "
  "hospitality to visitors, ye men and brethren, if ye have any word of exhortation for the "
  "people, say on."),
 ("insert", "Paul's Sermon at Pisidian Antioch", "The Next Sabbath, and the Envy (vv.42-45)",
  "The reception is enthusiastic and the invitation is to come back, and Luke gives the size of "
  "the second congregation, the next sabbath day came almost the whole city together to hear the "
  "word of God. That is what produces the opposition, and Luke names the motive without "
  "softening it, when the Jews saw the multitudes, they were filled with envy, and spake against "
  "those things which were spoken by Paul, contradicting and blaspheming."),
 ("insert", "The Turn to the Gentiles", "Expelled, and Filled with Joy (vv.49-52)",
  "The word is published throughout all the region, and the counter-move is political rather "
  "than theological: the devout and honourable women and the chief men of the city are stirred "
  "up, and Paul and Barnabas are expelled out of their coasts. They shake the dust off their "
  "feet, which is the gesture Jesus prescribed. Then the last verse, and it is one of Luke's "
  "quiet reversals, and the disciples were filled with joy, and with the Holy Ghost. The "
  "missionaries are thrown out and the congregation they leave behind is described as full."),
],
"acts14": [
 ("insert", "", "Iconium (vv.1-7)",
  "The pattern established at Antioch repeats, and Luke states it as a pattern: they go into the "
  "synagogue, a great multitude of Jews and Greeks believe, and the unbelieving stir up the "
  "Gentiles. The city divides, part held with the Jews, and part with the apostles, and when an "
  "assault is organised they leave rather than confront it, they were aware of it, and fled unto "
  "Lystra and Derbe. There is no bravado in the account. They stay a long time, they leave when "
  "it becomes impossible, and they preach in the next place."),
 ("insert", "Paul Stoned", "Confirming the Souls of the Disciples (vv.20-28)",
  "The day after being stoned and left for dead, he departed with Barnabas to Derbe, which Luke "
  "reports in one clause. Then the return journey, and it goes back through the same towns they "
  "were driven out of: Lystra, Iconium, Antioch, confirming the souls of the disciples, and the "
  "encouragement offered is not comfort but a warning, that we must through much tribulation "
  "enter into the kingdom of God. Elders are ordained in every church. The chapter ends with the "
  "report at Antioch, rehearsing all that God had done with them, and how he had opened the door "
  "of faith unto the Gentiles, which is the sentence chapter 15 will be fought over."),
],
"acts15": [
 ("insert", "The Jerusalem Council", "The Letter to the Gentiles (vv.22-35)",
  "The decision is put in writing and carried by named men, Judas and Silas, chosen so that the "
  "Gentile churches hear it from Jerusalem's own people rather than from Paul alone. The letter "
  "disowns the agitators explicitly, certain which went out from us have troubled you, saying, Ye "
  "must be circumcised, to whom we gave no such commandment. Then the clause that has been argued "
  "over ever since, it seemed good to the Holy Ghost, and to us, to lay upon you no greater "
  "burden than these necessary things. Four items follow, three of them about food and one about "
  "sexual conduct. The reception is recorded as relief, they rejoiced for the consolation."),
],
"acts16": [
 ("insert", "", "Timothy Joins Them (vv.1-5)",
  "Timothy is introduced by his parentage, the son of a certain woman, which was a Jewess, and "
  "believed, but his father was a Greek, and by his reputation, well reported of by the brethren. "
  "Then the decision that looks like a contradiction of the chapter before it: Paul took and "
  "circumcised him because of the Jews which were in those quarters. Having just won the argument "
  "that circumcision cannot be required, he performs it where it removes an obstacle, which is "
  "the distinction between a principle and a tactic. The council's letters are delivered as they "
  "go, and the churches were established in the faith, and increased in number daily."),
 ("insert", "The Macedonian Call", "Lydia at Philippi (vv.11-15)",
  "The first convert in Europe is a businesswoman. On the sabbath they go outside the city to the "
  "riverside, where prayer was wont to be made, which suggests Philippi had no synagogue, and "
  "speak to the women gathered there. Lydia is a seller of purple, an expensive trade, and Luke "
  "credits the outcome to God rather than to the argument, whose heart the Lord opened, that she "
  "attended unto the things which were spoken of Paul. Her household is baptized and she presses "
  "them to stay in her house, and Luke keeps the form of the invitation, if ye have judged me to "
  "be faithful to the Lord, come into my house, and abide there. And she constrained us."),
 ("insert", "Lydia at Philippi", "The Damsel and the Beating (vv.16-24)",
  "The girl with a spirit of divination follows them for many days shouting something true, these "
  "men are the servants of the most high God, which shew unto us the way of salvation, and Paul "
  "eventually finds it unbearable rather than useful. The charge brought after her deliverance is "
  "economic and is stated without embarrassment by her owners, they saw that the hope of their "
  "gains was gone, though the accusation they make in court is about religion and public order. "
  "Then the beating, and Luke gives the details that make the next scene legally explosive: they "
  "were rent of their clothes and beaten with many stripes without trial, thrust into the inner "
  "prison, and their feet made fast in the stocks."),
 ("insert", "The Philippian Jailer", "Roman Citizens, Uncondemned (vv.35-40)",
  "In the morning the magistrates send word to let them go quietly, and Paul refuses to be "
  "released quietly. The objection is legal and precise: they have beaten us openly uncondemned, "
  "being Romans, and have cast us into prison, and now do they thrust us out privily? nay verily, "
  "but let them come themselves and fetch us out. Beating an uncondemned Roman citizen was a "
  "serious offence, and Luke records the reaction, they feared, when they heard that they were "
  "Romans. The magistrates come in person. Paul's reason for insisting is left implicit and it is "
  "not personal, because the young church at Lydia's house has to live in this city after he "
  "leaves."),
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
        for op in ops:
            if op[0] == "retitle":
                prefix, rng = op[1], op[2]
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: retitle target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                notes.append(f"{page}: retitled {prefix!r} to {rng}")
            else:
                _, after, label, prose = op
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
