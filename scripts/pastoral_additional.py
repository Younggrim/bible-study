#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to 1 Tim, 2 Tim, Titus, Philemon."""
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

# 1 Timothy
tim1_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/15 - 1 Timothy"
tim1 = dict()
tim1[1] = """v.15 — NET: "Christ Jesus came into the world to save sinners
       — and I am the worst of them!" — "worst" (prOtos = first/
       chief). WEB: "of whom I am chief." KJV: "of whom I am
       chief." Paul doesn't say "was" but "am" — present tense
       humility, not just past-tense testimony.

v.17 — NET: "Now to the eternal king, immortal, invisible, the
       only God, be honor and glory forever and ever!" — "eternal
       king" (basilei tOn aiOnOn = king of the ages). WEB: "the
       King eternal." KJV: "the King eternal." A spontaneous
       doxology prompted by remembering his own salvation.

v.18 — NET: "fight the good fight" — "fight" (strateuE = wage
       warfare/campaign). WEB: "that you may wage the good warfare."
       KJV: "war a good warfare." Military language — Timothy is a
       soldier, not just a pastor.

v.19 — NET: "holding to faith and a good conscience, which some
       have rejected and so have suffered shipwreck in regard to
       the faith" — "shipwreck" (enauagEsan = suffered a wreck at
       sea). WEB: "made a shipwreck concerning the faith." Faith
       can be wrecked by abandoning conscience.

v.20 — NET: "Among these are Hymenaeus and Alexander, whom I
       handed over to Satan to be taught not to blaspheme" —
       "handed over to Satan" (paredOka tO satana) — excommunication
       with redemptive purpose (cf. 1 Cor 5:5). WEB: "delivered to
       Satan, that they might be taught not to blaspheme." Discipline
       as education."""

tim1[2] = """v.1  — NET: "I urge that requests, prayers, intercessions, and
       thanks be offered on behalf of all people" — four types of
       prayer: requests (deEseis), prayers (proseuchas), intercessions
       (enteuxeis), thanks (eucharistias). WEB: "petitions, prayers,
       intercessions, and givings of thanks." Comprehensive prayer
       vocabulary.

v.4  — NET: "who wants all people to be saved and to come to a
       knowledge of the truth" — "wants" (thelei = desires/wills).
       WEB: "who desires all people to be saved." KJV: "who will
       have all men to be saved." The scope of God's saving desire
       — universal intent, though not universal result.

v.5  — NET: "For there is one God and one intermediary between God
       and humanity, Christ Jesus, himself human" — "intermediary"
       (mesitEs = mediator/go-between). WEB: "one mediator between
       God and men." KJV: "one mediator between God and men." One
       God excludes polytheism; one mediator excludes all other
       intercessors.

v.6  — NET: "who gave himself as a ransom for all" — "ransom"
       (antilytron = substitutionary ransom price). WEB: "who gave
       himself as a ransom for all." KJV: "who gave himself a
       ransom for all." The "anti-" prefix emphasizes substitution:
       He paid IN PLACE OF all.

v.12 — NET: "But I do not allow a woman to teach or exercise
       authority over a man" — "exercise authority" (authentein =
       dominate/usurp authority — a rare word, debated meaning).
       WEB: "not to exercise authority over a man." KJV: "nor to
       usurp authority over the man." The meaning of authenteO is
       the crux of the complementarian/egalitarian debate."""

tim1[3] = """v.1  — NET: "If someone aspires to the office of overseer, he
       desires a good work" — "aspires" (oregetai = reaches for/
       stretches toward). WEB: "If a man seeks the office of an
       overseer, he desires a good work." The desire for leadership
       is good — what follows are the qualifications.

v.2  — NET: "The overseer then must be above reproach" — "above
       reproach" (anepilEmpton = not able to be seized upon/
       blameless). WEB: "without reproach." KJV: "blameless." Not
       sinless perfection but no legitimate accusation that sticks.

v.6  — NET: "He must not be a recent convert or he may become
       arrogant" — "recent convert" (neophyton = newly planted —
       English "neophyte"). WEB: "not a new convert." KJV: "not a
       novice." New believers need time to develop proven character
       before leading.

v.15 — NET: "the church of the living God, the support and
       bulwark of the truth" — "support and bulwark" (stylos kai
       hedraiOma = pillar and foundation). WEB: "the pillar and
       ground of the truth." KJV: "the pillar and ground of the
       truth." The church upholds truth in the world.

v.16 — NET: "He was revealed in the flesh, vindicated by the
       Spirit" — possibly an early hymn fragment. Textual variant:
       "God" (theos, KJV) vs. "He who" (hos, NET/ESV). WEB: "God
       was revealed in the flesh." The earliest manuscripts read
       "who" (hos); later ones "God" (theos) — one letter
       difference in Greek uncials."""

