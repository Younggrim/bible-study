#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Matthew chapters 2-28."""
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

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/01 - Matthew"
notes = dict()

notes[2] = """v.1  — NET: "After Jesus was born in Bethlehem in Judea, in
       the time of King Herod, wise men from the East came to
       Jerusalem" — "wise men" (magoi = Magi/astrologers). WEB:
       "wise men from the east." KJV: "wise men from the east."
       Not kings, not three (the number is unspecified) — they
       were Persian/Babylonian astrologer-priests.

v.2  — NET: "Where is the one who is born king of the Jews?" —
       "born king" — not made king but BORN king. WEB: "Where is
       he who is born King of the Jews?" KJV: "Where is he that is
       born King of the Jews?" The question threatens Herod who was
       MADE king by Rome, not born to it.

v.6  — NET: "a ruler who will shepherd my people Israel" —
       "shepherd" (poimanei = tend/feed/rule). WEB: "who will
       govern my people, Israel." KJV: "that shall rule my people
       Israel." Quoting Micah 5:2 — the Messiah is a shepherd-
       king, not merely a political ruler.

v.11 — NET: "they offered him gifts: gold, frankincense, and
       myrrh" — "offered" (prosEnenkan = presented formally). WEB:
       "they offered him gifts." Traditional interpretation: gold
       (kingship), frankincense (deity), myrrh (death/burial).

v.16 — NET: "he sent men to kill all the children in Bethlehem
       and throughout the surrounding region who were two years old
       and under" — "two years old and under" (apo dietous kai
       katOterO) — Herod calculated from when the star first
       appeared. WEB: "from two years old and under." The massacre
       of innocents — not recorded outside Matthew but consistent
       with Herod's documented paranoia."""

notes[3] = """v.2  — NET: "Repent, for the kingdom of heaven is near!" —
       "near" (Eggiken = has drawn near/is at hand — perfect tense).
       WEB: "Repent, for the Kingdom of Heaven is at hand!" KJV:
       "Repent ye: for the kingdom of heaven is at hand." The
       kingdom has already begun approaching — urgency.

v.7  — NET: "You offspring of vipers! Who warned you to flee from
       the coming wrath?" — "offspring of vipers" (gennEmata
       echidnOn = brood of snakes). WEB: "You offspring of vipers!"
       KJV: "O generation of vipers." John's language to the
       religious leaders is shocking — they are poisonous by nature.

v.11 — NET: "I baptize you with water, for repentance, but the
       one coming after me is more powerful" — "more powerful"
       (ischyroteros). WEB: "he who comes after me is mightier
       than I." KJV: "he that cometh after me is mightier than I."
       John contrasts water baptism with Spirit-and-fire baptism.

v.15 — NET: "Let it happen now, for it is right for us to fulfill
       all righteousness" — "fulfill all righteousness" (plErOsai
       pasan dikaiosynEn). WEB: "to fulfill all righteousness."
       KJV: "to fulfil all righteousness." Jesus' baptism is not
       for repentance but to identify with sinners and inaugurate
       His mission.

v.17 — NET: "This is my one dear Son; in him I take great
       delight" — "one dear Son" (ho huios mou ho agapEtos). WEB:
       "This is my beloved Son, in whom I am well pleased." KJV:
       "This is my beloved Son, in whom I am well pleased." NET
       paraphrases; KJV/WEB preserve the echoes of Psalm 2:7 and
       Isaiah 42:1."""

notes[4] = """v.1  — NET: "Then Jesus was led by the Spirit into the
       wilderness to be tempted by the devil" — "led by the Spirit"
       (anEchthE hypo tou pneumatos) — the Spirit deliberately
       takes Jesus into testing. WEB: "led up by the Spirit."
       God initiates the confrontation with evil.

v.4  — NET: "It is written: 'Man does not live by bread alone,
       but by every word that comes from the mouth of God'" —
       quoting Deuteronomy 8:3. WEB: "Man shall not live by bread
       alone." Jesus defeats each temptation with "It is written"
       — Scripture as the weapon against Satan.

v.10 — NET: "Go away, Satan! For it is written: 'You are to
       worship the Lord your God and serve only him'" — "Go away"
       (hypage = be gone/get behind). WEB: "Get behind me, Satan!"
       KJV: "Get thee hence, Satan." A direct command to the devil
       — Jesus exercises authority over the tempter.

v.17 — NET: "From that time Jesus began to preach this message:
       'Repent, for the kingdom of heaven is near'" — the same
       message as John the Baptist (3:2). WEB: "Repent! For the
       Kingdom of Heaven is at hand." Continuity between the
       forerunner and the King — identical call.

v.19 — NET: "Follow me, and I will turn you into fishers of
       people" — "fishers of people" (halieis anthrOpOn). WEB:
       "fishers for men." KJV: "fishers of men." NET uses inclusive
       "people"; the vocation changes from catching fish (for death)
       to catching humans (for life)."""

