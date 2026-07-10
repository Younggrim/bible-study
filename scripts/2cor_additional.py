#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to 2 Corinthians chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/08 - 2 Corinthians"

notes = dict()

notes[1] = """v.3  — NET: "Blessed is the God and Father of our Lord Jesus
       Christ, the Father of mercies and God of all comfort" —
       "Father of mercies" (patEr tOn oiktirmOn). WEB: "the Father
       of mercies and God of all comfort." KJV: "the Father of
       mercies, and the God of all comfort." Mercy defines God's
       paternal character.

v.5  — NET: "For just as the sufferings of Christ overflow toward
       us, so also our comfort through Christ overflows to you" —
       "overflow" (perisseuei = abounds/exceeds). WEB: "as the
       sufferings of Christ abound to us." Suffering and comfort
       both come in abundance — the ratio is maintained.

v.20 — NET: "For every one of God's promises are 'Yes' in him" —
       "Yes" (nai = affirmative). WEB: "For however many are the
       promises of God, in him is the 'Yes.'" KJV: "all the
       promises of God in him are yea, and in him Amen." Christ is
       the fulfillment of every divine promise.

v.22 — NET: "who also sealed us and gave us the Spirit in our
       hearts as a down payment" — "down payment" (arrabOna =
       deposit/guarantee/earnest). KJV: "the earnest of the Spirit."
       WEB: "the down payment of the Spirit." A commercial term —
       the Spirit now guarantees the full inheritance later.

v.24 — NET: "Not that we lord it over your faith, but we are
       workers with you for your joy" — "workers with you"
       (synergoi = co-workers). WEB: "we are fellow workers with
       you for your joy." Apostolic authority serves joy, not
       domination."""

notes[2] = """v.7  — NET: "you should rather forgive and comfort him, so that
       he will not be swallowed up by excessive grief" — "swallowed
       up" (katapothE = consumed/overwhelmed). WEB: "swallowed up
       with his excessive sorrow." Discipline without restoration
       destroys rather than heals.

v.11 — NET: "so that we may not be exploited by Satan (for we are
       not ignorant of his schemes)" — "schemes" (noEmata =
       thoughts/designs/strategies). WEB: "his schemes." KJV: "his
       devices." Satan has a strategy — unforgiveness is one of
       his primary tools.

v.14 — NET: "who always leads us in triumphal procession in
       Christ and who makes known through us the fragrance that
       consists of the knowledge of him in every place" — "triumphal
       procession" (thriambeuonti = leading in a Roman triumph
       parade). WEB: "always leads us in triumph in Christ." We
       are captives in Christ's victory march.

v.16 — NET: "To the one, we are the smell of death that leads to
       death; to the other, the smell of life that leads to life"
       — the same gospel produces opposite reactions. WEB: "to the
       one a stench from death to death; to the other a sweet
       aroma from life to life." Same message, different destinies.

v.17 — NET: "For we are not like so many others, hucksters who
       peddle the word of God for profit" — "hucksters" (kapEleuontes
       = retail traders/adulterators). WEB: "peddling the word of
       God." KJV: "which corrupt the word of God." False teachers
       commodify the gospel for personal gain."""

notes[3] = """v.3  — NET: "You are our letter, written on our hearts, known
       and read by everyone" — "written on our hearts" — the
       Corinthians themselves are Paul's credentials. WEB: "written
       in our hearts, known and read by all men." KJV: "written in
       our hearts, known and read of all men." Living epistles.

v.6  — NET: "the letter kills, but the Spirit gives life" — "the
       letter" (to gramma) = the written law code. WEB: "the
       letter kills, but the Spirit gives life." KJV: "the letter
       killeth, but the spirit giveth life." Not Scripture itself
       but law-as-system-of-merit kills — the Spirit vivifies.

v.17 — NET: "Now the Lord is the Spirit, and where the Spirit of
       the Lord is present, there is freedom" — "the Lord is the
       Spirit" — a profound Trinitarian identification. WEB: "where
       the Spirit of the Lord is, there is liberty." KJV: "where
       the Spirit of the Lord is, there is liberty." Freedom from
       the veil, from the letter, from condemnation.

v.18 — NET: "And we all, with unveiled faces reflecting the glory
       of the Lord, are being transformed into the same image from
       one degree of glory to another" — "being transformed"
       (metamorphoumetha = present passive — ongoing metamorphosis).
       WEB: "transformed into the same image from glory to glory."
       Progressive sanctification as beholding becomes becoming.

v.18 — NET: "from one degree of glory to another" — "from glory
       to glory" (apo doxEs eis doxan). KJV: "from glory to
       glory." WEB: "from glory to glory." Not instant but
       incremental — each stage more glorious than the last,
       driven by the Spirit's work."""

