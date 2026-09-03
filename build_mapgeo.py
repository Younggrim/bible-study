#!/usr/bin/env python3
"""
Compiles docs/site/mapgeo.js, the one asset behind every Map & Geography map.

    python3 build_mapgeo.py            # rebuild the asset
    python3 build_mapgeo.py --check    # report what would change, write nothing

It puts together three sources:

    mapgeo_basemap.py    Natural Earth coastlines, lakes and rivers, clipped to
                         the biblical world and encoded
    mapgeo_places.py     the gazetteer: where each place is, and its write-up
    mapgeo.template.js   the renderer
    mapgeo.css           the styling, injected at runtime

Only the coordinates go into the JavaScript. The write-ups are baked into each
chapter's HTML by add_mapgeo_maps.py instead, so that a reader with no
JavaScript still gets the whole of the content and only loses the picture.

Places nobody mentions are left out of the asset. The gazetteer is allowed to
carry more than the panes currently use, but there is no reason to ship it.
"""
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import mapgeo_basemap as bm      # noqa: E402
import mapgeo_places as mp       # noqa: E402

OUT = os.path.join(BASE_DIR, "docs", "site", "mapgeo.js")
TEMPLATE = os.path.join(BASE_DIR, "mapgeo.template.js")
STYLES = os.path.join(BASE_DIR, "mapgeo.css")
DOCS = os.path.join(BASE_DIR, "docs")

PANE = re.compile(
    r'<div class="tab-content" id="tab-mapgeo">(.*?)\n            </div>', re.S)


def panes():
    """(filename, pane html) for every chapter that has a Map & Geography tab."""
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        text = open(os.path.join(DOCS, name), encoding="utf-8").read()
        found = PANE.search(text)
        if found:
            yield name, found.group(1)


def keys_in_use():
    """Every gazetteer key at least one pane refers to, and the per-page lists,
    computed once so the asset build and the page rewrite cannot disagree."""
    per_page = {}
    used = set()
    for name, pane in panes():
        keys = mp.find_places(pane)
        per_page[name] = keys
        used.update(keys)
    return used, per_page


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


def js_string(text):
    """A single-quoted JS literal, for dropping the stylesheet into a var."""
    return (text.replace("\\", "\\\\").replace("'", "\\'")
                .replace("\n", "\\n").replace("\r", ""))


def build():
    problems = mp.validate()
    if problems:
        for line in problems:
            sys.stderr.write(f"gazetteer problem: {line}\n")
        sys.exit("refusing to build with a broken gazetteer")

    used, per_page = keys_in_use()

    # A pane that links a place the gazetteer has lost would silently render one
    # pin fewer than the prose promises, so make that a build failure.
    w2k = mp.wiki_to_key()
    for name, pane in panes():
        for target in re.findall(
                r'href="https://en\.wikipedia\.org/wiki/([^"]+)"', pane):
            if target not in w2k:
                sys.exit(f"{name} links {target}, which no gazetteer entry claims")

    places = {}
    for key in sorted(used):
        p = mp.PLACES[key]
        places[key] = [p["name"], round(p["lat"], 4), round(p["lon"], 4), p["kind"]]

    template = open(TEMPLATE, encoding="utf-8").read()
    js = (template
          .replace("__QUANT__", str(bm.QUANT))
          .replace("__ALPHA__", bm.ALPHA)
          .replace("__FRAME__", json.dumps(_frame(), separators=(",", ":")))
          .replace("__BASE__", json.dumps(bm.build(), separators=(",", ":")))
          .replace("__PLACES__", json.dumps(places, separators=(",", ":")))
          .replace("__CSS__", js_string(minify_css(open(STYLES, encoding="utf-8").read()))))

    left = [m for m in ("__QUANT__", "__ALPHA__", "__FRAME__", "__BASE__",
                        "__PLACES__", "__CSS__") if m in js]
    if left:
        sys.exit(f"template slots not filled: {', '.join(left)}")
    return js, places, per_page


def _frame():
    f = bm.frame()
    return {"x0": round(f["lon0"], 4), "x1": round(f["lon1"], 4),
            "y0": round(f["y0"], 4), "y1": round(f["y1"], 4)}


def main():
    check = "--check" in sys.argv
    js, places, per_page = build()
    old = open(OUT, encoding="utf-8").read() if os.path.isfile(OUT) else ""

    mapped = sum(1 for k in per_page.values() if k)
    print(f"  panes            {len(per_page)}")
    print(f"  with a map       {mapped}")
    print(f"  without one      {len(per_page) - mapped} (no locatable place named)")
    print(f"  places shipped   {len(places)} of {len(mp.PLACES)} in the gazetteer")
    print(f"  asset            {len(js)} bytes"
          f"{'' if js != old else ', unchanged'}")

    if check:
        print("  --check, nothing written")
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        open(OUT, "w", encoding="utf-8").write(js)
        print(f"  wrote            {os.path.relpath(OUT, BASE_DIR)}")

    warn_if_pages_stale(js if not check else old or js)


def warn_if_pages_stale(js):
    """The pages carry ?v=<hash of this file> so a rebuilt map cannot be served
    from a stale cache. That only holds if add_mapgeo_maps.py runs afterwards,
    which is easy to forget, so say so rather than letting it ship."""
    import hashlib
    want = hashlib.sha256(js.encode("utf-8")).hexdigest()[:8]
    stamped = set()
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        stamped.update(re.findall(
            r'src="site/mapgeo\.js\?v=([0-9a-f]+)"',
            open(os.path.join(DOCS, name), encoding="utf-8").read()))
    if stamped and stamped != {want}:
        print(f"  NOTE: pages are stamped {', '.join(sorted(stamped))} but this "
              f"asset is {want}; run add_mapgeo_maps.py to catch them up")


if __name__ == "__main__":
    main()
