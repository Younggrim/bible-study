#!/usr/bin/env python3
"""
Checks the four article sources for anything published since the last run and
reports it for human review. Like check_new_videos.py, it does not guess which
chapter or topic an article belongs on, and it never edits docs/.

That split is the whole design. Detection is mechanical and belongs on a runner.
Deciding that a Crossway piece on lament belongs on Lamentations 3 rather than
Psalm 88, or that a title mentioning Mark is about Mark Dever and not the Gospel,
needs judgment. So this opens an issue and stops.

Why it does not try to place articles automatically: it was measured, and it
cannot be done from titles. Author names collide with two thirds of the New
Testament. A single week of Crossway feeds produced "John Piper on Gambling",
"Podcast: John Owen's Advice for Killing Your Sin", "3 Marks of True
Repentance", "Podcast: Answering Tough Questions About the Holy Spirit (Joel
Beeke)" and "11 Passages to Read When You Lose Your Job", every one of which a
book-name matcher scores as a hit. gotquestions.org adds "David Hume", "David
Livingstone" and "Saul of Tarsus". The only reliable signal is a chapter number
next to the book name, which is why the derived per-book links in
article_sources.py are built from a table rather than from search.

State lives in .automation/articles/article_feed_state.json, in a subdirectory
on purpose. check_new_videos.py globs .automation/*.json and expects every one
to describe YouTube channels, so a sibling file there would make it warn every
week. A subdirectory is invisible to that glob and needs no change to a file
that is not shared between the repos.

Anything filtered out is still recorded as seen, so it is evaluated once and
never raised again. Without that, an article deliberately left off the site
would come back in next week's issue.

Usage:
    python3 check_new_articles.py [--check] [--seed]

--check reports findings but writes neither state nor issue body.
--seed  records everything currently published as already seen, without
        reporting any of it. Used once, when the feature was added.
"""
import datetime
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import article_sources as asrc  # noqa: E402
import automation_http as http  # noqa: E402

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         ".automation", "articles")
STATE_PATH = os.path.join(STATE_DIR, "article_feed_state.json")
ISSUE_BODY_PATH = "/tmp/new_articles_issue_body.md"

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
TIMEOUT = 30

# Article titles arrive from the feeds with curly quotes and en-dashes. Under a C
# locale Python gives stdout an ASCII encoder, so printing the report raised
# UnicodeEncodeError after the state had already been written -- the one ordering
# where new articles get marked as seen and then never reported. Both streams are
# pinned to UTF-8 here, and main() now writes the report before it saves state.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # not a real tty, or already wrapped
        pass

# How many articles to list per source in the issue. Crossway is polled across 51
# topic feeds, so a quiet week is a handful and a busy one can be dozens. The rest
# are still recorded as seen, so nothing is lost by not listing them; an issue
# nobody reads because it is 500 lines long is the worse outcome.
MAX_LISTED_PER_SOURCE = 40


def load_state():
    if not os.path.isfile(STATE_PATH):
        return {"sources": {}, "last_checked": None}
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        print(f"WARN: unreadable state file, treating as empty: {e}",
              file=sys.stderr)
        return {"sources": {}, "last_checked": None}
    data.setdefault("sources", {})
    return data


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    state["last_checked"] = datetime.date.today().isoformat()
    # Encoding is explicit here and on the issue body because article titles
    # arrive from the feeds with curly quotes and en-dashes in them. Python's
    # text mode otherwise picks the locale's encoding, and a runner with a C
    # locale would raise UnicodeEncodeError on the first smart quote.
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def parse_rss(body):
    """(url, title) for each item. Crossway's feeds are RSS 2.0."""
    root = ET.fromstring(body)
    out = []
    for item in root.iter("item"):
        url = (item.findtext("link") or "").strip()
        title = (item.findtext("title") or "").strip()
        if url:
            out.append((url, title))
    return out


def parse_sitemap(body):
    """(url, None) for each <loc>. Titles are not in a sitemap, so the issue
    shows the slug instead; that is enough to decide whether to open it."""
    root = ET.fromstring(body)
    out = []
    for loc in root.iter(f"{SITEMAP_NS}loc"):
        if loc.text:
            out.append((loc.text.strip(), None))
    if not out:  # a sitemap served without the namespace
        for loc in root.iter("loc"):
            if loc.text:
                out.append((loc.text.strip(), None))
    return out


def fetch(url, kind):
    status, body = http.get(url, timeout=TIMEOUT)
    if status != 200:
        raise OSError(f"HTTP {status}")
    if not body.strip():
        # BibleProject answers a request with no User-Agent with 202 and an
        # empty body. automation_http always sends one, so an empty body here
        # means something else changed and is worth surfacing.
        raise OSError("empty body")
    return parse_rss(body) if kind == "rss" else parse_sitemap(body)


