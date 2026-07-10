#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to James, 1-2 Peter, 1-3 John, Jude."""
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

# James
james_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/20 - James"
james = dict()
james[1] = """v.2  — NET: "Consider it all joy, my brothers and sisters, when
       you encounter various trials" — "various" (poikilois =
       many-colored/diverse). WEB: "Count it all joy, my brothers,
       when you fall into various temptations." KJV: "divers
       temptations." Trials come in many varieties — each produces
       different aspects of maturity.

v.5  — NET: "God, who gives to all generously and without
       reprimand" — "without reprimand" (mE oneidizontos = without
       reproaching/shaming). WEB: "who gives to all liberally and
       without reproach." KJV: "upbraideth not." God doesn't shame
       us for asking — He gives without making us feel guilty.

v.14 — NET: "each one is tempted when he is lured and enticed by
       his own desires" — "lured and enticed" (exelkomenos kai
       deleazomenos = dragged away and baited — fishing metaphor).
       WEB: "drawn away by his own lust, and enticed." Our desires
       are both the bait and the hook.

v.17 — NET: "Every good and perfect gift is from above, coming
       down from the Father of lights" — "Father of lights"
       (patros tOn phOtOn = Father of luminaries/heavenly bodies).
       WEB: "the Father of lights." KJV: "the Father of lights."
       God created the stars and is Himself pure light — no shadow.

v.22 — NET: "But be sure you live out the message and do not
       merely listen to it" — "live out" (poiEtai logou = doers of
       the word). WEB: "be doers of the word." KJV: "be ye doers
       of the word." The central command of James — faith produces
       action or it is not real faith."""

james[2] = """v.1  — NET: "do not show prejudice" — "prejudice"
       (prosOpolEmpsiais = face-receiving/favoritism). WEB: "don't
       show partiality." KJV: "have not the faith... with respect
       of persons." Faith in Jesus and favoritism are incompatible
       — you cannot hold both simultaneously.

v.14 — NET: "What good is it, my brothers and sisters, if someone
       claims to have faith but does not have works?" — "claims"
       (legE = says). WEB: "if a man says he has faith." KJV: "if
       a man say he hath faith." The emphasis: SAYS vs. SHOWS.
       Verbal faith without visible works is suspect.

v.19 — NET: "You believe that God is one; well and good. Even the
       demons believe that — and tremble with fear" — "tremble"
       (phrissousin = shudder/have hair stand on end). WEB: "the
       demons also believe, and shudder." Even demons have correct
       theology — belief alone is not saving faith.

v.23 — NET: "Abraham believed God and it was credited to him as
       righteousness" — quoting Genesis 15:6 (same text Paul uses
       in Romans 4). WEB: "it was accounted to him as righteousness."
       James and Paul are not contradicting but complementing — Paul
       addresses the ground of justification; James addresses its
       evidence.

v.26 — NET: "as the body without the spirit is dead, so also
       faith without works is dead" — "without the spirit" (chOris
       pneumatos = apart from breath/spirit). WEB: "faith apart
       from works is dead." An analogy: works are to faith what
       breath is to the body — the evidence of life, not its cause."""

james[3] = """v.2  — NET: "For we all stumble in many ways" — "stumble"
       (ptaiomen = trip/fail/make mistakes). WEB: "For in many
       things we all stumble." KJV: "For in many things we offend
       all." James includes himself — tongue control is universal
       struggle. No one has mastered it.

v.6  — NET: "the tongue is a fire, the world of unrighteousness
       among our members" — "world of unrighteousness" (ho kosmos
       tEs adikias). WEB: "a world of iniquity." KJV: "a world of
       iniquity." The tongue contains an entire cosmos of evil —
       small in size, infinite in destructive capacity.

v.8  — NET: "But no human being can subdue the tongue" — "subdue"
       (damasai = tame — used of wild animals). WEB: "no man can
       tame the tongue." KJV: "the tongue can no man tame." We can
       tame lions and dolphins — but not the tongue. Only God can.

v.17 — NET: "the wisdom from above is first pure, then peaceable,
       gentle, accommodating, full of mercy and good fruit" —
       "accommodating" (eupeithEs = easily persuaded/open to
       reason). WEB: "gentle, reasonable." KJV: "easy to be
       intreated." Heavenly wisdom is not stubborn or combative.

v.18 — NET: "the fruit of righteousness is sown in peace among
       those who make peace" — "sown in peace" (en eirEnE speiretai).
       WEB: "the fruit of righteousness is sown in peace by those
       who make peace." Righteousness grows in peaceful conditions
       — conflict is infertile soil."""

