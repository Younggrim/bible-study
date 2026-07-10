#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Romans chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/06 - Romans"

notes = dict()
notes[1] = """v.1  — NET: "called to be an apostle, set apart for the gospel
       of God" — "set apart" (aphorismenos) echoes Paul's Pharisee
       identity (pharisaios = separated one). WEB: "set apart for
       the Good News of God." He was separated FOR something, not
       just FROM something.

v.16 — NET: "For I am not ashamed of the gospel, for it is God's
       power for salvation to everyone who believes, to the Jew
       first and also to the Greek" — "God's power" (dynamis theou).
       WEB: "the power of God for salvation." KJV: "the power of
       God unto salvation." The gospel IS power, not just describes it.

v.17 — NET: "the righteousness of God is revealed in the gospel
       from faith to faith" — "from faith to faith" (ek pisteOs
       eis pistin) is debated. WEB: "from faith to faith." ASV:
       "from faith unto faith." NET preserves the ambiguity — faith
       as starting point AND destination.

v.25 — NET: "They exchanged the truth of God for a lie and
       worshiped and served the creation rather than the Creator"
       — "the creation rather than the Creator" makes the absurdity
       explicit. WEB: "served the creature rather than the Creator."
       KJV: "served the creature more than the Creator."

v.28 — NET: "God gave them over to a depraved mind, to do what
       should not be done" — "depraved mind" (adokimon noun = a
       mind that fails the test). WEB: "a reprobate mind." KJV:
       "a reprobate mind." There is wordplay in Greek: they did not
       approve (edokimasan) God, so God gave them an unapproved
       (adokimon) mind."""

notes[2] = """v.4  — NET: "do you not realize that God's kindness leads you
       to repentance?" — "leads" (agei = actively draws/guides).
       WEB: "the goodness of God leads you to repentance." KJV:
       "the goodness of God leadeth thee to repentance." God's
       kindness is not passive tolerance but active invitation.

v.11 — NET: "For there is no partiality with God" — "partiality"
       (prosOpolEmpsia = face-receiving/favoritism). WEB: "For
       there is no partiality with God." ASV: "for there is no
       respect of persons with God." KJV: "no respect of persons."
       God doesn't evaluate externals.

v.14 — NET: "For whenever the Gentiles, who do not have the law,
       do by nature the things required by the law" — "by nature"
       (physei) — the moral law written on conscience. WEB: "do by
       nature the things of the law." Gentiles have an internal
       witness even without Sinai.

v.16 — NET: "on the day when God will judge the secrets of people,
       according to my gospel, through Christ Jesus" — "the secrets
       of people" (ta krypta tOn anthrOpOn). WEB: "the secrets of
       men." Nothing hidden will remain so. KJV: "the secrets of
       men by Jesus Christ."

v.29 — NET: "but someone who is a Jew inwardly; and circumcision
       is of the heart, by the Spirit and not by the written code"
       — "by the Spirit" (en pneumati) — the true mark is spiritual,
       not physical. WEB: "in the spirit, not in the letter." KJV:
       "in the spirit, and not in the letter." Inner reality over
       outward ritual."""

notes[3] = """v.10 — NET: "There is no one righteous, not even one" — Paul
       begins a catena of OT quotations (Psalms, Isaiah, Ecclesiastes).
       WEB: "There is no one righteous; no, not one." KJV: "There
       is none righteous, no, not one." The universal indictment.

v.21 — NET: "But now apart from the law the righteousness of God
       has been disclosed" — "disclosed" (pephanerOtai = made
       manifest/revealed). WEB: "a righteousness of God has been
       revealed." KJV: "the righteousness of God without the law
       is manifested." A new era: righteousness available without
       law-keeping.

v.24 — NET: "justified freely by his grace through the redemption
       that is in Christ Jesus" — "freely" (dOrean = as a gift/
       without cause). WEB: "being justified freely by his grace."
       KJV: "justified freely by his grace." We contribute nothing
       to our justification.

v.25 — NET: "God publicly displayed him at his death as the mercy
       seat accessible through faith" — "mercy seat" (hilastErion)
       — the lid of the Ark where blood was sprinkled on Atonement
       Day. KJV: "propitiation." WEB: "a sacrifice of atonement."
       NET's rendering connects Christ directly to the Day of
       Atonement imagery.

v.28 — NET: "For we consider that a person is declared righteous
       by faith apart from the works of the law" — "declared
       righteous" (dikaiousthai) — forensic/legal declaration.
       WEB: "justified by faith apart from the works of the law."
       KJV: "justified by faith without the deeds of the law."
       Luther's sola fide finds its primary text here."""

