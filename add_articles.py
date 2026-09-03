#!/usr/bin/env python3
"""
Adds the Articles tab to every chapter page, and an Articles section block to
the topical and life pages.

Two page shapes, one script, because the site has two layouts:

  chapter pages     1189 of them, six tabs already. Articles becomes a seventh,
                    inserted between Videos and Reflection.
  topical / life    34 of them, no tabs at all -- a stack of section blocks all
                    visible at once. Articles becomes another section block,
                    appended last, exactly the way Video Resources sits last on
                    the life pages.

Making the topical pages tabbed to match the chapter pages was considered and
rejected: it would mean redesigning 34 hand-written files, and it would put
site/style.css and site/script.js in play. Those two are on the sync's preserve
list, so any change to them has to be made by hand in both repos. See
WORKFLOW.md.

The chapter tab needs no CSS and no JavaScript change at all. switchTab() in
site/script.js works off the data-tab / id="tab-X" pairing and nothing else, and
.study-tabs is a wrapping flexbox, so a seventh tab reflows on its own.

Why Reflection is the anchor rather than Videos. add_commentaries.py anchors
against the Videos tab, but strip_empty_videos_tab() in video_sources.py deletes
that tab when a chapter has no players left, so the anchor is not guaranteed to
exist. Reflection is on all 1189 pages and nothing removes it. Inserting before
Reflection also gives the ordering we want, with Reflection last.

Idempotency is by fenced comment, the same approach add_mapgeo_maps.py uses for
geo notes. Re-running regenerates the block between the fences and leaves the
rest of the page byte-identical, so this is safe to run after every change to
article_sources.py.

What content goes where lives in article_sources.py, not here. This file only
knows how to put a list of links into two shapes of HTML.

Usage:
    python3 add_articles.py [--check] [--chapters-only] [--topics-only]

--check reports what would change and writes nothing.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_commentaries as ac  # noqa: E402  -- reuse the canonical BOOKS table
import article_sources as asrc  # noqa: E402

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^([a-z0-9]+?)(\d+)\.html$")

FENCE_OPEN = "<!-- articles -->"
FENCE_CLOSE = "<!-- /articles -->"

TAB_BUTTON = '<div class="study-tab" data-tab="articles">Articles</div>'
REFLECTION_BUTTON = '<div class="study-tab" data-tab="reflection">Reflection</div>'
REFLECTION_PANE = '            <div class="tab-content" id="tab-reflection">'

# The whole pane, fences included, so a re-run can find and replace it.
PANE = re.compile(
    r'[ \t]*<div class="tab-content" id="tab-articles">.*?\n[ \t]*</div>\n',
    re.S)
BLOCK = re.compile(
    r'[ \t]*<div class="section-block">\s*<h2>Articles</h2>.*?\n[ \t]*</div>\n',
    re.S)


def render_items(entries, indent):
    pad = " " * indent
    return ("\n" + pad).join(asrc.render_li(*e) for e in entries)


def build_pane(entries):
    """The chapter-page tab pane. Indentation matches the other panes."""
    return ('            <div class="tab-content" id="tab-articles">\n'
            "                <h3>Articles</h3>\n"
            f"                {FENCE_OPEN}\n"
            "                <ul>\n"
            f"                    {render_items(entries, 20)}\n"
            "                </ul>\n"
            "                <p style=\"font-size:0.78rem;color:var(--text-faint);"
            "margin-top:14px;line-height:1.7;\">Links open on the publisher's own "
            "site. Nothing here is reproduced on this page.</p>\n"
            f"                {FENCE_CLOSE}\n"
            "            </div>\n")


def build_block(entries, indent):
    """The topical / life page section block.

    Indentation is passed in rather than hardcoded because </main> sits at four
    spaces on 20 of these pages and eight on the other 14. Hardcoding it meant
    matching the tail of the deeper indent and rewriting the </main> line, which
    left a 12-space opening div and re-indented a line this script has no
    business touching.
    """
    pad = " " * indent
    inner = " " * (indent + 4)
    return (f'{pad}<div class="section-block">\n'
            f"{inner}<h2>Articles</h2>\n"
            f"{inner}{FENCE_OPEN}\n"
            f"{inner}<ul>\n"
            f"{inner}    {render_items(entries, indent + 8)}\n"
            f"{inner}</ul>\n"
            f"{inner}<p style=\"font-size:0.78rem;color:var(--text-faint);"
            "margin-top:14px;line-height:1.7;\">Links open on the publisher's own "
            "site. Nothing here is reproduced on this page.</p>\n"
            f"{inner}{FENCE_CLOSE}\n"
            f"{pad}</div>\n")


def divs_balanced(text):
    return len(re.findall(r"<div\b", text)) == len(re.findall(r"</div>", text))


def sibling_indent(text, close_match):
    """Indent to use for a new section block: whatever the page already uses for
    its other section blocks.

    All 34 topic pages indent their section blocks at eight spaces, but only 20
    of them close </main> at four, so anchoring the indent to </main> would leave
    the new block out of line with its siblings on those 20. Falls back to the
    </main> indent plus four if a page somehow has no sibling.
    """
    sibs = re.findall(r'\n([ \t]*)<div class="section-block"', text)
    if sibs:
        return len(max(sibs, key=sibs.count))
    return len(close_match.group(1)) + 4


def do_chapters(check, problems):
    pages = []
    for name in sorted(os.listdir(DOCS)):
        m = CHAPTER.match(name)
        if m and m.group(1) in ac.BOOKS:
            pages.append((name, m.group(1), int(m.group(2))))

    changed = created = refreshed = skipped_untabbed = 0
    for name, slug, ch in pages:
        path = os.path.join(DOCS, name)
        text = original = open(path, encoding="utf-8").read()

        # 1190 files match the chapter filename pattern but only 1189 carry a
        # tab strip. Never assume the name implies the layout.
        if '<div class="study-tabs">' not in text:
            skipped_untabbed += 1
            continue

        entries = asrc.chapter_entries(slug, ch)
        if not entries:
            # Cannot happen while every book has a derived overview link, which
            # is the point of it. Guard anyway rather than write an empty pane.
            problems.append(f"{name}: no articles resolved for {slug} {ch}")
            continue

        pane = build_pane(entries)
        existing = PANE.search(text)
        if existing:
            text = text[:existing.start()] + pane + text[existing.end():]
            refreshed += 1
        else:
            if TAB_BUTTON in text:
                problems.append(f"{name}: Articles button present with no pane")
                continue
            if REFLECTION_BUTTON not in text:
                problems.append(f"{name}: no Reflection tab to anchor against")
                continue
            if REFLECTION_PANE not in text:
                problems.append(f"{name}: no Reflection pane to anchor against")
                continue
            text = text.replace(
                REFLECTION_BUTTON, TAB_BUTTON + "\n                "
                + REFLECTION_BUTTON, 1)
            text = text.replace(REFLECTION_PANE, pane + REFLECTION_PANE, 1)
            created += 1

        if not divs_balanced(text):
            problems.append(f"{name}: would unbalance divs, skipped")
            continue

        if text != original:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(text)

    return {
        "considered": len(pages),
        "changed": changed,
        "created": created,
        "refreshed": refreshed,
        "skipped_untabbed": skipped_untabbed,
    }


def do_topics(check, problems):
    changed = created = refreshed = 0
    names = sorted(asrc.TOPIC_ARTICLES)
    for name in names:
        path = os.path.join(DOCS, name)
        if not os.path.isfile(path):
            problems.append(f"{name}: listed in TOPIC_ARTICLES but not in docs/")
            continue
        text = original = open(path, encoding="utf-8").read()

        # These pages must not have tabs. If one ever does it is a chapter-style
        # page and belongs in the other pass.
        if "data-tab" in text:
            problems.append(f"{name}: has tabs, should not be a topic page")
            continue
        close = re.search(r"\n([ \t]*)</main>", text)
        if not close:
            problems.append(f"{name}: no </main> to anchor against")
            continue

        entries = asrc.page_entries(name)
        if not entries:
            problems.append(f"{name}: no articles resolved")
            continue

        existing = BLOCK.search(text)
        if existing:
            # Reuse whatever indent the block already has so a refresh is a
            # content-only diff.
            indent = len(existing.group(0)) - len(existing.group(0).lstrip(" \t"))
            block = build_block(entries, indent)
            text = text[:existing.start()] + block + text[existing.end():]
            refreshed += 1
        else:
            block = build_block(entries, sibling_indent(text, close))
            # Insert after the newline, so the </main> line itself is untouched.
            at = close.start() + 1
            text = text[:at] + block + text[at:]
            created += 1

        if not divs_balanced(text):
            problems.append(f"{name}: would unbalance divs, skipped")
            continue

        if text != original:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(text)

    return {
        "considered": len(names),
        "changed": changed,
        "created": created,
        "refreshed": refreshed,
    }


def main():
    check = "--check" in sys.argv
    chapters_only = "--chapters-only" in sys.argv
    topics_only = "--topics-only" in sys.argv

    problems = []
    verb = "would change" if check else "changed"

    if not topics_only:
        r = do_chapters(check, problems)
        print(f"chapter pages: {verb} {r['changed']} of {r['considered']}")
        print(f"  Articles tab created      : {r['created']}")
        print(f"  existing pane refreshed   : {r['refreshed']}")
        print(f"  skipped, no tab strip     : {r['skipped_untabbed']}")

    if not chapters_only:
        r = do_topics(check, problems)
        print(f"topical / life pages: {verb} {r['changed']} of {r['considered']}")
        print(f"  Articles block created    : {r['created']}")
        print(f"  existing block refreshed  : {r['refreshed']}")

    if problems:
        print(f"  {len(problems)} problem(s):")
        for p in problems[:15]:
            print(f"    {p}")
        if len(problems) > 15:
            print(f"    ... {len(problems)} problems total")
        print("  Nothing was written for those pages. To undo a bad run:")
        print("    git checkout -- docs/")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
