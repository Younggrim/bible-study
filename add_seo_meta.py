#!/usr/bin/env python3
"""Search and link-preview metadata for every page, plus sitemap.xml and
robots.txt.

Each page gets, fenced between <!-- seo --> and <!-- /seo --> right after its
<title>:

    <meta name="description">      what a search result shows under the title
    <link rel="canonical">         the one URL search engines should index
    og:title / og:description / og:url / og:type / og:site_name / og:image
    twitter:card                    what a shared link previews as

Descriptions come from the page itself: a chapter page uses its Summary tab
(verse ranges dropped, cut at a word boundary), the topical, life-study and
home pages use the hand-written lines in PAGE_DESCRIPTIONS below.

The domain comes from docs/CNAME. New River's sync rewrites it, and the
"Bible Study" site name, for its own deployment, so this script only ever
runs in bible-study.

Idempotent: the fenced block is replaced, never duplicated.

    python3 add_seo_meta.py [--check]
"""
import glob
import html
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "docs")
SITE_NAME = "Bible Study"
MAX_DESC = 155

PAGE_DESCRIPTIONS = {
    "index.html": "Study every book and chapter of the Bible in six translations, with background, maps, commentary, videos, reflection questions and a daily devotional.",
    "404.html": "The page you were looking for could not be found. Return to the home page to browse every book and chapter of the Bible.",
    "devotional.html": "A short daily devotional: a passage of Scripture, a reflection, a prayer and one way to apply it today.",
    "topical-studies.html": "Topical Bible studies on the names of God, covenants, parables, miracles, prophecy, the Trinity, the gospel and more.",
    "life-studies.html": "What the Bible says about the struggles of real life: anxiety, anger, grief, loneliness, addiction, doubt, temptation and more.",
    "addiction.html": "What the Bible says about addiction: why it takes hold, how Scripture describes freedom in Christ, and practical steps toward lasting change.",
    "anger.html": "What the Bible says about anger: when it is righteous, when it becomes sin, and how Scripture teaches us to handle it.",
    "anxiety-and-fear.html": "What the Bible says about anxiety and fear, and how Scripture points worried hearts toward prayer, trust and God's peace.",
    "armor-of-god.html": "A study of the armor of God in Ephesians 6: the belt of truth, breastplate of righteousness, shield of faith, sword of the Spirit and the rest.",
    "beatitudes.html": "A study of the Beatitudes from the Sermon on the Mount: what each blessing means and how it describes life in the kingdom of God.",
    "covenants.html": "The covenants of the Bible, from Noah, Abraham, Moses and David to the new covenant in Christ, and how they tie Scripture together.",
    "depression-and-hopelessness.html": "What the Bible says about depression and hopelessness, the honest laments of Scripture, and where it points for hope.",
    "doubt-and-unbelief.html": "What the Bible says about doubt and unbelief, how God met doubters in Scripture, and how faith can grow through questions.",
    "fruits-of-the-spirit.html": "A study of the fruit of the Spirit in Galatians 5: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness and self-control.",
    "greed-and-materialism.html": "What the Bible says about greed and materialism, contentment, generosity, and treasure that lasts.",
    "grief-and-loss.html": "What the Bible says about grief and loss, how Scripture gives permission to mourn, and the hope it holds out in sorrow.",
    "i-am-statements.html": "A study of the seven I AM statements of Jesus in John's Gospel, from the bread of life to the true vine.",
    "identity-and-self-worth.html": "What the Bible says about identity and self-worth: being made in God's image and who we are in Christ.",
    "kings-of-israel.html": "The kings of Israel and Judah, from Saul, David and Solomon through the divided kingdom to the exile.",
    "loneliness.html": "What the Bible says about loneliness, God's presence with His people, and the gift of community.",
    "lust-and-sexual-sin.html": "What the Bible says about lust and sexual sin, God's design for sexuality, and the path to purity and forgiveness.",
    "marriage-and-family.html": "What the Bible teaches about marriage and family: God's design, love and respect, raising children, and grace at home.",
    "men-of-the-bible.html": "Studies of men of the Bible, from Abraham, Moses and David to Peter and Paul: flawed, faithful and used by God.",
    "miracles-of-jesus.html": "The miracles of Jesus and what they reveal about His authority over nature, sickness, evil spirits and death.",
    "names-of-god.html": "The names of God in Scripture, from Elohim and Yahweh to Adonai, El Shaddai and Immanuel, and what each reveals about Him.",
    "parables-of-jesus.html": "The parables of Jesus explained: the stories He told about the kingdom of God and what they mean today.",
    "prayers-in-the-bible.html": "Great prayers in the Bible, from Abraham and Hannah to David, Daniel, Jesus and Paul, and what they teach about prayer.",
    "pride.html": "What the Bible says about pride, why Scripture calls it the root of so much sin, and the way of humility.",
    "promises-of-god.html": "The promises of God in Scripture: His presence, provision, forgiveness, strength and hope, kept across every generation.",
    "prophecy-and-fulfillment.html": "Old Testament prophecies fulfilled in Jesus: His birth, ministry, death and resurrection foretold centuries before.",
    "spiritual-disciplines.html": "The spiritual disciplines: prayer, Bible reading, fasting, worship, solitude, service and more, and how they help believers grow.",
    "suffering.html": "What the Bible says about suffering, why God allows it, and how Scripture sustains faith and hope through it.",
    "temptation.html": "What the Bible says about temptation, how Jesus resisted it, and the way of escape God provides.",
    "ten-commandments.html": "A study of the Ten Commandments: what each commandment means and how Jesus fulfilled and deepened the law.",
    "the-12-apostles.html": "The twelve apostles of Jesus: who they were, how they were called, and what tradition says became of them.",
    "the-gospel.html": "The gospel explained from Scripture: God's holiness, human sin, Christ's death and resurrection, and salvation by faith.",
    "the-trinity.html": "What the Bible teaches about the Trinity: one God in three persons, Father, Son and Holy Spirit.",
    "unforgiveness-and-bitterness.html": "What the Bible says about unforgiveness and bitterness, and how the forgiveness of God makes forgiving others possible.",
    "women-of-the-bible.html": "Studies of women of the Bible, from Sarah, Ruth and Esther to Mary and Priscilla: courage, faith and devotion.",
}

