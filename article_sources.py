#!/usr/bin/env python3
"""
The allowed article sources, and the per-page picks that fill the Articles tab.

This is the single source of truth for the Articles feature, imported by
add_articles.py (which writes the HTML) and check_new_articles.py (which polls
the sources weekly). Keeping the allow list and the picks in one module means
the writer and the poller can never disagree about what is permitted.

Nothing is copied from any of these sites. Every entry is a link plus a
description written here, exactly as the Commentary tab has always worked.
See add_commentaries.py for the same rule stated there.

Why these four:

  GotQuestions.org   The only source with a stable, derivable per-book URL, so
                     every one of the 1189 chapter pages gets at least one real
                     link without anyone curating it. Also carries two large
                     curated series, Bible-<topic> and Bible-verses-about-<topic>,
                     which land almost exactly on the topical and life pages.
  BibleProject       76 articles, unusually often anchored to a specific chapter
                     or passage rather than a theme. The narrowest but most
                     precise source, and already an allowed video channel here.
  Crossway           Publishes the ESV this site already uses. 93 topic feeds at
                     /articles/tag/<slug>/rss/, each carrying the latest 15, so
                     it is the freshest source week to week.
  GotQuestions Blog  S. Michael Houdmann's personal blog, a first-person
                     pastoral voice rather than reference material. Deliberately
                     used only on life pages, and only for the small subset of
                     posts that are pastoral rather than cultural commentary.
                     The site is also largely dormant, so it contributes little.

Three things this module deliberately does NOT do:

  It does not derive picks by matching book names in article titles. That was
  tried and it is unusable: "John Piper on Gambling", "Podcast: Answering Tough
  Questions About the Holy Spirit (Joel Beeke)", "11 Passages to Read When You
  Lose Your Job", "David Hume" and "Saul of Tarsus" all match a book name while
  having nothing to do with that book. Author names collide with two thirds of
  the New Testament. Anything not derivable from the book table is curated here
  by hand, or it waits in a weekly issue for a person to rule on it.

  It does not carry a per-deployment allow list the way video_sources.py does.
  All four sources are acceptable on both bible-study and New River, so there is
  nothing for the sync to filter and no second list to drift. If that ever stops
  being true, split it the way video_sources.py is split, not by editing the
  mirrored HTML.

  It does not store article text, dates, or authors. Those change upstream and
  would rot. Only the URL, the source, and a description of why a reader might
  want it.
"""
import re

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

# label -> (link text shown to the reader, home page, why it is allowed)
SOURCES = {
    "GotQuestions.org": (
        "gotquestions.org",
        "https://www.gotquestions.org/",
        "Question-and-answer Bible reference, already an allowed video source here",
    ),
    "BibleProject": (
        "bibleproject.com",
        "https://bibleproject.com/articles/",
        "Literary and thematic articles, already an allowed video source here",
    ),
    "Crossway": (
        "crossway.org",
        "https://www.crossway.org/articles/",
        "Publisher of the ESV, which this site already carries",
    ),
    "GotQuestions Blog": (
        "gotquestions.blog",
        "https://www.gotquestions.blog/",
        "First-person pastoral reflection; life pages only",
    ),
}

# Individual articles kept off the site even though their source is allowed.
# Removing a link from the HTML is not enough on its own: the source stays in the
# allow list, so the next weekly poll would suggest it again. Keyed by URL, with
# the reason, because "why was this left out" is the question anyone will have
# later. Same pattern as DROP_VIDEO_IDS in video_sources.py.
DROP_ARTICLE_URLS = {
    "https://www.gotquestions.org/Acts-29-Network.html":
        "matches the Acts 29 pattern but is about the Acts 29 church-planting "
        "network, not the book of Acts, which has 28 chapters",
    "https://www.gotquestions.org/Psalm-151.html":
        "Psalm 151 is outside the Protestant canon, so there is no psalms151 "
        "page for it to sit on",
    "https://www.gotquestions.org/American-Revolution-Romans-13.html":
        "reads Romans 13 through one nation's political history rather than "
        "explaining the chapter",
    "https://www.crossway.org/articles/crossway-special-40-off-all-books-by-john-piper/":
        "promotional, not teaching -- the article feeds carry sale and giveaway "
        "posts alongside real articles",
}

LINK = ('<a href="{url}" target="_blank" '
        'style="color:var(--accent-link);text-decoration:none;'
        'border-bottom:1px dotted var(--accent-link);">{label}</a>')

GQ = "https://www.gotquestions.org/"
BP = "https://bibleproject.com/articles/"
CW = "https://www.crossway.org/articles/"
GQB = "https://www.gotquestions.blog/"


# ---------------------------------------------------------------------------
# Derived: one GotQuestions.org overview page per book, all 66
# ---------------------------------------------------------------------------

# Most books are Book-of-<Name>. The four Gospels are Gospel-of-<Name> and Song
# of Solomon has no prefix at all. Every one of these 66 was confirmed to return
# 200 before being written here.
GQ_BOOK_PAGE = {
    "genesis": "Book-of-Genesis",
    "exodus": "Book-of-Exodus",
    "leviticus": "Book-of-Leviticus",
    "numbers": "Book-of-Numbers",
    "deuteronomy": "Book-of-Deuteronomy",
    "joshua": "Book-of-Joshua",
    "judges": "Book-of-Judges",
    "ruth": "Book-of-Ruth",
    "1samuel": "Book-of-1-Samuel",
    "2samuel": "Book-of-2-Samuel",
    "1kings": "Book-of-1-Kings",
    "2kings": "Book-of-2-Kings",
    "1chronicles": "Book-of-1-Chronicles",
    "2chronicles": "Book-of-2-Chronicles",
    "ezra": "Book-of-Ezra",
    "nehemiah": "Book-of-Nehemiah",
    "esther": "Book-of-Esther",
    "job": "Book-of-Job",
    "psalms": "Book-of-Psalms",
    "proverbs": "Book-of-Proverbs",
    "ecclesiastes": "Book-of-Ecclesiastes",
    "songofsolomon": "Song-of-Solomon",
    "isaiah": "Book-of-Isaiah",
    "jeremiah": "Book-of-Jeremiah",
    "lamentations": "Book-of-Lamentations",
    "ezekiel": "Book-of-Ezekiel",
    "daniel": "Book-of-Daniel",
    "hosea": "Book-of-Hosea",
    "joel": "Book-of-Joel",
    "amos": "Book-of-Amos",
    "obadiah": "Book-of-Obadiah",
    "jonah": "Book-of-Jonah",
    "micah": "Book-of-Micah",
    "nahum": "Book-of-Nahum",
    "habakkuk": "Book-of-Habakkuk",
    "zephaniah": "Book-of-Zephaniah",
    "haggai": "Book-of-Haggai",
    "zechariah": "Book-of-Zechariah",
    "malachi": "Book-of-Malachi",
    "matthew": "Gospel-of-Matthew",
    "mark": "Gospel-of-Mark",
    "luke": "Gospel-of-Luke",
    "john": "Gospel-of-John",
    "acts": "Book-of-Acts",
    "romans": "Book-of-Romans",
    "1corinthians": "Book-of-1-Corinthians",
    "2corinthians": "Book-of-2-Corinthians",
    "galatians": "Book-of-Galatians",
    "ephesians": "Book-of-Ephesians",
    "philippians": "Book-of-Philippians",
    "colossians": "Book-of-Colossians",
    "1thessalonians": "Book-of-1-Thessalonians",
    "2thessalonians": "Book-of-2-Thessalonians",
    "1timothy": "Book-of-1-Timothy",
    "2timothy": "Book-of-2-Timothy",
    "titus": "Book-of-Titus",
    "philemon": "Book-of-Philemon",
    "hebrews": "Book-of-Hebrews",
    "james": "Book-of-James",
    "1peter": "Book-of-1-Peter",
    "2peter": "Book-of-2-Peter",
    "1john": "Book-of-1-John",
    "2john": "Book-of-2-John",
    "3john": "Book-of-3-John",
    "jude": "Book-of-Jude",
    "revelation": "Book-of-Revelation",
}