james[4] = """v.2  — NET: "You desire and do not have; you murder and covet
       and are not able to obtain" — "murder" (phoneuete) — some
       manuscripts read "envy" (phthoneite). WEB: "You kill, and
       covet." KJV: "Ye kill, and desire to have." Whether literal
       murder or metaphorical is debated — James uses extreme
       language.

v.4  — NET: "Adulterers, do you not know that friendship with the
       world is hostility toward God?" — "Adulterers" (moichalides
       = adulteresses, feminine). WEB: "You adulteresses!" KJV:
       "Ye adulterers and adulteresses." The OT image of spiritual
       infidelity — Israel as God's unfaithful wife.

v.6  — NET: "God opposes the proud, but he gives grace to the
       humble" — quoting Proverbs 3:34 (LXX). "Opposes"
       (antitassetai = sets himself in battle array against). WEB:
       "God resists the proud." God actively resists the proud —
       military language.

v.7  — NET: "resist the devil and he will flee from you" —
       "resist" (antistEte = stand against/oppose). WEB: "Resist
       the devil, and he will flee from you." KJV: "Resist the
       devil, and he will flee from you." A promise: resistance
       produces retreat. The devil cannot endure determined opposition.

v.14 — NET: "you do not know about tomorrow. What is your life
       like?" — "What is your life?" (poia gar hE zOE hymOn).
       "You are a puff of smoke" (atmis = vapor/mist). WEB: "you
       are a vapor." KJV: "It is even a vapour." Life's brevity
       as morning mist — visible briefly, then gone."""

james[5] = """v.7  — NET: "Be patient, then, brothers and sisters, until the
       Lord's return" — "patient" (makrothymEsate = be long-
       tempered/endure without retaliation). WEB: "Be patient,
       therefore, brothers." KJV: "Be patient therefore, brethren."
       The farmer waits for rain — patience is not passive but
       purposeful waiting.

v.12 — NET: "do not swear, either by heaven or by earth or by any
       other oath. But let your 'Yes' be yes and your 'No' be no"
       — "let your yes be yes" (hEtO hymOn to nai nai). WEB: "let
       your 'yes' be 'yes'." Simple truthfulness removes the need
       for oaths — your word should be enough.

v.14 — NET: "Is anyone among you ill? He should call the elders
       of the church... and anoint him with oil in the name of the
       Lord" — "anoint" (aleipsantes = rubbing with oil). WEB:
       "anointing him with oil." KJV: "anointing him with oil."
       Whether medicinal (olive oil as medicine) or sacramental
       is debated — likely both.

v.16 — NET: "The prayer of a righteous person has great power in
       its effects" — "great power in its effects" (poly ischyei
       energoumenE = is strong when it works/is energized). WEB:
       "The insistent prayer of a righteous person is powerfully
       effective." KJV: "the effectual fervent prayer of a righteous
       man availeth much." Prayer that works is both fervent AND
       righteous.

v.20 — NET: "whoever turns a sinner back from his wandering path
       will save that person's soul from death and will cover a
       multitude of sins" — "cover a multitude of sins" (kalypsei
       plEthos hamartiOn). WEB: "will cover a multitude of sins."
       Whose sins? The sinner's? The rescuer's? Likely the
       converted sinner's — restoration through compassion."""

