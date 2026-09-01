#!/usr/bin/env python3
"""
Adds a YouTube video to a page, in whichever container that page uses.

Titles and channel names come from YouTube's oEmbed endpoint rather than being
typed in. That avoids both typos and the encoding corruption that put U+FFFD
into 173 captions, and it means the caption matches what the video is actually
called.

Three page shapes are recognised:

  chapter page          <div class="tab-content" id="tab-videos">
  life-study page       <div class="section-block"><h2>Video Resources</h2>
  spiritual-disciplines <h3>Videos</h3><div class="video-grid">, one per
                        section, so --section is required to pick one

Run this in bible-study, then sync into bible-study-newriver. New River Church
sermons do not belong here; they go in docs/newriver-videos.json.

Usage:
    python3 add_video.py <page.html> <video-id> [--section "Heading"] [--check]

    python3 add_video.py daniel2.html tj_WelWkR5Y
    python3 add_video.py spiritual-disciplines.html M4meOVbuB88 --section Worship
"""
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import automation_http as http  # noqa: E402

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
OEMBED = "https://www.youtube.com/oembed"

CARD = (
    '<div class="yt-facade" onclick="loadYT(this,\'{vid}\')" '
    'style="position:relative;cursor:pointer;border-radius:10px;overflow:hidden;'
    'border:1px solid var(--border-light);aspect-ratio:16/9;background:#000 '
    "url('https://img.youtube.com/vi/{vid}/hqdefault.jpg') center/cover;\">"
    '<div style="position:absolute;inset:0;display:flex;align-items:center;'
    'justify-content:center;background:rgba(0,0,0,0.3);">'
    '<div style="width:60px;height:42px;background:#c0392b;border-radius:10px;'
    'display:flex;align-items:center;justify-content:center;">'
    '<div style="width:0;height:0;border-left:18px solid #fff;border-top:10px '
    'solid transparent;border-bottom:10px solid transparent;margin-left:4px;">'
    '</div></div></div>'
    '<p style="position:absolute;bottom:0;left:0;right:0;padding:8px 12px;'
    'margin:0;background:rgba(0,0,0,0.7);color:#fff;font-size:0.78rem;'
    'font-weight:600;">{title}<br>'
    '<span class="yt-src" style="font-size:0.64rem;font-weight:400;'
    'opacity:0.75;">{channel}</span></p></div>'
)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lookup(vid):
    url = (f"{OEMBED}?url=" +
           urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="") +
           "&format=json")
    for _ in range(3):
        try:
            status, data = http.get_json(url, timeout=20)
        except (OSError, ValueError):
            continue
        if status == 200 and data:
            return data.get("title", "").strip(), data.get("author_name", "").strip()
        if status in (401, 404):
            sys.exit(f"{vid}: YouTube returned {status}. The video is deleted, "
                     f"private, or not embeddable, so it should not be added.")
    sys.exit(f"{vid}: could not reach YouTube after 3 attempts.")


def div_end(text, open_pos):
    """Given the index of a '<div', return the index just past its </div>."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", text[open_pos:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            return open_pos + m.end()
    raise ValueError("unbalanced <div> while scanning")


def container_region(text, section):
    """Return (start, end) of the region whose last card we append after,
    plus a human label for the shape."""
    # spiritual-disciplines style: several video-grid blocks, pick by heading
    grids = list(re.finditer(r'<div class="video-grid">', text))
    if grids:
        if not section:
            heads = re.findall(r"<h2[^>]*>(.*?)</h2>", text, re.S)
            heads = [re.sub(r"<[^>]+>", "", h).strip() for h in heads]
            sys.exit("This page has several video sections. Re-run with "
                     "--section and one of: "
                     + ", ".join(repr(h) for h in heads if h))
        # find the h2 whose following text contains the grid
        for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", text, re.S):
            name = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if name.lower() != section.strip().lower():
                continue
            nxt = re.search(r"<h2\b", text[m.end():])
            limit = m.end() + (nxt.start() if nxt else len(text) - m.end())
            g = re.search(r'<div class="video-grid">', text[m.end():limit])
            if not g:
                sys.exit(f"section {section!r} has no video-grid to add to")
            gs = m.end() + g.start()
            return gs, div_end(text, gs), f"video-grid under {name!r}"
        sys.exit(f"no <h2> section named {section!r} on this page")

    # chapter page
    m = re.search(r'<div class="tab-content" id="tab-videos">', text)
    if m:
        return m.start(), div_end(text, m.start()), "chapter Videos tab"

    # life-study page
    m = re.search(r'<div class="section-block">\s*<h2>Video Resources</h2>', text)
    if m:
        return m.start(), div_end(text, m.start()), "Video Resources block"

    sys.exit("could not find a video container on this page")


def main():
    argv = sys.argv[1:]
    check = "--check" in argv
    section = None
    if "--section" in argv:
        i = argv.index("--section")
        try:
            section = argv[i + 1]
        except IndexError:
            sys.exit("--section needs a heading")
        del argv[i:i + 2]
    argv = [a for a in argv if not a.startswith("--")]
    if len(argv) != 2:
        sys.exit(__doc__)

    page, vid = argv
    path = page if os.path.isabs(page) else os.path.join(DOCS, page)
    if not os.path.isfile(path):
        sys.exit(f"no such page: {path}")

    text = open(path, encoding="utf-8").read()
    if f"loadYT(this,'{vid}')" in text:
        print(f"  {os.path.basename(path)}: {vid} is already on this page, skipping")
        return 0

    title, channel = lookup(vid)
    start, end, shape = container_region(text, section)

    # append after the last existing card in the region, or right after the
    # container's heading if there are none yet
    region = text[start:end]
    cards = list(re.finditer(r'<div class="yt-facade"', region))
    if cards:
        last = cards[-1].start()
        insert_at = start + div_end(region, last)
        indent = "\n                "
    else:
        h = re.search(r"</h[23]>", region)
        insert_at = start + (h.end() if h else len(region) - len("</div>"))
        indent = "\n                "

    card = CARD.format(vid=vid, title=esc(title), channel=esc(channel))
    new = text[:insert_at] + indent + card + text[insert_at:]

    print(f"  {os.path.basename(path)}: + {title}")
    print(f"      channel {channel} | id {vid} | into {shape}")
    if check:
        print("      --check, not written")
        return 0

    open(path, "w", encoding="utf-8").write(new)

    after = open(path, encoding="utf-8").read()
    o, c = len(re.findall(r"<div\b", after)), len(re.findall(r"</div>", after))
    if o != c:
        sys.exit(f"      ABORT: div balance broken ({o} open vs {c} close). "
                 f"Restore with: git checkout -- docs/{os.path.basename(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