# Display name per book slug, for the generated overview description.
BOOK_TITLE = {
    "genesis": "Genesis", "exodus": "Exodus", "leviticus": "Leviticus",
    "numbers": "Numbers", "deuteronomy": "Deuteronomy", "joshua": "Joshua",
    "judges": "Judges", "ruth": "Ruth", "1samuel": "1 Samuel",
    "2samuel": "2 Samuel", "1kings": "1 Kings", "2kings": "2 Kings",
    "1chronicles": "1 Chronicles", "2chronicles": "2 Chronicles", "ezra": "Ezra",
    "nehemiah": "Nehemiah", "esther": "Esther", "job": "Job",
    "psalms": "Psalms", "proverbs": "Proverbs", "ecclesiastes": "Ecclesiastes",
    "songofsolomon": "Song of Solomon", "isaiah": "Isaiah",
    "jeremiah": "Jeremiah", "lamentations": "Lamentations",
    "ezekiel": "Ezekiel", "daniel": "Daniel", "hosea": "Hosea", "joel": "Joel",
    "amos": "Amos", "obadiah": "Obadiah", "jonah": "Jonah", "micah": "Micah",
    "nahum": "Nahum", "habakkuk": "Habakkuk", "zephaniah": "Zephaniah",
    "haggai": "Haggai", "zechariah": "Zechariah", "malachi": "Malachi",
    "matthew": "Matthew", "mark": "Mark", "luke": "Luke", "john": "John",
    "acts": "Acts", "romans": "Romans", "1corinthians": "1 Corinthians",
    "2corinthians": "2 Corinthians", "galatians": "Galatians",
    "ephesians": "Ephesians", "philippians": "Philippians",
    "colossians": "Colossians", "1thessalonians": "1 Thessalonians",
    "2thessalonians": "2 Thessalonians", "1timothy": "1 Timothy",
    "2timothy": "2 Timothy", "titus": "Titus", "philemon": "Philemon",
    "hebrews": "Hebrews", "james": "James", "1peter": "1 Peter",
    "2peter": "2 Peter", "1john": "1 John", "2john": "2 John",
    "3john": "3 John", "jude": "Jude", "revelation": "Revelation",
}

# Books the site treats as a single unit in prose, so the description reads
# "the book of Genesis" but "the Psalms" and "Song of Solomon".
NO_BOOK_OF = {"psalms", "songofsolomon", "lamentations"}


# ---------------------------------------------------------------------------
# Curated: chapter-specific picks
# ---------------------------------------------------------------------------

