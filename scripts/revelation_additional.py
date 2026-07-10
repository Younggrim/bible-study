#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Revelation chapters."""
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

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/27 - Revelation"
notes = dict()

notes[1] = """v.1  — NET: "The revelation of Jesus Christ, which God gave
       him to show his servants what must happen very soon" —
       "revelation" (apokalypsis = unveiling/disclosure). WEB:
       "The Revelation of Jesus Christ." KJV: "The Revelation of
       Jesus Christ." Not revelations (plural) but one singular
       unveiling of Christ in glory.

v.5  — NET: "To the one who loves us and has set us free from our
       sins at the cost of his own blood" — "set us free" (lysanti
       = loosed/released). Textual variant: "washed" (lousanti,
       KJV) vs. "freed" (lysanti, NET/ESV/WEB). WEB: "freed us
       from our sins." One letter difference in Greek — both
       theologically true.

v.7  — NET: "Look! He is returning with the clouds, and every eye
       will see him" — "returning with the clouds" (erchetai meta
       tOn nephelOn). WEB: "he is coming with the clouds." KJV:
       "he cometh with clouds." Echoing Daniel 7:13 — visible,
       public, undeniable return.

v.8  — NET: "I am the Alpha and the Omega... the one who is, and
       who was, and who is coming, the All-Powerful" — "All-Powerful"
       (pantokratOr = Almighty/ruler of all). WEB: "the Almighty."
       KJV: "the Almighty." The divine self-identification spans
       all time and holds all power.

v.17 — NET: "Do not be afraid! I am the first and the last" —
       "Do not be afraid" (mE phobou). WEB: "Don't be afraid."
       KJV: "Fear not." John falls as dead before the glorified
       Christ — the same Jesus who said "Fear not" during His
       earthly ministry says it again from heaven."""

notes[2] = """v.4  — NET: "you have left your first love" — "left"
       (aphEkes = abandoned/forsaken). WEB: "you left your first
       love." KJV: "thou hast left thy first love." Ephesus had
       orthodoxy and labor but lost passionate devotion — activity
       without affection.

v.7  — NET: "To the one who conquers, I will permit him to eat
       from the tree of life" — "conquers" (tO nikOnti = the one
       who overcomes/is victorious). WEB: "To him who overcomes."
       KJV: "To him that overcometh." Each of the seven letters
       ends with a promise to the overcomer.

v.10 — NET: "Do not be afraid of the things you are about to
       suffer... Be faithful until death, and I will give you the
       crown of life" — "crown" (stephanon = victor's wreath).
       WEB: "the crown of life." KJV: "a crown of life." Smyrna
       receives no rebuke — only encouragement for coming
       martyrdom.

v.17 — NET: "I will give him some of the hidden manna, and I will
       give him a white stone, and on that stone will be written a
       new name" — "white stone" (psEphon leukEn) — debated:
       acquittal stone? admission ticket? victory token? Personal
       intimacy — a name known only to the recipient and Christ.

v.26 — NET: "the one who conquers and who continues in my deeds
       until the end, I will give him authority over the nations"
       — "authority over the nations" (exousian epi tOn ethnOn).
       WEB: "authority over the nations." Quoting Psalm 2:9 —
       believers share in Christ's messianic rule."""

notes[3] = """v.1  — NET: "you have a reputation that you are alive, but in
       reality you are dead" — "reputation" (onoma = name). WEB:
       "you have a reputation of being alive." KJV: "thou hast a
       name that thou livest." Sardis had fame without substance —
       all reputation, no reality.

v.5  — NET: "I will never erase his name from the book of life"
       — "never erase" (ou mE exaleipsO = absolutely will not blot
       out — double negative). WEB: "I will in no way blot his
       name out of the book of life." The strongest possible
       assurance of security for the overcomer.

v.8  — NET: "I have put before you an open door that no one can
       shut" — "open door" (thyran aneOgmenEn = a door standing
       opened). WEB: "I have set before you an open door." KJV:
       "I have set before thee an open door." Philadelphia — small
       strength but great faithfulness. God opens what no one
       can close.

v.15 — NET: "because you are lukewarm, and neither hot nor cold,
       I am going to vomit you out of my mouth" — "vomit" (emesai
       = spew/vomit). WEB: "I will vomit you out of my mouth."
       KJV: "I will spue thee out of my mouth." Laodicea — their
       lukewarm water (unlike Colossae's cold or Hierapolis' hot)
       nauseates Christ.

v.20 — NET: "Listen! I am standing at the door and knocking!" —
       "standing" (hestEka = I have taken my stand — perfect tense:
       settled position). WEB: "I stand at the door and knock."
       KJV: "Behold, I stand at the door, and knock." Christ
       outside His own church, seeking entry. The door handle is
       on the inside."""

