#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Acts chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/05 - Acts"

notes = dict()

notes[1] = """v.5  — NET: "you will be baptized with the Holy Spirit not
       many days from now" — "baptized with" (en pneumati
       baptisthesesthe). WEB: "you will be baptized in the Holy
       Spirit." KJV: "ye shall be baptized with the Holy Ghost."
       The preposition "in/with" is the same Greek word (en).

v.8  — NET: "you will receive power when the Holy Spirit has come
       upon you, and you will be my witnesses" — "power" (dynamin)
       and "witnesses" (martyres, from which we get "martyr"). WEB:
       "you will receive power when the Holy Spirit has come upon
       you." Witness often cost them their lives.

v.9  — NET: "he was lifted up while they were watching, and a
       cloud hid him from their sight" — "a cloud" recalls the
       Shekinah glory cloud. WEB: "a cloud received him out of
       their sight." KJV: "a cloud received him out of their
       sight." The Ascension completes the earthly ministry.

v.11 — NET: "This same Jesus who has been taken up from you into
       heaven will come back in the same way" — "in the same way"
       (hon tropon) — visible, bodily, from the sky. WEB: "will
       come back in the same way." The Second Coming will mirror
       the Ascension.

v.26 — NET: "the lot fell to Matthias, and he was counted with
       the eleven apostles" — "the lot fell" (epesen ho kleros) —
       OT method of discerning God's will (Proverbs 16:33). WEB:
       "the lot fell on Matthias." This is the last time lots are
       used — after Pentecost, the Spirit guides directly."""

notes[2] = """v.2  — NET: "a sound like a violent wind blowing came from
       heaven and filled the entire house" — "violent wind" (pnoes
       biaias = a forceful breath/blast). WEB: "like a rushing
       mighty wind." KJV: "a rushing mighty wind." The word for
       "wind/breath" (pnoe) is related to pneuma (Spirit).

v.3  — NET: "tongues spreading out like a fire appeared to them
       and came to rest on each one of them" — "spreading out"
       (diamerizomenai = dividing/distributing). WEB: "tongues
       like fire appeared and were distributed to them." Individual
       flames on each person — personal, not corporate only.

v.4  — NET: "they were all filled with the Holy Spirit and began
       to speak in other languages" — "other languages" (heterais
       glOssais = different tongues). WEB: "other languages." KJV:
       "other tongues." These were real human languages (vv.8-11),
       not ecstatic speech.

v.21 — NET: "everyone who calls on the name of the Lord will be
       saved" — quoting Joel 2:32. WEB: "whoever will call on the
       name of the Lord will be saved." Peter applies Joel's "LORD"
       (Yahweh) to Jesus — a stunning Christological claim.

v.42 — NET: "They were devoting themselves to the apostles'
       teaching and to fellowship, to the breaking of bread and to
       prayer" — four marks of the early church. WEB: "continued
       steadfastly in the apostles' teaching and fellowship, in
       the breaking of bread, and prayer." KJV: "continued
       stedfastly." A pattern for all churches."""

notes[3] = """v.2  — NET: "a man lame from birth was being carried up, who
       was placed at the temple gate called 'the Beautiful Gate'"
       — "Beautiful Gate" — likely the Nicanor Gate between the
       Court of the Gentiles and Court of Women. WEB: "the
       Beautiful Gate." KJV: "the gate of the temple which is
       called Beautiful."

v.6  — NET: "Silver and gold I do not possess, but what I do have
       I give you. In the name of Jesus Christ the Nazarene, stand
       up and walk!" — "what I do have" — spiritual authority
       exceeds material wealth. WEB: "what I have, that I give
       you." KJV: "such as I have give I thee."

v.15 — NET: "you killed the Originator of life, whom God raised
       from the dead" — "Originator" (archEgon = author/pioneer/
       prince). KJV: "Prince of life." WEB: "the Prince of life."
       ASV: "the Prince of life." NET uniquely captures the idea
       of Jesus as the SOURCE of life.

v.19 — NET: "Repent, therefore, and turn back so that your sins
       may be wiped out" — "wiped out" (exaleiphthEnai = erased/
       blotted out). WEB: "that your sins may be blotted out."
       KJV: "that your sins may be blotted out." The image is of
       erasing a written record of debt.

v.21 — NET: "This one heaven must receive until the time all
       things are restored" — "time of restoration" (chronOn
       apokatastaseOs). WEB: "until the times of restoration of
       all things." KJV: "until the times of restitution of all
       things." Christ remains in heaven until God restores
       creation."""

