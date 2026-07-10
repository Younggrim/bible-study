#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Colossians, 1 Thess, 2 Thess."""
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

books = []

# Colossians
col_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/12 - Colossians"
col = dict()
col[1] = """v.15 — NET: "He is the image of the invisible God, the
       firstborn over all creation" — "firstborn" (prOtotokos) —
       not first created but preeminent/supreme (as firstborn has
       rights of inheritance). WEB: "the firstborn of all creation."
       KJV: "the firstborn of every creature." Supremacy, not
       origin — v.16 clarifies: all things were created BY Him.

v.16 — NET: "all things in heaven and on earth were created in
       him — all things, whether visible or invisible" — "in him"
       (en autO) — Christ as the sphere and agent of creation. WEB:
       "For by him all things were created." Four prepositions
       describe Christ's relationship to creation: in, through, by,
       and for Him.

v.17 — NET: "He himself is before all things and all things are
       held together in him" — "held together" (synestEken = cohere/
       consist). WEB: "in him all things are held together." KJV:
       "by him all things consist." Christ is the cosmic glue —
       without Him, reality disintegrates.

v.19 — NET: "For God was pleased to have all his fullness dwell
       in the Son" — "all his fullness" (pan to plErOma). WEB: "all
       the fullness was pleased to dwell in him." KJV: "in him
       should all fulness dwell." The totality of deity resides in
       Christ — not partially but completely.

v.27 — NET: "Christ in you, the hope of glory" — the mystery
       revealed: Christ indwelling Gentiles. WEB: "Christ in you,
       the hope of glory." KJV: "Christ in you, the hope of glory."
       The shortest summary of the Christian life — Christ within
       as present reality and future guarantee."""

col[2] = """v.8  — NET: "Be careful not to allow anyone to captivate you
       through an empty, deceitful philosophy" — "captivate"
       (sylagOgOn = carry off as plunder/kidnap). WEB: "lest anyone
       rob you through his philosophy." KJV: "lest any man spoil
       you through philosophy." The imagery is of being captured
       and enslaved by false ideas.

v.9  — NET: "For in him all the fullness of deity lives in bodily
       form" — "deity" (theotEtos = the essence of God/Godhood).
       WEB: "in him all the fullness of the Godhead dwells bodily."
       KJV: "in him dwelleth all the fulness of the Godhead bodily."
       Not just divine qualities but the full being of God in a
       physical body.

v.14 — NET: "He has destroyed what was against us, a certificate
       of indebtedness expressed in decrees opposed to us" —
       "certificate of indebtedness" (cheirographon = handwritten
       IOU). WEB: "the handwriting in ordinances." KJV: "the
       handwriting of ordinances." Our sin-debt nailed to the cross
       — marked PAID.

v.15 — NET: "Disarming the rulers and authorities, he has made a
       public disgrace of them, triumphing over them" — "public
       disgrace" (edeigmatisen = exposed/put to open shame). WEB:
       "having stripped the principalities and the powers." The
       cross as Christ's victory parade — Satan publicly humiliated.

v.23 — NET: "these things indeed have an appearance of wisdom...
       but they are worthless when it comes to restraining the
       indulgence of the flesh" — "appearance of wisdom" (logon
       sophias = reputation/word of wisdom). WEB: "a reputation of
       wisdom." Human rules look impressive but lack actual power
       over sin."""

col[3] = """v.1  — NET: "if then you have been raised with Christ, keep
       seeking the things above" — "keep seeking" (zEteite = present
       imperative — continue seeking). WEB: "seek the things that
       are above." KJV: "seek those things which are above." The
       indicative (raised) grounds the imperative (seek) — what you
       ARE determines what you DO.

v.3  — NET: "your life is hidden with Christ in God" — "hidden"
       (kekryptai = concealed/stored securely). WEB: "your life is
       hidden with Christ in God." KJV: "your life is hid with
       Christ in God." Triple security: your life, in Christ, in
       God. Nothing can reach it.

v.11 — NET: "there is neither Greek nor Jew, circumcised or
       uncircumcised, barbarian, Scythian, slave or free, but
       Christ is all and in all" — "Christ is all and in all"
       (panta kai en pasin Christos). WEB: "Christ is all, and in
       all." The categories collapse — only Christ matters.

v.16 — NET: "Let the word of Christ dwell in you richly" —
       "richly" (plousiOs = abundantly/lavishly). WEB: "Let the
       word of Christ dwell in you richly." KJV: "Let the word of
       Christ dwell in you richly." Not a little Scripture but
       saturating, overflowing presence of Christ's word.

v.17 — NET: "whatever you do in word or deed, do it all in the
       name of the Lord Jesus" — "whatever" (pan ho ti) — no
       exception. WEB: "whatever you do, in word or in deed, do
       all in the name of the Lord Jesus." The universal standard —
       every action under His authority and for His glory."""