notes[4] = """v.1  — NET: "After these things I looked, and there was a door
       standing open in heaven!" — "standing open" (aneOgmenE =
       opened and remaining open — perfect participle). WEB: "a
       door opened in heaven." The door opened for John gives
       readers access to heaven's perspective.

v.3  — NET: "the one seated on it was like jasper and carnelian
       in appearance" — "jasper" (iaspidi = likely diamond/clear
       crystal) and "carnelian" (sardiO = blood-red stone). WEB:
       "like a jasper stone and a sardius." God described in
       reflected light, not direct form — no anthropomorphism.

v.6  — NET: "In the middle of the throne and around the throne
       were four living creatures full of eyes in front and in
       back" — "living creatures" (zOa = living ones — not thEria/
       beasts). WEB: "four living creatures." KJV: "four beasts."
       NET/WEB correctly avoid "beasts" — these are exalted beings,
       not animals.

v.8  — NET: "Holy, Holy, Holy is the Lord God, the All-Powerful,
       Who was and who is, and who is still to come!" — the
       trisagion (thrice-holy). WEB: "Holy, holy, holy is the Lord
       God, the Almighty." KJV: "Holy, holy, holy, Lord God
       Almighty." Echoing Isaiah 6:3 — ceaseless worship (they
       never stop, day or night).

v.11 — NET: "You are worthy, our Lord and God, to receive glory
       and honor and power, since you created all things" — "you
       created" (ektisas = you brought into being). WEB: "You
       created all things." Creation as the ground of worship —
       God is worshipped because He is Creator."""

notes[5] = """v.5  — NET: "the Lion of the tribe of Judah, the root of
       David, has conquered" — "Lion" and "root" — messianic
       titles from Genesis 49:9 and Isaiah 11:1/10. WEB: "the
       Lion who is of the tribe of Judah." But when John LOOKS,
       he sees a LAMB (v.6) — the Lion conquers as a Lamb.

v.6  — NET: "a Lamb standing as though it had been killed" —
       "as though killed" (hOs esphagmenon = as having been
       slaughtered). WEB: "a Lamb standing, as though it had been
       slain." KJV: "a Lamb as it had been slain." The Lamb bears
       permanent marks of slaughter yet stands alive — resurrection
       body with crucifixion scars.

v.9  — NET: "You are worthy to take the scroll and to open its
       seals because you were killed, and at the cost of your own
       blood you have purchased for God persons from every tribe"
       — "purchased" (Egorasas = bought in the marketplace). WEB:
       "you bought us for God with your blood." Redemption as
       commercial transaction — the Lamb's blood as purchase price.

v.12 — NET: "Worthy is the Lamb who was killed to receive power
       and wealth and wisdom and might and honor and glory and
       praise!" — seven attributes (power, wealth, wisdom, might,
       honor, glory, praise). WEB: "Worthy is the Lamb who has
       been killed." Seven = completeness. The Lamb deserves ALL.

v.13 — NET: "To the one seated on the throne and to the Lamb be
       praise and honor and glory and ruling power forever" —
       "to the one on the throne AND to the Lamb" — equal worship
       to God and Christ. WEB: "To him who sits on the throne, and
       to the Lamb." Co-worship = co-deity."""