notes[4] = """v.12 — NET: "there is no other name under heaven given among
       people by which we must be saved" — "no other name"
       (ouk estin en allO oudeni hE sOtEria) — the exclusivity of
       Christ. WEB: "no other name under heaven given among men."
       KJV: "none other name under heaven given among men." The
       strongest exclusivist claim in Acts.

v.13 — NET: "they were astonished and began to recognize them as
       companions of Jesus" — "companions" (syn tO IEsou Esan =
       had been with Jesus). WEB: "they recognized that they had
       been with Jesus." KJV: "they took knowledge of them, that
       they had been with Jesus." Jesus' presence transforms
       ordinary people.

v.19 — NET: "Whether it is right before God to obey you rather
       than God, you decide" — "you decide" (krinate) — they throw
       the dilemma back. WEB: "Whether it is right in the sight of
       God to listen to you rather than to God, judge for
       yourselves." Civil disobedience when human law contradicts
       divine command.

v.29 — NET: "we must obey God rather than people" — the apostolic
       principle of conscience. WEB: "We must obey God rather than
       men." KJV: "We ought to obey God rather than men." ASV:
       "We must obey God rather than men." The verb "must" (dei)
       expresses divine necessity.

v.31 — NET: "the place where they were assembled together was
       shaken, and they were all filled with the Holy Spirit" —
       "shaken" (esaleuthE) — physical manifestation of God's
       power in answer to prayer. WEB: "the place was shaken." A
       second Pentecost-like filling in response to persecution."""

notes[5] = """v.3  — NET: "Ananias, why has Satan filled your heart to lie
       to the Holy Spirit?" — "filled your heart" (eplErOsen tEn
       kardian) — a counterfeit filling opposed to the Spirit's
       filling. WEB: "why has Satan filled your heart to lie to
       the Holy Spirit?" Lying to the Spirit = lying to God (v.4).

v.4  — NET: "You have not lied to people but to God!" — Peter
       equates the Holy Spirit (v.3) with God (v.4) — Trinitarian
       theology in action. WEB: "You haven't lied to men, but to
       God." KJV: "thou hast not lied unto men, but unto God."

v.15 — NET: "they even carried the sick out into the streets...
       so that when Peter came by at least his shadow would fall on
       some of them" — "his shadow" — extraordinary faith (or
       superstition) in the apostles' power. WEB: "that Peter's
       shadow might overshadow some of them." Reminiscent of
       Jesus' garment hem (Mark 5:28).

v.34 — NET: "a Pharisee named Gamaliel, a teacher of the law who
       was respected by all the people" — Gamaliel was Paul's
       teacher (22:3) and grandson of Hillel. WEB: "a Pharisee
       named Gamaliel." KJV: "a Pharisee, named Gamaliel." His
       counsel saves the apostles' lives.

v.41 — NET: "they left the council rejoicing because they had been
       considered worthy to suffer dishonor for the sake of the
       name" — "the name" (tou onomatos) — Jesus' name is so
       sacred it needs no further identification. WEB: "worthy to
       suffer dishonor for Jesus' name." Joy in suffering — a
       recurring apostolic theme."""

notes[6] = """v.3  — NET: "select from among you seven men of good reputation,
       full of the Spirit and of wisdom" — three qualifications for
       deacons: reputation, Spirit-fullness, wisdom. WEB: "seven
       men of good report, full of the Holy Spirit and of wisdom."
       KJV: "seven men of honest report, full of the Holy Ghost
       and wisdom."

v.5  — NET: "They chose Stephen, a man full of faith and of the
       Holy Spirit" — Stephen stands out even among the Spirit-
       filled seven. WEB: "full of faith and of the Holy Spirit."
       He is both the first deacon highlighted and the first
       martyr.

v.7  — NET: "The word of God continued to spread, the number of
       disciples in Jerusalem increased greatly" — Luke's growth
       summaries mark transitions (also 9:31, 12:24, 16:5, 19:20).
       WEB: "The word of God increased." KJV: "the word of God
       increased." The word itself grows — active and alive.

v.10 — NET: "they were not able to resist the wisdom and the
       Spirit with which he spoke" — "resist" (antistEnai =
       withstand/stand against). WEB: "they weren't able to
       withstand the wisdom and the Spirit by which he spoke." When
       the Spirit speaks through a person, human arguments fail.

v.15 — NET: "everyone who was sitting in the council looked
       intently at him and saw his face was like the face of an
       angel" — "face of an angel" — radiant, like Moses after
       Sinai (Exodus 34:29-30). WEB: "his face was like the face
       of an angel." KJV: "as it had been the face of an angel."
       Glory shining through flesh."""

notes[7] = """v.22 — NET: "Moses was trained in all the wisdom of the
       Egyptians and was powerful in his words and deeds" — "all
       the wisdom of the Egyptians" — the finest education the
       ancient world offered. WEB: "instructed in all the wisdom
       of the Egyptians." Yet God took 40 years in the desert to
       prepare him further.

v.37 — NET: "God will raise up a prophet for you from among your
       brothers like me" — Stephen quotes Deuteronomy 18:15 —
       Moses predicted a greater prophet (Christ). WEB: "a prophet
       like me from among your brothers." The chain: Abraham,
       Moses, prophets, Christ — all rejected by Israel.

v.48 — NET: "the Most High does not live in houses made by human
       hands" — "made by human hands" (cheiropoiEtois). WEB: "the
       Most High doesn't dwell in temples made with hands." KJV:
       "the most High dwelleth not in temples made with hands."
       Stephen challenges temple-centrism itself.

v.51 — NET: "You stiff-necked people, with uncircumcised hearts
       and ears! You always resist the Holy Spirit" — "always
       resist" (aei antipiptete) — a present-tense pattern across
       generations. WEB: "You always resist the Holy Spirit." The
       accusation that seals his fate.

v.56 — NET: "Look! I see the heavens opened, and the Son of Man
       standing at the right hand of God!" — "standing" (hestOta)
       — Jesus normally sits (Psalm 110:1); here He STANDS — to
       welcome His first martyr. WEB: "the Son of Man standing on
       the right hand of God." KJV: "the Son of man standing on
       the right hand of God." """

