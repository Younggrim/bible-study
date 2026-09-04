# Handoff for Claude — bible-study / bible-study-newriver

Updated **3 Sep 2026**. Everything below is merged to `main` in both repos and
deployed. This is a verification pass, not a rescue.

**Read `WORKFLOW.md` in either repo first** — it is byte-identical in both and is the
real contract. `REPO_OVERVIEW.md`, beside this file, explains how the two repos fit
together. This file covers what changed, what is left, and the traps.

All three live in `bible-study/` and are tracked. They sat loose in the parent folder
until 3 Sep, outside both repos and outside version control, which meant the densest
record of the project's traps and settled decisions was the least protected thing in
it. `WORKFLOW.md` is mirrored into New River by the sync; these two are upstream only,
since bible-study is the source of truth.

**Final shas.** upstream `2446c43`, New River `7efdcf2`. Both mains clean and in sync.

The 1 Sep section of this file has been folded down to what is still true. The
standing rules and traps from that pass are unchanged and still apply — they are at
the bottom and they are the most valuable part of this document.

---

## Headline, 3 Sep

The Authorship & Background format is **finished: 1189 of 1189 panes clean, 66 of 66
books, 0 defects.** Psalms was the last book and went from 0 to 150 in one pass.

A seventh tab, **Articles**, is on all 1189 chapter pages.

Two verification recipes in `WORKFLOW.md` were **quietly broken** and are fixed. Two
figures in it were badly stale, one by a factor of five.

### What shipped

| PR | repo | squashed to | what |
|---|---|---|---|
| #55 / #54 | both | `4ea66e8` / `3c18488` | Articles tab on 1189 chapter pages, foot block on topical and life pages |
| #57 / #55 | both | `e787659` / `5fbba28` | Psalms fold, 150 pages / 751 sections, plus the leviticus27 repair |
| #58 / #56 | both | `2627011` / `fc4d644` | WORKFLOW.md corrections |
| #59 / #57 | both | `2446c43` / `7efdcf2` | baseline additions, removed duplicated tab counts |

All four Pages deploys returned `success`, 15-33 seconds each.

---

## Articles tab

Order on the page is `summary → authorship → commentary → videos → articles →
reflection`, with `mapgeo` on the 842 that have one. Life and topical pages have no
tab bar, so they get an Articles block at the foot instead.

Every entry is an outbound link to the publisher with a one-line note. Nothing is
reproduced on the page and each pane says so.

Supporting scripts: `add_articles.py`, `article_sources.py`, `check_new_articles.py`,
and `.github/workflows/weekly-article-audit.yml`. That workflow exists **only in
bible-study** — New River has no article scripts, and keeping the file out avoids the
two copies diverging.

`DROP_ARTICLE_URLS` exists for the same reason `DROP_VIDEO_IDS` does. Deleting a link
from the HTML is not enough: the source stays in the allow list, so the next weekly
poll suggests it again. Record the reason.

---

## Psalms fold

150 pages, 751 verse-range sections, from 21 scripts named `fold_psalms_*.py`. Each
rebuilds its pane from its own `SECTIONS` table, so they are re-runnable and produce
identical output. Re-running the whole set leaves `docs/` hash-identical.

Sections are **deliberately shorter** for Psalms than for narrative, the same call
made earlier for the Proverbs couplets. A six-verse psalm does not support a
Mark-chapter exposition, and padding one to hit a character count produces worse prose
than leaving it short. Book fields are preserved on every page, including the
Psalms-only `Attributed Author:`.

### Three psalms state a difficulty rather than resolving it

This was deliberate. Reversing it is a change of editorial policy, not a tidy-up.

- **`psalms137`** ends by blessing whoever kills Babylonian infants. The section gives
  the verse, notes Isaiah 13:16 and Nahum 3:10 promise Babylon exactly this, notes the
  psalm asks God rather than acting, and notes the Church has largely kept the verse
  out of public reading. It does not soften it. A page covering all nine verses that
  went quiet at verse 9 would be worse.
- **`psalms149:6`** puts a two-edged sword in the congregation's hand and has been
  preached at crusades and at Münster. The section says so, then says what the psalm
  limits it to: *the judgment written*, a sentence already passed, not a licence to
  pass one.