notes[4] = """v.4  — NET: "among whom the god of this age has blinded the
       minds of those who do not believe" — "the god of this age"
       (ho theos tou aiOnos toutou) = Satan. WEB: "the god of this
       world." KJV: "the god of this world." Satan has temporary
       authority over this present evil age (cf. John 12:31).

v.6  — NET: "For God, who said, 'Let light shine out of darkness,'
       is the one who shined in our hearts to give us the light"
       — creation and conversion linked. WEB: "God, who said,
       'Light will shine out of darkness,' has shone in our hearts."
       Salvation is a new creation act — Genesis 1:3 repeated in
       the soul.

v.7  — NET: "But we have this treasure in clay jars, so that the
       extraordinary power belongs to God and does not come from
       us" — "clay jars" (ostrakinos skeuesi = earthenware vessels).
       WEB: "earthen vessels." KJV: "earthen vessels." The treasure
       is the gospel; the container is fragile humanity. The contrast
       is intentional.

v.16 — NET: "our inner person is being renewed day by day" —
       "being renewed" (anakainoutai = present passive — continuous
       renewal). WEB: "the inward man is renewed day by day." KJV:
       "the inward man is renewed day by day." Outer decay is
       matched by inner restoration — daily.

v.17 — NET: "For our momentary, light suffering is producing for
       us an eternal weight of glory far beyond all comparison" —
       "momentary" vs. "eternal," "light" vs. "weight" — deliberate
       contrasts. WEB: "our light affliction, which is for the
       moment, works for us more and more exceedingly an eternal
       weight of glory." Suffering as productive force."""

notes[5] = """v.1  — NET: "we have a building from God, a house not built by
       human hands, that is eternal in the heavens" — "building"
       (oikodomEn = structure/edifice). WEB: "a building from God."
       KJV: "a building of God." The resurrection body described
       as permanent architecture replacing a tent (the earthly body).

v.7  — NET: "for we live by faith, not by sight" — "faith" (pisteos)
       vs. "sight" (eidous = appearance/visible form). WEB: "we
       walk by faith, not by sight." KJV: "we walk by faith, not
       by sight." One of the most quoted verses — present existence
       is faith-directed, not evidence-dependent.

v.10 — NET: "For we must all appear before the judgment seat of
       Christ" — "judgment seat" (bEma = tribunal platform). WEB:
       "before the judgment seat of Christ." Not a condemnation
       trial (Romans 8:1) but an evaluation of works (rewards).

v.17 — NET: "if anyone is in Christ, he is a new creation; the
       old things have passed away — look, new things have come!"
       — "new creation" (kainE ktisis). WEB: "if anyone is in
       Christ, he is a new creation." KJV: "if any man be in Christ,
       he is a new creature." Not renovation but re-creation.

v.21 — NET: "God made the one who did not know sin to be sin for
       us, so that in him we would become the righteousness of God"
       — "made him to be sin" (hamartian epoiEsen) — the Great
       Exchange. WEB: "him who knew no sin he made to be sin on
       our behalf." KJV: "he hath made him to be sin for us." The
       most concise statement of substitutionary atonement."""