notes[4] = """v.3  — NET: "Abraham believed God, and it was credited to him
       as righteousness" — "credited" (elogisthE = counted/reckoned
       to his account). WEB: "it was accounted to him for
       righteousness." KJV: "it was counted unto him for
       righteousness." Accounting language — deposited to his
       ledger by God.

v.5  — NET: "his faith is credited as righteousness" — the one
       who does NOT work but BELIEVES. WEB: "his faith is accounted
       for righteousness." The paradox: the non-worker receives
       the worker's reward. Faith receives what it cannot earn.

v.17 — NET: "the God who makes the dead alive and summons the
       things that do not yet exist as though they already do" —
       "summons things that do not yet exist" (kalountos ta mE
       onta hOs onta). WEB: "calls the things that are not, as
       though they were." KJV: "calleth those things which be not
       as though they were." God's creative word.

v.19 — NET: "he did not weaken in faith, contemplating his own
       body which was already dead" — "already dead" (nenekrOmenon
       = having been made dead/impotent). WEB: "his own body, now
       as good as dead." KJV: "his own body now dead." Abraham was
       ~100 years old — biologically hopeless.

v.25 — NET: "He was given over because of our transgressions and
       was raised for the sake of our justification" — "for the
       sake of our justification" (dia tEn dikaiOsin hEmOn). WEB:
       "raised for our justification." KJV: "raised again for our
       justification." The resurrection proves the sacrifice was
       accepted — justification confirmed."""

notes[5] = """v.1  — NET: "we have peace with God through our Lord Jesus
       Christ" — textual variant: "we have" (echomen, indicative)
       vs. "let us have" (echOmen, subjunctive). NET/KJV/WEB take
       it as indicative (a fact). ASV: "let us have" (hortatory).
       The difference: statement of reality vs. exhortation.

v.5  — NET: "because the love of God has been poured out in our
       hearts through the Holy Spirit who was given to us" —
       "poured out" (ekkechytai = lavished/flooded). WEB: "the
       love of God has been poured into our hearts." KJV: "the
       love of God is shed abroad in our hearts." Not a trickle
       but a flood.

v.8  — NET: "God demonstrates his own love for us, in that while
       we were still sinners, Christ died for us" — "demonstrates"
       (synistEsin = commends/proves/establishes). WEB: "God
       commends his own love toward us." KJV: "God commendeth his
       love toward us." The cross is the permanent proof of love.

v.12 — NET: "just as sin entered the world through one man and
       death through sin, and so death spread to all people
       because all sinned" — "because all sinned" (eph' hO pantes
       hEmarton) — the most debated phrase. WEB: "for that all
       sinned." KJV: "for that all have sinned." How did all sin
       in Adam? Debate continues.

v.20 — NET: "where sin increased, grace multiplied all the more"
       — "multiplied all the more" (hyperperisseusen = super-
       abounded). WEB: "grace abounded more exceedingly." KJV:
       "grace did much more abound." Grace always outpaces sin —
       the greater the sin, the greater the display of grace."""