def slug_of(url):
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    return re.sub(r"\.html$", "", tail)


def main():
    check = "--check" in sys.argv
    seed = "--seed" in sys.argv

    state = load_state()
    found = {}
    failures = []
    skipped_on_site = []
    changed = False
    polled = 0

    for source, spec in sorted(asrc.FEEDS.items()):
        entry = state["sources"].setdefault(source, {"known_urls": []})
        known = set(entry.get("known_urls") or [])
        seen_now = {}
        ok = 0

        for feed_url in spec["urls"]:
            polled += 1
            try:
                items = fetch(feed_url, spec["kind"])
            except (ET.ParseError, OSError, ValueError) as e:
                failures.append(f"{source}: {feed_url} -- {type(e).__name__}: {e}")
                continue
            ok += 1
            for url, title in items:
                if asrc.in_scope(source, url):
                    seen_now.setdefault(url, title)

        if not ok:
            # Every feed for this source failed. Do not touch its state, or a
            # total outage would silently mark the whole catalogue as seen.
            failures.append(f"{source}: all {len(spec['urls'])} feed(s) failed, "
                            f"state left untouched")
            continue

        fresh = {u: t for u, t in seen_now.items() if u not in known}

        keep = {}
        for url, title in fresh.items():
            if asrc.already_on_site(url):
                skipped_on_site.append((source, url))
            else:
                keep[url] = title

        if fresh:
            # Everything newly seen is recorded, including what was filtered out,
            # so it is judged once and then left alone.
            entry["known_urls"] = sorted(known | set(fresh))
            changed = True
        if keep and not seed:
            found[source] = sorted(keep.items())

    total = sum(len(v) for v in found.values())
    gh_output = os.environ.get("GITHUB_OUTPUT")

    for f in failures:
        print(f"WARN: {f}", file=sys.stderr)
    if skipped_on_site:
        print(f"Skipped {len(skipped_on_site)} URL(s) already linked from the "
              f"site or on the drop list; recorded as seen.", file=sys.stderr)

    if seed:
        counts = {s: len(e.get("known_urls") or [])
                  for s, e in state["sources"].items()}
        if not check:
            save_state(state)
        verb = "would record" if check else "recorded"
        print(f"{verb} the current catalogue as seen across {polled} feed(s):")
        for s in sorted(counts):
            print(f"  {s:20} {counts[s]}")
        print("Nothing reported. Future runs will show only what is new.")
        return 1 if not any(counts.values()) else 0

    if not total:
        if changed and not check:
            save_state(state)
        print(f"No new articles. Polled {polled} feed(s) across "
              f"{len(asrc.FEEDS)} source(s).")
        if failures:
            print(f"{len(failures)} feed(s) could not be reached, see warnings "
                  f"above.")
        if gh_output and not check:
            with open(gh_output, "a", encoding="utf-8") as f:
                f.write("has_new=false\n")
        # A feed failing is worth surfacing but is not a reason to fail the run.
        return 0

    lines = [
        f"Found **{total}** article(s) across the watched sources that this repo "
        "has not seen before.",
        "",
        "Nothing has been added to the site. Each of these needs a person to "
        "decide whether it belongs on a chapter, a topical page, a life page, or "
        "nowhere. An accepted article goes into the tables in "
        "`article_sources.py`, then `python3 add_articles.py` writes it into the "
        "pages. One that is rejected goes into `DROP_ARTICLE_URLS` with a reason "
        "so it is not suggested again. See `WORKFLOW.md`.",
        "",
    ]
    for source, items in sorted(found.items()):
        lines.append(f"### {source} ({len(items)})")
        for url, title in items[:MAX_LISTED_PER_SOURCE]:
            label = title or slug_of(url).replace("-", " ")
            lines.append(f"- [{label}]({url})")
        if len(items) > MAX_LISTED_PER_SOURCE:
            lines.append(f"- ... and {len(items) - MAX_LISTED_PER_SOURCE} more, "
                         f"all recorded in the state file")
        lines.append("")
    if failures:
        lines += ["### Feeds that could not be checked", ""]
        lines += [f"- {f}" for f in failures] + [""]

    body = "\n".join(lines)

    # Report first, state last. Saving state before the issue body is written
    # means a failure in between marks these articles as seen while nobody ever
    # hears about them, and there is no way to recover the list. In the other
    # order the worst case is a duplicate report next week, which is noise rather
    # than loss. Printing comes last for the same reason.
    if not check:
        with open(ISSUE_BODY_PATH, "w", encoding="utf-8") as f:
            f.write(body)
        if gh_output:
            with open(gh_output, "a", encoding="utf-8") as f:
                f.write("has_new=true\n")
        if changed:
            save_state(state)

    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
