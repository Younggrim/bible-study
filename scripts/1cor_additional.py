#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to 1 Corinthians chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/07 - 1 Corinthians"

notes = dict()

notes[1] = """v.10 — NET: "I urge you, brothers and sisters, by the name of
       our Lord Jesus Christ, to agree together" — "brothers and
       sisters" (adelphoi = siblings, inclusive). WEB: "brothers."
       KJV: "brethren." NET uses gender-inclusive language for the
       Greek masculine plural that includes women.

v.18 — NET: "For the message about the cross is foolishness to
       those who are perishing, but to us who are being saved it
       is the power of God" — "being saved" (sOzomenois = present
       participle — ongoing process). WEB: "to us who are being
       saved." KJV: "unto us which are saved." The present tense
       suggests salvation as ongoing, not just past event.

v.23 — NET: "but we preach about a crucified Christ, a stumbling
       block to Jews and foolishness to Gentiles" — "stumbling
       block" (skandalon). WEB: "a stumbling block to Jews." KJV:
       "unto the Jews a stumblingblock." The cross offends Jewish
       expectation of a conquering Messiah.

v.27 — NET: "God chose what is foolish in the world to shame the
       wise" — "chose" (exelexato = deliberately selected). WEB:
       "God chose the foolish things of the world." God's selection
       criteria invert human hierarchies — weakness shames strength.

v.30 — NET: "He is the reason you have a relationship with Christ
       Jesus, who became for us wisdom from God, and righteousness,
       and sanctification, and redemption" — Christ as four things
       from God. WEB: "who was made to us wisdom from God, and
       righteousness and sanctification, and redemption." All
       sufficiency in Christ."""

notes[2] = """v.2  — NET: "For I decided to be concerned about nothing among
       you except Jesus Christ, and him crucified" — "decided"
       (ekrina = judged/determined). WEB: "I determined not to
       know anything among you, except Jesus Christ, and him
       crucified." A deliberate strategic choice — not ignorance.

v.9  — NET: "Things that no eye has seen, or ear heard, or mind
       imagined, are the things God has prepared for those who love
       him" — loosely quoting Isaiah 64:4. WEB: "Things which eye
       didn't see, and ear didn't hear." Often quoted about heaven
       but in context refers to the wisdom God NOW reveals by the
       Spirit (v.10).

v.10 — NET: "God has revealed these to us by the Spirit. For the
       Spirit searches all things, even the deep things of God" —
       "searches" (eraunai = investigates/explores). WEB: "the
       Spirit searches all things, yes, the deep things of God."
       The Spirit has access to God's unfathomable depths.

v.14 — NET: "The unbeliever does not receive the things of the
       Spirit of God" — "unbeliever" (psychikos anthrOpos = natural
       /soulish person). KJV: "natural man." WEB: "the natural
       man." Not merely intellectual limitation but spiritual
       inability without the Spirit's illumination.

v.16 — NET: "we have the mind of Christ" — "mind" (noun Christou).
       WEB: "we have Christ's mind." KJV: "we have the mind of
       Christ." A staggering claim — believers share Christ's
       perspective through the indwelling Spirit."""

notes[3] = """v.6  — NET: "I planted, Apollos watered, but God caused it to
       grow" — "caused it to grow" (Euxanen = was causing growth,
       imperfect tense — continuous). WEB: "God gave the increase."
       KJV: "God gave the increase." Ministers are tools; God is
       the grower. Human effort necessary but not sufficient.

v.11 — NET: "For no one can lay any foundation other than what is
       being laid, which is Jesus Christ" — "no one can" (ou
       dynatai) — impossibility, not just prohibition. WEB: "no
       one is able to lay another foundation." There is one
       foundation; everything else is superstructure.

v.13 — NET: "each builder's work will be plainly seen, for the
       Day will make it clear, because it will be revealed by fire"
       — "the Day" (hE hEmera) = judgment day. WEB: "the Day will
       declare it." KJV: "the day shall declare it." Fire tests
       quality, not sincerity. Wood, hay, stubble burn; gold,
       silver, precious stones survive.

v.16 — NET: "Do you not know that you are God's temple and that
       God's Spirit lives in you?" — "you" is PLURAL (naos theou
       este) — the church collectively is the temple. WEB: "you
       are a temple of God." Not primarily individual bodies (that's
       6:19) but the corporate assembly.

v.21 — NET: "So then, no more boasting about mere mortals!" —
       "all things are yours" (v.21-22) — Paul, Apollos, Cephas,
       the world, life, death, present, future. WEB: "let no one
       boast in men." KJV: "let no man glory in men." All teachers
       belong to the church; the church doesn't belong to teachers."""