col[4] = """v.2  — NET: "Be devoted to prayer, keeping alert in it with
       thanksgiving" — "be devoted" (proskartereite = persist/
       continue steadfastly). WEB: "Continue steadfastly in prayer."
       KJV: "Continue in prayer." The same word used of the early
       church's devotion (Acts 2:42).

v.5  — NET: "Conduct yourselves with wisdom toward outsiders,
       making the most of the opportunities" — "making the most"
       (ton kairon exagorazomenoi = buying up the time/redeeming
       the moment). WEB: "redeeming the time." KJV: "redeeming the
       time." Time with unbelievers is precious — use it wisely.

v.6  — NET: "Let your speech always be gracious, seasoned with
       salt" — "seasoned with salt" (halati Ertymenos). WEB:
       "seasoned with salt." KJV: "seasoned with salt." Salt
       preserves and flavors — speech should be both pure and
       interesting/memorable. Not bland but not caustic.

v.14 — NET: "Luke, the beloved physician, and Demas greet you" —
       "beloved physician" (ho iatros ho agapEtos). WEB: "Luke, the
       beloved physician." Luke is the only Gentile author of
       Scripture. Later, Demas deserts Paul "having loved this
       present world" (2 Tim 4:10) — a tragic contrast.

v.16 — NET: "also have it read in the church of the Laodiceans"
       — a lost letter to Laodicea (or possibly Ephesians, which
       may have circulated without a specific address). WEB: "cause
       it to be read also in the assembly of the Laodiceans." The
       early church shared apostolic letters between congregations."""

# 1 Thessalonians
thess1_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/13 - 1 Thessalonians"
thess1 = dict()
thess1[1] = """v.3  — NET: "your work of faith and labor of love and
       endurance of hope in our Lord Jesus Christ" — three Pauline
       virtues matched with three activities: faith works, love
       labors, hope endures. WEB: "your work of faith, labor of
       love, and patience of hope." A comprehensive summary of
       Christian character.

v.5  — NET: "our gospel did not come to you merely in words, but
       in power and in the Holy Spirit and with deep conviction" —
       "deep conviction" (plErophoria pollE = full assurance). WEB:
       "in much assurance." KJV: "in much assurance." The gospel
       came with four elements: words + power + Spirit + conviction.

v.9  — NET: "you turned to God from idols to serve the living and
       true God" — "turned" (epestrepshate = converted/turned
       around). WEB: "you turned to God from idols." Conversion
       defined: FROM idols, TO God, SERVING Him, WAITING for Christ.

v.10 — NET: "to wait for his Son from heaven... Jesus, who
       rescues us from the coming wrath" — "rescues" (rhyomenon =
       delivering, present participle — ongoing rescue). WEB: "who
       delivers us from the wrath to come." KJV: "which delivered
       us from the wrath to come." The Second Coming as rescue
       from judgment.

v.10 — WEB: "whom he raised from the dead" — the resurrection as
       the credential of the Son. All translations include this —
       the risen Jesus is the one who rescues. Past resurrection
       guarantees future deliverance."""

thess1[2] = """v.4  — NET: "we have been approved by God to be entrusted with
       the gospel" — "approved" (dedokimasmetha = tested and found
       reliable). WEB: "approved by God to be entrusted with the
       Good News." KJV: "allowed of God to be put in trust with the
       gospel." God tested them before trusting them with the message.

v.7  — NET: "we became little children among you. Like a nursing
       mother caring for her own children" — textual variant:
       "little children" (nEpioi) vs. "gentle" (Epioi). NET
       includes both readings in notes. WEB: "we were gentle among
       you." KJV: "we were gentle among you." One Greek letter
       difference (n vs no n) changes the meaning significantly.

v.13 — NET: "you received it not as a human word, but as it truly
       is, God's word, which is at work in you who believe" — "at
       work" (energeitai = actively operating). WEB: "which also
       works in you who believe." KJV: "which effectually worketh
       also in you that believe." The word is not inert text but
       active divine energy.

v.18 — NET: "Satan hindered us" — "hindered" (enekopsen = cut
       into/blocked the road). WEB: "Satan hindered us." KJV:
       "Satan hindered us." Military language — the enemy cutting
       the road to prevent advance. The spiritual opposition to
       ministry is real and personal.

v.19 — NET: "For who is our hope or joy or crown of boasting
       before our Lord Jesus at his coming? Is it not you?" —
       "crown of boasting" (stephanos kauchEseOs = wreath of
       exultation). WEB: "crown of rejoicing." People are Paul's
       reward — not money, fame, or buildings."""

