# Enduring Word Commentary — URL Reference

Base pattern: `https://enduringword.com/bible-commentary/{book-slug}-{chapter}/`

## URL Slug Map (all 66 books)

### Old Testament

| Book | Slug | Chapters |
|---|---|---|
| Genesis | `genesis` | 1–50 |
| Exodus | `exodus` | 1–40 |
| Leviticus | `leviticus` | 1–27 |
| Numbers | `numbers` | 1–36 |
| Deuteronomy | `deuteronomy` | 1–34 |
| Joshua | `joshua` | 1–24 |
| Judges | `judges` | 1–21 |
| Ruth | `ruth` | 1–4 |
| 1 Samuel | `1-samuel` | 1–31 |
| 2 Samuel | `2-samuel` | 1–24 |
| 1 Kings | `1-kings` | 1–22 |
| 2 Kings | `2-kings` | 1–25 |
| 1 Chronicles | `1-chronicles` | 1–29 |
| 2 Chronicles | `2-chronicles` | 1–36 |
| Ezra | `ezra` | 1–10 |
| Nehemiah | `nehemiah` | 1–13 |
| Esther | `esther` | 1–10 |
| Job | `job` | 1–42 |
| Psalms | `psalm` | 1–150 |
| Proverbs | `proverbs` | 1–31 |
| Ecclesiastes | `ecclesiastes` | 1–12 |
| Song of Solomon | `song-of-solomon` | 1–8 |
| Isaiah | `isaiah` | 1–66 |
| Jeremiah | `jeremiah` | 1–52 |
| Lamentations | `lamentations` | 1–5 |
| Ezekiel | `ezekiel` | 1–48 |
| Daniel | `daniel` | 1–12 |
| Hosea | `hosea` | 1–14 |
| Joel | `joel` | 1–3 |
| Amos | `amos` | 1–9 |
| Obadiah | `obadiah` | 1 |
| Jonah | `jonah` | 1–4 |
| Micah | `micah` | 1–7 |
| Nahum | `nahum` | 1–3 |
| Habakkuk | `habakkuk` | 1–3 |
| Zephaniah | `zephaniah` | 1–3 |
| Haggai | `haggai` | 1–2 |
| Zechariah | `zechariah` | 1–14 |
| Malachi | `malachi` | 1–4 |

### New Testament

| Book | Slug | Chapters |
|---|---|---|
| Matthew | `matthew` | 1–28 |
| Mark | `mark` | 1–16 |
| Luke | `luke` | 1–24 |
| John | `john` | 1–21 |
| Acts | `acts` | 1–28 |
| Romans | `romans` | 1–16 |
| 1 Corinthians | `1-corinthians` | 1–16 |
| 2 Corinthians | `2-corinthians` | 1–13 |
| Galatians | `galatians` | 1–6 |
| Ephesians | `ephesians` | 1–6 |
| Philippians | `philippians` | 1–4 |
| Colossians | `colossians` | 1–4 |
| 1 Thessalonians | `1-thessalonians` | 1–5 |
| 2 Thessalonians | `2-thessalonians` | 1–3 |
| 1 Timothy | `1-timothy` | 1–6 |
| 2 Timothy | `2-timothy` | 1–4 |
| Titus | `titus` | 1–3 |
| Philemon | `philemon` | 1 |
| Hebrews | `hebrews` | 1–13 |
| James | `james` | 1–5 |
| 1 Peter | `1-peter` | 1–5 |
| 2 Peter | `2-peter` | 1–3 |
| 1 John | `1-john` | 1–5 |
| 2 John | `2-john` | 1 |
| 3 John | `3-john` | 1 |
| Jude | `jude` | 1 |
| Revelation | `revelation` | 1–22 |

## Usage in App

Generate a commentary URL with:
```
https://enduringword.com/bible-commentary/{slug}-{chapter}/
```

Examples:
- Genesis 1 → `https://enduringword.com/bible-commentary/genesis-1/`
- Psalms 23 → `https://enduringword.com/bible-commentary/psalm-23/`
- John 3 → `https://enduringword.com/bible-commentary/john-3/`
- Revelation 22 → `https://enduringword.com/bible-commentary/revelation-22/`

## Notes
- Psalms uses the singular slug `psalm` (not `psalms`)
- Numbered books use a hyphen prefix: `1-samuel`, `2-kings`, `1-corinthians`, etc.
- Single-chapter books (Obadiah, Philemon, 2 John, 3 John, Jude) use chapter `1`
- All URLs confirmed returning HTTP 200
- No API key required — links open in the device browser
- Attribution: Commentary © David Guzik, enduringword.com