notes[5] = """v.3  — NET: "Blessed are the poor in spirit, for the kingdom
       of heaven belongs to them" — "poor in spirit" (hoi ptOchoi
       tO pneumati = the spiritually destitute). WEB: "Blessed are
       the poor in spirit." KJV: "Blessed are the poor in spirit."
       Not financially poor (Luke's version) but spiritually
       bankrupt — aware of their need for God.

v.17 — NET: "Do not think that I have come to abolish the law or
       the prophets. I have not come to abolish these things but
       to fulfill them" — "fulfill" (plErOsai = fill up/complete/
       bring to full meaning). WEB: "not to destroy, but to
       fulfill." Jesus completes what the Law pointed toward.

v.22 — NET: "everyone who is angry with a brother will be
       subjected to judgment" — some manuscripts add "without
       cause" (eikE). KJV includes "without cause"; NET/ESV omit
       it following earlier manuscripts. WEB: "everyone who is
       angry with his brother without a cause." A significant
       textual variant affecting the teaching.

v.44 — NET: "But I say to you, love your enemies and pray for
       those who persecute you" — "love" (agapate = active,
       willed love). WEB: "Love your enemies." KJV: "Love your
       enemies." Some manuscripts add "bless those who curse you,
       do good to those who hate you" (KJV includes; NET omits).

v.48 — NET: "So then, be perfect, as your heavenly Father is
       perfect" — "perfect" (teleioi = complete/mature/whole). WEB:
       "Therefore you shall be perfect." KJV: "Be ye therefore
       perfect." Not sinless perfection but wholeness of character
       — complete in love (the context: love for enemies)."""

notes[6] = """v.6  — NET: "go into your inner room, close the door, and
       pray to your Father in secret" — "inner room" (tameion =
       storeroom/private chamber). WEB: "enter into your inner
       room." KJV: "enter into thy closet." Privacy not for
       isolation but for sincerity — God sees in secret.

v.9  — NET: "So pray this way: Our Father in heaven, may your
       name be honored" — "may your name be honored" (hagiasthEtO
       to onoma sou). WEB: "may your name be kept holy." KJV:
       "Hallowed be thy name." NET interprets the passive
       imperative; KJV preserves the traditional form.

v.11 — NET: "Give us today our daily bread" — "daily" (epiousion
       = a unique word, meaning debated: for today? for tomorrow?
       necessary? supernatural?). WEB: "Give us today our daily
       bread." The word appears nowhere else in Greek literature —
       its exact meaning remains uncertain.

v.22 — NET: "The eye is the lamp of the body" — "lamp" (lychnos
       = oil lamp). WEB: "The lamp of the body is the eye." KJV:
       "The light of the body is the eye." How you see determines
       what enters you — healthy eyes let in light; bad eyes fill
       you with darkness.

v.34 — NET: "So then, do not worry about tomorrow, for tomorrow
       will worry about itself" — "worry" (merimnEsEte = be anxious/
       divided in mind). WEB: "Don't be anxious for tomorrow." KJV:
       "Take therefore no thought for the morrow." Each day has
       enough trouble of its own (v.34b)."""

notes[7] = """v.1  — NET: "Do not judge so that you will not be judged" —
       "judge" (krinete = pronounce condemning verdict). WEB:
       "Don't judge, so that you won't be judged." KJV: "Judge not,
       that ye be not judged." Not forbidding discernment (v.6:
       "don't give what is holy to dogs") but condemning
       hypocritical, self-righteous judgment.

v.6  — NET: "Do not give what is holy to dogs or throw your
       pearls before pigs" — "dogs... pigs" — animals considered
       unclean. WEB: "Don't give that which is holy to the dogs."
       Discernment IS required — some people will trample truth
       and turn to attack you.

v.11 — NET: "how much more will your Father in heaven give good
       gifts to those who ask him!" — "good gifts" (agatha = good
       things). Luke 11:13 has "Holy Spirit" instead of "good
       gifts." WEB: "give good things to those who ask him." The
       parallel shows the Holy Spirit IS the supreme good gift.

v.13 — NET: "Enter through the narrow gate, because the gate is
       wide and the way is spacious that leads to destruction" —
       "spacious" (eurychOros = broad/roomy). WEB: "wide is the
       gate and broad is the way." KJV: "wide is the gate, and
       broad is the way." The easy path accommodates many; the
       narrow requires effort and finds few.

v.23 — NET: "I never knew you. Go away from me, you lawbreakers!"
       — "knew" (egnOn = knew intimately/acknowledged). WEB:
       "I never knew you. Depart from me." KJV: "I never knew you:
       depart from me." Not ignorance but non-recognition —
       miracles without relationship count for nothing."""

notes[8] = """v.2  — NET: "Lord, if you are willing, you can make me clean"
       — "if you are willing" (ean thelEs = if you will). WEB:
       "Lord, if you want to, you can make me clean." The leper
       doesn't doubt Jesus' POWER — he questions His WILLINGNESS.
       Jesus answers: "I am willing" (v.3).

v.8  — NET: "Lord, I am not worthy to have you come under my
       roof" — "not worthy" (ouk eimi hikanos = I am not sufficient/
       deserving). WEB: "I'm not worthy for you to come under my
       roof." KJV: "I am not worthy that thou shouldest come under
       my roof." A Gentile centurion's humility — greater faith
       than any in Israel (v.10).

v.17 — NET: "He took our weaknesses and carried our diseases" —
       quoting Isaiah 53:4. "Took" (elaben) and "carried"
       (ebastasen). WEB: "He took our infirmities and bore our
       diseases." Matthew applies Isaiah's Suffering Servant
       prophecy to Jesus' healing ministry — not just the cross.

v.20 — NET: "Foxes have dens and the birds in the sky have nests,
       but the Son of Man has no place to lay his head" — "Son of
       Man" (ho huios tou anthrOpou) — Jesus' preferred self-
       designation, echoing Daniel 7:13. WEB: "The Son of Man has
       nowhere to lay his head." The King is homeless.

v.26 — NET: "Why are you cowardly, you people of little faith?"
       — "cowardly" (deiloi = fearful/timid). WEB: "Why are you
       fearful, O you of little faith?" KJV: "Why are ye fearful,
       O ye of little faith?" Jesus rebukes fear as insufficient
       faith — then rebukes the storm with equal authority."""

