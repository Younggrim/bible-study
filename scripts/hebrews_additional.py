#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Hebrews."""
import os

def add_additional_notes(filepath, notes_text):
    with open(filepath, 'r') as f:
        content = f.read()
    if 'ADDITIONAL TRANSLATION NOTES' in content:
        return False
    if 'GLOSSARY' in content:
        insertion_point = 'GLOSSARY'
    elif 'PERSONAL REFLECTION' in content:
        insertion_point = 'PERSONAL REFLECTION'
    else:
        return False
    block = "ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)\n------------------------------------\n" + notes_text.strip() + "\n\n"
    content = content.replace(insertion_point, block + insertion_point)
    with open(filepath, 'w') as f:
        f.write(content)
    return True

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/19 - Hebrews"
notes = dict()

notes[1] = """v.1  — NET: "God spoke to our ancestors through the prophets
       at many times and in various ways" — "at many times and in
       various ways" (polymerOs kai polytropOs). WEB: "at many
       times and in many ways." KJV: "at sundry times and in divers
       manners." The revelation was fragmentary; now in the Son it
       is complete and final.

v.2  — NET: "whom he appointed heir of all things, and through
       whom he created the world" — "the world" (tous aiOnas = the
       ages/eons — time and space). WEB: "through whom also he made
       the worlds." KJV: "by whom also he made the worlds." Christ
       made not just matter but time itself.

v.3  — NET: "He is the radiance of his glory and the
       representation of his essence" — "radiance" (apaugasma =
       effulgence/shining forth). "Representation" (charaktEr =
       exact imprint/stamp). WEB: "the very image of his substance."
       KJV: "the express image of his person." Two metaphors:
       light radiating and a die striking a coin.

v.3  — NET: "sustaining all things by his powerful word" —
       "sustaining" (pherOn = carrying/bearing/maintaining). WEB:
       "upholding all things by the word of his power." KJV:
       "upholding all things." Not static support but active,
       purposeful carrying toward a destination.

v.14 — NET: "Are they not all ministering spirits, sent to serve
       those who will inherit salvation?" — "ministering spirits"
       (leitourgika pneumata = liturgical/servant spirits). WEB:
       "serving spirits." Angels exist to serve believers — not
       the other way around."""

notes[2] = """v.1  — NET: "we must pay closer attention to what we have
       heard, so that we do not drift away" — "drift away"
       (pararruOmen = slip past/flow by like a river current). WEB:
       "lest perhaps we drift away." KJV: "lest at any time we
       should let them slip." Passive, imperceptible movement —
       drifting requires no effort.

v.9  — NET: "we see Jesus, who was made lower than the angels for
       a little while, now crowned with glory and honor because he
       suffered death" — "for a little while" (brachy ti = briefly/
       for a short time). WEB: "for a little while." The incarnation
       was temporary humiliation followed by permanent exaltation.

v.10 — NET: "to make the pioneer of their salvation perfect
       through sufferings" — "pioneer" (archEgon = author/leader/
       trailblazer). WEB: "the author of their salvation." KJV:
       "the captain of their salvation." Jesus blazes the trail
       of salvation through suffering — we follow His path.

v.14 — NET: "he himself shared in their humanity, so that through
       death he could destroy the one who holds the power of death"
       — "destroy" (katargEsE = render powerless/nullify). WEB:
       "bring to nothing him who had the power of death." KJV:
       "destroy him that had the power of death." Not annihilate
       but disarm — Satan's death-weapon is broken.

v.18 — NET: "he is able to help those who are tempted" — "help"
       (boEthEsai = run to the aid of/come to rescue). WEB: "able
       to help those who are tempted." A word of urgency — He
       RUNS to help. His own suffering qualifies Him as helper."""