notes[6] = """v.2  — NET: "How can we who died to sin still live in it?" —
       the logical impossibility of continuing in sin after dying
       to it. WEB: "How could we, who died to sin, live in it any
       longer?" KJV: "How shall we, that are dead to sin, live any
       longer therein?" The answer is assumed: we cannot.

v.4  — NET: "we have been buried with him through baptism into
       death" — "buried with" (syntaphEmen) — baptism as
       participation in Christ's death. WEB: "buried with him
       through baptism into death." KJV: "buried with him by
       baptism into death." Union with Christ in His death AND
       resurrection.

v.6  — NET: "our old man was crucified with him so that the body
       of sin would no longer dominate us" — "dominate" (douleuein
       = enslave). WEB: "that we would no longer be in bondage to
       sin." KJV: "that henceforth we should not serve sin." The
       old self is executed, not reformed.

v.14 — NET: "sin will not be master over you, for you are not
       under law but under grace" — "master" (kyrieusei = lord it
       over). WEB: "sin will not have dominion over you." KJV:
       "sin shall not have dominion over you." Grace doesn't
       permit sin — it BREAKS sin's reign.

v.23 — NET: "For the payoff of sin is death, but the gift of God
       is eternal life in Christ Jesus our Lord" — "payoff"
       (opsOnia = wages/soldier's pay). WEB: "the wages of sin is
       death." KJV: "the wages of sin is death." Sin pays what it
       owes — death. God gives what we don't deserve — life."""

notes[7] = """v.7  — NET: "Is the law sin? Absolutely not!" — "Absolutely
       not!" (mE genoito = may it never be!). KJV: "God forbid."
       WEB: "May it never be!" ASV: "God forbid." Paul's strongest
       denial — the law reveals sin but is not itself sinful.

v.14 — NET: "For we know that the law is spiritual — but I am
       unspiritual, sold into slavery to sin" — "unspiritual"
       (sarkinos = fleshly/made of flesh). WEB: "but I am fleshly,
       sold under sin." KJV: "I am carnal, sold under sin." The
       law is spiritual; the problem is in US, not in the law.

v.15 — NET: "For I don't understand what I am doing. For I do not
       do what I want — instead, I do what I hate" — "don't
       understand" (ou ginOskO = don't comprehend/acknowledge). WEB:
       "For I don't know what I am doing." KJV: "that which I do I
       allow not." The divided self — wanting good but doing evil.

v.18 — NET: "For I know that nothing good lives in me, that is,
       in my flesh" — "in my flesh" is Paul's qualifier. WEB:
       "that is, in my flesh." KJV: "that is, in my flesh." The
       indwelling Spirit IS good; the flesh is the problem domain.

v.24 — NET: "Wretched man that I am! Who will rescue me from this
       body of death?" — "wretched" (talaipOros = miserable/
       exhausted from the struggle). WEB: "What a wretched man I
       am!" KJV: "O wretched man that I am!" The cry of genuine
       desperation that leads to the answer: "Jesus Christ our
       Lord" (v.25)."""

notes[8] = """v.1  — NET: "There is therefore now no condemnation for those
       who are in Christ Jesus" — "no condemnation" (ouden katakrima)
       — a legal verdict: NOT GUILTY. WEB: "There is therefore now
       no condemnation to those who are in Christ Jesus." Some
       manuscripts add "who walk not after the flesh" — NET/ESV omit
       this as likely imported from v.4.

v.15 — NET: "you received the Spirit of adoption, by whom we cry
       'Abba, Father'" — "adoption" (huiothesias = placement as
       sons). WEB: "the Spirit of adoption." KJV: "the Spirit of
       adoption." Not just forgiveness but FAMILY — full rights as
       heirs. "Abba" = Aramaic intimate address for father.

v.26 — NET: "the Spirit himself intercedes for us with inexpressible
       groanings" — "inexpressible groanings" (stenagmois
       alalEtois = wordless/unspeakable groans). WEB: "with
       groanings which can't be uttered." KJV: "with groanings
       which cannot be uttered." Prayer beyond language.

v.28 — NET: "And we know that all things work together for good
       for those who love God" — "work together" (synergei = co-
       operate). WEB: "all things work together for good." KJV:
       "all things work together for good." Not that all things
       ARE good, but that God weaves them toward good.

v.38 — NET: "For I am convinced that neither death, nor life...
       will be able to separate us from the love of God" —
       "convinced" (pepeismai = I have been persuaded and remain
       persuaded). WEB: "For I am persuaded." KJV: "For I am
       persuaded." Perfect tense — settled, unshakeable conviction
       tested by experience (vv.35-36)."""

