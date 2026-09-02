#!/usr/bin/env python3
"""
Finishes 1 Samuel. Ten pages, 91 verses.

Two of these are the same failure John showed: a page keeps the memorable ending and
loses the event that caused it.

  1samuel4 had 'Eli's Death and Ichabod (vv.12-22)' and nothing for vv.1-11, which is
  the battle itself, the decision to fetch the ark as a talisman, the shout in the
  camp, thirty thousand dead, and the ark captured. The chapter's ending was described
  and its cause was not.
  1samuel7 had the victory at Ebenezer and Samuel's judgeship, and nothing for
  vv.1-9: twenty years of the ark at Kirjath-jearim, the call to put away strange
  gods, the water poured out at Mizpeh, and the lamb offered while the Philistines
  were already moving.

1samuel14 lost the largest single block, vv.25-46: the honey in the wood, Jonathan
eating it without knowing about his father's oath, the people falling on the spoil
and eating with the blood, and the lot cast that lands on Jonathan and is overruled
by the army. Twenty-two verses, and it is the passage that shows what Saul's oath
cost.

The rest: 1samuel6 vv.17-21 the golden emerods listed by city and the men struck at
Beth-shemesh, 1samuel9 vv.11-14 the maidens at the well, 1samuel10 vv.9-16 Saul among
the prophets and the proverb it produced, 1samuel11 vv.12-15 Saul refusing to execute
the men who had despised him, 1samuel12 vv.16-25 thunder in wheat harvest and the
charge that follows it, 1samuel13 vv.1-7 the garrison smitten and the people hiding in
caves, 1samuel23 vv.19-29 the Ziphites and the rock of divisions.

Usage:
    python3 finish_1samuel.py [--check]
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
"1samuel4": [
 ("", "The Ark Taken at Aphek (vv.1-11)",
  "Israel is beaten once, four thousand men, and the elders ask the right question, "
  "wherefore hath the LORD smitten us today? Their answer is the wrong one: let us fetch the "
  "ark of the covenant of the LORD out of Shiloh unto us, that it may save us. The ark is "
  "treated as equipment. Hophni and Phinehas come with it, which is the writer's way of "
  "noting who is in charge of it. The shout is loud enough that the Philistines hear it and "
  "are afraid, and their reasoning is more theologically alert than Israel's, these are the "
  "Gods that smote the Egyptians. So they fight harder. Thirty thousand footmen fall, the ark "
  "is taken, and Eli's two sons are dead in the same verse. The object brought to guarantee "
  "victory is carried off as plunder."),
],
"1samuel6": [
 ("The Ark's Return to Beth-shemesh",
  "Five Golden Emerods, and the Men Struck (vv.17-21)",
  "The guilt offering is itemised, five golden emerods and five golden mice, one for each "
  "Philistine city, and the cities are named: Ashdod, Gaza, Askelon, Gath, Ekron. Then the "
  "chapter turns on Israel rather than the Philistines. God smote the men of Beth-shemesh, "
  "because they had looked into the ark, and the response is not gratitude but dread: who is "
  "able to stand before this holy LORD God? and to whom shall he go up from us? A town that "
  "rejoiced at the ark's arrival in verse 13 sends messengers to get rid of it by verse 21. "
  "The narrative has just shown the ark to be no talisman in Philistine hands and no charm in "
  "Israelite ones."),
],
"1samuel7": [
 ("", "Twenty Years, and the Gathering at Mizpeh (vv.1-9)",
  "The ark goes to Kirjath-jearim and stays there, and the summary of the period is one of the "
  "saddest sentences in the book: the time was long, for it was twenty years, and all the "
  "house of Israel lamented after the LORD. Then Samuel sets a condition rather than leading "
  "a rally, if ye do return unto the LORD with all your hearts, then put away the strange "
  "gods and Ashtaroth from among you, and prepare your hearts unto the LORD, and serve him "
  "only. They do it, and gather at Mizpeh, where they draw water and pour it out before the "
  "LORD and fast. The Philistines hear of the assembly and come up, so the repentance is "
  "tested before it is rewarded, and Samuel's response is a suckling lamb offered whole and a "
  "cry to the LORD while the army is on its way."),
],
"1samuel9": [
 ("The Search for Lost Donkeys", "The Maidens at the Well (vv.11-14)",
  "Four verses of directions, and they are the kind of detail that only survives in an account "
  "somebody remembered. Saul and his servant meet young maidens going out to draw water and "
  "ask whether the seer is there. The answer is a rush of instruction: he is, go quickly, he "
  "came today to the city, for there is a sacrifice today, as soon as ye be come into the city "
  "ye shall straightway find him before he go up to the high place, for the people will not eat "
  "till he come. The future king of Israel is given walking directions by girls at a well, and "
  "he takes them."),
],
"1samuel10": [
 ("Samuel Anoints Saul Privately", "Saul Among the Prophets (vv.9-16)",
  "God gave him another heart, and all the signs came to pass that day. The last of them is "
  "the company of prophets with psaltery and tabret and pipe and harp, and the Spirit of God "
  "came upon him, and he prophesied among them. The reaction of the people who knew him is not "
  "reverence but bewilderment, and it hardens into a saying, is Saul also among the prophets? "
  "which the book will quote again later in a worse setting. Then the detail that says most "
  "about the man: his uncle asks what Samuel said, and Saul tells him about the donkeys and, "
  "of the matter of the kingdom, he told him not. He has been anointed king and says nothing "
  "about it to his own family."),
],
"1samuel11": [
 ("Victory Over the Ammonites", "Not a Man Shall Be Put to Death (vv.12-15)",
  "The victory produces a demand for a purge. The people come to Samuel and ask for the men "
  "who had said, shall Saul reign over us? bring the men, that we may put them to death. "
  "Saul's answer is the best thing he does in the book: there shall not a man be put to death "
  "this day, for today the LORD hath wrought salvation in Israel. He refuses to use a military "
  "success to settle a political score. So the kingdom is renewed at Gilgal with peace "
  "offerings, and Saul and all the men of Israel rejoiced greatly, which is the last time that "
  "clause appears about him."),
],
"1samuel12": [
 ("Conditions for the Monarchy", "Thunder in Wheat Harvest (vv.16-19)",
  "Samuel asks for a sign and names the season, is it not wheat harvest? which in that climate "
  "is the dry months when rain does not fall. I will call unto the LORD, and he shall send "
  "thunder and rain, that ye may perceive your wickedness in asking you a king. The sign is a "
  "weather event chosen because it cannot be mistaken for coincidence. The people's reaction is "
  "immediate and complete, all the people greatly feared the LORD and Samuel, and they ask him "
  "to pray for them, adding to all our sins this evil, to ask us a king."),
 ("Thunder in Wheat Harvest", "Fear Not, Only Serve the LORD (vv.20-25)",
  "The answer to their fear is not reassurance that the sin was small but an instruction about "
  "what to do next: fear not, ye have done all this wickedness, yet turn not aside from "
  "following the LORD. The ground of hope offered is God's own reputation, the LORD will not "
  "forsake his people for his great name's sake, because it hath pleased the LORD to make you "
  "his people. Then Samuel says something about his own office that reframes prophecy as duty: "
  "God forbid that I should sin against the LORD in ceasing to pray for you. The chapter ends "
  "with both possibilities still open, if ye shall still do wickedly, ye shall be consumed, "
  "both ye and your king."),
],
"1samuel13": [
 ("", "The Garrison Smitten and the People Hiding (vv.1-7)",
  "Jonathan smites the Philistine garrison at Geba, and Saul blows the trumpet and takes the "
  "credit in the same breath, Saul hath smitten a garrison of the Philistines. The Philistine "
  "response is overwhelming and the numbers are given to make that point: chariots and "
  "horsemen and people as the sand on the sea shore. What follows is a description of a nation "
  "dissolving rather than fighting. The people did hide themselves in caves, and in thickets, "
  "and in rocks, and in high places, and in pits, and some went over Jordan altogether. The "
  "men that followed Saul were trembling. This is the situation Saul is standing in when he "
  "decides not to wait for Samuel."),
],
"1samuel14": [
 ("Saul's Response and Foolish Oath", "The Honey in the Wood (vv.25-30)",
  "There was honey upon the ground and the people would not touch it, for the people feared "
  "the oath. Jonathan, who was not there when it was made, puts the end of his rod in the "
  "honeycomb and eats, and his eyes were enlightened. When he is told, his verdict on his "
  "father is public and blunt: my father hath troubled the land, see how mine eyes have been "
  "enlightened, because I tasted a little of this honey. Then the military argument, how much "
  "more if the people had eaten freely today of the spoil, had there not been now a much "
  "greater slaughter? The oath cost the victory it was meant to secure."),
 ("The Honey in the Wood", "Eating with the Blood (vv.31-35)",
  "The men are faint, so when the fighting stops they fall on the spoil and kill sheep and oxen "
  "and calves on the ground and eat them with the blood, which the law forbids twice over. "
  "Saul is told, and calls it transgression, and his remedy is practical: roll a great stone "
  "unto me, slay them here, and eat. Then the verse the writer places carefully, and Saul "
  "built an altar unto the LORD, the same was the first altar that he built. His first altar "
  "comes after a rash oath and a mass violation his own oath produced."),
 ("Eating with the Blood", "The Lot Falls on Jonathan (vv.36-46)",
  "Saul proposes a night pursuit and the priest suggests asking God first, and God does not "
  "answer. Saul's response to silence is to hunt for the sin by lot, with an oath attached, "
  "though it be in Jonathan my son, he shall surely die. The lot narrows to Saul and Jonathan, "
  "then to Jonathan, and Jonathan admits it in a sentence that concedes nothing, I did but "
  "taste a little honey with the end of the rod that was in mine hand, and, lo, I must die. "
  "Then the army overrules the king: shall Jonathan die, who hath wrought this great salvation "
  "in Israel? God forbid, as the LORD liveth, there shall not one hair of his head fall to the "
  "ground. So the people rescued Jonathan, and he died not. Saul goes home, and the pursuit is "
  "abandoned."),
],
"1samuel23": [
 ("Jonathan Strengthens David", "The Ziphites Betray Him (vv.19-24)",
  "The Ziphites go up to Saul at Gibeah and offer him David, and the offer is unprompted, doth "
  "not David hide himself with us in the strong holds in the wood? Saul's reply is a blessing, "
  "blessed be ye of the LORD, for ye have compassion on me, and it is the only time in the "
  "chapter anyone speaks of the LORD approvingly. He asks them to go back and confirm the "
  "place exactly, see his place where his haunt is, and who hath seen him there. Twice in this "
  "chapter David is handed over by the people he has been protecting."),
 ("The Ziphites Betray Him", "The Rock of Divisions (vv.25-29)",
  "The pursuit closes to within a hill. Saul went on this side of the mountain, and David and "
  "his men on that side of the mountain, and David made haste to get away, for Saul and his "
  "men compassed David round about to take them. It is the nearest Saul comes to catching him. "
  "What breaks it off is a message that has nothing to do with either of them: haste thee, and "
  "come, for the Philistines have invaded the land. So Saul turns aside, and the place is given "
  "a name that keeps the moment, Sela-hammahlekoth, the rock of divisions. David goes up to the "
  "strong holds at En-gedi, where the next chapter happens."),
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