# 1 Peter
pet1_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/21 - 1 Peter"
pet1 = dict()
pet1[1] = """v.1  — NET: "those temporarily residing abroad... who are
       chosen" — "temporarily residing abroad" (parepidEmois
       diasopras = sojourners of the dispersion). WEB: "foreigners
       of the Dispersion." KJV: "strangers scattered." Believers
       as aliens — this world is not home.

v.7  — NET: "so that your faith, which is more precious than gold
       — gold that is tested by fire — may be found to result in
       praise" — "tested by fire" (dia pyros de dokimazomenou).
       WEB: "more precious than gold which perishes, even though
       it is tested by fire." Gold is refined by heat; faith by
       trials. Faith is MORE precious than refined gold.

v.12 — NET: "things angels long to catch a glimpse of" — "long
       to catch a glimpse" (epithymousin parakupsai = desire to
       stoop down and peer into). WEB: "which things angels desire
       to look into." KJV: "which things the angels desire to look
       into." Angels crane forward to see — the gospel amazes even
       heavenly beings.

v.18 — NET: "you were redeemed... not by perishable things like
       silver or gold" — "redeemed" (elytrOthEte = ransomed/freed
       by payment). WEB: "knowing that you were redeemed." KJV:
       "ye were not redeemed with corruptible things." The cost of
       freedom: not money but blood (v.19).

v.23 — NET: "you have been born anew, not from perishable but
       from imperishable seed, through the living and enduring word
       of God" — "imperishable seed" (sporas aphthartou). WEB:
       "having been born again... of incorruptible seed." KJV:
       "being born again... by the word of God." The seed that
       causes new birth cannot decay."""

pet1[2] = """v.2  — NET: "Like newborn babies, crave pure spiritual milk" —
       "crave" (epipothEsate = long intensely for/desire eagerly).
       WEB: "as newborn babies, long for the pure milk of the Word."
       KJV: "desire the sincere milk of the word." The analogy: a
       baby's instinctive, urgent desire for milk.

v.5  — NET: "you yourselves, as living stones, are built up as a
       spiritual house" — "living stones" (lithoi zOntes). WEB:
       "you also, as living stones, are built up as a spiritual
       house." Each believer is a living stone in God's temple —
       corporate, not individualistic.

v.9  — NET: "But you are a chosen race, a royal priesthood, a
       holy nation, a people of his own" — four OT Israel titles
       now applied to the church. WEB: "a royal priesthood." KJV:
       "a royal priesthood." All believers are priests — no special
       class mediates between laity and God.

v.21 — NET: "Christ also suffered for you, leaving an example for
       you to follow in his steps" — "example" (hypogrammon = a
       writing pattern for children to trace). WEB: "leaving you
       an example, that you should follow his steps." KJV: "leaving
       us an example." Like tracing paper — we follow His pattern.

v.24 — NET: "He himself bore our sins in his body on the tree" —
       "bore" (anEnegken = carried up/offered up). WEB: "who his
       own self bore our sins in his body on the tree." KJV: "Who
       his own self bare our sins." Sacrificial language — He
       carried sins as a priest carries an offering to the altar."""

pet1[3] = """v.4  — NET: "the hidden person of the heart, the imperishable
       quality of a gentle and quiet spirit" — "imperishable"
       (aphthartO = incorruptible/undecaying). WEB: "in the
       incorruptible adornment of a gentle and quiet spirit." True
       beauty is internal and eternal — it doesn't fade with age.

v.15 — NET: "always be ready to give an answer to anyone who asks
       about the hope you possess" — "answer" (apologian = defense/
       reasoned explanation). WEB: "always be ready to give an
       answer." KJV: "be ready always to give an answer." Not
       aggressive argument but prepared, gentle explanation (v.16:
       "with gentleness and respect").

v.18 — NET: "Christ also suffered once for sins, the just for the
       unjust" — "once" (hapax = once for all, unrepeatable). WEB:
       "Christ also suffered for sins once, the righteous for the
       unrighteous." The finality and sufficiency of Christ's one
       sacrifice — never to be repeated.

v.19 — NET: "he went and preached to the spirits in prison" —
       "spirits in prison" (tois en phylakE pneumasin) — one of
       the most debated passages in the NT. WEB: "he went and
       preached to the spirits in prison." Who, when, what, and
       where are all debated. Context suggests Noah's generation.

v.21 — NET: "Baptism... now saves you — not the washing off of
       physical dirt but the pledge of a good conscience to God" —
       "pledge" (eperOtEma = appeal/answer/commitment). WEB: "the
       interrogation of a good conscience toward God." KJV: "the
       answer of a good conscience toward God." Baptism saves as a
       pledge/response — not the water but what it represents."""