notes[8] = """v.1  — NET: "a great persecution against the church in
       Jerusalem began, and all except the apostles were scattered"
       — "scattered" (diesparesan = scattered like seed). WEB: "All
       were scattered abroad." Persecution becomes the mechanism of
       mission — the scattered church plants everywhere it lands.

v.4  — NET: "those who had been scattered went around proclaiming
       the good news of the word" — "proclaiming" (euangelizomenoi
       = evangelizing). WEB: "went about preaching the word." KJV:
       "went every where preaching the word." Every believer a
       preacher — not just apostles.

v.20 — NET: "Give me this power too, so that everyone I place my
       hands on may receive the Holy Spirit" — Simon tries to BUY
       spiritual authority. WEB: "Give me also this power." KJV:
       "Give me also this power." Hence "simony" — the sin of
       purchasing spiritual office.

v.30 — NET: "Do you understand what you are reading?" — Philip's
       question to the Ethiopian. WEB: "Do you understand what you
       are reading?" KJV: "Understandest thou what thou readest?"
       Scripture requires explanation — the Spirit often uses
       people to illuminate the text.

v.36 — NET: "Look, there is water! What is to stop me from being
       baptized?" — the Ethiopian's eager response. WEB: "what is
       keeping me from being baptized?" KJV: "what doth hinder me
       to be baptized?" Faith leads immediately to obedience —
       no bureaucratic delay."""

notes[9] = """v.4  — NET: "Saul, Saul, why are you persecuting me?" — the
       doubled name (as with Abraham, Moses, Samuel) signals
       urgency. WEB: "Saul, Saul, why do you persecute me?" KJV:
       "Saul, Saul, why persecutest thou me?" Persecuting the
       church = persecuting Christ Himself.

v.5  — NET: "I am Jesus whom you are persecuting" — "I am"
       (egO eimi). WEB: "I am Jesus, whom you are persecuting."
       The identification of Christ with His people is absolute.
       To touch them is to touch Him.

v.15 — NET: "this man is my chosen instrument to carry my name
       before Gentiles and kings and the people of Israel" —
       "chosen instrument" (skeuos eklogEs = vessel of election).
       WEB: "he is my chosen vessel." KJV: "he is a chosen vessel
       unto me." A tool for a specific purpose — Gentile mission.

v.18 — NET: "immediately something like scales fell from his
       eyes, and he could see again" — "something like scales"
       (hOs lepides). WEB: "immediately something like scales fell
       from his eyes." Physical blindness removed paralleling
       spiritual blindness removed.

v.20 — NET: "immediately he began to proclaim Jesus in the
       synagogues, saying, 'This man is the Son of God'" — "Son
       of God" — Paul's first sermon. WEB: "he immediately
       proclaimed Jesus in the synagogues." KJV: "straightway he
       preached Christ in the synagogues." The persecutor becomes
       the preacher — immediately."""

notes[10] = """v.14 — NET: "I have never eaten anything defiled and ritually
       unclean!" — "defiled" (koinon = common/profane) and
       "unclean" (akatharton). WEB: "I have never eaten anything
       that is common or unclean." KJV: "I have never eaten any
       thing that is common or unclean." Peter's lifelong
       observance — about to be overturned.

v.15 — NET: "What God has made clean, you must not consider
       ritually unclean!" — "What God has made clean" (ha ho theos
       ekatharisen). WEB: "What God has cleansed, you must not
       call unclean." KJV: "What God hath cleansed, that call not
       thou common." Divine authority overrides human tradition.

v.34 — NET: "I now truly understand that God does not show
       favoritism in dealing with people" — "show favoritism"
       (prosOpolEmptEs = face-receiver). WEB: "God is no respecter
       of persons." KJV: "God is no respecter of persons." Peter's
       worldview shifts — the gospel is for ALL ethnicities.

v.44 — NET: "the Holy Spirit fell on all those who heard the
       message" — "fell on" (epepesen) — sudden, sovereign,
       uninvited. WEB: "the Holy Spirit fell on all those who
       heard the word." No laying on of hands, no prayer — the
       Spirit acts sovereignly on Gentiles.

v.47 — NET: "No one can withhold the water for these people to
       be baptized, who have received the Holy Spirit just as we
       did, can he?" — "just as we did" (hOs kai hEmeis) — full
       equality. WEB: "who have received the Holy Spirit just as
       we did." The Spirit's gift settles the Gentile question."""

