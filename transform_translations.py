#!/usr/bin/env python3
"""
Transform TRANSLATION NOTES + ADDITIONAL TRANSLATION NOTES into unified TRANSLATION COMPARISON.

The output format for each verse:
v.X  — Hebrew "word" — meaning.
       KJV: "quote"
       ESV: "quote"
       ASV: "quote"
       NET: "quote"
       WEB: "quote"
       Analysis: explanation of differences and theological significance.
"""

import re
import os

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/05 - Deuteronomy"


def find_section_bounds(content, header_text):
    """
    Returns (section_start, section_end) where section_start is the beginning of
    the header line, and section_end is where the next section begins.
    """
    pattern = header_text + "\n" + "-" * 36
    idx = content.find(pattern)
    if idx == -1:
        return -1, -1
    
    body_start = idx + len(pattern) + 1  # skip past the newline after dashes
    
    # Find next section: a line of ALL CAPS (with spaces/punctuation) followed by dashes
    rest = content[body_start:]
    m = re.search(r'\n([A-Z][A-Z &/(),\u2019]+)\n-{4,}', rest)
    if m:
        section_end = body_start + m.start()
    else:
        section_end = len(content)
    
    return idx, section_end


def split_tn_entries(body):
    """
    Split TRANSLATION NOTES section body into individual entries.
    Each entry starts with 'v.XX  —' at the start of a line.
    Returns list of (verse_str, full_raw_text_of_entry).
    """
    entries = []
    # Split on lines that begin with v.\d+
    parts = re.split(r'^(v\.\d+)\s+—\s+', body, flags=re.MULTILINE)
    # parts[0] is empty/preamble, then alternating: verse, content, verse, content...
    i = 1
    while i < len(parts) - 1:
        verse = parts[i]
        text = parts[i + 1].strip()
        entries.append((verse, text))
        i += 2
    return entries


def split_atn_entries(body):
    """
    Split ADDITIONAL TRANSLATION NOTES section body into individual entries.
    Each entry starts with '- v.XX —' at the start of a line.
    Returns list of (verse_str, full_raw_text_of_entry).
    """
    entries = []
    parts = re.split(r'^-\s+(v\.\d+)\s+—\s+', body, flags=re.MULTILINE)
    i = 1
    while i < len(parts) - 1:
        verse = parts[i]
        text = parts[i + 1].strip()
        entries.append((verse, text))
        i += 2
    return entries


