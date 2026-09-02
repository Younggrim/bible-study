#!/usr/bin/env python3
"""
Finishes 2 Kings. Seven pages, 106 verses that had no section at all.

This book's omissions have a pattern the earlier ones did not: what is missing is
consistently the Assyrian material and the aftermath. Four pages stop where the
Assyrians arrive.

  2kings18 described Hezekiah's reforms and the fall of Israel, vv.1-12, and stopped.
  Missing were vv.13-37, the whole of Sennacherib's campaign: the tribute paid by
  stripping the temple doors, the Rabshakeh at the conduit of the upper pool, and the
  speech shouted in Hebrew over the wall on purpose so the men on it would hear.
  2kings19 had Isaiah's answer and the angel, and not vv.1-19, which is Hezekiah
  going into the temple with the letter and spreading it before the LORD. The prayer
  is the reason the chapter ends the way it does.
  2kings20 had the illness and the sundial and not vv.12-21, the Babylonian envoys
  shown the treasury and Isaiah's sentence on it, which is the first mention of
  Babylon as the coming threat rather than Assyria.
  2kings16 had Ahaz's apostasy and not vv.10-20, where he copies an altar he admired
  in Damascus and has it built in Jerusalem.

The other three: 2kings4 vv.18-37, the Shunammite's son dying and being raised,
which is the longest single narrative in the Elisha cycle and had no section between
his birth and the poisoned stew. 2kings21 vv.17-26 on Amon. 2kings22 vv.1-11, Josiah
at eight years old, the repair fund handled without accounting, and the book found in
the temple, without which Huldah has nothing to prophesy about.

Usage:
    python3 finish_2kings.py [--check]
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
"2kings4": [
 ("insert", "The Shunammite's Son — Birth",
  "The Shunammite's Son: Death and Raising (vv.18-37)",
  "The boy grows, goes out to his father among the reapers, says my head, my head, and dies "
  "on his mother's knees at noon. What follows is the most closely observed sequence in the "
  "Elisha stories, and it is driven entirely by the woman. She lays the body on the prophet's "
  "own bed, tells her husband nothing except that it shall be well, rides to Carmel, and when "
  "Gehazi meets her with the polite question she answers it, It is well, and keeps going. She "
  "catches Elisha by the feet, and when he sends Gehazi ahead with the staff she refuses to "
  "leave without him, as the LORD liveth, I will not leave thee. The staff does not work: "
  "Gehazi lays it on the child and there is neither voice nor hearing. Elisha shuts the door, "
  "prays, and lies on the boy twice, mouth to mouth, eyes to eyes, hands to hands, and the "
  "flesh waxes warm. The child sneezes seven times. The prophet's method here is contact and "
  "prayer rather than word and gesture, and the woman's persistence is what got him into the "
  "room."),
],
"2kings16": [
 ("insert", "Ahaz's Apostasy",
  "The Altar Copied from Damascus (vv.10-20)",
  "Ahaz goes to Damascus to meet Tiglath-pileser, sees an altar there, and sends the pattern "
  "of it to Urijah the priest with instructions. By the time the king gets home the copy is "
  "built. What follows is a quiet, thorough displacement: Ahaz offers on the new altar, moves "
  "the brasen altar of the LORD from the front of the house round to the north side, and "
  "reserves it for himself to enquire by. Then the fittings are dismantled, the borders cut "
  "off the bases, the sea taken down from the brazen oxen and set on a stone pavement. Some "
  "of this is tribute, metal going to Assyria, and some is taste. Urijah does all of it "
  "without a recorded objection, which is the detail the writer leaves standing."),
],
"2kings18": [
 ("insert", "Hezekiah's Reforms and the Fall of Israel",
  "Sennacherib's Invasion and the Tribute (vv.13-16)",
  "In the fourteenth year of Hezekiah, Sennacherib came up against all the fenced cities of "
  "Judah and took them. Forty-six of them, by the Assyrian's own account. Hezekiah's first "
  "move is not faith but money: I have offended, return from me, that which thou puttest on "
  "me will I bear. Three hundred talents of silver and thirty of gold, and the writer records "
  "exactly where the gold came from. Hezekiah cut off the gold from the doors of the temple "
  "and from the pillars which he had himself overlaid. The king who cleansed the temple "
  "stripped it, and the tribute did not work."),
 ("insert", "Sennacherib's Invasion and the Tribute",
  "The Rabshakeh at the Wall (vv.17-37)",
  "A delegation comes up to Jerusalem and stands by the conduit of the upper pool, which is "
  "the water supply, and the speech that follows is a professional piece of work. It attacks "
  "the alliance with Egypt, that bruised reed. It attacks the reform itself, arguing that "
  "Hezekiah has taken away the LORD's high places and so offended him. It offers an "
  "unanswerable wager, two thousand horses if Judah can find riders for them. And it claims "
  "the LORD's own commission, am I now come up without the LORD against this place? When "
  "Hezekiah's officers ask him to speak Aramaic so the men on the wall will not understand, "
  "the Rabshakeh turns and shouts louder in Hebrew, and adds the offer of bread and water and "
  "a vine and a fig tree to anyone who surrenders. The list of nations whose gods failed is "
  "delivered as evidence. And the reply is silence, because the king's commandment was, Answer "
  "him not."),
],
"2kings19": [
 ("insert", "", "Hezekiah Sends to Isaiah (vv.1-7)",
  "The king tears his clothes, covers himself with sackcloth and goes into the house of the "
  "LORD, and the message he sends to Isaiah is an image rather than a request: the children "
  "are come to the birth, and there is not strength to bring forth. A labour that cannot be "
  "completed. The one hope he names is not military, it may be the LORD thy God will hear "
  "the words of Rabshakeh, and reprove them. Isaiah's answer is short and specific, be not "
  "afraid, I will send a blast upon him, and he shall return to his own land, and I will "
  "cause him to fall by the sword there."),
 ("insert", "Hezekiah Sends to Isaiah",
  "The Letter Spread Before the LORD (vv.8-19)",
  "Sennacherib withdraws to fight Libnah and sends a letter instead, and it is nastier than "
  "the speech because it goes straight at the one thing left: let not thy God in whom thou "
  "trustest deceive thee. Then the list again, Gozan, Haran, Rezeph, the children of Eden. "
  "What Hezekiah does with the letter is the centre of the chapter. He went up into the house "
  "of the LORD, and spread it before the LORD. Not read it out, spread it out, the way you "
  "would put a document in front of someone who should deal with it. The prayer that follows "
  "concedes the Assyrian's evidence rather than disputing it, of a truth, the kings of Assyria "
  "have destroyed the nations, and answers it in one clause, for they were no gods, but the "
  "work of men's hands. And the request is not survival, it is reputation: that all the "
  "kingdoms of the earth may know that thou art the LORD God, even thou only."),
],
"2kings20": [
 ("insert", "Hezekiah's Illness and Recovery",
  "The Babylonian Envoys and the Sentence (vv.12-21)",
  "Berodach-baladan of Babylon sends letters and a present, and the stated reason is that he "
  "had heard Hezekiah had been sick. Babylon was not yet the danger. Hezekiah shows them "
  "everything, all the house of his precious things, the silver, the gold, the spices, the "
  "armour, there was nothing among his treasures that he shewed them not. Isaiah's two "
  "questions are procedural and devastating: what said these men? and from whence came they? "
  "Then the sentence. All that is in thine house shall be carried into Babylon, and of thy "
  "sons shall they take away, and they shall be eunuchs in the palace of the king of Babylon. "
  "The first prophecy of the Babylonian exile is delivered a century early, over a diplomatic "
  "visit, and Hezekiah's reply is the most uncomfortable line in his story: good is the word "
  "of the LORD which thou hast spoken. Is it not good, if peace and truth be in my days? The "
  "chapter closes with the pool and the conduit he built, the one piece of his work still "
  "visible in Jerusalem."),
],
"2kings21": [
 ("insert", "God's Irreversible Judgment",
  "Amon's Two Years (vv.17-26)",
  "Manasseh is buried in the garden of his own house rather than with the kings, which the "
  "writer records without comment. Amon reigns two years and gets six verses, and the verdict "
  "is that he did as his father Manasseh did, walked in all the way that his father walked "
  "in, and served the idols that his father served. What is conspicuously absent is Manasseh's "
  "late repentance, which Chronicles records and this book does not. Amon inherited the "
  "idolatry and not the change of mind. His own servants conspire against him and kill him in "
  "his house, and the people of the land make Josiah king, a boy of eight."),
],
"2kings22": [
 ("insert", "", "Josiah, the Repairs, and the Book Found (vv.1-11)",
  "Josiah was eight years old when he began to reign, and the verdict on him has no "
  "qualification attached, he did that which was right in the sight of the LORD, and turned "
  "not aside to the right hand or to the left. In his eighteenth year he sends Shaphan to "
  "the temple with money for repairs, and the instruction includes a striking clause: there "
  "was no reckoning made with the workmen, because they dealt faithfully. The accounts were "
  "not audited because they did not need to be. Then, in the middle of ordinary building "
  "work, Hilkiah the priest says, I have found the book of the law in the house of the LORD. "
  "It is read to the king, and he rends his clothes. A nation had been running its temple for "
  "decades without the document the temple existed to serve, and it turned up during "
  "maintenance."),
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