notes[6] = """v.2  — NET: "a white horse, and the one seated on it had a
       bow" — "white horse" (hippos leukos). WEB: "a white horse."
       KJV: "a white horse." Debated: Christ? Antichrist? Conquest
       in general? The crown given (not inherent) and the bow
       suggest a counterfeit conqueror.

v.9  — NET: "the souls of those who had been violently killed
       because of the word of God" — "violently killed" (esphagmenOn
       = slaughtered — same word used of the Lamb in 5:6). WEB:
       "the souls of those who had been killed." Martyrs share
       the Lamb's experience of slaughter.

v.10 — NET: "How long, Sovereign Master, holy and true, before
       you judge those who live on the earth and avenge our blood?"
       — "Sovereign Master" (ho despotEs = absolute ruler). WEB:
       "How long, Master, the holy and true." KJV: "How long, O
       Lord, holy and true." The martyrs' prayer for justice —
       not revenge but vindication.

v.12 — NET: "the full moon became blood red" — "blood red" (hOs
       haima = as blood). WEB: "the whole moon became as blood."
       KJV: "the moon became as blood." Cosmic collapse at the
       sixth seal — sun dark, moon blood, stars falling, sky
       rolled up.

v.17 — NET: "the great day of their wrath has come, and who is
       able to withstand it?" — "their wrath" (tEs orgEs autOn =
       the wrath of BOTH the Father and the Lamb). WEB: "the great
       day of his wrath has come." Some manuscripts: "his" (singular);
       others: "their" (plural). The Lamb has wrath — a terrifying
       paradox."""

notes[7] = """v.3  — NET: "Do not damage the earth or the sea or the trees
       until we have put a seal on the foreheads of the servants
       of our God" — "seal" (sphragisOmen = stamp with a mark of
       ownership/protection). WEB: "until we have sealed the
       bondservants of our God." Divine marking before judgment
       falls — protection for God's own.

v.9  — NET: "a large crowd that no one could count, from every
       nation, tribe, people, and language" — "no one could count"
       (arithmEsai auton oudeis edynato). WEB: "a great multitude,
       which no man could count." The redeemed are innumerable —
       God's saving purpose succeeds on a massive scale.

v.14 — NET: "These are the ones who have come out of the great
       tribulation. They have washed their robes and made them
       white in the blood of the Lamb" — "washed... in blood" —
       paradox: blood that whitens. WEB: "washed their robes, and
       made them white in the Lamb's blood." Purity through
       sacrifice, not self-effort.

v.16 — NET: "They will never go hungry or be thirsty again, and
       the sun will not beat down on them" — echoing Isaiah 49:10.
       WEB: "They will never be hungry or thirsty any more." The
       end of all deprivation — reversing the sufferings of
       earthly tribulation.

v.17 — NET: "the Lamb in the middle of the throne will shepherd
       them and lead them to springs of living water" — "shepherd"
       (poimanei = tend/feed/guide). WEB: "the Lamb who is in the
       middle of the throne will be their shepherd." The slain Lamb
       becomes the Shepherd — imagery from Psalm 23 and John 10
       consummated in eternity."""

notes[8] = """v.1  — NET: "Now when the Lamb opened the seventh seal there
       was silence in heaven for about half an hour" — "silence"
       (sigE = hush). WEB: "there was silence in heaven for about
       half an hour." The only silence in heaven in all of
       Revelation — dramatic pause before the final judgments.
       Even angels hold their breath.

v.3  — NET: "he was given a large amount of incense to offer up,
       with the prayers of all the saints" — "with the prayers"
       (tais proseuchais tOn hagiOn). WEB: "with the prayers of
       all the saints." Prayers of the saints rise as incense to
       God's throne — they are heard and they trigger action (v.5).

v.5  — NET: "the angel took the censer, filled it with fire from
       the altar, and threw it on the earth" — prayers answered
       with fire — the saints' cries for justice (6:10) now
       produce thunders, flashes, earthquake. WEB: "threw it to
       the earth." Prayer produces cosmic consequences.

v.11 — NET: "The name of the star is Wormwood" — "Wormwood"
       (ho Apsinthos = bitter herb/absinthe). WEB: "The name of
       the star is called Wormwood." KJV: "the name of the star
       is called Wormwood." Bitterness poisons the waters — a
       third of rivers made deadly.

v.13 — NET: "Woe! Woe! Woe to those who live on the earth" —
       triple "woe" (ouai ouai ouai) — one for each remaining
       trumpet. WEB: "Woe! Woe! Woe to those who dwell on the
       earth." The worst is yet to come — the first four trumpets
       are preliminary to the final three."""

