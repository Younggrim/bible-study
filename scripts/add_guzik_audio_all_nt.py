#!/usr/bin/env python3
"""Add David Guzik Enduring Word audio teaching links to all NT VIDEO RESOURCES sections."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament"

# Map book folder names to their enduringword.com media page URLs
book_media_urls = {
    "01 - Matthew": "https://enduringword.com/sermons/matthew/matthew/",
    "02 - Mark": "https://enduringword.com/media/mark/",
    "03 - Luke": "https://enduringword.com/media/luke/",
    "04 - John": "https://enduringword.com/media/john/",
    "05 - Acts": "https://enduringword.com/media/acts/",
    "06 - Romans": "https://enduringword.com/media/romans/",
    "07 - 1 Corinthians": "https://enduringword.com/media/1-corinthians/",
    "08 - 2 Corinthians": "https://enduringword.com/media/2-corinthians/",
    "09 - Galatians": "https://enduringword.com/media/galatians/",
    "10 - Ephesians": "https://enduringword.com/sermons/ephesians/ephesians",
    "11 - Philippians": "https://enduringword.com/sermons/philippians/philippians/",
    "12 - Colossians": "https://enduringword.com/sermons/colossians/colossians/",
    "13 - 1 Thessalonians": "https://enduringword.com/sermons/1-thessalonians/1-thessalonians/",
    "14 - 2 Thessalonians": "https://enduringword.com/sermons/2-thessalonians/2-thessalonians/",
    "15 - 1 Timothy": "https://enduringword.com/sermons/1-timothy/1-timothy/",
    "16 - 2 Timothy": "https://enduringword.com/sermons/2-timothy/2-timothy/",
    "17 - Titus": "https://enduringword.com/sermons/titus/titus/",
    "18 - Philemon": "https://enduringword.com/sermons/philiemon/philemon/",
    "19 - Hebrews": "https://enduringword.com/sermons/hebrews/hebrews/",
    "20 - James": "https://enduringword.com/media/james",
    "21 - 1 Peter": "https://enduringword.com/media/1-2-peter/",
    "22 - 2 Peter": "https://enduringword.com/media/1-2-peter/",
    "23 - 1 John": "https://enduringword.com/sermons/123john/1-john/",
    "24 - 2 John": "https://enduringword.com/sermons/123john/1-john/",
    "25 - 3 John": "https://enduringword.com/sermons/123john/1-john/",
    "26 - Jude": "https://enduringword.com/sermons/Jude/Jude/",
    "27 - Revelation": "https://enduringword.com/sermons/revelation/revelation/",
}

count = 0
for bookdir in sorted(os.listdir(base)):
    bookpath = os.path.join(base, bookdir)
    if not os.path.isdir(bookpath) or bookdir.startswith('.'):
        continue
    if bookdir not in book_media_urls:
        continue

    media_url = book_media_urls[bookdir]
    book_short = bookdir.split(" - ")[1]

    for chapdir in sorted(os.listdir(bookpath)):
        if not chapdir.startswith("Chapter"):
            continue
        filepath = os.path.join(bookpath, chapdir, chapdir + " - Study Notes.txt")
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'r') as f:
            content = f.read()

        # Skip if already has a Guzik audio/teaching link (not just the video one for John)
        if "Enduring Word Audio" in content or "Enduring Word Teaching Series" in content:
            continue
        # Skip John since it already has the video series
        if bookdir == "04 - John" and "Enduring Word Video Series" in content:
            continue

        # Build the audio link block
        audio_block = "\nDavid Guzik — Enduring Word Teaching Series (" + book_short + "):\n"
        audio_block += "  " + media_url + "\n"
        audio_block += "  Verse-by-verse audio/video teaching through " + book_short + ".\n"

        # Insert before PODCAST RESOURCES
        if 'PODCAST RESOURCES' in content:
            content = content.replace('PODCAST RESOURCES', audio_block + "\nPODCAST RESOURCES")
            with open(filepath, 'w') as f:
                f.write(content)
            count += 1

print("Added Guzik teaching links to " + str(count) + " files")
