#!/usr/bin/env python3
"""
Enforces the allowed video sources on this repo, and strips YouTube Shorts.

Run in bible-study. New River gets the same treatment automatically, with its
own tighter list, as a step inside sync_from_bible_study.py.

Three things happen, in this order:

  relabel   Some players were captioned inconsistently for the same channel:
            "David Guzik Devotionals" and "David Guzik / Enduring Word" are both
            Guzik, and one page had the Knechtle ampersand HTML-escaped. These
            are rewritten to the canonical label first, so the filter does not
            delete videos from channels that are actually allowed.

  filter    Players whose channel is not in the allow list are removed, along
            with any video id passed via --drop-shorts.

  tidy      If a chapter ends up with no players at all, the Videos tab is
            removed rather than left as an empty pane.

Usage:
    python3 filter_videos.py [--check] [--drop-shorts shorts_scan.json]

The Shorts file is the output of scan_shorts.py. Only ids it recorded as a
definite Short are dropped; anything it could not determine is left alone.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import video_sources as vs  # noqa: E402

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def main():
    check = "--check" in sys.argv
    drop_ids = set()
    if "--drop-shorts" in sys.argv:
        path = sys.argv[sys.argv.index("--drop-shorts") + 1]
        data = json.load(open(path))
        drop_ids = set(data.get("shorts", {}))
        print(f"Shorts to drop: {len(drop_ids)} "
              f"(from {data.get('scanned')} scanned; "
              f"{len(data.get('unknown', {}))} undetermined and left alone)")

    total_removed = total_relabelled = tabs_dropped = files = 0
    per_channel = {}

    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        original = open(path, encoding="utf-8").read()

        # record what is about to go, for the report
        for _, _, vid, label in vs.players(original):
            if label not in vs.BIBLE_STUDY_ALLOW or (vid and vid in drop_ids):
                key = label if label not in vs.BIBLE_STUDY_ALLOW \
                    else f"{label} (Short)"
                per_channel[key] = per_channel.get(key, 0) + 1

        text, removed, relabelled = vs.apply_filter(
            original, vs.BIBLE_STUDY_ALLOW, drop_ids)
        text, dropped_tab = vs.strip_empty_videos_tab(text)

        o, c = len(re.findall(r"<div\b", text)), len(re.findall(r"</div>", text))
        if o != c:
            print(f"  SKIPPED {name}: would unbalance divs ({o} vs {c})")
            continue

        if text != original:
            files += 1
            total_removed += removed
            total_relabelled += relabelled
            tabs_dropped += 1 if dropped_tab else 0
            if not check:
                open(path, "w", encoding="utf-8").write(text)

    verb = "would change" if check else "changed"
    print(f"\n{verb} {files} pages")
    print(f"  players removed        : {total_removed}")
    print(f"  labels corrected       : {total_relabelled}")
    print(f"  empty Videos tabs tidied: {tabs_dropped}")
    print("\n  removed by source:")
    for k, v in sorted(per_channel.items(), key=lambda x: -x[1]):
        print(f"    {k[:54]:56}{v:>5}")


if __name__ == "__main__":
    main()