notes[11] = """v.14 — NET: "a message by which you and your entire household
       will be saved" — "your entire household" (pas ho oikos sou)
       — household salvation is a pattern in Acts (16:15, 16:31,
       18:8). WEB: "you and all your house will be saved."

v.18 — NET: "God has granted the repentance that leads to life
       even to the Gentiles" — "granted" (edOken = gave as a gift).
       WEB: "God has also granted to the Gentiles repentance to
       life." KJV: "Then hath God also to the Gentiles granted
       repentance unto life." Repentance itself is a divine gift.

v.21 — NET: "The hand of the Lord was with them, and a great
       number who believed turned to the Lord" — "the hand of the
       Lord" — OT idiom for divine power/favor. WEB: "the hand of
       the Lord was with them." KJV: "the hand of the Lord was
       with them." Human preaching + divine power = conversions.

v.26 — NET: "the disciples were first called Christians at
       Antioch" — "Christians" (Christianous = Christ-followers).
       WEB: "The disciples were called Christians first in
       Antioch." KJV: "the disciples were called Christians first
       in Antioch." Originally likely a nickname/insult — they
       owned it.

v.28 — NET: "Agabus stood up and predicted by the Spirit that a
       severe famine was about to come over the whole inhabited
       world" — "predicted by the Spirit" (esEmanen dia tou
       pneumatos). WEB: "signified by the Spirit." Fulfilled under
       Claudius (AD 44-48). Prompted the relief collection."""

notes[12] = """v.2  — NET: "He had James, the brother of John, executed with
       a sword" — "James the brother of John" — the first apostle
       martyred. WEB: "killed James, the brother of John, with the
       sword." KJV: "killed James the brother of John with the
       sword." One sentence — Luke's restraint regarding apostolic
       death.

v.7  — NET: "an angel of the Lord appeared, and a light shone in
       the prison cell. He struck Peter on the side and woke him
       up" — "struck" (pataxas = hit/slapped). WEB: "struck Peter
       on the side." Peter sleeps so soundly between two soldiers
       the night before his likely execution that an angel must
       physically hit him.

v.15 — NET: "You're out of your mind! But she kept insisting that
       it was Peter" — the praying church doesn't believe their
       prayer was answered. WEB: "You are crazy!" KJV: "Thou art
       mad." The irony: they prayed earnestly (v.5) then refused
       to believe.

v.23 — NET: "an angel of the Lord struck Herod down because he
       did not give the glory to God, and he was eaten by worms
       and died" — "eaten by worms" (genomenosSkOlEkobrOtos). WEB:
       "he was eaten by worms and died." KJV: "he was eaten of
       worms, and gave up the ghost." Josephus confirms this death.

v.24 — NET: "But the word of God kept on increasing and spreading"
       — contrast: Herod dies, the word grows. WEB: "the word of
       God grew and multiplied." KJV: "the word of God grew and
       multiplied." The king dies; the King's message thrives."""

notes[13] = """v.2  — NET: "The Holy Spirit said, 'Set apart for me Barnabas
       and Saul for the work to which I have called them'" — "Set
       apart for ME" — the Spirit speaks in the first person,
       claiming divine prerogative. WEB: "Separate Barnabas and
       Saul for me." The Spirit initiates mission.

v.9  — NET: "Saul (also known as Paul)" — the transition from
       his Hebrew name to his Roman name occurs here. WEB: "who is
       also called Paul." KJV: "Saul, (who also is called Paul)."
       Not a name change at conversion but a contextual shift for
       Gentile ministry.

v.38 — NET: "through this one forgiveness of sins is proclaimed
       to you, and by this one everyone who believes is justified
       from everything from which the law of Moses could not
       justify you" — "justified from everything" — beyond what
       the Law could accomplish. WEB: "everyone who believes is
       justified from all things." Grace exceeds law.

v.46 — NET: "Since you reject it and do not consider yourselves
       worthy of eternal life, we are turning to the Gentiles" —
       "do not consider yourselves worthy" (ouk axious krinete
       heautous) — they judged themselves unworthy by their
       rejection. WEB: "judge yourselves unworthy of eternal life."

v.48 — NET: "all who had been appointed for eternal life believed"
       — "appointed" (tetagmenoi = ordered/arranged/enrolled). WEB:
       "as many as were appointed to eternal life believed." KJV:
       "as many as were ordained to eternal life believed." One of
       the strongest predestination texts in Acts."""

notes[14] = """v.3  — NET: "they spent considerable time there, speaking
       boldly for the Lord, who testified to his message of grace
       by granting miraculous signs and wonders" — "testified to
       his message" — God Himself confirming the word. WEB: "who
       testified to the word of his grace." Signs serve the word.

v.11 — NET: "The gods have come down to us in human form!" —
       the Lystrans identify Barnabas as Zeus and Paul as Hermes.
       WEB: "The gods have come down to us in the likeness of
       men!" A local legend about Zeus/Hermes visiting Lystra
       (Ovid's story of Philemon and Baucis) fueled this reaction.

v.15 — NET: "we are proclaiming the good news to you, that you
       should turn from these worthless things to the living God"
       — "worthless things" (mataiOn = vain/futile). WEB: "turn
       from these vain things to the living God." KJV: "turn from
       these vanities unto the living God." Idols are empty.

v.19 — NET: "they stoned Paul and dragged him out of the city,
       presuming him to be dead" — "presuming him to be dead"
       (nomisantes auton tethnEkenai). WEB: "supposing that he was
       dead." KJV: "supposing he had been dead." Whether Paul
       actually died (cf. 2 Cor 12:2-4) is debated.

v.22 — NET: "We must enter the kingdom of God through many
       persecutions" — "must" (dei = divine necessity). WEB:
       "through many afflictions we must enter into God's Kingdom."
       KJV: "through much tribulation enter into the kingdom of
       God." Suffering is the normal path, not the exception."""

