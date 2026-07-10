#!/usr/bin/env python3
"""Add New River Church Hebrews playlist to all 13 Hebrews chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/19 - Hebrews"
playlist_url = "https://www.youtube.com/playlist?list=PLUBpLcqCn5ul0W_fQ6HRlBlioQKOYLEEp"

count = 0
for ch in range(1, 14):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if not os.path.isfile(filepath):
        print("  missing Chapter " + str(ch))
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    if "New River Church" in content:
        print("  skip Chapter " + str(ch) + " (already has it)")
        continue

    video_block = "\nNew River Church — Hebrews Teaching Series:\n"
    video_block += "  " + playlist_url + "\n"
    video_block += "  Verse-by-verse teaching through Hebrews " + str(ch) + ".\n"

    if 'PODCAST RESOURCES' in content:
        content = content.replace('PODCAST RESOURCES', video_block + "\nPODCAST RESOURCES")
        with open(filepath, 'w') as f:
            f.write(content)
        count += 1
        print("  done Chapter " + str(ch))

print("\nAdded to " + str(count) + " files")