pet1[4] = """v.1  — NET: "arm yourselves with the same attitude, because the
       one who has suffered in the flesh has finished with sin" —
       "arm yourselves" (hoplisasthe = take up weapons/equip for
       battle). WEB: "arm yourselves also with the same mind." KJV:
       "arm yourselves likewise with the same mind." Christ's
       suffering-mindset as spiritual weaponry.

v.8  — NET: "Above all keep your love for one another fervent,
       because love covers a multitude of sins" — "fervent"
       (ektenE = stretched out/strained/intense). WEB: "above all
       things being fervent in your love among yourselves." KJV:
       "have fervent charity among yourselves." Love stretched to
       its limit — not casual but intense.

v.12 — NET: "do not be surprised at the fiery ordeal among you...
       as though something strange were happening" — "fiery ordeal"
       (pyrOsei = burning/smelting). WEB: "don't be astonished at
       the fiery trial." Suffering is normal, not exceptional —
       the surprise would be its absence.

v.14 — NET: "If you are insulted for the name of Christ, you are
       blessed, because the Spirit of glory and of God rests on
       you" — "Spirit of glory" (to tEs doxEs kai to tou theou
       pneuma). WEB: "the Spirit of glory and of God rests on you."
       Suffering for Christ brings special divine presence.

v.17 — NET: "For it is time for judgment to begin, starting with
       the house of God" — "starting with" (arxamenon apo). WEB:
       "the time has come for judgment to begin at the house of
       God." KJV: "judgment must begin at the house of God." God
       judges His own first — greater privilege, greater
       accountability."""

pet1[5] = """v.2  — NET: "shepherd the flock of God among you, exercising
       oversight not by compulsion but willingly" — "shepherd"
       (poimanate = tend/pastor/feed). WEB: "Shepherd the flock of
       God which is among you." KJV: "Feed the flock of God." Three
       contrasts: not compulsion but willing, not greed but eager,
       not domineering but exemplary.

v.5  — NET: "clothe yourselves with humility toward one another"
       — "clothe yourselves" (enkombOsasthe = tie on like an apron/
       slave's garment). WEB: "be clothed with humility." KJV:
       "be clothed with humility." The rare word may echo Jesus
       tying on a towel to wash feet (John 13).

v.7  — NET: "by casting all your cares on him because he cares
       for you" — "casting" (epirripsantes = throwing upon — a
       decisive action). WEB: "casting all your worries on him."
       KJV: "Casting all your care upon him." An active throwing —
       not gently placing but hurling your anxieties onto God.

v.8  — NET: "your adversary the devil prowls around like a
       roaring lion, looking for someone to devour" — "prowls"
       (peripatei = walks about). "Devour" (katapiein = swallow
       whole). WEB: "the devil, walks around like a roaring lion,
       seeking whom he may devour." A predator seeking isolated,
       weakened prey.

v.10 — NET: "after you have suffered for a little while, the God
       of all grace... will himself restore, confirm, strengthen,
       and establish you" — four verbs of divine action: restore
       (katartisei), confirm (stErixei), strengthen (sthenOsei),
       establish (themeliOsei). WEB: "restore, confirm, strengthen,
       and establish you." God Himself does the rebuilding."""

# 2 Peter
pet2_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/22 - 2 Peter"
pet2 = dict()
pet2[1] = """v.3  — NET: "His divine power has bestowed on us everything
       necessary for life and godliness" — "everything necessary"
       (panta... ta pros zOEn). WEB: "seeing that his divine power
       has granted to us all things." KJV: "all things that pertain
       unto life and godliness." Complete provision — nothing
       lacking for spiritual life.

v.4  — NET: "precious and most magnificent promises, so that
       through them you may become partakers of the divine nature"
       — "partakers of divine nature" (theias koinOnoi physeOs).
       WEB: "partakers of the divine nature." KJV: "partakers of
       the divine nature." Not becoming God but sharing in His
       moral character — the Eastern church's concept of theosis.

v.5  — NET: "make every effort to supplement your faith with
       excellence" — "supplement" (epichorEgEsate = supply/furnish
       generously). WEB: "adding on your part all diligence." A
       chain of virtues: faith, virtue, knowledge, self-control,
       perseverance, godliness, brotherly love, love.

v.19 — NET: "we possess the prophetic word as an altogether
       reliable thing" — "altogether reliable" (bebaioteron =
       more sure/more confirmed). WEB: "the more sure word of
       prophecy." KJV: "a more sure word of prophecy." Scripture
       is more reliable than even eyewitness experiences (v.18 —
       the Transfiguration).

v.21 — NET: "men spoke from God as they were carried along by the
       Holy Spirit" — "carried along" (pheromenoi = borne/moved —
       same word for a ship driven by wind). WEB: "moved by the
       Holy Spirit." KJV: "moved by the Holy Ghost." Human authors
       carried by divine wind — not dictation but organic
       inspiration."""

