#!/usr/bin/env python3
"""
Puts a map and a set of place write-ups into every Map & Geography pane.

    python3 add_mapgeo_maps.py            # rewrite the panes
    python3 add_mapgeo_maps.py --check    # report, change nothing

What each pane gains
--------------------
1. A locator map above the existing notes, drawn by docs/site/mapgeo.js from the
   place keys in `data-places`.
2. A "Places on this map" list under them: for each place, where it is now and a
   couple of sentences of context.

What it loses
-------------
The Wikipedia links in the prose. Those became anchors to the write-up on the
same page, so a reader who wants to know where Nineveh is gets the map and the
note instead of being sent to another site. The Wikipedia article is still one
click away, from the write-up, where it belongs as a source rather than as the
answer.

Run order
---------
    python3 build_mapgeo.py       # first, it decides which places ship
    python3 add_mapgeo_maps.py    # then this, it stamps that file's hash

Safe to run repeatedly. Everything this adds is fenced between the geo-notes
comments or lives in the map div, and both are stripped before the pane is read,
so a second run sees the pane it saw the first time and produces the same bytes.
"""
import hashlib
import html
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import mapgeo_places as mp  # noqa: E402

DOCS = os.path.join(BASE_DIR, "docs")
ASSET = os.path.join(DOCS, "site", "mapgeo.js")

PANE = re.compile(
    r'(<div class="tab-content" id="tab-mapgeo">)(.*?)(\n            </div>)', re.S)
HEADING = "<h3>Map &amp; Geography</h3>"
HEADING_RAW = "<h3>Map & Geography</h3>"

WIKI_LINK = re.compile(r'<a href="https://en\.wikipedia\.org/wiki/([^"]+)"[^>]*>(.*?)</a>')
SCRIPT_TAG = re.compile(r'[ \t]*<script src="site/mapgeo\.js(?:\?v=[^"]*)?"></script>\n?')
SCRIPT_ANCHOR = re.compile(r'(<script src="site/script\.js(?:\?v=[^"]*)?"></script>\n)')

IND = " " * 16


def asset_version():
    if not os.path.isfile(ASSET):
        sys.exit("docs/site/mapgeo.js is missing; run build_mapgeo.py first")
    h = hashlib.sha256(open(ASSET, "rb").read()).hexdigest()[:8]
    return h


def strip_ours(pane):
    """The pane as it was before this script ever touched it, apart from the
    prose links, which are rewritten in place and read back by find_places.
    Shared with build_mapgeo.py so the two cannot disagree about what a pane
    says."""
    return mp.pane_source(pane)


def esc(text):
    return html.escape(text, quote=False)


def note_item(key):
    p = mp.PLACES[key]
    bits = [f'<span class="geo-name">{esc(p["name"])}</span>']
    if p["modern"]:
        bits.append(f'<span class="geo-where">{esc(p["modern"])}</span>')
    more = (f'<a class="geo-more" href="https://en.wikipedia.org/wiki/{p["wiki"]}"'
            f' target="_blank" rel="noopener">Wikipedia</a>')
    bits.append(f'<span class="geo-note">{esc(p["note"])} {more}</span>')
    return (f'{IND}    <li id="geo-note-{key}" data-place="{key}">'
            + "".join(bits) + "</li>")


def notes_block(keys):
    lines = [f"{IND}<!-- geo-notes -->",
             f'{IND}<h4 class="geo-heading">Places on this map</h4>',
             f'{IND}<ul class="geo-notes">']
    lines += [note_item(k) for k in keys]
    lines += [f"{IND}</ul>",
              f'{IND}<p class="geo-credit">Towns sit on their excavated or '
              f"traditional site. Regions, rivers and seas are ringed rather "
              f"than dotted, because for those a single point is only an "
              f"anchor. Coastlines from Natural Earth.</p>",
              f"{IND}<!-- /geo-notes -->"]
    return "\n".join(lines)


def relink(pane, keys):
    """Turn the Wikipedia links in the prose into anchors to the write-ups.
    A link whose place did not make it into the gazetteer is left alone rather
    than pointed at a note that does not exist."""
    w2k = mp.wiki_to_key()

    def swap(m):
        key = w2k.get(m.group(1))
        if not key or key not in keys:
            return m.group(0)
        return f'<a class="geo-ref" href="#geo-note-{key}">{m.group(2)}</a>'

    return WIKI_LINK.sub(swap, pane)


def rewrite_pane(pane):
    """Returns the new pane body and the keys it uses."""
    bare = strip_ours(pane)
    keys = mp.find_places(bare)
    if not keys:
        # Genesis 3 to 9 and the wilderness legislation in Numbers name nothing
        # that can be put on a map. A map of nowhere is worse than no map.
        return bare, []

    body = relink(bare, keys)
    heading = HEADING if HEADING in body else HEADING_RAW
    if heading not in body:
        return None, keys
    body = body.replace(
        heading,
        f'{heading}\n{IND}<div class="geo-map" data-places="{",".join(keys)}"></div>',
        1)
    return body + "\n" + notes_block(keys), keys


def add_script(text, version):
    """One script tag, after the site's own, with the asset's hash so a rebuilt
    map is never served from a stale cache."""
    tag = f'    <script src="site/mapgeo.js?v={version}"></script>\n'
    text = SCRIPT_TAG.sub("", text)
    if not SCRIPT_ANCHOR.search(text):
        return text
    return SCRIPT_ANCHOR.sub(lambda m: m.group(1) + tag, text, count=1)


def main():
    check = "--check" in sys.argv
    version = asset_version()

    touched = 0
    mapped = 0
    skipped = []
    unlinked = 0
    pins = 0
    failures = []

    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        original = open(path, encoding="utf-8").read()
        found = PANE.search(original)
        if not found:
            continue

        body, keys = rewrite_pane(found.group(2))
        if body is None:
            failures.append(f"{name}: could not find the Map & Geography heading")
            continue

        text = original[:found.start()] + found.group(1) + body + found.group(3) \
            + original[found.end():]
        if keys:
            mapped += 1
            pins += len(keys)
            text = add_script(text, version)
        else:
            skipped.append(name)
            text = SCRIPT_TAG.sub("", text)

        left = len(WIKI_LINK.findall(body))
        unlinked += left

        if text != original:
            touched += 1
            if not check:
                open(path, "w", encoding="utf-8").write(text)

    print(f"  asset version    {version}")
    print(f"  panes with a map {mapped}")
    print(f"  panes skipped    {len(skipped)} "
          f"({', '.join(n[:-5] for n in skipped)})")
    print(f"  pins placed      {pins}")
    print(f"  wikipedia links  {unlinked} left in prose"
          f"{' (each one is a place the gazetteer does not have)' if unlinked else ''}")
    print(f"  files {'to change' if check else 'changed'}      {touched}")
    for line in failures:
        print(f"  PROBLEM {line}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