notes[9] = """v.1  — NET: "a star that had fallen from heaven to earth, and
       he was given the key to the shaft of the abyss" — "a star
       fallen" (astera peptOkota = a star having fallen — perfect
       participle). WEB: "a star from the sky which had fallen."
       Not a meteorite but a personal being (given a key) —
       likely a fallen angel.

v.3  — NET: "locusts came out of the smoke onto the earth" —
       "locusts" (akrides) — but not ordinary locusts (v.4: they
       don't harm vegetation). WEB: "out of the smoke came
       locusts." Demonic beings in locust form — tormenting but
       not killing.

v.6  — NET: "In those days people will seek death, but will not
       be able to find it; they will long to die, but death will
       flee from them" — "death will flee" (pheuxetai ho thanatos).
       WEB: "death will flee from them." A terrifying inversion —
       death itself becomes unattainable. Suffering without the
       escape of dying.

v.11 — NET: "whose name in Hebrew is Abaddon, and in Greek,
       Apollyon" — both names mean "Destroyer." WEB: "In Hebrew,
       Abaddon, but in Greek, Apollyon." KJV: "Abaddon... Apollyon."
       Named in two languages for both audiences — the king over
       the abyss army.

v.20 — NET: "The rest of humanity, who had not been killed by
       these plagues, did not repent" — "did not repent" (ou
       metenoEsan = refused to change their minds). WEB: "didn't
       repent." The purpose of judgment is repentance (cf. 16:9,
       11) — but humanity refuses. Hardened beyond response."""

notes[10] = """v.1  — NET: "I saw another powerful angel descending from heaven,
       wrapped in a cloud, with a rainbow above his head" —
       "powerful angel" (angelon ischyron = a strong angel). WEB:
       "a mighty angel coming down out of the sky." Not Christ
       (angels are sent; Christ sends) but a glorious messenger.

v.6  — NET: "there will be no more delay!" — "no more delay"
       (chronos ouketi estai = time will be no more/no more time).
       WEB: "there will no longer be delay." KJV: "there should be
       time no longer." Debated: no more delay before judgment? or
       time itself ceasing? Context favors: no further postponement.

v.7  — NET: "the mystery of God is completed, just as he
       announced to his servants the prophets" — "mystery"
       (mystErion = hidden plan now revealed). WEB: "the mystery
       of God is finished." KJV: "the mystery of God should be
       finished." God's secret plan reaches its culmination.

v.9  — NET: "Take the scroll and eat it. It will be bitter in
       your stomach, but sweet as honey in your mouth" — "eat it"
       (kataphage = devour/consume completely). WEB: "Take it, and
       eat it up." Echoing Ezekiel 3:1-3 — internalizing God's
       word. Sweet truth contains bitter content (judgment).

v.11 — NET: "You must prophesy again about many peoples, nations,
       languages, and kings" — "must" (dei = divine necessity).
       WEB: "You must prophesy again." John's commission is not
       finished — more revelation follows. The universal scope
       continues."""

notes[11] = """v.3  — NET: "I will grant my two witnesses authority to
       prophesy for 1,260 days" — "1,260 days" = 42 months = 3.5
       years (the symbolic half-week of Daniel 9:27). WEB: "my two
       witnesses will prophesy one thousand two hundred sixty days."
       Their identity is debated: Moses/Elijah? the church? two
       individuals?

v.7  — NET: "the beast that comes up from the abyss will make war
       on them and conquer them and kill them" — "the beast" (to
       thErion) — first appearance of this major figure. WEB: "the
       beast that comes up out of the abyss." The witnesses are
       invincible during their ministry (v.5) but killed at its end.

v.11 — NET: "after three and a half days a breath of life from
       God entered them and they stood on their feet" — "breath of
       life" (pneuma zOEs = spirit of life). WEB: "the breath of
       life from God entered into them." Echoing Ezekiel 37 (dry
       bones) — resurrection before their enemies' eyes.

v.15 — NET: "The kingdom of the world has become the kingdom of
       our Lord and of his Christ, and he will reign forever and
       ever" — "kingdom of the world" (hE basileia tou kosmou —
       singular: one kingdom transferred). WEB: "The kingdom of
       the world has become the Kingdom of our Lord." KJV: "The
       kingdoms of this world." The seventh trumpet's climactic
       announcement.

v.18 — NET: "the time has come to destroy those who destroy the
       earth" — "destroy those who destroy" (diaphtheirai tous
       diaphtheirontas). WEB: "to destroy those who destroy the
       earth." Judgment matches crime — those who corrupt creation
       are themselves destroyed."""