pet2[2] = """v.1  — NET: "there will be false teachers among you. They will
       bring in destructive opinions" — "destructive opinions"
       (haireseis apOleias = heresies of destruction). WEB:
       "destructive heresies." KJV: "damnable heresies." False
       teaching smuggled in secretly — not overt but subtle
       introduction.

v.4  — NET: "God did not spare the angels who sinned, but threw
       them into hell and locked them up" — "threw into hell"
       (tartarOsas = cast into Tartarus — the only NT use). WEB:
       "cast them down to Tartarus." KJV: "cast them down to hell."
       Tartarus was Greek mythology's deepest pit — Peter uses it
       for the angels' prison.

v.5  — NET: "he did not spare the ancient world, but did protect
       Noah, a herald of righteousness" — "herald" (kEryka =
       preacher/proclaimer). WEB: "a preacher of righteousness."
       KJV: "a preacher of righteousness." Noah preached repentance
       for 120 years while building — no one listened.

v.9  — NET: "the Lord knows how to rescue the godly from their
       trials" — "rescue" (rhyesthai = deliver/extract from danger).
       WEB: "the Lord knows how to deliver the godly out of
       temptation." KJV: "the Lord knoweth how to deliver the
       godly out of temptations." God's ability is proven by
       history (Noah, Lot).

v.22 — NET: "A dog returns to its own vomit" — quoting Proverbs
       26:11. WEB: "The dog turns to his own vomit again." KJV:
       "The dog is turned to his own vomit again." False teachers
       who tasted freedom but returned to corruption — nature
       reasserts itself without genuine transformation."""

pet2[3] = """v.8  — NET: "with the Lord one day is like a thousand years
       and a thousand years are like one day" — quoting Psalm 90:4.
       WEB: "one day is with the Lord as a thousand years, and a
       thousand years as one day." God operates outside human time
       — what seems like delay is divine patience.

v.9  — NET: "The Lord is not slow concerning his promise, as some
       regard slowness, but is being patient toward you because he
       does not wish for any to perish" — "does not wish" (mE
       boulomenos = not wanting/not purposing). WEB: "not wishing
       that anyone should perish." KJV: "not willing that any
       should perish." God's patience has a redemptive purpose.

v.10 — NET: "the day of the Lord will come like a thief" —
       "like a thief" (hOs kleptEs) — unexpected timing. WEB:
       "the day of the Lord will come as a thief in the night."
       "The heavens will disappear with a rushing sound" (rhoizEdon
       = with a roar/whizzing). KJV: "with a great noise." Cosmic
       dissolution — elements melting.

v.13 — NET: "we are waiting for new heavens and a new earth, in
       which righteousness truly resides" — "truly resides"
       (dikaiosynE katoikei = righteousness dwells/is at home).
       WEB: "new heavens and a new earth, in which righteousness
       dwells." Righteousness will be the atmosphere of the new
       creation — evil permanently excluded.

v.18 — NET: "grow in the grace and knowledge of our Lord and
       Savior Jesus Christ" — "grow" (auxanete = increase). WEB:
       "grow in the grace and knowledge of our Lord and Savior
       Jesus Christ." The letter's final command: keep growing.
       Stagnation is dangerous (ch.2); growth is the alternative."""