notes[6] = """v.2  — NET: "now is the acceptable time; now is the day of
       salvation!" — "now" (nyn) repeated for emphasis — quoting
       Isaiah 49:8. WEB: "now is the acceptable time. Behold, now
       is the day of salvation." Urgency of present opportunity.

v.4  — NET: "as servants of God we commend ourselves in every
       way: with great endurance, in afflictions, in hardships" —
       Paul's credential list: 28 items of suffering and virtue.
       WEB: "in great endurance, in afflictions, in hardships."
       Authentic ministry authenticated by suffering, not success.

v.10 — NET: "as sorrowful, but always rejoicing; as poor, but
       making many rich; as having nothing, and yet possessing
       everything" — paradox on paradox — the apostolic life defies
       human categories. WEB: "as sorrowful, yet always rejoicing."
       The Christian life is simultaneously suffering and joy.

v.14 — NET: "Do not become partners with those who do not believe.
       For what partnership is there between righteousness and
       lawlessness?" — "partners" (heterozygountes = unequally
       yoked). WEB: "Don't be unequally yoked with unbelievers."
       KJV: "Be ye not unequally yoked together with unbelievers."
       The metaphor is agricultural — two different animals in one yoke.

v.18 — NET: "and I will be a father to you, and you will be my
       sons and daughters" — "sons and daughters" — quoting/adapting
       2 Samuel 7:14 with the addition of "daughters" (not in the
       OT source). WEB: "you will be my sons and daughters." Paul
       expands the promise to include women explicitly."""

notes[7] = """v.1  — NET: "let us cleanse ourselves from everything that
       could defile the body and the spirit" — "body and spirit"
       (sarkos kai pneumatos = flesh and spirit). WEB: "cleansing
       ourselves from all defilement of flesh and spirit." Holiness
       is both physical and spiritual — inside and outside.

v.5  — NET: "we were troubled in every way — Loss conflicts on
       the outside, fears within" — "conflicts outside, fears
       within" (exOthen machai, esOthen phoboi). WEB: "fightings
       without, fears within." KJV: "without were fightings,
       within were fears." Even apostles experience anxiety.

v.9  — NET: "not because you were made sad, but because your
       sadness led to repentance" — "sadness led to repentance"
       (elypEthEte eis metanoian). WEB: "you were made sorry to
       repentance." Godly grief produces change; worldly grief
       produces death (v.10).

v.10 — NET: "For sadness as intended by God produces a repentance
       that leads to salvation, leaving no regret, but worldly
       sadness brings about death" — "leaving no regret" (ametamelEton
       = without regret/irrevocable). WEB: "repentance to salvation,
       which brings no regret." True repentance never regrets itself.

v.11 — NET: "what eagerness, what defense of yourselves, what
       indignation, what alarm, what longing, what zeal, what
       justice!" — seven marks of genuine repentance listed in
       rapid succession. WEB: "what earnest care it worked in you."
       Repentance produces observable fruit — not just feeling sorry."""

notes[8] = """v.2  — NET: "their abundant joy and their extreme poverty have
       overflowed in the wealth of their generosity" — "extreme
       poverty" + "abundant joy" = "wealth of generosity" — the
       equation defies logic. WEB: "their deep poverty abounded to
       the riches of their generosity." Grace-powered giving.

v.5  — NET: "they first gave themselves to the Lord and to us by
       the will of God" — "gave themselves first" — self-giving
       precedes money-giving. WEB: "first they gave their own
       selves to the Lord." The order matters: self, then substance.

v.9  — NET: "For you know the grace of our Lord Jesus Christ,
       that although he was rich, for your sakes he became poor, so
       that you by his poverty could become rich" — the Incarnation
       as economic language. WEB: "though he was rich, yet for your
       sakes he became poor." Christ's poverty = our riches. The
       theological foundation of generosity.

v.12 — NET: "For if the eagerness is present, the gift itself is
       acceptable according to whatever one has, not according to
       what he does not have" — proportional giving, not equal
       amounts. WEB: "it is accepted according to what you have."
       God measures generosity by capacity, not quantity.

v.21 — NET: "For we are concerned about what is right not only
       before the Lord but also before people" — "before people"
       (enOpion anthrOpOn). WEB: "providing honorable things, not
       only in the sight of the Lord, but also in the sight of
       men." Financial transparency as ministry principle."""