notes[9] = """v.2  — NET: "Take courage, son! Your sins are forgiven" —
       "take courage" (tharsei = be of good cheer/be bold). WEB:
       "Son, be of good cheer." KJV: "Son, be of good cheer."
       Jesus addresses the paralytic's spiritual need before his
       physical one — forgiveness before healing.

v.6  — NET: "the Son of Man has authority on earth to forgive
       sins" — "authority" (exousian = power/right). WEB: "the Son
       of Man has authority on earth to forgive sins." The healing
       proves the forgiveness claim — visible miracle validates
       invisible reality.

v.13 — NET: "I did not come to call the righteous, but sinners"
       — "call" (kalesai = invite/summon). WEB: "I came not to
       call the righteous, but sinners to repentance." KJV adds
       "to repentance" — some manuscripts include it, others don't.
       NET/ESV omit following earlier texts.

v.17 — NET: "new wine is poured into new wineskins" — "new
       wineskins" (askous kainous = fresh/unused leather bags). WEB:
       "new wine into fresh wineskins." KJV: "new wine into new
       bottles." Jesus' teaching can't be contained in old
       structures — it requires new forms.

v.36 — NET: "he had compassion on them because they were
       bewildered and helpless, like sheep without a shepherd" —
       "compassion" (esplanchnisthE = moved in his guts/visceral
       emotion). WEB: "he was moved with compassion for them." KJV:
       "he was moved with compassion on them." Deep, physical
       empathy — the shepherd sees scattered sheep."""

notes[10] = """v.8  — NET: "Heal the sick, raise the dead, cleanse lepers,
       cast out demons. Freely you received, freely give" —
       "freely" (dOrean = as a gift/without payment). WEB: "Freely
       you received, freely give." KJV: "freely ye have received,
       freely give." Grace received must become grace distributed.

v.16 — NET: "I am sending you out like sheep among wolves, so be
       wise as serpents and innocent as doves" — "wise" (phronimoi
       = shrewd/prudent) and "innocent" (akeraioi = pure/unmixed).
       WEB: "wise as serpents, and harmless as doves." Both
       qualities together — shrewdness without corruption.

v.28 — NET: "Do not be afraid of those who kill the body but
       cannot kill the soul" — "cannot kill the soul" (tEn psychEn
       mE dynamenOn apokteinai). WEB: "Don't be afraid of those
       who kill the body." Human power is limited to the physical
       — fear the One who governs both body and soul.

v.29 — NET: "Aren't two sparrows sold for a penny? Yet not one of
       them falls to the ground apart from your Father's will" —
       "penny" (assariou = smallest Roman coin). WEB: "Aren't two
       sparrows sold for an assarion coin?" God's providence
       extends to the cheapest, most insignificant creatures.

v.34 — NET: "Do not think that I have come to bring peace on the
       earth. I have not come to bring peace but a sword" — "sword"
       (machairan = short sword/dagger). WEB: "I came not to send
       peace, but a sword." KJV: "I came not to send peace, but a
       sword." The gospel divides — even families (vv.35-36)."""

notes[11] = """v.5  — NET: "the blind see, the lame walk, lepers are cleansed,
       the deaf hear, the dead are raised, and the poor have good
       news proclaimed to them" — Jesus answers John's doubt with
       evidence from Isaiah 35:5-6 and 61:1. WEB: "the blind
       receive their sight." Actions speak louder than assertions.

v.12 — NET: "the kingdom of heaven has been forcefully advancing,
       and forceful people are seizing it" — "forcefully advancing"
       (biazetai — debated: middle or passive voice). WEB: "the
       Kingdom of Heaven suffers violence." KJV: "the kingdom of
       heaven suffereth violence." One of the most debated verses
       in Matthew — is the kingdom being attacked or advancing?

v.19 — NET: "The Son of Man came eating and drinking, and they
       say, 'Look at him, a glutton and a drunk'" — "glutton"
       (phagos) and "drunk" (oinopotEs = wine-drinker). WEB: "a
       gluttonous man and a drunkard." Jesus was slandered for
       His table fellowship — He was neither but was accused.

v.28 — NET: "Come to me, all you who are weary and burdened, and
       I will give you rest" — "weary" (kopiontes = laboring to
       exhaustion) and "burdened" (pephortismenoi = loaded down).
       WEB: "Come to me, all you who labor and are heavily
       burdened." The most tender invitation in the Gospels.

v.30 — NET: "For my yoke is easy to bear, and my load is not
       hard to carry" — "easy" (chrEstos = well-fitting/kind) and
       "light" (elaphron = not heavy). WEB: "my yoke is easy, and
       my burden is light." Not no yoke but a GOOD yoke — fitted
       properly, shared with Christ."""