# 1 John
john1_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/23 - 1 John"
john1 = dict()
john1[1] = """v.1  — NET: "what existed from the beginning, what we have
       heard, what we have seen with our eyes" — four verbs of
       firsthand experience: heard, seen, observed, touched. WEB:
       "that which was from the beginning, that which we have
       heard." KJV: "That which was from the beginning." John
       stresses physical, sensory witness against Gnostic denial.

v.3  — NET: "so that you may have fellowship with us (and indeed
       our fellowship is with the Father and with his Son)" —
       "fellowship" (koinOnia = shared participation/partnership).
       WEB: "our fellowship is with the Father, and with his Son."
       Horizontal fellowship is grounded in vertical fellowship.

v.5  — NET: "God is light, and in him there is no darkness at
       all" — "no darkness at all" (skotia en autO ouk estin
       oudemia = double negative for emphasis). WEB: "in him is no
       darkness at all." Absolute moral purity — zero shadow.

v.7  — NET: "if we walk in the light as he himself is in the
       light, we have fellowship with one another" — "walk in the
       light" (en tO phOti peripatOmen). WEB: "walk in the light."
       Walking = ongoing lifestyle. Light = transparency/holiness.
       Result = genuine community AND cleansing (v.7b).

v.9  — NET: "he is faithful and righteous, forgiving us our sins
       and cleansing us from all unrighteousness" — "faithful and
       righteous" (pistos... dikaios) — forgiveness is not mercy
       contradicting justice but justice fulfilled through Christ.
       WEB: "faithful and righteous to forgive." God is JUST in
       forgiving because Christ paid."""

john1[2] = """v.1  — NET: "we have an advocate with the Father, Jesus Christ
       the righteous one" — "advocate" (paraklEton = one called
       alongside/intercessor). WEB: "we have a Counselor with the
       Father." KJV: "we have an advocate with the Father." Same
       word Jesus used for the Spirit (John 14:16) — now applied
       to Himself.

v.2  — NET: "he himself is the atoning sacrifice for our sins" —
       "atoning sacrifice" (hilasmos = propitiation/expiation). WEB:
       "the atoning sacrifice for our sins." KJV: "the propitiation
       for our sins." Does God's wrath need appeasing (propitiation)
       or sin need covering (expiation)? The word includes both.

v.15 — NET: "Do not love the world or the things in the world" —
       "love" (agapate = don't set your affection on). WEB: "Don't
       love the world." KJV: "Love not the world." Not creation
       or people (John 3:16) but the world-SYSTEM opposed to God.

v.18 — NET: "just as you heard that the antichrist is coming, so
       now many antichrists have appeared" — "many antichrists"
       (antichristoi polloi). WEB: "many antichrists have arisen."
       The spirit of antichrist manifests in many opponents before
       the final Antichrist — a present reality, not just future.

v.27 — NET: "the anointing that you received from him resides in
       you, and you have no need for anyone to teach you" — 
       "anointing" (chrisma = unction). WEB: "the anointing which
       you received from him remains in you." The Holy Spirit's
       internal teaching — not rejecting human teachers but
       affirming the Spirit's authority."""

john1[3] = """v.1  — NET: "See what sort of love the Father has given to us:
       that we should be called God's children" — "what sort"
       (potapEn = what country/what kind — amazement at its foreign
       quality). WEB: "See how great a love the Father has given to
       us." KJV: "Behold, what manner of love." This love is
       otherworldly — it doesn't originate on earth.

v.2  — NET: "when he is revealed we will be like him, because we
       will see him just as he is" — "like him" (homoioi autO).
       WEB: "we will be like him; for we will see him just as he
       is." Seeing produces becoming — the beatific vision
       transforms the viewer.

v.9  — NET: "Everyone who has been fathered by God does not
       practice sin" — "practice sin" (hamartian ou poiei = does
       not keep on sinning). WEB: "Whoever is born of God doesn't
       commit sin." KJV: "doth not commit sin." The present tense
       indicates habitual practice — not sinless perfection but a
       changed pattern of life.

v.14 — NET: "We know that we have crossed over from death to life
       because we love our fellow Christians" — "crossed over"
       (metabebEkamen = have transferred/migrated). WEB: "We know
       that we have passed out of death into life." KJV: "We know
       that we have passed from death unto life." Perfect tense —
       a completed transfer with present results.

v.16 — NET: "We have come to know love by this: that Jesus laid
       down his life for us" — "laid down" (ethEken = placed/set
       down deliberately). WEB: "he laid down his life for us."
       Love defined by action, not emotion — self-sacrificial
       giving is the measure."""