notes[4] = """v.1  — NET: "One should think about us this way — as servants
       of Christ and stewards of the mysteries of God" — "servants"
       (hypEretas = under-rowers, subordinate workers). WEB:
       "servants of Christ and stewards of God's mysteries." KJV:
       "ministers of Christ." The lowest rank of servants.

v.5  — NET: "do not judge anything before the time. Wait until
       the Lord comes" — "before the time" (pro kairou = before
       the proper season). WEB: "judge nothing before the time."
       Premature evaluation is unreliable — wait for the final
       Judge who illuminates hidden motives.

v.7  — NET: "What do you have that you did not receive? And if
       you received it, why do you boast as though you did not?" —
       the logic that destroys all pride. WEB: "What do you have
       that you didn't receive?" Everything is gift — boasting is
       irrational.

v.13 — NET: "We have become the world's dirt and the scum of all
       things" — "dirt" (perikatharmata = offscouring/refuse) and
       "scum" (peripsEma = filth wiped off). WEB: "the filth of
       the world, the dirt wiped off by all." Apostolic ministry
       is not glamorous — it is despised.

v.20 — NET: "For the kingdom of God is demonstrated not in idle
       talk but with power" — "not in idle talk" (ouk en logO =
       not in word/speech). WEB: "the Kingdom of God is not in
       word, but in power." KJV: "the kingdom of God is not in
       word, but in power." Spiritual reality over rhetoric."""

notes[5] = """v.5  — NET: "hand this man over to Satan for the destruction
       of the flesh, so that his spirit may be saved in the day of
       the Lord" — "destruction of the flesh" (olethron tEs sarkos)
       — debated: physical suffering? death? removal of fleshly
       desires? WEB: "for the destruction of the flesh." The goal
       is redemptive, not merely punitive.

v.6  — NET: "Your boasting is not good. Don't you know that a
       little yeast affects the whole batch of dough?" — "yeast"
       (zymE = leaven). WEB: "a little leaven leavens the whole
       lump." KJV: "a little leaven leaveneth the whole lump."
       Tolerated sin spreads — no contamination stays contained.

v.7  — NET: "Clean out the old yeast so that you may be a new
       batch of dough — you are, in fact, without yeast. For Christ,
       our Passover lamb, has been sacrificed" — "Christ our
       Passover" (to pascha hEmOn Christos). WEB: "our Passover,
       Christ, has been sacrificed." The Exodus imagery applied to
       the cross.

v.11 — NET: "not to associate with anyone who calls himself a
       Christian who is sexually immoral, or greedy, or an idolater"
       — "calls himself a Christian" (onomazomenos adelphos = named
       a brother). WEB: "anyone who is called a brother." The
       distinction: professing believers held to higher standard
       than outsiders (v.12).

v.13 — NET: "Remove the evil person from among you" — quoting
       Deuteronomy 17:7. WEB: "Put away the wicked man from among
       yourselves." KJV: "put away from among yourselves that
       wicked person." Church discipline is a biblical command,
       not optional."""

