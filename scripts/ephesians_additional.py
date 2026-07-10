#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Ephesians chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/10 - Ephesians"

notes = dict()

notes[1] = """v.3  — NET: "Blessed is the God and Father of our Lord Jesus
       Christ, who has blessed us with every spiritual blessing in
       the heavenly realms in Christ" — "heavenly realms" (tois
       epouraniois = the heavenlies). WEB: "in the heavenly places."
       KJV: "in heavenly places." A key Ephesians phrase (1:3, 20;
       2:6; 3:10; 6:12) — the spiritual dimension where believers
       are already seated.

v.4  — NET: "he chose us in Christ before the foundation of the
       world" — "before the foundation" (pro katabolEs kosmou).
       WEB: "before the foundation of the world." Election is
       pre-temporal — decided before creation, not in response to
       foreseen faith or merit.

v.7  — NET: "In him we have redemption through his blood, the
       forgiveness of our trespasses" — "redemption" (apolytrOsin
       = ransom/release by payment). WEB: "redemption through his
       blood." KJV: "redemption through his blood." Slave-market
       language — purchased out of bondage at the cost of blood.

v.13 — NET: "you were sealed with the promised Holy Spirit" —
       "sealed" (esphragisthEte = stamped with a seal of ownership).
       WEB: "you were sealed with the Holy Spirit of promise." KJV:
       "ye were sealed with that holy Spirit of promise." A seal
       marks ownership, authenticity, and security.

v.19 — NET: "what is the incomparably great power for us who
       believe" — "incomparably great" (hyperballon megethos =
       surpassing greatness). WEB: "the exceeding greatness of his
       power toward us who believe." The same power that raised
       Christ from the dead (v.20) works in believers."""

notes[2] = """v.1  — NET: "And although you were dead in your transgressions
       and sins" — "dead" (nekrous = corpses). WEB: "you were dead
       in your transgressions and sins." Not sick or weak — DEAD.
       Dead people cannot contribute to their own resurrection.

v.4  — NET: "But God, being rich in mercy, because of his great
       love with which he loved us" — "But God" (ho de theos) —
       the great turning point. WEB: "But God, being rich in mercy."
       KJV: "But God, who is rich in mercy." Two words that change
       everything — divine intervention into human helplessness.

v.8  — NET: "For by grace you are saved through faith, and this
       is not from yourselves, it is the gift of God" — "this"
       (touto) — what is the gift? Grace? Faith? The whole package?
       The neuter pronoun doesn't match "faith" (feminine) or
       "grace" (feminine) — it refers to the entire salvation
       arrangement. WEB: "it is the gift of God."

v.10 — NET: "For we are his creative work, having been created in
       Christ Jesus for good works" — "creative work" (poiEma =
       masterpiece/workmanship). WEB: "we are his workmanship."
       KJV: "we are his workmanship." English "poem" derives from
       this — we are God's artistic creation.

v.14 — NET: "For he is our peace, the one who made both groups
       into one and who destroyed the middle wall of partition" —
       "middle wall of partition" (to mesotoichon tou phragmou).
       WEB: "the middle wall of separation." KJV: "the middle wall
       of partition." Likely refers to the temple barrier
       separating Gentile and Jewish courts."""

notes[3] = """v.5  — NET: "that the Gentiles are fellow heirs, fellow
       members of the body, and fellow partakers of the promise
       in Christ Jesus" — three "fellow" (syn-) compounds:
       synklEronoma, syssOma, symmetocha. WEB: "fellow heirs and
       fellow members of the body, and fellow partakers of his
       promise." The triple syn- emphasizes full equality.

v.8  — NET: "To me — Loss less than the least of all the saints —
       this grace was given" — "less than the least" (tO
       elachistoterO = a comparative of a superlative — grammatically
       impossible, emotionally powerful). WEB: "to me, the very
       least of all saints." Paul invents a word to express his
       unworthiness.

v.16 — NET: "that he may grant you to be strengthened with power
       through his Spirit in the inner person" — "inner person"
       (eis ton esO anthrOpon). WEB: "strengthened with power
       through his Spirit in the inner person." KJV: "strengthened
       with might by his Spirit in the inner man." The Spirit's
       primary work is internal.

v.18 — NET: "may be able to comprehend with all the saints what
       is the breadth and length and height and depth" — four
       dimensions of Christ's love. WEB: "the breadth and length
       and height and depth." No object specified — the love is so
       vast it requires spatial metaphor yet exceeds all dimensions.

v.20 — NET: "Now to him who by the power that is working within
       us is able to do far beyond all that we ask or think" —
       "far beyond" (hyper ek perissou = super-abundantly above).
       WEB: "exceedingly abundantly above all that we ask or
       think." KJV: "exceeding abundantly above all that we ask or
       think." Triple intensification — God's ability exceeds
       imagination."""