notes[3] = """v.1  — NET: "think carefully about Jesus, the apostle and high
       priest whom we confess" — "apostle" (apostolon) — the only
       place Jesus is called "apostle" (sent one). WEB: "the
       Apostle and High Priest of our confession." He is both SENT
       by God (apostle) and represents us TO God (high priest).

v.7  — NET: "Today, if you hear his voice, do not harden your
       hearts" — quoting Psalm 95:7-8. "Today" (sEmeron) — the
       urgency of present response. WEB: "Today if you will hear
       his voice." KJV: "To day if ye will hear his voice." Quoted
       three times in Hebrews (3:7, 3:15, 4:7) — repeated warning.

v.12 — NET: "See to it, brothers and sisters, that none of you
       has an evil, unbelieving heart that forsakes the living God"
       — "forsakes" (apostEnai = apostatize/stand away from). WEB:
       "departing from the living God." KJV: "departing from the
       living God." Apostasy begins with an unbelieving heart, not
       intellectual doubt.

v.13 — NET: "exhort one another each day, as long as it is called
       'Today'" — "exhort" (parakaleite = encourage/urge alongside).
       WEB: "exhort one another day by day." Daily mutual
       encouragement as the antidote to hard hearts — community
       prevents apostasy.

v.19 — NET: "they were unable to enter because of unbelief" —
       "unbelief" (apistian = lack of faith/faithlessness). WEB:
       "because of unbelief." KJV: "because of unbelief." The
       wilderness generation's ultimate failure diagnosis — not
       weakness but unbelief. The same danger faces new covenant
       people."""

notes[4] = """v.9  — NET: "a Sabbath rest remains for the people of God" —
       "Sabbath rest" (sabbatismos = a keeping of Sabbath — unique
       word in the NT). WEB: "a Sabbath rest for the people of
       God." Not just any rest but a SABBATH rest — cessation from
       self-effort in salvation.

v.12 — NET: "For the word of God is living and active and sharper
       than any double-edged sword" — "living and active" (zOn kai
       energEs = alive and at work). WEB: "living and active." KJV:
       "quick, and powerful." God's word is not inert text but
       operative, penetrating force.

v.12 — NET: "penetrating even to the point of dividing soul from
       spirit" — "dividing" (merismos = separation/distribution).
       WEB: "piercing even to the dividing of soul and spirit."
       The word discerns what we cannot — our own deepest motives.

v.15 — NET: "we do not have a high priest incapable of sympathizing
       with our weaknesses" — "sympathizing" (sympathEsai = suffer
       with/feel together). WEB: "one who can't be touched with the
       feeling of our infirmities." KJV: "cannot be touched with
       the feeling of our infirmities." Jesus doesn't observe our
       pain — He FEELS it.

v.16 — NET: "let us confidently approach the throne of grace to
       receive mercy and find grace whenever we need help" —
       "confidently" (meta parrEsias = with boldness/freedom of
       speech). WEB: "with boldness." KJV: "boldly." We approach
       not cautiously but freely — the throne is GRACE, not judgment."""

notes[5] = """v.7  — NET: "During his earthly life Christ offered both
       requests and supplications, with loud cries and tears" —
       "loud cries and tears" (meta kraugEs ischyras kai dakryOn).
       WEB: "with strong crying and tears." KJV: "with strong
       crying and tears." Gethsemane — Jesus' prayers were not
       calm and composed but agonized.

v.8  — NET: "Although he was a son, he learned obedience through
       the things he suffered" — "learned" (emathen = learned by
       experience). WEB: "though he was a Son, yet learned
       obedience by the things which he suffered." Even the Son
       needed experiential learning — obedience was not automatic
       for His human nature.

v.9  — NET: "he became the source of eternal salvation to all who
       obey him" — "source" (aitios = cause/author). WEB: "author
       of eternal salvation." KJV: "the author of eternal
       salvation." Christ didn't just procure salvation — He IS
       its origin and cause.

v.12 — NET: "you have come to need milk, not solid food" — "milk"
       (galaktos) vs. "solid food" (stereas trophEs). WEB: "you
       have become such as have need of milk." KJV: "ye have need
       of milk." A rebuke: by now they should be teachers, but
       they've regressed to infancy.

v.14 — NET: "solid food is for the mature, whose perceptions are
       trained by practice to discern both good and evil" — "trained
       by practice" (gegymnasmenOn = exercised/gymnasiumed). WEB:
       "those who by reason of use have their senses exercised."
       Spiritual maturity comes through repeated exercise of
       discernment — not theory but practice."""