notes[6] = """v.9  — NET: "Do you not know that the unrighteous will not
       inherit the kingdom of God?" — "unrighteous" (adikoi). WEB:
       "the unrighteous will not inherit God's Kingdom." The vice
       list follows (vv.9-10): fornicators, idolaters, adulterers,
       effeminate, homosexuals, thieves, covetous, drunkards,
       revilers, extortioners.

v.11 — NET: "Some of you once lived this way. But you were washed,
       you were sanctified, you were justified in the name of the
       Lord Jesus Christ and by the Spirit of our God" — three
       past-tense verbs: washed, sanctified, justified. WEB: "you
       were washed. You were sanctified. You were justified." Past
       identity transformed.

v.12 — NET: "'All things are lawful for me' — but not everything
       is beneficial" — Paul quotes the Corinthians' slogan back
       to them and qualifies it. WEB: "All things are lawful for
       me, but not all things are expedient." Liberty is not
       license.

v.19 — NET: "Do you not know that your body is the temple of the
       Holy Spirit who is in you?" — "your body" (to sOma hymOn)
       — HERE it is individual bodies (unlike 3:16 which is
       corporate). WEB: "your body is a temple of the Holy Spirit."
       KJV: "your body is the temple of the Holy Ghost." Individual
       sanctity.

v.20 — NET: "For you were bought at a price. Therefore glorify
       God with your body" — "bought at a price" (EgorasthEte
       timEs = purchased at cost). WEB: "you were bought with a
       price." KJV: "ye are bought with a price." Redemption
       language — slaves purchased and freed. The price: Christ's
       blood."""

notes[7] = """v.7  — NET: "each has his own gift from God, one this way,
       another that" — "gift" (charisma = grace-gift). WEB: "each
       man has his own gift from God." Marriage AND singleness are
       both charismata — both require grace.

v.10 — NET: "To the married I give this command — not I, but the
       Lord — a wife should not separate from her husband" — "not
       I, but the Lord" — Paul distinguishes between direct
       dominical teaching (from Jesus' earthly ministry) and his
       own apostolic instruction (v.12). WEB: "not I, but the Lord."

v.15 — NET: "God has called you in peace" — "in peace" (en
       eirEnE). WEB: "God has called us in peace." KJV: "God hath
       called us to peace." If an unbelieving spouse departs, the
       believer is "not bound" (ou dedoulOtai = not enslaved).
       The extent of this freedom is debated.

v.29 — NET: "the time is short" — "short" (synestalmenos =
       compressed/contracted). WEB: "the time is short." KJV: "the
       time is short." Eschatological urgency shapes present
       decisions — live with eternity in view.

v.31 — NET: "those who use the world as though they were not
       using it to the full. For the present form of this world is
       passing away" — "present form" (to schEma tou kosmou = the
       fashion/outward shape). WEB: "the mode of this world passes
       away." KJV: "the fashion of this world passeth away." The
       current arrangement is temporary."""

notes[8] = """v.1  — NET: "knowledge puffs up, but love builds up" —
       "puffs up" (physioi = inflates/makes arrogant) vs. "builds
       up" (oikodomei = edifies/constructs). WEB: "Knowledge puffs
       up, but love builds up." The governing principle for all
       that follows: love trumps knowledge.

v.4  — NET: "we know that 'an idol in this world is nothing' and
       that 'there is no God but one'" — Paul quotes Corinthian
       slogans approvingly — monotheism means idols have no real
       existence. WEB: "we know that no idol is anything in the
       world." Theologically true but pastorally insufficient.

v.9  — NET: "But be careful that this liberty of yours does not
       become a hindrance to the weak" — "hindrance" (proskomma =
       stumbling block). WEB: "be careful that by no means does
       this liberty of yours become a stumbling block to the weak."
       Freedom exercised without love becomes a weapon.

v.11 — NET: "So by your knowledge the weak brother or sister, for
       whom Christ died, is destroyed" — "for whom Christ died"
       (di' hon Christos apethanen) — the value of the weaker
       brother measured by Christ's death. WEB: "the weak perish,
       the brother for whose sake Christ died." Your knowledge
       destroys what Christ died to save.

v.13 — NET: "if food causes my brother or sister to sin, I will
       never eat meat again" — Paul's personal resolution. WEB:
       "if food causes my brother to stumble, I will eat no meat
       forever more." KJV: "I will eat no flesh while the world
       standeth." Voluntary limitation motivated by love."""

