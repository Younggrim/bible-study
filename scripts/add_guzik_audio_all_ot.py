#!/usr/bin/env python3
"""Add David Guzik Enduring Word audio teaching links to all OT VIDEO RESOURCES sections."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament"

# Map book folder names to their enduringword.com media page URLs
book_media_urls = {
    "01 - Genesis": "https://enduringword.com/sermons/genesis/genesis/",
    "02 - Exodus": "https://enduringword.com/sermons/exodus/exodus/",
    "03 - Leviticus": "https://enduringword.com/media/leviticus/",
    "04 - Numbers": "https://enduringword.com/sermons/numbers/numbers/",
    "05 - Deuteronomy": "https://enduringword.com/sermons/deuteronomy/deuteronomy/",
    "06 - Joshua": "https://enduringword.com/media/joshua/",
    "07 - Judges": "https://enduringword.com/media/judges/",
    "08 - Ruth": "https://enduringword.com/media/ruth/",
    "09 - 1 Samuel": "https://enduringword.com/media/1-samuel/",
    "10 - 2 Samuel": "https://enduringword.com/media/2-samuel/",
    "11 - 1 Kings": "https://enduringword.com/media/1-kings/",
    "12 - 2 Kings": "https://enduringword.com/media/2-kings/",
    "13 - 1 Chronicles": "https://enduringword.com/sermons/chronicles-letters/1-2-chronicles/",
    "14 - 2 Chronicles": "https://enduringword.com/sermons/chronicles-letters/1-2-chronicles/",
    "15 - Ezra": "https://enduringword.com/media/ezra/",
    "16 - Nehemiah": "https://enduringword.com/sermons/nehemiah/nehemiah/",
    "17 - Esther": "https://enduringword.com/sermons/esther/esther/",
    "18 - Job": "https://enduringword.com/media/job/",
    "19 - Psalms": "https://enduringword.com/media/psalms/",
    "20 - Proverbs": "https://enduringword.com/media/proverbs/",
    "21 - Ecclesiastes": "https://enduringword.com/media/ecclesiastes/",
    "22 - Song of Solomon": "https://enduringword.com/media/song-of-solomon/",
    "23 - Isaiah": "https://enduringword.com/media/isaiah/",
    "24 - Jeremiah": "https://enduringword.com/media/jeremiah/",
    "25 - Lamentations": "https://enduringword.com/sermons/jeremiah-lamentations/lamentations/",
    "26 - Ezekiel": "https://enduringword.com/sermons/ezekiel/ezekiel/",
    "27 - Daniel": "https://enduringword.com/media/daniel/",
    "28 - Hosea": "https://enduringword.com/media/minor-prophets/",
    "29 - Joel": "https://enduringword.com/media/minor-prophets/",
    "30 - Amos": "https://enduringword.com/media/minor-prophets/",
    "31 - Obadiah": "https://enduringword.com/media/minor-prophets/",
    "32 - Jonah": "https://enduringword.com/media/minor-prophets/",
    "33 - Micah": "https://enduringword.com/media/minor-prophets/",
    "34 - Nahum": "https://enduringword.com/media/minor-prophets/",
    "35 - Habakkuk": "https://enduringword.com/media/minor-prophets/",
    "36 - Zephaniah": "https://enduringword.com/media/minor-prophets/",
    "37 - Haggai": "https://enduringword.com/media/minor-prophets/",
    "38 - Zechariah": "https://enduringword.com/media/minor-prophets/",
    "39 - Malachi": "https://enduringword.com/media/minor-prophets/",
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

        # Skip if already has Guzik teaching link
        if "Enduring Word Teaching Series" in content:
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

print("Added Guzik teaching links to " + str(count) + " OT files")
