#!/usr/bin/env python3
"""
Finishes Exodus, Ephesians, Galatians and Hebrews, and resolves the three overlaps
that rejoining the colon-split labels created.

The overlaps are worth naming because they are a consequence of an earlier repair
rather than an inherited fault. Rejoining a stranded heading restores a section
that the audit could not previously see, and in three places something else had
already been made to cover those verses:

  deuteronomy14 ended up with two sections for vv.1-2, the restored
  "Israel's Identity: Holy People" and the one written for it in the previous pass.
  The written prose is folded into the restored heading and the duplicate removed.
  genesis5's death refrain had been narrowed to vv.1-27 to make room for Noah's
  birth at vv.28-32, which left it sitting over Enoch at vv.21-24 once that section
  reappeared. It is now vv.1-20 and vv.25-27.
  leviticus23's summary statement covers vv.37-38 and v.44, which falls inside
  Tabernacles at vv.33-43. That is how the chapter reads, a summary interrupting the
  last feast, so Tabernacles becomes vv.33-36 and vv.39-43. Its opening two verses
  had no section at all.

The book completions:

  exodus20 was missing vv.3-17, which is the Ten Commandments. The page had a
  preamble, the people's reaction and the altar instructions, and nothing for the
  commandments themselves. They are written as the two tables.
  galatians2 vv.15-21 is 'I am crucified with Christ', galatians3 vv.10-18 the
  curse and the promise and vv.26-29 'neither Jew nor Greek', galatians4 vv.8-20
  Paul's appeal to his own reception among them. Three of the letter's best-known
  passages were undescribed.
  ephesians6 vv.21-24 and hebrews13 vv.18-19 and vv.22-25 are closings again,
  Tychicus carrying the letter, and the only place in Hebrews where the author
  asks for anything.

Usage:
    python3 finish_four_more_books.py [--check]
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
"deuteronomy14": [
 ("merge", "Sons of the LORD, a Holy People", "Israel's Identity"),
],
# Two pages the rejoin made legible enough for the audit to see a small gap in.
"1kings3": [
 ("extend", "God's Offer and Solomon's Request", "(vv.5-15)",
  "Then Solomon awoke, and behold, it was a dream. The chapter says so plainly, and then "
  "records what he did about it: came to Jerusalem, stood before the ark, offered burnt "
  "offerings and peace offerings, and made a feast to all his servants. A dream is answered "
  "with public sacrifice and a party, which is how the request becomes a matter of record "
  "rather than a private experience."),
],
"judges12": [
 ("insert", "", "Ephraim's Complaint (vv.1-3)",
  "The men of Ephraim gather and cross over to Jephthah with a grievance and a threat in the "
  "same breath: wherefore wentest thou to fight against the children of Ammon, and didst not "
  "call us? we will burn thine house upon thee with fire. Jephthah's answer is that he did "
  "call and they did not come, I called you, and ye delivered me not out of their hands. "
  "Whether that is true the book does not say. What it does say is that the tribe most "
  "concerned with being consulted arrives after the fighting is over."),
],
"genesis5": [
 ("retitle", "The Refrain of Death", "(vv.1-20,25-27)"),
],
"leviticus23": [
 ("retitle", "Feast 7", "(vv.33-36,39-43)"),
 ("insert", "", "These Are the Feasts of the LORD (vv.1-2)",
  "The chapter opens by naming what it is about to list, the feasts of the LORD, which ye "
  "shall proclaim to be holy convocations. Two words in that phrase carry the weight. They "
  "are the LORD's feasts rather than Israel's, and they are convocations, meetings called "
  "rather than festivals kept, which is why the calendar that follows is legislation and "
  "not custom."),
],
"exodus20": [
 ("insert", "The Preamble",
  "The First Table: Duties Toward God (vv.3-11)",
  "Four commandments, and each one closes a door the surrounding nations left open. Thou "
  "shalt have no other gods before me, which rules out addition rather than substitution, "
  "the ordinary religious instinct being to keep the old god and add a new one. Then no "
  "graven image, with the reason given as jealousy and the reach of consequence stated in "
  "both directions, visiting iniquity to the third and fourth generation and showing mercy "
  "unto thousands. Then the name, thou shalt not take the name of the LORD thy God in vain, "
  "which is about the misuse of a thing already granted. Then the Sabbath, the longest of "
  "the ten, and it is grounded not in Israel's history but in creation, for in six days the "
  "LORD made heaven and earth, and rested the seventh day. The rest is extended to the son, "
  "the daughter, the servant, the cattle and the stranger within thy gates, so the "
  "commandment protects everyone who cannot stop working on their own authority."),
 ("insert", "The First Table: Duties Toward God",
  "The Second Table: Duties Toward Neighbor (vv.12-17)",
  "Six commandments, and the first of them carries the only promise attached to any: honour "
  "thy father and thy mother, that thy days may be long upon the land. Then four "
  "prohibitions of two or three words each, the shortest sentences in the law. Thou shalt "
  "not kill, thou shalt not commit adultery, thou shalt not steal, thou shalt not bear false "
  "witness. Life, marriage, property, reputation, and the brevity is the point, no case law, "
  "no qualification, nothing to argue with. Then the tenth breaks the pattern by naming an "
  "interior act, thou shalt not covet, and then lists what may not be coveted, house, wife, "
  "servant, ox, ass. No court can try it, which is why Paul says in Romans 7 that this was "
  "the commandment that found him out."),
],
"ephesians6": [
 ("insert", "The Armor of God", "Tychicus and the Final Blessing (vv.21-24)",
  "Tychicus, a beloved brother and faithful minister in the Lord, shall make known to you "
  "all things. The letter has spent six chapters on the church as a body and a building and "
  "an army, and it is carried to them by a man whose job is to fill in what the letter does "
  "not say. Then the blessing, and it is unusual in Paul for being in the third person "
  "throughout, peace be to the brethren, and love with faith, from God the Father and the "
  "Lord Jesus Christ. It ends with grace be with all them that love our Lord Jesus Christ "
  "in sincerity, which names its recipients by their affection rather than their address."),
],
"hebrews13": [
 ("insert", "Sacrifices That Please God", "Pray for Us (vv.18-19)",
  "Pray for us, for we trust we have a good conscience, in all things willing to live "
  "honestly. It is the only request the author makes for himself in the whole letter, and "
  "the reason given is oddly specific, that I may be restored to you the sooner. Whoever "
  "wrote Hebrews was separated from these readers and wanted to be back with them, which is "
  "the closest the book comes to telling us anything about its author's circumstances."),
 ("insert", "The Benediction", "Bear With My Letter (vv.22-25)",
  "Suffer the word of exhortation, for I have written a letter unto you in few words. "
  "Thirteen chapters described as few words, which suggests the author knew how much he had "
  "left out rather than how much he had said. Timothy is named, which is the letter's one "
  "link to the Pauline circle and the reason for centuries of argument about who held the "
  "pen. They of Italy salute you, a greeting that could mean written from Italy or written "
  "to it and has been read both ways. Grace be with you all."),
],
"galatians2": [
 ("insert", "The Antioch Incident", "I Am Crucified With Christ (vv.15-21)",
  "The argument moves from what happened at Antioch to why it mattered, and the pronoun "
  "stays at we: we who are Jews by nature know that a man is not justified by the works of "
  "the law, but by the faith of Jesus Christ. Then the objection Paul expects, that this "
  "makes Christ the minister of sin, and the answer that rebuilding what you tore down is "
  "what makes a man a transgressor. Then the sentence the letter is remembered for, and it "
  "is autobiography rather than doctrine: I am crucified with Christ, nevertheless I live, "
  "yet not I, but Christ liveth in me. The chapter closes by putting the whole controversy "
  "on one point, if righteousness come by the law, then Christ is dead in vain."),
],
"galatians3": [
 ("insert", "The Argument from Abraham",
  "The Curse and the Promise (vv.10-18)",
  "Two verdicts are set against each other and both are quoted from the law itself. Cursed "
  "is every one that continueth not in all things which are written in the book of the law, "
  "and the just shall live by faith. Then the exchange, Christ hath redeemed us from the "
  "curse of the law, being made a curse for us, with Deuteronomy's line about a man hanged "
  "on a tree applied to the cross. The second half turns on a legal point about documents: a "
  "covenant confirmed cannot be annulled or added to afterwards, and the promise to Abraham "
  "came four hundred and thirty years before the law, so the law cannot have replaced it. "
  "Paul also presses the singular, he saith not, And to seeds, as of many, but as of one."),
 ("insert", "The Argument from the Law's Purpose",
  "Neither Jew Nor Greek (vv.26-29)",
  "For ye are all the children of God by faith in Christ Jesus. Then the three pairs, and "
  "each names a division that organised the ancient world: there is neither Jew nor Greek, "
  "there is neither bond nor free, there is neither male nor female. Paul is not saying the "
  "distinctions vanish, he is saying they no longer determine standing, which is precisely "
  "what the circumcision party was arguing they did. The conclusion returns to Abraham and "
  "closes the chapter's whole argument, if ye be Christ's, then are ye Abraham's seed, and "
  "heirs according to the promise."),
],
"galatians4": [
 ("insert", "Sons, Not Slaves", "How Turn Ye Again (vv.8-20)",
  "The tone changes here from argument to appeal, and it is the most personal passage in the "
  "letter. Paul asks how people who once served nothing that was a god can turn again to the "
  "weak and beggarly elements, and names what he sees, ye observe days, and months, and "
  "times, and years. Then the memory, and it comes with an admission about his own state: he "
  "first preached to them through infirmity of the flesh, and they did not despise him for "
  "it but received him as an angel of God, and would have plucked out their own eyes and "
  "given them to him. Where is then the blessedness ye spake of? He asks whether telling "
  "them the truth has made him their enemy, calls them my little children, and says he "
  "travails in birth again until Christ be formed in them. Then the frankest line in the "
  "letter, I desire to be present with you now, and to change my voice, for I stand in doubt "
  "of you. He is saying that a letter is the wrong instrument for this."),
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
            kind = op[0]
            if kind == "retitle":
                _, prefix, rng = op
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
            elif kind == "extend":
                _, prefix, rng, prose = op
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: extend target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                items[i][1] += " " + prose
                notes.append(f"{page}: extended {prefix!r} to {rng}")
            elif kind == "insert":
                _, after, label, prose = op
                at = first_section(items) if after == "" else find(items, after) + 1
                if after and at == 0:
                    problems.append(f"{page}: insert anchor {after!r} not found")
                    continue
                items.insert(at, [label + ":", prose])
                notes.append(f"{page}: inserted {label!r}")
            elif kind == "merge":
                _, nested, parent = op
                i, j = find(items, nested), find(items, parent)
                if i < 0 or j < 0:
                    problems.append(f"{page}: merge {nested!r} into {parent!r} not found")
                    continue
                items[j][1] += " " + items[i][1]
                del items[i]
                notes.append(f"{page}: merged {nested!r} into {parent!r}")
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
