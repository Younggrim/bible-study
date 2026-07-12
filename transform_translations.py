#!/usr/bin/env python3
"""
Transform TRANSLATION NOTES and ADDITIONAL TRANSLATION NOTES sections
into a unified TRANSLATION COMPARISON section for Deuteronomy Study Notes.
"""

import re
import os

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/05 - Deuteronomy"


def find_section_boundaries(content, header_text):
    """Find the start and end of a section by its header."""
    header_with_dashes = header_text + "\n------------------------------------"
    start = content.find(header_with_dashes)
    if start == -1:
        return -1, -1
    
    # Content starts after the dashes line
    content_start = start + len(header_with_dashes) + 1  # +1 for newline
    
    # Find the next section header (uppercase text followed by dashes)
    rest = content[content_start:]
    # Match a line that is all caps (possibly with spaces/&) followed by \n----
    next_match = re.search(r'\n([A-Z][A-Z &/(),]+)\n----', rest)
    if next_match:
        end = content_start + next_match.start()
    else:
        end = len(content)
    
    return start, end


def parse_kjv_esv_entries(text):
    """
    Parse TRANSLATION NOTES section into list of (verse_num, full_text) tuples.
    Each entry starts with 'v.XX' at the beginning of a line.
    """
    entries = []
    lines = text.split('\n')
    current_verse = None
    current_lines = []
    
    for line in lines:
        match = re.match(r'^(v\.\d+)\s+—\s+(.*)$', line)
        if match:
            if current_verse:
                entries.append((current_verse, '\n'.join(current_lines)))
            current_verse = match.group(1)
            current_lines = [match.group(2)]
        elif current_verse is not None:
            current_lines.append(line)
    
    if current_verse:
        entries.append((current_verse, '\n'.join(current_lines)))
    
    return entries


def parse_additional_entries(text):
    """
    Parse ADDITIONAL TRANSLATION NOTES section into list of (verse_num, full_text) tuples.
    Each entry starts with '- v.XX' at the beginning of a line.
    """
    entries = []
    lines = text.split('\n')
    current_verse = None
    current_lines = []
    
    for line in lines:
        match = re.match(r'^-\s+(v\.\d+)\s+—\s+(.*)$', line)
        if match:
            if current_verse:
                entries.append((current_verse, '\n'.join(current_lines)))
            current_verse = match.group(1)
            current_lines = [match.group(2)]
        elif current_verse is not None:
            if line.strip() == '' and current_lines and current_lines[-1].strip() == '':
                # Double blank line might end the entry, but let's just keep going
                current_lines.append(line)
            else:
                current_lines.append(line)
    
    if current_verse:
        entries.append((current_verse, '\n'.join(current_lines)))
    
    return entries


def extract_quotes_from_kjv_esv(text):
    """Extract KJV quote, ESV quote, Hebrew info, and analysis from a KJV/ESV entry."""
    kjv_quote = ""
    esv_quote = ""
    hebrew_word = ""
    analysis_text = ""
    
    # Extract KJV/ESV quotes - handle multiline
    full_text = ' '.join(text.split('\n'))  # Flatten for regex
    full_text = re.sub(r'\s+', ' ', full_text)  # Normalize spaces
    
    kjv_match = re.search(r'KJV:\s*"([^"]+)"', full_text)
    esv_match = re.search(r'ESV:\s*"([^"]+)"', full_text)
    
    if kjv_match:
        kjv_quote = kjv_match.group(1)
    if esv_match:
        esv_quote = esv_match.group(1)
    
    # Extract Hebrew word/phrase
    hebrew_match = re.search(r'Hebrew\s+"([^"]+)"', full_text)
    if not hebrew_match:
        hebrew_match = re.search(r'Hebrew\s+[""]([^""]+)[""]', full_text)
    if hebrew_match:
        hebrew_word = hebrew_match.group(1)
    
    # The analysis is everything after "KJV:... / ESV:..." and the dash separator
    # Usually format is: KJV: "x" / ESV: "y" — Hebrew "z". Explanation...
    # Find content after the KJV/ESV pattern
    dash_split = full_text.split(' — ', 1)
    if len(dash_split) > 1:
        analysis_text = dash_split[1].strip()
    else:
        # Try after ESV quote
        if esv_match:
            analysis_text = full_text[esv_match.end():].strip(' —.')
            if analysis_text.startswith('— '):
                analysis_text = analysis_text[2:]
        elif kjv_match:
            analysis_text = full_text[kjv_match.end():].strip(' —.')
    
    # Clean trailing whitespace
    analysis_text = analysis_text.rstrip()
    
    return kjv_quote, esv_quote, hebrew_word, analysis_text