notes[12] = """v.6  — NET: "something greater than the temple is here" —
       "something greater" (meizon — neuter, not masculine: greater
       THING, not greater person). WEB: "one greater than the
       temple is here." KJV: "one greater than the temple is here."
       Jesus claims authority over the temple system itself.

v.18 — NET: "Here is my servant whom I have chosen, the one I
       love, in whom I take great delight" — quoting Isaiah 42:1-4.
       WEB: "my servant whom I have chosen." Jesus as the Suffering
       Servant — gentle, not breaking bruised reeds (v.20).

v.28 — NET: "But if I cast out demons by the Spirit of God, then
       the kingdom of God has already overtaken you" — "overtaken"
       (ephthasen = has arrived/come upon). WEB: "the Kingdom of
       God has come upon you." KJV: "the kingdom of God is come
       unto you." The kingdom is PRESENT in Jesus' exorcisms.

v.36 — NET: "on the day of judgment, people will give an account
       for every worthless word they speak" — "worthless" (argon =
       idle/unproductive/careless). WEB: "every idle word." KJV:
       "every idle word." Words reveal the heart (v.34) and will
       be examined at judgment.

v.40 — NET: "just as Jonah was in the belly of the huge fish for
       three days and three nights, so the Son of Man will be in
       the heart of the earth" — "huge fish" (kEtous = sea monster).
       WEB: "the whale." KJV: "the whale." NET avoids "whale"
       since the Hebrew/Greek doesn't specify species."""

notes[13] = """v.11 — NET: "You have been given the opportunity to know the
       secrets of the kingdom of heaven, but they have not" —
       "secrets" (mystEria = mysteries/hidden truths now revealed).
       WEB: "To you it is given to know the mysteries of the
       Kingdom of Heaven." Parables reveal to insiders and conceal
       from outsiders simultaneously.

v.15 — NET: "For the heart of this people has become dull" —
       quoting Isaiah 6:9-10. "Dull" (epachynthE = made thick/fat/
       calloused). WEB: "this people's heart has grown callous."
       KJV: "this people's heart is waxed gross." Spiritual
       deafness from repeated refusal to hear.

v.31 — NET: "The kingdom of heaven is like a mustard seed" —
       "mustard seed" (kokkO sinapeOs) — the smallest garden seed
       producing a large shrub. WEB: "like a grain of mustard
       seed." The kingdom starts invisibly small but grows to
       shelter nations (v.32: "birds of the air lodge in its
       branches").

v.44 — NET: "The kingdom of heaven is like a treasure, hidden in
       a field, that a person found and hid" — "treasure" (thEsaurO
       = stored wealth). WEB: "like treasure hidden in the field."
       The finder sells EVERYTHING to buy the field — the kingdom
       is worth total investment.

v.52 — NET: "every expert in the law who has been trained for the
       kingdom of heaven is like the owner of a house" — "trained"
       (mathEteutheIs = discipled/made a student). WEB: "made a
       disciple to the Kingdom of Heaven." A scribe who follows
       Jesus brings out old (OT) and new (kingdom) treasures."""

notes[14] = """v.14 — NET: "he had compassion on them and healed their sick"
       — "compassion" (esplanchnisthE = visceral, gut-level
       emotion). WEB: "he had compassion on them." KJV: "was moved
       with compassion toward them." Jesus' motivation for miracles
       is never display but compassion.

v.19 — NET: "he gave thanks, and breaking the loaves he gave them
       to the disciples" — "gave thanks" (eulogEsen = blessed).
       WEB: "looking up to heaven, he blessed." KJV: "blessed."
       Jewish blessing formula: blessing God for providing the food,
       not blessing the food itself.

v.25 — NET: "he came to them walking on the sea" — "on the sea"
       (epi tEn thalassan = upon the sea). WEB: "walking on the
       sea." KJV: "walking on the sea." In the OT, walking on
       water is God's exclusive prerogative (Job 9:8; Psalm 77:19).
       Jesus does what only God does.

v.27 — NET: "Have courage! It is I. Do not be afraid" — "It is
       I" (egO eimi = I AM). WEB: "Cheer up! It is I! Don't be
       afraid." The divine name spoken on the water — theophany
       in action. "I AM" calms the storm and the fear.

v.31 — NET: "You of little faith, why did you doubt?" — "little
       faith" (oligopiste) and "doubt" (edistasas = hesitated/
       wavered). WEB: "You of little faith, why did you doubt?"
       Peter's faith was genuine (he walked!) but insufficient
       (he sank when he looked at waves instead of Jesus)."""