tim1[4] = """v.1  — NET: "the Spirit explicitly says that in the later times
       some will desert the faith" — "explicitly" (rhEtOs = in
       express words/clearly). WEB: "the Spirit says expressly."
       KJV: "the Spirit speaketh expressly." The Spirit gives clear
       warning — apostasy is predicted, not surprising.

v.4  — NET: "everything God created is good, and no food is to
       be rejected if it is received with thanksgiving" — "received
       with thanksgiving" (meta eucharistias lambanomenon). WEB:
       "nothing is to be rejected, if it is received with
       thanksgiving." Echoes Genesis 1 — creation is good.

v.7  — NET: "But reject those myths fit only for the godless and
       gullible, and train yourself for godliness" — "train"
       (gymnaze = exercise/train — English "gymnasium"). WEB:
       "exercise yourself toward godliness." KJV: "exercise thyself
       rather unto godliness." Athletic discipline applied to
       spiritual growth.

v.12 — NET: "Let no one look down on you because you are young,
       but set an example for the believers in speech, in conduct"
       — "young" (neotEtos = youth). WEB: "Let no man despise your
       youth." Timothy was likely in his 30s — young for the
       authority he carried. Combat disdain with exemplary living.

v.14 — NET: "Do not neglect the spiritual gift you have" —
       "spiritual gift" (charismatos = grace-gift). WEB: "Don't
       neglect the gift that is in you." KJV: "Neglect not the
       gift that is in thee." Gifts require cultivation — they can
       be neglected into dormancy."""

tim1[5] = """v.1  — NET: "Do not address an older man harshly but appeal to
       him as a father" — "appeal" (parakalei = encourage/exhort
       gently). WEB: "Don't rebuke an older man, but exhort him
       as a father." KJV: "Rebuke not an elder, but intreat him
       as a father." Age-appropriate pastoral care.

v.8  — NET: "But if someone does not provide for his own relatives
       and especially his immediate family, he has denied the faith
       and is worse than an unbeliever" — "worse than an unbeliever"
       (apistos cheirOn) — even pagans care for family. WEB: "worse
       than an unbeliever." Neglecting family is faith-denial.

v.17 — NET: "Elders who provide effective leadership must be
       counted worthy of double honor" — "double honor" (diplEs
       timEs = double compensation/respect). WEB: "counted worthy
       of double honor." KJV: "worthy of double honour." This
       includes financial support (v.18 — "the laborer is worthy
       of his wages").

v.22 — NET: "Do not lay hands on anyone hastily" — "hastily"
       (tacheOs = quickly/prematurely). WEB: "Lay hands hastily on
       no one." KJV: "Lay hands suddenly on no man." Ordination
       should not be rushed — premature endorsement shares in
       another's potential sins.

v.23 — NET: "use a little wine because of your stomach and your
       frequent illnesses" — a personal aside: Timothy had health
       issues. WEB: "use a little wine for your stomach's sake."
       Paul's pragmatism — neither total abstinence nor excess,
       but medicinal use."""

tim1[6] = """v.6  — NET: "godliness with contentment is great gain" —
       "contentment" (autarkeias = self-sufficiency/satisfaction
       with what one has). WEB: "godliness with contentment is
       great gain." KJV: "godliness with contentment is great
       gain." The combination — not godliness alone, not
       contentment alone, but both together.

v.10 — NET: "For the love of money is the root of all evils" —
       "root of ALL evils" (rhiza pantOn tOn kakOn). WEB: "the
       love of money is a root of all kinds of evil." KJV: "the
       love of money is the root of all evil." Note: love of money,
       not money itself. NET/KJV: "all evils"; WEB: "all kinds of
       evil" — the scope is debated.

v.12 — NET: "Compete well for the faith and be grasped by eternal
       life" — "compete" (agOnizou = agonize/strive). WEB: "Fight
       the good fight of faith." KJV: "Fight the good fight of
       faith." Athletic/military imagery — active exertion, not
       passive reception.

v.15 — NET: "the blessed and only Sovereign, the King of kings
       and Lord of lords" — "Sovereign" (dynastEs = Potentate/
       Ruler). WEB: "the blessed and only Ruler." KJV: "the
       blessed and only Potentate." A title later applied to
       Christ (Rev 19:16) here applied to God.

v.20 — NET: "guard what has been entrusted to you" — "what has
       been entrusted" (tEn parathEkEn = the deposit). WEB: "guard
       that which is committed to you." KJV: "keep that which is
       committed to thy trust." The gospel is a deposit to be
       guarded, not a product to be innovated upon."""

