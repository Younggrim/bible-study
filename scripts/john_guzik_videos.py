#!/usr/bin/env python3
"""Add David Guzik video links to John chapter VIDEO RESOURCES sections."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/04 - John"

# Map chapters to their Guzik video entries
# Format: chapter -> list of (title, url)
playlist_base = "https://www.youtube.com/watch?v=lLl3NFD3Wqs&list=PL_QIfO0mxbX4zgQH4vuK6q1q7gu8Ok6tz"

videos = {
    1: [
        ("John 1:1-18 - God the Son Presented to Us", "https://enduringword.com/media/john-1-god-son-presented-us/"),
        ("John 1:19-51 - Revealed to John the Baptist", "https://enduringword.com/media/john-119-51-revealed-john-baptist/"),
    ],
    2: [
        ("John 2:1-12 - Revealed at Cana", "https://enduringword.com/media/john-2-revealed-cana/"),
        ("John 2:13-25 - Revealed in the Temple", "https://enduringword.com/media/john-2-revealed-temple/"),
    ],
    3: [
        ("John 3:1-21 - Revealed in Secret", "https://enduringword.com/media/john-3-revealed-secret/"),
        ("John 3:22-26 - Revealed as Greater", "https://enduringword.com/media/john-3-revealed-greater/"),
    ],
    4: [
        ("John 4:1-26 - Revealed as Living Water", "https://enduringword.com/media/john-4-revealed-living-water/"),
        ("John 4:27-42 - Revealed As Savior of the World", "https://enduringword.com/media/john-4-revealed-savior-world/"),
        ("John 4:43-54 - Revealed as Worth Believing", "https://enduringword.com/media/john-4-revealed-worth-believing/"),
    ],
    5: [
        ("John 5:1-9 - Opposed by Hopelessness", "https://enduringword.com/media/john-5-opposed-hopelessness/"),
        ("John 5:10-18 - Opposed by Religious Tradition", "https://enduringword.com/media/john-5-opposed-religious-tradition/"),
        ("John 5:19-47 - Opposed by Unbelief", "https://enduringword.com/media/john-5-opposed-unbelief/"),
    ],
    6: [
        ("John 6:1-13 - Opposed by the Impossible", "https://enduringword.com/media/john-6-opposed-impossible/"),
        ("John 6:14-21 - Opposed by the Storm", "https://enduringword.com/media/john-6-opposed-storm/"),
        ("John 6:22-46 - Opposed by Sign-Seekers", "https://enduringword.com/media/john-6-opposed-sign-seekers/"),
        ("John 6:47-71 - Opposed by Word-Twisters", "https://enduringword.com/media/john-6-opposed-word-twisters/"),
    ],
    7: [
        ("John 7:1-13 - Opposed by His Family", "https://enduringword.com/media/john-7-opposed-family/"),
        ("John 7:14-36 - Opposed at the Temple", "https://enduringword.com/media/john-7-opposed-temple/"),
        ("John 7:37-52 - Opposed by the Religious Rulers", "https://enduringword.com/media/john-7-opposed-religious-rulers/"),
    ],
    8: [
        ("John 8:1-11 - Opposed by Accusers", "https://enduringword.com/media/john-8-opposed-accusers/"),
        ("John 8:12-30 - Opposed by Darkness", "https://enduringword.com/media/john-8-opposed-darkness/"),
        ("John 8:31-59 - Opposed by the Devil", "https://enduringword.com/media/john-8-opposed-devil/"),
    ],
    9: [
        ("John 9:1-16 - Opposed by Blindness", "https://enduringword.com/media/john-9-opposed-blindness/"),
        ("John 9:17-41 - Opposed by Ignorance", "https://enduringword.com/media/john-9-opposed-ignorance/"),
    ],
    10: [
        ("John 10:1-21 - Opposed by Wolves", "https://enduringword.com/media/john-10-opposed-wolves/"),
        ("John 10:22-42 - Opposed by Stoning", "https://enduringword.com/media/john-10-opposed-stoning/"),
    ],
    11: [
        ("John 11:1-27 - Opposed by Grief", "https://enduringword.com/media/john-11-opposed-grief/"),
        ("John 11:28-57 - Opposed by Death", "https://enduringword.com/media/john-11-opposed-death/"),
    ],
    12: [
        ("John 12:1-19 - Prepared for Burial", "https://enduringword.com/media/john-12-prepared-burial/"),
        ("John 12:20-50 - Prepared for Sacrifice", "https://enduringword.com/media/john-12-prepared-sacrifice/"),
    ],
    13: [
        ("John 13:1-17 - Prepared to Serve", "https://enduringword.com/media/john-13-prepared-serve/"),
        ("John 13:18-38 - Prepared for Glory", "https://enduringword.com/media/john-13-prepared-glory/"),
    ],
    14: [
        ("John 14:1-14 - Prepared for Departure", "https://enduringword.com/media/john-14-prepared-departure/"),
        ("John 14:15-31 - Prepared for the Spirit", "https://enduringword.com/media/john-14-prepared-spirit/"),
    ],
    15: [
        ("John 15:1-11 - Prepared to Abide", "https://enduringword.com/media/john-15-prepared-abide/"),
        ("John 15:12-16:4 - Prepared for Persecution", "https://enduringword.com/media/john-15-16-prepared-persecution/"),
    ],
    16: [
        ("John 16:5-33 - Prepared for Advantage", "https://enduringword.com/media/john-16-prepared-advantage/"),
    ],
    17: [
        ("John 17:1-10 - Prepared by Prayer", "https://enduringword.com/media/john-17-prepared-prayer/"),
        ("John 17:11-19 - Prepared for Preservation", "https://enduringword.com/media/john-17-prepared-preservation/"),
        ("John 17:20-26 - Prepared to Proclaim", "https://enduringword.com/media/john-17-prepared-proclaim/"),
    ],
    18: [
        ("John 18:1-18 - Glory Under Arrest", "https://enduringword.com/media/john-18-glory-arrest/"),
        ("John 18:19-40 - Glory On Trial", "https://enduringword.com/media/john-18-glory-trial/"),
    ],
    19: [
        ("John 19:1-16 - Glory Mocked and Condemned", "https://enduringword.com/media/john-19-glory-mocked-condemned/"),
        ("John 19:17-30 - Glory Crucified", "https://enduringword.com/media/john-19-glory-crucified/"),
        ("John 19:31-42 - Glory Buried", "https://enduringword.com/media/john-19-glory-buried/"),
    ],
    20: [
        ("John 20:1-18 - Resurrection Glory", "https://enduringword.com/media/john-20-resurrection-glory/"),
        ("John 20:19-31 - Glory Believed", "https://enduringword.com/media/john-20-glory-believed/"),
    ],
    21: [
        ("John 21:1-14 - Glory at Breakfast", "https://enduringword.com/media/john-21-glory-breakfast/"),
        ("John 21:15-25 - Glory's Restoration", "https://enduringword.com/media/john-21-glorys-restoration/"),
    ],
}

for ch, vids in sorted(videos.items()):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if not os.path.isfile(filepath):
        print("  missing Chapter " + str(ch))
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Check if Guzik videos already added
    if "Enduring Word" in content and "enduringword.com/media/john" in content:
        print("  skip Chapter " + str(ch) + " (already has Guzik videos)")
        continue

    # Build the video block
    video_block = "\nDavid Guzik — Enduring Word Video Series (John):\n"
    video_block += "  YouTube Playlist: https://www.youtube.com/playlist?list=PL_QIfO0mxbX4zgQH4vuK6q1q7gu8Ok6tz\n"
    for title, url in vids:
        video_block += "  " + title + ":\n"
        video_block += "    " + url + "\n"

    # Insert before PODCAST RESOURCES
    if 'PODCAST RESOURCES' in content:
        content = content.replace('PODCAST RESOURCES', video_block + "\nPODCAST RESOURCES")
    else:
        print("  error Chapter " + str(ch) + " (no PODCAST RESOURCES section)")
        continue

    with open(filepath, 'w') as f:
        f.write(content)
    print("  done Chapter " + str(ch))