john1[4] = """v.1  — NET: "do not believe every spirit, but test the spirits
       to determine if they are from God" — "test" (dokimazete =
       examine/prove/assay). WEB: "test the spirits." KJV: "try
       the spirits." Discernment is commanded, not optional —
       gullibility is not a fruit of the Spirit.

v.8  — NET: "The one who does not love does not know God, because
       God is love" — "God is love" (ho theos agapE estin). WEB:
       "God is love." KJV: "God is love." Not "love is God" (making
       love ultimate) but "God is love" (love defined by God's
       character). God defines love, not the reverse.

v.10 — NET: "In this is love: not that we have loved God, but
       that he loved us and sent his Son to be the atoning
       sacrifice for our sins" — love's definition: God's initiative,
       not our response. WEB: "sent his Son to be the atoning
       sacrifice." Love originates with God, not with us.

v.18 — NET: "There is no fear in love, but perfect love drives
       out fear" — "drives out" (ballei = throws out/casts out —
       violent expulsion). WEB: "perfect love casts out fear." KJV:
       "perfect love casteth out fear." Love and fear cannot coexist
       — God's love evicts our terror of judgment.

v.19 — NET: "We love because he first loved us" — "he first
       loved" (autos prOtos EgapEsen). WEB: "We love him, because
       he first loved us." Some manuscripts include "him" (KJV/WEB);
       others have just "we love" (NET/ESV). Either way: God's
       love precedes and enables ours."""

john1[5] = """v.3  — NET: "For this is the love of God: that we keep his
       commandments. And his commandments do not weigh us down" —
       "do not weigh us down" (bareiai ouk eisin = are not heavy/
       burdensome). WEB: "his commandments are not grievous." KJV:
       "his commandments are not grievous." Obedience is not
       oppressive for the born-again — love makes duty light.

v.4  — NET: "this is the conquering power that has conquered the
       world: our faith" — "conquering power" (nikE = victory).
       WEB: "this is the victory that has overcome the world: our
       faith." KJV: "this is the victory that overcometh the world,
       even our faith." Faith IS the victory — not produces it
       but IS it.

v.7  — NET: "For there are three that testify" — the longer
       reading (Comma Johanneum: "in heaven, the Father, the Word,
       and the Holy Ghost") is found in KJV but NOT in NET/ESV/WEB/
       ASV. It is absent from all Greek manuscripts before the 16th
       century. NET omits it following all early manuscript evidence.

v.13 — NET: "I have written these things to you who believe in
       the name of the Son of God so that you may know that you
       have eternal life" — "that you may KNOW" (hina eidEte =
       that you may have settled knowledge). WEB: "that you may
       know that you have eternal life." Assurance is possible and
       intended — John writes for certainty, not doubt.

v.21 — NET: "Little children, guard yourselves from idols" —
       "guard yourselves" (phylaxate heauta = keep/protect
       yourselves). WEB: "Little children, keep yourselves from
       idols." KJV: "Little children, keep yourselves from idols."
       The abrupt ending — the opposite of loving God is idolatry.
       A final warning."""

# 2 John
john2_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/24 - 2 John"
john2 = dict()
john2[1] = """v.1  — NET: "To the elect lady and her children, whom I love
       in truth" — "elect lady" (eklektE kyria) — debated: a
       specific woman or a church personified? WEB: "the chosen
       lady." KJV: "the elect lady." If a church, "her children"
       are its members; "her sister" (v.13) is another church.

v.7  — NET: "many deceivers have gone out into the world, people
       who do not confess Jesus as Christ coming in the flesh" —
       "coming in the flesh" (erchomenon en sarki = present
       participle). WEB: "who don't confess that Jesus Christ came
       in the flesh." The incarnation as the test of orthodoxy —
       deny it and you have "the deceiver and the antichrist."

v.8  — NET: "Watch out, so that you do not lose the things we
       have worked for" — "worked for" (eirgasametha). WEB: "Watch
       yourselves, that we don't lose the things which we have
       accomplished." KJV: "that we lose not those things which we
       have wrought." Progress can be lost — vigilance required.

v.9  — NET: "Everyone who goes on ahead and does not remain in
       the teaching of Christ does not have God" — "goes on ahead"
       (proagOn = progresses beyond). WEB: "Whoever transgresses
       and doesn't remain in the teaching of Christ." "Progress"
       beyond Christ's teaching is actually regress — departure
       from God.

v.10 — NET: "do not receive him into your house and do not give
       him any greeting" — "greeting" (chairein = rejoice/welcome).
       WEB: "don't receive him into your house, and don't welcome
       him." Hospitality to false teachers = partnership in their
       deception (v.11). Not rude but protective."""

