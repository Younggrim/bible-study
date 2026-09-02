#!/usr/bin/env python3
"""
Completes Leviticus: chapters 2, 3, 4 and 5, the four offerings still unfolded.

Unlike every batch so far these pages have no Structure: sublist to work from.
They carry only Author, Historical Context and one headless continuation
paragraph, so the sections are written from the text rather than inherited. The
divisions follow the chapters' own procedural breaks, which in Leviticus are
unusually clear: each offering is set out by material, then by variation, then by
the rule that governs all of them.

The headless paragraph on each page is substantive -- the pagan contrast and the
typology on chapter 2, the voluntary character of the peace offering on chapter 3,
the graduated liability on chapter 4, the restitution principle on chapter 5. Each
is appended to Historical Context, matching the reference pages which carry no
headless items. Checked first: none of the four pages has emphatic capitals, so
these merge verbatim rather than needing a rewrite as Lamentations did.

Classification and Key Themes are added; these pages had neither.

Usage:
    python3 fold_leviticus_offerings.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"leviticus2": 16, "leviticus3": 17, "leviticus4": 35, "leviticus5": 19}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV"}

KEEP = ["Author:", "Historical Context:"]

META = {
"leviticus2": ("Law \u2014 Sacrificial Instruction",
  "The one offering with no death in it, grain as the fruit of human labour given "
  "back, a memorial portion burned and the rest fed to the priests, leaven and "
  "honey excluded while salt is required, and firstfruits given before the harvest "
  "is enjoyed"),
"leviticus3": ("Law \u2014 Sacrificial Instruction",
  "The only offering the worshipper ate, a meal shared between God, priest and "
  "family, fellowship rather than atonement as the occasion, female animals "
  "permitted, and a standing rule against eating fat or blood"),
"leviticus4": ("Law \u2014 Sacrificial Instruction",
  "Atonement required for sins committed unknowingly, liability graduated by "
  "office, the priest and the congregation treated alike, blood carried inside the "
  "tent for some sins and not others, and the carcass burned outside the camp"),
"leviticus5": ("Law \u2014 Sacrificial Instruction",
  "Guilt incurred by silence and by contact as well as by act, confession required "
  "before sacrifice, the cost of the offering scaled to what the worshipper can "
  "afford, and restitution with a fifth added where a wrong has a victim"),
}

SECTIONS = {
"leviticus2": [
  ("Fine Flour, Oil, and Frankincense (vv.1-3)",
   "The grain offering is the only one of the five that involves no death. What is "
   "brought is fine flour with oil poured on it and frankincense laid on top, and "
   "the priest burns a handful as a memorial while the remainder goes to Aaron and "
   "his sons. That remainder is called \u201ca thing most holy\u201d, the highest "
   "grade of sanctity in the system, applied here to what is essentially the "
   "priests' food. The offering represents cultivated produce, so what is given back "
   "is the result of work rather than something taken from a herd."),
  ("Baked, Fried, and Griddled (vv.4-10)",
   "Three prepared forms follow, and the variety is practical rather than "
   "symbolic: cakes or wafers baked in an oven, a flat offering from the griddle, "
   "and one cooked in a pan. Each is unleavened and each uses oil, mixed in or "
   "poured over or both. The pattern in every case is identical to the uncooked "
   "form, a memorial portion burned and the rest to the priest, which keeps the "
   "differences from becoming a hierarchy of offerings."),
  ("No Leaven, No Honey, Always Salt (vv.11-13)",
   "Two exclusions and one requirement, and they belong together. Leaven and honey "
   "are both agents of fermentation, so neither goes on the altar, though they were "
   "permitted in offerings not burned. Salt is required with every grain offering "
   "and is called \u201cthe salt of the covenant of thy God\u201d. The contrast is "
   "between what changes a thing over time and what keeps it, and in the surrounding "
   "cultures grain offerings were common while these particular rules were not."),
  ("The Firstfruits Offering (vv.14-16)",
   "A seasonal variation closes the chapter: green ears of corn dried by fire and "
   "beaten out of full ears, with oil and frankincense added as before. What makes "
   "it distinct is timing rather than substance. The first of a harvest is handed "
   "over before any of it has been enjoyed, which asks for confidence that the rest "
   "will come."),
],
"leviticus3": [
  ("The Peace Offering from the Herd (vv.1-5)",
   "The peace offering takes its name from shelamim, from the same root as shalom, "
   "and the occasion is wholeness rather than guilt. The animal may be male or "
   "female, which the burnt offering does not allow, and the difference reflects "
   "that this is not an atoning sacrifice. The worshipper lays a hand on its head, "
   "the blood is sprinkled around the altar, and what is burned is the fat, the "
   "kidneys and the caul \u2014 the richest parts rather than the whole."),
  ("From the Flock: A Lamb (vv.6-11)",
   "The same procedure is set out for a lamb, with the whole rump included in what "
   "is burned. Verse 11 calls the portion on the altar \u201cthe food of the "
   "offering\u201d, language of God being fed that the Old Testament elsewhere goes "
   "out of its way to qualify. Here it stands without embarrassment, because the "
   "occasion is a shared meal and the point is that God is a participant in it."),
  ("From the Flock: A Goat (vv.12-16)",
   "A third option, handled identically, and the repetition is the point: the rite "
   "does not change with the means of the worshipper. Verse 16 states the principle "
   "the chapter has been building \u2014 \u201call the fat is the LORD's\u201d. The "
   "best of the animal goes to God, the breast and right shoulder to the priest, and "
   "the rest to the worshipper and his household, so the same animal feeds all three."),
  ("A Perpetual Statute: Neither Fat Nor Blood (v.17)",
   "One verse closes the chapter and it is binding beyond the sanctuary: eat neither "
   "fat nor blood, in all your dwellings, as a perpetual statute. The fat is "
   "withheld because it belongs to God and the blood because life is in it, a "
   "reason chapter 17 will state outright. A rule about worship becomes a rule about "
   "dinner."),
],
"leviticus4": [
  ("Sins Done in Ignorance (vv.1-2)",
   "The chapter opens by defining what it covers: sin committed \u201cthrough "
   "ignorance\u201d against any of the commandments. The premise is that not knowing "
   "does not settle the matter, and that guilt can be incurred without intent. "
   "Everything that follows assumes the offender comes forward once the sin becomes "
   "known to him, so the system depends on people reporting themselves."),
  ("When the Anointed Priest Sins (vv.3-12)",
   "The most elaborate rite in the chapter belongs to the priest, and the reason "
   "given is consequence: his sin brings guilt on the people. The blood is carried "
   "inside the tent, sprinkled seven times before the veil and put on the horns of "
   "the incense altar, which no other case in this chapter requires. The carcass is "
   "then taken outside the camp and burned. Hebrews 13:11-12 draws on that last "
   "detail directly."),
  ("When the Whole Congregation Sins (vv.13-21)",
   "Corporate sin is treated with the same procedure as the priest's, blood inside "
   "the tent and the carcass burned outside. The elders lay their hands on the head "
   "of the bullock on the assembly's behalf. That a community can sin in ignorance "
   "as a body, and needs atonement as a body, is stated without argument, and the "
   "equivalence with the priest's case says something about how much either "
   "mattered."),
  ("When a Ruler Sins (vv.22-26)",
   "The rite simplifies. A male goat is brought, and the blood goes on the horns of "
   "the altar of burnt offering in the courtyard rather than being carried inside. "
   "The priest eats his portion, which he could not do where the blood went into the "
   "tent. The offering is real but the reach of the sin is smaller, and the ritual "
   "reflects the difference rather than flattening it."),
  ("When One of the Common People Sins (vv.27-35)",
   "The last case allows a female goat or a female lamb, and the procedure matches "
   "the ruler's. Reading the four cases together, the pattern is plain: the higher "
   "the office the costlier the sacrifice and the further the blood travels. What "
   "does not vary is that each case ends the same way, with atonement made and the "
   "sin forgiven."),
],
"leviticus5": [
  ("Sins of Silence, Contact, and Rash Oaths (vv.1-6)",
   "The chapter opens with three cases that are not obviously acts at all. A man "
   "who hears an adjuration and does not testify bears his iniquity, so keeping "
   "quiet is the offence. Touching what is unclean incurs guilt without any "
   "intention. So does swearing thoughtlessly, whether to do good or evil. Verse 5 "
   "adds a step the earlier chapters did not require: he shall confess, and only "
   "then bring the offering."),
  ("If He Cannot Afford a Lamb (vv.7-13)",
   "Two provisions scale the cost down. A worshipper who cannot bring a lamb brings "
   "two turtledoves or two young pigeons, and one who cannot afford birds brings "
   "fine flour \u2014 without oil or frankincense, since this is a sin offering and "
   "not a gift. The atonement is described in exactly the same terms in every case. "
   "The offering's value varies and its effect does not, which is the most "
   "practically merciful arrangement in the sacrificial code."),
  ("The Trespass Offering: Restitution with a Fifth Added (vv.14-16)",
   "The guilt offering, asham, introduces something absent from the others: paying "
   "the wrong back. A ram is brought, and alongside it the offender restores what "
   "he took and adds a fifth of its value. Sacrifice alone does not settle a debt "
   "that has a victim. Isaiah 53:10 uses this same word for the servant's offering, "
   "which is the one place the Old Testament applies the term to a person."),
  ("Guilt Without Knowing It (vv.17-19)",
   "The chapter closes on the hardest case: a man who sins and \u201cwist it "
   "not\u201d is still guilty and still bears his iniquity. No mechanism is offered "
   "for discovering such a sin, and the offering is prescribed for when he does. "
   "Read alongside chapter 4, the effect is to remove ignorance as a defence "
   "entirely while providing a remedy in every instance where it applies."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        fields, extra = {}, []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields.get("Historical Context:", "")] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged into "
                         f"Historical Context")

        genre, themes = META[page]
        sections = SECTIONS[page]

        covered = set()
        for label, body in [("Key Themes", themes)] + \
                           [(f"section {h!r}", p) for h, p in sections]:
            stray = sorted({w for w in CAPS.findall(body) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: emphatic capitals {stray} in {label}")
            if "*" in body:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
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
        for want in KEEP:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=genre) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=themes) + "\n")
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
