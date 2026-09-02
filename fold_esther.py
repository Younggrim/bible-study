#!/usr/bin/env python3
"""
Completes Esther: all ten chapters.

No Structure: sublists anywhere in this book, so the sections are written from the
text. Esther is unusually easy to divide because it is narrative built on scenes --
feasts, audiences, decrees -- and the scene breaks are the section breaks.

Four fragment-labelled fields folded into the section covering the same material:
"Esther's character emerges through the chapter:", "The timing is exquisite:", "The
chapter begins with dramatic reversals:", "The chapter records the battles:".

esther10 is three verses long and takes two sections. Padding it to the usual four
would mean inventing divisions the chapter does not have.

Usage:
    python3 fold_esther.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"esther1": 22, "esther2": 23, "esther3": 15, "esther4": 17,
          "esther5": 14, "esther6": 14, "esther7": 10, "esther8": 17,
          "esther9": 32, "esther10": 3}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Historical Context:"]

DROP = {
    "esther2": ["Esther&#x27;s character emerges through the chapter:"],
    "esther6": ["The timing is exquisite:"],
    "esther8": ["The chapter begins with dramatic reversals:"],
    "esther9": ["The chapter records the battles:"],
}

GENRE = "Historical Narrative"

THEMES = {
"esther1": "An empire displayed over 180 days, a queen who refuses a summons, "
  "advisers who turn a domestic quarrel into imperial policy, and a vacancy created "
  "without anyone intending it",
"esther2": "A search conducted across 127 provinces, a Benjaminite of Saul's line "
  "raising his orphaned cousin, a Hebrew name kept hidden behind a Persian one, and "
  "a loyalty recorded and then forgotten",
"esther3": "An old enmity revived between Amalek and the house of Saul, one man's "
  "refusal answered with a plan to kill a nation, a lot cast to choose the day, and "
  "a king who sells a people without asking who they are",
"esther4": "Public mourning in every province, a queen insulated from the crisis "
  "until told, position reframed as responsibility rather than safety, and a "
  "decision made without any guarantee",
"esther5": "Three days of fasting before one step through a door, a sceptre held "
  "out, a request deferred twice for no stated reason, and a man whose triumph is "
  "ruined by the sight of one unbowed head",
"esther6": "A king who cannot sleep, a chronicle read at random, a reward twelve "
  "years overdue, a question answered by the wrong man about himself, and an enemy "
  "made to lead the horse",
"esther7": "A petition that finally names its subject, a queen revealing she is "
  "among the condemned, a king's fury turned on his favourite, and a gallows used "
  "by the man who built it",
"esther8": "A signet ring changing hands, Persian law that cannot be repealed and "
  "must be answered instead, couriers sent on royal horses, and a city that had "
  "been perplexed now rejoicing",
"esther9": "The appointed day turned inside out, plunder authorised and three times "
  "refused, a second day requested in Susa, and a festival named after the lot that "
  "was meant to destroy them",
"esther10": "A three-verse epilogue, a reader pointed to the Persian chronicles for "
  "verification, and a book that opens with a king displaying his own glory closing "
  "with a man seeking the good of his people",
}

SECTIONS = {
"esther1": [
  ("The King's Feasts: 180 Days and Seven (vv.1-9)",
   "The book opens on scale rather than plot: Ahasuerus, generally identified with "
   "Xerxes I, ruling 127 provinces from India to Ethiopia, and a display of royal wealth "
   "lasting a hundred and eighty days followed by a seven-day feast in the palace court "
   "at Susa. The inventory of hangings, marble pillars, gold and silver couches and "
   "vessels is given in detail because the point of the chapter is what all of it is "
   "worth. Vashti holds a separate feast for the women."),
  ("Vashti Refuses to Come (vv.10-12)",
   "On the seventh day, when the king's heart was merry with wine, he sends for the "
   "queen to show her beauty to the assembled officials. She will not come. The text "
   "gives no reason -- modesty, dignity or plain defiance have all been argued -- and "
   "its silence is part of why the scene has been read so many ways. What it does record "
   "is the effect: the king was very wroth, and his anger burned in him."),
  ("Memucan's Counsel and the Irrevocable Decree (vv.13-20)",
   "Seven advisers are consulted and Memucan escalates a private embarrassment into an "
   "imperial emergency: if this becomes known, wives throughout the provinces will "
   "despise their husbands. The remedy proposed is a royal commandment that cannot be "
   "altered -- the first appearance of the Persian legal principle the whole plot will "
   "later turn on. Vashti is removed and her place given to another."),
  ("The Letters Sent to Every Province (vv.21-22)",
   "The decree goes out in every province's own script and language, which the book "
   "notes each time a decree is issued. From a human view the chapter is a drunken "
   "king's overreaction. In the shape of the book it is the first move: the vacancy now "
   "exists that Esther will fill. God is never named in Esther, and this is where the "
   "absence starts being conspicuous."),
],
"esther2": [
  ("A Search for a New Queen (vv.1-4)",
   "The king's anger cools and he remembers Vashti, possibly with regret, and his "
   "servants propose a solution: gather beautiful young virgins from every province to "
   "the house of the women at Susa. Four years separate this from chapter 1, a gap that "
   "corresponds to Xerxes's failed campaign against Greece. The proposal pleases him, "
   "which is how most decisions get made in this book."),
  ("Mordecai and Hadassah (vv.5-7)",
   "Mordecai's genealogy runs back to Kish, a Benjaminite, which places him in Saul's "
   "line -- a detail that matters once Haman is introduced as an Agagite. He had brought "
   "up his orphaned cousin Hadassah, her Hebrew name meaning myrtle, also called Esther, "
   "a Persian name possibly from star or from Ishtar. Two names for one person, one of "
   "which is not being used."),
  ("Twelve Months of Preparation (vv.8-14)",
   "The procedure is described plainly and it is not flattering: twelve months of "
   "purification, one night with the king, and then the second house of the women "
   "whether or not he ever calls again. Esther conceals her people at Mordecai's "
   "instruction. The book never comments on the morality of any of this, which is "
   "characteristic -- it reports and leaves the reader to weigh it."),
  ("Esther Made Queen (vv.15-18)",
   "Her character shows in a small detail: she asked for nothing beyond what Hegai the "
   "keeper advised, where others presumably asked for whatever they could get. She "
   "obtained favour in the sight of all that looked upon her. The crown is set on her "
   "head and a feast is proclaimed. A hidden Jew now stands at the top of the empire, "
   "and nobody in the palace knows it."),
  ("Mordecai Uncovers a Plot (vv.19-23)",
   "Sitting at the king's gate, Mordecai learns of an assassination plot by two "
   "doorkeepers and reports it through Esther in his own name. The men are hanged and "
   "the matter written in the book of the chronicles. Nothing is given to Mordecai, and "
   "the chapter ends without remarking on it. That unpaid debt sits in the record for "
   "four chapters until a sleepless king has it read aloud."),
],
"esther3": [
  ("Haman the Agagite Promoted (vv.1-2)",
   "Five years pass between Esther's coronation in the seventh year and the events of "
   "this chapter in the twelfth. Haman is promoted above all the princes and the king "
   "commands that all bow. He is called an Agagite, and Agag was king of the Amalekites "
   "-- the nation Israel was told to blot out, and the nation Saul spared, which cost "
   "him his throne. A descendant of Saul's line now faces a descendant of Agag."),
  ("Mordecai Will Not Bow (vv.3-6)",
   "Mordecai neither bows nor gives a reason, and the servants report him daily until "
   "Haman is told. When Haman learns that Mordecai is a Jew, the response skips over the "
   "man entirely: he sought to destroy all the Jews throughout the whole kingdom. The "
   "disproportion is the point of the scene, and the old national enmity explains it "
   "better than personal offence does."),
  ("The Lot Cast, the King Bought (vv.7-11)",
   "Haman casts Pur, the lot, to choose the date, and it falls on the twelfth month, "
   "Adar -- eleven months away, which is the entire reason the story has time to happen. "
   "His approach to the king is a masterpiece of omission: a certain people, scattered, "
   "with different laws, who do not keep the king's laws. He never names them. Ten "
   "thousand talents of silver are offered and the king waves the money away and hands "
   "over his ring, agreeing to a genocide without asking who is being killed."),
  ("Letters Sealed with the King's Ring (vv.12-15)",
   "The decree goes out in every language, sealed with the king's own ring, ordering "
   "the destruction of young and old, women and children, on a single day, with their "
   "goods as spoil. The last verse holds the two halves of the chapter side by side: "
   "the king and Haman sat down to drink, and the city of Susa was perplexed. The "
   "capital does not understand what has just been done in its name."),
],
"esther4": [
  ("Mordecai in Sackcloth at the Gate (vv.1-3)",
   "Mordecai tears his clothes, puts on sackcloth and ashes, and cries out publicly as "
   "far as the king's gate, which he cannot enter dressed that way. The same mourning is "
   "reported in every province where the decree arrived. This is the theological centre "
   "of the book approaching, and it opens with a man making himself impossible to "
   "ignore while remaining just outside the palace."),
  ("Esther Sends Clothes; Hathach Sends Word (vv.4-9)",
   "Esther's first response is telling: she sends clothes to replace the sackcloth, "
   "which would solve the appearance of the problem rather than the problem. She does "
   "not yet know what has happened, and the fact that the queen can be unaware of an "
   "empire-wide death sentence says something about her position. Mordecai sends back "
   "a copy of the decree itself and a charge to go in to the king."),
  ("Who Knoweth Whether Thou Art Come for Such a Time (vv.10-14)",
   "Esther raises a real obstacle: anyone approaching the king unsummoned may be put "
   "to death, and she has not been called for thirty days. Mordecai's reply is the "
   "book's most quoted passage and it has three parts, in an order worth noticing. Do "
   "not imagine you will escape. Deliverance will arise from another place regardless. "
   "And who knows whether you have come to the kingdom for such a time as this. The "
   "argument does not depend on her being indispensable."),
  ("If I Perish, I Perish (vv.15-17)",
   "Her answer reverses the direction of the relationship -- she has been receiving "
   "instructions and now gives them. Fast three days and nights, and I will go in unto "
   "the king, which is not according to the law. \u201cIf I perish, I perish\u201d is "
   "not resignation but a decision made with the outcome genuinely unknown. Mordecai "
   "does as she commands, which is the first time that sentence runs that way."),
],
"esther5": [
  ("The Golden Sceptre Held Out (vv.1-4)",
   "After three days she puts on her royal apparel and stands in the inner court. The "
   "narrative gives no interior monologue, only the action and the response: the king "
   "held out the golden sceptre, and she touched the top of it. He offers up to half "
   "the kingdom. Her answer asks for a banquet, which is not what anyone expects and "
   "not what the crisis appears to require."),
  ("A Second Banquet Tomorrow (vv.5-8)",
   "At the banquet the offer is repeated and she defers again, inviting the king and "
   "Haman to a second banquet the following day. Nothing in the text explains why. What "
   "the delay produces is the night in between, when the king cannot sleep and Mordecai's "
   "unpaid debt surfaces. Had she spoken on the first evening, chapter 6 would not have "
   "happened."),
  ("All This Availeth Me Nothing (vv.9-13)",
   "Haman leaves joyful, uniquely honoured with a private royal invitation, and then "
   "sees Mordecai at the gate still not bowing. He goes home and recites his own "
   "greatness to his household -- riches, sons, promotion, the queen's invitation -- and "
   "ends with the line that undoes all of it: yet all this availeth me nothing, so long "
   "as I see Mordecai the Jew sitting at the king's gate. One man's posture is enough to "
   "empty an empire's worth of honour."),
  ("Zeresh Suggests a Gallows (v.14)",
   "His wife and friends propose a gallows fifty cubits high and an early morning "
   "request to the king. The thing pleased Haman, and he had it made. Building it "
   "overnight, before asking permission, is the same confidence that will have him "
   "answering the king's question in chapter 6 as though it were about himself."),
],
"esther6": [
  ("The King Cannot Sleep (vv.1-3)",
   "On that night the king could not sleep. It is the smallest hinge in Scripture and "
   "the whole book turns on it. He calls for the chronicles to be read, and what is read "
   "is the record of Mordecai exposing the assassination plot -- twelve years earlier, "
   "and never rewarded. The king asks what honour was done him and is told: nothing. "
   "God is not mentioned. The coincidences are doing the work instead."),
  ("Who Is in the Court? (vv.4-6)",
   "The timing is exact. At the moment the king asks who is in the court, Haman has "
   "arrived at dawn to request Mordecai's execution. He is brought in, and instead of "
   "being asked for a request he is asked a question: what shall be done unto the man "
   "whom the king delighteth to honour? Haman assumes it is about himself, which is the "
   "only assumption available to a man in his frame of mind."),
  ("Haman Leads the Horse (vv.7-11)",
   "He proposes the most extravagant honour he can imagine -- royal apparel, the king's "
   "own horse, a crown, and a noble to lead him through the city proclaiming it. The "
   "king agrees to every detail and names the recipient. So Haman fetches the robes, "
   "puts them on Mordecai, and walks in front of the horse shouting the proclamation "
   "himself. The scene he designed for his own glory is executed against him without a "
   "word altered."),
  ("Zeresh Reverses Her Counsel (vv.12-14)",
   "Mordecai returns to the king's gate as though nothing has happened, which is its "
   "own comment. Haman hurries home mourning with his head covered, and the same wife "
   "who suggested the gallows now delivers the verdict: if Mordecai be of the seed of "
   "the Jews, thou shalt not prevail against him but shalt surely fall. Then the "
   "chamberlains arrive to take him to the banquet, and he goes from this to that."),
],
"esther7": [
  ("The Second Banquet: Let My Life Be Given Me (vv.1-4)",
   "The king asks a third time, and this time she answers. The request is framed "
   "personally before it is political: let my life be given me at my petition, and my "
   "people at my request. In one sentence she identifies herself as one of the "
   "condemned, which the king has not known through two banquets and five years of "
   "marriage. Her closing clause is commercial and precise -- the enemy could not "
   "compensate the king for the loss."),
  ("Who Is He, and Where Is He? (vv.5-6)",
   "The king's question is the reaction of a man who does not know he authorised it: "
   "who is he, and where is he, that durst presume in his heart to do so? He signed the "
   "decree himself and handed over the ring. Esther's answer is four words of substance "
   "-- the adversary and enemy is this wicked Haman -- and Haman is afraid before the "
   "king and the queen."),
  ("Haman Falls at the Queen's Feet (vv.7-8)",
   "The king goes out into the garden in his wrath, and Haman is left to beg the woman "
   "he had condemned. When the king returns Haman has fallen across her couch, and the "
   "king reads it as assault. Whether it was is beside the point by now. The chamberlains "
   "cover his face, which in Persian practice marked a man already condemned."),
  ("Fifty Cubits High (vv.9-10)",
   "Harbonah mentions, as if in passing, that Haman has built a gallows fifty cubits "
   "high for Mordecai -- the man who saved the king. The order is one word: hang him "
   "thereon. So Haman dies on the structure he raised overnight for someone else, and "
   "the king's wrath is pacified. The reversal is complete and the book does not "
   "editorialise about it."),
],
"esther8": [
  ("Haman's House and the King's Ring (vv.1-2)",
   "Haman's estate passes to Esther and Mordecai receives the signet ring taken from "
   "him -- the same ring that sealed the decree of destruction now in the hand of the "
   "man it was meant to kill. Esther tells the king what Mordecai is to her, the "
   "relationship she had concealed for years. Authority has changed hands entirely, and "
   "the legal problem is still unsolved."),
  ("Esther Pleads at His Feet (vv.3-6)",
   "She does not stop at personal victory. She falls at the king's feet weeping, and "
   "asks again -- the decree still stands and the date is still coming. Her argument is "
   "put as a question she cannot answer: how can I endure to see the destruction of my "
   "kindred? Approaching unsummoned once was the risk of chapter 5; doing it again after "
   "winning is a choice."),
  ("Write Ye Also for the Jews (vv.7-12)",
   "The king's reply states the constraint that shapes the solution: what is written in "
   "the king's name and sealed with his ring may not be reversed, not even by him. So the "
   "answer is not repeal but a second decree written alongside the first, authorising the "
   "Jews to assemble and defend their lives on the same day. The problem is solved by "
   "addition because subtraction is legally impossible."),
  ("Couriers on Royal Horses; Susa Rejoices (vv.13-17)",
   "The counter-decree is dated Sivan 23, two months and ten days after Haman's, and "
   "sent by the fastest posts on royal horses to all 127 provinces. Mordecai goes out in "
   "blue and white and purple, and the city of Susa rejoiced and was glad -- the same "
   "city described as perplexed at the end of chapter 3. The final verse notes that many "
   "people of the land became Jews, for the fear of the Jews fell upon them."),
],
"esther9": [
  ("The Thirteenth of Adar Reversed (vv.1-5)",
   "The day arrives that Haman's lot had chosen, and the verse states the inversion "
   "directly: it was turned to the contrary. The Jews gathered in their cities and no "
   "one could withstand them, because the fear of them had fallen on all people and the "
   "officials helped them on Mordecai's account. Nine months of notice had changed the "
   "balance completely without changing the date."),
  ("Five Hundred in Susa, and Haman's Ten Sons (vv.6-10)",
   "Five hundred are killed in Susa along with Haman's ten sons, who are named. The "
   "detail the text is careful about appears here for the first of three times: but on "
   "the spoil laid they not their hand. They were authorised to plunder by the terms of "
   "the decree and did not, which distinguishes what happens in this chapter from the "
   "looting the original decree had licensed against them."),
  ("A Second Day Granted (vv.11-15)",
   "The king reports the numbers to Esther and asks what more she wants. She requests a "
   "second day in Susa and that Haman's sons be hanged, which is granted. Three hundred "
   "more are killed, and again they laid not their hands on the prey. Whether the request "
   "for another day sits comfortably is a fair question, and the book raises it without "
   "answering."),
  ("Seventy-Five Thousand in the Provinces (vv.16-19)",
   "In the provinces seventy-five thousand of their enemies are killed on the thirteenth, "
   "and the third repetition of the restraint clause closes the account. The difference "
   "in dates -- the thirteenth in the provinces, the fourteenth in Susa -- is why the "
   "festival ends up covering two days, which the next section explains."),
  ("Mordecai Writes: Purim Established (vv.20-28)",
   "Mordecai writes to all the provinces establishing an annual observance on the "
   "fourteenth and fifteenth of Adar. The name comes from Pur, the lot Haman cast, so "
   "the festival is named after the instrument of the intended destruction. The "
   "prescribed observance is worth noting: feasting and gladness, sending portions to "
   "one another, and gifts to the poor. Remembrance is defined as generosity rather than "
   "ceremony."),
  ("Esther Confirms It (vv.29-32)",
   "Esther writes with Mordecai to confirm the letters, with words of peace and truth, "
   "and the decree of Esther confirmed the matters of Purim. The book ends its main "
   "action with the queen's authority set alongside his in writing. The observance is "
   "recorded as written in the book, which is where the reader is."),
],
"esther10": [
  ("The Tribute and the Chronicles (vv.1-2)",
   "The epilogue is three verses and its first act is to place the story in ordinary "
   "history: Ahasuerus laid a tribute on the empire, and the acts of his power and of "
   "Mordecai's greatness are written in the chronicles of the kings of Media and Persia. "
   "The reader is pointed to records outside the book for verification, which is an "
   "unusual move and a confident one."),
  ("Mordecai Next unto the King (v.3)",
   "The final verse describes Mordecai in four clauses: next unto king Ahasuerus, great "
   "among the Jews, accepted of the multitude of his brethren, seeking the wealth of his "
   "people and speaking peace to all his seed. Honoured by the empire and by his own "
   "people, and not resented by either. The book opened with a king spending a hundred "
   "and eighty days displaying his own glory and closes on a man seeking the good of "
   "someone else. That contrast is the last thing it says, and it says it without "
   "mentioning God once from beginning to end."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[6:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        want_drop = DROP.get(page, [])
        fields, dropped, extra = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")
        if dropped:
            notes.append(f"{page}: fragment label folded into prose")

        sections = SECTIONS[page]
        covered = set()
        for label, text in [("Key Themes", THEMES[page])] + \
                           [(f"section {h!r}", p) for h, p in sections] + \
                           [(w, fields[w]) for w in KEEP]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        parts.append(ITEM.format(label="Author:", body=fields["Author:"]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=GENRE) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=THEMES[page]) + "\n")
        parts.append(ITEM.format(label="Historical Context:",
                                 body=fields["Historical Context:"]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