thess1[3] = """v.2  — NET: "we sent Timothy... to strengthen and encourage
       you about your faith" — "strengthen" (stErixai = establish/
       make firm). WEB: "to establish you and to comfort you." KJV:
       "to establish you, and to comfort you." Two pastoral verbs:
       stabilize and encourage.

v.5  — NET: "I sent to find out about your faith, for fear that
       the tempter somehow tempted you" — "the tempter" (ho
       peirazOn = the one who tests/tempts). WEB: "the tempter had
       tempted you." KJV: "the tempter have tempted you." Satan
       has a specific role: testing faith through suffering.

v.8  — NET: "For now we are alive again, if you stand firm in the
       Lord" — "alive again" (zOmen = we live). WEB: "we live, if
       you stand firm in the Lord." Their faithfulness gives Paul
       life — pastoral joy is tied to converts' perseverance.

v.10 — NET: "as we pray earnestly night and day to see you in
       person and to supply what is lacking in your faith" —
       "supply what is lacking" (katartisai ta hysterEmata =
       complete the deficiencies/mend the gaps). WEB: "perfect
       that which is lacking." Faith has gaps that need filling
       through ongoing teaching.

v.12 — NET: "may the Lord cause you to increase and overflow with
       love for one another" — "overflow" (perisseuai = abound/
       exceed). WEB: "abound in love toward one another." KJV:
       "abound in love one toward another." Love should exceed
       normal bounds — not just adequate but overflowing."""

thess1[4] = """v.3  — NET: "For this is God's will: that you become holy, that
       you keep away from sexual immorality" — "become holy"
       (hagiasmos = sanctification/holiness as process). WEB: "your
       sanctification." KJV: "even your sanctification." God's will
       is not mysterious here — it is moral purity.

v.11 — NET: "to aspire to lead a quiet life, to attend to your
       own business, and to work with your hands" — "aspire"
       (philotimeisthai = make it your ambition). WEB: "aspire to
       live quietly." The paradox: be AMBITIOUS about being QUIET.
       The Thessalonians had become busybodies due to eschatological
       excitement.

v.13 — NET: "we do not want you to be uninformed about those who
       are asleep, so that you will not grieve like the rest who
       have no hope" — "asleep" (koimOmenOn = sleeping — euphemism
       for death). WEB: "concerning those who have fallen asleep."
       Christian grief is not hopeless — it is informed by
       resurrection promise.

v.16 — NET: "the Lord himself will come down from heaven with a
       shout of command, with the voice of the archangel, and with
       the trumpet of God" — "shout of command" (en keleusmati =
       a military order). WEB: "with a shout." KJV: "with a shout."
       Three sounds: command, archangel's voice, trumpet. Military
       imagery — the King arrives.

v.17 — NET: "we who are alive, who are left, will be suddenly
       caught up together with them in the clouds to meet the Lord
       in the air" — "caught up" (harpagEsometha = snatched/seized
       — Latin: rapturo, English: rapture). WEB: "will be caught up
       together with them in the clouds." KJV: "shall be caught up
       together with them in the clouds." The only explicit rapture
       text in the NT."""

thess1[5] = """v.2  — NET: "the day of the Lord will come like a thief in the
       night" — "thief in the night" — unexpected to the unprepared.
       WEB: "the day of the Lord comes like a thief in the night."
       KJV: "the day of the Lord so cometh as a thief in the night."
       Not unexpected to believers (v.4: "you are not in darkness").

v.6  — NET: "let us not sleep as the rest do, but let us be alert
       and sober" — "alert" (grEgorOmen = stay awake/be watchful).
       WEB: "let's watch and be sober." KJV: "let us watch and be
       sober." Two contrasts: sleeping vs. watching, drunk vs. sober.
       Spiritual vigilance as lifestyle.

v.16 — NET: "Always rejoice" — two words in Greek (pantote
       chairete). The shortest verse in Greek. WEB: "Rejoice always."
       KJV: "Rejoice evermore." A command, not a suggestion — joy
       is obedience, not mere emotion.

v.17 — NET: "constantly pray" — "constantly" (adialeiptOs =
       without interruption). WEB: "Pray without ceasing." KJV:
       "Pray without ceasing." Not 24/7 formal prayer but an
       ongoing attitude of communication — breathing prayer
       throughout the day.

v.19 — NET: "Do not extinguish the Spirit" — "extinguish"
       (sbennyte = quench/put out fire). WEB: "Don't quench the
       Spirit." KJV: "Quench not the Spirit." The Spirit's work
       can be stifled/suppressed by human resistance — fire
       imagery requires fuel and oxygen."""