notes[9] = """v.16 — NET: "For if I preach the gospel, I have nothing to
       boast about, for I am compelled to do this. Woe to me if I
       do not preach the gospel!" — "compelled" (anankE = necessity/
       divine constraint). WEB: "necessity is laid on me." KJV:
       "necessity is laid upon me." Paul cannot NOT preach — it is
       existential obligation.

v.19 — NET: "For though I am free from all people, I have made
       myself a slave to all" — "free from all... slave to all" —
       the paradox of apostolic ministry. WEB: "though I was free
       from all, I brought myself under bondage to all." Freedom
       voluntarily surrendered for others.

v.22 — NET: "I have become all things to all people, so that by
       all means I may save some" — "all things to all people" —
       contextual flexibility without moral compromise. WEB: "I
       have become all things to all men." KJV: "I am made all
       things to all men." Adaptation of method, not message.

v.24 — NET: "Do you not know that all the runners in a stadium
       compete, but only one receives the prize? So run to win" —
       "run to win" (houtOs trechete hina katalabEte). WEB: "Run,
       that you may attain." Athletic imagery — effort, discipline,
       focus required in the Christian life.

v.27 — NET: "I discipline my body and make it my slave, so that
       after preaching to others I myself will not be disqualified"
       — "disqualified" (adokimos = failing the test/rejected).
       WEB: "lest by any means, after I have preached to others,
       I myself should be rejected." Even Paul considers this
       danger real."""

notes[10] = """v.4  — NET: "they all drank the same spiritual drink. For they
       were all drinking from the spiritual rock that followed
       them, and the rock was Christ" — "the rock was Christ" —
       Paul identifies the wilderness rock with Christ's pre-
       incarnate presence. WEB: "the rock was Christ." Christological
       reading of the OT.

v.12 — NET: "So let the one who thinks he is standing be careful
       that he does not fall" — "thinks he is standing" (ho dokOn
       hestanai) — the danger of overconfidence. WEB: "let him who
       thinks he stands be careful that he doesn't fall." Self-
       assurance is the prelude to collapse.

v.13 — NET: "God is faithful, and he will not let you be tempted
       beyond what you can bear. But with the temptation he will
       also provide a way out" — "a way out" (tEn ekbasin = the
       exit/escape). WEB: "will with the temptation also make the
       way of escape." God engineers escapes for every test.

v.16 — NET: "Is not the cup of blessing that we bless a sharing
       in the blood of Christ?" — "sharing" (koinOnia = communion/
       participation/fellowship). WEB: "a communion of the blood
       of Christ." KJV: "the communion of the blood of Christ."
       The Lord's Supper as genuine participation in Christ.

v.31 — NET: "So whether you eat or drink, or whatever you do,
       do everything for the glory of God" — the simplest and most
       comprehensive ethical principle. WEB: "do all to the glory
       of God." KJV: "do all to the glory of God." Every action —
       even the mundane — can glorify God."""

notes[11] = """v.3  — NET: "But I want you to know that Christ is the head of
       every man, and the man is the head of a woman, and God is
       the head of Christ" — "head" (kephalE) — debated: authority?
       source? preeminence? WEB: "the head of every man is Christ."
       The meaning of kephalE drives the entire head covering debate.

v.24 — NET: "This is my body that is for you. Do this in
       remembrance of me" — "for you" (to hyper hymOn). WEB: "This
       is my body, which is broken for you." KJV: "this is my
       body, which is broken for you." Some manuscripts omit
       "broken" — NET/ESV omit; KJV/WEB include.

v.26 — NET: "For every time you eat this bread and drink the cup,
       you proclaim the Lord's death until he comes" — "until he
       comes" (achri hou elthE) — the Supper is temporary,
       pointing forward to the Marriage Supper of the Lamb. WEB:
       "until he comes." An eschatological ordinance.

v.29 — NET: "For the one who eats and drinks without careful
       regard for the body eats and drinks judgment against himself"
       — "without careful regard for the body" (mE diakrinOn to
       sOma = not discerning the body). WEB: "not discerning the
       Lord's body." Which body — Christ's physical body or the
       church body? Both are possible.

v.30 — NET: "That is why many of you are weak and sick, and quite
       a few are dead" — "dead" (koimOntai = sleeping/have fallen
       asleep). WEB: "not a few sleep." KJV: "many sleep." Physical
       consequences of spiritual carelessness — God disciplines
       His own (v.32)."""

