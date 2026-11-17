#!/usr/bin/env python3
"""
Adds the Deep Dive pane to chapter pages from deepdives/<slug>.md.

    python3 add_deep_dives.py            # every deepdives/*.md
    python3 add_deep_dives.py acts19     # one chapter
    python3 add_deep_dives.py --check    # report coverage, change nothing

The Deep Dive is a section-by-section study of the chapter: background, the
ESV section headings with bullets on history, people, Greek and Hebrew words,
Old Testament links, parallels and textual notes, and a Commentators bullet
per section drawing on Guzik (paraphrased only: under copyright), Matthew
Henry (1710) and Jamieson-Fausset-Brown (1871). The links to all three stay
in the Commentary pane, which sits right under the Deep Dive in the Study group.

The pane goes immediately before tab-commentary (present on all 1189 chapters),
and its button immediately before the Commentary button, so the order is
Summary, Authorship, Map, Deep Dive, Commentary. script.js folds the bar into
Study and Reflect; see "Study / Reflect" in WORKFLOW.md.

Re-running replaces an existing Deep Dive pane, so a .md file can be corrected
and re-applied. The .md files live outside docs/ and are not served.

Markdown accepted (deliberately small, so every chapter looks the same):
    *Setting:* ...            first paragraph, shown in italics
    #### Section heading (vv1-10)
    - bullet, with **bold**, *italic* and [links](https://...)
    - **Commentators:** ...   set off with a rule on the left
    plain paragraph
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(ROOT, "deepdives")
IND = "            "  # pane indentation used by the chapter pages

# Shown at the top of every Deep Dive so no one mistakes it for original
# scholarship. Wording agreed with Jeremy, 16 Nov 2026 (contact form link added 17 Nov); about.html has the rest.
NOTE = (f'{IND}    <p class="dd-note" style="background:var(--bg-tint-2);border:1px solid var(--border-light);border-radius:10px;padding:10px 14px;font-size:0.88rem;color:var(--text-secondary);">This Deep Dive was put together with AI help, drawing on the '
        f'commentators named below. I&rsquo;m a learner, not a scholar, so test everything against '
        f'Scripture. Spot a mistake or have an idea? <a href="contact.html?page=__SLUG__&amp;from=deepdive" style="color:var(--accent-link);">Let me know</a>. '
        f'<a href="about.html" style="color:var(--accent-link);">How this site is made</a></p>\n')

PANE_RE = re.compile(r'[ \t]*<div class="tab-content" id="tab-deepdive">.*?(?=[ \t]*<div class="tab-content")', re.S)
BTN_RE = re.compile(r'[ \t]*<div class="study-tab" data-tab="deepdive">[^<]*</div>\n')
COMMENTARY_PANE = re.compile(r'([ \t]*)<div class="tab-content" id="tab-commentary">')
COMMENTARY_BTN = re.compile(r'([ \t]*)<div class="study-tab" data-tab="commentary">')


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',
               lambda m: f'<a href="{html.escape(m.group(2))}" target="_blank" rel="noopener">{m.group(1)}</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    return s


def render(md, slug):
    out, items, para = [], [], []

    def flush_list():
        if items:
            out.append(IND + "    <ul>")
            for it in items:
                cls = ' class="dd-commentators"' if it.startswith("**Commentators:**") else ""
                out.append(f"{IND}        <li{cls}>{inline(it)}</li>")
            out.append(IND + "    </ul>")
            items.clear()

    def flush_para():
        if para:
            text = " ".join(para)
            cls = ' class="dd-setting"' if text.startswith("*Setting:*") else ""
            out.append(f"{IND}    <p{cls}>{inline(text)}</p>")
            para.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para(); flush_list(); continue
        if line.startswith("#### "):
            flush_para(); flush_list()
            out.append(f"{IND}    <h4>{inline(line[5:].strip())}</h4>")
        elif line.startswith("- "):
            flush_para()
            items.append(line[2:].strip())
        elif line.startswith("  ") and items:
            items[-1] += " " + line.strip()  # wrapped bullet
        elif line.startswith("#"):
            raise ValueError(f"only #### headings are allowed: {line!r}")
        else:
            flush_list()
            para.append(line.strip())
    flush_para(); flush_list()
    return (f'{IND}<div class="tab-content" id="tab-deepdive">\n'
            f'{IND}    <h3>Deep Dive</h3>\n' + NOTE.replace('__SLUG__', slug) + "\n".join(out) + f"\n{IND}</div>\n")


def apply(slug):
    path = os.path.join(DOCS, slug + ".html")
    md = open(os.path.join(SRC, slug + ".md"), encoding="utf-8").read()
    page = open(path, encoding="utf-8").read()
    pane = render(md, slug)
    page = PANE_RE.sub("", page)
    page = BTN_RE.sub("", page)
    if not COMMENTARY_PANE.search(page) or not COMMENTARY_BTN.search(page):
        raise SystemExit(f"{slug}: no Commentary tab to anchor on")
    page = COMMENTARY_PANE.sub(lambda m: pane + m.group(0), page, count=1)
    page = COMMENTARY_BTN.sub(lambda m: f'{m.group(1)}<div class="study-tab" data-tab="deepdive">Deep Dive</div>\n' + m.group(0), page, count=1)
    # Every tab button must still pair with a pane.
    assert set(re.findall(r'data-tab="([a-z]+)"', page)) == set(re.findall(r'id="tab-([a-z]+)"', page)), slug
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    have = sorted(f[:-3] for f in os.listdir(SRC) if re.match(r"^[0-9a-z]+?\d+\.md$", f)) if os.path.isdir(SRC) else []
    if "--check" in sys.argv:
        on_pages = sum('id="tab-deepdive"' in open(os.path.join(DOCS, f), encoding="utf-8").read()
                       for f in os.listdir(DOCS) if re.match(r"^[0-9a-z]+?\d+\.html$", f) and "tab-commentary" in
                       open(os.path.join(DOCS, f), encoding="utf-8").read())
        print(f"deep dive sources: {len(have)}  pages with a Deep Dive: {on_pages} of 1189")
        return
    todo = args or have
    for slug in todo:
        apply(slug)
    print(f"deep dives applied: {len(todo)}")


if __name__ == "__main__":
    main()
