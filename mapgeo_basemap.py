#!/usr/bin/env python3
"""
Turns Natural Earth vector data into the compact basemap that
`docs/site/mapgeo.js` draws behind the Map & Geography pins.

Natural Earth is public domain, so the output can be committed and served
directly. That is the whole point of doing it this way: the alternative was a
tile service, which would mean an API key, a usage policy, and a map that goes
blank when the site is used offline through its service worker.

Run this only when the frame or the level of detail needs to change:

    python3 mapgeo_basemap.py            # fetch (cached) and rebuild
    python3 mapgeo_basemap.py --stats    # report sizes, write nothing

Output is a dict of layer -> list of encoded paths, consumed by build_mapgeo.py.

Encoding
--------
Coordinates are Web Mercator degrees, quantised to 1/500 of a degree (~220 m,
which is under half a pixel at the tightest zoom the renderer allows), delta
encoded against the previous point, then written as base-32 varints in a
URL-safe alphabet. Plain JSON of the same geometry is 260 KB; this is 52 KB,
and the decoder is a dozen lines in mapgeo.js.
"""
import json
import math
import os
import sys
import urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".ne-cache")
NE_BASE = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector"
           "/master/geojson")
LAYERS = {
    "land": "ne_10m_land",
    "lakes": "ne_10m_lakes",
    "rivers": "ne_10m_rivers_lake_centerlines",
}

# The frame has to hold every pin in mapgeo_places.py, which is why it reaches
# as far as Tartessos in south-west Spain (Tarshish, Jonah 1:3), Persepolis in
# the east, and Sheba in the south. Nothing outside it is ever drawn.
LON0, LON1, LAT0, LAT1 = -11.0, 56.0, 11.0, 48.0

# Detail is spent where the maps actually zoom in. A Jerusalem-and-Bethlehem
# view is about 3 degrees across and a Mediterranean voyage view is 60, so one
# tolerance for the whole frame either flattens the Jordan valley into a
# straight line or spends most of the file on Aegean islands.
CORE = (29.0, 42.0, 25.0, 40.0)
TOL_CORE = 0.0015
TOL_WIDE = 0.02

QUANT = 500  # coordinate units per degree
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def merc_y(lat):
    lat = max(-85.0, min(85.0, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


Y0, Y1 = merc_y(LAT0), merc_y(LAT1)
CY0, CY1 = merc_y(CORE[2]), merc_y(CORE[3])


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name + ".geojson")
    if not os.path.isfile(path):
        url = f"{NE_BASE}/{name}.geojson"
        sys.stderr.write(f"fetching {url}\n")
        with urllib.request.urlopen(url, timeout=120) as r, open(path, "wb") as f:
            f.write(r.read())
    return json.load(open(path, encoding="utf-8"))


def project(coords):
    return [(x, merc_y(y)) for x, y in coords]


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def touches_core(pts):
    x0, y0, x1, y1 = bbox(pts)
    return not (x1 < CORE[0] or x0 > CORE[1] or y1 < CY0 or y0 > CY1)


def clip_polygon(ring):
    """Sutherland-Hodgman against the frame. The frame is a rectangle, so a
    convex-window algorithm is enough, and the seams it leaves along the edge
    are invisible under a nonzero fill."""
    def ix(a, b, x):
        t = (x - a[0]) / (b[0] - a[0])
        return (x, a[1] + t * (b[1] - a[1]))

    def iy(a, b, y):
        t = (y - a[1]) / (b[1] - a[1])
        return (a[0] + t * (b[0] - a[0]), y)

    edges = (
        (lambda p: p[0] >= LON0, lambda a, b: ix(a, b, LON0)),
        (lambda p: p[0] <= LON1, lambda a, b: ix(a, b, LON1)),
        (lambda p: p[1] >= Y0, lambda a, b: iy(a, b, Y0)),
        (lambda p: p[1] <= Y1, lambda a, b: iy(a, b, Y1)),
    )
    pts = ring
    for keep, isect in edges:
        if not pts:
            return []
        out = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            ka, kb = keep(a), keep(b)
            if ka:
                out.append(a)
                if not kb:
                    out.append(isect(a, b))
            elif kb:
                out.append(isect(a, b))
        pts = out
    return pts


def clip_line(pts):
    """Split a polyline into the runs that fall inside the frame, keeping the
    first point beyond each end so rivers meet the edge instead of stopping
    just short of it."""
    def inside(p):
        return LON0 <= p[0] <= LON1 and Y0 <= p[1] <= Y1

    runs, cur = [], []
    for i, p in enumerate(pts):
        if inside(p):
            if not cur and i:
                cur.append(pts[i - 1])
            cur.append(p)
        elif cur:
            cur.append(p)
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) > 1]