- **`psalms119`** spends 175 verses praising God's instruction and ends at 176 with *I
  have gone astray like a lost sheep*. The last of its 22 stanza sections treats that
  as the key to the poem rather than an accident.

### Editorial facts named on the page

`psalms108` is Psalm 57:7-11 joined to Psalm 60:5-12 with no seam. The doxology at
`psalms106:48` closes Book IV rather than answering the petition at verse 47.
`psalms145`'s acrostic skips the letter nun, and English Bibles disagree about whether
to print the line the Greek and the Dead Sea scroll supply, so two readers comparing
versions at verse 13 will count different lines.

---

## leviticus27, and why it matters beyond one page

The last non-Psalms pane with a sublist, and it survived because **the prose depended
on it**. The `vv.1-8` section body ended mid-sentence on a colon:

```
... Since the person cannot literally be sacrificed, a monetary equivalent
is established:
```

The eight shekel figures lived in the list, with a headless `auth-item` continuing
after it. Every check passed it: all list items carried verse ranges so the drop rule
cleared them, the sections covered every verse so coverage passed, and the label was
well formed so `label_fault` passed. Nothing could see the prose was cut in half.
`WORKFLOW.md` now carries a detection snippet — a section body whose last character is
a colon is handing off to something.

**The repair also corrected two false claims**, which is the wider lesson: a pane
nobody has re-read since it was generated may be wrong as well as malformed.

| old claim | why it is wrong |
|---|---|
| thirty shekels is "the price of ... a male between 5-20" | v.5 sets a male 5-20 at **twenty** |
| thirty shekels is "the price of the least valuable category of adult" | v.7 sets a male over sixty at **fifteen**, a female over sixty at **ten** |

Accurate now: thirty shekels is a woman aged 20-60 in v.4, the compensation Exodus
21:32 requires when an ox kills a slave, and the sum of Matthew 26:15, which Matthew
27:9-10 reads against Zechariah 11:12-13.

---

## Two checks in WORKFLOW.md were broken

### The diff-hunk invariant

It claimed **0 unexplained hunks**. It was really reporting **267**, every one a
dropped video player, because its `BRAND` list had no key for the video facade — so
the allow list New River exists to apply read as a fault. Added `yt-facade` and
`loadYT`.

That fix could then hide a player going missing, so it is now **paired with a
direction check**: the allow list can only make New River show *fewer* players, never
more, never a different set. Current state 358 dropped, 0 extra.

The honest expectation is **1 unexplained hunk, not 0**: `matthew28.html`, where all
three players come from disallowed sources, so the pane emptied and the sync removed
the tab too. Compare against the sync's `1 empty Videos tabs tidied` rather than
expecting a constant.

### The obvious div-balance check

Counting `<div` against `</div>` **inside the captured authorship pane reports all
1189 as unbalanced**, and that is correct. The captured region runs to the next
`tab-content` div and so includes the pane's own closing tag, leaving exactly one
unmatched closer. The right assertion is a delta of **+1**. All 1189 sit there and all
1228 files balance end to end. The audit for this handoff flagged 1189 broken panes
before spotting it.

### And two stale figures

**Authorship status** read `559 of 1189 done, 630 remaining`. It is **1189 of 1189**.

**The deferred Key Themes count read 122 pages. It is 661** — wrong by five times.
122 was correct when written at 559 folded pages and grew with every book folded
after, because a page only entered the count once folded. Anyone scoping that work
from the file would have been badly wrong. Both figures now carry a re-measure snippet
and a note saying why not to trust the printed number.

Also corrected: sublists 455 → 0, emphatic capitals 413 pages/1,115 words → 179/282,
and the tab counts that had started being duplicated in the baseline were removed in
favour of the one table that holds them. **Two copies of a number is how most of the
stale figures in that file happened.**

---

## Verified state, 3 Sep

The whole local suite below runs in **about 10 seconds**. The commands themselves are
in `WORKFLOW.md` under "Verifying the invariant". **Run the cross-repo ones from the
folder containing both clones**, not from inside a repo — their paths are relative and
this file now lives inside `bible-study`, which makes that the easy mistake.

