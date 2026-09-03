# bible-study / bible-study-newriver — how it all fits together

A one-page map. `WORKFLOW.md`, committed byte-identical in both repos, is the
authoritative contract; this is the diagram version.

## The two repos

```
        bible-study                         bible-study-newriver
   source of truth, all content      ──▶    mirror + New River additions
   bible.macdwellings.com                   bible.nrc.macdwellings.com
   warm palette #8b3a2a                     black palette #000000
```

They differ in exactly three ways. Anything else is drift and should be fixed.

1. **Palette** — CSS custom properties in `docs/site/style.css`
2. **New River Church sermons** — `docs/newriver-videos.json`, downstream only
3. **Branding** — title suffix, theme-color, favicons, Cinzel font, dove nav

## Translations

Six, in selector order: **ESV, BSB, KJV, ASV, NET, WEB**.

```
  baked into the HTML                    fetched at runtime
  BSB KJV ASV NET WEB                    ESV
  public domain or attribution-only      licence forbids storing the text
  works offline, cannot fail             Cloudflare Worker proxy, needs a key
```

BSB was added on 1 Sep and is the point of interest: public domain since 30 April
2023, so it gives the site a modern readable translation that needs no key, no
proxy and no network. Before it was added, ESV was both the only modern
translation and the only one that could fail at load.

`sw.js` serves scripture **cache-first with background revalidation** and
everything else network-first, so a slow ESV API no longer delays the default
view. `CACHE_NAME` is `bible-study-v8`.

Adding another translation means: the block on 1189 pages, the `<option>` on 1190
pages, `TRANSLATION_COLORS` **in both repos**, the PWA info panel **in both
repos**, and the homepage Translation Guide.

## Content flow

```
  you edit bible-study/docs/*.html
              │
              ▼
  python3 sync_from_bible_study.py ../bible-study
              │
              │  wipes docs/, copies upstream, then:
              │    preserves 12 New River files
              │    re-applies 5 branding rules
              │    cache-busts css/js by content hash
              ▼
  bible-study-newriver/docs/*.html
```

Idempotent — two runs produce byte-identical trees. Rebuilt from upstream every
run, which is why hand-edits to New River's `docs/` never survive.

**The 12 preserved files:** `CNAME`, `favicon.ico`, `manifest.json`,
`newriver-videos.json`, `site/style.css`, `site/script.js`, `site/dove-*.png`,
`site/favicon-*.png`, `site/icon-*.png`

**Watch out for two of those.** `site/style.css` and `site/script.js` are
preserved, so a change to either has to be made **twice, by hand**, once per
repo. The sync only warns you afterwards. This has already caused two misses:
BSB's colour and panel entry, and Spurgeon lingering in the in-app info panel
after being removed from the front page.

Anything shown in the installed app's info panel exists in two places — once in
`index.html` and once as a JavaScript string in `script.js`. Grep both.

## Video flow

Two separate paths that must not cross.

```
  17 general channels                    New River Church channel
          │                                        │
          ▼                                        ▼
  bible-study chapter HTML               newriver-videos.json
  via add_video.py                       (New River repo only)
          │                                        │
          ▼                                        │
  sync ──▶ New River                               │
          │                                        ▼
          └──────────▶ both sites          rendered at runtime by
                                           script.js, New River only
```

`script.js` is identical in both repos. Upstream it fetches
`newriver-videos.json`, gets a 404, and no-ops. That single mechanism is what
keeps church sermons off the main site.

## Weekly automation

`.github/workflows/weekly-video-audit.yml`, identical in both repos, Mondays
13:00 UTC plus manual dispatch.

```
  ┌─ job: new-uploads ──────────────┐   ┌─ job: dead-links ───────────────┐
  │ check_new_videos.py             │   │ check_video_links.py            │
  │ reads .automation/*.json        │   │ oEmbed probe, no API key        │
  │                                 │   │   200 plays                     │
  │ upstream: 17 channels           │   │   404 gone                      │
  │ New River: New River Church     │   │   401 private / no embed        │
  │                                 │   │                                 │
  │ commits state, opens an issue   │   │ opens an issue if any broke     │
  └─────────────────────────────────┘   └─────────────────────────────────┘
                    │                                   │
                    └───────────────┬───────────────────┘
                                    ▼
                        GitHub issue → email to you
                                    │
                                    ▼
                    you or an assistant decides, then
                    add_video.py upstream → sync
```