notes[15] = """v.9  — NET: "he made no distinction between us and them,
       cleansing their hearts by faith" — Peter's argument at the
       Jerusalem Council. "No distinction" (ouden diekrinen). WEB:
       "making no distinction between us and them." The Spirit
       treats Jew and Gentile identically.

v.10 — NET: "why are you putting God to the test by placing on
       the neck of the disciples a yoke that neither our ancestors
       nor we have been able to bear?" — "a yoke" (zygon) — the
       Law as impossible burden. WEB: "a yoke on the neck of the
       disciples which neither our fathers nor we were able to
       bear." Honest Jewish admission.

v.11 — NET: "we believe that we are saved through the grace of
       the Lord Jesus, in the same way as they are" — "in the same
       way as THEY are" — remarkable reversal. Not "Gentiles saved
       like Jews" but "Jews saved like Gentiles" — by grace alone.
       WEB: "we believe that we are saved through the grace of the
       Lord Jesus, just as they are."

v.28 — NET: "For it seemed best to the Holy Spirit and to us" —
       "the Holy Spirit and to us" — divine and human agreement.
       WEB: "it seemed good to the Holy Spirit, and to us." KJV:
       "it seemed good to the Holy Ghost, and to us." The Spirit
       leads; the church confirms.

v.39 — NET: "They had such a sharp disagreement that they parted
       company" — "sharp disagreement" (paroxysmos = irritation/
       provocation). WEB: "the contention was so sharp." KJV: "the
       contention was so sharp between them." Even apostles
       disagree — God uses both resulting mission teams."""

notes[16] = """v.6  — NET: "they were prevented by the Holy Spirit from
       speaking the message in the province of Asia" — "prevented
       by the Holy Spirit" — the Spirit closes doors as well as
       opens them. WEB: "forbidden by the Holy Spirit to speak the
       word in Asia." Divine redirection toward Macedonia.

v.9  — NET: "a vision appeared to Paul during the night: A
       Macedonian man was standing there urging him, 'Come over to
       Macedonia and help us!'" — "Come over and help us" — the
       Macedonian call. WEB: "Come over into Macedonia and help
       us." The gospel enters Europe.

v.14 — NET: "The Lord opened her heart to respond to what Paul
       was saying" — "opened her heart" (ho kyrios diEnoixen tEn
       kardian). WEB: "The Lord opened her heart." KJV: "whose
       heart the Lord opened." God must open hearts for people to
       respond — divine initiative in conversion.

v.25 — NET: "About midnight Paul and Silas were praying and
       singing hymns to God, and the rest of the prisoners were
       listening to them" — "singing hymns" in chains, feet in
       stocks, backs bleeding. WEB: "praying and singing hymns to
       God." Worship in suffering — the prisoners were an audience.

v.31 — NET: "Believe in the Lord Jesus and you will be saved, you
       and your household" — "you and your household" (sy kai ho
       oikos sou). WEB: "Believe in the Lord Jesus Christ, and you
       will be saved, you and your household." KJV: "Believe on
       the Lord Jesus Christ, and thou shalt be saved, and thy
       house." Household salvation pattern."""

notes[17] = """v.2  — NET: "he reasoned with them from the scriptures" —
       "reasoned" (dielexato = dialogued/discussed). WEB: "reasoned
       with them from the Scriptures." KJV: "reasoned with them
       out of the scriptures." Paul's method: argument from the
       OT, not mere assertion.

v.11 — NET: "these Jews were more open-minded than those in
       Thessalonica, for they received the message with great
       eagerness, examining the scriptures every day" — "more
       open-minded" (eugenesteroi = more noble). WEB: "more noble."
       KJV: "more noble." The Bereans' nobility was their eagerness
       to test teaching against Scripture.

v.23 — NET: "as I went around and observed closely your objects
       of worship, I even found an altar with this inscription:
       'To an unknown god'" — "unknown god" (agnOstO theO). WEB:
       "TO AN UNKNOWN GOD." Paul uses their own religiosity as a
       bridge — not condemnation but connection point.

v.28 — NET: "For in him we live and move and have our being" —
       Paul quotes pagan poets (Epimenides and Aratus) to establish
       common ground. WEB: "In him we live, move, and have our
       being." Using secular sources to point toward the true God.

v.32 — NET: "when they heard about the resurrection of the dead,
       some began to scoff" — "scoff" (echleuazon = mock/jeer).
       WEB: "some mocked." KJV: "some mocked." The resurrection
       was the stumbling block for Greek philosophers — they
       accepted immortality of the soul but not bodily resurrection."""