```
authorship            1189 of 1189, 66 books, 0 defects
surviving sublists    0        sections ending on a colon   0
duplicate labels      0        verse gaps                   0
past last verse       0        sections out of order        0
stray label caps      0        pane div delta               +1 on all 1189 (correct)
whole-file div balance          0 unbalanced of 1228

unexplained diff hunks          1, and it is matthew28.html only
players dropped / extra         358 / 0
upstream palette literals       0 for each of the five
undefined CSS var()             none, either repo
U+FFFD in captions              0, both repos
sync idempotent                 yes, two consecutive runs hash identically
WORKFLOW.md                     byte-identical on both mains
```

**Reproducibility.** Re-running all 21 fold scripts plus both repair scripts leaves
`docs/` hash-identical and the tree clean. `fix_section_order.py` reports 0 pages to
reorder, because the fold scripts emit sections in verse order and their own
`verify()` enforces it.

**New River branding, unchanged through the sync.** CNAME
`bible.nrc.macdwellings.com`, both dove marks, overlay 127 videos across 60 chapters,
Cinzel on all 1228 pages, `style.css` and `script.js` byte-identical before and after.

---

## Not verified, and why

**The live sites have not been looked at, and still have not been since 1 Sep.**
`bible.macdwellings.com` and `bible.nrc.macdwellings.com` both return a Charter
"Access Blocked" 503 from the authoring network, and the `github.io` origins 301 to
those same domains. Everything above is verified against the deployed *source* through
the GitHub API, not a rendered page.

Worth a human eye on:

- **the tab bar on a phone.** Seven tabs is the most it has ever carried and it wraps
  rather than scrolls.
- **`matthew28`**, the one page where New River shows no Videos tab at all.
- the colours: rust `#8b3a2a` links upstream, black links and the dove in New River's
  nav. Still unconfirmed visually since the CSS refactor.

---

## Outstanding

**1. Chapter-level `Key Themes:` on 661 pages.** The big one. Only 528 pages carry the
field at all. Re-measure before planning; snippet is in `WORKFLOW.md`.

**2. Strip embedded `Key themes:` from `Author:` on 386 pages.** 13 distinct strings,
one repeated 150 times across Psalms. **Must run after item 1**, so no page is ever
left without themes. Together these give one shape: Author, Classification, Key
Themes, Historical Context, sections.

**3. Emphatic capitals on 179 pages, 282 distinct words.** All in `Author:` and
`Historical Context:` bodies, which the folds preserved verbatim by design. Needs a
pass over `CAPS_OK` in `audit_authorship.py` first. **Never bulk-transform** —
lowercasing by rule destroys divine names, Roman numerals and abbreviations.

**4. British spellings** in the project's own prose only. KJV quotations keep
`favour`, `honour`, `labour`.

**5. Owner-only: the weekly article audit has never run.** The token lacks
`Actions: write`. Trigger once from the Actions tab in `bible-study`. Upstream
`e13849d` un-recorded seven recent articles specifically so the first run has
something to report.

**6. The four undecided videos from 1 Sep — resolved to two placed, one dropped, one
still open.** oEmbed only ever gave truncated titles; fetching the full title and
`author_name` for each settled three of the four:

| video | id | resolution |
|---|---|---|
| Ein Gedi: Where David Hid from Saul \| Israel Trip Part 14 | `EEOaTgDp6zM` | **Placed** on `1samuel24` — David Guzik (allowed), and the full title confirms the location is tied to that chapter's cave scene, travelogue framing notwithstanding |
| Sweet and sour...prophetic words? | `97KHCS7Pq_s` | **Placed** on `revelation10` — Spoken Gospel (allowed). Confirmed against the text: Revelation 10:9-10 is the passage where the scroll is sweet in the mouth and sour in the belly; Ezekiel 3:3 is sweet only, no sour, so it doesn't fit the title |
| Incredible \*HIDDEN\* Detail in Story of Jonah in Bible | `_pIGyMFIuIg` | **Dropped, not a placement question.** Channel is Lakepointe Church, which is not in `BIBLE_STUDY_ALLOW` (`video_sources.py`) and never has been. Adding it would just have it stripped by the next `filter_videos.py` run. Not worth a `DROP_VIDEO_IDS` entry since the channel itself was never eligible |
| He Obeyed God Perfectly. God Still Rejected Him. | `rnMh5XPfN_8` | **Still open.** THE BEAT by Allen Parr (allowed). A search turned up a synopsis — "a man in the Bible God personally praised — and then rejected... most Christians have never heard his name" — which argues *against* the earlier guess of Saul (1 Samuel 15): Saul is not an obscure name. No transcript was reachable to confirm who it actually is |

