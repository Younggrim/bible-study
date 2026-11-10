"""Share cards (1200x630 PNG): one per study page plus a default.

    python3 make_cards.py bs <bible-study>/docs <out-dir>
    python3 make_cards.py nr <bible-study>/docs <out-dir> <new-river>/docs

Titles and passages are read from the bible-study pages. The palette, brand
line and domain differ by site; everything else is identical.

Needs Playwright and the three fonts, which are not kept in the repo:

    npm i @fontsource/poppins @fontsource/merriweather @fontsource/inter

FONT_DIR (default ./node_modules/@fontsource) says where they are. Run it again
whenever a study page is added or retitled, for both sites, then
python3 add_seo_meta.py picks the new card up."""
import glob, html, os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from emblems import E, SECTION
from playwright.sync_api import sync_playwright

site, docs, out = sys.argv[1], sys.argv[2], sys.argv[3]
nr_docs = os.path.abspath(sys.argv[4]) if len(sys.argv) > 4 else None
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.abspath(os.environ.get("FONT_DIR", "node_modules/@fontsource"))

PAL = {
    "bs": dict(bg="#33241a", gold="#e9c46f", line="rgba(233,196,111,0.34)", ring="rgba(233,196,111,0.55)", soft="#d9c7ae", text="#f5ebe0",
               brand="Bible Study", domain="bible.macdwellings.com"),
    "nr": dict(bg="#171717", gold="#c9a96e", line="rgba(201,169,110,0.40)", ring="rgba(201,169,110,0.60)", soft="#b9b9b9", text="#f2f2f2",
               brand="New River Bible Study", domain="bible.nrc.macdwellings.com"),
}[site]

BOOK_MARK = ('<svg viewBox="0 0 512 512" width="46" height="46"><rect x="238" y="104" width="36" height="262" rx="5" fill="{g}"/>'
             '<rect x="170" y="176" width="172" height="36" rx="5" fill="{g}"/>'
             '<path d="M108 352C156 330 216 334 256 366C296 334 356 330 404 352" fill="none" stroke="{g}" stroke-width="20" stroke-linecap="round"/>'
             '<path d="M108 392C156 370 216 374 256 406C296 374 356 370 404 392" fill="none" stroke="{g}" stroke-width="20" stroke-linecap="round"/></svg>')


NT = {"matthew", "mark", "luke", "john", "acts", "romans", "1corinthians", "2corinthians", "galatians",
      "ephesians", "philippians", "colossians", "1thessalonians", "2thessalonians", "1timothy", "2timothy",
      "titus", "philemon", "hebrews", "james", "1peter", "2peter", "1john", "2john", "3john", "jude", "revelation"}


def books():
    """One card per book of the Bible (book-<slug>.png), shared by its chapter pages."""
    found = {}
    for p in sorted(glob.glob(os.path.join(docs, "*.html"))):
        m = re.match(r"^(.+?)(\d+)\.html$", os.path.basename(p))
        if not m:
            continue
        t = re.search(r"<title>(.*?) (\d+) — Bible Study</title>", open(p, encoding="utf-8").read())
        if not t:
            continue
        slug = m.group(1)
        found.setdefault(slug, [html.unescape(t.group(1)), 0])[1] += 1
    items = []
    for slug, (name, n) in found.items():
        nt = slug in NT
        ref = f"{n} chapter{'s' if n != 1 else ''} · key words in the original {'Greek' if nt else 'Hebrew'}"
        items.append((f"book-{slug}", SECTION["bible"], "New Testament" if nt else "Old Testament", name, ref))
    return items


