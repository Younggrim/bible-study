#!/usr/bin/env python3
"""
Transform TRANSLATION NOTES and ADDITIONAL TRANSLATION NOTES sections
into a unified TRANSLATION COMPARISON section for Deuteronomy Study Notes.

Strategy:
- Parse each entry from TRANSLATION NOTES (KJV/ESV focused)
- Parse each entry from ADDITIONAL TRANSLATION NOTES (ASV/NET/WEB focused)
- Match entries by verse number (sequential matching for same-verse duplicates)
- For each KJV/ESV entry, extract: Hebrew word, KJV quote, ESV quote, analysis
- For each additional entry, extract: ASV quote, NET quote, WEB quote, analysis
- Merge into unified format with all 5 translations + combined analysis
"""

import re
import os

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/05 - Deuteronomy"


def find_section(content, header):
    """Find a section's header start position and its body text."""
    marker = header + "\n" + "-" * 36
    start = content.find(marker)
    if start == -1:
        return -1, -1, ""
    
    body_start = start + len(marker) + 1  # +1 for newline after dashes
    
    # Find end: next section header (UPPERCASE TITLE\n----)
    rest = content[body_start:]
    next_match = re.search(r'\n([A-Z][A-Z &/(),]+)\n-{4,}', rest)
    if next_match:
        body_end = body_start + next_match.start()
    else:
        body_end = len(content)
    
    body = content[body_start:body_end]
    return start, body_end, body


def parse_tn_entries(body):
    """Parse TRANSLATION NOTES body into list of (verse, raw_text) tuples."""
    entries = []
    lines = body.split('\n')
    current_verse = None
    current_lines = []
    
    for line in lines:
        m = re.match(r'^(v\.\d+)\s+—\s+(.*)', line)
        if m:
            if current_verse:
                entries.append((current_verse, '\n'.join(current_lines)))
            current_verse = m.group(1)
            current_lines = [m.group(2)]
        elif current_verse is not None:
            current_lines.append(line)
    
    if current_verse:
        entries.append((current_verse, '\n'.join(current_lines)))
    
    return entries


def parse_atn_entries(body):
    """Parse ADDITIONAL TRANSLATION NOTES body into list of (verse, raw_text) tuples."""
    entries = []
    lines = body.split('\n')
    current_verse = None
    current_lines = []
    
    for line in lines:
        m = re.match(r'^-\s+(v\.\d+)\s+—\s+(.*)', line)
        if m:
            if current_verse:
                entries.append((current_verse, '\n'.join(current_lines)))
            current_verse = m.group(1)
            current_lines = [m.group(2)]
        elif current_verse is not None:
            current_lines.append(line)
    
    if current_verse:
        entries.append((current_verse, '\n'.join(current_lines)))
    
    return entries