notes[15] = """v.3  — NET: "Why do you also break the commandment of God
       because of your tradition?" — "tradition" (paradosin =
       handed-down teaching). WEB: "Why do you also disobey the
       commandment of God because of your tradition?" Human
       traditions elevated above divine commands — the perennial
       temptation of religion.

v.11 — NET: "it is not what goes into the mouth that defiles a
       person, but what comes out of the mouth" — "defiles" (koinoi
       = makes common/ritually unclean). WEB: "that which proceeds
       out of the mouth, this defiles the man." A revolutionary
       principle overturning the entire Jewish purity system.

v.22 — NET: "Have mercy on me, Lord, Son of David! My daughter
       is horribly demon-possessed" — "have mercy" (eleEson =
       show compassion). WEB: "Have mercy on me." KJV: "Have mercy
       on me." A Canaanite woman uses the messianic title "Son of
       David" — greater faith from a pagan than from Israel.

v.28 — NET: "Woman, your faith is great! Let what you want be
       done for you" — "great" (megalE = large). WEB: "great is
       your faith!" KJV: "O woman, great is thy faith." Only two
       people receive this commendation in Matthew: this Canaanite
       and the centurion (8:10) — both Gentiles.

v.32 — NET: "I have compassion on the crowd, because they have
       already been here with me three days" — "compassion"
       (splanchnizomai) again — the same visceral emotion as 14:14.
       WEB: "I have compassion on the multitude." Jesus feeds 4,000
       — a second feeding miracle."""

notes[16] = """v.16 — NET: "You are the Christ, the Son of the living God" —
       "the Christ" (ho Christos = the Anointed One/Messiah). WEB:
       "You are the Christ, the Son of the living God." KJV: "Thou
       art the Christ, the Son of the living God." Peter's
       confession — the hinge of Matthew's Gospel.

v.17 — NET: "flesh and blood did not reveal this to you, but my
       Father in heaven!" — "flesh and blood" (sarx kai haima =
       human nature/human reasoning). WEB: "flesh and blood has
       not revealed this to you." The Father reveals what human
       intellect cannot discover — divine illumination.

v.18 — NET: "you are Peter, and on this rock I will build my
       church" — "Peter" (Petros = stone) and "rock" (petra =
       bedrock). WEB: "on this rock I will build my assembly." The
       wordplay: Petros/petra. Debated: is the rock Peter himself,
       his confession, or Christ? All views have support.

v.23 — NET: "Get behind me, Satan! You are a stumbling block to
       me" — "stumbling block" (skandalon = trap/snare). WEB: "Get
       behind me, Satan!" KJV: "Get thee behind me, Satan." Peter
       goes from "blessed" (v.17) to "Satan" (v.23) in six verses
       — speaking for God, then for the enemy.

v.25 — NET: "whoever wants to save his life will lose it, but
       whoever loses his life because of me will find it" — "life"
       (psychEn = soul/life/self). WEB: "whoever desires to save
       his life will lose it." The paradox of the cross: self-
       preservation destroys; self-surrender saves."""

notes[17] = """v.2  — NET: "his face shone like the sun, and his clothes
       became white as light" — "shone" (elampsen = radiated/
       blazed). WEB: "his face shone like the sun." KJV: "his face
       did shine as the sun." The veil of humanity momentarily
       pulled back — the divine glory breaks through.

v.5  — NET: "This is my one dear Son, in whom I take great
       delight. Listen to him!" — "Listen to him!" (akouete autou
       = hear/obey him). WEB: "This is my beloved Son, in whom I
       am well pleased. Listen to him." The Father's command — the
       Son's words carry divine authority.

v.14 — NET: "Lord, have mercy on my son, because he has seizures
       and suffers terribly" — "seizures" (selEniazetai = is
       moonstruck/epileptic). WEB: "he is epileptic." KJV: "he is
       lunatick." The condition is real (seizures into fire/water)
       but the cause is demonic (v.18). Medical and spiritual
       realities coexist.

v.20 — NET: "if you have faith the size of a mustard seed, you
       will say to this mountain, 'Move from here to there,' and
       it will move" — "mustard seed" — the smallest measure of
       genuine faith moves mountains. WEB: "faith as a grain of
       mustard seed." The quantity isn't the issue — the quality
       (genuine, God-directed) matters.

v.22 — NET: "The Son of Man is going to be betrayed into the
       hands of men" — "betrayed" (paradidosthai = handed over/
       delivered up). WEB: "The Son of Man is about to be delivered
       up." KJV: "The Son of Man shall be betrayed." The passive
       voice: God hands Him over through human betrayal."""

notes[18] = """v.3  — NET: "unless you turn around and become like little
       children, you will never enter the kingdom of heaven" —
       "turn around" (straphEte = convert/change direction). WEB:
       "unless you turn and become as little children." Not
       childish but child-LIKE: dependent, trusting, humble.

v.8  — NET: "If your hand or your foot causes you to sin, cut it
       off" — "causes you to sin" (skandalizei = ensnares/trips
       you up). WEB: "if your hand or your foot causes you to
       stumble." Radical self-surgery — amputation metaphor for
       eliminating sin's sources.

v.10 — NET: "their angels in heaven always see the face of my
       Father in heaven" — "their angels" — guardian angels with
       direct access to God. WEB: "their angels in heaven always
       see the face of my Father." KJV: "their angels do always
       behold the face of my Father." Children have heavenly
       representatives.

v.20 — NET: "where two or three are assembled in my name, I am
       there among them" — "assembled in my name" (synagmenoi eis
       to emon onoma). WEB: "where two or three are gathered
       together in my name." Christ's presence in the smallest
       gathering — not dependent on numbers.

v.22 — NET: "Not seven times, I tell you, but seventy-seven
       times!" — "seventy-seven" (hebdomEkontakis hepta) — or
       "seventy times seven" (490). KJV: "seventy times seven."
       WEB: "seventy times seven." Either way: unlimited forgiveness,
       not mathematical calculation."""