notes[9] = """v.6  — NET: "the person who sows generously will also reap
       generously" — "generously" (ep' eulogiais = upon blessings).
       WEB: "He who sows bountifully will also reap bountifully."
       KJV: "He which soweth bountifully shall reap also
       bountifully." Agricultural law applied to giving — the
       harvest matches the sowing.

v.7  — NET: "Each one of you should give just as he has decided
       in his heart, not reluctantly or under compulsion, because
       God loves a cheerful giver" — "cheerful" (hilaron = joyful/
       glad — English "hilarious" derives from this). WEB: "God
       loves a cheerful giver." Compelled giving contradicts grace.

v.8  — NET: "And God is able to make all grace overflow to you so
       that because you always have enough of everything, you may
       overflow in every good work" — "all grace... always... enough
       of everything... every good work" — comprehensive provision.
       WEB: "God is able to make all grace abound to you." Grace
       enables generosity in a cycle.

v.10 — NET: "will supply and multiply your seed for sowing and
       will cause the harvest of your righteousness to grow" —
       quoting Isaiah 55:10. WEB: "multiply your seed for sowing,
       and increase the fruits of your righteousness." God supplies
       the resources to be generous — He funds what He commands.

v.15 — NET: "Thanks be to God for his indescribable gift!" —
       "indescribable" (anekdiEgEtO = beyond words/inexpressible).
       WEB: "Thanks be to God for his unspeakable gift!" KJV:
       "Thanks be unto God for his unspeakable gift." The ultimate
       gift (Christ) makes all other giving possible."""

notes[10] = """v.3  — NET: "the weapons of our warfare are not human weapons,
       but are made powerful by God for tearing down strongholds"
       — "strongholds" (ochyrOmatOn = fortifications). WEB: "the
       weapons of our warfare are not of the flesh, but mighty
       before God to the throwing down of strongholds." Spiritual
       warfare requires spiritual weapons.

v.4  — NET: "We tear down arguments" — "arguments" (logismous =
       reasonings/speculations). WEB: "throwing down imaginations."
       KJV: "Casting down imaginations." The battlefield is the
       mind — false ideologies and human reasoning opposed to God.

v.5  — NET: "and every arrogant obstacle that is raised up against
       the knowledge of God, and we take every thought captive to
       make it obey Christ" — "every thought captive" (pan noEma
       aichmalOtizontes). WEB: "bringing every thought into
       captivity to the obedience of Christ." Comprehensive mental
       discipline — no thought exempt from Christ's lordship.

v.10 — NET: "His letters are weighty and powerful, but his
       physical presence is weak and his speech is of no account"
       — the opponents' critique of Paul. WEB: "his bodily presence
       is weak, and his speech is despised." Paul may have had
       physical ailments and lacked rhetorical polish.

v.12 — NET: "we do not dare to classify or compare ourselves with
       some of those who recommend themselves" — "compare ourselves"
       (synkrinai heautous) — measuring ministry by comparison is
       foolish. WEB: "comparing themselves with themselves." Self-
       referential metrics produce self-deception."""

