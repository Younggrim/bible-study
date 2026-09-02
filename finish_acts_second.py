#!/usr/bin/env python3
"""
Acts, second half: chapters 17 to 28. Twelve pages, and this completes the book.

The last third of Acts is Paul under arrest, and that is exactly the part these pages
lost. acts22 had one section, 'Roman Citizenship (vv.25-29)', for thirty verses, so
the defence speech in Hebrew that produced the riot had no description while the legal
technicality that stopped the flogging did. acts26 had 'Paul's Commission (vv.16-18)'
and 'Paul's Wish (v.29)', which is to say two extracts from a speech whose twenty-eight
other verses were undescribed, including 'almost thou persuadest me' in the mouth of
the man it is addressed to.

acts20 had one section, the farewell at Miletus, and nothing for vv.1-16, which is
where Eutychus falls out of the window during a sermon that had already run to
midnight.

acts27 lost the beginning and the end of the shipwreck, keeping the storm and Paul's
leadership in the middle. The lost verses include the decision to sail against his
advice and the landing where every one of the two hundred and seventy-six gets ashore.

Two structural repairs. acts18's 'Aquila and Priscilla (vv.2-3,18,26)' overlapped
'Apollos (vv.24-28)' at v.26, so it becomes vv.2-3 and v.18, and the Apollos section
keeps the verse where they take him aside. acts28's 'Paul in Rome (vv.16-31)' sat over
'The Open Ending (vv.30-31)', so it becomes vv.16-29.

Usage:
    python3 finish_acts_second.py [--check]
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
"acts17": [
 ("insert", "", "Thessalonica, and the World Turned Upside Down (vv.1-9)",
  "Luke describes the method as a habit, as his manner was, and gives the content in three "
  "sabbaths of reasoning out of the scriptures, opening and alleging that Christ must needs have "
  "suffered. The charge brought against them is the most quotable line in the chapter and it is "
  "the opposition's, not Luke's: these that have turned the world upside down are come hither "
  "also. The legal accusation is political, they do contrary to the decrees of Caesar, saying "
  "that there is another king, one Jesus. Jason is made to post security, which is why Paul "
  "leaves rather than stays to argue."),
],
"acts18": [
 ("retitle", "Aquila and Priscilla", "(vv.2-3,18)"),
 ("insert", "", "Corinth, and the Turn to the Gentiles (vv.1,4-8)",
  "Paul comes to Corinth and works, and the reasoning in the synagogue continues every sabbath "
  "until Silas and Timothy arrive from Macedonia and he is pressed in the spirit. When the "
  "opposition turns to blasphemy the break is made with a gesture, he shook his raiment, and a "
  "sentence, your blood be upon your own heads, from henceforth I will go unto the Gentiles. "
  "Then Luke records where he went: into the house next door, and the man he converted was "
  "Crispus, the chief ruler of the synagogue, with all his house."),
 ("insert", "God's Encouragement", "A Year and Six Months (vv.11-17)",
  "The promise of the previous verses is followed by the longest settled stay in the book so far, "
  "a year and six months, teaching the word of God among them. Then the case before Gallio, and "
  "Luke's interest is in how it collapses. Paul is not permitted to speak. Gallio dismisses it "
  "before he can, and the reason he gives is jurisdictional, if it be a question of words and "
  "names, and of your law, look ye to it, for I will be no judge of such matters. A Roman "
  "official declining to adjudicate Christian doctrine is a precedent that protects the mission "
  "for years."),
 ("insert", "A Year and Six Months", "Ephesus, and the Vow at Cenchrea (vv.19-23)",
  "The return journey is compressed and two details survive it. At Ephesus he reasons in the "
  "synagogue and is asked to stay, and declines, but promises to come back if God will, which he "
  "does in the next chapter. And at Cenchrea he had shorn his head, for he had a vow, which Luke "
  "reports without explanation. The man who fought the circumcision party in chapter 15 keeps a "
  "Nazarite-style vow of his own accord. The section ends with him going over all the country of "
  "Galatia and Phrygia in order, strengthening all the disciples."),
],
"acts19": [
 ("insert", "The Disciples of John", "Two Years in the School of Tyrannus (vv.8-12)",
  "Three months in the synagogue, then a move to a lecture hall, disputing daily in the school of "
  "one Tyrannus, for the space of two years. It is the longest single stay Luke records and the "
  "result is stated geographically, all they which dwelt in Asia heard the word. Then a detail "
  "Luke labels as unusual himself, God wrought special miracles by the hands of Paul, so that "
  "from his body were brought unto the sick handkerchiefs and aprons. The wording keeps a "
  "distance from the practice while reporting that it worked, which sets up the counterfeits in "
  "the next paragraph."),
 ("insert", "The Burning of the Books", "Paul Purposed to Go to Jerusalem (vv.21-22)",
  "Two verses of planning that shape the rest of the book. After these things were ended, Paul "
  "purposed in the spirit, when he had passed through Macedonia and Achaia, to go to Jerusalem, "
  "saying, After I have been there, I must also see Rome. Both destinations are named here, and "
  "he reaches both, though not in the manner he intends. Timothy and Erastus are sent ahead into "
  "Macedonia while he stays in Asia."),
],
"acts20": [
 ("insert", "", "Through Macedonia to Troas (vv.1-6)",
  "The itinerary is given briskly, and one line in it explains a change of route: when the Jews "
  "laid wait for him, as he was about to sail into Syria, he purposed to return through "
  "Macedonia. Then a list of seven travelling companions by name and province, which is the "
  "delegation carrying the collection Paul spends two letters organising. Luke slips back into "
  "the first person here, we sailed away from Philippi, and gives the crossing as five days."),
 ("insert", "Through Macedonia to Troas", "Eutychus Falls from the Window (vv.7-12)",
  "The meeting is on the first day of the week to break bread, and Paul preaches until midnight "
  "in an upper chamber with many lights. Luke gives the young man a name, Eutychus, a location, "
  "sitting in a window, and a cause, being fallen into a deep sleep, and then the fall from the "
  "third loft, and was taken up dead. The recovery is handled in a sentence and Paul goes back "
  "upstairs and talks until daybreak. The chapter that contains the most famous farewell speech "
  "in Acts also contains the most human detail in it: a boy who could not stay awake."),
 ("insert", "Eutychus Falls from the Window", "The Coasting Voyage to Miletus (vv.13-16)",
  "Four verses of sailing that exist to explain why the elders have to come to him. Paul had "
  "determined to sail by Ephesus rather than into it, because he hasted, if it were possible for "
  "him, to be at Jerusalem the day of Pentecost. He does not want to spend time in Asia. So the "
  "farewell that follows is delivered at a port thirty miles away to men who travelled to reach "
  "it."),
],
"acts21": [
 ("insert", "", "The Voyage to Tyre (vv.1-3)",
  "Three verses of coastline, Coos, Rhodes, Patara, then a ship crossing to Phenicia with Cyprus "
  "left on the port side, and Tyre, where they landed to unlade her burden. The detail about "
  "cargo is the kind of thing that survives only in an eyewitness account, and Luke is writing "
  "in the first person through this whole passage."),
 ("insert", "Warnings Against Going",
  "Caesarea, and Philip's Four Daughters (vv.5-10)",
  "The departure from Tyre is described as a scene rather than a schedule: they brought us on our "
  "way, with wives and children, till we were out of the city, and we kneeled down on the shore, "
  "and prayed. Then Ptolemais, then Caesarea, and the house of Philip the evangelist, which is "
  "the same Philip who baptized the Ethiopian in chapter 8, now settled with a family. Luke notes "
  "in passing that he had four daughters, virgins, which did prophesy, and says nothing more "
  "about them."),
 ("insert", "Caesarea, and Philip's Four Daughters", "The Will of the Lord Be Done (vv.13-14)",
  "Everyone in the room is weeping and trying to stop him, and his answer refuses the premise "
  "that this is about danger: what mean ye to weep and to break mine heart? for I am ready not to "
  "be bound only, but also to die at Jerusalem for the name of the Lord Jesus. The company gives "
  "up in a sentence Luke puts carefully, and when he would not be persuaded, we ceased, saying, "
  "The will of the Lord be done. They do not conclude that they were wrong. They conclude that "
  "the argument is over."),
 ("insert", "The Will of the Lord Be Done", "James, and Four Men Under a Vow (vv.15-26)",
  "The reception at Jerusalem is warm and the report is well received, and then James raises the "
  "problem: thou seest, brother, how many thousands of Jews there are which believe, and they are "
  "all zealous of the law. The rumour to be dealt with is that Paul teaches Jews to forsake "
  "Moses. The proposal is a demonstration, join four men who have a vow and pay their charges, "
  "that all may know that those things, whereof they were informed concerning thee, are nothing. "
  "The council's own decision about Gentiles is restated unchanged in the same breath. Paul "
  "agrees and goes into the temple, which is where he is when the mob forms."),
 ("insert", "Paul's Arrest", "May I Speak Unto the People (vv.37-40)",
  "The chapter ends on two surprises for the officer holding him. The first is language, canst "
  "thou speak Greek? because he had assumed he was the Egyptian agitator who led four thousand "
  "men into the wilderness. The second is composure: Paul asks permission to address the crowd "
  "that has just tried to kill him. Licence is given, and Luke sets the scene precisely, Paul "
  "stood on the stairs, and beckoned with the hand unto the people, and when there was made a "
  "great silence, he spake unto them in the Hebrew tongue."),
],
"acts22": [
 ("insert", "", "The Defence in Hebrew (vv.1-21)",
  "Speaking in Hebrew wins him a hearing, they kept the more silence, and the speech is built "
  "entirely on common ground. He is a Jew of Tarsus, brought up in this city at the feet of "
  "Gamaliel, taught according to the perfect manner of the law of the fathers, and he persecuted "
  "this way unto the death. The high priest and all the estate of the elders are cited as "
  "witnesses to that. Then the Damascus road told for the second of three times in Acts, with "
  "Ananias described in terms this audience would accept, a devout man according to the law, "
  "having a good report of all the Jews which dwelt there. The speech is going well until the "
  "last sentence, and it is one word that ends it: I will send thee far hence unto the Gentiles."),
 ("insert", "The Defence in Hebrew", "Away With Such a Fellow (vv.22-24)",
  "They gave him audience unto this word, and then lifted up their voices, and said, Away with "
  "such a fellow from the earth, for it is not fit that he should live. Luke records the crowd "
  "crying out and casting off their clothes and throwing dust into the air. The chief captain, "
  "who cannot follow the Hebrew and can see the reaction, does what a Roman officer does with an "
  "unexplained riot: he orders him examined by scourging, that he might know wherefore they cried "
  "so against him."),
 ("insert", "Roman Citizenship", "Brought Before the Council (v.30)",
  "The examination by torture having been abandoned, the chief captain tries the other way of "
  "finding out what the charge is: on the morrow he loosed him from his bands, and commanded the "
  "chief priests and all their council to appear, and brought Paul down and set him before them. "
  "A Roman officer convenes the Sanhedrin as a fact-finding exercise, which is how chapter 23 "
  "begins."),
],
"acts23": [
 ("insert", "The Assassination Plot", "Sent to Felix by Night (vv.23-35)",
  "The transfer is a military operation and Luke gives the numbers: two hundred soldiers, seventy "
  "horsemen, two hundred spearmen, at the third hour of the night. Four hundred and seventy men "
  "to move one prisoner. Then the letter from Claudius Lysias to Felix, quoted in full, and the "
  "interesting thing about it is what it improves. Lysias writes that he rescued Paul having "
  "understood that he was a Roman, whereas chapter 22 has him discovering that afterwards, when "
  "he had already ordered him bound. An official report tidying up the officer's own conduct, "
  "reproduced without comment. Felix asks which province he is from and adjourns until the "
  "accusers arrive."),
],
"acts24": [
 ("insert", "", "The Accusation of Tertullus (vv.1-9)",
  "The prosecution opens with flattery of the governor that Luke lets run to three verses, "
  "seeing that by thee we enjoy great quietness, and then states the charge in three parts: a "
  "mover of sedition among all the Jews throughout the world, a ringleader of the sect of the "
  "Nazarenes, and one who went about to profane the temple. The first is a matter Rome would act "
  "on, the second is a description rather than a crime, and the third is the original accusation "
  "from chapter 21, which nobody has produced evidence for."),
 ("insert", "Paul's Defense", "Felix Kept Him Bound (vv.22-24)",
  "Felix defers, and Luke gives the reason for the deferral in the same sentence as the reason he "
  "was able to, having more perfect knowledge of that way. The custody arranged is unusually "
  "loose, he commanded a centurion to keep Paul, and to let him have liberty, and that he should "
  "forbid none of his acquaintance to come unto him. Then Drusilla is introduced, and Luke notes "
  "that she was a Jewess, which is why the couple send for Paul to hear him concerning the faith "
  "in Christ."),
 ("insert", "Felix Trembles", "Two Years, and Porcius Festus (vv.26-27)",
  "Two verses that explain a two-year gap, and neither reason is legal. The first is money, he "
  "hoped also that money should have been given him, and Luke states it as fact rather than "
  "rumour. The second is politics, but after two years Felix, willing to shew the Jews a "
  "pleasure, left Paul bound. A man Felix believes to be innocent stays in prison because "
  "releasing him would be inconvenient, and the sentence that records it is the last thing said "
  "about Felix."),
],
"acts25": [
 ("insert", "", "Festus and the Jewish Leaders (vv.1-10)",
  "The new governor is in the province three days before the case is raised with him, which is a "
  "measure of how much it matters to the prosecution. Their request is that Paul be brought to "
  "Jerusalem, and Luke tells the reader what Festus does not know, laying wait in the way to kill "
  "him. Festus insists on Caesarea, and the hearing produces the same result as before, they "
  "brought none accusation of such things as I supposed. Then Festus offers the transfer as a "
  "favour, wilt thou go up to Jerusalem, and there be judged? and Paul refuses it on the record, "
  "I stand at Caesar's judgment seat, where I ought to be judged."),
 ("insert", "Paul's Appeal to Caesar", "Unto Caesar Shalt Thou Go (v.12)",
  "Festus confers with his council and answers in eight words, hast thou appealed unto Caesar? "
  "unto Caesar shalt thou go. The decision removes the case from every court in Judaea and takes "
  "it to Rome, which is where Paul said in chapter 19 he must go. Nothing in the remaining "
  "chapters is a legal contest any more. It is a journey."),
],
"acts26": [
 ("insert", "", "Before Agrippa (vv.1-15)",
  "The last and fullest of the three accounts of the Damascus road, and this one is shaped for a "
  "king who knows Jewish affairs. Paul says so, I know thee to be expert in all customs and "
  "questions which are among the Jews, and grounds his whole defence in a doctrine his accusers "
  "share, I am judged for the hope of the promise made unto our fathers, and asks why that should "
  "be incredible, why should it be thought a thing incredible with you, that God should raise the "
  "dead? His own past is stated without mitigation: many of the saints did I shut up in prison, "
  "and being exceedingly mad against them, I persecuted them even unto strange cities. Only this "
  "telling includes the proverb, it is hard for thee to kick against the pricks."),
 ("insert", "Paul's Commission", "Almost Thou Persuadest Me (vv.19-28)",
  "Whereupon, O king Agrippa, I was not disobedient unto the heavenly vision. The summary of what "
  "he has been preaching is deliberately modest, none other things than those which the prophets "
  "and Moses did say should come, and it ends on the point that breaks the hearing, that Christ "
  "should suffer, and that he should be the first that should rise from the dead. Festus "
  "interrupts, Paul, thou art beside thyself, much learning doth make thee mad, and the reply is "
  "courteous and unmoved, I am not mad, most noble Festus, but speak forth the words of truth and "
  "soberness. Then he turns to the one man present who cannot plead ignorance, for this thing was "
  "not done in a corner, and puts the question directly. Agrippa's answer is the most famous "
  "sentence in the chapter, almost thou persuadest me to be a Christian."),
 ("insert", "Paul's Wish", "Nothing Worthy of Death (vv.30-32)",
  "The verdict is given in private after they leave the room, and it is unanimous, this man doeth "
  "nothing worthy of death or of bonds. Then Agrippa adds the sentence that closes the legal "
  "question and opens the last two chapters, then said Agrippa unto Festus, I might have set this "
  "man at liberty, if he had not appealed unto Caesar. Everyone with authority to release him now "
  "agrees he is innocent, and the appeal he made to save his life is what obliges them to send "
  "him to Rome."),
],
"acts27": [
 ("insert", "", "The Voyage Begins (vv.1-12)",
  "Luke is aboard, we should sail into Italy, and the account is full of the kind of detail only a "
  "passenger keeps: the centurion Julius, the courtesy of letting Paul visit friends at Sidon, "
  "sailing under Cyprus because the winds were contrary, the transfer at Myra to a ship of "
  "Alexandria. Then the argument at Fair Havens. Paul advises wintering there, because sailing is "
  "now dangerous, the fast being already past. He is overruled, and Luke records exactly who by "
  "and on what grounds: nevertheless the centurion believed the master and the owner of the ship, "
  "more than those things which were spoken by Paul. The majority preferred a better harbour."),
 ("insert", "Paul's Leadership", "Two Hundred Threescore and Sixteen Souls (vv.37-44)",
  "The number is given, and Luke gives it at the point where it matters, we were in all in the "
  "ship two hundred threescore and sixteen souls. They lighten the ship by throwing the wheat "
  "into the sea, cut the anchors, and run her aground where two seas met, and the forepart sticks "
  "fast while the stern breaks up. Then the detail that nearly undoes everything: the soldiers' "
  "counsel was to kill the prisoners, lest any of them should swim out and escape, and it is the "
  "centurion who prevents it, willing to save Paul. Some swim, some go on boards and broken "
  "pieces of the ship, and the chapter ends as it was promised it would, and so it came to pass, "
  "that they escaped all safe to land."),
],
"acts28": [
 ("retitle", "Paul in Rome", "(vv.16-29)"),
 ("insert", "Malta", "Syracuse, Rhegium, Puteoli (vv.11-15)",
  "Three months on the island, then a ship whose figurehead Luke records, whose sign was Castor "
  "and Pollux, the twin gods sailors prayed to. The last leg is given port by port, and at "
  "Puteoli they find brethren and are asked to stay seven days. Then the arrival that Luke "
  "clearly regards as the emotional end of the journey: believers walk out from Rome as far as "
  "Appii forum and the Three Taverns to meet him on the road, forty and thirty miles out. And the "
  "effect on a prisoner who has been shipwrecked, bitten and held two years without charge is "
  "given in six words, he thanked God, and took courage."),
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