notes[19] = """v.4  — NET: "the one who made them at the beginning made them
       male and female" — "at the beginning" (ap' archEs). WEB:
       "He who made them from the beginning made them male and
       female." Jesus grounds marriage in creation design — God's
       original intent, not cultural convention.

v.6  — NET: "So they are no longer two, but one flesh. Therefore
       what God has joined together, let no one separate" — "one
       flesh" (sarka mian). WEB: "what therefore God has joined
       together, don't let man tear apart." KJV: "let not man put
       asunder." Marriage is God's work — human dissolution
       contradicts divine action.

v.14 — NET: "Let the little children come to me and do not try to
       stop them, for the kingdom of heaven belongs to such as
       these" — "do not try to stop them" (mE kOlyete = stop
       hindering). WEB: "Don't forbid them." The disciples tried
       to prevent access; Jesus insists on it.

v.21 — NET: "If you wish to be perfect, go sell your possessions
       and give the money to the poor" — "perfect" (teleios =
       complete/mature). WEB: "If you want to be perfect." KJV:
       "If thou wilt be perfect." Not sinlessness but wholeness —
       total devotion unhindered by possessions.

v.24 — NET: "it is easier for a camel to go through the eye of a
       needle than for a rich person to enter the kingdom of God"
       — "eye of a needle" (trypEmatos rhaphidos). WEB: "the eye
       of a needle." A literal impossibility — no "small gate"
       theory is textually supported. The disciples understood:
       "Who then can be saved?" (v.25)."""

notes[20] = """v.1  — NET: "the kingdom of heaven is like a landowner who
       went out early in the morning to hire workers" — "landowner"
       (oikodespotE = master of the house). WEB: "a man who was a
       householder." KJV: "a man that is an householder." The parable
       teaches God's sovereign generosity, not labor economics.

v.15 — NET: "Are you envious because I am generous?" — literally
       "Is your eye evil because I am good?" (ho ophthalmos sou
       ponEros estin). WEB: "Is your eye evil, because I am good?"
       KJV: "Is thine eye evil, because I am good?" "Evil eye" =
       jealousy/stinginess in Jewish idiom.

v.22 — NET: "You don't know what you are asking! Are you able to
       drink the cup I am about to drink?" — "the cup" (to potErion)
       = suffering and death. WEB: "Are you able to drink the cup
       that I am about to drink?" KJV: "Are ye able to drink of
       the cup?" The mother asks for thrones; Jesus offers cups.

v.26 — NET: "whoever wants to be great among you must be your
       servant" — "servant" (diakonos = minister/one who serves
       tables). WEB: "whoever desires to become great among you
       shall be your servant." Kingdom greatness is measured by
       service, not authority.

v.28 — NET: "the Son of Man did not come to be served but to
       serve, and to give his life as a ransom for many" — "ransom"
       (lytron = redemption price). WEB: "to give his life as a
       ransom for many." KJV: "to give his life a ransom for many."
       The theological center of Mark/Matthew — substitutionary
       atonement summarized."""

notes[21] = """v.5  — NET: "your king is coming to you, gentle and riding on
       a donkey" — quoting Zechariah 9:9. "Gentle" (prays =
       humble/meek). WEB: "humble, and riding on a donkey." KJV:
       "meek, and sitting upon an ass." The King enters not on a
       war horse but a beast of peace.

v.12 — NET: "My house will be called a house of prayer, but you
       are turning it into a den of robbers!" — "den of robbers"
       (spElaion lEstOn — quoting Jeremiah 7:11). WEB: "a den of
       robbers!" KJV: "a den of thieves." A robbers' den is where
       they hide AFTER crimes — the temple as cover for exploitation.

v.16 — NET: "Out of the mouths of children and nursing infants
       you have prepared praise for yourself" — quoting Psalm 8:2.
       WEB: "Out of the mouth of babes and nursing babies." Children
       praise what the religious leaders refuse to acknowledge.

v.42 — NET: "The stone the builders rejected has become the
       cornerstone" — quoting Psalm 118:22. "Cornerstone"
       (kephalEn gOnias = head of the corner). WEB: "The stone
       which the builders rejected was made the head of the corner."
       Jesus is the rejected stone that becomes the foundation.

v.43 — NET: "the kingdom of God will be taken from you and given
       to a people who will produce its fruit" — "a people"
       (ethnei = a nation — singular). WEB: "given to a nation
       producing its fruits." KJV: "given to a nation bringing
       forth the fruits thereof." Israel's privilege transferred
       to a fruit-bearing people."""