# 2 Timothy
tim2_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/16 - 2 Timothy"
tim2 = dict()
tim2[1] = """v.7  — NET: "For God did not give us a Spirit of fear but of
       power and love and self-control" — "self-control" (sOphronismou
       = sound mind/discipline). KJV: "a sound mind." WEB: "self-
       control." Three positive gifts replacing fear: power (dynamis),
       love (agapE), sound mind (sOphronismos).

v.12 — NET: "I am not ashamed, because I know the one in whom I
       have believed, and I am confident that he is able to guard
       what has been entrusted to me until that day" — "guard what
       has been entrusted" (tEn parathEkEn mou phylaxai). WEB:
       "guard that which I have committed to him." KJV: "keep that
       which I have committed unto him." God guards the deposit.

v.13 — NET: "Hold to the standard of sound words that you heard
       from me" — "standard" (hypotypOsin = pattern/outline/model).
       WEB: "Hold the pattern of sound words." KJV: "Hold fast the
       form of sound words." A template of healthy teaching to be
       maintained.

v.14 — NET: "Guard that good thing entrusted to you, through the
       Holy Spirit who lives within us" — "through the Holy Spirit"
       — the deposit is guarded not by human effort alone but by
       the indwelling Spirit. WEB: "by the Holy Spirit who dwells
       in us." Human faithfulness + divine power.

v.16 — NET: "May the Lord grant mercy to the household of
       Onesiphorus, because he often refreshed me and was not
       ashamed of my imprisonment" — "refreshed" (anepsyxen =
       revived/cooled like a breeze). WEB: "he often refreshed me."
       KJV: "he oft refreshed me." A beautiful word — like cool
       air to someone overheated."""

tim2[2] = """v.2  — NET: "entrust to faithful people who will be competent
       to teach others as well" — "entrust" (parathou = deposit/
       commit). WEB: "commit to faithful men." KJV: "commit thou
       to faithful men." Four generations of transmission: Paul,
       Timothy, faithful men, others also. Multiplication.

v.4  — NET: "No one serving in the army gets entangled in matters
       of everyday life; otherwise he will not please the one who
       recruited him" — "entangled" (empleketai = woven into/
       entangled). WEB: "No soldier on duty entangles himself in
       the affairs of life." Single-minded focus for the soldier.

v.15 — NET: "Make every effort to present yourself before God as
       a proven worker... who correctly handles the word of truth"
       — "correctly handles" (orthotomounta = cuts straight). KJV:
       "rightly dividing the word of truth." WEB: "handling
       aright the word of truth." The metaphor may be cutting
       straight furrows or cutting stone precisely.

v.19 — NET: "The Lord knows those who are his" — quoting Numbers
       16:5. WEB: "The Lord knows those who are his." KJV: "The
       Lord knoweth them that are his." God's knowledge of His own
       is the foundation of assurance — not our knowledge of
       ourselves.

v.25 — NET: "perhaps God will grant them repentance and then
       knowledge of the truth" — "grant repentance" (dOE metanoian
       = give repentance as a gift). WEB: "God may perhaps give
       them repentance leading to a knowledge of the truth."
       Repentance is God's gift, not just human decision."""

tim2[3] = """v.1  — NET: "in the last days difficult times will come" —
       "difficult" (chalepoi = fierce/hard to bear/dangerous). WEB:
       "In the last days, grievous times will come." KJV: "perilous
       times shall come." The same word describes the Gadarene
       demoniacs (Matt 8:28) — savage, fierce times.

v.5  — NET: "They will maintain the outward appearance of
       religion but will have repudiated its power" — "outward
       appearance" (morphOsin = form/shape without substance). WEB:
       "holding a form of godliness, but having denied its power."
       KJV: "Having a form of godliness, but denying the power
       thereof." Religious exterior, empty interior.

v.12 — NET: "all who desire to live godly lives in Christ Jesus
       will be persecuted" — "all" (pantes) — no exceptions. WEB:
       "all who desire to live godly in Christ Jesus will suffer
       persecution." KJV: "all that will live godly in Christ Jesus
       shall suffer persecution." Guaranteed, not possible.

v.16 — NET: "Every scripture is inspired by God and useful for
       teaching, for reproof, for correction, and for training in
       righteousness" — "inspired" (theopneustos = God-breathed).
       WEB: "Every Scripture is God-breathed." KJV: "All scripture
       is given by inspiration of God." Not that God breathed INTO
       Scripture but that Scripture is breathed OUT by God.

v.17 — NET: "that the person dedicated to God may be capable and
       equipped for every good work" — "capable" (artios = complete/
       fit/ready). WEB: "complete, thoroughly equipped for every
       good work." KJV: "perfect, throughly furnished." Scripture's
       purpose: producing equipped people for God's work."""

