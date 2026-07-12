#!/usr/bin/env python3
"""
Transform TRANSLATION NOTES + ADDITIONAL TRANSLATION NOTES into unified TRANSLATION COMPARISON.

Output format per entry:
v.X  — Hebrew "word" — short meaning description.
       KJV: "quote"
       ESV: "quote"
       ASV: "quote"
       NET: "quote"
       WEB: "quote"
       Analysis: full explanation of differences and theological significance.
"""

import re
import os

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/05 - Deuteronomy"


def find_section_bounds(content, header_text):
    """Find where a section starts (header line) and ends (next section header)."""
    pattern = header_text + "\n" + "-" * 36
    idx = content.find(pattern)
    if idx == -1:
        return -1, -1
    body_start = idx + len(pattern) + 1
    rest = content[body_start:]
    m = re.search(r'\n([A-Z][A-Z &/(),\u2019\']+)\n-{4,}', rest)
    if m:
        section_end = body_start + m.start()
    else:
        section_end = len(content)
    return idx, section_end


def split_entries(body, prefix_pattern):
    """
    Split section body into entries. 
    prefix_pattern: regex that matches the start of each entry and captures the verse.
    Returns list of (verse_str, raw_body_text).
    """
    entries = []
    parts = re.split(r'^' + prefix_pattern, body, flags=re.MULTILINE)
    # parts[0] is preamble (usually empty), then alternating verse/content
    i = 1
    while i < len(parts) - 1:
        verse = parts[i].strip()
        text = parts[i + 1]
        # Clean up: remove trailing empty lines
        text = text.rstrip('\n').strip()
        entries.append((verse, text))
        i += 2
    return entries