# (book slug, chapter) -> [(source label, url, description)]
#
# These are hand-checked. Every URL here returned 200 when it was added. An
# article that treats a passage spanning two chapters is listed under both.
CHAPTER_ARTICLES = {
    ("genesis", 3): [
        ("Crossway", CW + "how-jesus-fulfilled-a-prophecy-from-genesis-3/",
         "How the promise made to the serpent in this chapter is read as the "
         "first announcement of the gospel."),
    ],
    ("genesis", 18): [
        ("GotQuestions.org", GQ + "three-men-Genesis-18.html",
         "Who the three visitors to Abraham were, and why one of them speaks "
         "as the LORD."),
    ],
    ("exodus", 3): [
        ("GotQuestions.org", GQ + "I-AM-WHO-I-AM-Exodus-3-14.html",
         "What God's answer at the burning bush means, and why the name given "
         "here shapes the rest of Scripture."),
    ],
    ("exodus", 21): [
        ("GotQuestions.org", GQ + "Exodus-21-22-23-abortion.html",
         "A close reading of the disputed case law in verses 22-23 and what the "
         "Hebrew actually describes."),
    ],
    ("exodus", 25): [
        ("Crossway", CW + "why-was-the-tabernacle-so-intricate-exodus-2531/",
         "Why the instructions for the tabernacle run to seven chapters of "
         "detail rather than a summary."),
    ],
    ("leviticus", 11): [
        ("Crossway", CW + "why-were-there-such-strict-dietary-laws-in-the-old-testament-leviticus-11/",
         "What the clean and unclean food laws were for, and why they read so "
         "strangely now."),
    ],
    ("numbers", 31): [
        ("GotQuestions.org", GQ + "Numbers-31-17-Midianites.html",
         "One of the hardest commands in the Old Testament, taken seriously "
         "rather than explained away."),
    ],
    ("deuteronomy", 6): [
        ("GotQuestions.org", GQ + "Jesus-God-one-Deuteronomy-6-4.html",
         "The Shema in verse 4, and how the New Testament reads it alongside "
         "the deity of Christ."),
        ("BibleProject", BP + "what-is-the-shema/",
         "The prayer at the centre of this chapter, and what it asks of the "
         "whole person."),
    ],
    ("deuteronomy", 22): [
        ("GotQuestions.org", GQ + "Deuteronomy-22-28-29-marry-rapist.html",
         "What verses 28-29 actually legislate, and why the common reading of "
         "them misses the Hebrew."),
    ],
    ("deuteronomy", 24): [
        ("GotQuestions.org", GQ + "Deuteronomy-24-divorce.html",
         "The divorce provision Jesus is asked about in the Gospels, read in "
         "its own setting first."),
    ],
    ("judges", 1): [
        ("Crossway", CW + "how-judges-prophesied-a-true-and-better-deliverer/",
         "How the cycle of judges and deliverers across this book points past "
         "itself."),
    ],
    ("psalms", 8): [
        ("BibleProject", BP + "ruling-the-world-through-weakness-in-psalm-8/",
         "Why this psalm sets human smallness and human authority side by "
         "side, and what the New Testament does with it."),
    ],
    ("psalms", 14): [
        ("GotQuestions.org", GQ + "Psalms-14-53.html",
         "Why Psalm 14 and Psalm 53 are nearly the same psalm, and what the "
         "differences between them suggest."),
    ],
    ("psalms", 22): [
        ("GotQuestions.org", GQ + "Psalm-22-16-lion-pierced.html",
         "The textual question behind verse 16, and why translations differ "
         "between 'pierced' and 'like a lion'."),
    ],
    ("psalms", 23): [
        ("BibleProject", BP + "what-does-psalm-23-lord-my-shepherd-mean/",
         "The best known psalm read as a whole rather than a line at a time, "
         "including the valley and the table."),
        ("GotQuestions.org", GQ + "rod-staff-Psalm-23.html",
         "What a shepherd's rod and staff were actually for, and why they are "
         "described as a comfort."),
    ],
    ("psalms", 45): [
        ("Crossway", CW + "taking-a-closer-look-at-psalm-45/",
         "A royal wedding psalm, and how Hebrews reads it as addressed to the "
         "Son."),
    ],
    ("psalms", 49): [
        ("GotQuestions.org", GQ + "Psalm-49-7-Jesus.html",
         "Verse 7 says no one can redeem another, which raises the question "
         "the New Testament answers."),
    ],
    ("psalms", 53): [
        ("GotQuestions.org", GQ + "Psalms-14-53.html",
         "Why Psalm 53 and Psalm 14 are nearly the same psalm, and what the "
         "differences between them suggest."),
    ],
    ("psalms", 90): [
        ("Crossway", CW + "psalm-90-reminds-us-that-our-suffering-is-temporary/",
         "The one psalm attributed to Moses, on the shortness of life and the "
         "permanence of God."),
    ],
    ("psalms", 119): [
        ("GotQuestions.org", GQ + "Psalm-119.html",
         "How the longest chapter in the Bible is built, and why its structure "
         "is part of its argument."),
    ],
    ("psalms", 148): [
        ("BibleProject", BP + "exalted-horn-of-psalm-148/",
         "What the closing image of a raised horn means, and how it ties this "
         "psalm to the rest of the Psalter."),
    ],
    ("proverbs", 8): [
        ("BibleProject", BP + "proverbs-8-how-gods-wisdom-leads-to-joy/",
         "Wisdom speaking in the first person, and why this chapter is quoted "
         "so often in discussions of Christ."),
    ],
    ("proverbs", 26): [
        ("GotQuestions.org", GQ + "Proverbs-26-4-5.html",
         "Two verses that appear to contradict each other in consecutive "
         "lines, and why they do not."),
    ],
    ("proverbs", 31): [
        ("GotQuestions.org", GQ + "Proverbs-31-virtuous-woman.html",
         "What the closing poem is and is not asking of a reader."),
    ],
    ("isaiah", 40): [
        ("BibleProject", BP + "what-does-isaiah-4031-wings-eagles-verse-mean/",
         "The promise about waiting and renewed strength, read in the context "
         "of exile rather than as a slogan."),
    ],
    ("isaiah", 41): [
        ("BibleProject", BP + "what-does-isaiah-4110-do-not-fear-i-am-you-mean/",
         "Who 'do not fear' was first spoken to, and what that does to how it "
         "is heard now."),
    ],
    ("isaiah", 45): [
        ("GotQuestions.org", GQ + "Isaiah-45-7.html",
         "Verse 7 says God creates calamity, which is one of the hardest "
         "statements about God in the book."),
    ],
    ("isaiah", 52): [
        ("BibleProject", BP + "isaiah-and-the-suffering-servant-king/",
         "The servant songs that begin here and run into chapter 53, and how "
         "they fit the shape of the whole book."),
    ],
    ("isaiah", 53): [
        ("GotQuestions.org", GQ + "suffering-servant-Isaiah-53.html",
         "Who the suffering servant is, and how Jewish and Christian readings "
         "of this chapter differ."),
        ("Crossway", CW + "how-isaiah-prophesied-that-jesus-would-submit-and-suffer/",
         "How the New Testament writers use this chapter when they describe "
         "the cross."),
    ],
    ("jeremiah", 29): [
        ("BibleProject", BP + "what-does-jeremiah-2911-mean-i-know-plans-i-have-you/",
         "Verse 11 is one of the most quoted and most misapplied in the Bible. "
         "What it promised, and to whom."),
        ("GotQuestions.org", GQ + "Jeremiah-29-11.html",
         "The same verse read against the seventy years of exile it was "
         "written into."),
    ],
    ("hosea", 11): [
        ("GotQuestions.org", GQ + "Hosea-11-1-Messianic.html",
         "Why Matthew applies a verse about Israel leaving Egypt to Jesus."),
    ],
    ("hosea", 13): [
        ("GotQuestions.org", GQ + "Hosea-13-14-God-will-deliver.html",
         "A verse of rescue set in the middle of judgment, and how Paul picks "
         "it up in 1 Corinthians 15."),
    ],
    ("joel", 1): [
        ("Crossway", CW + "joel-1-shows-us-that-it-is-not-too-late-to-seek-the-lord/",
         "What the locust plague opening this book is doing, and the call it "
         "leads to."),
    ],
    ("amos", 9): [
        ("Crossway", CW + "how-amos-prophesied-the-coming-of-jesus-and-salvation-for-the-world/",
         "How the promise closing this book is used at the Jerusalem council "
         "in Acts 15."),
    ],
    ("micah", 5): [
        ("GotQuestions.org", GQ + "Micah-5-2-Messianic.html",
         "The Bethlehem prophecy, and what the rest of the verse claims about "
         "the one who comes from there."),
    ],
    ("habakkuk", 1): [
        ("GotQuestions Blog", GQB + "Habakkuk-syndrome.html",
         "On praying the complaint this book opens with, and what happens when "
         "God answers it."),
    ],
    ("zechariah", 11): [
        ("GotQuestions.org", GQ + "Zechariah-11-12-13-Messianic.html",
         "The thirty pieces of silver, and how Matthew reads this passage."),
    ],
    ("zechariah", 12): [
        ("GotQuestions.org", GQ + "Zechariah-12-10-Messianic.html",
         "'They will look on me, the one they have pierced' -- who is speaking "
         "and who is pierced."),
    ],
    ("zechariah", 14): [
        ("GotQuestions.org", GQ + "Zechariah-14-4-second-coming.html",
         "The Mount of Olives in this chapter, and how it is read alongside "
         "Acts 1."),
    ],
    ("daniel", 9): [
        ("Crossway", CW + "how-to-plead-with-god-when-youve-blown-it-badly/",
         "Daniel's prayer of confession in this chapter as a pattern for "
         "praying after failure."),
    ],
    ("matthew", 2): [
        ("GotQuestions.org", GQ + "Matthew-2-23-Jesus-Nazarene.html",
         "Matthew quotes a prophecy about Nazareth that appears nowhere in the "
         "Old Testament. What he is doing."),
    ],
    ("matthew", 5): [
        ("BibleProject", BP + "what-is-the-sermon-on-the-mount/",
         "An overview of the sermon that begins here and runs through chapter "
         "7, and how its parts hold together."),
        ("BibleProject", BP + "what-jesus-meant-turn-other-cheek-matthew-539/",
         "What turning the other cheek asked of someone under Roman "
         "occupation."),
    ],
    ("matthew", 6): [
        ("BibleProject", BP + "jesus-gods-forgiveness-meaning-matthew-614-15/",
         "The line about forgiveness attached to the Lord's Prayer, and what "
         "it does and does not make conditional."),
        ("BibleProject", BP + "what-matthew-622-23-eye-lamp-body-means/",
         "The saying about the eye as the lamp of the body, and the Hebrew "
         "idiom behind it."),
        ("BibleProject", BP + "what-matthew-6-33-seek-first-the-kingdom-of-god-means/",
         "What seeking the kingdom first meant in a passage about food and "
         "clothing."),
    ],
    ("matthew", 7): [
        ("BibleProject", BP + "what-matthew-71-5-judge-not-lest-ye-be-judged-means/",
         "'Judge not' read with the plank and the speck rather than on its "
         "own."),
        ("BibleProject", BP + "what-narrow-gate-bible-matthew-713-14-meaning/",
         "The narrow gate and the hard road, and what the image assumed about "
         "its first hearers."),
        ("GotQuestions.org", GQ + "Matthew-7-21-23.html",
         "'I never knew you' -- one of the most sobering paragraphs in the "
         "Gospels."),
    ],
    ("matthew", 23): [
        ("GotQuestions.org", GQ + "father-Matthew-23-9.html",
         "Why Jesus says to call no one father, and how that has been read."),
    ],
    ("matthew", 27): [
        ("GotQuestions.org", GQ + "Matthew-27-9-Jeremiah-Zechariah.html",
         "Matthew attributes a quotation to Jeremiah that reads like "
         "Zechariah. The explanations, weighed."),
    ],
    ("mark", 8): [
        ("Crossway", CW + "what-does-it-mean-to-pick-up-your-cross-and-follow-jesus-mark-8/",
         "What taking up a cross meant before it was a figure of speech."),
    ],
    ("mark", 16): [
        ("GotQuestions.org", GQ + "Mark-16-9-20.html",
         "Why most Bibles mark verses 9-20 as doubtful, and what the "
         "manuscript evidence actually shows."),
    ],
    ("luke", 16): [
        ("GotQuestions.org", GQ + "Luke-16-19-31-parable.html",
         "Whether the rich man and Lazarus is a parable or an account, and "
         "what turns on the answer."),
        ("GotQuestions.org", GQ + "worldly-wealth-Luke-16-9.html",
         "The most puzzling commendation in the Gospels, and what the shrewd "
         "manager is being praised for."),
    ],
    ("john", 1): [
        ("BibleProject", BP + "john-1/",
         "How this prologue reaches back past Genesis 1, and why the Word is "
         "the term John chooses."),
    ],
    ("john", 3): [
        ("GotQuestions.org", GQ + "John-3-16.html",
         "The most quoted verse in the Bible, read in the conversation with "
         "Nicodemus that surrounds it."),
        ("GotQuestions.org", GQ + "John-3-13.html",
         "What Jesus claims about himself in verse 13, and why it is easy to "
         "read past."),
        ("GotQuestions.org", GQ + "baptism-John-3-5.html",
         "Whether being born of water in verse 5 refers to baptism."),
    ],
    ("john", 7): [
        ("GotQuestions.org", GQ + "John-7-53-8-11.html",
         "The account of the woman caught in adultery spans 7:53-8:11 and is "
         "absent from the earliest manuscripts. What that means for reading "
         "it."),
    ],
    ("john", 8): [
        ("GotQuestions.org", GQ + "John-7-53-8-11.html",
         "The account of the woman caught in adultery is absent from the "
         "earliest manuscripts. What that means for reading it."),
    ],
    ("john", 11): [
        ("Crossway", CW + "why-would-jesus-weep-right-before-raising-lazarus-john-11/",
         "Why Jesus wept at a tomb he was about to open."),
    ],
    ("john", 20): [
        ("GotQuestions.org", GQ + "John-20-23.html",
         "'If you forgive anyone's sins' -- what authority is being given and "
         "to whom."),
    ],
    ("acts", 2): [
        ("GotQuestions.org", GQ + "baptism-Acts-2-38.html",
         "Whether Peter's call to be baptised for the forgiveness of sins "
         "makes baptism a condition of salvation."),
    ],
    ("acts", 8): [
        ("GotQuestions.org", GQ + "Acts-8-receive-Holy-Spirit.html",
         "Why the Samaritan believers here receive the Spirit separately from "
         "their believing."),
    ],
    ("acts", 9): [
        ("GotQuestions.org", GQ + "Acts-9-7-22-9.html",
         "The three accounts of Paul's conversion differ in detail. The "
         "differences, set out plainly."),
    ],
    ("acts", 15): [
        ("Crossway", CW + "how-amos-prophesied-the-coming-of-jesus-and-salvation-for-the-world/",
         "How James uses Amos 9 at the council in this chapter to settle the "
         "Gentile question."),
    ],
    ("acts", 19): [
        ("GotQuestions.org", GQ + "receive-Spirit-Acts-19.html",
         "The disciples at Ephesus who had not heard of the Holy Spirit, and "
         "what their case does and does not establish."),
    ],
    ("acts", 22): [
        ("GotQuestions.org", GQ + "baptism-Acts-22-16.html",
         "'Be baptised and wash your sins away' -- what Paul is recounting "
         "here."),
    ],
    ("romans", 1): [
        ("Crossway", CW + "setting-the-stage-for-the-book-of-romans/",
         "Who Paul was writing to and why, before the argument begins."),
    ],
    ("romans", 2): [
        ("GotQuestions.org", GQ + "Romans-2-7-works-salvation.html",
         "A verse that appears to promise eternal life for doing good, read "
         "alongside the rest of the letter."),
    ],
    ("romans", 7): [
        ("GotQuestions.org", GQ + "Romans-7-14-25.html",
         "Whether Paul is describing his life before Christ or after it, and "
         "why the answer matters pastorally."),
    ],
    ("romans", 14): [
        ("Crossway", CW + "taking-a-closer-look-at-romans-14-1-4/",
         "How Paul handles disagreement between Christians over things "
         "Scripture does not settle."),
    ],
    ("1corinthians", 14): [
        ("GotQuestions.org", GQ + "1-Corinthians-14-34-35.html",
         "The instruction about women keeping silent, and the readings that "
         "have been offered of it."),
    ],
    ("galatians", 3): [
        ("GotQuestions.org", GQ + "neither-Jew-nor-Greek-Galatians-3-28.html",
         "What 'neither Jew nor Greek, neither slave nor free' claims, and "
         "what it is often made to claim."),
        ("GotQuestions.org", GQ + "baptism-Galatians-3-27.html",
         "Being baptised into Christ in this chapter, and whether the water is "
         "in view."),
    ],
    ("ephesians", 1): [
        ("Crossway", CW + "what-is-distinct-about-the-theology-of-ephesians/",
         "What this letter is preoccupied with that the others are not."),
    ],
    ("ephesians", 2): [
        ("GotQuestions.org", GQ + "Ephesians-2-8-9.html",
         "Grace, faith and works in two verses, and how they fit together."),
    ],
    ("ephesians", 4): [
        ("GotQuestions.org", GQ + "tenderhearted-Ephesians-4-32.html",
         "What the word behind 'tenderhearted' meant, and what it asks."),
    ],
    ("ephesians", 6): [
        ("GotQuestions.org", GQ + "full-armor-of-God.html",
         "The armour described in this chapter, piece by piece."),
    ],
    ("philippians", 4): [
        ("GotQuestions.org", GQ + "Philippians-4-6.html",
         "'Do not be anxious about anything' as an instruction rather than a "
         "reassurance."),
    ],
    ("colossians", 3): [
        ("Crossway", CW + "taking-a-closer-look-at-colossians-31-4/",
         "What being raised with Christ means for what a reader does on an "
         "ordinary morning."),
    ],
    ("hebrews", 6): [
        ("GotQuestions.org", GQ + "Hebrews-6.html",
         "One of the most argued passages in the New Testament, on whether "
         "someone can fall away."),
    ],
    ("hebrews", 10): [
        ("GotQuestions.org", GQ + "Hebrews-10-26.html",
         "The warning about deliberate sin after receiving the truth."),
    ],
    ("hebrews", 12): [
        ("GotQuestions.org", GQ + "Hebrews-12-2.html",
         "Fixing your eyes on Jesus, and the race image the chapter builds it "
         "on."),
    ],
    ("james", 1): [
        ("Crossway", CW + "10-things-you-should-know-about-the-book-of-james/",
         "Ten short observations that hold this letter together as one "
         "argument rather than a collection of sayings."),
    ],
    ("james", 2): [
        ("BibleProject", BP + "what-does-faith-without-works-dead-mean-james-214-26/",
         "The passage most often set against Paul, read on its own terms "
         "first."),
    ],
    ("2peter", 3): [
        ("GotQuestions.org", GQ + "2-Peter-3-8-thousand-years-day.html",
         "'A day is like a thousand years' -- what the comparison is for."),
    ],
    ("2thessalonians", 3): [
        ("GotQuestions.org", GQ + "2-Thessalonians-3-10-no-work-eat.html",
         "'If anyone is not willing to work, let him not eat' in its setting."),
    ],
    ("2chronicles", 7): [
        ("GotQuestions.org", GQ + "2-Chronicles-7-14.html",
         "A verse applied to nations constantly. Who it was spoken to, and "
         "what follows from that."),
    ],
    ("revelation", 21): [
        ("GotQuestions.org", GQ + "God-will-wipe-away-every-tear-Revelation-21-4.html",
         "The promise about tears, death and mourning, and what it says has "
         "passed away."),
    ],
    ("revelation", 22): [
        ("GotQuestions.org", GQ + "Revelation-22-18-19.html",
         "The warning against adding to or taking from the words of this "
         "book, and its scope."),
    ],
}


