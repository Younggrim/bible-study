"""Catch the mistakes that are easy to make and hard to see: a page that uses an
icon nobody drew, a link-preview image that does not exist, a banner with no
emblem, a file the HTML points at that is missing.

    python3 check_site.py docs                         # bible-study
    python3 check_site.py ../bible-study-newriver/docs  # New River

Exits 1 and lists the problems if there are any. Run it after any edit that adds
pages, icons or images (and weekly, as a scheduled task, if you like)."""
import glob, json, os, re, sys
from collections import defaultdict

docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
problems = defaultdict(list)
css = open(os.path.join(docs, "site", "style.css"), encoding="utf-8").read()
drawn = set(re.findall(r"\.fa-([a-z0-9-]+)\s*\{\s*--ico", css)) | {"spin"}
used = defaultdict(set)
pages = sorted(glob.glob(os.path.join(docs, "*.html")))

for p in pages:
    name = os.path.basename(p)
    h = open(p, encoding="utf-8").read()
    for ic in re.findall(r"\bfa-([a-z0-9-]+)", h):
        used[ic].add(name)
    if "cdnjs.cloudflare.com" in h:
        problems["still loads from cdnjs"].append(name)
    if 'class="topic-hero"' in h and 'class="hero-emblem"' not in h:
        problems["banner without an emblem"].append(name)
    m = re.search(r'og:image" content="https://[^/]+/([^"]+)"', h)
    if m and not os.path.exists(os.path.join(docs, m.group(1))):
        problems["og:image file missing"].append(f"{name} -> {m.group(1)}")
    if name not in ("404.html", "offline.html") and 'rel="apple-touch-icon"' not in h:
        problems["no apple-touch-icon"].append(name)
    for ref in re.findall(r'(?:href|src)="(site/[^"?#]+)', h):
        if not os.path.exists(os.path.join(docs, ref)):
            problems["linked file missing"].append(f"{name} -> {ref}")

for f in glob.glob(os.path.join(docs, "site", "*.js")):
    for ic in re.findall(r"\bfa-([a-z0-9-]+)", open(f, encoding="utf-8").read()):
        used[ic].add("site/" + os.path.basename(f))
for ic in sorted(set(used) - drawn):
    problems["icon used but not drawn (make_icon_css.py)"].append(f"fa-{ic} in {sorted(used[ic])[0]}")

man = json.load(open(os.path.join(docs, "manifest.json")))
for i in man.get("icons", []):
    if not os.path.exists(os.path.join(docs, i["src"])):
        problems["manifest icon missing"].append(i["src"])

sw = open(os.path.join(docs, "sw.js"), encoding="utf-8").read()
for ref in re.findall(r"'(/[^']+\.(?:html|css|js|png))'", sw):
    if not os.path.exists(os.path.join(docs, ref.lstrip("/"))):
        problems["service worker caches a missing file"].append(ref)

print(f"{len(pages)} pages checked in {docs}")
if problems:
    for k, v in problems.items():
        print(f"\n{k} ({len(v)}):")
        for x in v[:8]:
            print("  ", x)
        if len(v) > 8:
            print(f"   ... and {len(v) - 8} more")
    sys.exit(1)
print("no problems")