notes[11] = """v.2  — NET: "I am jealous for you with godly jealousy, because
       I promised you in marriage to one husband, to present you as
       a pure virgin to Christ" — "godly jealousy" (theou zElO =
       God's own jealousy). WEB: "a godly jealousy." Paul as
       spiritual father protecting his daughter for her Bridegroom.

v.4  — NET: "For if someone comes and proclaims another Jesus
       than the one we proclaimed" — "another Jesus" (allon IEsoun)
       — a counterfeit Christ. WEB: "preaches another Jesus." False
       teaching doesn't deny Jesus — it redefines Him.

v.14 — NET: "And no wonder, for even Satan disguises himself as an
       angel of light" — "disguises himself" (metaschEmatizesthai =
       transforms his appearance). WEB: "even Satan transforms
       himself into an angel of light." KJV: "Satan himself is
       transformed into an angel of light." The most dangerous
       deception looks most spiritual.

v.24 — NET: "Five times I received from the Jews forty lashes
       less one" — 39 lashes (the maximum without risking death).
       WEB: "Five times from the Jews I received forty stripes
       minus one." Paul endured this five times — 195 lashes total.
       None of these are recorded in Acts.

v.28 — NET: "Apart from other things, there is the daily pressure
       on me of my anxiety for all the churches" — "daily pressure"
       (epistasis... kath' hEmeran). WEB: "that which presses on
       me daily: anxiety for all the assemblies." The heaviest
       burden isn't physical — it's pastoral concern."""

notes[12] = """v.2  — NET: "I know a man in Christ who fourteen years ago...
       was caught up to the third heaven" — "the third heaven" =
       God's presence (first = atmosphere, second = space, third =
       God's dwelling). WEB: "caught up into the third heaven."
       Paul speaks of himself in third person out of humility.

v.4  — NET: "was caught up into paradise and heard things too
       sacred to be put into words" — "too sacred" (arrhEta
       rhEmata = inexpressible utterances). WEB: "unspeakable words."
       KJV: "unspeakable words, which it is not lawful for a man
       to utter." Some revelations are meant only for the recipient.

v.7  — NET: "a thorn in the flesh was given to me, a messenger
       of Satan to trouble me" — "thorn" (skolops = stake/splinter).
       WEB: "a thorn in the flesh." KJV: "a thorn in the flesh."
       Its exact nature is unknown — theories include: eye disease,
       malaria, epilepsy, opposition, or a speech impediment.

v.9  — NET: "My grace is sufficient for you, for my power is
       made perfect in weakness" — "made perfect" (teleitai =
       completed/reaches its goal). WEB: "My grace is sufficient
       for you, for my power is made perfect in weakness." KJV:
       "My grace is sufficient for thee: for my strength is made
       perfect in weakness." God's answer to Paul's three requests.

v.10 — NET: "when I am weak, then I am strong" — the great
       paradox. WEB: "when I am weak, then am I strong." KJV:
       "when I am weak, then am I strong." Human weakness becomes
       the venue for divine power — not despite weakness but
       THROUGH it."""

notes[13] = """v.5  — NET: "Put yourselves to the test to see if you are in
       the faith; examine yourselves!" — "examine" (dokimazete =
       test/prove/assay — metallurgical language). WEB: "Test your
       own selves, whether you are in the faith." Self-examination
       before accusing others.

v.4  — NET: "For he was crucified by reason of weakness, but he
       lives because of God's power. For we also are weak in him,
       but we will live together with him, because of God's power"
       — Christ's weakness (cross) led to power (resurrection).
       WEB: "he was crucified through weakness, yet he lives
       through the power of God." The pattern for apostolic ministry.

v.11 — NET: "Aim for restoration, heed my appeal, agree with one
       another, live in peace" — "aim for restoration" (katartizesthe
       = be mended/be put in order). WEB: "Be perfected." KJV:
       "Be perfect." Not sinless perfection but wholeness/maturity.

v.12 — NET: "Greet one another with a holy kiss" — "holy kiss"
       (philEmati hagiO) — a standard greeting in the early church,
       distinguishing Christian fellowship. WEB: "Greet one another
       with a holy kiss." Cultural form; the principle is warm,
       genuine affection among believers.

v.14 — NET: "The grace of the Lord Jesus Christ and the love of
       God and the fellowship of the Holy Spirit be with you all"
       — the fullest Trinitarian benediction in Scripture. WEB:
       "The grace of the Lord Jesus Christ, God's love, and the
       fellowship of the Holy Spirit be with you all." Three persons,
       three gifts: grace, love, fellowship."""


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