# ---------------------------------------------------------------------------
# Curated: whole-book picks, shown on every chapter of that book
# ---------------------------------------------------------------------------

# book slug -> [(source label, url, description)]
#
# These appear on every chapter page of the book, after any chapter-specific
# entry. The description says plainly that it covers the whole book, so a
# reader on Genesis 37 knows why a Genesis-wide article is there.
BOOK_ARTICLES = {
    "genesis": [
        ("BibleProject", BP + "how-do-we-make-sense-of-the-book-of-genesis/",
         "On the whole book: how its opening chapters work as literature and "
         "how they set up everything that follows."),
    ],
    "exodus": [
        ("BibleProject", BP + "the-larger-story-of-exodus/",
         "On the whole book: the shape of the rescue from Egypt and where the "
         "story is going."),
    ],
    "leviticus": [
        ("BibleProject", BP + "why-leviticus-is-worth-your-time/",
         "On the whole book: a case for reading the book most reading plans "
         "stall in."),
    ],
    "numbers": [
        ("BibleProject", BP + "what-does-the-book-numbers-teach-us/",
         "On the whole book: what the census lists and wilderness years are "
         "doing in Scripture."),
    ],
    "job": [
        ("BibleProject", BP + "gods-gives-job-tour-wise-world/",
         "On the whole book: the speech from the whirlwind, and why it answers "
         "Job the way it does."),
    ],
    "isaiah": [
        ("BibleProject", BP + "isaiah-messianic-king/",
         "On the whole book: the promised king who runs through Isaiah from "
         "beginning to end."),
    ],
    "romans": [
        ("Crossway", CW + "why-romans-is-the-greatest-letter-ever-written/",
         "On the whole letter: why Romans has carried the weight it has in "
         "church history."),
    ],
}