def simplify(pts, tol):
    """Douglas-Peucker, iterative. Recursion overflows on the 90,000-point
    Africa ring."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        ax, ay = pts[i]
        dx, dy = pts[j][0] - ax, pts[j][1] - ay
        norm = math.hypot(dx, dy)
        far, at = -1.0, -1
        for k in range(i + 1, j):
            px, py = pts[k]
            if norm:
                d = abs(dy * (px - ax) - dx * (py - ay)) / norm
            else:
                d = math.hypot(px - ax, py - ay)
            if d > far:
                far, at = d, k
        if far > tol:
            keep[at] = True
            stack.append((i, at))
            stack.append((at, j))
    return [p for p, k in zip(pts, keep) if k]


def varint(n):
    """Zig-zag then base-32, high bit of each digit means 'more to come'."""
    n = (-n * 2 - 1) if n < 0 else n * 2
    out = []
    while True:
        digit = n & 31
        n >>= 5
        out.append(ALPHA[digit + 32] if n else ALPHA[digit])
        if not n:
            return "".join(out)


def encode(pts):
    """Quantise, flip y for SVG, delta encode. Returns None if the path
    collapses to fewer than two distinct points."""
    out = []
    px = py = 0
    for x, y in pts:
        qx, qy = round(x * QUANT), round(-y * QUANT)
        if out and (qx, qy) == (px, py):
            continue
        out.append(varint(qx - px))
        out.append(varint(qy - py))
        px, py = qx, qy
    return "".join(out) if len(out) >= 4 else None


def polygons(name, min_extent):
    paths = []
    for feat in fetch(name)["features"]:
        geom = feat["geometry"]
        polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
                 else geom["coordinates"] if geom["type"] == "MultiPolygon" else [])
        for poly in polys:
            for ring in poly:
                pr = project(ring)
                x0, y0, x1, y1 = bbox(pr)
                if x1 < LON0 or x0 > LON1 or y1 < Y0 or y0 > Y1:
                    continue
                # Drop specks. At the widest view an islet this small is a
                # single pixel of noise; at the tightest it is off frame.
                if (x1 - x0) * (y1 - y0) < min_extent:
                    continue
                clipped = clip_polygon(pr)
                if len(clipped) < 3:
                    continue
                tol = TOL_CORE if touches_core(clipped) else TOL_WIDE
                d = encode(simplify(clipped + [clipped[0]], tol))
                if d:
                    paths.append(d)
    return paths


def lines(name, keep=None):
    paths = []
    for feat in fetch(name)["features"]:
        if keep and not keep(feat["properties"]):
            continue
        geom = feat["geometry"]
        segs = ([geom["coordinates"]] if geom["type"] == "LineString"
                else geom["coordinates"] if geom["type"] == "MultiLineString" else [])
        for seg in segs:
            for run in clip_line(project(seg)):
                tol = TOL_CORE if touches_core(run) else TOL_WIDE
                d = encode(simplify(run, tol))
                if d:
                    paths.append(d)
    return paths


def build():
    return {
        "land": polygons(LAYERS["land"], 0.004),
        "lakes": polygons(LAYERS["lakes"], 0.0015),
        # scalerank 7 and below is the Nile, Euphrates, Tigris, Jordan and
        # their peers. Above that the Levant disappears under wadis.
        "rivers": lines(LAYERS["rivers"],
                        lambda p: (p.get("scalerank") or 99) <= 7),
    }


def frame():
    return {"lon0": LON0, "lon1": LON1, "y0": -Y1, "y1": -Y0, "q": QUANT}


if __name__ == "__main__":
    data = build()
    blob = json.dumps(data, separators=(",", ":"))
    for layer, paths in data.items():
        print(f"  {layer:8} {len(paths):5} paths  "
              f"{sum(len(p) for p in paths):7} chars")
    print(f"  {'total':8} {len(blob):7} bytes of JSON")
    if "--stats" not in sys.argv:
        out = os.path.join(CACHE, "basemap.json")
        open(out, "w").write(blob)
        print(f"  wrote {out}")