notes[18] = """v.3  — NET: "because he worked at the same trade, he stayed
       with them and they worked together, for they were tentmakers
       by trade" — "tentmakers" (skEnopoioi). WEB: "by trade, they
       were tent makers." KJV: "they were tentmakers." Paul's
       bi-vocational ministry — self-supporting to avoid being a
       burden (1 Thess 2:9).

v.9  — NET: "Do not be afraid, but speak and do not be silent,
       for I am with you" — the Lord's night vision to Paul. WEB:
       "Don't be afraid, but speak and don't be silent." KJV: "Be
       not afraid, but speak." God meets Paul's fear with His
       presence and promise.

v.10 — NET: "because I have many people in this city" — "many
       people" (laos polys) — God's elect in Corinth, not yet
       converted but known to God. WEB: "I have many people in
       this city." God knows His own before they know Him.

v.25 — NET: "He spoke and taught accurately the things about
       Jesus, although he knew only the baptism of John" — Apollos
       had partial knowledge but taught what he knew accurately.
       WEB: "knowing only the baptism of John." Priscilla and
       Aquila filled in the gaps privately (v.26).

v.28 — NET: "he refuted the Jews vigorously in public debate,
       demonstrating from the scriptures that the Christ was Jesus"
       — "vigorously" (eutonOs = powerfully/with stretched sinew).
       WEB: "powerfully refuted the Jews." KJV: "mightily
       convinced the Jews." Apollos' rhetorical gift combined with
       scriptural knowledge."""

notes[19] = """v.2  — NET: "Did you receive the Holy Spirit when you believed?"
       — the crucial question to Ephesian disciples. WEB: "Did you
       receive the Holy Spirit when you believed?" KJV: "Have ye
       received the Holy Ghost since ye believed?" The grammar is
       debated: simultaneous ("when") or subsequent ("since").

v.11 — NET: "God was performing extraordinary miracles through
       the hands of Paul" — "extraordinary" (ou tas tychousas =
       not the ordinary kind). WEB: "God worked special miracles."
       KJV: "God wrought special miracles." Even for Acts, these
       miracles were unusual.

v.19 — NET: "many of those who had practiced magic collected their
       books and burned them in public" — the value: 50,000 silver
       coins (v.19). WEB: "burned them in the sight of all." A
       dramatic public break with the occult — costly repentance.

v.20 — NET: "In this way the word of the Lord continued to grow
       in power and to prevail" — another Lukan growth summary.
       WEB: "the word of the Lord was growing and becoming mighty."
       KJV: "so mightily grew the word of God, and prevailed."
       The word has inherent power.

v.35 — NET: "the city of the Ephesians is the keeper of the
       temple of the great goddess Artemis" — "keeper" (neOkoron =
       temple warden). WEB: "guardian of the temple of the great
       goddess Artemis." The city clerk calms the riot with civic
       logic — the most effective evangelism sometimes comes from
       unexpected sources."""

notes[20] = """v.7  — NET: "On the first day of the week, when we gathered
       together to break bread, Paul began to speak" — "first day
       of the week" — early Christian worship on Sunday (resurrection
       day). WEB: "On the first day of the week." Evidence of
       Sunday gathering in the apostolic era.

v.9  — NET: "a young man named Eutychus...sank into a deep sleep
       while Paul continued to speak" — Paul preached until midnight
       (v.7). WEB: "overcome with deep sleep." KJV: "fallen into
       a deep sleep." The young man fell three stories — Luke notes
       "was picked up dead" (not "appeared dead").

v.24 — NET: "But I do not consider my life worth anything to
       myself, so that I may finish my task and the ministry that
       I received from the Lord Jesus" — "do not consider my life
       worth anything" (oudenos logou poioumai tEn psychEn). WEB:
       "I don't count my own life dear to myself." KJV: "neither
       count I my life dear unto myself."

v.28 — NET: "Watch out for yourselves and for all the flock of
       which the Holy Spirit has made you overseers" — "overseers"
       (episkopous = bishops/overseers). WEB: "which the Holy
       Spirit has made you overseers." Elders appointed by the
       Spirit, not just human selection.

v.35 — NET: "by working in this way we must help the weak, and
       remember the words of the Lord Jesus that he himself said,
       'It is more blessed to give than to receive'" — an unwritten
       saying of Jesus (agraphon) preserved only here. WEB: "It is
       more blessed to give than to receive." Not in the Gospels."""

notes[21] = """v.4  — NET: "they repeatedly told Paul through the Spirit not
       to go to Jerusalem" — "through the Spirit" (dia tou
       pneumatos) — the Spirit revealed the danger, but did the
       Spirit forbid the trip? Paul went anyway. WEB: "through the
       Spirit, that he should not go up to Jerusalem." A difficult
       interpretive question.

v.11 — NET: "a prophet named Agabus came down from Judea... he
       took Paul's belt and tied his own hands and feet" — prophetic
       sign-act (like OT prophets). WEB: "binding his own feet and
       hands." KJV: "bound his own hands and feet." Visual prophecy
       of Paul's arrest.

v.13 — NET: "I am ready not only to be tied up, but even to die
       in Jerusalem for the name of the Lord Jesus" — Paul's
       resolve. WEB: "I am ready not only to be bound, but also to
       die at Jerusalem." KJV: "ready not to be bound only, but
       also to die." Echoes Jesus setting His face toward Jerusalem.

v.14 — NET: "Since he would not be dissuaded, we said no more
       except, 'The Lord's will be done'" — "The Lord's will be
       done" (tou kyriou to thelEma ginesthO). WEB: "The will of
       the Lord be done." Echoes Gethsemane. Submission to God's
       plan even when it means suffering.

v.20 — NET: "You see, brother, how many thousands of Jews there
       are who have believed, and they are all ardent observers of
       the law" — "thousands" (myriades = tens of thousands/
       myriads). WEB: "how many thousands there are among the Jews
       of those who have believed." Jewish Christianity was
       massive and law-observant."""

