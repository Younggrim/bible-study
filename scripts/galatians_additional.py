#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Galatians chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/09 - Galatians"

notes = dict()

notes[1] = """v.4  — NET: "who gave himself for our sins to rescue us from
       this present evil age" — "rescue" (exelEtai = deliver/
       extract). WEB: "who gave himself for our sins, that he
       might deliver us out of this present evil age." KJV: "that
       he might deliver us from this present evil world." The cross
       as rescue operation from an evil system.

v.6  — NET: "I am astonished that you are so quickly deserting
       the one who called you by the grace of Christ" — "astonished"
       (thaumazO = amazed/marvel). WEB: "I marvel that you are so
       quickly deserting." No thanksgiving section — Paul is too
       upset. This is the angriest letter in the NT.

v.8  — NET: "But even if we or an angel from heaven should preach
       a gospel contrary to the one we preached to you, let him be
       condemned to hell!" — "condemned to hell" (anathema estO).
       WEB: "let him be cursed." KJV: "let him be accursed." NET
       intensifies the translation; the Greek is a solemn curse.

v.15 — NET: "set me apart from birth and called me by his grace"
       — "set apart from birth" (aphorisas me ek koilias mEtros
       mou = separated me from my mother's womb). WEB: "separated
       me from my mother's womb." Echoes Jeremiah 1:5 — prophetic
       calling before birth.

v.16 — NET: "to reveal his Son in me so that I could preach him
       among the Gentiles" — "in me" (en emoi) — not just "to me"
       but "in me." WEB: "to reveal his Son in me." The revelation
       was internal transformation, not just information transfer."""

notes[2] = """v.9  — NET: "James, Cephas, and John, who had a reputation as
       pillars, gave to Barnabas and me the right hand of
       fellowship" — "pillars" (styloi = columns/supports). WEB:
       "who were reputed to be pillars." KJV: "who seemed to be
       pillars." The metaphor: they hold up the church structure.

v.11 — NET: "I opposed him to his face, because he had clearly
       done wrong" — "to his face" (kata prosOpon) — public sin
       required public correction. WEB: "I resisted him to his
       face." KJV: "I withstood him to the face." Paul rebukes
       Peter — apostolic authority doesn't exempt one from rebuke.

v.16 — NET: "a person is not justified by the works of the law
       but by the faithfulness of Jesus Christ" — "faithfulness of
       Jesus Christ" (pisteOs IEsou Christou) — major debate:
       "faith IN Christ" (objective genitive, KJV/WEB) vs. "faith
       OF Christ" (subjective genitive, NET option). Both meanings
       may be intended.

v.20 — NET: "I have been crucified with Christ, and it is no
       longer I who live, but Christ lives in me" — "crucified
       with" (Christoi synestaurOmai = co-crucified, perfect tense
       — completed action with ongoing result). WEB: "I have been
       crucified with Christ." The old self permanently executed.

v.21 — NET: "if righteousness could come through the law, then
       Christ died for nothing!" — "for nothing" (dOrean = without
       cause/gratuitously). WEB: "then Christ died for nothing."
       KJV: "then Christ is dead in vain." The logical conclusion:
       if law saves, the cross is pointless."""

notes[3] = """v.1  — NET: "You foolish Galatians! Who has cast a spell on
       you?" — "foolish" (anoEtoi = without understanding/senseless).
       "Cast a spell" (ebaskanen = bewitched/given the evil eye).
       WEB: "who has bewitched you?" KJV: "who hath bewitched you?"
       Paul uses magical language — they've been enchanted away
       from truth.

v.6  — NET: "Just as Abraham believed God, and it was credited to
       him as righteousness" — quoting Genesis 15:6. WEB: "Abraham
       believed God, and it was accounted to him for righteousness."
       The same verb (logizesthai = reckon/credit) as Romans 4.
       Faith has always been the means of righteousness.

v.13 — NET: "Christ redeemed us from the curse of the law by
       becoming a curse for us" — "becoming a curse" (genomenos
       hyper hEmOn katara). WEB: "having become a curse for us."
       KJV: "being made a curse for us." Quoting Deuteronomy 21:23
       — "cursed is everyone who hangs on a tree." Substitution.

v.24 — NET: "the law had become our guardian until Christ came,
       so that we could be declared righteous by faith" — "guardian"
       (paidagOgos = child-conductor/tutor-slave). WEB: "the law
       has become our tutor to bring us to Christ." KJV: "the law
       was our schoolmaster to bring us unto Christ." Not a teacher
       but a slave who escorted children — temporary authority.

v.28 — NET: "There is neither Jew nor Greek, there is neither
       slave nor free, there is neither male nor female — for all
       of you are one in Christ Jesus" — three social divisions
       abolished in Christ. WEB: "There is neither Jew nor Greek...
       male nor female." KJV: "There is neither Jew nor Greek."
       Not elimination of distinction but equality of access."""