# 2 Thessalonians
thess2_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/14 - 2 Thessalonians"
thess2 = dict()
thess2[1] = """v.5  — NET: "This is evidence of God's righteous judgment, to
       make you worthy of the kingdom of God" — "evidence"
       (endeigma = proof/demonstration). WEB: "a clear sign of the
       righteous judgment of God." Their endurance under persecution
       PROVES God's justice — they are being refined.

v.7  — NET: "when the Lord Jesus is revealed from heaven with his
       mighty angels" — "revealed" (apokalypsei = apocalypse/
       unveiling). WEB: "when the Lord Jesus is revealed from heaven
       with his mighty angels." KJV: "when the Lord Jesus shall be
       revealed from heaven with his mighty angels." The Second
       Coming as an unveiling of hidden reality.

v.8  — NET: "with a flaming fire, inflicting punishment on those
       who do not know God" — "flaming fire" (en pyri phlogos).
       WEB: "in flaming fire." KJV: "In flaming fire." Theophany
       language — God's self-revelation in fire (Sinai, bush,
       Pentecost, judgment).

v.9  — NET: "They will undergo the penalty of eternal destruction,
       away from the presence of the Lord" — "eternal destruction"
       (olethron aiOnion). WEB: "eternal destruction from the face
       of the Lord." KJV: "everlasting destruction from the presence
       of the Lord." Separation from God as the essence of judgment.

v.10 — NET: "when he comes to be glorified among his saints" —
       "among his saints" (en tois hagiois autou). WEB: "to be
       glorified in his saints." KJV: "to be glorified in his
       saints." Christ glorified IN believers — they reflect His
       glory like mirrors."""

thess2[2] = """v.3  — NET: "that day will not come unless the rebellion comes
       first and the man of lawlessness is revealed" — "rebellion"
       (apostasia = apostasy/falling away). WEB: "unless the
       departure comes first." KJV: "except there come a falling
       away first." Whether "departure" means doctrinal apostasy
       or physical departure (rapture) is debated.

v.4  — NET: "He opposes and exalts himself above every so-called
       god or object of worship, and as a result he takes his seat
       in God's temple" — "takes his seat" (kathisai = sits down).
       WEB: "he sits as God in the temple of God." The man of
       lawlessness claims divine status — ultimate blasphemy.

v.7  — NET: "For the hidden power of lawlessness is already at
       work" — "hidden power" (mystErion tEs anomias = mystery of
       lawlessness). WEB: "the mystery of lawlessness already
       works." KJV: "the mystery of iniquity doth already work."
       Evil is active NOW but restrained — waiting for the right
       moment.

v.8  — NET: "the Lord will destroy him with the breath of his
       mouth" — "breath of his mouth" (tO pneumati tou stomatos
       autou). WEB: "whom the Lord will kill with the breath of his
       mouth." KJV: "whom the Lord shall consume with the spirit
       of his mouth." Christ's word alone destroys the antichrist —
       no battle required.

v.13 — NET: "God chose you from the beginning for salvation
       through sanctification by the Spirit and faith in the truth"
       — "from the beginning" (ap' archEs). Some manuscripts:
       "firstfruits" (aparchEn). WEB: "God chose you from the
       beginning." KJV: "God hath from the beginning chosen you."
       Election, sanctification, and faith together."""

thess2[3] = """v.3  — NET: "But the Lord is faithful, and he will strengthen
       you and guard you from the evil one" — "guard" (phylaxei =
       protect/keep). WEB: "the Lord is faithful, who will
       establish you and guard you from the evil one." God's
       faithfulness, not ours, is the ground of security.

v.6  — NET: "keep away from every brother who lives an undisciplined
       life" — "undisciplined" (ataktOs = out of order/disorderly —
       a military term for breaking ranks). WEB: "every brother who
       walks in rebellion." KJV: "every brother that walketh
       disorderly." Not moral scandal but refusal to work.

v.10 — NET: "if someone does not want to work, he should not eat"
       — "does not want" (ou thelei = is unwilling — not unable).
       WEB: "if anyone will not work, don't let him eat." KJV: "if
       any would not work, neither should he eat." The command
       targets willful idleness, not the disabled or unemployed.

v.13 — NET: "do not grow weary in doing what is right" — "grow
       weary" (enkakEsEte = lose heart/become discouraged). WEB:
       "don't be weary in doing well." KJV: "be not weary in well
       doing." Persistence in good despite the disobedience of
       others — don't let their failure stop your faithfulness.

v.15 — NET: "Do not regard him as an enemy but admonish him as a
       brother" — "admonish" (noutheteite = put sense into/correct
       by instruction). WEB: "admonish him as a brother." KJV:
       "admonish him as a brother." Discipline without dehumanization
       — the goal is restoration, not rejection."""

# Process all
for ch, note_text in sorted(col.items()):
    filepath = os.path.join(col_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Colossians " + str(ch))

for ch, note_text in sorted(thess1.items()):
    filepath = os.path.join(thess1_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done 1 Thess " + str(ch))

for ch, note_text in sorted(thess2.items()):
    filepath = os.path.join(thess2_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done 2 Thess " + str(ch))