def pages():
    items = books()
    for p in sorted(glob.glob(os.path.join(docs, "*.html"))):
        stem = os.path.basename(p)[:-5]
        h = open(p, encoding="utf-8").read()
        if stem in E:
            t = re.search(r'<div class="topic-hero">.*?<h1>(.*?)</h1>', h, re.S).group(1)
            ref = re.search(r'<span class="ref">(.*?)</span>', h)
            life = bool(ref) and 'class="subtitle"' not in h
            r = re.sub(r"^[—–-]\s*|\s*\(ESV\)\s*$", "", html.unescape(ref.group(1)).strip()) if ref else ""
            items.append((stem, E[stem], "Life Study" if life else "Topical Study", html.unescape(t), r))
    items.append(("topical-studies", SECTION["topical"], "Bible Study", "Topical Studies", ""))
    items.append(("life-studies", SECTION["life"], "Bible Study", "What the Bible Says About…", ""))
    items.append(("default", SECTION["home"], "Chapter-by-chapter study", PAL["brand"], "Scripture in six translations, with the original Hebrew and Greek"))
    return items


def card_html(inner, kicker, title, ref):
    n = len(title)
    size = 68 if n <= 32 else 58 if n <= 46 else 50
    brand_mark = (f'<img src="file://{nr_docs}/site/dove-white.png" style="height:40px;width:auto;display:block">'
                  if site == "nr" and nr_docs else BOOK_MARK.format(g=PAL["gold"]))
    refline = f'<p class="ref">{html.escape(ref)}</p>' if ref else ""

    def ff(fam, w, style, f):
        return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{style};src:url('file://{FONTS}/{f}') format('woff2')}}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{ff('Poppins', 700, 'normal', 'poppins/files/poppins-latin-700-normal.woff2')}
{ff('Merriweather', 400, 'italic', 'merriweather/files/merriweather-latin-400-italic.woff2')}
{ff('Inter', 400, 'normal', 'inter/files/inter-latin-400-normal.woff2')}
{ff('Inter', 600, 'normal', 'inter/files/inter-latin-600-normal.woff2')}
html,body{{margin:0}}
.card{{position:relative;width:1200px;height:630px;box-sizing:border-box;padding:76px 84px 64px;background:{PAL['bg']};display:flex;gap:56px;font-family:Inter,sans-serif;overflow:hidden}}
.frame{{position:absolute;inset:24px;border:1.5px solid {PAL['line']};border-radius:12px}}
.l{{flex:1 1 0;min-width:0;display:flex;flex-direction:column;justify-content:space-between}}
.k{{margin:0 0 22px;font-size:22px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{PAL['gold']}}}
h1{{margin:0;font-family:Poppins,sans-serif;font-weight:700;font-size:{size}px;line-height:1.12;color:#fff}}
.ref{{margin:22px 0 0;font-family:Merriweather,serif;font-style:italic;font-size:26px;line-height:1.5;color:{PAL['text']}}}
.f{{display:flex;align-items:center;gap:16px;font-size:24px}}
.f b{{font-weight:600;color:{PAL['text']}}} .f span{{color:{PAL['soft']}}}
.r{{flex:0 0 auto;display:flex;align-items:center}}
.ring{{width:250px;height:250px;border-radius:50%;border:2.5px solid {PAL['ring']};display:flex;align-items:center;justify-content:center;color:{PAL['gold']}}}
.ring svg{{width:156px;height:156px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
</style></head><body><div class="card"><div class="frame"></div>
<div class="l"><div><p class="k">{html.escape(kicker)}</p><h1>{html.escape(title)}</h1>{refline}</div>
<div class="f">{brand_mark}<b>{PAL['brand']}</b><span>{PAL['domain']}</span></div></div>
<div class="r"><div class="ring"><svg viewBox="0 0 64 64">{inner}</svg></div></div></div></body></html>"""


os.makedirs(out, exist_ok=True)
items = pages()
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    for stem, inner, kicker, title, ref in items:
        tmp = os.path.join(tempfile.gettempdir(), "_share_card.html")
        open(tmp, "w", encoding="utf-8").write(card_html(inner, kicker, title, ref))
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(120)
        pg.screenshot(path=f"{out}/{stem}.png")
    b.close()
os.remove(os.path.join(tempfile.gettempdir(), "_share_card.html"))
print(f"{len(items)} cards ({site}) -> {out}")
