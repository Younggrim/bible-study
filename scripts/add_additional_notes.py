#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB) to study notes files.
Reads a data file with format: filepath|||notes_text (multiline blocks separated by ===)
"""
import os
import sys

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

# Read entries from data file - format is blocks separated by ===
data_file = sys.argv[1]
with open(data_file, 'r') as f:
    raw = f.read()

entries = raw.strip().split('\n===\n')
for entry in entries:
    lines = entry.strip().split('\n')
    if not lines:
        continue
    filepath = lines[0].strip()
    notes_text = '\n'.join(lines[1:])
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, notes_text):
            ch = os.path.basename(os.path.dirname(filepath))
            print(f"  done {ch}")
        else:
            print(f"  skip {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"  missing: {filepath}")