---

## Traps

### One clone, two sessions — this bit twice on 3 Sep

Mid-run another session switched New River's `HEAD` to `main`, and a commit landed
there instead of on the working branch. Recovered non-destructively with
`git branch -f <branch> <sha>` then `git branch -f main origin/main`. Both remotes
also advanced while work was in progress.

**Check `git branch --show-current` immediately before every commit.** Prefer one
session per clone.

### `style.css` and `script.js` do not mirror — bit twice on 1 Sep

They are on the sync's **preserve** list. Any change must be made in **both repos by
hand**; the sync only warns afterwards:

```
WARNING: upstream site/script.js changed since the last sync
         (8c78a039 -> 59ad3c9b); review whether New River's copy needs the same edit
```

Worse, **anything in the installed app's info panel exists twice** — once in
`index.html` and once as a JavaScript string in `script.js`. Spurgeon was removed from
the front page and missed in the panel, so app users were still shown a commentator
the site no longer carries. Grep both before assuming a change is complete.

`sw.js` is **not** preserved, so it mirrors normally and only needs editing upstream.

### `git diff --name-only A..B` is a tree comparison, not a file list

Used it to check whether an incoming merge overlapped the psalms files and got a false
positive listing all 150. `git show --stat <sha>` is the right tool.

### Python cannot reach the GitHub API from the authoring Mac

`urllib` fails with `CERTIFICATE_VERIFY_FAILED: Missing Authority Key Identifier` —
the corporate proxy's root CA is in the macOS system trust store but not in Python's
certifi bundle. `/usr/bin/curl` works, `git` works. This is why `automation_http.py`
exists; **do not remove it thinking it is redundant.** On a CI runner urllib is used.

For API work: read the token from the keychain via `git credential fill`, feed curl
its config on **stdin** so the token never reaches `argv` or the disk, and put any
request body in a temp file, because the config has already consumed stdin.

### Other sharp edges

- **`fs_write` truncates silently on very large files.** This is why Psalms is 21
  scripts rather than 3. Keep generated scripts to roughly 6 pages of content.
- **Stage explicit pathspecs, never `git add -A docs`.** With other sessions in the
  same tree a blanket add sweeps their work into your commit. Assert the staged count
  before committing.
- **`halves()` in `audit_authorship.py` only understands `a`/`b` suffixes.** A
  three-way verse split double-covers and fails the audit. Consolidate to two
  sections; that call was already made for `jeremiah45`.
- **A section label must END with its verse range**, `Seventy Weeks (vv.24-27):`. A
  range anywhere else does not count as folded. Three pages were miscounted for
  exactly that reason.
- `static.yml` has no `paths` filter, so **any** push to `main` triggers a full Pages
  redeploy, including one touching no page. The weekly audits commit to
  `.automation/`, so that is a wasted deploy per week. `paths: ['docs/**']` would fix
  it. Left alone deliberately.
- `pages.status` reads `errored` on bible-study from a pre-fix failure. Stale legacy
  field; the authoritative signal is the deployment status, which is success.

---

## Rules not to break

1. **All content changes go to bible-study first**, then
   `python3 sync_from_bible_study.py ../bible-study`. Never hand-edit
   `bible-study-newriver/docs/*.html` — the next sync discards it.
2. **Never hardcode a theme color in HTML.** Use `var(--accent-link)` and friends.
3. **New River Church videos only go in `newriver-videos.json`**, never inline, never
   upstream.
4. **Any `site/script.js` or `site/style.css` change must be made in both repos by
   hand.** Preserved by the sync, not mirrored. Has already caused two misses.