# ---------------------------------------------------------------------------
# Curated: topical and life pages
# ---------------------------------------------------------------------------

# page filename -> [(source label, url, description)]
#
# These pages have no tabs, so the same entries render as a section block at the
# end of the page instead. See add_articles.py.
TOPIC_ARTICLES = {
    # --- life pages -------------------------------------------------------
    "addiction.html": [
        ("GotQuestions.org", GQ + "Bible-verses-about-addiction.html",
         "What Scripture says about addiction, gathered in one place."),
        ("GotQuestions.org", GQ + "Bible-alcohol.html",
         "A careful walk through what the Bible does and does not say about "
         "drinking."),
        ("GotQuestions Blog", GQB + "sin-alcohol.html",
         "A pastor's own answer to whether drinking is sin, written "
         "conversationally."),
    ],
    "anger.html": [
        ("GotQuestions.org", GQ + "Bible-anger.html",
         "The difference Scripture draws between anger and sin, and where the "
         "line falls."),
        ("GotQuestions.org", GQ + "Bible-verses-about-anger.html",
         "Passages on anger, patience and self-control, collected."),
    ],
    "anxiety-and-fear.html": [
        ("GotQuestions.org", GQ + "Bible-anxiety.html",
         "What the Bible says to someone who is anxious, without minimising "
         "it."),
        ("GotQuestions.org", GQ + "Bible-verses-about-fear.html",
         "Passages on fear and courage, collected."),
        ("GotQuestions.org", GQ + "Bible-panic-attacks.html",
         "On panic attacks specifically, including when to seek medical help."),
    ],
    "depression-and-hopelessness.html": [
        ("GotQuestions.org", GQ + "Bible-despair.html",
         "On despair, and the biblical writers who wrote from inside it."),
        ("GotQuestions.org", GQ + "Bible-verses-about-suicide.html",
         "What Scripture says where suicide is concerned, handled carefully."),
        ("GotQuestions Blog", GQB + "Christian-depression.html",
         "Whether a Christian should be able to overcome depression by faith "
         "alone, answered honestly."),
    ],
    "doubt-and-unbelief.html": [
        ("GotQuestions.org", GQ + "Bible-doubt.html",
         "Whether doubt is sin, and what the Bible does with the people in it "
         "who doubted."),
        ("GotQuestions.org", GQ + "Bible-verses-about-unbelief.html",
         "Passages on belief and unbelief, collected."),
        ("GotQuestions Blog", GQB + "understand-vs-trust.html",
         "On the difference between understanding God and trusting him."),
    ],
    "greed-and-materialism.html": [
        ("GotQuestions.org", GQ + "Bible-greed.html",
         "What greed is, as Scripture describes it, and how it hides."),
        ("GotQuestions.org", GQ + "Bible-covetousness.html",
         "Coveting as the commandment that deals with the heart rather than "
         "the hands."),
        ("GotQuestions.org", GQ + "Bible-verses-about-money.html",
         "Passages on money, wealth and generosity, collected."),
    ],
    "grief-and-loss.html": [
        ("GotQuestions.org", GQ + "Bible-grief.html",
         "What Scripture gives to someone grieving, including permission to "
         "grieve."),
        ("GotQuestions.org", GQ + "Bible-mourning.html",
         "How mourning was practised in the Bible, and what that offers now."),
        ("GotQuestions Blog", GQB + "failed-adoption.html",
         "One family's account of a loss most people never hear about."),
    ],
    "identity-and-self-worth.html": [
        ("GotQuestions.org", GQ + "identity-in-Christ.html",
         "What it means to have an identity in Christ rather than in what you "
         "do."),
        ("GotQuestions.org", GQ + "self-worth.html",
         "Where Scripture locates human worth, and where it does not."),
        ("GotQuestions.org", GQ + "image-of-God.html",
         "The image of God, which is the ground everything else here stands "
         "on."),
    ],
    "loneliness.html": [
        ("GotQuestions.org", GQ + "Bible-verses-about-loneliness.html",
         "Passages for someone who is alone, collected."),
        ("GotQuestions.org", GQ + "Bible-solitude.html",
         "The difference between loneliness and solitude, and why Jesus sought "
         "the second."),
    ],
    "lust-and-sexual-sin.html": [
        ("GotQuestions.org", GQ + "Bible-verses-about-lust.html",
         "Passages on lust and purity, collected."),
        ("GotQuestions.org", GQ + "Bible-adultery.html",
         "What Scripture says about adultery, including Jesus' widening of the "
         "term."),
        ("GotQuestions Blog", GQB + "pornography-sin.html",
         "A direct pastoral answer on pornography."),
    ],
    "marriage-and-family.html": [
        ("GotQuestions.org", GQ + "Bible-verses-about-marriage.html",
         "Passages on marriage, collected."),
        ("GotQuestions.org", GQ + "Bible-parenting.html",
         "What the Bible actually gives parents, and what it leaves to "
         "wisdom."),
        ("GotQuestions.org", GQ + "Bible-verses-about-divorce.html",
         "Passages on divorce, collected, with the hard cases named."),
    ],
    "pride.html": [
        ("GotQuestions.org", GQ + "Bible-verses-about-pride.html",
         "Passages on pride, collected."),
        ("GotQuestions.org", GQ + "Bible-humility.html",
         "Humility as Scripture defines it, which is not self-contempt."),
        ("GotQuestions Blog", GQB + "pride-sin.html",
         "On pride as the sin underneath the other ones."),
    ],
    "suffering.html": [
        ("GotQuestions.org", GQ + "Bible-suffering.html",
         "Why God allows suffering, taken as a real question rather than a "
         "rhetorical one."),
        ("GotQuestions.org", GQ + "Bible-verses-about-trials.html",
         "Passages on trials and endurance, collected."),
        ("BibleProject", BP + "how-does-the-bible-explain-suffering/",
         "How the whole Bible handles suffering, from Job to the cross."),
        ("GotQuestions Blog", GQB + "crash-turn.html",
         "On whether God uses injury and illness to get our attention."),
    ],
    "temptation.html": [
        ("GotQuestions.org", GQ + "Bible-temptation.html",
         "What temptation is, how it works, and what Scripture says to do with "
         "it."),
        ("BibleProject", BP + "sin-iniquity-and-transgression-in-the-bible/",
         "Three words the Bible uses for sin, and why the distinctions "
         "matter."),
    ],
    "unforgiveness-and-bitterness.html": [
        ("GotQuestions.org", GQ + "Bible-forgiveness.html",
         "What forgiveness is, and what it does not require."),
        ("GotQuestions.org", GQ + "Bible-bitterness.html",
         "How bitterness takes hold, and what Scripture says undoes it."),
        ("GotQuestions.org", GQ + "Bible-grudges.html",
         "On holding a grudge, and the cost of it."),
    ],

    # --- topical pages ----------------------------------------------------
    "armor-of-god.html": [
        ("GotQuestions.org", GQ + "full-armor-of-God.html",
         "The armour of Ephesians 6, piece by piece."),
        ("GotQuestions.org", GQ + "spiritual-warfare.html",
         "What spiritual warfare is in Scripture, and what it is not."),
    ],
    "beatitudes.html": [
        ("GotQuestions.org", GQ + "beatitudes.html",
         "The Beatitudes as a set, and what 'blessed' translates."),
        ("BibleProject", BP + "what-is-the-sermon-on-the-mount/",
         "The sermon the Beatitudes open, and how its parts hold together."),
        ("BibleProject", BP + "what-does-it-mean-hunger-and-thirst-righteousness/",
         "One Beatitude at length: what righteousness meant to hunger for."),
    ],
    "covenants.html": [
        ("BibleProject", BP + "covenants-the-backbone-bible/",
         "How the covenants connect into one storyline across both "
         "Testaments."),
        ("GotQuestions.org", GQ + "Bible-covenants.html",
         "Each covenant listed with its parties, promises and conditions."),
        ("GotQuestions.org", GQ + "new-covenant.html",
         "The new covenant, and what it does with the earlier ones."),
    ],
    "fruits-of-the-spirit.html": [
        ("BibleProject", BP + "fruits-spirit-and-their-meanings-bible/",
         "The nine fruits, with what each word meant in Greek."),
        ("GotQuestions.org", GQ + "fruit-of-the-Holy-Spirit.html",
         "Why Paul writes fruit singular rather than fruits plural, and what "
         "follows from it."),
    ],
    "i-am-statements.html": [
        ("GotQuestions.org", GQ + "Good-Shepherd.html",
         "'I am the good shepherd' against its Old Testament background."),
        ("GotQuestions.org", GQ + "bread-of-life.html",
         "'I am the bread of life' and the crowd that had just been fed."),
        ("GotQuestions.org", GQ + "I-AM-WHO-I-AM-Exodus-3-14.html",
         "The name at the burning bush that every 'I am' saying reaches back "
         "to."),
    ],
    "kings-of-israel.html": [
        ("GotQuestions.org", GQ + "kings-Israel-Judah.html",
         "The kings of both kingdoms in order, with reigns and assessments."),
        ("GotQuestions.org", GQ + "Israel-Northern-Southern-kingdoms.html",
         "How and why the kingdom split, which is what makes two king lists "
         "necessary."),
        ("BibleProject", BP + "david-whats-big-deal/",
         "Why David occupies so much of the Old Testament."),
        ("BibleProject", BP + "solomon-love-hate/",
         "Solomon read as the Bible itself reads him, admiringly and "
         "critically at once."),
    ],
    "men-of-the-bible.html": [
        ("GotQuestions.org", GQ + "life-Abraham.html",
         "Abraham's life, gathered from across Genesis."),
        ("GotQuestions.org", GQ + "life-Moses.html",
         "Moses' life, from the basket to Mount Nebo."),
        ("BibleProject", BP + "abraham-melchizedek-jesus/",
         "The strangest encounter in Abraham's story, and where Hebrews takes "
         "it."),
    ],
    "miracles-of-jesus.html": [
        ("GotQuestions.org", GQ + "miracles-of-Jesus.html",
         "The miracles listed by Gospel, with where each is recorded."),
        ("BibleProject", BP + "teaching-and-signs-in-the-bible/",
         "Why John calls the miracles signs, and what they are signs of."),
    ],
    "names-of-god.html": [
        ("GotQuestions.org", GQ + "names-of-God.html",
         "The names and titles of God, with the Hebrew behind each."),
        ("BibleProject", BP + "god-name-many-actually/",
         "Whether God has one name or many, and what the question is really "
         "asking."),
        ("BibleProject", BP + "what-is-the-shema/",
         "The confession that God is one, and what it asks of a reader."),
    ],
    "parables-of-jesus.html": [
        ("GotQuestions.org", GQ + "Jesus-parables.html",
         "The parables listed with their references and their point."),
        ("BibleProject", BP + "are-the-parables-of-jesus-confusing-on-purpose/",
         "Why Jesus taught in a form that some of his hearers did not "
         "understand."),
    ],
    "prayers-in-the-bible.html": [
        ("GotQuestions.org", GQ + "Lords-Prayer.html",
         "The Lord's Prayer line by line."),
        ("GotQuestions.org", GQ + "Bible-verses-about-prayer.html",
         "Passages on prayer, collected."),
    ],
    "promises-of-god.html": [
        ("GotQuestions.org", GQ + "promises-of-God.html",
         "What the promises of God are, and how to tell which ones are "
         "addressed to you."),
        ("BibleProject", BP + "if-god-remembers-does-he-also-forget/",
         "What biblical language about God remembering and forgetting is "
         "doing."),
    ],
    "prophecy-and-fulfillment.html": [
        ("GotQuestions.org", GQ + "messianic-prophecies.html",
         "The messianic prophecies with their fulfilments, side by side."),
        ("GotQuestions.org", GQ + "Bible-prophecy.html",
         "What biblical prophecy is, which is broader than prediction."),
        ("BibleProject", BP + "how-does-the-bibles-story-lead-to-jesus/",
         "How the Old Testament story arrives where it does, read as one "
         "narrative."),
    ],
    "spiritual-disciplines.html": [
        ("GotQuestions.org", GQ + "spiritual-disciplines.html",
         "The disciplines named, with what each is for."),
        ("GotQuestions.org", GQ + "Bible-meditation.html",
         "Biblical meditation, and how it differs from other things by that "
         "name."),
        ("BibleProject", BP + "what-happens-when-we-read-bible-together/",
         "On reading Scripture in company rather than alone."),
    ],
    "ten-commandments.html": [
        ("GotQuestions.org", GQ + "Ten-Commandments.html",
         "The ten, listed, with the numbering differences between traditions "
         "explained."),
        ("BibleProject", BP + "keeping-the-sabbath-is-it-still-relevant-to-christians-today/",
         "The fourth commandment specifically, and whether it still binds."),
        ("BibleProject", BP + "how-does-jesus-fulfill-law/",
         "What Jesus meant by fulfilling the law rather than abolishing it."),
    ],
    "the-12-apostles.html": [
        ("GotQuestions.org", GQ + "twelve-apostles-disciples-12.html",
         "The twelve named, with what is known about each."),
        ("GotQuestions.org", GQ + "apostles-die.html",
         "How the apostles died, separating the recorded from the "
         "traditional."),
        ("GotQuestions.org", GQ + "difference-disciple-apostle.html",
         "The difference between a disciple and an apostle."),
    ],
    "the-gospel.html": [
        ("GotQuestions.org", GQ + "what-is-the-gospel.html",
         "The gospel stated plainly, in the terms the New Testament uses."),
        ("BibleProject", BP + "what-are-the-gospels/",
         "What kind of writing the four Gospels are, and why there are four."),
        ("BibleProject", BP + "why-did-jesus-have-to-die-a-question-worth-unpacking/",
         "Why the cross was necessary, treated as a question rather than a "
         "formula."),
    ],
    "the-trinity.html": [
        ("GotQuestions.org", GQ + "Trinity-Bible.html",
         "The doctrine set out, with the passages it rests on."),
        ("GotQuestions.org", GQ + "Jesus-God-one-Deuteronomy-6-4.html",
         "How the confession that God is one sits alongside the deity of "
         "Christ."),
    ],
    "women-of-the-bible.html": [
        ("GotQuestions.org", GQ + "women-in-the-Bible.html",
         "The women of Scripture, with where each appears."),
        ("BibleProject", BP + "7-powerful-women-bible-who-help-rescue-gods-people/",
         "Seven women whose actions turn the story, several of them easy to "
         "read past."),
        ("BibleProject", BP + "what-hagar-and-ishmaels-story-reveals-about-gods-purposes/",
         "Hagar, who is met by God in the wilderness and names him."),
    ],
}


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def link_label(source):
    """The text the reader sees for a source's link."""
    return SOURCES[source][0]