notes[9] = """v.3  — NET: "I could wish that I myself were accursed — Loss
       cut off from Christ — for the sake of my people" — "accursed"
       (anathema = devoted to destruction/damned). WEB: "accursed
       from Christ." KJV: "accursed from Christ." Paul's love for
       Israel echoes Moses' offer in Exodus 32:32.

v.5  — NET: "To them belong the patriarchs, and from them, by
       human descent, came the Christ, who is God over all,
       blessed forever!" — "who is God over all" — a direct
       affirmation of Christ's deity. WEB: "who is over all, God,
       blessed forever." Punctuation affects meaning; NET affirms
       the strongest Christological reading.

v.15 — NET: "I will have mercy on whom I have mercy, and I will
       have compassion on whom I have compassion" — quoting Exodus
       33:19. WEB: "I will have mercy on whom I have mercy." KJV:
       "I will have mercy on whom I will have mercy." God's
       sovereign freedom in mercy.

v.20 — NET: "who are you, O man, to talk back to God?" — "talk
       back" (antapokrinomenos = answer against/contradict). WEB:
       "who indeed are you, a man, to reply against God?" KJV:
       "who art thou that repliest against God?" The pot doesn't
       question the potter's design.

v.33 — NET: "Look, I am laying in Zion a stone that will make
       people stumble and a rock that will make them fall, yet the
       one who believes in him will not be put to shame" — combining
       Isaiah 28:16 and 8:14. WEB: "whoever believes in him will
       not be disappointed." NET: "not put to shame." KJV: "shall
       not be ashamed." Faith in Christ never disappoints."""

notes[10] = """v.4  — NET: "For Christ is the end of the law, with the result
       that there is righteousness for everyone who believes" —
       "end" (telos) — debated: termination? goal? fulfillment?
       WEB: "Christ is the fulfillment of the law." KJV: "Christ
       is the end of the law." NET's "end... with the result" tries
       to capture both senses.

v.9  — NET: "if you confess with your mouth that Jesus is Lord
       and believe in your heart that God raised him from the dead,
       you will be saved" — "Jesus is Lord" (kyrion IEsoun) — the
       earliest Christian confession. WEB: "Jesus is Lord." KJV:
       "the Lord Jesus." Lordship and resurrection belief together.

v.10 — NET: "with the heart one believes and thus has righteousness
       and with the mouth one confesses and thus has salvation" —
       "thus has" (eis = resulting in/leading to). WEB: "with the
       heart, one believes resulting in righteousness." Internal
       faith and external confession together constitute salvation.

v.13 — NET: "everyone who calls on the name of the Lord will be
       saved" — quoting Joel 2:32. "Everyone" (pas) — universal
       offer. WEB: "whoever will call on the name of the Lord will
       be saved." KJV: "whosoever shall call upon the name of the
       Lord shall be saved." No ethnic restriction.

v.17 — NET: "Consequently faith comes from what is heard, and
       what is heard comes through the preached word of Christ" —
       "what is heard" (akoEs = hearing/report/message). WEB:
       "faith comes by hearing, and hearing by the word of God."
       KJV: "faith cometh by hearing, and hearing by the word of
       God." Some manuscripts: "word of Christ" (NET) vs. "word of
       God" (KJV/WEB)."""

notes[11] = """v.5  — NET: "So too at the present time there is a remnant
       chosen by grace" — "remnant" (leimma = what is left over).
       WEB: "there is a remnant according to the election of grace."
       KJV: "there is a remnant according to the election of grace."
       Grace and election together — not works-based selection.

v.17 — NET: "you, a wild olive shoot, were grafted in among them
       and participated in the richness of the olive root" —
       "wild olive shoot" — Gentile believers, grafted unnaturally
       into Israel's cultivated tree. WEB: "grafted in among them."
       The image is horticulturally backwards (wild into cultivated)
       — emphasizing grace over nature.

v.22 — NET: "Notice therefore the kindness and harshness of God"
       — "harshness" (apotomian = severity/cutting off). WEB:
       "the goodness and severity of God." KJV: "the goodness and
       severity of God." God is both kind AND severe — not one
       without the other.

v.25 — NET: "a partial hardening has happened to Israel until the
       full number of the Gentiles has come in" — "full number"
       (plErOma = fullness/completion). WEB: "until the fullness
       of the Gentiles has come in." KJV: "until the fulness of
       the Gentiles be come in." A definite number and time known
       to God.

v.33 — NET: "Oh, the depth of the riches and wisdom and knowledge
       of God!" — Paul's doxology after three chapters of wrestling
       with sovereignty. WEB: "Oh the depth of the riches both of
       the wisdom and the knowledge of God!" KJV: "O the depth of
       the riches both of the wisdom and knowledge of God!" Theology
       leads to worship."""