def flatten(text):
    """Normalize whitespace to single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def extract_hebrew_word(flat_text):
    """Extract the Hebrew word/phrase from text. Returns (word, text_after_hebrew)."""
    # Pattern: Hebrew "word(s)." or Hebrew "word(s)"
    m = re.search(r'Hebrew\s+"([^"]+)"', flat_text)
    if m:
        return m.group(1), flat_text[m.end():].strip('. ')
    return "", flat_text


def make_meaning(hebrew, flat_text):
    """
    Create a short meaning/definition for the header line.
    The meaning should be a concise phrase, NOT the full analysis.
    """
    # Strategy: if we have Hebrew word, get the definition that follows it
    # Typical patterns in the TN analysis:
    # 1. Hebrew "word." Meaning/explanation sentences.
    # 2. Hebrew "word" = meaning. Longer explanation.
    # 3. Hebrew "word" — literally "translation". Explanation.
    
    if not flat_text:
        return "translation comparison."
    
    text = flat_text
    
    # Skip past the Hebrew transliteration if it's at the start
    # e.g., starts with: "b'ever ha-Yarden." The phrase means...
    if text.startswith('"'):
        end_q = text.find('"', 1)
        if end_q > 0 and end_q < 80:
            text = text[end_q+1:].strip('. —')
    
    # Now try to get a SHORT meaning (one phrase or short sentence)
    # Look for common definition patterns:
    
    # Pattern: "word" = meaning; 
    eq_match = re.match(r'"[^"]+"?\s*=\s*([^;.]+)', text)
    if eq_match:
        return eq_match.group(1).strip() + '.'
    
    # Pattern: means/means to...
    means_match = re.search(r'(?:means?|literally)\s+"?([^".]+)"?', text[:150])
    if means_match:
        meaning = means_match.group(1).strip()
        if len(meaning) < 80:
            return meaning + '.'
    
    # Pattern: "The phrase means..." 
    phrase_match = re.search(r'The (?:phrase|word|term|verb|name)\s+(?:means?|is|refers to)\s+(.+?)(?:\.|;|—)', text[:200])
    if phrase_match:
        meaning = phrase_match.group(1).strip('" ')
        if len(meaning) < 80:
            return meaning + '.'
    
    # Fall back: first short sentence or clause
    # Try to get text before first period that's less than 80 chars
    period_match = re.search(r'^(.{10,80}?)\.\s', text)
    if period_match:
        return period_match.group(1).strip() + '.'
    
    # Last resort: first 70 chars with ellipsis
    if len(text) > 70:
        # Try to break at a word boundary
        cut = text.rfind(' ', 40, 70)
        if cut > 0:
            return text[:cut] + '...'
        return text[:70] + '...'
    
    return text.strip().rstrip('.') + '.'


def extract_quotes(flat_text, *labels):
    """Extract quoted text for given translation labels (KJV, ESV, etc.)."""
    results = {}
    for label in labels:
        m = re.search(label + r':\s*"([^"]+)"', flat_text)
        results[label] = m.group(1) if m else ""
    return results


def process_file(filepath):
    """Process a single study notes file."""
    fname = os.path.basename(filepath)
    dname = os.path.basename(os.path.dirname(filepath))
    print(f"\nProcessing: {dname}/{fname}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find sections
    tn_start, tn_end = find_section_bounds(content, "TRANSLATION NOTES")
    atn_start, atn_end = find_section_bounds(content, "ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)")
    
    if tn_start == -1:
        print("  ERROR: No TRANSLATION NOTES found!")
        return False
    
    # Get TN body (handle GLOSSARY between sections)
    tn_header_end = tn_start + len("TRANSLATION NOTES\n" + "-" * 36 + "\n")
    
    gloss_start, gloss_end = find_section_bounds(content, "GLOSSARY")
    glossary_between = (gloss_start > tn_start and 
                       (atn_start == -1 or gloss_start < atn_start))
    
    if glossary_between:
        tn_body = content[tn_header_end:gloss_start]
    else:
        tn_body = content[tn_header_end:tn_end]
    
    # Parse TN entries: each starts with "v.XX  — "
    tn_entries = split_entries(tn_body, r'(v\.\d+)\s+—\s+')
    
    # Parse ATN entries if they exist
    atn_entries = []
    if atn_start != -1:
        atn_header_end = atn_start + len("ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)\n" + "-" * 36 + "\n")
        atn_body = content[atn_header_end:atn_end]
        atn_entries = split_entries(atn_body, r'-\s+(v\.\d+)\s+—\s+')
    
    print(f"  TN: {len(tn_entries)} entries, ATN: {len(atn_entries)} entries")
    
    # Now build unified entries
    # Each TN entry becomes a unified entry with KJV+ESV
    # Each ATN entry either supplements an existing entry (same verse) or becomes standalone
    # Strategy: keep all entries separate (even for same verse), just merge in additional quotes
    
    # Build list of all entries as unified objects
    unified = []
    
    # Group ATN entries by verse for matching
    atn_queue = {}
    for verse, raw in atn_entries:
        atn_queue.setdefault(verse, []).append(raw)
    atn_idx = {v: 0 for v in atn_queue}
    
    for verse, tn_raw in tn_entries:
        flat = flatten(tn_raw)
        
        # Extract KJV and ESV quotes
        quotes = extract_quotes(flat, 'KJV', 'ESV')
        kjv = quotes['KJV']
        esv = quotes['ESV']
        
        # Extract Hebrew word
        hebrew, after_heb = extract_hebrew_word(flat)
        
        # Get analysis text: everything after "KJV:... / ESV:..." and " — "
        # The analysis is the explanatory content
        analysis = flat
        # Remove the KJV/ESV intro to get pure analysis
        esv_end = flat.find(esv) + len(esv) + 1 if esv else 0
        if esv_end > 1:
            analysis = flat[esv_end:].strip()
            if analysis.startswith('—'):
                analysis = analysis[1:].strip()
            elif analysis.startswith('— '):
                analysis = analysis[2:].strip()
        
        # Try to get ASV/NET/WEB from matching ATN entry
        asv = net = web = ""
        atn_analysis = ""
        
        if verse in atn_queue and atn_idx[verse] < len(atn_queue[verse]):
            atn_raw = atn_queue[verse][atn_idx[verse]]
            atn_idx[verse] += 1
            atn_flat = flatten(atn_raw)
            
            atn_quotes = extract_quotes(atn_flat, 'NET', 'ASV', 'WEB', 'KJV')
            net = atn_quotes['NET']
            asv = atn_quotes['ASV']
            web = atn_quotes['WEB']
            
            # Get ATN analysis (text after all quotes and " — ")
            last_quote_end = 0
            for label in ['NET', 'ASV', 'WEB', 'KJV']:
                m = re.search(label + r':\s*"[^"]+"', atn_flat)
                if m and m.end() > last_quote_end:
                    last_quote_end = m.end()
            if last_quote_end > 0:
                atn_analysis = atn_flat[last_quote_end:].strip()
                if atn_analysis.startswith('/'):
                    # There might be another quote after /
                    pass
                if atn_analysis.startswith('—') or atn_analysis.startswith('— '):
                    atn_analysis = re.sub(r'^—\s*', '', atn_analysis)
        
        # Build meaning for header
        meaning = make_meaning(hebrew, analysis)
        
        # Build combined analysis
        combined_analysis = analysis
        if atn_analysis and len(atn_analysis) > 10:
            # Add ATN analysis if substantively different
            if atn_analysis[:25] not in combined_analysis:
                combined_analysis = combined_analysis.rstrip('. ') + '. ' + atn_analysis.strip()
        
        # Format entry
        if hebrew:
            header = f'{verse}  — Hebrew "{hebrew}" — {meaning}'
        else:
            header = f'{verse}  — {meaning}'
        
        lines = [header]
        if kjv: lines.append(f'       KJV: "{kjv}"')
        if esv: lines.append(f'       ESV: "{esv}"')
        if asv: lines.append(f'       ASV: "{asv}"')
        if net: lines.append(f'       NET: "{net}"')
        if web: lines.append(f'       WEB: "{web}"')
        lines.append(f'       Analysis: {combined_analysis}')
        
        unified.append('\n'.join(lines))
    
    # Add remaining unmatched ATN entries as standalone
    for verse, raw_list in atn_queue.items():
        start = atn_idx.get(verse, 0)
        for i in range(start, len(raw_list)):
            atn_flat = flatten(raw_list[i])
            
            quotes = extract_quotes(atn_flat, 'NET', 'ASV', 'WEB', 'KJV')
            net = quotes['NET']
            asv = quotes['ASV']
            web = quotes['WEB']
            kjv = quotes['KJV']
            
            # Get the analysis
            last_quote_end = 0
            for label in ['NET', 'ASV', 'WEB', 'KJV']:
                m = re.search(label + r':\s*"[^"]+"', atn_flat)
                if m and m.end() > last_quote_end:
                    last_quote_end = m.end()
            
            analysis = ""
            if last_quote_end > 0:
                analysis = atn_flat[last_quote_end:].strip()
                analysis = re.sub(r'^[/—]\s*', '', analysis).strip()
                # If it still has " — " separator, take text after
                if ' — ' in analysis:
                    analysis = analysis.split(' — ', 1)[1].strip()
            else:
                analysis = atn_flat
            
            meaning = make_meaning("", analysis)
            
            header = f'{verse}  — {meaning}'
            lines = [header]
            if kjv: lines.append(f'       KJV: "{kjv}"')
            if asv: lines.append(f'       ASV: "{asv}"')
            if net: lines.append(f'       NET: "{net}"')
            if web: lines.append(f'       WEB: "{web}"')
            lines.append(f'       Analysis: {analysis}')
            
            unified.append('\n'.join(lines))
    
    # Sort by verse number
    def verse_key(entry):
        m = re.match(r'v\.(\d+)', entry)
        return int(m.group(1)) if m else 999
    unified.sort(key=verse_key)
    
    # Build new section
    new_section = "TRANSLATION COMPARISON\n" + "-" * 36 + "\n"
    new_section += '\n\n'.join(unified) + '\n'
    
    # Replace in content
    if atn_start != -1:
        if glossary_between:
            glossary_text = content[gloss_start:gloss_end]
            replacement = new_section + '\n' + glossary_text + '\n'
            new_content = content[:tn_start] + replacement + content[atn_end:]
        else:
            new_content = content[:tn_start] + new_section + content[atn_end:]
    else:
        # No ATN section - just replace TN
        if glossary_between:
            new_content = content[:tn_start] + new_section + '\n' + content[gloss_start:]
        else:
            new_content = content[:tn_start] + new_section + content[tn_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  SUCCESS: {len(unified)} unified entries written.")
    return True


def main():
    success = failed = 0
    for ch in range(1, 18):
        fp = os.path.join(BASE_PATH, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
        if os.path.exists(fp):
            if process_file(fp):
                success += 1
            else:
                failed += 1
        else:
            print(f"  NOT FOUND: Chapter {ch}")
            failed += 1
    print(f"\n{'='*50}")
    print(f"Done: {success}/{success+failed} succeeded.")


if __name__ == "__main__":
    main()