def render_item(source, url, note):
    """The inner content of one entry, without the <li> wrapper."""
    return (f"<strong>{source}:</strong> "
            f"{LINK.format(url=url, label=link_label(source))} {note}")


def render_li(source, url, note):
    """One list item for a chapter page's tab pane, matching the Commentary
    tab's shape exactly. .tab-content in site/style.css supplies the indent and
    the gold star bullet, so nothing is needed here."""
    return f"<li>{render_item(source, url, note)}</li>"


# Styling for a list item on a topical or life page, which has no .tab-content
# ancestor to inherit from.
#
# style.css opens with `* { margin: 0; padding: 0; box-sizing: border-box; }`,
# which zeroes a ul's default padding-left. It does not reset list-style, so a
# plain <ul> there keeps its disc marker with no room to sit in, and because
# markers are drawn outside the content box the discs hang left of the text --
# visibly flush against the card's left edge on mobile, where .section-block
# padding drops from 32px to 16px. Chapter pages avoid this because
# `.tab-content ul { padding-left: 20px; list-style: none; }` restores the room
# and swaps the disc for the gold star.
#
# These declarations reproduce that rule's box model exactly rather than merely
# approximating it: 20px of padding on the ul, no list marker, the star as the
# first inline content of each item followed by a space, and the same
# 0.92rem / 1.7 / --text-secondary body with 10px between items.
#
# Inline content, not an absolutely positioned marker. Absolute positioning would
# give a hanging indent where wrapped lines clear the star, which looks tidier but
# is NOT what the chapter pages do -- `content: "✦ "` on a ::before is inline, so
# there the star sits at the 20px mark and wrapped lines return to 20px, under it.
# Matching the tab meant copying that, not improving on it.
#
# Each repo resolves --accent-gold-light to its own gold, #c49a2a upstream and
# #c9a96e on New River, so no colour is hardcoded.
#
# The star is markup rather than a ::before rule on purpose. site/style.css is on
# the sync's preserve list, so a rule there has to be added by hand in both
# repos, and both WORKFLOW.md and CLAUDE_HANDOFF.md flag that as the mistake that
# has already been made twice. Keeping it inline keeps it in one regenerable
# script.
TOPIC_UL_STYLE = "padding-left:20px;list-style:none;margin:0;"
TOPIC_LI_STYLE = ("font-size:0.92rem;line-height:1.7;"
                  "color:var(--text-secondary);margin-bottom:10px;")
