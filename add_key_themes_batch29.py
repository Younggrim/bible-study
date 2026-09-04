#!/usr/bin/env python3
"""Batch 29: Revelation 1-15, 17-22 (chapter 16 already has Key Themes).

    python3 add_key_themes_batch29.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS_PROLOGUE = "Apocalyptic Prophecy — Prologue and Vision of Christ"
CLS_LETTERS = "Apocalyptic Prophecy — Letters to the Seven Churches"
CLS_THRONE = "Apocalyptic Prophecy — The Throne Room of Heaven"
CLS_SCROLL = "Apocalyptic Prophecy — The Sealed Scroll and the Lamb"
CLS_SEALS = "Apocalyptic Prophecy — The Seal Judgments"
CLS_SEALED_MULT = "Apocalyptic Prophecy — The Sealed Multitude"
CLS_TRUMPETS = "Apocalyptic Prophecy — The Trumpet Judgments"
CLS_LITTLE_BOOK = "Apocalyptic Prophecy — The Little Book"
CLS_WITNESSES = "Apocalyptic Prophecy — The Two Witnesses"
CLS_WOMAN_DRAGON = "Apocalyptic Prophecy — The Woman and the Dragon"
CLS_BEASTS = "Apocalyptic Prophecy — The Two Beasts"
CLS_LAMB_144K = "Apocalyptic Prophecy — The Lamb and the 144,000"
CLS_BOWL_PRELUDE = "Apocalyptic Prophecy — Prelude to the Bowl Judgments"
CLS_HARLOT = "Apocalyptic Prophecy — Babylon the Great Harlot"
CLS_BABYLON_FALL = "Apocalyptic Prophecy — The Fall of Babylon"
CLS_RETURN = "Apocalyptic Prophecy — The Return of Christ"
CLS_MILLENNIUM = "Apocalyptic Prophecy — The Millennium and Final Judgment"
CLS_NEW_CREATION = "Apocalyptic Prophecy — The New Heaven and New Earth"
CLS_EPILOGUE = "Apocalyptic Prophecy — Epilogue"

DATA = {
    "revelation1": (CLS_PROLOGUE,
        "a title naming itself in its first three words, the "
        "Revelation of Jesus Christ, before tracing its own chain of "
        "transmission through four hands from God to a reader, the "
        "book's only beatitude aimed at a room listening aloud rather "
        "than a solitary scholar, a greeting naming its source three "
        "times over before three titles are given to Jesus that set "
        "the terms for everything that follows, a vision assembled "
        "deliberately from Daniel and Ezekiel describing someone "
        "standing in the midst of the lampstands rather than above "
        "them, and a collapse answered by a hand and a credential, I "
        "am he that liveth, and was dead, and behold, I am alive for "
        "evermore, and have the keys of hell and of death"),
    "revelation2": (CLS_LETTERS,
        "a fixed pattern repeated for every letter, address, "
        "self-description, commendation, rebuke, command, promise "
        "and a call to hear, a church at Ephesus commended for labor "
        "and discernment yet charged with having left its first love, "
        "a persecuted church at Smyrna receiving no rebuke at all, "
        "only encouragement to be faithful unto death, a compromising "
        "church at Pergamos tolerating false doctrine even while "
        "holding fast where Satan's seat is, and a corrupt church at "
        "Thyatira tolerating a false prophetess the letter simply "
        "calls Jezebel"),
    "revelation3": (CLS_LETTERS,
        "three final churches representing conditions that recur in "
        "every era, a dead church at Sardis holding a reputation for "
        "life it does not actually possess, a faithful church at "
        "Philadelphia receiving no rebuke and only an open door no "
        "one can shut, a lukewarm church at Laodicea so self-"
        "satisfied it cannot see its own wretchedness, poverty and "
        "blindness, and one of the most famous verses in Scripture "
        "arriving not as an evangelistic appeal to outsiders but as a "
        "knock addressed to a church that has locked him out"),
    "revelation4": (CLS_THRONE,
        "a door opened in heaven and John caught up through it into "
        "the very control center from which all authority proceeds, "
        "a throne described entirely in gemstone imagery rather than "
        "in any human features, twenty-four elders crowned and "
        "enthroned around it, four living creatures full of eyes "
        "offering ceaseless worship, holy, holy, holy, and elders who "
        "respond to that worship by casting their own crowns before "
        "the throne and naming creation itself as the reason God is "
        "worthy"),
    "revelation5": (CLS_SCROLL,
        "a sealed scroll in God's right hand that no one in heaven, "
        "earth or under the earth is found worthy to open, John's "
        "weeping answered by an elder's announcement of a Lion that, "
        "when John actually looks, turns out to be a Lamb as it had "
        "been slain, seven horns and seven eyes standing for complete "
        "power and complete knowledge on a creature defined by its "
        "wounds rather than its strength, a new song crediting "
        "redemption to blood drawn from every kindred, tongue, people "
        "and nation, and worship that spreads outward from the throne "
        "to angels beyond counting to every creature in all "
        "creation"),
    "revelation6": (CLS_SEALS,
        "four horsemen released one at a time, each summoned by a "
        "living creature's own command, come and see, a black horse "
        "and a pair of balances turning famine into what reads almost "
        "like an inflation report, a fourth rider named simply Death "
        "with Hell following behind him and granted power over a "
        "fourth of the earth, martyred souls under the altar crying "
        "how long and told to wait until their number is complete, "
        "and cosmic upheaval so total that kings and slaves alike "
        "hide together asking the same terrified question, who shall "
        "be able to stand"),
    "revelation7": (CLS_SEALED_MULT,
        "an interlude answering the very question that closed the "
        "previous chapter, four angels holding back destructive winds "
        "until a seal is placed on God's servants first, a hundred "
        "forty-four thousand sealed in exact, equal numbers from "
        "twelve tribes of Israel, an innumerable multitude from every "
        "nation appearing suddenly in white robes with palm branches, "
        "an identity given for that multitude that ties their white "
        "robes to blood rather than to bleach, these are they which "
        "came out of great tribulation, and have washed their robes "
        "in the blood of the Lamb, and a reward described entirely in "
        "terms of absence, no more hunger, no more thirst, no more "
        "tears"),
    "revelation8": (CLS_TRUMPETS,
        "half an hour of silence in heaven following chapters of "
        "ceaseless worship, an unexpected pause that reads as awe "
        "rather than emptiness, seven angels receiving seven trumpets "
        "while another angel offers incense mixed with the prayers of "
        "the saints, that same censer then filled with fire and cast "
        "down to earth so prayer itself triggers judgment, four "
        "trumpets each striking a third of something, trees, sea, "
        "rivers, sun, moon and stars, the plagues of Egypt run at a "
        "larger scale but stopped short every time, and a flying "
        "angel announcing three woes still to come before the worst "
        "of it even starts"),
    "revelation9": (CLS_TRUMPETS,
        "a fallen star opening the bottomless pit and releasing smoke "
        "that darkens the sky, locusts described in exhausting, "
        "hybrid detail, horse-like, crowned, human-faced, "
        "lion-toothed, scorpion-tailed, commanded to torment for five "
        "months rather than to kill, men seeking death and unable to "
        "find it, four angels bound at the Euphrates prepared for "
        "this exact moment and released to kill a third of mankind, "
        "an army numbered at two hundred million described by its "
        "horses rather than its riders, and a closing verdict that "
        "lands harder than any plague described so far, the rest of "
        "the men repented not"),
    "revelation10": (CLS_LITTLE_BOOK,
        "an interlude between the sixth and seventh trumpets built "
        "around a mighty angel who straddles sea and land as a claim "
        "on all creation, seven thunders that speak and are then "
        "sealed, John explicitly told not to write down what they "
        "said, an oath sworn by the eternal Creator that there should "
        "be time no longer, a little scroll John is told to eat, "
        "sweet as honey in the mouth but turning bitter in the "
        "stomach, and a command to prophesy again to many peoples, "
        "nations, tongues and kings"),
    "revelation11": (CLS_WITNESSES,
        "a temple measured, altar and worshippers included, while its "
        "outer court is deliberately left unmeasured and handed over "
        "to Gentiles for forty-two months, two witnesses prophesying "
        "twelve hundred sixty days in sackcloth with power like "
        "Elijah's and Moses' combined, their bodies left lying in "
        "Jerusalem's streets for three and a half days while the "
        "world celebrates their deaths, a resurrection and ascension "
        "witnessed publicly by their enemies, and a seventh trumpet "
        "announcing in a single verse what the entire book has been "
        "building toward, the kingdoms of this world are become the "
        "kingdoms of our Lord, and of his Christ"),
    "revelation12": (CLS_WOMAN_DRAGON,
        "a woman clothed with the sun, the moon under her feet and "
        "twelve stars for a crown, imagery that reaches directly back "
        "to Joseph's own dream in Genesis, a great red dragon waiting "
        "specifically to devour her child the moment he is born, a "
        "male child caught up to God's throne the instant he is born, "
        "escaping the very danger that defines the rest of the "
        "chapter, war in heaven ending with Satan cast out "
        "permanently and identified outright, that old serpent, "
        "called the Devil, and Satan, victory credited not to "
        "angelic strength but to the blood of the Lamb and the word "
        "of a testimony held even unto death, and a dragon's pursuit "
        "of the woman's remaining children once he can no longer "
        "reach her directly"),
    "revelation13": (CLS_BEASTS,
        "a beast rising from the sea combining features of Daniel's "
        "four beasts at once, leopard, bear and lion in a single "
        "body, a fatal wound healed that leaves the whole world "
        "marveling and following, forty-two months of blasphemy "
        "permitted before any check is placed on it, a second beast "
        "that imitates in every particular, lamb's horns and a "
        "dragon's voice, promoting worship of the first beast through "
        "wonders rather than through its own claims, and an economic "
        "mark enforcing that worship through the ordinary mechanism "
        "of buying and selling rather than through open persecution"),
    "revelation14": (CLS_LAMB_144K,
        "a hundred forty-four thousand standing with the Lamb on "
        "Mount Zion, marked on the forehead and singing a song no one "
        "else can even learn, three angels flying in succession, each "
        "with exactly one thing to announce, an eternal gospel, a "
        "fallen city named twice for emphasis, Babylon is fallen, is "
        "fallen, and the severest warning in the whole book aimed at "
        "those who take the mark, two sentences of comfort set "
        "deliberately against that warning, blessed are the dead "
        "which die in the Lord, and two harvests closing the chapter, "
        "grain gathered gently and grapes crushed in a winepress "
        "whose blood runs for roughly two hundred miles"),
    "revelation15": (CLS_BOWL_PRELUDE,
        "the shortest chapter in the whole book serving as a prelude "
        "to the final and most severe plagues, wrath called filled up "
        "rather than merely poured for the first time, overcomers "
        "standing on a sea of glass mixed with fire and singing both "
        "the song of Moses and the song of the Lamb together, a "
        "question that assumes its own answer, who shall not fear "
        "thee, O Lord, seven angels emerging from the temple in pure "
        "white with golden sashes, and a heavenly temple filled with "
        "smoke from God's glory that no one may enter until the seven "
        "plagues are complete"),
    "revelation17": (CLS_HARLOT,
        "a great prostitute seated on many waters identified "
        "explicitly as peoples and nations, kings said to have "
        "committed fornication with her while she rides a beast that "
        "ultimately turns against her, a name written on her forehead "
        "that the chapter treats as a mystery to be explained rather "
        "than merely displayed, mystery, Babylon the great, the "
        "mother of harlots, seven heads interpreted as seven "
        "mountains and ten horns as ten kings who give their power to "
        "the beast for one hour, and those same kings destroying the "
        "very woman they once served the moment the beast turns them "
        "against her"),
    "revelation18": (CLS_BABYLON_FALL,
        "a city's fall announced in the past tense before the details "
        "are even given, Babylon the great is fallen, a direct call "
        "issued to God's own people still living inside her, come out "
        "of her, my people, three separate laments in succession, "
        "kings, merchants and sailors, each mourning wealth rather "
        "than mourning the city itself, a cargo list that ends, "
        "without comment, on slaves and the souls of men, and a "
        "millstone cast into the sea as the chapter's own image for "
        "how suddenly and completely the whole system goes under"),
    "revelation19": (CLS_RETURN,
        "four uses of Alleluia, the only occurrences anywhere in the "
        "New Testament, a wedding announced for the Lamb whose bride "
        "is already dressed in the righteous acts of the saints "
        "rather than in anything of her own making, heaven opening "
        "onto a white horse and a rider whose name no one but himself "
        "actually knows, a robe already dipped in blood before a "
        "single battle has been fought, a title given last rather "
        "than first, king of kings, and lord of lords, and a beast "
        "and false prophet captured and thrown alive into the lake of "
        "fire while everyone else is simply slain by a sword coming "
        "from the rider's own mouth"),
    "revelation20": (CLS_MILLENNIUM,
        "Satan bound with a chain and cast into the abyss for a "
        "thousand years specifically so he cannot deceive the nations "
        "during that time, martyrs who refused the beast's mark "
        "resurrected to reign with Christ in what the text itself "
        "calls the first resurrection, a brief release at the end of "
        "the thousand years that Satan uses immediately to deceive "
        "nations and gather them for one final battle, fire from "
        "heaven ending that battle before it properly starts, and a "
        "great white throne before which earth and heaven themselves "
        "flee away, books opened alongside one particular book whose "
        "absence, rather than any recorded deed, decides the final "
        "sentence"),
    "revelation21": (CLS_NEW_CREATION,
        "a first heaven and first earth passing away and a new one "
        "appearing with a single detail singled out, no more sea, a "
        "city descending as a bride adorned for her husband rather "
        "than being built up from the ground, a repeated refrain of "
        "absence naming exactly what is gone, no more tears, death, "
        "sorrow, crying or pain, a declaration spoken twice in "
        "different tenses, behold, I make all things new, and it is "
        "done, and a city measured as a perfect cube some fourteen "
        "hundred miles on each side, containing no temple at all "
        "because God and the Lamb are themselves the temple"),
    "revelation22": (CLS_EPILOGUE,
        "a pure river of the water of life flowing directly from the "
        "throne, a tree of life bearing twelve kinds of fruit and "
        "leaves specifically for the healing of the nations, no more "
        "curse stated in three words that reverse the opening "
        "chapters of Genesis, the phrase behold, I come quickly "
        "repeated three times across a short epilogue, John rebuked "
        "for trying to worship the very angel who showed him all of "
        "this, a book left deliberately unsealed because the time is "
        "near rather than distant, and the whole of Scripture closing "
        "on an invitation rather than a warning, whosoever will, let "
        "him take the water of life freely"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