notes[12] = """v.1  — NET: "a woman clothed with the sun, and with the moon
       under her feet" — "clothed with the sun" (peribeblEmenE ton
       hElion). WEB: "a woman clothed with the sun." Israel/the
       church/Mary? — the imagery draws from Genesis 37:9 (Joseph's
       dream) suggesting Israel giving birth to the Messiah.

v.5  — NET: "She gave birth to a son, a male child, who is going
       to rule all the nations with an iron rod" — "iron rod"
       (rhabdO sidEra — quoting Psalm 2:9). WEB: "a son, a male
       child, who is to rule all the nations with a rod of iron."
       The child is Christ — born, ascended (caught up to God's
       throne).

v.7  — NET: "Then war broke out in heaven: Michael and his angels
       fought against the dragon" — "war" (polemos = battle/
       warfare). WEB: "There was war in heaven." KJV: "there was
       war in heaven." Michael leads heaven's armies; Satan and his
       angels are defeated and cast down permanently.

v.11 — NET: "they conquered him by the blood of the Lamb and by
       the word of their testimony, and they did not love their
       lives so much that they were afraid to die" — three weapons:
       blood (Christ's sacrifice), testimony (their witness), and
       willingness to die. WEB: "They overcame him." Martyrdom as
       victory, not defeat.

v.17 — NET: "the dragon became enraged at the woman and went away
       to make war on the rest of her children" — "the rest of her
       children" (tOn loipOn tou spermatos autEs = the remainder
       of her seed). WEB: "went away to make war with the rest of
       her offspring." Believers as targets — those who keep God's
       commandments and hold to Jesus' testimony."""

notes[13] = """v.1  — NET: "I saw a beast coming up out of the sea. It had
       ten horns and seven heads" — "out of the sea" (ek tEs
       thalassEs). WEB: "a beast coming up out of the sea." The
       sea represents chaos/nations (17:15). Daniel 7's four beasts
       combined into one — a composite of all human opposition to
       God.

v.4  — NET: "they worshiped the dragon because he gave ruling
       authority to the beast" — "worshiped the dragon" (prosekynEsan
       tO drakonti). WEB: "they worshiped the dragon." KJV: "they
       worshipped the dragon." Satan's ultimate goal achieved —
       worship directed to himself through a human proxy.

v.8  — NET: "all those who live on the earth will worship the
       beast, everyone whose name has not been written since the
       foundation of the world in the book of life" — "since the
       foundation" (apo katabolEs kosmou). WEB: "from the
       foundation of the world." Names written BEFORE creation —
       divine foreknowledge and election.

v.10 — NET: "This requires steadfast endurance and faith from the
       saints" — "steadfast endurance" (hypomonE = patient
       perseverance under pressure). WEB: "Here is the perseverance
       and the faith of the saints." In the face of the beast's
       power, endurance IS victory.

v.18 — NET: "let the one who has insight calculate the beast's
       number, for it is man's number, and his number is 666" —
       "man's number" (arithmos anthrOpou). WEB: "his number is
       six hundred sixty-six." Some manuscripts read 616. Gematria
       (number = letters) most commonly yields "Nero Caesar" in
       Hebrew. Ultimate meaning debated across millennia."""

notes[14] = """v.1  — NET: "the Lamb was standing on Mount Zion, and with him
       were one hundred and forty-four thousand" — "Mount Zion"
       (to oros SiOn) — heavenly Zion, in contrast to the beast's
       earthly domain. WEB: "the Lamb standing on Mount Zion." The
       sealed ones of chapter 7 appear here victorious.

v.6  — NET: "an eternal gospel to proclaim to those who live on
       the earth — to every nation, tribe, language, and people" —
       "eternal gospel" (euangelion aiOnion). WEB: "an eternal Good
       News." Even at the end, the gospel is proclaimed — God's
       mercy persists until the last possible moment.

v.8  — NET: "Fallen, fallen is Babylon the great" — "fallen,
       fallen" (epesen epesen — doubled for emphasis/certainty).
       WEB: "Fallen, fallen is Babylon the great." Echoing Isaiah
       21:9 — the announcement precedes the detailed destruction
       (chapters 17-18).

v.13 — NET: "Blessed are the dead who die in the Lord from this
       point on" — "from this point on" (ap' arti = from now on).
       WEB: "Blessed are the dead who die in the Lord from now on."
       KJV: "Blessed are the dead which die in the Lord from
       henceforth." The second of seven beatitudes in Revelation.

v.20 — NET: "the winepress was stomped outside the city, and
       blood poured out of the winepress up to the horses' bridles
       for a distance of almost two hundred miles" — "two hundred
       miles" (stadiOn chiliOn hexakosiOn = 1,600 stadia). WEB:
       "one thousand six hundred stadia." Hyperbolic imagery of
       devastating judgment — rivers of blood."""