notes[22] = """v.14 — NET: "For many are called, but few are chosen" —
       "called" (klEtoi) vs. "chosen" (eklektoi). WEB: "many are
       called, but few chosen." KJV: "many are called, but few are
       chosen." The wedding invitation goes widely; those who
       respond properly are the elect.

v.17 — NET: "Is it right to pay taxes to Caesar or not?" — "taxes"
       (kEnson = census tax/poll tax — Latin loanword). WEB: "Is
       it lawful to pay taxes to Caesar, or not?" A trap: yes =
       lose the crowd; no = face Rome. Jesus transcends the binary.

v.21 — NET: "Give to Caesar the things that are Caesar's, and to
       God the things that are God's" — "give" (apodote = render/
       give back what is owed). WEB: "Give therefore to Caesar."
       KJV: "Render therefore unto Caesar." Coins bear Caesar's
       image — render them. Humans bear GOD'S image — render
       yourselves.

v.37 — NET: "Love the Lord your God with all your heart, with all
       your soul, and with all your mind" — quoting Deuteronomy 6:5.
       "Mind" (dianoia — Matthew adds this). WEB: "with all your
       heart, with all your soul, and with all your mind." Total
       love: emotional (heart), volitional (soul), intellectual (mind).

v.44 — NET: "The Lord said to my lord, 'Sit at my right hand,
       until I put your enemies under your feet'" — quoting Psalm
       110:1. WEB: "The Lord said to my Lord." KJV: "The LORD said
       unto my Lord." David's Son is also David's Lord — an
       unanswerable riddle proving the Messiah's deity."""

notes[23] = """v.3  — NET: "do whatever they tell you and follow it, but do
       not do what they do, for they do not practice what they
       teach" — "do not do what they do" (kata de ta erga autOn
       mE poieite). WEB: "don't do their works." Authority is
       valid even when the authority-holder is hypocritical.

v.13 — NET: "you shut the door of the kingdom of heaven in
       people's faces" — "shut the door" (kleiete = lock/close).
       WEB: "you shut up the Kingdom of Heaven against men." KJV:
       "ye shut up the kingdom of heaven against men." They neither
       enter nor allow others to enter.

v.23 — NET: "you neglect what is more important in the law —
       justice, mercy, and faithfulness!" — "more important" (ta
       barytera = the weightier things). WEB: "the weightier
       matters of the law: justice, mercy, and faith." KJV: "the
       weightier matters of the law." Not all commandments are
       equal — some are weightier.

v.27 — NET: "you are like whitewashed tombs that look beautiful
       on the outside but inside are full of dead men's bones" —
       "whitewashed tombs" (taphois kekoniamenois). WEB: "like
       whitewashed tombs." Beautiful exterior concealing interior
       corruption — the most vivid image of religious hypocrisy.

v.37 — NET: "how often I have longed to gather your children
       together as a hen gathers her chicks under her wings" —
       "longed" (EthelEsa = wanted/desired repeatedly). WEB: "how
       often I would have gathered your children together." KJV:
       "how often would I have gathered." Maternal imagery for God
       — tender, protective, rejected."""

notes[24] = """v.3  — NET: "what will be the sign of your coming and of the
       end of the age?" — "coming" (parousias = presence/arrival)
       and "end of the age" (synteleias tou aiOnos). WEB: "the
       sign of your coming, and of the end of the age." Two
       questions or one? The disciples may not have distinguished
       between temple destruction and world-end.

v.14 — NET: "And this gospel of the kingdom will be preached
       throughout the whole inhabited earth as a testimony to all
       the nations" — "whole inhabited earth" (holE tE oikoumenE).
       WEB: "preached in the whole world." KJV: "preached in all
       the world." Global proclamation as a precondition of the end.

v.27 — NET: "For just like the lightning comes from the east and
       flashes to the west, so the coming of the Son of Man will
       be" — "lightning" (astrapE = a flash visible everywhere
       simultaneously). WEB: "as the lightning flashes from the
       east." No secret coming — visible, unmistakable, universal.

v.36 — NET: "But as for that day and hour no one knows it — not
       even the angels in heaven — except the Father alone" — "no
       one knows" (oudeis oiden). Some manuscripts add "nor the
       Son" (as in Mark 13:32). WEB: "no one knows." KJV: "no man
       knoweth." Uncertainty about the time is part of the design.

v.44 — NET: "Therefore you also must be ready, because the Son of
       Man will come at an hour when you do not expect him" —
       "ready" (hetoimoi = prepared/in a state of readiness). WEB:
       "be ready." KJV: "be ye also ready." Readiness is not
       prediction but faithful living at all times."""

notes[25] = """v.1  — NET: "the kingdom of heaven will be like ten virgins
       who took their lamps and went out to meet the bridegroom" —
       "lamps" (lampadas = torches). WEB: "ten virgins who took
       their lamps." Not small oil lamps but torches for a
       nighttime procession — they need oil reserves.

v.14 — NET: "it is like a man going on a journey, who summoned
       his slaves and entrusted his property to them" — "entrusted"
       (paredOken = handed over). WEB: "entrusted his goods to
       them." "Talent" (talanton = ~20 years' wages) — enormous
       sums, not small coins.

v.21 — NET: "Well done, good and faithful slave!" — "faithful"
       (piste = trustworthy/reliable). WEB: "Well done, good and
       faithful servant." KJV: "Well done, thou good and faithful
       servant." The commendation is for FAITHFULNESS, not the size
       of the return — both 5-talent and 2-talent servants receive
       identical praise.

v.40 — NET: "whatever you did for one of the least of these
       brothers or sisters of mine, you did for me" — "the least"
       (tOn elachistOn = the most insignificant). WEB: "inasmuch
       as you did it to one of the least of these my brothers."
       Christ identifies with the hungry, naked, sick, imprisoned.

v.46 — NET: "And these will depart into eternal punishment, but
       the righteous into eternal life" — "eternal" (aiOnion) —
       the same adjective modifies both punishment and life. WEB:
       "these will go away into eternal punishment." If one is
       temporary, both must be — the parallel demands equal duration."""