notes[12] = """v.3  — NET: "no one speaking by the Spirit of God says, 'Jesus
       is cursed,' and no one can say, 'Jesus is Lord,' except by
       the Holy Spirit" — "Jesus is Lord" (Kyrios IEsous) — the
       most basic Christian confession requires Spirit-enablement.
       WEB: "no one can say, 'Jesus is Lord,' but by the Holy Spirit."

v.7  — NET: "To each person the manifestation of the Spirit is
       given for the benefit of all" — "for the benefit of all"
       (pros to sympheron = for the common advantage). WEB: "for
       the profit of all." KJV: "to profit withal." Gifts are not
       for personal display but communal edification.

v.11 — NET: "It is one and the same Spirit, distributing as he
       decides to each person" — "as he decides" (kathOs bouletai
       = as He wills). WEB: "dividing to each one separately as he
       desires." The Spirit is sovereign in gift distribution — not
       the believer's choice.

v.18 — NET: "But as a matter of fact, God has placed each of the
       members in the body just as he decided" — "just as he
       decided" (kathOs EthelEsen = as He willed). WEB: "God has
       set the members, each one of them, in the body, just as he
       desired." Your place in the body is divine appointment.

v.26 — NET: "If one member suffers, everyone suffers with it. If
       a member is honored, all rejoice with it" — organic
       interconnection. WEB: "when one member suffers, all the
       members suffer with it." The body cannot compartmentalize
       pain or glory — it is shared."""

notes[13] = """v.1  — NET: "If I speak in the tongues of men and of angels,
       but I do not have love, I am a noisy gong or a clanging
       cymbal" — "noisy gong" (chalkos EchOn). WEB: "sounding
       brass or a clanging cymbal." KJV: "sounding brass, or a
       tinkling cymbal." Without love, even supernatural speech is
       empty noise — no content, just volume.

v.4  — NET: "Love is patient, love is kind, it is not envious.
       Love does not brag, it is not puffed up" — fifteen
       descriptors of love, mostly negatives (what love does NOT
       do). WEB: "Love is patient and is kind." ASV: "Love
       suffereth long, and is kind." The portrait fits Christ
       perfectly.

v.7  — NET: "It bears all things, believes all things, hopes all
       things, endures all things" — four "all things" (panta) —
       comprehensive, without exception. WEB: "bears all things,
       believes all things, hopes all things, endures all things."
       Love's capacity is unlimited.

v.12 — NET: "For now we see in a mirror indirectly, but then we
       will see face to face" — "in a mirror indirectly" (di'
       esoptrou en ainigmati = through a mirror in a riddle). WEB:
       "now we see in a mirror, dimly." Ancient bronze mirrors gave
       imperfect reflections — current knowledge is partial.

v.13 — NET: "And now these three remain: faith, hope, and love.
       But the greatest of these is love" — "greatest" (meizOn =
       larger/greater). WEB: "the greatest of these is love." KJV:
       "the greatest of these is charity." Love outlasts faith
       (which becomes sight) and hope (which becomes possession)."""