**Nothing automated edits `docs/`.** Detection is mechanical and lives on a
runner. Deciding whether a video belongs on Ephesians 4 needs judgment and stays
with a person.

Only definitive 404s and 401s are called broken. Timeouts and rate limits are
retried then listed as inconclusive, because a false positive would get a
working video deleted.

## Deploys

```
  push to main ──▶ static.yml ──▶ upload docs/ ──▶ GitHub Pages
```

- Only `main` deploys. Any other branch is safe.
- Pages source must stay **GitHub Actions**, not legacy. Two publishers racing
  is what deadlocked the deploy on 1 Sep; after the fix it takes ~23 seconds.
- Merge order: **bible-study first**, then New River, which expects upstream's
  CSS variables to exist.
- There is no `paths` filter, so any push to `main` redeploys even if no page
  changed.

## Tooling

| script | where | does what |
|---|---|---|
| `sync_from_bible_study.py` | New River | mirror upstream, re-apply branding |
| `add_video.py` | bible-study | place a video, title pulled from oEmbed |
| `check_new_videos.py` | both | report unseen uploads on tracked channels |
| `check_video_links.py` | both | find videos that no longer play |
| `fix_video_titles.py` | bible-study | repair captions corrupted to U+FFFD |
| `add_bsb.py` | bible-study | one-time, added the BSB translation |
| `automation_http.py` | both | shared transport, urllib with curl fallback |

`automation_http.py` exists because the authoring Mac sits behind a
TLS-inspecting proxy whose CA has no Authority Key Identifier, which Python's
OpenSSL refuses outright while curl accepts. Without it none of these scripts can
be run by hand from that machine. On a CI runner urllib is used and curl is never
touched.

## Current baseline

Measured 3 Sep 2026, after the Articles tab and the Psalms fold merged and deployed.

| | value |
|---|---|
| chapter pages | 1189 |
| tabs | 7: summary, authorship, commentary, videos, articles, reflection, plus mapgeo on 842 |
| tab coverage | 1189 each, except mapgeo 842, and videos 1188 in New River |
| Authorship & Background | 1189 of 1189 clean, 66 of 66 books, 0 defects |
| translations | 6: ESV, BSB, KJV, ASV, NET, WEB |
| BSB blocks, both repos | 1189, verse counts matching KJV exactly |
| unique videos, both repos | 3631, all playable |
| New River sermon overlay | 127 videos across 60 chapters |
| unexplained diffs between repos | 1, `matthew28.html` |
| players dropped by New River | 358, with 0 extra |
| undefined CSS custom properties | 0 |
| corrupted captions | 0 |

Three entries need reading rather than glancing at.

**videos is 1188 in New River, not 1189.** `matthew28`'s three players all come from
sources New River does not allow, so the pane emptied and the sync removed the tab
with it. It is the only page in either repo where a tab count differs, and it is also
the one unexplained diff hunk.

**unexplained diffs is 1, not 0.** This table said 0 for a while and the check behind
it was broken: its `BRAND` list had no key for the video facade, so New River's video
allow list read as a fault and it was really reporting 267 hunks, every one a dropped
player. Fixed in `WORKFLOW.md`, which now also carries a companion check that the
divergence only ever runs one way. Run the checks from there rather than trusting this
table.

**commentary read 972 here until 3 Sep.** `add_commentaries.py` filled the 217
chapters that had no Commentary tab at all, the Psalms and the twelve Minor Prophets.
972 + 217 = 1189.

## The seven rules

1. Content changes go to **bible-study first**, then sync.
2. Never hand-edit `bible-study-newriver/docs/*.html`.
3. Never hardcode a theme color in HTML — use `var(--accent-link)` and friends.
4. New River Church videos live only in `newriver-videos.json`.
5. Any `site/script.js` or `site/style.css` edit must be made in **both** repos.
6. Use `add_video.py` rather than writing card markup by hand.
7. Merge bible-study before New River.

## Deliberately asymmetric, do not "fix"

- `esv-proxy-worker/` and `push-worker/` live in bible-study only. **Both sites
  call the same deployed Cloudflare Workers**, so one source location is correct.
- `add_video.py` and `fix_video_titles.py` are upstream only. They edit content,
  and content is edited upstream.
- `sync_from_bible_study.py` and `.sync-state.json` are downstream only.
- `sw.js` uses `CACHE_NAME = 'bible-study-v7'` in both. Separate origins, so no
  collision.
- `psalms131.html` mentions Spurgeon in both. That is quoted prose in the
  summary, not a commentary reference, and it stays.