def extract_quotes_from_additional(text):
    """Extract NET, ASV, WEB quotes and analysis from an additional entry."""
    net_quote = ""
    asv_quote = ""
    web_quote = ""
    kjv_quote = ""
    analysis_text = ""
    
    # Flatten text
    full_text = ' '.join(text.split('\n'))
    full_text = re.sub(r'\s+', ' ', full_text)
    
    net_match = re.search(r'NET:\s*"([^"]+)"', full_text)
    asv_match = re.search(r'ASV:\s*"([^"]+)"', full_text)
    web_match = re.search(r'WEB:\s*"([^"]+)"', full_text)
    kjv_match = re.search(r'KJV:\s*"([^"]+)"', full_text)
    
    if net_match:
        net_quote = net_match.group(1)
    if asv_match:
        asv_quote = asv_match.group(1)
    if web_match:
        web_quote = web_match.group(1)
    if kjv_match:
        kjv_quote = kjv_match.group(1)
    
    # Analysis is typically after the last " — " or after last closing quote
    # Find the explanation portion (after the translation quotes and dash)
    dash_split = full_text.split(' — ')
    if len(dash_split) > 1:
        analysis_text = dash_split[-1].strip()
    else:
        # Everything after the last quote
        last_quote_pos = max(
            full_text.rfind('/"') if '/"' in full_text else -1,
            full_text.rfind('" —') if '" —' in full_text else -1,
            full_text.rfind('".') if '".' in full_text else -1,
        )
        if last_quote_pos > 0:
            analysis_text = full_text[last_quote_pos+2:].strip(' —.')
    
    return net_quote, asv_quote, web_quote, kjv_quote, analysis_text


def build_unified_section(tn_entries, atn_entries):
    """Build the unified TRANSLATION COMPARISON section."""
    # Group additional entries by verse for lookup
    atn_by_verse = {}
    for verse, text in atn_entries:
        atn_by_verse.setdefault(verse, []).append(text)
    
    # Track which additional entries have been used
    used_atn_verses = set()
    
    output_entries = []
    
    # Process each KJV/ESV entry
    for verse, tn_text in tn_entries:
        kjv_quote, esv_quote, hebrew_word, tn_analysis = extract_quotes_from_kjv_esv(tn_text)
        
        # Find matching additional entry for this verse
        net_quote = ""
        asv_quote = ""
        web_quote = ""
        atn_analysis = ""
        atn_kjv_quote = ""
        
        if verse in atn_by_verse and atn_by_verse[verse]:
            # Pop the first available additional entry for this verse
            add_text = atn_by_verse[verse].pop(0)
            if not atn_by_verse[verse]:
                used_atn_verses.add(verse)
            net_quote, asv_quote, web_quote, atn_kjv_quote, atn_analysis = extract_quotes_from_additional(add_text)
        
        # Build header line
        if hebrew_word:
            # Get a short meaning from the analysis
            meaning = get_short_meaning(tn_analysis, hebrew_word)
            header = f'{verse}  — Hebrew "{hebrew_word}" — {meaning}'
        else:
            meaning = get_short_meaning(tn_analysis, "")
            header = f'{verse}  — {meaning}'
        
        # Build combined analysis
        combined_analysis = tn_analysis
        if atn_analysis and atn_analysis.strip() not in combined_analysis:
            combined_analysis = combined_analysis.rstrip('. ') + '. ' + atn_analysis
        
        # Format the entry
        lines = [header]
        if kjv_quote:
            lines.append(f'       KJV: "{kjv_quote}"')
        if esv_quote:
            lines.append(f'       ESV: "{esv_quote}"')
        if asv_quote:
            lines.append(f'       ASV: "{asv_quote}"')
        if net_quote:
            lines.append(f'       NET: "{net_quote}"')
        if web_quote:
            lines.append(f'       WEB: "{web_quote}"')
        lines.append(f'       Analysis: {combined_analysis}')
        
        output_entries.append('\n'.join(lines))
    
    # Now handle additional entries that have no corresponding KJV/ESV entry
    for verse, remaining_list in atn_by_verse.items():
        for add_text in remaining_list:
            net_quote, asv_quote, web_quote, kjv_quote, atn_analysis = extract_quotes_from_additional(add_text)
            
            meaning = get_short_meaning(atn_analysis, "")
            header = f'{verse}  — {meaning}'
            
            lines = [header]
            if kjv_quote:
                lines.append(f'       KJV: "{kjv_quote}"')
            if asv_quote:
                lines.append(f'       ASV: "{asv_quote}"')
            if net_quote:
                lines.append(f'       NET: "{net_quote}"')
            if web_quote:
                lines.append(f'       WEB: "{web_quote}"')
            lines.append(f'       Analysis: {atn_analysis}')
            
            output_entries.append('\n'.join(lines))
    
    return output_entries