TOPIC_MARKER_STYLE = "color:var(--accent-gold-light);"

# U+2726 BLACK FOUR POINTED STAR, the same glyph style.css uses. Written as a
# numeric reference rather than the literal character so it cannot be turned into
# U+FFFD by a non-UTF-8 tool, which has happened to this repo before -- 173 video
# captions needed repairing for exactly that reason. The verification pass greps
# for U+FFFD and expects zero.
STAR = "&#10022;"


def render_li_standalone(source, url, note):
    """One list item for a topical or life page, carrying its own star because no
    stylesheet rule covers it. The trailing space after the star matches the
    `content: "✦ "` it is standing in for. See TOPIC_UL_STYLE above."""
    return (f'<li style="{TOPIC_LI_STYLE}">'
            f'<span aria-hidden="true" style="{TOPIC_MARKER_STYLE}">{STAR}</span> '
            f"{render_item(source, url, note)}</li>")


def gq_book_entry(book_slug):
    """The derived GotQuestions.org overview link for a book. This is what
    guarantees every chapter page has at least one article."""
    page = GQ_BOOK_PAGE[book_slug]
    title = BOOK_TITLE[book_slug]
    subject = title if book_slug in NO_BOOK_OF else f"the book of {title}"
    return ("GotQuestions.org", f"{GQ}{page}.html",
            f"On the whole book: an overview of {subject} -- who wrote it, "
            f"when, why, and how it fits the rest of Scripture.")


def chapter_entries(book_slug, chapter):
    """Ordered entries for one chapter page: anything specific to this chapter
    first, then whole-book material, then the derived overview last.

    Chapter-first ordering matters. A reader on Psalm 23 should meet the article
    about Psalm 23 before the one about the Psalms in general.
    """
    out = []
    out += list(CHAPTER_ARTICLES.get((book_slug, chapter), []))
    out += list(BOOK_ARTICLES.get(book_slug, []))
    out.append(gq_book_entry(book_slug))
    return [e for e in out if e[1] not in DROP_ARTICLE_URLS]


def page_entries(filename):
    """Entries for a topical or life page. Empty list if the page has none."""
    out = list(TOPIC_ARTICLES.get(filename, []))
    return [e for e in out if e[1] not in DROP_ARTICLE_URLS]


def all_urls():
    """Every URL this module would put on the site, for link checking."""
    seen = set()
    for entries in list(CHAPTER_ARTICLES.values()) + \
            list(BOOK_ARTICLES.values()) + list(TOPIC_ARTICLES.values()):
        for _, url, _ in entries:
            seen.add(url)
    for slug in GQ_BOOK_PAGE:
        seen.add(gq_book_entry(slug)[1])
    return sorted(seen - set(DROP_ARTICLE_URLS))


def source_of(url):
    """Which allowed source a URL belongs to, or None if it is not one of ours."""
    for label, (_, home, _why) in SOURCES.items():
        host = re.match(r"https?://[^/]+", home).group(0)
        if url.startswith(host):
            return label
    return None