notes[6] = """v.4  — NET: "For it is impossible in the case of those who have
       once been enlightened... if they fall away, to renew them
       again to repentance" — "impossible" (adynaton = without
       power/unable). WEB: "it is impossible." KJV: "it is
       impossible." The most debated warning passage in Hebrews —
       who are these people and what is their state?

v.5  — NET: "tasted the good word of God and the miracles of the
       coming age" — "tasted" (geusamenos = experienced/sampled).
       WEB: "tasted the good word of God." Does "tasted" mean full
       experience or merely sampling? The debate shapes the
       interpretation of the whole passage.

v.11 — NET: "we passionately want each of you to demonstrate the
       same eagerness for the fulfillment of your hope" —
       "passionately want" (epithymoumen = intensely desire). WEB:
       "we desire that each one of you may show the same diligence."
       Despite the warning, the author expresses confidence (v.9).

v.18 — NET: "we who have fled for refuge may find strong
       encouragement to cling to the hope set before us" — "fled
       for refuge" (kataphygontes = those who have run for shelter).
       WEB: "who have fled for refuge." Cities of refuge imagery —
       we have run to Christ for asylum.

v.19 — NET: "We have this hope as an anchor for the soul, sure
       and steadfast" — "anchor" (ankyran = anchor). WEB: "an
       anchor of the soul." KJV: "an anchor of the soul." The
       only NT use of "anchor" — our hope is fastened in the
       heavenly Holy of Holies where Christ has entered."""

notes[7] = """v.3  — NET: "without father, without mother, without genealogy,
       he has neither beginning of days nor end of life" —
       describing Melchizedek's literary presentation (not ontology).
       WEB: "without father, without mother, without genealogy."
       Genesis records no birth, death, or family — he appears and
       disappears, prefiguring Christ's eternal priesthood.

v.19 — NET: "through which we draw near to God" — "draw near"
       (engizomen tO theO = come close to God). WEB: "through
       which we draw near to God." KJV: "by the which we draw nigh
       unto God." The Law couldn't accomplish this — only a better
       hope through a better priest can bring us near.

v.22 — NET: "Jesus has become the guarantee of a better covenant"
       — "guarantee" (engyos = surety/one who pledges). WEB:
       "Jesus has become the collateral of a better covenant." KJV:
       "Jesus made a surety of a better testament." Only here in
       the NT — Jesus personally guarantees the new covenant.

v.25 — NET: "he is able to save completely those who come to God
       through him" — "completely" (eis to panteles = to the
       uttermost/forever/perfectly). WEB: "to the uttermost." KJV:
       "to the uttermost." Both temporal (forever) and qualitative
       (completely) — no limit to His saving power.

v.27 — NET: "he did this once for all when he offered himself" —
       "once for all" (ephapax). WEB: "once for all." KJV: "once."
       The single, unrepeatable sacrifice — no repetition needed
       or possible. The finality of Christ's offering."""

notes[8] = """v.6  — NET: "But now Jesus has obtained a superior ministry,
       since the covenant that he mediates is also better" —
       "superior" (diaphorOteras = more excellent/distinguished).
       WEB: "a more excellent ministry." KJV: "a more excellent
       ministry." Better ministry, better covenant, better promises
       — the argument of the whole book.

v.10 — NET: "I will put my laws in their minds and I will inscribe
       them on their hearts" — quoting Jeremiah 31:33. "Inscribe"
       (epigraphO = write upon). WEB: "I will put my laws into
       their mind, I will also write them on their heart." Internal
       law replacing external tablets — the Spirit writes.

v.12 — NET: "I will be merciful toward their evil deeds, and
       their sins I will remember no longer" — "remember no longer"
       (ou mE mnEsthO eti = absolutely will not recall). WEB:
       "Their sins and their iniquities will I remember no more."
       Double negative + emphatic = the strongest possible denial.
       God CHOOSES to forget.

v.13 — NET: "When he speaks of a new covenant, he makes the first
       obsolete" — "obsolete" (pepalaiken = made old/outdated).
       WEB: "he has made the first old." KJV: "he hath made the
       first old." The old covenant is not evil but expired — it
       served its purpose and is now superseded.

v.13 — NET: "what is growing obsolete and aging is about to
       disappear" — "about to disappear" (engys aphanismou = near
       vanishing). Written before AD 70 when the temple was
       destroyed — prophetic timing. WEB: "near to vanishing away."
       The temple system was already fading when this was written."""