tim2[4] = """v.2  — NET: "Preach the message, be ready whether it is
       convenient or not" — "be ready" (epistEthi = stand by/be at
       hand/be urgent). WEB: "be urgent in season and out of
       season." KJV: "be instant in season, out of season." Not
       just when it's comfortable or welcome.

v.3  — NET: "For there will be a time when people will not
       tolerate sound teaching" — "tolerate" (anechontai = put up
       with/endure). WEB: "they will not listen to the sound
       doctrine." KJV: "they will not endure sound doctrine."
       Doctrinal intolerance as a sign of the times.

v.6  — NET: "I am already being poured out as an offering, and
       the time for me to depart is at hand" — "poured out"
       (spendomai = drink offering being poured). WEB: "I am
       already being offered." KJV: "I am now ready to be offered."
       Paul's death as a sacrificial libation — voluntary, worship.

v.7  — NET: "I have competed well; I have finished the race; I
       have kept the faith!" — "competed" (agonismai = fought the
       contest). WEB: "I have fought the good fight." KJV: "I have
       fought a good fight." Three perfect tenses: the contest is
       over, the race is done, the faith is intact.

v.8  — NET: "a crown of righteousness awaits me, which the Lord,
       the righteous Judge, will award to me on that day" — "crown"
       (stephanos = victor's wreath, not diadEma/royal crown). WEB:
       "the crown of righteousness." Not earned by merit but
       awarded by the righteous Judge to all who love His appearing."""

# Titus
titus_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/17 - Titus"
titus = dict()
titus[1] = """v.2  — NET: "in hope of eternal life, which God, who does not
       lie, promised before time began" — "who does not lie" (ho
       apseudEs theos = the non-lying God). WEB: "God, who can't
       lie." KJV: "God, that cannot lie." God's truthfulness as
       the foundation of hope — the promise precedes creation.

v.5  — NET: "to set in order the remaining matters and to appoint
       elders in every town" — "set in order" (epidiorthOsE =
       straighten out/correct what remains). WEB: "set in order
       the things that were lacking." KJV: "set in order the things
       that are wanting." Titus is a church organizer/troubleshooter.

v.9  — NET: "holding to the faithful message as taught" — "faithful
       message" (tou pistos logou = the trustworthy word). WEB:
       "holding to the faithful word." KJV: "holding fast the
       faithful word." Elders must both believe AND teach sound
       doctrine — offensive and defensive roles.

v.12 — NET: "'Cretans are always liars, evil beasts, lazy
       gluttons'" — Paul quotes Epimenides (a Cretan poet/prophet).
       WEB: "Cretans are always liars, evil beasts, and idle
       gluttons." Using a pagan source to confirm cultural
       observation — and Paul says "this testimony is true" (v.13).

v.15 — NET: "All is pure to those who are pure. But to those who
       are corrupt and unbelieving, nothing is pure" — "nothing is
       pure" (ouden katharon). WEB: "to those who are defiled and
       unbelieving, nothing is pure." Internal corruption
       contaminates everything it touches — the problem is the
       person, not the thing."""

titus[2] = """v.5  — NET: "so that the message of God may not be discredited"
       — "discredited" (blasphEmEtai = blasphemed/slandered). WEB:
       "that God's word may not be blasphemed." KJV: "that the word
       of God be not blasphemed." Bad behavior by believers gives
       outsiders ammunition against the gospel.

v.11 — NET: "For the grace of God has appeared, bringing salvation
       to all people" — "appeared" (epephanE = shined forth/became
       visible — an epiphany). WEB: "the grace of God has appeared."
       KJV: "the grace of God that bringeth salvation hath appeared."
       Grace personified — it appeared in Christ.

v.12 — NET: "training us to reject godless ways and worldly
       desires and to live self-controlled, upright, and godly
       lives" — "training" (paideuousa = educating/disciplining as
       a child). WEB: "instructing us." KJV: "teaching us." Grace
       doesn't just forgive — it TRAINS. Three dimensions: self-
       ward (self-controlled), other-ward (upright), God-ward (godly).

v.13 — NET: "as we wait for the happy fulfillment of our hope in
       the glorious appearing of our great God and Savior, Jesus
       Christ" — "our great God and Savior, Jesus Christ" (tou
       megalou theou kai sOtEros hEmOn IEsou Christou) — a direct
       affirmation of Christ's deity. WEB: "our great God and
       Savior, Jesus Christ." Granville Sharp rule applies.

v.14 — NET: "who gave himself for us to set us free from every
       kind of lawlessness and to purify for himself a people who
       are truly his" — "truly his" (periousion = His own special
       possession). WEB: "a people for his own possession." KJV:
       "a peculiar people." Echoes Exodus 19:5 — Israel's
       identity now applied to the church."""