# ---------------------------------------------------------------------------
# Weekly polling
# ---------------------------------------------------------------------------
#
# What check_new_articles.py fetches. Kept here rather than in that script so
# the allow list and the feed list cannot disagree about which sites are in
# scope.
#
# Two shapes, because the sources offer different things:
#
#   rss       Crossway. It has no article sitemap at all -- its sitemap.xml is
#             11,588 URLs of books, authors, bibles and tracts with zero
#             articles -- and ?page=N on the archive is ignored. What it does
#             have is a feed per topic tag, each carrying the latest 15. Fanning
#             out across the tags below is the only way to see more than 15
#             articles, and it is also the freshest view of the four sources.
#             /search/ is Disallow in their robots.txt and is not touched.
#
#   sitemap   The other three. BibleProject has no feed but a clean 76-article
#             sitemap; both GotQuestions properties publish a sitemap with
#             lastmod on every URL.

# Crossway topic feeds worth watching. Chosen to match what this site actually
# has pages for: chapter study, the topical pages, and the life pages. The 20-odd
# tags left out are company-news, book-news, digital-news, bible-news, giveaway,
# interview, video, product-series, ministry-projects and similar -- they carry
# announcements and sales rather than teaching.
CROSSWAY_TAGS = [
    # scripture and study
    "the-bible", "old-testament", "new-testament", "biblical-theology",
    "bible-study", "bible-translation", "theology", "the-gospel",
    "how-jesus-fulfilled-prophecy", "breaking-down-jesuss-most-famous-sermons",
    # God and doctrine
    "god-the-father", "god-the-son", "god-the-holy-spirit", "the-trinity",
    "grace", "salvation", "justification", "sanctification", "sin", "humanity",
    "angels-and-demons", "spiritual-warfare", "the-end-times",
    "heaven-and-hell", "death",
    # the topical pages
    "prayer", "discipleship", "apologetics", "baptism", "the-lords-supper",
    "corporate-worship", "the-church", "women", "men",
    # the life pages
    "fear-and-anxiety", "trials-and-suffering", "marriage", "family",
    "parenting", "motherhood", "fatherhood", "money", "sex", "singleness",
    "dating", "hope-for-idolaters", "putting-on-the-new-self",
    "the-christian-life", "work-and-vocation", "health",
    "infertility-miscarriage",
]

# Slug shapes on gotquestions.org that could plausibly become an Articles entry.
#
# The English sitemap is 10,887 URLs. Tracking all of them would mean a 550 KB
# state file committed every week, and most of those pages answer questions this
# site has no page for. These five patterns select the 920 URLs that map onto
# something here -- the per-book overviews, the two large curated series, the
# pages naming a book and chapter, and the per-person life summaries. Anything
# outside them is out of scope for the weekly poll, not forbidden: a page found
# by hand can still be added to the tables above.
_GQ_BOOKS = (
    "Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1-Samuel|"
    "2-Samuel|1-Kings|2-Kings|1-Chronicles|2-Chronicles|Ezra|Nehemiah|Esther|"
    "Job|Psalms|Psalm|Proverbs|Ecclesiastes|Isaiah|Jeremiah|Lamentations|"
    "Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|"
    "Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|"
    "1-Corinthians|2-Corinthians|Galatians|Ephesians|Philippians|Colossians|"
    "1-Thessalonians|2-Thessalonians|1-Timothy|2-Timothy|Titus|Philemon|"
    "Hebrews|James|1-Peter|2-Peter|1-John|2-John|3-John|Jude|Revelation"
)
GQ_KEEP = [
    r"/(?:Book|Gospel)-of-[A-Za-z0-9-]+\.html$",
    r"/Bible-[A-Za-z][A-Za-z0-9-]*\.html$",
    r"/life-[A-Z][A-Za-z0-9-]*\.html$",
    r"/[A-Za-z0-9-]*(?<![A-Za-z0-9])(?:%s)-\d{1,3}(?![0-9])[A-Za-z0-9-]*\.html$"
    % _GQ_BOOKS,
]

# Navigation and housekeeping pages on the blog, which sits in the same flat
# directory as its posts and so cannot be told apart by URL shape.
GQB_SKIP = {
    "about", "cultural", "insights", "life", "musings", "new", "top20",
    "haters", "testimony", "s-michael-houdmann", "recommended-resources",
    "follow-up", "got-donations", "got-debate", "got-hate-mail",
    "favorite-question", "funny-questions", "stupid-questions",
    "question-wording", "millstone-award", "copy-it-right",
}

FEEDS = {
    "Crossway": {
        "kind": "rss",
        "urls": [CW + "rss/"] + [CW + f"tag/{t}/rss/" for t in CROSSWAY_TAGS],
        "keep": [r"^https://www\.crossway\.org/articles/[a-z0-9][^/]*/$"],
    },
    "BibleProject": {
        "kind": "sitemap",
        "urls": ["https://bibleproject.com/en/sitemap.xml"],
        "keep": [r"^https://bibleproject\.com/articles/[a-z0-9][^/]*/$"],
    },
    "GotQuestions.org": {
        "kind": "sitemap",
        "urls": [GQ + "sitemap.xml"],
        "keep": GQ_KEEP,
    },
    "GotQuestions Blog": {
        "kind": "sitemap",
        "urls": [GQB + "sitemap.xml"],
        "keep": [r"^https://www\.gotquestions\.blog/[A-Za-z0-9][A-Za-z0-9-]*\.html$"],
    },
}


def in_scope(source, url):
    """True if a URL found in a feed is the kind of thing this source is watched
    for. Keeps navigation pages, tag indexes and non-article sections out of the
    weekly report."""
    spec = FEEDS.get(source)
    if not spec:
        return False
    if not any(re.search(p, url) for p in spec["keep"]):
        return False
    if source == "GotQuestions Blog":
        slug = url.rstrip("/").rsplit("/", 1)[-1][: -len(".html")]
        if slug in GQB_SKIP:
            return False
    return True


def already_on_site(url):
    """True if this URL is already linked from a page, or has been ruled out.
    Either way it should never be suggested again."""
    return url in set(all_urls()) or url in DROP_ARTICLE_URLS


# ---------------------------------------------------------------------------
# Auto-approved additions
# ---------------------------------------------------------------------------
#
# Entries a person approved by number from a weekly-audit issue, via
# apply_approved.py -- see suggest_placements.py for how the suggestion that
# produced each one was drafted, and WORKFLOW.md for the approve-by-number
# flow. Kept as their own dicts rather than inserted into CHAPTER_ARTICLES /
# TOPIC_ARTICLES directly, so an approval never has to locate and edit inside
# those hand-curated literals. Move an entry up into its permanent home above
# whenever convenient; nothing breaks either way, since the merge below runs
# before anything reads CHAPTER_ARTICLES or TOPIC_ARTICLES.
#
# apply_approved.py finds this exact block by the fence comments and rewrites
# it whole -- never hand-edit between the fences, or the next approval could
# clobber the hand edit. Move an entry above the fences to hand-curate it.
# AUTO_FENCE_OPEN
AUTO_CHAPTER_ARTICLES = {
}

AUTO_TOPIC_ARTICLES = {
}

for _key, _entries in AUTO_CHAPTER_ARTICLES.items():
    CHAPTER_ARTICLES[_key] = list(CHAPTER_ARTICLES.get(_key, [])) + list(_entries)
for _key, _entries in AUTO_TOPIC_ARTICLES.items():
    TOPIC_ARTICLES[_key] = list(TOPIC_ARTICLES.get(_key, [])) + list(_entries)
# AUTO_FENCE_CLOSE