FENCE = re.compile(r"\n?[ \t]*<!-- seo -->.*?<!-- /seo -->", re.S)
CHAPTER = re.compile(r"^[1-3]?[a-z]+\d+\.html$")


def clip(text, limit=MAX_DESC):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    cut = cut[:cut.rfind(" ")].rstrip(",;:—- ")
    return cut + "…"


def chapter_description(h):
    m = re.search(r'id="tab-summary">\s*<h3>Summary</h3>\s*<p>(.*?)</p>', h, re.S)
    if not m:
        return None
    t = html.unescape(re.sub(r"<[^>]*>", "", m.group(1)))
    t = re.sub(r"\s*\((?:vv?\.|verses?)\s*[\d,:\s–-]+[a-c]?\)", "", t)
    return clip(t)


def attr(s):
    return html.escape(s, quote=True)


def block(name, h, domain):
    title = html.unescape(re.search(r"<title>(.*?)</title>", h, re.S).group(1)).strip()
    desc = PAGE_DESCRIPTIONS.get(name) or chapter_description(h)
    if not desc:
        return None
    url = f"https://{domain}/" + ("" if name == "index.html" else name)
    lines = [
        "<!-- seo -->",
        f'<meta name="description" content="{attr(desc)}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{attr(title)}">',
        f'<meta property="og:description" content="{attr(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="https://{domain}/site/icon-512.png">',
        '<meta name="twitter:card" content="summary">',
        "<!-- /seo -->",
    ]
    return "\n    ".join(lines)


def main():
    check = "--check" in sys.argv
    domain = open(os.path.join(DOCS, "CNAME")).read().strip()
    changed, missing, urls = 0, [], []
    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        h = open(path, encoding="utf-8").read()
        b = block(name, h, domain)
        if b is None:
            missing.append(name)
            continue
        if name != "404.html":
            urls.append(f"https://{domain}/" + ("" if name == "index.html" else name))
        stripped = FENCE.sub("", h)
        new = re.sub(r"(</title>)", r"\1\n    " + b.replace("\\", r"\\"), stripped, count=1)
        if new != h:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(new)

    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
               + "</urlset>\n")
    robots = f"User-agent: *\nAllow: /\n\nSitemap: https://{domain}/sitemap.xml\n"
    for fname, content in (("sitemap.xml", sitemap), ("robots.txt", robots)):
        p = os.path.join(DOCS, fname)
        old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if old != content:
            changed += 1
            if not check:
                open(p, "w", encoding="utf-8").write(content)

    print(f"{len(urls)} URLs in sitemap, {changed} file(s) {'to change' if check else 'changed'}")
    if missing:
        print("no description for: " + ", ".join(missing))


if __name__ == "__main__":
    main()