notes[14] = """v.2  — NET: "For the one who speaks in a tongue does not speak
       to people but to God" — "to God" (theO lalei) — tongues
       directed Godward, not humanward. WEB: "speaks not to men,
       but to God." KJV: "speaketh not unto men, but unto God."
       Private communication with God in prayer.

v.5  — NET: "I wish you all spoke in tongues, but even more I
       wish you would prophesy" — Paul doesn't forbid tongues
       (v.39: "do not forbid speaking in tongues") but values
       prophecy higher for corporate gatherings. WEB: "I desire
       that you all spoke with other languages, but rather that
       you would prophesy."

v.19 — NET: "in the church I want to speak five words with my
       mind to instruct others, rather than ten thousand words in a
       tongue" — "five words... ten thousand" — hyperbolic ratio.
       WEB: "I would rather speak five words with my understanding
       ...than ten thousand words in another language." Intelligibility
       over impressiveness.

v.33 — NET: "for God is not characterized by disorder but by
       peace" — "disorder" (akatastasias = instability/confusion).
       WEB: "God is not a God of confusion, but of peace." KJV:
       "God is not the author of confusion, but of peace." The
       character of God defines proper worship.

v.40 — NET: "But everything must be done in a proper and orderly
       manner" — "proper and orderly" (euschEmonOs kai kata taxin).
       WEB: "Let all things be done decently and in order." KJV:
       "Let all things be done decently and in order." The closing
       principle for all charismatic expression."""

notes[15] = """v.3  — NET: "Christ died for our sins according to the
       scriptures" — "according to the scriptures" (kata tas
       graphas) — the death was scripturally predicted and
       scripturally interpreted. WEB: "Christ died for our sins
       according to the Scriptures." The gospel has four elements:
       died, buried, rose, appeared.

v.14 — NET: "and if Christ has not been raised, then our
       preaching is futile and your faith is empty" — "futile"
       (kenon = empty/vain). WEB: "our preaching is in vain, and
       your faith also is in vain." Without resurrection,
       Christianity collapses entirely — Paul stakes everything.

v.22 — NET: "For just as in Adam all die, so also in Christ all
       will be made alive" — "in Adam... in Christ" — the two
       representative heads of humanity. WEB: "as in Adam all die,
       so also in Christ all will be made alive." Universal death
       through Adam; life through Christ.

v.51 — NET: "Listen, I will tell you a mystery: We will not all
       sleep, but we will all be changed" — "mystery" (mystErion =
       previously hidden truth now revealed). WEB: "we will all be
       changed." KJV: "we shall all be changed." The rapture/
       transformation — mortality swallowed by life.

v.55 — NET: "Where, O death, is your victory? Where, O death, is
       your sting?" — quoting Hosea 13:14 and Isaiah 25:8. WEB:
       "Death, where is your sting? Hades, where is your victory?"
       KJV: "O death, where is thy sting? O grave, where is thy
       victory?" Death taunted by the resurrected — its power broken."""

notes[16] = """v.2  — NET: "On the first day of the week, each of you should
       set aside some income and save it" — "first day of the week"
       — confirms Sunday as the gathering day. WEB: "On the first
       day of every week, let each one of you save." Systematic,
       proportional, regular giving.

v.9  — NET: "a door of great opportunity stands wide open for me,
       but there are many opponents" — opportunity and opposition
       together — a typical ministry pattern. WEB: "a great and
       effective door has opened to me, and there are many
       adversaries." Open doors don't mean easy roads.

v.13 — NET: "Stay alert, stand firm in the faith, show courage,
       be strong" — four military imperatives. WEB: "Watch! Stand
       firm in the faith! Be courageous! Be strong!" KJV: "Watch
       ye, stand fast in the faith, quit you like men, be strong."
       ASV: "Watch ye, stand fast in the faith, quit you like men,
       be strong." Vigilance, stability, courage, strength.

v.14 — NET: "Everything you do should be done in love" — the
       summary command after the imperatives. WEB: "Let all that
       you do be done in love." KJV: "Let all your things be done
       with charity." Strength without love is brutality; love
       without strength is sentimentality.

v.22 — NET: "If anyone does not love the Lord, let him be
       accursed. Maranatha!" — "Maranatha" (Aramaic: marana tha =
       "Our Lord, come!" or maran atha = "Our Lord has come").
       WEB: "If any man doesn't love the Lord Jesus Christ, let
       him be accursed. Come, Lord!" The oldest recorded prayer
       of the church in its original language."""


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