def get_short_meaning(analysis, hebrew_word):
    """Extract a short meaning description from the analysis text."""
    if not analysis:
        return "translation comparison."
    
    # Often the analysis starts with the Hebrew word definition
    # e.g., '"b\'ever ha-Yarden." The phrase means...'
    # Try to get the first meaningful sentence
    
    # Remove leading Hebrew transliteration in quotes if present
    cleaned = analysis
    if cleaned.startswith('"'):
        end_quote = cleaned.find('"', 1)
        if end_quote > 0:
            cleaned = cleaned[end_quote+1:].strip('. ')
    
    # Get first sentence
    first_period = cleaned.find('.')
    if first_period > 0 and first_period < 150:
        return cleaned[:first_period+1].strip()
    elif len(cleaned) > 120:
        # Find a reasonable break point
        break_point = cleaned.find('.', 40)
        if break_point > 0 and break_point < 150:
            return cleaned[:break_point+1].strip()
        break_point = cleaned.find(';', 40)
        if break_point > 0 and break_point < 120:
            return cleaned[:break_point+1].strip()
        return cleaned[:100].strip() + "..."
    else:
        return cleaned.strip()


def sort_entries_by_verse(entries):
    """Sort unified entries by verse number."""
    def get_verse_num(entry):
        match = re.match(r'v\.(\d+)', entry)
        if match:
            return int(match.group(1))
        return 999
    
    return sorted(entries, key=get_verse_num)


def process_file(filepath):
    """Process a single study notes file."""
    print(f"\nProcessing: {os.path.basename(os.path.dirname(filepath))}/{os.path.basename(filepath)}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find TRANSLATION NOTES section
    tn_start, tn_end = find_section_boundaries(content, "TRANSLATION NOTES")
    if tn_start == -1:
        print(f"  ERROR: No TRANSLATION NOTES section found!")
        return False
    
    # Find ADDITIONAL TRANSLATION NOTES section
    atn_start, atn_end = find_section_boundaries(content, "ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)")
    if atn_start == -1:
        print(f"  ERROR: No ADDITIONAL TRANSLATION NOTES section found!")
        return False
    
    # Extract the content of each section (just the body, not the headers)
    tn_header_end = content.find("\n", content.find("----", tn_start) + 4) + 1
    tn_body = content[tn_header_end:tn_end]
    
    atn_header_end = content.find("\n", content.find("----", atn_start) + 4) + 1
    atn_body = content[atn_header_end:atn_end]
    
    # Check if GLOSSARY is between TRANSLATION NOTES and ADDITIONAL
    glossary_start, glossary_end = find_section_boundaries(content, "GLOSSARY")
    glossary_between = False
    glossary_text = ""
    
    if glossary_start > tn_start and glossary_start < atn_start:
        glossary_between = True
        glossary_text = content[glossary_start:glossary_end]
        # Adjust tn_body to end at glossary
        tn_body = content[tn_header_end:glossary_start]
    
    # Parse entries from both sections
    tn_entries = parse_kjv_esv_entries(tn_body)
    atn_entries = parse_additional_entries(atn_body)
    
    print(f"  Found {len(tn_entries)} KJV/ESV entries, {len(atn_entries)} additional entries")
    
    # Build unified section
    unified_entries = build_unified_section(tn_entries, atn_entries)
    
    # Sort by verse number
    unified_entries = sort_entries_by_verse(unified_entries)
    
    # Build the new section text
    new_section = "TRANSLATION COMPARISON\n------------------------------------\n"
    new_section += '\n\n'.join(unified_entries)
    new_section += '\n'
    
    # Determine what to replace
    # We want to replace from TRANSLATION NOTES header through the end of ADDITIONAL TRANSLATION NOTES
    if glossary_between:
        # Replace: TRANSLATION NOTES + GLOSSARY + ADDITIONAL => TRANSLATION COMPARISON + GLOSSARY
        replace_start = tn_start
        replace_end = atn_end
        replacement = new_section + '\n' + glossary_text + '\n'
    else:
        # Check if GLOSSARY comes right after ADDITIONAL
        if glossary_start > atn_start:
            # GLOSSARY is after ADDITIONAL - replace just the two translation sections
            replace_start = tn_start
            replace_end = atn_end
            replacement = new_section
        else:
            # No glossary at all or it's elsewhere
            replace_start = tn_start
            replace_end = atn_end
            replacement = new_section
    
    # Do the replacement
    new_content = content[:replace_start] + replacement + content[replace_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  SUCCESS: Written unified section with {len(unified_entries)} entries.")
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
            print(f"  File not found: {filepath}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Complete: {success} succeeded, {failed} failed out of {len(chapters)} files.")


if __name__ == "__main__":
    main()