notes[9] = """v.5  — NET: "the cherubim of glory overshadowing the mercy
       seat" — "mercy seat" (hilastErion = place of propitiation/
       atonement cover). WEB: "the cherubim of glory overshadowing
       the mercy seat." KJV: "the mercyseat." The lid of the Ark
       where blood was sprinkled — the meeting point of God's
       holiness and mercy.

v.12 — NET: "he entered once for all into the most holy place not
       by the blood of goats and calves but by his own blood" —
       "once for all" (ephapax). WEB: "once for all." KJV: "once."
       The decisive, unrepeatable entry — no annual repetition
       like the earthly high priest.

v.14 — NET: "how much more will the blood of Christ, who through
       the eternal Spirit offered himself without blemish to God,
       purify our consciences" — "eternal Spirit" (pneumatos
       aiOniou). WEB: "through the eternal Spirit." Christ's
       sacrifice offered through the Spirit — Trinitarian atonement.

v.22 — NET: "without the shedding of blood there is no
       forgiveness" — "shedding of blood" (haimatekchysias =
       blood-pouring). WEB: "apart from shedding of blood there is
       no remission." KJV: "without shedding of blood is no
       remission." A foundational OT principle fulfilled in Christ.

v.27 — NET: "people are appointed to die once, and then to face
       judgment" — "appointed" (apokeitai = laid up/reserved/stored
       away). WEB: "it is appointed for men to die once." KJV: "it
       is appointed unto men once to die." The universality and
       finality of death — then judgment. No second chances."""

notes[10] = """v.1  — NET: "the law is only a shadow of the good things to
       come and not the reality itself" — "shadow" (skian) vs.
       "reality" (eikona = image/true form). WEB: "a shadow of the
       good things to come, not the very image." The law was a
       silhouette — Christ is the substance casting the shadow.

v.10 — NET: "we have been made holy through the offering of the
       body of Jesus Christ once for all" — "made holy"
       (hEgiasmenoi esmen = we have been sanctified — perfect
       tense). WEB: "we have been sanctified." KJV: "we are
       sanctified." Perfect tense: completed act with ongoing
       result. Positional holiness is settled.

v.14 — NET: "by one offering he has perfected for all time those
       who are made holy" — "perfected for all time" (teteleiOken
       eis to diEnekes). WEB: "he has perfected forever those who
       are being sanctified." "Perfected" (past/complete) + "being
       sanctified" (present/ongoing) — positional and progressive.

v.19 — NET: "we have confidence to enter the most holy place by
       the blood of Jesus" — "confidence" (parrEsian = boldness/
       freedom of speech/access). WEB: "boldness to enter into the
       holy place." KJV: "boldness to enter into the holiest." Not
       timid approach but confident access — the veil is torn.

v.31 — NET: "It is a terrifying thing to fall into the hands of
       the living God" — "terrifying" (phoberon = fearful/dreadful).
       WEB: "It is a fearful thing to fall into the hands of the
       living God." KJV: "It is a fearful thing." After the warning
       of vv.26-30, this conclusion — God as judge is terrifying."""

notes[11] = """v.1  — NET: "Now faith is being sure of what we hope for,
       being convinced of what we do not see" — "being sure"
       (hypostasis = substance/foundation/confidence). "Being
       convinced" (elenchos = proof/evidence/conviction). WEB:
       "faith is assurance of things hoped for, proof of things
       not seen." KJV: "substance... evidence." Faith is itself
       the proof — not blind but substantive.

v.3  — NET: "By faith we understand that the worlds were set in
       order at God's command" — "set in order" (katErtisthai =
       framed/prepared/equipped). WEB: "the universe has been
       framed by the word of God." KJV: "the worlds were framed
       by the word of God." Creation by divine speech — the first
       act of faith-understanding.

v.6  — NET: "without faith it is impossible to please him" —
       "impossible" (adynaton = without power/unable). WEB: "without
       faith it is impossible to be well pleasing to him." The most
       absolute statement: no faith = no pleasing God. Period.

v.13 — NET: "These all died in faith without receiving the
       things promised" — "without receiving" (mE labontes = not
       having obtained). WEB: "not having received the promises."
       KJV: "not having received the promises." Faith's greatest
       test: dying without seeing the fulfillment.

v.40 — NET: "God had planned something better for us, so that
       they would be made perfect together with us" — "something
       better for us" (peri hEmOn kreitton ti problepsamenos). WEB:
       "God having provided some better thing concerning us." OT
       saints wait for completion WITH us — one people of God,
       perfected together."""

