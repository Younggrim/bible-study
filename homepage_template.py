"""Homepage template for build_site.py — replaces build_index() return value."""

HOMEPAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bible Study</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Inter:wght@400;500;600;700&family=Cinzel:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="site/style.css?v=3">
    <style>
        .home-content {{ margin-top: 56px; padding: 0; max-width: 900px; margin-left: auto; margin-right: auto; padding-bottom: 60px; }}
        .scroll-section {{ margin: 32px 32px 0; }}
        .scroll-banner {{ display: flex; align-items: center; cursor: pointer; user-select: none; }}
        .scroll-end {{ width: 40px; height: 100px; border-radius: 20px; background: linear-gradient(to right, #c9a96e, #a67c52, #c9a96e); box-shadow: inset 0 0 8px rgba(0,0,0,0.3), 2px 2px 6px rgba(0,0,0,0.15); }}
        .scroll-end.left {{ border-right: 2px solid #8b6914; }}
        .scroll-end.right {{ border-left: 2px solid #8b6914; }}
        .scroll-body {{ flex: 1; background: linear-gradient(180deg, #faf3e0 0%, #f5ebe0 30%, #f0e4d4 70%, #ebe0cc 100%); border-top: 3px solid #c9a96e; border-bottom: 3px solid #c9a96e; padding: 22px 32px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: all 0.3s; }}
        .scroll-title {{ font-family: "Cinzel", serif; font-size: 1.8rem; color: #8b3a2a; margin-bottom: 4px; letter-spacing: 2px; }}
        .scroll-subtitle {{ font-family: "Merriweather", serif; font-size: 0.95rem; color: #5a4e44; font-style: italic; }}
        .scroll-toggle {{ font-size: 0.8rem; color: #8b6914; margin-top: 6px; transition: transform 0.3s; }}
        .scroll-banner:hover .scroll-body {{ background: linear-gradient(180deg, #f5ebe0 0%, #f0e4d4 30%, #ebe0cc 70%, #e5d9c0 100%); }}
        .parchment-body {{ margin: 0 72px; background: linear-gradient(180deg, #f5ebe0 0%, #faf5ed 5%, #fdf9f4 50%, #faf5ed 95%, #f0e4d4 100%); border-left: 3px solid #d4c4a8; border-right: 3px solid #d4c4a8; border-bottom: 3px solid #c9a96e; border-radius: 0 0 8px 8px; padding: 36px 40px 48px; box-shadow: 4px 4px 16px rgba(0,0,0,0.08), -4px 0 16px rgba(0,0,0,0.05); display: none; }}
        .parchment-body.open {{ display: block; }}
        .testament-section {{ margin-bottom: 36px; }}
        .testament-section:last-child {{ margin-bottom: 0; }}
        .testament-title {{ font-family: "Cinzel", serif; font-size: 1.3rem; margin-bottom: 16px; padding-bottom: 8px; font-weight: 700; }}
        .testament-title.ot {{ color: #6b4c3b; border-bottom: 2px solid #6b4c3b; }}
        .testament-title.nt {{ color: #2c5a6b; border-bottom: 2px solid #2c5a6b; }}
        .book-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }}
        .book-link {{ display: block; padding: 12px 16px; background: #fdf9f4; border: 1px solid #e0d6c8; border-left: 4px solid #6b4c3b; border-radius: 10px; text-decoration: none; font-size: 0.85rem; font-weight: 600; color: #3d2b1f; transition: box-shadow 0.2s, transform 0.15s, background 0.2s, color 0.2s; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .book-link:hover {{ box-shadow: 0 6px 16px rgba(0,0,0,0.12); transform: translateY(-3px); background: #8b3a2a; color: #fff; border-left-color: #8b3a2a; }}
        .topic-link {{ border-left-color: #5c3d6e !important; }}
        .topic-link:hover {{ background: #5c3d6e !important; border-left-color: #5c3d6e !important; }}
        .commentary-card {{ background: #fdf9f4; border: 1px solid #e0d6c8; border-radius: 10px; padding: 24px; margin-bottom: 20px; }}
        .commentary-card:last-child {{ margin-bottom: 0; }}
        .commentary-card h4 {{ font-family: "Cinzel", serif; font-size: 1.1rem; color: #8b3a2a; margin-bottom: 8px; }}
        .commentary-card p {{ font-size: 0.9rem; line-height: 1.7; color: #5a4e44; margin: 0; }}
        .trans-guide-item {{ margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #e8e0d6; }}
        .trans-guide-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .trans-guide-item strong {{ font-size: 1rem; }}
        .trans-guide-item p {{ font-size: 0.88rem; line-height: 1.7; color: #5a4e44; margin-top: 4px; }}
        @media (max-width: 768px) {{ .scroll-title {{ font-size: 1.4rem; }} .scroll-subtitle {{ font-size: 0.85rem; }} .scroll-end {{ width: 24px; height: 80px; }} .scroll-body {{ padding: 16px 14px; }} .parchment-body {{ margin: 0 16px; padding: 24px 16px; }} .scroll-section {{ margin: 16px 16px 0; }} .book-grid {{ grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); }} }}
    </style>
</head>
<body>
    <nav class="top-nav">
        <a href="index.html" class="nav-brand">Bible Study</a>
        <div class="nav-center"></div>
    </nav>
    <main class="home-content">

        <div class="scroll-section">
            <div class="scroll-banner" onclick="toggleScroll('bible')">
                <div class="scroll-end left"></div>
                <div class="scroll-body">
                    <h1 class="scroll-title">Bible Study</h1>
                    <p class="scroll-subtitle">Select a book to begin studying</p>
                    <div class="scroll-toggle"><i class="fas fa-chevron-down"></i></div>
                </div>
                <div class="scroll-end right"></div>
            </div>
            <div class="parchment-body" id="scroll-bible">
                <div class="testament-section">
                    <h2 class="testament-title ot">Old Testament</h2>
                    <div class="book-grid">
{ot_cards}                    </div>
                </div>
                <div class="testament-section">
                    <h2 class="testament-title nt">New Testament</h2>
                    <div class="book-grid">
{nt_cards}                    </div>
                </div>
            </div>
        </div>

        <div class="scroll-section">
            <div class="scroll-banner" onclick="toggleScroll('topical')">
                <div class="scroll-end left"></div>
                <div class="scroll-body">
                    <h1 class="scroll-title">Topical Studies</h1>
                    <p class="scroll-subtitle">Explore themes across Scripture</p>
                    <div class="scroll-toggle"><i class="fas fa-chevron-down"></i></div>
                </div>
                <div class="scroll-end right"></div>
            </div>
            <div class="parchment-body" id="scroll-topical">
                <div class="book-grid">
                    <a class="book-link topic-link" href="fruits-of-the-spirit.html">Fruits of the Spirit</a>
                    <a class="book-link topic-link" href="the-12-apostles.html">The 12 Apostles</a>
                    <a class="book-link topic-link" href="names-of-god.html">Names of God</a>
                    <a class="book-link topic-link" href="armor-of-god.html">Armor of God</a>
                    <a class="book-link topic-link" href="parables-of-jesus.html">Parables of Jesus</a>
                    <a class="book-link topic-link" href="prophecy-and-fulfillment.html">Prophecy &amp; Fulfillment</a>
                    <a class="book-link topic-link" href="prayers-in-the-bible.html">Prayers in the Bible</a>
                    <a class="book-link topic-link" href="i-am-statements.html">I AM Statements of Jesus</a>
                    <a class="book-link topic-link" href="ten-commandments.html">The Ten Commandments</a>
                    <a class="book-link topic-link" href="beatitudes.html">The Beatitudes</a>
                    <a class="book-link topic-link" href="covenants.html">Covenants of the Bible</a>
                    <a class="book-link topic-link" href="men-of-the-bible.html">Men of the Bible</a>
                    <a class="book-link topic-link" href="women-of-the-bible.html">Women of the Bible</a>
                    <a class="book-link topic-link" href="kings-of-israel.html">Kings of Israel &amp; Judah</a>
                    <a class="book-link topic-link" href="promises-of-god.html">Promises of God</a>
                    <a class="book-link topic-link" href="spiritual-disciplines.html">Spiritual Disciplines</a>
                    <a class="book-link topic-link" href="marriage-and-family.html">Marriage &amp; Family</a>
                    <a class="book-link topic-link" href="the-trinity.html">The Trinity</a>
                    <a class="book-link topic-link" href="the-gospel.html">The Gospel: Salvation</a>
                    <a class="book-link topic-link" href="miracles-of-jesus.html">Miracles of Jesus</a>
                </div>
            </div>
        </div>

        <div class="scroll-section">
            <div class="scroll-banner" onclick="toggleScroll('translations')">
                <div class="scroll-end left"></div>
                <div class="scroll-body">
                    <h1 class="scroll-title">Translation Guide</h1>
                    <p class="scroll-subtitle">Understanding the five translations used</p>
                    <div class="scroll-toggle"><i class="fas fa-chevron-down"></i></div>
                </div>
                <div class="scroll-end right"></div>
            </div>
            <div class="parchment-body" id="scroll-translations">
                <div class="trans-guide-item"><strong style="color:#8b3a2a;">ESV — English Standard Version (2001)</strong><p>An essentially literal translation balancing word-for-word accuracy with modern readability. Translated from the Masoretic Hebrew text and Nestle-Aland Greek text. Widely used for preaching, study, and memorization.</p></div>
                <div class="trans-guide-item"><strong style="color:#4a5a8a;">KJV — King James Version (1611)</strong><p>The most influential English Bible in history. Commissioned by King James I and translated by 47 scholars from the Textus Receptus. Known for majestic, poetic language that has shaped English literature for over 400 years.</p></div>
                <div class="trans-guide-item"><strong style="color:#7a5c2e;">ASV — American Standard Version (1901)</strong><p>A revision of the KJV using more accurate manuscript evidence. Extremely literal — almost word-for-word from the original languages. Excellent for detailed word studies. Uses "Jehovah" instead of "LORD."</p></div>
                <div class="trans-guide-item"><strong style="color:#5c3d6e;">NET — New English Translation (2005)</strong><p>Created by over 25 biblical scholars with 60,000+ translator notes explaining translation choices. Balances accuracy with natural English. An exceptional study resource.</p></div>
                <div class="trans-guide-item"><strong style="color:#2c6b4f;">WEB — World English Bible (2000)</strong><p>A modern-language update of the ASV. Completely public domain — free to copy, share, and use. Based on the Majority Text tradition. Modern English while faithful to the original languages.</p></div>
            </div>
        </div>

        <div class="scroll-section">
            <div class="scroll-banner" onclick="toggleScroll('commentaries')">
                <div class="scroll-end left"></div>
                <div class="scroll-body">
                    <h1 class="scroll-title">Commentaries</h1>
                    <p class="scroll-subtitle">Study resources referenced throughout</p>
                    <div class="scroll-toggle"><i class="fas fa-chevron-down"></i></div>
                </div>
                <div class="scroll-end right"></div>
            </div>
            <div class="parchment-body" id="scroll-commentaries">
                <div class="commentary-card">
                    <h4>David Guzik — Enduring Word</h4>
                    <p>David Guzik is a pastor, author, and Bible commentator whose verse-by-verse commentary covers the entire Bible. His work through Enduring Word (enduringword.com) is one of the most widely accessed Bible commentaries in the world, freely available online in multiple languages. Guzik writes for the everyday believer — combining solid evangelical scholarship with practical application. He draws from commentators across church history including Matthew Henry, Adam Clarke, and Charles Spurgeon. His commentary is used by pastors for sermon preparation, small group leaders for study material, and individuals for personal devotion.</p>
                </div>
                <div class="commentary-card">
                    <h4>Charles Haddon Spurgeon — The Prince of Preachers</h4>
                    <p>Charles Haddon Spurgeon (1834-1892) was a British Baptist preacher known as the "Prince of Preachers." By age 22 he was the most popular preacher in London, regularly speaking to crowds of 6,000+ at the Metropolitan Tabernacle. Over his lifetime he preached to an estimated 10 million people. His sermon collection — the Metropolitan Tabernacle Pulpit — spans 63 volumes and remains the largest set of books by a single author in Christian history. Spurgeon's preaching was Christ-centered, doctrinally rich, and deeply pastoral. He founded an orphanage, a pastors' college, and distributed literature worldwide. His sermons are in the public domain and remain widely read over 130 years after his death.</p>
                </div>
            </div>
        </div>

    </main>
    <script>
    function toggleScroll(id) {{
        var el = document.getElementById('scroll-' + id);
        el.classList.toggle('open');
    }}
    </script>
</body>
</html>'''