notes[4] = """v.4  — NET: "But when the appropriate time had come, God sent
       out his Son, born of a woman, born under the law" — "the
       appropriate time" (to plErOma tou chronou = the fullness of
       time). WEB: "when the fullness of the time came." KJV: "when
       the fulness of the time was come." History has a divine
       timetable — Christ arrived at the precise moment.

v.6  — NET: "And because you are sons, God sent the Spirit of his
       Son into our hearts, who calls 'Abba! Father!'" — "Abba"
       (Aramaic intimate address). WEB: "crying, 'Abba, Father!'"
       KJV: "crying, Abba, Father." The Spirit enables the
       intimate cry that proves adoption — slaves don't call the
       master "Daddy."

v.9  — NET: "how can you turn back again to the weak and
       worthless basic forces? Do you want to be enslaved to them
       all over again?" — "basic forces" (stoicheia = elemental
       principles/rudiments). WEB: "the weak and miserable elemental
       principles." KJV: "weak and beggarly elements." Returning to
       law-keeping is regression, not progress.

v.19 — NET: "My children — Loss Loss I am again undergoing birth
       pains until Christ is formed in you!" — "formed" (morphOthE
       = takes shape). WEB: "until Christ is formed in you." KJV:
       "until Christ be formed in you." Paul as a mother in labor
       — the goal is Christ's character reproduced in them.

v.26 — NET: "But the Jerusalem above is free, and she is our
       mother" — "Jerusalem above" — the heavenly city, the true
       homeland of faith. WEB: "the Jerusalem that is above is
       free, which is the mother of us all." Two Jerusalems: earthly
       (bondage) and heavenly (freedom)."""

notes[5] = """v.1  — NET: "For freedom Christ has set us free. Stand firm,
       then, and do not be subject again to the yoke of slavery" —
       "for freedom" (tE eleutheria = for the purpose of freedom).
       WEB: "Stand firm therefore in the liberty by which Christ
       has made us free." Freedom is both the means and the goal
       of Christ's work.

v.4  — NET: "You who are trying to be declared righteous by the
       law have been alienated from Christ; you have fallen away
       from grace!" — "fallen away from grace" (tEs charitos
       exepesate). WEB: "you are fallen from grace." Not loss of
       salvation but departure from the grace-principle back to
       law-principle.

v.6  — NET: "For in Christ Jesus neither circumcision nor
       uncircumcision carries any weight — the only thing that
       matters is faith working through love" — "faith working
       through love" (pistis di' agapEs energoumenE). WEB: "faith
       working through love." KJV: "faith which worketh by love."
       Not bare faith or bare love — faith energized by love.

v.17 — NET: "For the flesh has desires that are opposed to the
       Spirit, and the Spirit has desires that are opposed to the
       flesh" — "opposed" (antikeitai = set against/in conflict).
       WEB: "the flesh lusts against the Spirit, and the Spirit
       against the flesh." Ongoing internal war — not passive
       coexistence.

v.22 — NET: "But the fruit of the Spirit is love, joy, peace,
       patience, kindness, goodness, faithfulness, gentleness, and
       self-control" — "fruit" (karpos) is SINGULAR — one fruit
       with nine characteristics. WEB: "the fruit of the Spirit is
       love, joy, peace..." Not fruits (plural) but one integrated
       character produced by the Spirit."""

notes[6] = """v.1  — NET: "Brothers and sisters, if a person is discovered in
       some sin, you who are spiritual restore such a person in a
       spirit of gentleness" — "restore" (katartizete = mend/set a
       bone/repair a net). WEB: "restore such a one in a spirit of
       gentleness." KJV: "restore such an one in the spirit of
       meekness." Medical/fishing imagery — gentle repair.

v.2  — NET: "Carry one another's burdens, and in this way you
       will fulfill the law of Christ" — "burdens" (barE = heavy
       loads, crushing weights). WEB: "Bear one another's burdens."
       KJV: "Bear ye one another's burdens." Contrasted with v.5
       "each one shall bear his own load" (phortion = pack/
       knapsack) — different Greek words, different responsibilities.

v.7  — NET: "Do not be deceived. God will not be made a fool.
       For a person will reap what he sows" — "will not be made a
       fool" (ou myktErizetai = is not mocked/turned up the nose
       at). WEB: "God is not mocked." KJV: "God is not mocked."
       The harvest is inevitable and proportional.

v.14 — NET: "But may I never boast except in the cross of our
       Lord Jesus Christ, through which the world has been
       crucified to me, and I to the world" — "crucified to me...
       I to the world" — mutual death. WEB: "the world has been
       crucified to me, and I to the world." Double crucifixion —
       the world is dead to Paul and Paul to the world.

v.17 — NET: "I carry the marks of Jesus on my body" — "marks"
       (stigmata = brand marks/scars). WEB: "I bear the marks of
       the Lord Jesus in my body." KJV: "I bear in my body the
       marks of the Lord Jesus." His scars from persecution are
       his credentials — branded as Christ's slave."""


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