def flatten_text(text):
    """Flatten multiline text to single line with normalized spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def extract_kjv_esv(flat_text):
    """
    From a flattened TN entry, extract:
    - KJV quote
    - ESV quote  
    - Hebrew word/phrase
    - Analysis text (the explanation)
    """
    kjv = esv = hebrew = ""
    
    # Pattern: KJV: "..." / ESV: "..." — Hebrew "...". Analysis...
    kjv_m = re.search(r'KJV:\s*"([^"]+)"', flat_text)
    esv_m = re.search(r'ESV:\s*"([^"]+)"', flat_text)
    
    if kjv_m:
        kjv = kjv_m.group(1)
    if esv_m:
        esv = esv_m.group(1)
    
    # Hebrew word - appears after " — Hebrew " 
    heb_m = re.search(r'Hebrew\s+"([^"]+)"', flat_text)
    if heb_m:
        hebrew = heb_m.group(1)
    
    # Analysis: everything after the "Hebrew 'word.'" explanation
    # The typical format is:
    # KJV: "x" / ESV: "y" — Hebrew "z." Explanation of the term...
    # So analysis starts after " — " that follows the ESV quote
    
    # Find the " — " after the ESV quote (or KJV if no ESV)
    analysis = ""
    if esv_m:
        after_esv = flat_text[esv_m.end():]
        # Strip leading " — " 
        after_esv = re.sub(r'^\s*—\s*', '', after_esv)
        analysis = after_esv.strip()
    elif kjv_m:
        after_kjv = flat_text[kjv_m.end():]
        after_kjv = re.sub(r'^\s*—\s*', '', after_kjv)
        analysis = after_kjv.strip()
    else:
        analysis = flat_text
    
    return kjv, esv, hebrew, analysis


def extract_asv_net_web(flat_text):
    """
    From a flattened ATN entry, extract:
    - NET quote
    - ASV quote
    - WEB quote
    - KJV quote (sometimes included in additional)
    - Analysis text
    """
    net = asv = web = kjv = ""
    
    net_m = re.search(r'NET:\s*"([^"]+)"', flat_text)
    asv_m = re.search(r'ASV:\s*"([^"]+)"', flat_text)
    web_m = re.search(r'WEB:\s*"([^"]+)"', flat_text)
    kjv_m = re.search(r'KJV:\s*"([^"]+)"', flat_text)
    
    if net_m:
        net = net_m.group(1)
    if asv_m:
        asv = asv_m.group(1)
    if web_m:
        web = web_m.group(1)
    if kjv_m:
        kjv = kjv_m.group(1)
    
    # Analysis: text after " — " that follows the last quote
    # Find the last translation quote end
    last_pos = 0
    for m in [net_m, asv_m, web_m, kjv_m]:
        if m and m.end() > last_pos:
            last_pos = m.end()
    
    if last_pos > 0:
        after_quotes = flat_text[last_pos:]
        # Strip leading " / " or " — " separators  
        after_quotes = re.sub(r'^\s*[/—]\s*', '', after_quotes)
        # If there's still a " — " separator, take what's after it
        if ' — ' in after_quotes:
            analysis = after_quotes.split(' — ', 1)[1].strip()
        else:
            analysis = after_quotes.strip()
    else:
        analysis = flat_text
    
    return net, asv, web, kjv, analysis


def get_meaning_line(hebrew, analysis):
    """
    Create a concise meaning description for the header line.
    Should be a short phrase describing what the Hebrew word means.
    """
    if not analysis:
        return "translation differences."
    
    # The analysis often starts with the Hebrew transliteration in quotes
    # e.g.: "b'ever ha-Yarden." The phrase means "on the other side..."
    # Skip past any leading quoted Hebrew
    text = analysis
    
    # Skip leading Hebrew transliteration if it matches the hebrew param
    if text.startswith('"'):
        end_q = text.find('"', 1)
        if end_q > 0 and end_q < 60:
            text = text[end_q+1:].strip('. ')
    
    # Get the first meaningful sentence
    # Split on periods, but be careful about abbreviations
    sentences = re.split(r'(?<=[a-z])\.\s+(?=[A-Z])', text, maxsplit=1)
    if sentences:
        first = sentences[0].strip().rstrip('.')
        if len(first) <= 100:
            return first + '.'
        # Too long - find a break
        cut = first.find(';', 30)
        if 30 < cut < 100:
            return first[:cut+1]
        cut = first.find(' — ', 30)
        if 30 < cut < 90:
            return first[:cut] + '.'
        return first[:90] + '...'
    
    return text[:90] + ('...' if len(text) > 90 else '.')


def format_unified_entry(verse, kjv, esv, asv, net, web, hebrew, tn_analysis, atn_analysis):
    """Format a single unified TRANSLATION COMPARISON entry."""
    # Build header line
    meaning = get_meaning_line(hebrew, tn_analysis if tn_analysis else atn_analysis)
    
    if hebrew:
        header = f'{verse}  — Hebrew "{hebrew}" — {meaning}'
    else:
        header = f'{verse}  — {meaning}'
    
    lines = [header]
    
    # Add translation quotes
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
    
    # Build combined analysis
    combined = ""
    if tn_analysis:
        combined = tn_analysis.rstrip('. ')
    if atn_analysis:
        if combined:
            # Add additional analysis if it's substantively different
            # Don't add if it's essentially the same content
            if len(atn_analysis) > 15 and atn_analysis[:30] not in combined:
                combined += '. ' + atn_analysis.rstrip('. ')
        else:
            combined = atn_analysis.rstrip('. ')
    
    if combined:
        combined = combined.strip() + '.'
        lines.append(f'       Analysis: {combined}')
    
    return '\n'.join(lines)


def verse_sort_key(entry_text):
    """Extract verse number for sorting."""
    m = re.match(r'v\.(\d+)', entry_text)
    return int(m.group(1)) if m else 999


def process_file(filepath):
    """Process a single study notes file."""
    fname = os.path.basename(filepath)
    dname = os.path.basename(os.path.dirname(filepath))
    print(f"\nProcessing: {dname}/{fname}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find both sections
    tn_start, tn_end = find_section_bounds(content, "TRANSLATION NOTES")
    atn_start, atn_end = find_section_bounds(content, "ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)")
    
    if tn_start == -1:
        print("  ERROR: No TRANSLATION NOTES section found!")
        return False
    
    # Get TRANSLATION NOTES body
    tn_header_len = len("TRANSLATION NOTES\n" + "-" * 36 + "\n")
    tn_body = content[tn_start + tn_header_len:tn_end]
    
    # Check for GLOSSARY between them
    gloss_start, gloss_end = find_section_bounds(content, "GLOSSARY")
    glossary_between = gloss_start > tn_start and (atn_start == -1 or gloss_start < atn_start)
    
    if glossary_between:
        # TN body ends at GLOSSARY
        tn_body = content[tn_start + tn_header_len:gloss_start]
    
    # Parse TN entries
    tn_entries = split_tn_entries(tn_body)
    
    if atn_start == -1:
        print("  No ADDITIONAL section — converting TRANSLATION NOTES only...")
        # Just convert TN entries to new format
        unified = []
        for verse, raw in tn_entries:
            flat = flatten_text(raw)
            kjv, esv, hebrew, analysis = extract_kjv_esv(flat)
            entry = format_unified_entry(verse, kjv, esv, "", "", "", hebrew, analysis, "")
            unified.append(entry)
        
        # Build new section
        new_section = "TRANSLATION COMPARISON\n" + "-" * 36 + "\n"
        new_section += '\n\n'.join(unified) + '\n'
        
        # Replace TN section only
        if glossary_between:
            new_content = content[:tn_start] + new_section + '\n' + content[gloss_start:]
        else:
            new_content = content[:tn_start] + new_section + content[tn_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Done: {len(unified)} entries.")
        return True
    
    # Both sections exist — get ATN body
    atn_header_len = len("ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)\n" + "-" * 36 + "\n")
    atn_body = content[atn_start + atn_header_len:atn_end]
    
    # Parse ATN entries
    atn_entries = split_atn_entries(atn_body)
    
    print(f"  Found {len(tn_entries)} KJV/ESV entries, {len(atn_entries)} additional entries")
    
    # Build lookup for ATN by verse (preserving order for same-verse)
    atn_by_verse = {}
    for verse, raw in atn_entries:
        atn_by_verse.setdefault(verse, []).append(raw)
    atn_consumed = {v: 0 for v in atn_by_verse}
    
    unified = []
    
    # Process each TN entry, try to match with ATN
    for verse, tn_raw in tn_entries:
        flat_tn = flatten_text(tn_raw)
        kjv, esv, hebrew, tn_analysis = extract_kjv_esv(flat_tn)
        
        # Try to find matching ATN entry
        net = asv = web = ""
        atn_analysis = ""
        
        if verse in atn_by_verse and atn_consumed[verse] < len(atn_by_verse[verse]):
            atn_raw = atn_by_verse[verse][atn_consumed[verse]]
            atn_consumed[verse] += 1
            flat_atn = flatten_text(atn_raw)
            net, asv, web, atn_kjv, atn_analysis = extract_asv_net_web(flat_atn)
        
        entry = format_unified_entry(verse, kjv, esv, asv, net, web, hebrew, tn_analysis, atn_analysis)
        unified.append(entry)
    
    # Handle remaining unmatched ATN entries
    for verse, raw_list in atn_by_verse.items():
        start_idx = atn_consumed.get(verse, 0)
        for i in range(start_idx, len(raw_list)):
            flat_atn = flatten_text(raw_list[i])
            net, asv, web, atn_kjv, atn_analysis = extract_asv_net_web(flat_atn)
            entry = format_unified_entry(verse, atn_kjv, "", asv, net, web, "", "", atn_analysis)
            unified.append(entry)
    
    # Sort by verse number
    unified.sort(key=verse_sort_key)
    
    # Build new section
    new_section = "TRANSLATION COMPARISON\n" + "-" * 36 + "\n"
    new_section += '\n\n'.join(unified) + '\n'
    
    # Determine replacement range
    # Replace from TN start through ATN end, preserving GLOSSARY if between
    if glossary_between:
        glossary_text = content[gloss_start:gloss_end]
        replacement = new_section + '\n' + glossary_text + '\n'
        new_content = content[:tn_start] + replacement + content[atn_end:]
    else:
        new_content = content[:tn_start] + new_section + content[atn_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  SUCCESS: {len(unified)} unified entries.")
    return True


def main():
    success = 0
    failed = 0
    
    for ch in range(1, 18):
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
    print(f"Complete: {success}/{success+failed} files processed successfully.")


if __name__ == "__main__":
    main()