notes[22] = """v.3  — NET: "I am a Jew, born in Tarsus in Cilicia, but
       brought up in this city, educated with strictness under
       Gamaliel" — "strictness" (akribeian = exactness/precision).
       WEB: "educated at the feet of Gamaliel according to the
       strict tradition." Paul's Jewish credentials are impeccable.

v.6  — NET: "about noon a very bright light from heaven suddenly
       flashed around me" — "very bright" (hikanon) — brighter
       than the midday sun. WEB: "a great light shone around me."
       Paul adds details not in chapter 9 — the brightness, the
       time (noon).

v.16 — NET: "Get up, be baptized, and have your sins washed away,
       calling on his name" — "have your sins washed away"
       (apolousai tas hamartias sou). WEB: "wash away your sins."
       KJV: "wash away thy sins." The aorist middle voice suggests
       personal appropriation through the act of baptism.

v.21 — NET: "Go, because I will send you far away to the
       Gentiles" — "far away to the Gentiles" — the word that
       triggers the riot. WEB: "I will send you far away to the
       Gentiles." KJV: "I will send thee far hence unto the
       Gentiles." Jewish rage at Gentile inclusion.

v.28 — NET: "I acquired this citizenship with a large sum of
       money" — the tribune paid for his citizenship. Paul: "But I
       was even born a citizen." WEB: "I bought my citizenship for
       a great price." Inherited citizenship outranked purchased —
       the tribune is now afraid."""

notes[23] = """v.1  — NET: "I have lived my life with a clear conscience
       before God to this day" — "clear conscience" (syneidEsei
       agathE = good conscience). WEB: "I have lived before God in
       all good conscience until today." KJV: "I have lived in all
       good conscience before God until this day."

v.6  — NET: "I am on trial concerning the hope of the resurrection
       of the dead!" — Paul's masterstroke — splitting the council
       between Pharisees (who believed in resurrection) and
       Sadducees (who didn't). WEB: "concerning the hope and
       resurrection of the dead I am being judged."

v.8  — NET: "the Sadducees say there is no resurrection, or
       angel, or spirit, but the Pharisees acknowledge them all" —
       Luke provides a theological footnote. WEB: "the Sadducees
       say that there is no resurrection, nor angel, nor spirit."
       The Sadducees denied the supernatural realm entirely.

v.11 — NET: "The following night the Lord stood near Paul and
       said, 'Have courage, for just as you have testified about
       me in Jerusalem, so you must also testify in Rome'" — "you
       MUST" (dei = divine necessity). WEB: "you must testify also
       at Rome." The Lord's promise guarantees Paul reaches Rome.

v.24 — NET: "provide mounts for Paul to ride so that he may be
       brought safely to Felix the governor" — 470 soldiers escort
       one prisoner (200 soldiers + 70 cavalry + 200 spearmen).
       WEB: "provide animals for Paul to ride." The conspiracy
       of 40+ men (v.12-13) requires an army to foil."""

notes[24] = """v.5  — NET: "we have found this man to be a troublemaker,
       one who stirs up riots among all the Jews throughout the
       world" — "troublemaker" (loimon = pest/plague). WEB: "a
       plague, an instigator of insurrections." KJV: "a pestilent
       fellow." Tertullus uses inflammatory rhetoric — Paul is a
       disease infecting the empire.

v.14 — NET: "this I confess to you, that I worship the God of our
       ancestors according to the Way, which they call a sect" —
       "the Way" (tEn hodon) — early Christian self-designation.
       WEB: "after the Way." KJV: "after the way." Paul doesn't
       deny belonging to The Way — he redefines it as true Judaism.

v.16 — NET: "I do my best to maintain a clear conscience toward
       God and toward people" — "do my best" (askO = exercise/
       train/discipline myself). WEB: "I exercise myself." KJV:
       "do I exercise myself." Conscience requires ongoing training
       and vigilance.

v.25 — NET: "as Paul talked about righteousness, self-control,
       and the coming judgment, Felix became frightened" —
       "frightened" (emphobos genomenos = becoming terrified). WEB:
       "Felix was terrified." KJV: "Felix trembled." The prisoner
       makes the judge tremble — but Felix never acts on his fear.

v.27 — NET: "After two years had passed, Porcius Festus succeeded
       Felix, and because Felix wanted to do the Jews a favor, he
       left Paul in prison" — two years imprisoned without trial.
       WEB: "desiring to gain favor with the Jews, Felix left Paul
       in bonds." Political calculation over justice."""

