#!/usr/bin/env python3
"""
Applies whichever numbered items a person approved on a suggest_placements.py
issue, then reports what happened. This is the only script in this pipeline
that writes to docs/ or article_sources.py, and it only runs from a reply on
an issue the "Apply approved placements" workflow already gated to the repo
owner -- see WORKFLOW.md for the full approve-by-number flow.

Reads two environment variables (never args, so their content is never
interpolated into a shell command -- see the workflow's own comment on why):
    ISSUE_BODY     the issue body written by suggest_placements.py, containing
                    a PLACEMENT_JSON HTML comment
    COMMENT_BODY    the reply being acted on

Writes a result to $GITHUB_OUTPUT (if set) plus a plain-text summary to
/tmp/apply_result.md, for the workflow to post back as a comment. Exits 0
whether or not anything was approved -- "no recognisable approval" and
"nothing left to approve" are both normal outcomes, not failures. A per-item
apply failure (a deleted video, a page that no longer parses) is reported in
the summary and does not abort the rest of the batch.

Usage (local testing):
    ISSUE_BODY="$(cat body.md)" COMMENT_BODY="approve: 1,3" python3 apply_approved.py [--check]
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULT_PATH = "/tmp/apply_result.md"

FENCE_OPEN = "# AUTO_FENCE_OPEN"
FENCE_CLOSE = "# AUTO_FENCE_CLOSE"


def extract_placement_json(issue_body):
    m = re.search(r"<!-- PLACEMENT_JSON\n(.*?)\n-->", issue_body, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def parse_approved_numbers(comment_body, valid_max):
    """Returns a sorted list of approved indices, or None if the comment does
    not look like an approval at all (a plain discussion comment on the issue,
    which must be left alone rather than acted on)."""
    text = comment_body.strip()
    low = text.lower()

    if re.search(r"\bapprove\s*:?\s*all\b", low):
        return list(range(1, valid_max + 1))
    if re.search(r"\bapprove\s*:?\s*none\b", low) or low in ("skip", "none"):
        return []

    m = re.search(r"\bapprove\b\s*:?\s*(.+)", low, re.S)
    if m:
        nums = re.findall(r"\d+", m.group(1))
        if nums:
            return sorted({int(n) for n in nums if 1 <= int(n) <= valid_max})

    # A bare list of numbers with nothing else on the line, e.g. "1, 3, 5".
    if re.fullmatch(r"[\d,\s]+", text) and re.search(r"\d", text):
        nums = re.findall(r"\d+", text)
        return sorted({int(n) for n in nums if 1 <= int(n) <= valid_max})

    return None


def apply_video(item, suggestion, check):
    page = suggestion["target"]
    vid = item["id"]
    cmd = [sys.executable, os.path.join(ROOT, "add_video.py"), page, vid]
    if check:
        cmd.append("--check")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    ok = r.returncode == 0
    detail = (r.stdout + r.stderr).strip().splitlines()
    detail = detail[-1] if detail else ("added" if ok else "failed")
    return ok, f"{page}: {detail}"


def rewrite_auto_block(new_chapter, new_topic):
    """Rewrites the AUTO_CHAPTER_ARTICLES / AUTO_TOPIC_ARTICLES block in
    article_sources.py between its fence comments, from the two dicts passed
    in. This is the only place that ever writes inside the fences, so it is
    always a full, deterministic regeneration -- never a text-splice into
    hand-authored content."""
    path = os.path.join(ROOT, "article_sources.py")
    with open(path, encoding="utf-8") as f:
        text = f.read()

    start = text.index(FENCE_OPEN)
    end = text.index(FENCE_CLOSE) + len(FENCE_CLOSE)

    def render_entries(entries):
        out = []
        for source, url, note in entries:
            out.append(f"        ({source!r}, {url!r}, {note!r}),")
        return "\n".join(out)

    lines = [FENCE_OPEN, "AUTO_CHAPTER_ARTICLES = {"]
    for (slug, ch), entries in sorted(new_chapter.items()):
        lines.append(f"    ({slug!r}, {ch}): [")
        lines.append(render_entries(entries))
        lines.append("    ],")
    lines.append("}")
    lines.append("")
    lines.append("AUTO_TOPIC_ARTICLES = {")
    for page, entries in sorted(new_topic.items()):
        lines.append(f"    {page!r}: [")
        lines.append(render_entries(entries))
        lines.append("    ],")
    lines.append("}")
    lines.append("")
    lines.append("for _key, _entries in AUTO_CHAPTER_ARTICLES.items():")
    lines.append("    CHAPTER_ARTICLES[_key] = list(CHAPTER_ARTICLES.get(_key, [])) + list(_entries)")
    lines.append("for _key, _entries in AUTO_TOPIC_ARTICLES.items():")
    lines.append("    TOPIC_ARTICLES[_key] = list(TOPIC_ARTICLES.get(_key, [])) + list(_entries)")
    lines.append(FENCE_CLOSE)

    new_text = text[:start] + "\n".join(lines) + text[end:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)


def load_current_auto():
    """Re-imports article_sources fresh (a subprocess, so stale bytecode from
    an already-imported copy is never a risk) to read back the AUTO_* dicts
    exactly as Python parses them, rather than re-parsing our own rendered
    text -- the two must never be allowed to disagree."""
    r = subprocess.run(
        [sys.executable, "-c",
         "import article_sources as a, json, sys; "
         "json.dump({'chapter': [[list(k), v] for k, v in a.AUTO_CHAPTER_ARTICLES.items()], "
         "'topic': list(a.AUTO_TOPIC_ARTICLES.items())}, sys.stdout)"],
        capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"could not read current AUTO_* state: {r.stderr}")
    data = json.loads(r.stdout)
    chapter = {tuple(k): [tuple(e) for e in v] for k, v in data["chapter"]}
    topic = {k: [tuple(e) for e in v] for k, v in data["topic"]}
    return chapter, topic


def apply_article(item, suggestion, pending_chapter, pending_topic):
    import article_sources as asrc
    source = asrc.source_of(item["url"])
    if not source:
        return False, f"{item['url']}: not from an allowed source, skipped"
    note = suggestion.get("note") or ""
    if not note.strip():
        return False, f"{item['url']}: no draft note, skipped"
    entry = (source, item["url"], note.strip())

    if suggestion["target_type"] == "chapter":
        # Non-greedy on purpose -- matches CHAPTER in add_articles.py. A greedy
        # \d+ would parse "matthew12.html" as slug "matthew1" chapter 2.
        m = re.match(r"^([a-z0-9]+?)(\d+)\.html$", suggestion["target"])
        if not m:
            return False, f"{item['url']}: bad chapter target {suggestion['target']!r}"
        key = (m.group(1), int(m.group(2)))
        pending_chapter.setdefault(key, []).append(entry)
        return True, f"{suggestion['target']}: + {item['url']}"
    if suggestion["target_type"] == "topic":
        key = suggestion["target"]
        pending_topic.setdefault(key, []).append(entry)
        return True, f"{key}: + {item['url']}"
    return False, f"{item['url']}: no target, skipped"


def main():
    check = "--check" in sys.argv
    issue_body = os.environ.get("ISSUE_BODY", "")
    comment_body = os.environ.get("COMMENT_BODY", "")

    payload = extract_placement_json(issue_body)
    if not payload:
        print("no PLACEMENT_JSON in issue body, nothing to do")
        _write_output(acted="false")
        return 0

    items = payload["items"]
    suggestions = {int(k): v for k, v in payload["suggestions"].items()}

    approved = parse_approved_numbers(comment_body, len(items))
    if approved is None:
        print("comment does not look like an approval, ignoring")
        _write_output(acted="false")
        return 0
    if not approved:
        print("approval reply approved nothing")
        _write_output(acted="true", summary="No items were approved.")
        with open(RESULT_PATH, "w", encoding="utf-8") as f:
            f.write("No items were approved.\n")
        return 0

    kind = payload["kind"]
    results = []
    video_changed = False

    pending_chapter, pending_topic = ({}, {})
    if kind == "article":
        pending_chapter, pending_topic = load_current_auto()

    for i in approved:
        item = items[i - 1]
        s = suggestions.get(i)
        if not s or s.get("target_type") == "none" or not s.get("target"):
            results.append((i, False, "no suggested target -- place manually"))
            continue
        if kind == "video":
            ok, detail = apply_video(item, s, check)
            video_changed = video_changed or ok
        else:
            ok, detail = apply_article(item, s, pending_chapter, pending_topic)
        results.append((i, ok, detail))

    if kind == "article" and not check:
        any_new = any(ok for _, ok, _ in results)
        if any_new:
            rewrite_auto_block(pending_chapter, pending_topic)
            r = subprocess.run([sys.executable, os.path.join(ROOT, "add_articles.py")],
                              capture_output=True, text=True, cwd=ROOT)
            if r.returncode != 0:
                # Roll back: article_sources.py's own state is the only thing
                # this branch wrote, and add_articles.py never writes docs/ on
                # a problem, so reverting the source file is a clean undo.
                subprocess.run(["git", "checkout", "--", "article_sources.py"], cwd=ROOT)
                results.append((0, False, f"add_articles.py failed, rolled back: "
                                          f"{(r.stdout + r.stderr).strip()[-300:]}"))

    lines = [f"**{sum(1 for _, ok, _ in results if ok)}** of {len(approved)} "
             f"approved item(s) applied." + (" (--check, nothing written)" if check else ""),
             ""]
    for i, ok, detail in results:
        mark = "✅" if ok else "❌"
        prefix = f"{i}. " if i else ""
        lines.append(f"{mark} {prefix}{detail}")
    summary = "\n".join(lines)

    print(summary)
    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        f.write(summary + "\n")

    any_change = video_changed or (kind == "article" and any(ok for _, ok, _ in results))
    _write_output(acted="true", changed=str(any_change).lower())
    return 0


def _write_output(**kv):
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if not gh_output:
        return
    with open(gh_output, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


if __name__ == "__main__":
    sys.exit(main())