notes[15] = """v.2  — NET: "those who had conquered the beast and his image...
       standing beside the sea of glass, holding harps of God" —
       "conquered" (nikOntas = those overcoming/victorious). WEB:
       "those who overcame the beast." Victory through faithfulness
       (not military power) — they stood firm and now they stand
       glorified.

v.3  — NET: "They sang the song of Moses the servant of God and
       the song of the Lamb" — "song of Moses AND the Lamb" — old
       and new covenants united in one worship. WEB: "the song of
       Moses, the servant of God, and the song of the Lamb."
       Exodus 15 (Red Sea deliverance) meets the Lamb's redemption.

v.3  — NET: "Great and astounding are your deeds, Lord God, the
       All-Powerful!" — "astounding" (thaumasta = marvelous/
       wonderful). WEB: "Great and marvelous are your works." KJV:
       "Great and marvellous are thy works." The content echoes
       multiple OT psalms (Psalms 111:2, 139:14, 145:17).

v.4  — NET: "Who will not fear you, O Lord, and glorify your
       name? Because you alone are holy" — "you alone are holy"
       (monos hosios = uniquely set apart). WEB: "for you only are
       holy." After all the judgments, the conclusion: God is
       righteous, God alone is holy, all nations will worship.

v.8  — NET: "no one could enter the temple until the seven
       plagues from the seven angels were completed" — "no one
       could enter" (oudeis edynato eiselthein). WEB: "No one was
       able to enter into the temple." Access blocked during wrath
       — intercession is suspended while justice runs its full
       course."""

notes[16] = """v.1  — NET: "Go and pour out on the earth the seven bowls of
       the wrath of God" — "pour out" (ekcheate = empty/dump out).
       WEB: "Go and pour out the seven bowls of the wrath of God."
       No restraint, no mixture — pure, undiluted divine wrath
       released.

v.5  — NET: "You are just — the one who is and who was, the Holy
       One — because you have passed these judgments" — "you are
       just" (dikaios ei). WEB: "You are righteous." Even the
       angel of the waters affirms God's justice in judgment —
       these plagues are DESERVED.

v.9  — NET: "people were scorched by the terrible heat, yet they
       blasphemed the name of God... and refused to repent" —
       "refused to repent" (ou metenoEsan). WEB: "they didn't
       repent." Repeated refrain (vv.9, 11, 21) — judgment hardens
       rather than softens those who refuse God.

v.15 — NET: "Look! I will come like a thief! Blessed is the one
       who stays alert" — "stays alert" (grEgorOn = watching).
       WEB: "Blessed is he who watches." KJV: "Blessed is he that
       watcheth." Christ's voice interrupts the bowl judgments —
       the third beatitude of Revelation.

v.16 — NET: "they assembled them at the place that in Hebrew is
       called Armageddon" — "Armageddon" (HarmagedOn = Mountain of
       Megiddo). WEB: "Har-Magedon." KJV: "Armageddon." The great
       battlefield — whether literal or symbolic of the final
       conflict between God and evil."""

notes[17] = """v.1  — NET: "the judgment of the great prostitute who is
       seated on many waters" — "great prostitute" (tEs pornEs tEs
       megalEs). WEB: "the great prostitute." KJV: "the great
       whore." False religion/political power seducing the nations
       — "many waters" = peoples and nations (v.15).

v.5  — NET: "Babylon the Great, the Mother of prostitutes and of
       the detestable things of the earth" — "Mother of prostitutes"
       (mEtEr tOn pornOn). WEB: "BABYLON THE GREAT, THE MOTHER OF
       THE PROSTITUTES." The source/originator of all false
       religion and corruption.

v.8  — NET: "The beast that you saw was, and is not, but is about
       to come up from the abyss" — "was, and is not, and is about
       to come" — a satanic parody of God's title ("who is, was,
       and is to come," 1:8). WEB: "The beast that you saw was,
       and is not; and is about to come up." A counterfeit
       resurrection.

v.14 — NET: "They will make war with the Lamb, but the Lamb will
       conquer them, because he is Lord of lords and King of kings"
       — "Lord of lords" (kyrios kyriOn). WEB: "the Lamb will
       overcome them, for he is Lord of lords, and King of kings."
       The outcome is certain before the battle begins.

v.17 — NET: "God has put into their minds to carry out his
       purpose" — "put into their minds" (edOken... poiEsai tEn
       gnOmEn autou = gave to do His purpose). WEB: "God has put
       in their hearts to do what he has in mind." Even the beast's
       allies serve God's sovereign plan unknowingly."""