notes[12] = """v.1  — NET: "let us run with endurance the race set out for
       us" — "endurance" (hypomonEs = patient steadfastness). WEB:
       "let's run with perseverance the race." KJV: "let us run
       with patience the race." Not a sprint but a marathon —
       endurance, not speed, is the virtue.

v.2  — NET: "keeping our eyes fixed on Jesus, the pioneer and
       perfecter of our faith" — "pioneer and perfecter" (archEgon
       kai teleiOtEn = author/originator and completer/finisher).
       WEB: "the author and perfecter of faith." KJV: "the author
       and finisher of our faith." He starts it AND finishes it.

v.6  — NET: "the Lord disciplines the one he loves and chastises
       every son he accepts" — "chastises" (mastigoi = scourges/
       whips). WEB: "scourges every son whom he receives." KJV:
       "scourgeth every son whom he receiveth." Strong language —
       divine discipline is sometimes painful, not just gentle
       correction.

v.11 — NET: "it yields the peaceful fruit of righteousness for
       those trained by it" — "trained" (gegymnasmenos = exercised/
       gymnased). WEB: "the peaceful fruit of righteousness." KJV:
       "the peaceable fruit of righteousness." Discipline PRODUCES
       something — not pointless suffering but purposeful training.

v.29 — NET: "our God is indeed a consuming fire" — quoting
       Deuteronomy 4:24. "Consuming" (katanaliskon = completely
       devouring). WEB: "our God is a consuming fire." KJV: "our
       God is a consuming fire." The final word of the chapter —
       after grace and access comes holy reverence."""

notes[13] = """v.5  — NET: "I will never leave you and never abandon you" —
       five negatives in Greek (ou mE se anO, oud' ou mE se
       enkatalipO) — the strongest possible denial. WEB: "I will
       in no way leave you, neither will I in any way forsake you."
       KJV: "I will never leave thee, nor forsake thee." Five-fold
       negation = absolute certainty of presence.

v.8  — NET: "Jesus Christ is the same yesterday and today and
       forever" — "the same" (ho autos = identical/unchanging).
       WEB: "Jesus Christ is the same yesterday, today, and
       forever." KJV: "Jesus Christ the same yesterday, and to day,
       and for ever." Immutability — past faithfulness guarantees
       future faithfulness.

v.12 — NET: "Therefore Jesus also suffered outside the camp in
       order to sanctify the people by his own blood" — "outside
       the camp" (exO tEs pylEs = outside the gate). WEB: "outside
       of the gate." Jesus died outside Jerusalem — outside the
       system, rejected by the establishment.

v.13 — NET: "We must go out to him outside the camp, bearing the
       abuse he experienced" — "bearing the abuse" (ton oneidismon
       autou pherontes = carrying His reproach). WEB: "bearing his
       reproach." KJV: "bearing his reproach." Identification with
       the rejected Christ means rejection by the religious system.

v.15 — NET: "Through him then let us continually offer up a
       sacrifice of praise to God, that is, the fruit of our lips,
       acknowledging his name" — "sacrifice of praise" (thysian
       aineseOs). WEB: "a sacrifice of praise." KJV: "the sacrifice
       of praise." Our lips replace animal sacrifices — praise is
       the new covenant offering."""

for ch, note_text in sorted(notes.items()):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Hebrews " + str(ch))
        else:
            print("  skip Hebrews " + str(ch))
    else:
        print("  missing Hebrews " + str(ch))
