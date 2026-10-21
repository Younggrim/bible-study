#!/usr/bin/env python3
"""Load site/account.js and site/study.js (highlights, bookmarks, "pick up
where you left off") on every chapter page and the home page.

Both tags go right after the site/script.js tag. study.js is stamped with
?v=<hash of study.js> so a changed file is fetched fresh, the same way
add_mapgeo_maps.py stamps mapgeo.js. Idempotent: a second run changes 0 files.

    python3 add_study_scripts.py           # write
    python3 add_study_scripts.py --check   # report only

Run in bible-study, then sync New River as usual. study.js and account.js are
mirrored by the sync like any other new file under docs/site/.
"""
import hashlib
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CHAPTER = re.compile(r"^(\d?[a-z]+?)(\d+)\.html$")
SCRIPT_JS = re.compile(r'(<script src="site/script\.js(?:\?v=[^"]*)?"></script>)')
OURS = re.compile(r'\n?[ \t]*<script src="site/(?:account|study)\.js(?:\?v=[^"]*)?"></script>')


def main():
    check = "--check" in sys.argv
    study = open(os.path.join(DOCS, "site", "study.js"), "rb").read()
    v = hashlib.sha256(study).hexdigest()[:8]
    changed = problems = pages = 0
    for name in sorted(os.listdir(DOCS)):
        if not (name == "index.html" or (CHAPTER.match(name) and name != "404.html")):
            continue
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()
        if name != "index.html" and 'class="scripture-container"' not in text:
            continue
        pages += 1
        stripped = OURS.sub("", text)
        m = SCRIPT_JS.search(stripped)
        if not m:
            print("PROBLEM no site/script.js tag:", name)
            problems += 1
            continue
        indent = re.search(r"([ \t]*)$", stripped[: m.start()]).group(1)
        tags = (f'\n{indent}<script src="site/account.js"></script>'
                f'\n{indent}<script src="site/study.js?v={v}"></script>')
        new = stripped[: m.end()] + tags + stripped[m.end():]
        if new != text:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    print(f"pages {pages}, {'would change' if check else 'changed'} {changed}, problems {problems}, study.js v={v}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