def flatten(text):
    """Flatten multiline text into single line, normalized spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def extract_from_tn(raw):
    """Extract KJV, ESV, Hebrew word, and analysis from a TN entry."""
    flat = flatten(raw)
    
    kjv = ""
    esv = ""
    hebrew = ""
    
    # KJV/ESV pattern: KJV: "..." / ESV: "..."
    kjv_m = re.search(r'KJV:\s*"([^"]+)"', flat)
    esv_m = re.search(r'ESV:\s*"([^"]+)"', flat)
    if kjv_m:
        kjv = kjv_m.group(1)
    if esv_m:
        esv = esv_m.group(1)
    
    # Hebrew word: Hebrew "..."
    heb_m = re.search(r'Hebrew\s+"([^"]+)"', flat)
    if not heb_m:
        heb_m = re.search(r'Hebrew\s+\u201c([^\u201d]+)\u201d', flat)
    if heb_m:
        hebrew = heb_m.group(1)
    
    # Analysis: everything after "— Hebrew ..." or after the KJV/ESV intro
    # The format is typically: KJV: "x" / ESV: "y" — Hebrew "z." Analysis...
    # Find everything after the initial "KJV.../ESV..." pattern
    # Split on the " — " that separates the quote comparison from the analysis
    analysis = flat
    
    # The full entry text IS the analysis - it contains the Hebrew and explanation
    # Let's just use the whole flat text as the analysis
    
    return kjv, esv, hebrew, analysis


def extract_from_atn(raw):
    """Extract NET, ASV, WEB quotes and analysis from an ATN entry."""
    flat = flatten(raw)
    
    net = ""
    asv = ""
    web = ""
    kjv = ""
    
    net_m = re.search(r'NET:\s*"([^"]+)"', flat)
    asv_m = re.search(r'ASV:\s*"([^"]+)"', flat)
    web_m = re.search(r'WEB:\s*"([^"]+)"', flat)
    kjv_m = re.search(r'KJV:\s*"([^"]+)"', flat)
    
    if net_m:
        net = net_m.group(1)
    if asv_m:
        asv = asv_m.group(1)
    if web_m:
        web = web_m.group(1)
    if kjv_m:
        kjv = kjv_m.group(1)
    
    # Analysis: text after the last " — " separator
    parts = flat.split(' — ')
    if len(parts) > 1:
        analysis = parts[-1].strip()
    else:
        analysis = flat
    
    return net, asv, web, kjv, analysis


def build_header(hebrew, analysis):
    """Build the header line: v.X  — Hebrew "word" — meaning."""
    # Get a short meaning from the analysis
    # The analysis often starts with: Hebrew "word." followed by explanation
    # Or it starts with the explanation directly
    meaning = get_meaning(analysis)
    
    if hebrew:
        return f'Hebrew "{hebrew}" — {meaning}'
    else:
        return meaning


def get_meaning(analysis):
    """Extract a concise meaning/description for the header line."""
    if not analysis:
        return "translation comparison."
    
    text = analysis.strip()
    
    # If it starts with a Hebrew transliteration in quotes, skip past it
    if text.startswith('"'):
        end_q = text.find('"', 1)
        if end_q > 0 and end_q < 80:
            text = text[end_q+1:].strip('. ')
    
    # Also skip patterns like: Hebrew "word." or  "word" = meaning
    # Get the first complete sentence that's a good description
    sentences = re.split(r'(?<=[.!])\s+', text)
    if sentences:
        first = sentences[0].strip()
        if len(first) <= 120:
            return first
        # Too long, try to cut at a natural point
        cut = first.find(';')
        if cut > 30 and cut < 100:
            return first[:cut+1]
        cut = first.find(',', 50)
        if cut > 0 and cut < 100:
            return first[:cut] + "..."
        return first[:100] + "..."
    
    return text[:100] + ("..." if len(text) > 100 else "")


def format_entry(verse, kjv, esv, asv, net, web, tn_analysis, atn_analysis, hebrew):
    """Format a single unified entry."""
    # Build header
    header_content = build_header(hebrew, tn_analysis if tn_analysis else atn_analysis)
    
    lines = [f'{verse}  — {header_content}']
    
    if kjv:
        lines.append(f'       KJV: "{kjv}"')
    if esv:
        lines.append(f'       ESV: "{esv}"')
    if asv:
        lines.append(f'       ASV: "{asv}"')
    if net:
        lines.append(f'       NET: "{net}"')
    if web:
        lines.append(f'       WEB: "{web}"')
    
    # Combined analysis
    combined = ""
    if tn_analysis:
        combined = tn_analysis
    if atn_analysis:
        if combined:
            # Only append if it adds new information
            # Check if the additional analysis is substantially different
            if atn_analysis not in combined and len(atn_analysis) > 20:
                combined = combined.rstrip('. ') + '. ' + atn_analysis
        else:
            combined = atn_analysis
    
    if combined:
        lines.append(f'       Analysis: {combined}')
    
    return '\n'.join(lines)


def verse_num(v):
    """Extract numeric verse number for sorting."""
    m = re.search(r'(\d+)', v)
    return int(m.group(1)) if m else 999


def process_file(filepath):
    """Process a single study notes file."""
    fname = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))
    print(f"\nProcessing: {dirname}/{fname}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find both sections
    tn_start, tn_end, tn_body = find_section(content, "TRANSLATION NOTES")
    atn_start, atn_end, atn_body = find_section(content, "ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)")
    
    if tn_start == -1:
        print("  ERROR: No TRANSLATION NOTES section found!")
        return False
    
    if atn_start == -1:
        print("  WARNING: No ADDITIONAL TRANSLATION NOTES section found.")
        print("  Converting TRANSLATION NOTES only...")
        # Just rename the section header
        tn_entries = parse_tn_entries(tn_body)
        unified = []
        for verse, raw in tn_entries:
            kjv, esv, hebrew, analysis = extract_from_tn(raw)
            entry = format_entry(verse, kjv, esv, "", "", "", analysis, "", hebrew)
            unified.append(entry)
        
        # Replace just the TRANSLATION NOTES header
        new_header = "TRANSLATION COMPARISON\n" + "-" * 36
        old_header = "TRANSLATION NOTES\n" + "-" * 36
        new_section = new_header + "\n" + '\n\n'.join(unified) + '\n'
        
        # Replace old section
        old_section = content[tn_start:tn_end]
        new_content = content[:tn_start] + new_section + content[tn_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Done (TN only): {len(unified)} entries.")
        return True
    
    # Both sections exist
    # Check if there's a GLOSSARY between them
    gloss_start, gloss_end, gloss_body = find_section(content, "GLOSSARY")
    glossary_between = (gloss_start > tn_start and gloss_start < atn_start)
    
    # Parse entries
    tn_entries = parse_tn_entries(tn_body if not glossary_between else content[tn_start + len("TRANSLATION NOTES\n" + "-"*36) + 1:gloss_start])
    atn_entries = parse_atn_entries(atn_body)
    
    print(f"  Found {len(tn_entries)} KJV/ESV entries, {len(atn_entries)} additional entries")
    
    # Match entries: pair up by verse number sequentially
    # Build a dict: verse -> list of additional entries
    atn_dict = {}
    for verse, raw in atn_entries:
        atn_dict.setdefault(verse, []).append(raw)
    
    # Track used additional entries
    atn_used = {v: 0 for v in atn_dict}
    
    unified = []
    
    # Process each TN entry
    for verse, tn_raw in tn_entries:
        kjv, esv, hebrew, tn_analysis = extract_from_tn(tn_raw)
        
        # Try to match with an additional entry for the same verse
        net = ""
        asv = ""
        web = ""
        atn_analysis = ""
        atn_kjv = ""
        
        if verse in atn_dict and atn_used[verse] < len(atn_dict[verse]):
            atn_raw = atn_dict[verse][atn_used[verse]]
            atn_used[verse] += 1
            net, asv, web, atn_kjv, atn_analysis = extract_from_atn(atn_raw)
        
        entry = format_entry(verse, kjv, esv, asv, net, web, tn_analysis, atn_analysis, hebrew)
        unified.append(entry)
    
    # Add any unmatched additional entries
    for verse, entries_list in atn_dict.items():
        start_idx = atn_used.get(verse, 0)
        for i in range(start_idx, len(entries_list)):
            atn_raw = entries_list[i]
            net, asv, web, atn_kjv, atn_analysis = extract_from_atn(atn_raw)
            entry = format_entry(verse, atn_kjv, "", asv, net, web, "", atn_analysis, "")
            unified.append(entry)
    
    # Sort by verse number
    unified.sort(key=lambda e: verse_num(e))
    
    # Build new section text
    new_section = "TRANSLATION COMPARISON\n" + "-" * 36 + "\n"
    new_section += '\n\n'.join(unified) + '\n'
    
    # Determine replacement boundaries
    # We need to replace from TRANSLATION NOTES start through ADDITIONAL end
    # But keep GLOSSARY if it's between them
    if glossary_between:
        # Keep glossary: replace TN...GLOSSARY boundary, then skip glossary, then replace ATN
        # Actually simpler: replace from TN_start to ATN_end, and insert new section + glossary
        glossary_full = content[gloss_start:gloss_end]
        replacement = new_section + '\n' + glossary_full + '\n'
        new_content = content[:tn_start] + replacement + content[atn_end:]
    else:
        # No glossary between them - just replace both sections
        # The replacement area is from tn_start to atn_end
        new_content = content[:tn_start] + new_section + content[atn_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  SUCCESS: Written unified section with {len(unified)} entries.")
    return True


def main():
    chapters = list(range(1, 18))
    success = 0
    failed = 0
    
    for ch in chapters:
        filepath = os.path.join(BASE_PATH, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
        if os.path.exists(filepath):
            if process_file(filepath):
                success += 1
            else:
                failed += 1
        else:
            print(f"  File not found: Chapter {ch}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Complete: {success} succeeded, {failed} failed out of {len(chapters)} files.")


if __name__ == "__main__":
    main()
