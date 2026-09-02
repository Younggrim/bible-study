#!/usr/bin/env python3
"""
Finds every YouTube Short referenced by the site.

Detection needs no API key. youtube.com/shorts/<id> answers the question by
itself: a genuine Short serves 200, while a normal video 303-redirects to
/watch?v=<id>. Verified in both directions before this was written.

Only a clean 200 counts as a Short and only a clean 303 counts as normal.
Anything else is retried and then recorded as unknown, never as a Short,
because a false positive here deletes a good video from the site.

Writes JSON to the path given so the result survives the process:

    {"shorts": {id: label}, "normal": [...], "unknown": {id: reason}}

Usage:
    python3 scan_shorts.py <out.json> [--workers N]
"""
import collections
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
lock = threading.Lock()


def collect():
    """id -> channel label, from every player on every page."""
    found = {}
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        t = open(os.path.join(DOCS, name), encoding="utf-8").read()
        for m in re.finditer(r"loadYT\(this,'([^']+)'", t):
            seg = t[m.end():m.end() + 1500]
            s = re.search(r'class="yt-src"[^>]*>([^<]*)</span>', seg)
            found.setdefault(m.group(1), s.group(1).strip() if s else "?")
    return found


def probe(vid):
    for attempt in range(3):
        p = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-A", UA, "-w", "%{http_code}",
             "--max-time", "25", f"https://www.youtube.com/shorts/{vid}"],
            capture_output=True, text=True)
        c = p.stdout.strip()
        if c == "200":
            return "short"
        if c == "303":
            return "normal"
        time.sleep(3 * (attempt + 1))
    return f"http {c}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    out_path = args[0]
    workers = 6
    if "--workers" in sys.argv:
        workers = int(sys.argv[sys.argv.index("--workers") + 1])

    found = collect()
    ids = sorted(found)
    print(f"scanning {len(ids)} unique video ids with {workers} workers",
          flush=True)

    shorts, normal, unknown = {}, [], {}
    done = 0

    def work(vid):
        nonlocal done
        r = probe(vid)
        with lock:
            if r == "short":
                shorts[vid] = found[vid]
            elif r == "normal":
                normal.append(vid)
            else:
                unknown[vid] = r
            done += 1
            if done % 200 == 0:
                print(f"  {done}/{len(ids)}  shorts so far: {len(shorts)}",
                      flush=True)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(work, ids))

    by_channel = collections.Counter(shorts.values())
    payload = {"scanned": len(ids), "shorts": shorts,
               "normal_count": len(normal), "unknown": unknown,
               "by_channel": dict(by_channel)}
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"\nscanned      {len(ids)}")
    print(f"SHORTS       {len(shorts)}")
    print(f"normal       {len(normal)}")
    print(f"unknown      {len(unknown)}  (not treated as Shorts)")
    print("\nshorts by channel:")
    for lbl, c in by_channel.most_common():
        print(f"  {c:>4}  {lbl}")
    print(f"\nwritten to {out_path}")


if __name__ == "__main__":
    main()