notes[12] = """v.1  — NET: "present your bodies as a sacrifice — Loss alive,
       holy, and pleasing to God" — "living sacrifice" (thysian
       zOsan) — OT sacrifices died; this one stays alive. WEB:
       "present your bodies a living sacrifice." KJV: "present your
       bodies a living sacrifice." The paradox: a sacrifice that
       lives, dies daily but keeps breathing.

v.2  — NET: "Do not be conformed to this present world, but be
       transformed by the renewing of your mind" — "transformed"
       (metamorphousthe = metamorphosis). WEB: "be transformed by
       the renewing of your mind." KJV: "be ye transformed." Same
       word as Jesus' transfiguration — a fundamental change from
       inside out.

v.9  — NET: "Love must be without hypocrisy" — "without hypocrisy"
       (anypokritos = unfeigned/genuine). WEB: "Let love be without
       hypocrisy." KJV: "Let love be without dissimulation." Love
       that performs is not love. The word comes from actors wearing
       masks (hypokritEs).

v.19 — NET: "Do not avenge yourselves, dear friends, but give
       place to God's wrath" — "give place" (dote topon = make
       room for). WEB: "give place to God's wrath." KJV: "give
       place unto wrath." Step back and let God handle vengeance —
       it's His department, not yours.

v.21 — NET: "Do not be overcome by evil, but overcome evil with
       good" — the summary command of the chapter. WEB: "Don't be
       overcome by evil, but overcome evil with good." KJV: "Be
       not overcome of evil, but overcome evil with good." Good is
       the weapon; evil is overcome by being out-loved."""

notes[13] = """v.1  — NET: "Let every person be subject to the governing
       authorities" — "be subject" (hypotassesthO = place yourself
       under in an orderly way). WEB: "Let every soul be in
       subjection to the higher authorities." KJV: "Let every soul
       be subject unto the higher powers." Not blind obedience but
       ordered respect for God-established authority.

v.4  — NET: "for it is God's servant for your good" — the state
       as "God's servant" (theou diakonos). WEB: "for he is a
       servant of God to you for good." KJV: "the minister of God
       to thee for good." Government exists for public good under
       God's sovereignty.

v.8  — NET: "Owe no one anything, except to love one another" —
       "owe" (opheilete = be indebted). WEB: "Owe no one anything,
       except to love one another." KJV: "Owe no man any thing, but
       to love one another." Love is the one debt never fully paid.

v.11 — NET: "it is already the hour for you to awake from sleep"
       — "awake" (egerthEnai = rise/be raised — resurrection
       language). WEB: "knowing the time, that it is already time
       for you to awaken out of sleep." KJV: "now it is high time
       to awake out of sleep." Spiritual drowsiness is dangerous.

v.14 — NET: "Instead, put on the Lord Jesus Christ, and make no
       provision for the flesh to arouse its desires" — "put on"
       (endysasthe = clothe yourself with). WEB: "put on the Lord
       Jesus Christ." KJV: "put ye on the Lord Jesus Christ."
       Augustine's conversion verse — he read this and was changed."""

