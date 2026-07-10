#!/usr/bin/env python3
"""Add specific Guzik video links to James and 1 Timothy chapters."""
import os

def add_video_links(filepath, video_block):
    with open(filepath, 'r') as f:
        content = f.read()
    if "Video Series" in content and "enduringword.com/media/" in content:
        return False
    if 'PODCAST RESOURCES' in content:
        content = content.replace('PODCAST RESOURCES', video_block + "\nPODCAST RESOURCES")
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# James videos mapped to chapters
james_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/20 - James"
james_videos = {
    1: [
        ("James 1:1-8 - Hard Times and Wisdom", "https://enduringword.com/media/hard-times-and-wisdom-james-1-1-8/"),
        ("James 1:9-18 - How Temptation Works", "https://enduringword.com/media/how-temptation-works-james-1-9-18/"),
        ("James 1:19-27 - Being Doers, Not Only Hearers", "https://enduringword.com/media/being-doers-not-only-hearers-james-1-19-27/"),
    ],
    2: [
        ("James 2:1-13 - Genuine Faith Among God's People", "https://enduringword.com/media/genuine-faith-gods-people-james-2-1-13/"),
        ("James 2:14-26 - Dead Faith and Living Faith", "https://enduringword.com/media/dead-faith-living-faith-james-2-14-26/"),
    ],
    3: [
        ("James 3:1-12 - Taming the Tongue", "https://enduringword.com/media/taming-the-tongue-james-3-1-12/"),
        ("James 3:13-18 - Earthly Wisdom and Heavenly Wisdom", "https://enduringword.com/media/earthly-wisdom-heavenly-wisdom-james-3-13-18/"),
    ],
    4: [
        ("James 4:1-6 - Grace and Getting Along", "https://enduringword.com/media/grace-and-getting-along-james-4-1-6/"),
        ("James 4:7-17 - Humility and Getting Along", "https://enduringword.com/media/humility-and-getting-along-james-4-7-17/"),
    ],
    5: [
        ("James 5:1-12 - Humble, Patient, Enduring", "https://enduringword.com/media/humble-patient-enduring-james-5-1-12/"),
        ("James 5:13-20 - Confession of Sin and Answered Prayer", "https://enduringword.com/media/confession-of-sin-answered-prayer-james-5-13-20/"),
    ],
}

# 1 Timothy videos mapped to chapters
tim1_base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/15 - 1 Timothy"
tim1_videos = {
    1: [("1 Timothy 1 - Fighting for the Faith", "https://enduringword.com/media/1-timothy-1-fighting-for-the-faith/")],
    2: [
        ("1 Timothy 2:1-10 - Instructions for Public Worship", "https://enduringword.com/media/1-timothy-21-10-instructions-for-public-worship/"),
        ("1 Timothy 2:8-15 - Men and Women in the Church", "https://enduringword.com/media/1-timothy-28-15-men-and-women-in-the-church/"),
    ],
    3: [("1 Timothy 3 - Qualifications for Leaders", "https://enduringword.com/media/1-timothy-3-qualifications-for-leaders/")],
    4: [("1 Timothy 4 - God's Man of Truth and Integrity", "https://enduringword.com/media/1-timothy-4-gods-man-of-truth-and-integrity/")],
    5: [("1 Timothy 5 - How to Treat People in the Church", "https://enduringword.com/media/1-timothy-5-how-to-treat-people-in-the-church/")],
    6: [("1 Timothy 6 - Riches and Godliness", "https://enduringword.com/media/1-timothy-6-riches-and-godliness/")],
}

# Process James
for ch, vids in sorted(james_videos.items()):
    filepath = os.path.join(james_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if not os.path.isfile(filepath):
        continue
    block = "\nDavid Guzik — Enduring Word Video Series (James):\n"
    for title, url in vids:
        block += "  " + title + ":\n"
        block += "    " + url + "\n"
    if add_video_links(filepath, block):
        print("  done James " + str(ch))

# Process 1 Timothy
for ch, vids in sorted(tim1_videos.items()):
    filepath = os.path.join(tim1_base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if not os.path.isfile(filepath):
        continue
    block = "\nDavid Guzik — Enduring Word Video Series (1 Timothy):\n"
    for title, url in vids:
        block += "  " + title + ":\n"
        block += "    " + url + "\n"
    if add_video_links(filepath, block):
        print("  done 1 Timothy " + str(ch))