5. **Use `add_video.py`**, do not hand-write card markup. It pulls the title from
   oEmbed, refuses dead videos, and aborts on unbalanced divs.
   ```bash
   python3 add_video.py daniel5.html <id>
   python3 add_video.py spiritual-disciplines.html <id> --section Worship
   ```
6. **Merge bible-study before New River.** New River's HTML expects upstream's CSS
   variables to already exist on `main`.
7. **Pre-approved:** the 2BeLikeChrist Daniel series, chapters 5 onward as they
   appear. Nothing else is pre-approved.
8. **Video sources differ by repo on purpose.** Upstream allows 1-11, 14, 15; New
   River allows 1, 2, 3, 4, 6, 11. Never suggest Shorts for either.

---

## Translations

Six, in selector order: **ESV, BSB, KJV, ASV, NET, WEB**. Five are baked into the
HTML. **ESV is the only one fetched at runtime**, because its licence does not allow
storing the text the way the others are. It goes through a Cloudflare Worker at
`esv-proxy.cloudflare-dust598.workers.dev`, which also serves New River.

BSB is public domain since 30 April 2023, so no key, no proxy, no runtime fetch. It
exists specifically because ESV was both the only modern readable translation and the
only one that could fail at load. `add_bsb.py` confirmed BSB's verse count matched the
KJV block in all 1189 chapters before writing, so versification agrees exactly.

`sw.js` serves scripture **cache-first with background revalidation**, everything else
network-first. `CACHE_NAME` is `bible-study-v8`.

Adding another translation: the block on 1189 pages, the `<option>` on 1190,
`TRANSLATION_COLORS` **in both repos**, the PWA info panel **in both repos**, and the
homepage Translation Guide.

---

## Editorial decisions that are settled

Not open questions. Re-litigating any of these is a policy change.

- Long-prose sections with verse-range exposition, one uniform format across all 1189.
- Preserve book fields; never downgrade to generic ones.
- Shorter sections for poetry and miscellanies than for narrative.
- State difficulties rather than resolve them. `psalms88` never turns, `psalms137:9`,
  `psalms149:6`, `jer 4:10` and `7:22`, `isa 7:14`, `14:12`, `45:7`.
- Name duplicates and editorial furniture explicitly: `psalms53` = Ps 14, `psalms70` =
  Ps 40:13-17, doxologies at 41:13 / 72:19 / 89:52 / 106:48, colophon at 72:20.
- Drop inherited items with no verse range when they are cross-references; note the
  fact on the owning page instead.
- Merge overlapping inherited outline items when the smaller sits inside the larger;
  re-divide when genuinely separate.
- Verse ranges compact, `(vv.1-2)`, hyphen not en-dash.
- Capitals: extend the allow list, never transform.

---

## Reference: where the tooling lives

| file | bible-study | New River | why |
|---|---|---|---|
| `audit_authorship.py` | yes | no | the audit. bare, `<book>`, `--defects`, `--labels` |
| `fold_psalms_*.py` (21) | yes | no | Psalms fold, all support `--check` |
| `fix_section_order.py` | yes | no | reorders verse sections, `--check` |
| `fix_leviticus27_valuation.py` | yes | no | one-time repair, `--check`, idempotent |
| `dump_outlines.py` | yes | no | prints a page's inherited outline plus coverage |
| `dump_kjv.py` | yes | no | prints KJV verse text for a chapter range |
| `add_articles.py` | yes | no | articles are added upstream then synced |
| `article_sources.py` | yes | no | curated allow lists and `DROP_ARTICLE_URLS` |
| `check_new_articles.py` | yes | no | weekly article poll, 55 feeds |
| `automation_http.py` | yes | yes | shared transport, curl fallback |
| `check_new_videos.py` | yes | yes | channel list comes from `.automation/` |
| `check_video_links.py` | yes | yes | also scans the overlay where present |
| `add_video.py` | yes | no | videos are added upstream then synced |
| `fix_video_titles.py` | yes | no | keep it; the corruption can recur |
| `add_bsb.py` | yes | no | one-time, added the BSB translation |
| `sync_from_bible_study.py` | no | yes | downstream only |
