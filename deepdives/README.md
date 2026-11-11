# Deep Dives

One file per chapter, `deepdives/<slug>.md` (slug as in `docs/<slug>.html`, e.g. `acts22`,
`1corinthians13`). `python3 add_deep_dives.py <slug>` turns it into the Deep Dive pane on that
chapter page. Re-running replaces the pane, so a file can be corrected and re-applied.

`QUEUE.txt` is the order to write them in: the rest of the 2026 Bible Reading list first, then
the Bible-in-a-year (chronological) plan from Jan 1 2027. A chapter is done when its `.md` exists.
`acts19.md`, `acts20.md` and `acts21.md` are the reference examples. Match their depth and voice.

## Gathering, per chapter

1. ESV text with verse numbers, to confirm the ESV section headings and quote accurately.
2. Tyndale study notes for the chapter (Study Bible connector `get_study_notes`, chapter_only),
   cross-references on the key verse, and `word_study` for any Greek or Hebrew word that changes
   the reading. Use `get_textual_variant` for passages the ESV brackets or footnotes, and
   `get_ane_context` for Old Testament background.
3. The three commentators linked in the Commentary pane. Search first, then fetch a link the
   search returned (a URL built from a pattern is refused):
   - Guzik: search `Guzik <Book> <ch> study guide blueletterbible` and fetch the
     `blueletterbible.org/Comm/guzik_david/StudyGuide_...` result. Fall back to the
     `enduringword.com` result.
   - Matthew Henry: search `Matthew Henry commentary <Book> <ch> biblegateway` and fetch the
     whole-chapter Bible Gateway page for his outline, plus a section page where it matters.
   - Jamieson-Fausset-Brown: search `Jamieson-Fausset-Brown commentary <Book> <ch> christianity.com`.
     Use the christianity.com, sacred-texts.com or biblehub.com result, whichever loads.
     JFB skips some verses. Say so rather than filling the gap.
   If one can't be fetched, carry on with the others. Never use Steven Furtick.

## Writing

The audience is a believer a few years into the faith, reading on a phone. Explain plainly with
no unexplained jargon, and never talk down. Write for any reader: no "you" addressed to a
particular person, and no mention of a study session or "next chapter".

- First paragraph: `*Setting:* ...` (author or speaker if it matters, rough date, where we are
  in the story, what just happened, any setting that frames the chapter).
- One `#### <ESV section heading> (vv1–10)` per ESV section, covering the whole chapter in order.
- Under each, `- ` bullets, each opening with a bold phrase or short ESV quote and its verse:
  `- **"It is finished" (v30).** ...`. Weave in, where they matter: historical, cultural and
  geographic background; who people are; Greek or Hebrew words (transliteration, meaning, what
  English hides); Old Testament background and fulfilment; parallel accounts and what each adds;
  repeated words, irony and structure; textual variants stated calmly; how the passage fits the
  larger story.
- Where faithful Christian traditions disagree, give the main views briefly and fairly. Keep
  text, scholarly reconstruction and tradition distinct ("most scholars think", "tradition holds").
- End each section with one `- **Commentators:** ...` bullet: 1–3 points from Guzik, Matthew Henry
  and JFB, each named. Say where they agree, where they differ from each other or the Tyndale
  notes, and what each adds. Check any word claim against `word_study` and say when the lexicon
  doesn't support it. Skip the bullet if none of them adds anything.
- Close with `#### Pointing to Christ` and a short paragraph, honest and not forced.
- Short ESV quotes only, never long stretches of Scripture.

### Copyright

Guzik and the Tyndale notes are under copyright: paraphrase them, never quote them (this is a
public site). Matthew Henry (1710) and JFB (1871) are public domain, so short quotes are fine.

### Length

About 1,800–3,000 words for a full chapter. Genealogies, census lists, building specifications
and repeated laws get a shorter, honest treatment. Say what the list is for and don't pad it.

## Allowed markdown

`*italic*`, `**bold**`, `[text](https://...)`, `#### ` headings, `- ` bullets and plain
paragraphs. Nothing else. `add_deep_dives.py` rejects other headings.
