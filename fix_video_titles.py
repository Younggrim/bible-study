#!/usr/bin/env python3
"""
One-time repair for video titles corrupted by a bad encoding round-trip.

Roughly 173 video captions across 132 chapter pages contain U+FFFD, the Unicode
replacement character, where an en-dash or curly apostrophe belongs:

    1 Corinthians 1:1-17 <?> The Foolishness of Division

Rather than guessing which character was lost, this asks YouTube for the current
title through the oEmbed endpoint and uses that. If a video no longer resolves,
its caption is left exactly as it is and reported, so a dead video never gets
silently rewritten.

Run this in bible-study, then sync into bible-study-newriver. Running it
directly against New River would work but the next sync would discard the
result.

Usage:
    python3 fix_video_titles.py [--check] [--workers N]

--check reports what would change and writes nothing.
"""
import html
import os
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import automation_http as http  # noqa: E402

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE_DIR, "docs")
OEMBED = "https://www.youtube.com/oembed"
BAD = "\ufffd"

# The caption sits immediately after the play-button markup for a given video.
FACADE = re.compile(
    r"(loadYT\(this,'([A-Za-z0-9_-]{6,})'.{0,1400}?font-weight:600;\">)(.*?)(<br>)",
    re.S)


def live_title(vid):
    url = (f"{OEMBED}?url=" +
           urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="") +
           "&format=json")
    for _ in range(3):
        try:
            status, data = http.get_json(url, timeout=20)
        except (OSError, ValueError):
            continue
        if status == 200 and data and data.get("title"):
            return data["title"].strip()
        if status in (401, 404):
            return None
    return None


def escape(title):
    """Escape only what must be escaped in HTML text content. The files are
    UTF-8, so dashes and quotes stay as themselves."""
    return title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    check = "--check" in sys.argv
    workers = 8
    if "--workers" in sys.argv:
        try:
            workers = int(sys.argv[sys.argv.index("--workers") + 1])
        except (IndexError, ValueError):
            sys.exit("--workers needs an integer")

    if not os.path.isdir(DOCS):
        sys.exit(f"no docs/ directory at {DOCS}")

    # Find every video whose on-page caption is corrupted.
    broken = {}
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        text = open(os.path.join(DOCS, name), encoding="utf-8").read()
        for _, vid, title, _ in FACADE.findall(text):
            if BAD in html.unescape(re.sub(r"<[^>]+>", "", title)):
                broken.setdefault(vid, set()).add(name)

    if not broken:
        print("No corrupted video titles found.")
        return 0

    print(f"{len(broken)} video(s) with corrupted captions across "
          f"{len({p for ps in broken.values() for p in ps})} page(s). "
          f"Asking YouTube for the real titles...")

    ids = sorted(broken)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        titles = dict(zip(ids, pool.map(live_title, ids)))

    resolved = {v: t for v, t in titles.items() if t}
    unresolved = [v for v, t in titles.items() if not t]
    still_bad = {v: t for v, t in resolved.items() if BAD in t}
    usable = {v: t for v, t in resolved.items() if BAD not in t}

    print(f"  resolved   {len(resolved)}")
    print(f"  unusable   {len(unresolved)} (video gone or private, left untouched)")
    if still_bad:
        print(f"  odd        {len(still_bad)} (YouTube itself returns U+FFFD, left untouched)")

    edits = 0
    files_changed = 0
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()
        local = 0

        def repl(m):
            nonlocal local
            prefix, vid, title, suffix = m.groups()
            plain = html.unescape(re.sub(r"<[^>]+>", "", title))
            if BAD not in plain or vid not in usable:
                return m.group(0)
            local += 1
            return prefix + escape(usable[vid]) + suffix

        new = FACADE.sub(repl, text)
        if local:
            edits += local
            files_changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(new)

    verb = "would fix" if check else "fixed"
    print(f"\n{verb} {edits} caption(s) in {files_changed} file(s)")

    for vid, t in list(usable.items())[:8]:
        print(f"    {vid}  ->  {t[:70]}")
    if len(usable) > 8:
        print(f"    ... {len(usable)} total")

    if unresolved:
        print(f"\n  left alone, could not resolve ({len(unresolved)}):")
        for v in unresolved:
            print(f"    {v}  on {', '.join(sorted(broken[v]))}")
        print("  These are probably deleted or private. Run check_video_links.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