# 3 John
john3_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/25 - 3 John"
john3 = dict()
john3[1] = """v.2  — NET: "I pray that all may go well with you and that you
       may be in good health, just as it is well with your soul" —
       "go well" (euodousthai = prosper/succeed). WEB: "I pray that
       you may prosper in all things and be healthy." KJV: "I wish
       above all things that thou mayest prosper and be in health."
       A standard greeting, not a health-wealth promise.

v.4  — NET: "I have no greater joy than this: to hear that my
       children are living according to the truth" — "living
       according to the truth" (en alEtheia peripatounta = walking
       in truth). WEB: "to hear of my children walking in truth."
       The aged apostle's greatest joy — spiritual faithfulness.

v.7  — NET: "For they went out for the sake of the Name,
       accepting nothing from the Gentiles" — "the Name" (tou
       onomatos = THE name — Jesus). WEB: "for the sake of the
       Name." KJV: "for his name's sake." Missionaries who refuse
       support from unbelievers to maintain integrity.

v.9  — NET: "Diotrephes, who loves to be first among them, does
       not acknowledge us" — "loves to be first" (ho philoprOteuOn
       = the one loving preeminence). WEB: "Diotrephes, who loves
       to be first among them." A one-word character diagnosis:
       lover of first place. Authority addiction.

v.11 — NET: "Dear friend, do not imitate what is bad but what is
       good. The one who does good is of God; the one who does
       what is bad has not seen God" — "imitate" (mimou = mimic/
       copy). WEB: "Don't imitate that which is evil, but that
       which is good." Two models: Diotrephes (bad) and Demetrius
       (good). Choose your example wisely."""

# Jude
jude_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/26 - Jude"
jude = dict()
jude[1] = """v.3  — NET: "I now feel compelled instead to write to encourage
       you to contend earnestly for the faith" — "contend earnestly"
       (epagOnizesthai = fight strenuously/agonize for). WEB:
       "to contend earnestly for the faith." KJV: "earnestly
       contend for the faith." Athletic/military intensity —
       THE faith (body of doctrine) needs active defense.

v.4  — NET: "certain men have secretly slipped in among you" —
       "secretly slipped in" (pareisedysan = crept in sideways/
       infiltrated). WEB: "there are certain men who crept in
       secretly." KJV: "certain men crept in unawares." They
       didn't announce themselves — stealth entry into the church.

v.9  — NET: "Michael the archangel, when he argued with the devil
       and disputed about the body of Moses, did not dare to bring
       a slandering judgment" — "did not dare" (ouk etolmEsen =
       did not presume). WEB: "dared not bring against him a
       railing judgment." Even an archangel defers to God in
       dealing with Satan — unlike the false teachers (v.10).

v.14 — NET: "Enoch, the seventh from Adam, prophesied about them"
       — Jude quotes 1 Enoch (an apocryphal book). WEB: "Enoch,
       the seventh from Adam, also prophesied." Quoting a non-
       canonical source does not canonize it — Paul quoted pagan
       poets (Acts 17:28; Titus 1:12) the same way.

v.24 — NET: "Now to the one who is able to keep you from falling,
       and to cause you to stand, without blemish, in joyful
       exultation, before his glorious presence" — "keep from
       falling" (phylaxai aptaistous = guard without stumbling).
       WEB: "able to keep you from stumbling." KJV: "able to keep
       you from falling." God's preserving power — the final
       doxology and the book's crowning promise."""

# Process all
for ch, note_text in sorted(james.items()):
    fp = os.path.join(james_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done James " + str(ch))

for ch, note_text in sorted(pet1.items()):
    fp = os.path.join(pet1_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done 1 Peter " + str(ch))

for ch, note_text in sorted(pet2.items()):
    fp = os.path.join(pet2_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done 2 Peter " + str(ch))

for ch, note_text in sorted(john1.items()):
    fp = os.path.join(john1_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done 1 John " + str(ch))

for ch, note_text in sorted(john2.items()):
    fp = os.path.join(john2_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done 2 John " + str(ch))

for ch, note_text in sorted(john3.items()):
    fp = os.path.join(john3_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done 3 John " + str(ch))

for ch, note_text in sorted(jude.items()):
    fp = os.path.join(jude_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(fp) and add_additional_notes(fp, note_text):
        print("  done Jude " + str(ch))