notes[26] = """v.15 — NET: "What are you willing to give me to betray him to
       you?" — "willing to give" (thelete moi dounai). WEB: "What
       are you willing to give me?" KJV: "What will ye give me?"
       Judas initiates. "They set out for him thirty pieces of
       silver" — the price of a slave (Exodus 21:32).

v.26 — NET: "Take, eat, this is my body" — "this is" (touto estin)
       — the words of institution. WEB: "Take, eat; this is my
       body." Debated across church history: literal? spiritual?
       memorial? The simplicity of the words conceals centuries of
       theological debate.

v.28 — NET: "this is my blood of the covenant, that is poured out
       for many for the forgiveness of sins" — "blood of the
       covenant" (to haima mou tEs diathEkEs). WEB: "my blood of
       the new covenant." KJV: "my blood of the new testament."
       Some manuscripts omit "new" — NET/ESV omit; KJV includes.

v.39 — NET: "My Father, if possible, let this cup pass from me!
       Yet not what I will, but what you will" — "if possible"
       (ei dynaton estin). WEB: "if it is possible." KJV: "if it
       be possible." Honest prayer + total submission — the model
       for all prayer in suffering.

v.64 — NET: "You have said it yourself. But I tell you, from now
       on you will see the Son of Man sitting at the right hand of
       the Power" — "You have said it" (sy eipas = affirmative
       answer in rabbinic idiom). WEB: "You have said so." KJV:
       "Thou hast said." Jesus affirms He is the Christ (v.63)
       then escalates: He will sit at God's right hand (Psalm 110)
       and come on clouds (Daniel 7:13)."""

notes[27] = """v.3  — NET: "I have sinned by betraying innocent blood!" —
       "innocent blood" (haima athOon). WEB: "I have sinned in
       that I betrayed innocent blood." KJV: "I have sinned in
       that I have betrayed the innocent blood." Judas' remorse is
       not repentance — it leads to suicide, not restoration.

v.22 — NET: "What then shall I do with Jesus who is called the
       Christ?" — "What shall I do?" (ti poiEsO). WEB: "What then
       shall I do to Jesus, who is called Christ?" Pilate's
       question — the question every person must answer. He chose
       politically rather than justly.

v.37 — NET: "This is Jesus, the King of the Jews" — the charge
       (titlon = inscription/notice) above the cross. WEB: "THIS
       IS JESUS, THE KING OF THE JEWS." Written in Hebrew, Greek,
       and Latin (John 19:20) — universal proclamation even in
       execution.

v.46 — NET: "My God, my God, why have you forsaken me?" — quoting
       Psalm 22:1. "Forsaken" (enkatelipes = abandoned/left behind).
       WEB: "My God, my God, why have you forsaken me?" The cry of
       dereliction — the Son experiences separation from the
       Father as He bears sin. The darkest moment in Scripture.

v.51 — NET: "the temple curtain was torn in two, from top to
       bottom" — "from top to bottom" (ap' anOthen heOs katO =
       from above downward). WEB: "from the top to the bottom."
       God tears it from heaven downward — not human action but
       divine. Access to God's presence is now open to all."""

notes[28] = """v.2  — NET: "there was a violent earthquake, for an angel of
       the Lord descending from heaven came and rolled away the
       stone" — "violent earthquake" (seismos megas). WEB: "a
       great earthquake." The same creation that groaned at His
       death shakes at His rising.

v.6  — NET: "He is not here, for he has been raised, just as he
       said" — "has been raised" (EgerthE — passive: God raised
       Him). WEB: "He is not here, for he has risen." KJV: "He is
       not here: for he is risen." The angel's announcement —
       the tomb is evidence, not residence.

v.18 — NET: "All authority in heaven and on earth has been given
       to me" — "all authority" (pasa exousia = every kind of
       power, in every realm). WEB: "All authority has been given
       to me." KJV: "All power is given unto me." The universal
       scope grounds the universal commission.

v.19 — NET: "Therefore go and make disciples of all nations,
       baptizing them in the name of the Father and the Son and
       the Holy Spirit" — "make disciples" (mathEteusate = the
       main imperative — going, baptizing, teaching are participles
       supporting it). WEB: "Go and make disciples of all nations."
       The single command is discipling; the method is going,
       baptizing, teaching.

v.20 — NET: "I am with you always, to the end of the age" —
       "always" (pasas tas hEmeras = all the days). WEB: "I am
       with you always, even to the end of the age." KJV: "I am
       with you alway, even unto the end of the world." Emmanuel
       ("God with us," 1:23) bookends the Gospel — He who was
       WITH us at birth is WITH us until the end."""

for ch, note_text in sorted(notes.items()):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Matthew " + str(ch))
        else:
            print("  skip Matthew " + str(ch))
    else:
        print("  missing Matthew " + str(ch))