notes[18] = """v.2  — NET: "Fallen, fallen, is Babylon the great!" — doubled
       "fallen" (epesen epesen — echoing 14:8 and Isaiah 21:9).
       WEB: "Fallen, fallen is Babylon the great!" The announcement
       made earlier is now executed — the verdict becomes reality.

v.4  — NET: "Come out of her, my people, so you will not
       participate in her sins" — "come out" (exelthate = depart/
       leave). WEB: "Come out of her, my people." KJV: "Come out
       of her, my people." Echoing Jeremiah 51:45 and Isaiah 48:20
       — separation before judgment falls.

v.8  — NET: "For this reason, her plagues will come in a single
       day" — "single day" (en mia hEmera = in one day). WEB: "in
       one day her plagues will come." The swiftness of Babylon's
       fall — she thought she was invincible (v.7: "I sit as queen
       and will never see grief").

v.20 — NET: "Rejoice over her, O heaven, and you saints and
       apostles and prophets, for God has pronounced judgment
       against her on your behalf!" — "pronounced judgment on your
       behalf" (ekrinen ho theos to krima hymOn ex autEs). WEB:
       "God has judged your judgment on her." Heaven rejoices
       while earth mourns — perspectives depend on allegiance.

v.24 — NET: "The blood of saints and prophets was found in her,
       and of all those who had been killed on the earth" — "all
       those killed" (pantOn tOn esphagmenOn). WEB: "the blood of
       prophets and of saints, and of all who have been slain on
       the earth." Babylon is guilty of all martyrdom — the system
       behind every persecution."""

notes[19] = """v.1  — NET: "After these things I heard what sounded like the
       loud voice of a vast throng in heaven, saying, 'Hallelujah!'"
       — "Hallelujah" (hallElouia = Praise Yah/Praise the LORD).
       WEB: "Hallelujah!" The only NT occurrences of "Hallelujah"
       are in this chapter (vv.1, 3, 4, 6) — reserved for this
       climactic moment.

v.7  — NET: "the wedding celebration of the Lamb has come, and
       his bride has made herself ready" — "bride" (hE gynE autou
       = His wife). WEB: "the marriage of the Lamb has come." KJV:
       "the marriage of the Lamb is come." The church prepared
       through centuries of suffering now presented in glory.

v.11 — NET: "I saw heaven standing open and a white horse
       appeared... the one riding it was called Faithful and True"
       — "Faithful and True" (pistos kai alEthinos). WEB: "called
       Faithful and True." Christ returns not on a donkey (first
       coming: humility) but a white horse (second coming: conquest).

v.13 — NET: "He is dressed in clothing dipped in blood, and he
       is called the Word of God" — "the Word of God" (ho logos
       tou theou). WEB: "The Word of God." KJV: "The Word of God."
       The same title as John 1:1 — now the Word rides in judgment
       rather than lying in a manger.

v.16 — NET: "He has a name written on his clothing and on his
       thigh: 'King of kings and Lord of lords'" — "King of kings"
       (basileus basileOn). WEB: "KING OF KINGS, AND LORD OF LORDS."
       The supreme title — no competitor, no equal. Written visibly
       for all to read as He descends."""