notes[14] = """v.1  — NET: "Now accept the one who is weak in faith, and do
       not have disputes over differing opinions" — "weak in faith"
       — not morally weak but with a sensitive/immature conscience.
       WEB: "accept him who is weak in faith." KJV: "Him that is
       weak in the faith receive ye." Welcome without argument.

v.5  — NET: "One person regards one day holier than other days,
       and another regards them all alike. Each must be fully
       convinced in his own mind" — "fully convinced" (plErophoreisthO
       = carry to full assurance). WEB: "Let each man be fully
       assured in his own mind." Conviction, not conformity.

v.10 — NET: "For we will all stand before the judgment seat of
       God" — "judgment seat" (bEmati = tribunal/platform). WEB:
       "we will all stand before the judgment seat of Christ." Some
       manuscripts: "of God" (NET) vs. "of Christ" (WEB/KJV).
       Either way — divine evaluation of believers.

v.17 — NET: "For the kingdom of God does not consist of food and
       drink, but righteousness, peace, and joy in the Holy Spirit"
       — the kingdom's essence defined. WEB: "the Kingdom of God
       is not eating and drinking, but righteousness, peace, and
       joy in the Holy Spirit." Not dietary rules but Spirit-fruit.

v.23 — NET: "everything that does not come from faith is sin" —
       the chapter's conclusion and one of the most sweeping
       ethical principles in Scripture. WEB: "whatever is not of
       faith is sin." KJV: "whatsoever is not of faith is sin."
       If you can't do it in good conscience before God, don't."""

notes[15] = """v.1  — NET: "We who are strong ought to bear with the failings
       of the weak, and not just please ourselves" — "bear with"
       (bastazein = carry/bear the burden of). WEB: "bear the
       weaknesses of the weak." KJV: "bear the infirmities of the
       weak." The strong carry the weak — not mock, avoid, or
       correct them.

v.4  — NET: "For everything that was written in former times was
       written for our instruction" — "instruction" (didaskalian
       = teaching/doctrine). WEB: "for our learning." KJV: "for
       our learning." The OT has ongoing relevance for NT believers.

v.13 — NET: "Now may the God of hope fill you with all joy and
       peace as you believe in him, so that you may abound in hope
       by the power of the Holy Spirit" — "God of hope" — a unique
       title. WEB: "the God of hope fill you with all joy and
       peace in believing." All Trinitarian: God of hope, believe
       in Him, power of Spirit.

v.16 — NET: "to be a minister of Christ Jesus to the Gentiles. I
       serve the gospel of God like a priest" — "like a priest"
       (hierourgounta = performing priestly service). WEB:
       "ministering as a priest the Good News of God." KJV:
       "ministering the gospel of God." Paul sees his evangelism
       as priestly — offering Gentiles as a sacrifice to God.

v.20 — NET: "not where Christ has already been named, so that I
       would not build on someone else's foundation" — Paul's
       pioneer missionary principle. WEB: "not where Christ was
       already named." KJV: "not where Christ was named." He
       deliberately went where no one else had gone."""

notes[16] = """v.1  — NET: "I commend to you our sister Phoebe, who is a
       servant of the church in Cenchreae" — "servant" (diakonon
       = deacon/minister). WEB: "a servant of the assembly." KJV:
       "a servant of the church." Whether this indicates the office
       of deacon or general service is debated. She likely carried
       this letter to Rome.

v.7  — NET: "Greet Andronicus and Junia, my compatriots and my
       fellow prisoners. They are well known to the apostles" —
       "Junia" — likely a woman (NET/ESV). Some manuscripts have
       "Junias" (masculine). WEB: "Junias." KJV: "Junia." If
       female, she was "outstanding among the apostles" — though
       "known to" vs. "among" is also debated.

v.17 — NET: "watch out for those who create dissensions and
       obstacles" — "watch out" (skopein = keep your eye on/mark).
       WEB: "mark those who are causing the divisions." KJV: "mark
       them which cause divisions." Active vigilance against
       divisive people — not passive tolerance.

v.20 — NET: "The God of peace will quickly crush Satan under your
       feet" — echoing Genesis 3:15. WEB: "The God of peace will
       quickly crush Satan under your feet." KJV: "shall bruise
       Satan under your feet shortly." The promise of final victory
       — and it is SOON and UNDER YOUR FEET (the church participates).

v.25 — NET: "to the only wise God, through Jesus Christ, be glory
       forever! Amen" — the closing doxology. WEB: "to the only
       wise God, through Jesus Christ, to whom be the glory forever!
       Amen." KJV: "To God only wise, be glory through Jesus Christ
       for ever. Amen." Some manuscripts place this doxology after
       14:23 or 15:33 — its position varies."""

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
    filepath = os.path.join(base, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print(f"  done Chapter {ch}")
        else:
            print(f"  skip Chapter {ch}")
    else:
        print(f"  missing Chapter {ch}")