titus[3] = """v.3  — NET: "For we too were once foolish, disobedient,
       misled, enslaved to various passions and desires" — "we too"
       (Emen... kai hEmeis = we ourselves also). WEB: "For we were
       also once foolish." The "we" prevents self-righteousness —
       Paul includes himself in the pre-conversion description.

v.4  — NET: "But when the kindness of God our Savior and his love
       for mankind appeared" — "love for mankind" (philanthrOpia =
       philanthropy). WEB: "the kindness of God our Savior and his
       love toward mankind appeared." KJV: "the kindness and love
       of God our Saviour toward man appeared." God is a
       philanthropist — He loves humanity.

v.5  — NET: "he saved us not by works of righteousness that we
       have done but on the basis of his mercy, through the washing
       of the new birth and the renewing of the Holy Spirit" —
       "washing of the new birth" (loutrou palingenesias = bath of
       regeneration). WEB: "the washing of regeneration." KJV:
       "the washing of regeneration." Baptismal language connected
       to spiritual rebirth — the relationship is debated.

v.8  — NET: "This saying is trustworthy" — "trustworthy" (pistos
       ho logos = faithful is the word — a Pastoral Epistles
       formula). WEB: "This saying is faithful." KJV: "This is a
       faithful saying." Paul uses this formula five times in the
       Pastorals to mark key doctrinal statements.

v.10 — NET: "Reject a divisive person after one or two warnings"
       — "divisive person" (hairetikon anthrOpon = factious/
       heretical person). WEB: "Avoid a man who is causing
       divisions." KJV: "A man that is an heretick after the first
       and second admonition reject." Two chances, then separation."""

# Philemon
phm_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/18 - Philemon"
phm = dict()
phm[1] = """v.10 — NET: "I am appealing to you concerning my child,
       Onesimus, whose father I have become during my imprisonment"
       — "my child" (tou emou teknou = my begotten one). WEB: "my
       child, Onesimus." Paul converted Onesimus in prison — he
       is a spiritual father sending his son back.

v.11 — NET: "who was formerly useless to you, but is now useful
       to you and to me" — "useless/useful" (achrEston/euchrEston)
       — a wordplay on Onesimus' name which means "useful/
       profitable." WEB: "who once was useless to you, but now is
       useful." The runaway slave now lives up to his name.

v.15 — NET: "Perhaps this is the reason he was separated from you
       for a while, so that you would have him back forever" —
       "separated" (echOristhE = passive — was separated, perhaps
       by God's providence). WEB: "perhaps he was therefore
       separated from you for a while." Paul reframes the escape as
       providence — temporary loss for eternal gain.

v.16 — NET: "no longer as a slave, but more than a slave, as a
       dear brother" — "dear brother" (adelphon agapEton = beloved
       brother). WEB: "no longer as a slave, but more than a slave,
       a beloved brother." The gospel doesn't just reform social
       structures — it transforms relationships at the identity level.

v.18 — NET: "if he has done anything wrong to you or owes you
       anything, charge it to my account" — "charge to my account"
       (touto emoi elloga = reckon this to me). WEB: "put that to
       my account." KJV: "put that on mine account." Paul models
       substitutionary atonement — he takes Onesimus' debt on
       himself. A picture of what Christ does for us."""

# Process all
for ch, note_text in sorted(tim1.items()):
    filepath = os.path.join(tim1_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done 1 Tim " + str(ch))

for ch, note_text in sorted(tim2.items()):
    filepath = os.path.join(tim2_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done 2 Tim " + str(ch))

for ch, note_text in sorted(titus.items()):
    filepath = os.path.join(titus_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Titus " + str(ch))

for ch, note_text in sorted(phm.items()):
    filepath = os.path.join(phm_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Philemon " + str(ch))