notes[20] = """v.2  — NET: "He seized the dragon — the ancient serpent, who
       is the devil and Satan — and tied him up for a thousand
       years" — four titles identifying the enemy: dragon, ancient
       serpent, devil (diabolos = accuser), Satan (satanas =
       adversary). WEB: "bound him for a thousand years."

v.4  — NET: "they came to life and reigned with Christ for a
       thousand years" — "came to life" (ezEsan = lived/came alive).
       WEB: "they lived and reigned with Christ for a thousand
       years." KJV: "they lived and reigned with Christ." The "first
       resurrection" — whether literal/physical or spiritual is
       the key millennial debate.

v.6  — NET: "Blessed and holy is the one who takes part in the
       first resurrection" — the fifth beatitude. "The second death
       has no power over them" (ho deuteros thanatos ouk echei
       exousian). WEB: "the second death has no power over them."
       Immunity from eternal death through participation in the
       first resurrection.

v.12 — NET: "I saw the dead, the great and the small, standing
       before the throne, and books were opened" — "books" (biblia)
       — records of deeds; and "the book of life" (biblos tEs zOEs)
       — the register of the saved. WEB: "the dead, the great and
       the small, standing before the throne." Universal judgment —
       no exceptions.

v.15 — NET: "If anyone's name was not found written in the book
       of life, that person was thrown into the lake of fire" —
       "lake of fire" (limnEn tou pyros = the burning lake). WEB:
       "cast into the lake of fire." The final destiny of all whose
       names are absent. This IS the second death (v.14)."""

notes[21] = """v.1  — NET: "Then I saw a new heaven and a new earth, for the
       first heaven and earth had passed away" — "new" (kainon =
       new in quality/character, not neos/new in time). WEB: "a
       new heaven and a new earth." Not replacement but renewal —
       transformed creation, not annihilation.

v.2  — NET: "the holy city — the new Jerusalem — descending out
       of heaven from God, made ready like a bride adorned for her
       husband" — "adorned" (kekosmEmenEn = beautifully arranged —
       English "cosmetics"). WEB: "prepared like a bride adorned
       for her husband." The city IS the bride — the church in
       its final, glorified form.

v.3  — NET: "the dwelling of God is with mankind! He will live
       among them" — "dwelling" (skEnE = tabernacle/tent). WEB:
       "God's dwelling is with people." KJV: "the tabernacle of God
       is with men." The tabernacle/temple trajectory reaches its
       goal — God dwelling permanently among His people with no
       barrier.

v.4  — NET: "He will wipe away every tear from their eyes, and
       death will not exist any more" — "wipe away" (exaleipsei =
       completely remove). WEB: "He will wipe away every tear."
       KJV: "God shall wipe away all tears." The personal tenderness
       — God Himself touching faces, removing grief.

v.5  — NET: "Look! I am making all things new!" — "making new"
       (kaina poiO = creating anew). WEB: "Behold, I am making all
       things new." KJV: "Behold, I make all things new." Present
       tense — the renewal is not just future but already in
       process. Not "all new things" but "all things NEW."""

notes[22] = """v.1  — NET: "Then the angel showed me the river of the water
       of life — Loss clear as crystal — flowing from the throne
       of God and of the Lamb" — "water of life" (hydatos zOEs).
       WEB: "a river of water of life, clear as crystal." Echoing
       Ezekiel 47 and Genesis 2 — paradise restored and surpassed.

v.2  — NET: "On each side of the river is the tree of life
       producing twelve kinds of fruit, yielding its fruit every
       month" — "tree of life" (xylon zOEs = wood/tree of life).
       WEB: "the tree of life." Genesis 3 barred access; Revelation
       22 restores it — no more cherubim guarding the way.

v.4  — NET: "They will see his face, and his name will be on
       their foreheads" — "see his face" (opsontai to prosOpon
       autou). WEB: "They will see his face." The beatific vision
       — what Moses was denied (Exodus 33:20) believers receive
       eternally. Face-to-face with God.

v.17 — NET: "And the Spirit and the bride say, 'Come!' And let
       the one who hears say, 'Come!' And let the one who is
       thirsty come; let the one who wants it take the water of
       life free of charge" — "free of charge" (dOrean = as a
       gift). WEB: "let him who desires take the water of life
       freely." The final gospel invitation — free, universal,
       Spirit-empowered.

v.20 — NET: "The one who testifies to these things says, 'Yes, I
       am coming soon!' Amen! Come, Lord Jesus!" — "Come, Lord
       Jesus" (erchou kyrie IEsou — Maranatha in Aramaic). WEB:
       "Amen! Yes, come, Lord Jesus." KJV: "Even so, come, Lord
       Jesus." The last prayer of the Bible — the church's longing
       across two millennia, still unanswered, still urgent."""

for ch, note_text in sorted(notes.items()):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Revelation " + str(ch))
        else:
            print("  skip Revelation " + str(ch))
    else:
        print("  missing Revelation " + str(ch))
