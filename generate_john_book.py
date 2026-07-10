#!/usr/bin/env python3
"""
Generate an HTML Bible Book viewer for the entire Gospel of John.
Reads all chapter files (5 translations + study notes) and produces a single HTML file.
"""

import os
import json
import re

BASE_DIR = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/04 - John"
OUTPUT_FILE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/John-BibleBook.html"

TRANSLATIONS = ["ESV", "KJV", "ASV", "NET", "WEB"]
NUM_CHAPTERS = 21


def parse_verses(filepath):
    """Parse a translation file and return list of verse strings."""
    verses = []
    if not os.path.exists(filepath):
        return verses
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match:
            verses.append(match.group(2))
    return verses


def parse_study_notes(filepath):
    """Parse study notes file and return the raw text content."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    all_data = {}
    for ch in range(1, NUM_CHAPTERS + 1):
        chapter_dir = os.path.join(BASE_DIR, f"Chapter {ch}")
        chapter_data = {"translations": {}, "studyNotes": ""}
        for trans in TRANSLATIONS:
            filepath = os.path.join(chapter_dir, f"Chapter {ch} - {trans}.txt")
            chapter_data["translations"][trans] = parse_verses(filepath)
        notes_path = os.path.join(chapter_dir, f"Chapter {ch} - Study Notes.txt")
        chapter_data["studyNotes"] = parse_study_notes(notes_path)
        all_data[str(ch)] = chapter_data

    # Serialize to JSON
    json_str = json.dumps(all_data, ensure_ascii=False)
    # Escape </script> to prevent breaking the HTML
    json_str = json_str.replace('</script>', '<\\/script>')

    # Build chapter options
    chapter_options = '\n'.join(
        f'                <option value="{i}">Chapter {i}</option>'
        for i in range(1, 22)
    )

    # Write the HTML using template parts (no f-strings to avoid brace issues)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(HTML_TOP)
        f.write(chapter_options)
        f.write(HTML_MID)
        f.write(json_str)
        f.write(HTML_BOTTOM)

    print(f"Generated: {OUTPUT_FILE}")
    for ch in range(1, NUM_CHAPTERS + 1):
        for trans in TRANSLATIONS:
            count = len(all_data[str(ch)]["translations"][trans])
            if count == 0:
                print(f"  WARNING: Chapter {ch} {trans} has 0 verses!")


HTML_TOP = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Gospel of John \u2014 Bible Study</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #2c1810;
            background-image: radial-gradient(ellipse at center, #3d2317 0%, #1a0f0a 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            font-family: 'Source Serif 4', serif;
        }
        h1.page-title {
            font-family: 'Playfair Display', serif;
            color: #d4a84b;
            font-size: 2.2rem;
            text-align: center;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        .controls {
            margin-bottom: 30px;
            text-align: center;
            display: flex;
            gap: 25px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .control-group { display: flex; align-items: center; gap: 10px; }
        .controls label { font-family: 'Inter', sans-serif; color: #c9a96e; font-size: 1.1rem; }
        .controls select {
            font-family: 'Source Serif 4', serif;
            font-size: 1rem;
            padding: 8px 16px;
            border: 2px solid #8b6914;
            border-radius: 4px;
            background: #f5e6c8;
            color: #3d2317;
            cursor: pointer;
            outline: none;
        }
        .controls select:focus { border-color: #d4a84b; box-shadow: 0 0 8px rgba(212, 168, 75, 0.4); }
        .book-wrapper { display: flex; align-items: center; gap: 20px; margin-bottom: 15px; }
        .nav-arrow {
            background: none; border: none; color: #c9a96e; font-size: 2.5rem;
            cursor: pointer; padding: 15px 10px; border-radius: 8px;
            transition: all 0.3s ease; user-select: none; opacity: 0.8;
        }
        .nav-arrow:hover { color: #d4a84b; opacity: 1; background: rgba(212,168,75,0.1); transform: scale(1.1); }
        .nav-arrow:disabled { opacity: 0.2; cursor: default; transform: none; background: none; }
        .book-container { perspective: 1800px; }
        .book {
            display: flex; width: 900px; max-width: 80vw; height: 620px;
            position: relative; transform: rotateX(2deg);
            box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 5px 20px rgba(0,0,0,0.4);
        }
        .book::before {
            content: ''; position: absolute; left: 50%; top: 0; bottom: 0; width: 6px;
            transform: translateX(-50%);
            background: linear-gradient(to right, #1a0f0a, #4a3020, #1a0f0a);
            z-index: 10; box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        .page { flex: 1; padding: 40px 45px; position: relative; overflow: hidden; }
        .page-left {
            background: linear-gradient(135deg, #f7eed8 0%, #f0e4c8 50%, #e8d9b4 100%);
            border-radius: 8px 0 0 8px; box-shadow: inset -5px 0 15px rgba(0,0,0,0.08);
        }
        .page-right {
            background: linear-gradient(225deg, #f7eed8 0%, #f0e4c8 50%, #e8d9b4 100%);
            border-radius: 0 8px 8px 0; box-shadow: inset 5px 0 15px rgba(0,0,0,0.08);
        }
        .page::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
            pointer-events: none; border-radius: inherit;
        }
        .chapter-heading {
            font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #5c3a1e;
            text-align: center; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #c9a96e;
        }
        .chapter-heading span {
            display: block; font-family: 'Inter', sans-serif; font-size: 0.85rem;
            color: #8b6914; margin-top: 4px; font-style: italic;
        }
        .verse { margin-bottom: 8px; line-height: 1.7; color: #2c1810; font-size: 0.95rem; text-align: justify; }
        .verse-number { font-weight: 700; color: #8b4513; font-size: 0.8rem; vertical-align: super; margin-right: 3px; }
        .page-number { position: absolute; bottom: 20px; font-family: 'Inter', sans-serif; color: #8b6914; font-size: 0.85rem; }
        .page-left .page-number { left: 45px; }
        .page-right .page-number { right: 45px; }
        .page-indicator { text-align: center; font-family: 'Inter', sans-serif; color: #c9a96e; font-size: 0.95rem; margin-bottom: 40px; font-style: italic; }
        .study-notes-section { width: 900px; max-width: 80vw; margin-top: 20px; }
        .study-notes-title {
            font-family: 'Playfair Display', serif; color: #d4a84b; font-size: 1.6rem;
            text-align: center; margin-bottom: 25px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        .study-notes-content {
            background: linear-gradient(135deg, #faf3e3 0%, #f5ecd5 100%);
            border: 2px solid #c9a96e; border-radius: 12px; padding: 40px 50px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.5);
            position: relative; white-space: pre-wrap;
            font-family: 'Inter', sans-serif; font-size: 1.05rem; line-height: 1.8; color: #3d2317;
        }
        .study-notes-content::before {
            content: ''; position: absolute; top: 15px; left: 15px; right: 15px; bottom: 15px;
            border: 1px solid rgba(201, 169, 110, 0.3); border-radius: 8px; pointer-events: none;
        }
        .study-notes-content h2 {
            font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #1a2744;
            margin: 25px 0 12px 0; padding-bottom: 8px;
            border-bottom: 1px solid rgba(26, 39, 68, 0.2); white-space: normal;
            text-align: center;
        }
        .study-notes-content h2:first-child { margin-top: 0; }
        .study-notes-content a { color: #8b4513; text-decoration: underline; }
        .study-notes-content a:hover { color: #d4a84b; }
        .study-notes-content .ornament { text-align: center; color: #c9a96e; font-size: 1.5rem; margin: 20px 0; opacity: 0.7; display: block; }
        .no-notes { text-align: center; font-style: italic; color: #8b6914; padding: 40px; }
        .study-notes-content table { font-family: 'Inter', sans-serif; }
        .study-notes-content td { word-wrap: break-word; }
        @media (max-width: 768px) {
            .book { flex-direction: column; width: 100%; height: auto; }
            .page-left { border-radius: 8px 8px 0 0; border-bottom: 3px solid #4a3020; }
            .page-right { border-radius: 0 0 8px 8px; }
            .book::before { left: 0; right: 0; top: 50%; bottom: auto; width: 100%; height: 6px; transform: translateY(-50%); background: linear-gradient(to bottom, #1a0f0a, #4a3020, #1a0f0a); }
            .page { padding: 25px 20px; }
            h1.page-title { font-size: 1.5rem; }
            .study-notes-content { padding: 25px 20px; }
            .nav-arrow { font-size: 1.8rem; padding: 10px 5px; }
            .controls { flex-direction: column; gap: 15px; }
        }
    </style>
</head>
<body>
    <h1 class="page-title">The Gospel of John</h1>
    <div class="controls">
        <div class="control-group">
            <label for="translation">Translation:</label>
            <select id="translation" onchange="render()">
                <option value="ESV">English Standard Version (ESV)</option>
                <option value="KJV">King James Version (KJV)</option>
                <option value="ASV">American Standard Version (ASV)</option>
                <option value="NET">NET Bible (NET)</option>
                <option value="WEB">World English Bible (WEB)</option>
            </select>
        </div>
        <div class="control-group">
            <label for="chapter">Chapter:</label>
            <select id="chapter" onchange="changeChapter()">
'''

HTML_MID = '''
            </select>
        </div>
    </div>
    <div class="book-wrapper">
        <button class="nav-arrow" id="prev-btn" onclick="prevPage()" title="Previous page">&#9664;</button>
        <div class="book-container">
            <div class="book">
                <div class="page page-left" id="page-left">
                    <div class="chapter-heading" id="chapter-heading">
                        Chapter 1
                        <span id="translation-label">English Standard Version</span>
                    </div>
                    <div id="verses-left"></div>
                    <div class="page-number" id="page-num-left"></div>
                </div>
                <div class="page page-right" id="page-right">
                    <div id="verses-right"></div>
                    <div class="page-number" id="page-num-right"></div>
                </div>
            </div>
        </div>
        <button class="nav-arrow" id="next-btn" onclick="nextPage()" title="Next page">&#9654;</button>
    </div>
    <div class="page-indicator" id="page-indicator"></div>
    <div class="study-notes-section">
        <h2 class="study-notes-title">&#10022; Notes &#10022;</h2>
        <div class="study-notes-content" id="study-notes-content"></div>
    </div>
    <script>
    const VERSES_PER_PAGE = 8;
    let currentSpread = 0;
    let totalSpreads = 0;
    const bookData = '''

HTML_BOTTOM = ''';
    const translationNames = {
        "ESV": "English Standard Version",
        "KJV": "King James Version",
        "ASV": "American Standard Version",
        "NET": "NET Bible",
        "WEB": "World English Bible"
    };
    function getCurrentChapter() { return document.getElementById('chapter').value; }
    function getCurrentTranslation() { return document.getElementById('translation').value; }
    function changeChapter() { currentSpread = 0; render(); }

    function render() {
        const ch = getCurrentChapter();
        const trans = getCurrentTranslation();
        const chData = bookData[ch];
        if (!chData) return;

        const verses = chData.translations[trans] || [];
        document.getElementById('chapter-heading').innerHTML =
            `Chapter ${ch}<span id="translation-label">${translationNames[trans]}</span>`;

        totalSpreads = Math.max(1, Math.ceil(verses.length / (VERSES_PER_PAGE * 2)));
        const startIndex = currentSpread * VERSES_PER_PAGE * 2;
        const leftVerses = verses.slice(startIndex, startIndex + VERSES_PER_PAGE);
        const rightVerses = verses.slice(startIndex + VERSES_PER_PAGE, startIndex + VERSES_PER_PAGE * 2);

        let leftHTML = '';
        leftVerses.forEach((verse, i) => {
            const verseNum = startIndex + i + 1;
            leftHTML += `<p class="verse"><span class="verse-number">${verseNum}</span>${verse}</p>`;
        });

        let rightHTML = '';
        rightVerses.forEach((verse, i) => {
            const verseNum = startIndex + VERSES_PER_PAGE + i + 1;
            rightHTML += `<p class="verse"><span class="verse-number">${verseNum}</span>${verse}</p>`;
        });

        document.getElementById('verses-left').innerHTML = leftHTML;
        document.getElementById('verses-right').innerHTML = rightHTML;

        const leftPageNum = currentSpread * 2 + 1;
        const rightPageNum = currentSpread * 2 + 2;
        document.getElementById('page-num-left').textContent = leftPageNum;
        document.getElementById('page-num-right').textContent = rightPageNum;
        document.getElementById('page-indicator').textContent =
            `Pages ${leftPageNum}\\u2013${rightPageNum} of ${totalSpreads * 2}`;

        document.getElementById('prev-btn').disabled = (currentSpread === 0);
        document.getElementById('next-btn').disabled = (currentSpread >= totalSpreads - 1);

        renderStudyNotes(chData.studyNotes);
    }

    function renderStudyNotes(rawNotes) {
        const container = document.getElementById('study-notes-content');
        if (!rawNotes || rawNotes.trim() === '') {
            container.innerHTML = '<p class="no-notes">No study notes available for this chapter.</p>';
            return;
        }
        let html = rawNotes;
        // Remove header lines up to first ====
        html = html.replace(/^[\\s\\S]*?={5,}\\n/, '');
        // Remove PERSONAL NOTES section and everything after it
        html = html.replace(/\\nPERSONAL NOTES[\\s\\S]*$/, '');
        // Remove PERSONAL REFLECTION & APPLICATION section
        html = html.replace(/\\nPERSONAL REFLECTION[^\\n]*\\n-{4,}[\\s\\S]*?(?=\\n[A-Z]{3,}[^\\n]*\\n-{4,}|$)/g, '');
        // Remove REFLECTION QUESTIONS section
        html = html.replace(/\\nREFLECTION QUESTIONS[^\\n]*\\n-{4,}[\\s\\S]*?(?=\\n[A-Z]{3,}[^\\n]*\\n-{4,}|$)/g, '');
        // Remove KEY VERSES section
        html = html.replace(/\\nKEY VERSES[^\\n]*\\n-{4,}[\\s\\S]*?(?=\\n[A-Z]{3,}[^\\n]*\\n-{4,}|$)/g, '');
        // Remove "ADDITIONAL TRANSLATION NOTES" header (merge into TRANSLATION NOTES)
        html = html.replace(/\\nADDITIONAL TRANSLATION NOTES[^\\n]*\\n-{4,}/g, '');
        // Remove trailing ==== footer and "Study Notes generated..." text
        html = html.replace(/\\n={5,}[\\s\\S]*$/, '');
        // Remove "NOTE: Links may change..." lines
        html = html.replace(/\\nNOTE: Links may change[^\\n]*\\n?/g, '');
        // Convert section headers (ALL CAPS followed by dashes) - centered
        html = html.replace(/^([A-Z][A-Z &(),'\\d]+)\\n-{4,}/gm, '<span class="ornament">\\u271a</span><h2>$1</h2>');
        // Convert URLs to clickable links
        html = html.replace(/(https?:\\/\\/[^\\s<)]+)/g, '<a href="$1" target="_blank">$1</a>');
        // Make "Enduring Word" text a clickable link using the nearby URL, and hide the raw URL line
        html = html.replace(/Enduring Word \\(David Guzik\\):\\n\\s*<a href="([^"]+)"[^>]*>[^<]*<\\/a>/g, '<a href="$1" target="_blank" style="color:#6b1c2a;font-weight:600;">Enduring Word (David Guzik)</a>');
        // Color and bold category labels (Author:, Date Written:, Audience:, etc.)
        html = html.replace(/^((?:Author|Date Written|Audience|Historical Context|Purpose[^:]*|Roman Crucifixion|Fulfilled Prophecy|Peter's Restoration|The Greek Words[^:]*|153 Fish[^:]*|Thomas|Purpose Statement|The Empty Tomb)[^:]*:)/gm, '<strong style="color:#6b1c2a;">$1</strong>');
        // Also color verse references at start of lines (v.1, v.14, vv.15-17, etc.)
        html = html.replace(/^(v{1,2}\\.?[\\d\\-,\\s]+\\s*—)/gm, '<span style="color:#6b1c2a;font-weight:600;">$1</span>');
        // Replace key verse quotes with the actual verse text from the selected translation
        const trans = getCurrentTranslation();
        const verses = bookData[getCurrentChapter()].translations[trans] || [];
        html = html.replace(/^(v\\.?(\\d+)\\s*—\\s*)"[^"]*"[^"]*"[^"]*"/gm, function(match, prefix, vNum) {
            const idx = parseInt(vNum) - 1;
            if (idx >= 0 && idx < verses.length) {
                return prefix + '"' + verses[idx] + '"';
            }
            return match;
        });
        html = html.replace(/^(v\\.?(\\d+)\\s*—\\s*)"([^"]+)"/gm, function(match, prefix, vNum, quote) {
            const idx = parseInt(vNum) - 1;
            if (idx >= 0 && idx < verses.length) {
                return prefix + '"' + verses[idx] + '"';
            }
            return match;
        });
        // Trim trailing whitespace
        html = html.trimEnd();
        container.innerHTML = html;

        // Convert TRANSLATION NOTES into a table layout
        const transSection = container.querySelector('h2');
        let transH2 = null;
        const allH2s = container.querySelectorAll('h2');
        allH2s.forEach(h2 => { if (h2.textContent.trim() === 'TRANSLATION NOTES') transH2 = h2; });

        if (transH2) {
            // Find content between TRANSLATION NOTES h2 and the next h2 or ornament
            let contentNodes = [];
            let node = transH2.nextSibling;
            while (node && !(node.nodeType === 1 && (node.tagName === 'H2' || (node.className && node.className.includes('ornament'))))) {
                contentNodes.push(node);
                node = node.nextSibling;
            }
            // Get the raw text of translation notes
            let rawText = '';
            contentNodes.forEach(n => { rawText += n.textContent || ''; });

            // Parse verse entries
            const verseBlocks = rawText.split(/\\n(?=v{1,2}\\.?\\s*\\d)/);
            let tableHTML = '';

            verseBlocks.forEach(block => {
                block = block.trim();
                if (!block) return;

                // Extract verse ref
                const refMatch = block.match(/^(v{1,2}\\.?\\s*[\\d\\-,]+)\\s*[—\\-]?\\s*(.*)/s);
                if (!refMatch) return;

                const verseRef = refMatch[1].trim();
                const content = refMatch[2];

                // Extract each translation line
                const translations = ['KJV', 'ESV', 'ASV', 'NET', 'WEB'];
                let rows = {};
                let noteText = '';
                let greekTerm = '';

                // Check for Greek term at start
                const greekMatch = content.match(/^Greek\\s+"([^"]+)"/);
                if (greekMatch) greekTerm = greekMatch[1];

                translations.forEach(t => {
                    const regex = new RegExp(t + ':\\s*(.+?)(?=\\n\\s*(?:KJV|ESV|ASV|NET|WEB|Note):|$)', 's');
                    const m = content.match(regex);
                    if (m) rows[t] = m[1].trim().replace(/\\n\\s*/g, ' ');
                });

                // Extract Note:
                const noteMatch = content.match(/Note:\\s*(.+?)$/s);
                if (noteMatch) noteText = noteMatch[1].trim().replace(/\\n\\s*/g, ' ');

                // Build table for this verse
                tableHTML += '<div style="margin-bottom:20px;border:1px solid rgba(26,39,68,0.15);border-radius:8px;overflow:hidden;">';
                tableHTML += '<div style="background:rgba(26,39,68,0.06);padding:8px 12px;font-weight:600;color:#1a2744;">' + verseRef + (greekTerm ? ' — Greek: <em>' + greekTerm + '</em>' : '') + '</div>';
                tableHTML += '<table style="width:100%;border-collapse:collapse;font-size:0.95rem;">';

                translations.forEach(t => {
                    if (rows[t]) {
                        tableHTML += '<tr style="border-top:1px solid rgba(26,39,68,0.08);">';
                        tableHTML += '<td style="padding:6px 12px;width:50px;font-weight:600;color:#6b1c2a;vertical-align:top;white-space:nowrap;">' + t + '</td>';
                        tableHTML += '<td style="padding:6px 12px;">' + rows[t] + '</td>';
                        tableHTML += '</tr>';
                    }
                });

                if (noteText) {
                    tableHTML += '<tr style="border-top:1px solid rgba(26,39,68,0.08);background:rgba(107,28,42,0.03);">';
                    tableHTML += '<td colspan="2" style="padding:6px 12px;font-style:italic;color:#444;">' + noteText + '</td>';
                    tableHTML += '</tr>';
                }

                tableHTML += '</table></div>';
            });

            // Replace the raw text with the table
            if (tableHTML) {
                contentNodes.forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
                const wrapper = document.createElement('div');
                wrapper.style.whiteSpace = 'normal';
                wrapper.innerHTML = tableHTML;
                transH2.parentNode.insertBefore(wrapper, transH2.nextSibling);
            }
        }
    }

    function nextPage() { if (currentSpread < totalSpreads - 1) { currentSpread++; render(); } }
    function prevPage() { if (currentSpread > 0) { currentSpread--; render(); } }

    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'SELECT') return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') nextPage();
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prevPage();
    });

    render();
    </script>
</body>
</html>'''


if __name__ == '__main__':
    main()
