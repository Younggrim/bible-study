#!/usr/bin/env python3
"""Load the study scripts on the pages that use them, right after the
site/script.js tag:

    chapter pages, index.html   account.js, study.js (highlights, bookmarks,
                                "pick up where you left off"), progress.js
                                (chapters studied, streaks), translations.js
                                (other-language Bibles), i18n.js (labels)
    notes.html                  account.js, i18n.js
    every other page with       i18n.js, so the app's bottom bar follows the
    site/script.js              reader's language everywhere

Files that change are stamped with ?v=<hash of that file> so a new version is
fetched fresh, the way add_mapgeo_maps.py stamps mapgeo.js. Idempotent: a
second run changes 0 files.

    python3 add_study_scripts.py           # write
    python3 add_study_scripts.py --check   # report only

Run in bible-study, then sync New River as usual. These files are mirrored
by the sync like any other new file under docs/site/.
"""
import hashlib
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^(\d?[a-z]+?)(\d+)\.html$")
SCRIPT_JS = re.compile(r'(<script src="site/script\.js(?:\?v=[^"]*)?"></script>)')
OURS = re.compile(r'\n?[ \t]*<script src="site/(?:account|study|progress|translations|i18n)\.js(?:\?v=[^"]*)?"></script>')
FULL = ["account", "study", "progress", "translations", "i18n"]
STAMPED = {"study", "progress", "translations", "i18n"}


def main():
    check = "--check" in sys.argv
    stamp = {n: hashlib.sha256(open(os.path.join(DOCS, "site", n + ".js"), "rb").read()).hexdigest()[:8] for n in STAMPED}
    changed = problems = pages = 0
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()
        stripped = OURS.sub("", text)
        m = SCRIPT_JS.search(stripped)
        if not m:
            continue
        if name == "index.html" or (CHAPTER.match(name) and 'class="scripture-container"' in text):
            want = FULL
        elif 'src="site/account.js"' in text:
            want = ["account", "i18n"]          # notes.html, memory.html: pages with their own sign-in
        else:
            want = ["i18n"]
        pages += 1
        indent = re.search(r"([ \t]*)$", stripped[: m.start()]).group(1)
        tags = "".join(f'\n{indent}<script src="site/{n}.js' + (f'?v={stamp[n]}' if n in stamp else "") + '"></script>' for n in want)
        new = stripped[: m.end()] + tags + stripped[m.end():]
        if new != text:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    print(f"pages {pages}, {'would change' if check else 'changed'} {changed}, problems {problems}, "
          + ", ".join(f"{n}.js v={v}" for n, v in sorted(stamp.items())))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