notes[25] = """v.8  — NET: "I have committed no offense against the Jewish
       law or against the temple or against Caesar" — three charges
       denied in order. WEB: "Neither against the law of the Jews,
       nor against the temple, nor against Caesar, have I sinned
       at all." Paul covers all jurisdictions.

v.10 — NET: "I am standing before Caesar's judgment seat, where
       I should be tried" — "Caesar's judgment seat" (epi tou
       bEmatos Kaisaros). WEB: "I am standing before Caesar's
       judgment seat." KJV: "I stand at Caesar's judgment seat."
       Paul claims proper Roman jurisdiction.

v.11 — NET: "I appeal to Caesar!" — "I appeal" (epikaloumai =
       I call upon). WEB: "I appeal to Caesar!" KJV: "I appeal
       unto Caesar." A Roman citizen's right — once invoked, the
       case must go to Rome. God's promise (23:11) fulfilled
       through legal process.

v.19 — NET: "they had some points of disagreement with him about
       their own religion and about a man named Jesus who was dead,
       whom Paul claimed to be alive" — Festus' summary to Agrippa
       — reductive but accurate. WEB: "about one Jesus, who was
       dead, whom Paul affirmed to be alive." The resurrection
       distilled to one sentence.

v.25 — NET: "But I found that he had done nothing that deserved
       death" — Festus' verdict: innocent — yet still imprisoned.
       WEB: "I found that he had committed nothing worthy of
       death." KJV: "I found that he had committed nothing worthy
       of death." Echoes Pilate's verdict on Jesus."""

notes[26] = """v.9  — NET: "I too was convinced that I had to do many things
       hostile to the name of Jesus the Nazarene" — "I was
       convinced" (edoxa = I thought/supposed). WEB: "I thought to
       myself that I ought to do many things contrary to the name
       of Jesus of Nazareth." Zeal without knowledge (Rom 10:2).

v.14 — NET: "Saul, Saul, why are you persecuting me? You are
       hurting yourself by kicking against the goads" — "kicking
       against the goads" (pros kentra laktizein) — a proverb: an
       ox kicking the sharp stick only hurts itself. WEB: "It is
       hard for you to kick against the goads." Resistance to God
       is self-destructive.

v.18 — NET: "to open their eyes so that they turn from darkness
       to light and from the power of Satan to God" — Paul's
       commission summarized: illumination, conversion, transfer of
       allegiance. WEB: "to turn them from darkness to light." The
       gospel as rescue operation.

v.28 — NET: "In a short time you will persuade me to become a
       Christian!" — "in a short time" (en oligO) — whether
       sarcastic or sincere is debated. WEB: "With a little
       persuasion you would make me a Christian!" KJV: "Almost thou
       persuadest me to be a Christian." One of Scripture's most
       tragic "almosts."

v.32 — NET: "This man could have been released if he had not
       appealed to Caesar" — the legal irony. WEB: "This man might
       have been set free, if he had not appealed to Caesar." But
       God's plan required Rome (23:11). Human legal decisions
       serve divine purposes."""

notes[27] = """v.10 — NET: "Men, I can see that this voyage is going to end
       in disaster" — "I can see" (theOrO = I perceive/observe).
       WEB: "I perceive that the voyage will be with injury and
       much loss." Paul's practical wisdom — ignored by the captain
       and centurion.

v.20 — NET: "when neither sun nor stars appeared for many days
       and a violent storm continued to batter us, we finally
       abandoned all hope of being saved" — "abandoned all hope"
       (periEreito elpis pasa). WEB: "all hope that we would be
       saved was now taken away." Human hopelessness sets up
       divine intervention.

v.23 — NET: "an angel of the God to whom I belong and whom I
       serve came to me" — "to whom I belong" (hou eimi) — Paul's
       identity: God's possession. WEB: "An angel of God, whose I
       am and whom I serve." Ownership before service.

v.25 — NET: "I have faith in God that it will be just as I have
       been told" — "I have faith" (pisteuO tO theO). WEB: "I
       believe God." KJV: "I believe God." Simple, direct trust —
       the basis for Paul's calm amid 276 panicking people.

v.34 — NET: "not a hair of your head will be lost" — echoing
       Luke 21:18. WEB: "not a hair will perish from any of your
       heads." Sovereign protection — all 276 survive (v.44). God
       keeps His word to the letter."""

notes[28] = """v.3  — NET: "when Paul had gathered a bundle of brushwood and
       was putting it on the fire, a viper came out because of the
       heat and fastened itself on his hand" — "fastened" (kathEpsen
       = attached/bit). WEB: "a viper came out because of the
       heat, and fastened on his hand." The islanders expect him to
       drop dead (v.4).

v.5  — NET: "he shook the creature off into the fire and suffered
       no harm" — fulfilling Mark 16:18 ("they will pick up
       serpents"). WEB: "he shook off the creature into the fire,
       and wasn't harmed." From "murderer" (v.4) to "a god" (v.6)
       — the crowd's fickle judgment.

v.8  — NET: "Paul went in to see him and after praying, placed
       his hands on him and healed him" — "praying... placed his
       hands" — the method: prayer first, then laying on of hands.
       WEB: "praying and laying his hands on him, healed him."
       Paul's miracles on Malta open the door for ministry.

v.23 — NET: "From morning until evening he explained things to
       them, testifying about the kingdom of God and trying to
       convince them about Jesus from both the law of Moses and the
       prophets" — Paul's method: all-day Scripture exposition.
       WEB: "explaining to them, testifying about God's Kingdom."
       The OT proves Jesus.

v.31 — NET: "proclaiming the kingdom of God and teaching about
       the Lord Jesus Christ with complete boldness and without
       restriction" — "without restriction" (akOlytOs = unhindered).
       WEB: "with all boldness, without hindrance." KJV: "with all
       confidence, no man forbidding him." The final word of Acts:
       UNHINDERED. The gospel cannot be stopped."""


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
