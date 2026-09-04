#!/usr/bin/env python3
"""
Drafts a placement suggestion for each newly found video or article, and
rewrites the issue body check_new_videos.py / check_new_articles.py already
wrote into a numbered list a human can approve by number.

This does NOT write anything to docs/. It only suggests. The suggestion is
one Claude API call (Haiku 4.5, billed on its own key -- see ANTHROPIC_API_KEY
below, never the Claude.ai session this repo is otherwise edited from) that
reads each item's title (and, for articles, page-derived context) and proposes
a target page, or "none" when nothing in the title supports a confident guess.
That mirrors the caution article_sources.py's own docstring insists on: a
title alone is not enough to place an article by book-name matching, so the
model is instructed the same way a person would be -- prefer "none" over a
guess, and never invent a chapter number a title doesn't support.

The numbered list plus a machine-readable copy of every item and its
suggestion is embedded in the issue body as a hidden HTML comment
(PLACEMENT_JSON). apply_approved.py reads that back out when a reply approves
some of the numbers, so nothing has to be re-fetched or re-guessed between the
two workflow runs -- the issue itself is the full state.

Usage:
    python3 suggest_placements.py --kind video --items PATH --issue-body PATH
    python3 suggest_placements.py --kind article --items PATH --issue-body PATH

Both --items and --issue-body are read AND overwritten in place: --items is
the JSON check_new_videos.py/check_new_articles.py wrote via their own
--json-out, --issue-body is the markdown issue body they wrote, which this
script replaces with the numbered, suggestion-annotated version.

Requires ANTHROPIC_API_KEY in the environment. If it is unset, or the API
call fails for any reason, this script leaves the original issue body
untouched and exits 0 -- a missing suggestion is a smaller problem than a
detection week silently going unreported because a suggestion step broke.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
MODEL = "claude-haiku-4-5"


def book_chapter_counts():
    """{book_slug: max_chapter}, derived from docs/*.html so it can never drift
    from what pages actually exist."""
    import re
    pat = re.compile(r"^([a-z0-9]+?)(\d+)\.html$")
    counts = {}
    for name in os.listdir(DOCS):
        m = pat.match(name)
        if m:
            slug, ch = m.group(1), int(m.group(2))
            counts[slug] = max(counts.get(slug, 0), ch)
    return counts


def topic_pages():
    import article_sources as asrc
    return sorted(asrc.TOPIC_ARTICLES.keys())


def build_reference_block(kind):
    counts = book_chapter_counts()
    books = ", ".join(f"{slug}(1-{n})" for slug, n in sorted(counts.items()))
    lines = [
        "Valid chapter targets are book-slug + chapter number, ONLY from this "
        "list (book(max chapter)): " + books + ".",
    ]
    if kind == "article":
        pages = ", ".join(topic_pages())
        lines.append(
            "Valid topic-page targets, for an article about a life struggle or "
            "a cross-book theme rather than one specific passage: " + pages + ".")
    return "\n".join(lines)


def build_prompt(kind, items):
    numbered = "\n".join(
        f"{i}. " + (f"[{it.get('channel') or it.get('source')}] {it['title']}"
                    + (f" ({it['url']})" if it.get("url") else ""))
        for i, it in enumerate(items, 1)
    )
    if kind == "video":
        task = (
            "Each item is a YouTube video title from a channel this Bible study "
            "site already tracks. For each, suggest which single chapter page it "
            "most likely belongs on, based ONLY on what the title itself names -- "
            "a specific book and chapter, or a clear verse range. Do not guess a "
            "chapter from a general topic; if the title does not name a specific "
            "passage, use target_type \"none\"."
        )
    else:
        task = (
            "Each item is an article title (and URL) from a source this Bible "
            "study site already allows. For each, suggest either the single "
            "chapter page it is about, or one topic page if it is about a life "
            "struggle or cross-book theme, based ONLY on what the title itself "
            "supports. Do NOT match on an author's name or an incidental word "
            "that happens to match a book name -- 'John Piper on Gambling' is "
            "not about the Gospel of John, 'David Hume' is not about King David, "
            "'11 Passages to Read When You Lose Your Job' names no chapter. When "
            "in real doubt, use target_type \"none\": a wrong guess a person "
            "rubber-stamps is worse than no guess. When you do suggest a target, "
            "also write a one-sentence, third-person, present-tense `note` "
            "describing what the article covers and why a reader on that page "
            "would want it -- matching the style of an editorial blurb, not a "
            "summary of the title."
        )
    return (
        f"{task}\n\n{build_reference_block(kind)}\n\n"
        "Respond with one suggestion per numbered item below, in the same "
        "order, `index` matching the number shown. Be conservative -- \"none\" "
        "is a correct and expected answer for many items, not a failure.\n\n"
        f"{numbered}"
    )


def call_model(kind, items):
    import anthropic
    from pydantic import BaseModel
    from typing import Literal, Optional, List

    class Suggestion(BaseModel):
        index: int
        target_type: Literal["chapter", "topic", "none"]
        target: str
        confidence: Literal["high", "medium", "low"]
        reason: str
        note: Optional[str] = None

    class Suggestions(BaseModel):
        items: List[Suggestion]

    client = anthropic.Anthropic()
    response = client.messages.parse(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": build_prompt(kind, items)}],
        output_format=Suggestions,
    )
    by_index = {s.index: s for s in response.parsed_output.items}
    return by_index


def validate(kind, suggestion, counts):
    """Downgrade to none rather than trust an out-of-range or invalid target --
    a hallucinated chapter number is exactly the failure mode the reference
    block is meant to prevent, but the model is not guaranteed to obey it."""
    if suggestion.target_type == "chapter":
        import re
        # Non-greedy on purpose -- a greedy [a-z0-9]+ parses "matthew12" as
        # slug "matthew1" chapter 2 instead of slug "matthew" chapter 12.
        m = re.match(r"^([a-z0-9]+?)(\d+)$", suggestion.target.strip())
        if not m or m.group(1) not in counts:
            return "none", ""
        slug, ch = m.group(1), int(m.group(2))
        if not (1 <= ch <= counts[slug]):
            return "none", ""
        return "chapter", f"{slug}{ch}.html"
    if suggestion.target_type == "topic" and kind == "article":
        pages = set(topic_pages())
        if suggestion.target.strip() in pages:
            return "topic", suggestion.target.strip()
        return "none", ""
    return "none", ""


def render_body(kind, items, suggestions, header_lines):
    lines = list(header_lines)
    lines.append("")
    lines.append(
        "Each item below has an AI-drafted suggestion -- a starting point, not "
        "a decision. To add items to the site, reply on this issue with the "
        "numbers to approve, e.g. `approve: 1, 3, 5`. Unlisted numbers are left "
        "for another week; nothing is added until you reply. Only the repo "
        "owner's reply is acted on.")
    lines.append("")
    for i, it in enumerate(items, 1):
        s = suggestions.get(i)
        title = it["title"] or it.get("url", "")
        src = it.get("channel") or it.get("source") or ""
        link = it.get("url") or (f"https://www.youtube.com/watch?v={it.get('id')}"
                                 if it.get("id") else "")
        lines.append(f"**{i}.** [{title}]({link})  <sub>{src}</sub>")
        if s and s.target_type != "none":
            where = s.target
            lines.append(f"   - Suggested: `{where}` (confidence: {s.confidence}) "
                        f"-- {s.reason}")
            if s.note:
                lines.append(f"   - Draft note: {s.note}")
        else:
            reason = f" -- {s.reason}" if s else ""
            lines.append(f"   - Suggested: *no confident placement*{reason}")
        lines.append("")
    return "\n".join(lines)


def main():
    argv = sys.argv[1:]

    def arg(name):
        if name in argv:
            return argv[argv.index(name) + 1]
        sys.exit(f"{name} is required")

    kind = arg("--kind")
    if kind not in ("video", "article"):
        sys.exit("--kind must be video or article")
    items_path = arg("--items")
    issue_body_path = arg("--issue-body")

    if not os.path.isfile(items_path):
        print(f"no items file at {items_path}, nothing to suggest", file=sys.stderr)
        return 0
    with open(items_path, encoding="utf-8") as f:
        items = json.load(f)
    if not items:
        print("no items, nothing to suggest", file=sys.stderr)
        return 0

    original_body = ""
    if os.path.isfile(issue_body_path):
        with open(issue_body_path, encoding="utf-8") as f:
            original_body = f.read()
    header_lines = original_body.split("\n")[:3] if original_body else [
        f"Found **{len(items)}** new item(s)."]

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set, leaving issue body without "
              "suggestions", file=sys.stderr)
        return 0

    try:
        by_index = call_model(kind, items)
    except Exception as e:  # noqa: BLE001 -- any failure here must not block
        # the underlying detection report from being filed.
        print(f"WARN: suggestion call failed, leaving issue body without "
              f"suggestions: {type(e).__name__}: {e}", file=sys.stderr)
        return 0

    counts = book_chapter_counts()
    resolved = {}
    for i, it in enumerate(items, 1):
        s = by_index.get(i)
        if not s:
            continue
        target_type, target = validate(kind, s, counts)
        resolved[i] = {
            "target_type": target_type,
            "target": target,
            "confidence": s.confidence,
            "reason": s.reason,
            "note": s.note if target_type != "none" else None,
        }
        # keep the object usable by render_body, but with the validated target
        s.target_type, s.target = target_type, target

    body = render_body(kind, items, by_index, header_lines)

    payload = {"kind": kind, "items": items, "suggestions": resolved}
    body += ("\n<!-- PLACEMENT_JSON\n" +
             json.dumps(payload, indent=2) +
             "\n-->\n")

    with open(issue_body_path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"wrote {len(items)} suggestion(s) into {issue_body_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