notes[4] = """v.3  — NET: "making every effort to keep the unity of the
       Spirit in the bond of peace" — "making every effort"
       (spoudazontes = being diligent/eager). WEB: "being eager to
       keep the unity of the Spirit." KJV: "Endeavouring to keep
       the unity." Unity exists; our job is to MAINTAIN it, not
       create it.

v.11 — NET: "It was he who gave some as apostles, some as
       prophets, some as evangelists, and some as pastors and
       teachers" — "gave" (edOken = gifted). WEB: "He gave some
       to be apostles." The leaders ARE the gifts to the church —
       not just their abilities but their persons.

v.13 — NET: "until we all attain to the unity of the faith and of
       the knowledge of the Son of God — to a mature person" —
       "mature person" (andra teleion = complete/full-grown man).
       WEB: "to a full grown man." KJV: "unto a perfect man." Not
       individual perfection but corporate maturity — the whole
       body growing up together.

v.15 — NET: "speaking the truth in love, we will in all things
       grow up into him who is the head, that is, Christ" —
       "speaking the truth in love" (alEtheuontes en agapE =
       truthing in love — a rare verb). WEB: "speaking truth in
       love." Truth without love wounds; love without truth deceives.
       Both together produce growth.

v.26 — NET: "Be angry and do not sin; do not let the sun go down
       on the cause of your anger" — quoting Psalm 4:4. "Be angry"
       (orgizesthe) — anger itself is not sin; nursing it overnight
       is. WEB: "Be angry, and don't sin." KJV: "Be ye angry, and
       sin not." A time limit on anger — sunset is the deadline."""

notes[5] = """v.2  — NET: "and live in love, just as Christ also loved us and
       gave himself for us, a sacrificial and fragrant offering to
       God" — "fragrant offering" (prosphoran kai thysian tO theO
       eis osmEn euOdias). WEB: "a fragrant offering and sacrifice
       to God." KJV: "a sweetsmelling savour." Christ's death
       pleased the Father — a voluntary, accepted sacrifice.

v.14 — NET: "Awake, O sleeper! Rise from the dead, and Christ
       will shine on you!" — possibly an early Christian hymn or
       baptismal formula. WEB: "Awake, you who sleep, and arise
       from the dead, and Christ will shine on you." KJV: "Awake
       thou that sleepest." Source unknown — perhaps adapted from
       Isaiah 60:1.

v.18 — NET: "And do not get drunk with wine, which is
       debauchery, but be filled by the Spirit" — "be filled"
       (plErousthe = present passive imperative — keep on being
       filled). WEB: "be filled with the Spirit." KJV: "be filled
       with the Spirit." Not a one-time event but a continuous
       state — the ongoing alternative to drunkenness.

v.25 — NET: "Husbands, love your wives just as Christ loved the
       church and gave himself for her" — "gave himself" (heauton
       paredOken) — self-sacrificial love as the husband's model.
       WEB: "love your wives, even as Christ also loved the
       assembly." The standard is the cross — not feelings but
       sacrifice.

v.32 — NET: "This mystery is great — but I am actually speaking
       with reference to Christ and the church" — "mystery"
       (mystErion) — marriage was always meant to picture something
       bigger. WEB: "This mystery is great, but I speak concerning
       Christ and the assembly." Marriage as icon of redemption."""

notes[6] = """v.10 — NET: "Finally, be strengthened in the Lord and in the
       strength of his might" — "be strengthened" (endynamousthe =
       be empowered, present passive). WEB: "be strong in the Lord,
       and in the strength of his might." KJV: "be strong in the
       Lord." Not self-strength but divine empowerment.

v.11 — NET: "Clothe yourselves with the full armor of God so that
       you may be able to stand against the schemes of the devil"
       — "schemes" (methodias = methods/strategies/wiles). WEB:
       "Put on the whole armor of God." KJV: "Put on the whole
       armour of God." The enemy has strategies — believers need
       corresponding equipment.

v.12 — NET: "For our struggle is not against flesh and blood, but
       against the rulers, against the powers, against the world
       rulers of this darkness, against the spiritual forces of
       evil in the heavens" — four ranks of spiritual opposition.
       WEB: "against the principalities, against the powers."
       The real enemy is invisible.

v.17 — NET: "the sword of the Spirit, which is the word of God"
       — "word" (rhEma = spoken/specific word, not logos = written
       word). WEB: "the sword of the Spirit, which is the word of
       God." The only offensive weapon listed — all others are
       defensive. The spoken word of God is the attack weapon.

v.18 — NET: "With every prayer and petition, pray at all times
       in the Spirit" — "at all times" (en panti kairO = in every
       season/at every opportunity). WEB: "praying at all times in
       the Spirit." KJV: "Praying always with all prayer." Prayer
       undergirds all the armor — it is the atmosphere in which
       the armor is worn."""


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

for ch, note_text in sorted(notes.items()):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Chapter " + str(ch))
        else:
            print("  skip Chapter " + str(ch))
    else:
        print("  missing Chapter " + str(ch))
