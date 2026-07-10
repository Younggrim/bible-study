# Requirements Document

## Introduction

The Men's Devotional App is a content-driven application designed for men's small groups and individual study. It provides curated devotionals tied to Bible passages, organized around topics relevant to men's spiritual lives — such as leadership, integrity, fatherhood, temptation, identity, purpose, and relationships. The app draws from a local library of Bible text files (5 translations: KJV, ESV, WEB, ASV, NET) covering all 66 books, and allows users to browse by topic, search for relevant studies, and share devotional content with a men's group.

---

## Glossary

- **App**: The Men's Devotional App, the system being specified.
- **Devotional**: A short study unit consisting of a title, one or more Bible passages, a written reflection, discussion questions, and one or more topic tags.
- **Bible_Library**: The local collection of Bible text files organized by testament, book, and chapter across 5 translations (KJV, ESV, WEB, ASV, NET).
- **Topic**: A men's-specific theme used to categorize devotionals (e.g., Leadership, Integrity, Fatherhood, Temptation, Identity, Purpose, Relationships, Courage, Work, Prayer, Grief, Marriage).
- **Passage**: A reference to one or more Bible verses identified by book, chapter, and verse range.
- **Translation**: One of the five Bible versions available in the Bible_Library: KJV, ESV, WEB, ASV, or NET.
- **Group**: A named collection of users who share devotional content with each other.
- **User**: A person who uses the App to read, search, or share devotionals.
- **Admin**: A User with permission to create, edit, and publish devotionals.
- **Content_Ingestion_Pipeline**: The system component responsible for parsing Bible_Library text files and loading them into the App's data store.
- **Validator**: The system component responsible for checking that a Devotional's required fields are present, correctly typed, and that all Passage references resolve to verses in the data store.
- **Search_Engine**: The system component responsible for full-text and topic-based search over devotionals and Bible passages.
- **Share_Service**: The system component responsible for generating and distributing shareable devotional content to Group members.

---

## Requirements

### Requirement 1: Bible Content Ingestion

**User Story:** As an Admin, I want the app to load Bible text from the local file library, so that devotionals can reference accurate, versioned Scripture.

#### Acceptance Criteria

1. THE Content_Ingestion_Pipeline SHALL parse each Bible text file using the following format: one or more header lines containing the book name, translation identifier, and a separator line, followed by numbered verse lines in the form `{verse_number}. {verse_text}`; for translations that include inline multi-verse spans (such as ESV), a single verse line MAY contain text covering multiple verse numbers, in which case the pipeline SHALL assign that text to the starting verse number of the span.
2. WHEN a Bible text file is successfully parsed, THE Content_Ingestion_Pipeline SHALL extract the chapter number from the file path or a designated chapter header line and SHALL store the book name, chapter number, verse number, verse text, and translation identifier in the data store.
3. IF a Bible text file does not contain the required header lines or does not contain at least one verse line matching the form `{verse_number}. {verse_text}`, THEN THE Content_Ingestion_Pipeline SHALL log the file path and a descriptive error message indicating which structural element was missing or malformed, and SHALL continue processing remaining files.
4. THE Content_Ingestion_Pipeline SHALL support all five translations: KJV, ESV, WEB, ASV, and NET.
5. WHEN ingestion is complete, THE Content_Ingestion_Pipeline SHALL report the total number of files processed, the number successfully parsed, and the number that failed.
6. FOR ALL valid Bible text files, parsing then re-serializing then parsing SHALL produce a verse set that is identical in book name, chapter number, verse number, translation identifier, and verse text for every verse stored in the first parse.

---

### Requirement 2: Devotional Content Management

**User Story:** As an Admin, I want to create and publish devotionals tied to Bible passages and topics, so that men's group members have curated, relevant content to study.

#### Acceptance Criteria

1. THE App SHALL allow an Admin to create a Devotional with the following required fields: a title of 1 to 200 characters, at least one Passage reference in the format `Book Chapter:Verse` or `Book Chapter:Verse-Verse` (e.g., "John 3:16" or "Romans 8:1-4"), a written reflection of 50 to 10,000 characters, 1 to 20 Topic tags, and a publication status of either draft or published.
2. WHEN an Admin saves a Devotional, THE App SHALL invoke the Validator to confirm all required fields are present and within their defined bounds.
3. WHEN the Validator confirms all required fields are present and within bounds, THE Validator SHALL confirm that each Passage reference resolves to at least one verse in the data store.
4. IF a required field is absent or outside its defined bounds, THEN THE App SHALL display an error message identifying the invalid field and SHALL NOT save the Devotional.
5. IF a Passage reference does not resolve to any verse in the data store, THEN THE App SHALL display a descriptive error message identifying the unresolved reference by its `Book Chapter:Verse` value and SHALL NOT save the Devotional.
6. THE App SHALL allow an Admin to edit any existing Devotional, including its title, Passage references, reflection text, Topic tags, and publication status.
7. THE App SHALL allow an Admin to delete any existing Devotional.
8. WHILE a Devotional has a publication status of draft, THE App SHALL make it visible only to Admins and SHALL NOT include it in any User-facing search results, Topic browsing lists, or Group shares.
9. WHEN a Devotional is deleted, THE App SHALL remove it from all search results and Group shares within 5 seconds.

---

### Requirement 3: Topic-Based Browsing

**User Story:** As a User, I want to browse devotionals by topic, so that I can find studies relevant to what I'm facing right now.

#### Acceptance Criteria

1. THE App SHALL display a browsable list of all Topics that have at least one published Devotional, sorted alphabetically ascending by Topic name.
2. WHEN a User selects a Topic, THE App SHALL display all published Devotionals tagged with that Topic, sorted by publication date descending; IF two or more Devotionals share the same publication date, THEN THE App SHALL sort those Devotionals by title ascending as a tiebreaker.
3. THE App SHALL support at minimum the following Topics: Leadership, Integrity, Fatherhood, Temptation, Identity, Purpose, Relationships, Courage, Work, Prayer, Grief, and Marriage.
4. WHILE a User is browsing a Topic, THE App SHALL display for each result: the Devotional title, the first-listed Passage reference as the primary Passage reference, and a preview consisting of the first 150 characters of the reflection text followed by an ellipsis ("…") if the reflection text exceeds 150 characters.
5. IF a Topic has no published Devotionals, THEN THE App SHALL display a message indicating no content is currently available for that Topic.

---

### Requirement 4: Search

**User Story:** As a User, I want to search for devotionals and Bible passages by keyword or topic, so that I can quickly find studies relevant to a specific issue or question.

#### Acceptance Criteria

1. THE Search_Engine SHALL accept a search query of 1 to 200 non-whitespace characters and return matching published Devotionals and Passages; IF a query is empty, contains only whitespace, or exceeds 200 characters, THEN THE Search_Engine SHALL display an error message indicating the query is invalid and SHALL NOT execute a search.
2. WHEN a User submits a valid search query, THE Search_Engine SHALL return results within 2 seconds for a data set of up to 10,000 Devotionals.
3. THE Search_Engine SHALL perform case-insensitive matching, tokenize the query by whitespace into individual terms, and return all published Devotionals and Passages where at least one token matches against Devotional titles, reflection text, Topic tags, or Bible verse text; the result set SHALL be capped at 100 results and SHALL contain no duplicate entries.
4. THE Search_Engine SHALL rank results in two tiers: Tier 1 contains Devotionals whose title or a Topic tag exactly matches the full query string (case-insensitive); Tier 2 contains all remaining results matched in reflection text or Bible verse text; within each tier, results SHALL be sorted by publication date descending.
5. WHEN a User searches by a Topic name, THE Search_Engine SHALL return all published Devotionals tagged with that Topic in addition to any text-match results, subject to the 100-result cap.
6. WHEN a search query matches no results, THE Search_Engine SHALL display a message indicating no results were found and SHALL suggest up to 3 related Topics.

---

### Requirement 5: Bible Passage Viewer

**User Story:** As a User, I want to read the full Bible passage associated with a devotional in my preferred translation, so that I can engage directly with Scripture.

#### Acceptance Criteria

1. WHEN a User opens a Devotional, THE App SHALL display the associated Passage text using the User's selected Translation.
2. THE App SHALL allow a User to switch the active Translation from any screen in the App, and the selected Translation SHALL apply to all Passage displays throughout the App.
3. WHILE a User is viewing a Passage, THE App SHALL display the book name, chapter number, and verse numbers alongside each verse.
4. IF the User's selected Translation does not contain the requested Passage, THEN THE App SHALL display the Passage in the next available Translation and SHALL notify the User which Translation is being used.
5. THE App SHALL persist the User's Translation preference across sessions.

---

### Requirement 6: Group Sharing

**User Story:** As a User, I want to share a devotional with my men's group, so that we can study the same content together and discuss it.

#### Acceptance Criteria

1. THE Share_Service SHALL allow a User to share a published Devotional with one or more Groups of which the User is a member.
2. WHEN a Devotional is shared with a Group, THE Share_Service SHALL deliver a notification containing the Devotional title, the first-listed Passage reference as the primary Passage reference, and a deep link to the Devotional to all members of that Group.
3. THE App SHALL allow a User to create a Group by providing a group name of 1 to 50 characters that is unique across the platform, and SHALL generate an invite code that expires 7 days after generation and that other Users can use to join the Group.
4. WHEN a User joins a Group using a valid, non-expired invite code, THE App SHALL add the User to the Group and SHALL display the Group's shared Devotional history.
5. IF an invite code does not match any issued code or has passed its 7-day expiry, THEN THE App SHALL display an error message indicating the code is invalid or expired and SHALL NOT add the User to any Group.
6. IF a User attempts to create a Group with a name that already exists on the platform, THEN THE App SHALL display an error message indicating the name is already taken and SHALL NOT create the Group.
7. THE App SHALL allow a Group member to view all Devotionals previously shared with that Group, sorted by share date descending.
8. IF a User attempts to share a Devotional that has already been shared with the same Group, THEN THE Share_Service SHALL display an error message indicating the Devotional has already been shared with that Group and SHALL NOT create a duplicate share entry.
9. IF THE Share_Service fails to deliver a notification to one or more Group members, THEN THE Share_Service SHALL record the failed delivery and SHALL still complete the share action; the Devotional SHALL appear in the Group's shared Devotional history regardless of notification delivery outcome.
10. WHERE a Group has designated a Group Leader, THE App SHALL allow the Group Leader to remove members from the Group.

---

### Requirement 7: User Accounts and Preferences

**User Story:** As a User, I want a personal account so that my preferences, group memberships, and reading history are saved across devices.

#### Acceptance Criteria

1. THE App SHALL require a User to create an account with a unique email address and a password of 8 to 128 characters before accessing Group features.
2. WHEN a User creates an account, THE App SHALL send a verification email to the provided address within 60 seconds of account creation; the verification link SHALL remain valid for 24 hours.
3. IF a User attempts to log in with an email address and password combination that does not match any account, THEN THE App SHALL display an error message indicating the credentials are invalid and SHALL NOT grant access; after 5 consecutive failed login attempts for the same email address, THE App SHALL lock that account for 15 minutes and SHALL display a message indicating the account is temporarily locked.
4. THE App SHALL allow a User to browse Topics and read Devotionals without creating an account.
5. THE App SHALL persist the following User preferences across sessions and across all devices on which the User is signed in: selected Translation, notification preferences, and bookmarked Devotionals; changes made on one device SHALL be reflected on all other signed-in devices within 30 seconds.
6. WHEN a User bookmarks a Devotional, THE App SHALL atomically add it to the User's saved list and update the saved section display so that both the list and the UI reflect the addition at the same time.
7. IF a User attempts to access Group features without a verified account, THEN THE App SHALL prompt the User to verify their email and SHALL NOT grant access to Group features.
8. IF a verification email has not been acted upon within 24 hours, THEN THE App SHALL allow the User to request a new verification email, and THE App SHALL invalidate the previously issued verification link upon sending the new one.

---

### Requirement 9: Enduring Word Commentary (David Guzik)

**User Story:** As a User, I want to access David Guzik's commentary for any Bible chapter, so that I can go deeper into the meaning and context of the passage I'm studying.

#### Acceptance Criteria

1. WHEN a User is viewing any Bible chapter or Devotional passage, THE App SHALL display a "Commentary" button that opens the corresponding Enduring Word commentary page.
2. THE App SHALL construct the commentary URL using the pattern `https://enduringword.com/bible-commentary/{book-slug}-{chapter}/` where `book-slug` is the book's designated slug (e.g., `genesis`, `1-samuel`, `psalm`, `1-corinthians`) and `chapter` is the chapter number.
3. WHEN a User taps the Commentary button, THE App SHALL open the URL in the device's default browser or an in-app browser view.
4. THE App SHALL use the slug `psalm` (singular) for Psalms and hyphenated slugs for numbered books (e.g., `1-samuel`, `2-kings`, `1-corinthians`).
5. IF the commentary URL returns an error or is unreachable, THE App SHALL display a message indicating the commentary is currently unavailable and SHALL provide the URL as a fallback so the User can open it manually.
6. THE App SHALL display attribution text "Commentary by David Guzik — enduringword.com" adjacent to the Commentary button.

---

### Requirement 8: Daily Devotional

**User Story:** As a User, I want a daily devotional delivered to me, so that I stay consistent in my study without having to search every day.

#### Acceptance Criteria

1. THE App SHALL surface one published Devotional per day as the "Daily Devotional" on the home screen.
2. WHEN a new calendar day begins in the device's local timezone, THE App SHALL update the Daily Devotional to a different published Devotional than the one displayed the previous day.
3. THE App SHALL prepare Daily Devotional notification content — including the Devotional title and the first-listed Passage reference as the primary Passage reference — regardless of whether the User has enabled push notifications. WHERE a User has enabled push notifications, THE App SHALL deliver that content as a push notification at the User's configured time each day; the configurable time SHALL be a value between 12:00 AM and 11:59 PM in the device's local timezone, and SHALL default to 8:00 AM local time if the User has not configured a time.
4. WHEN the rolling window is set to a value between 1 and 365 days inclusive, THE App SHALL ensure that the same Devotional is not repeated as the Daily Devotional within that rolling window; IF the pool of published Devotionals not appearing in the rolling window is exhausted, THEN THE App SHALL select the least-recently-used published Devotional as the Daily Devotional. WHEN the rolling window is set to 0 days, THE App SHALL allow immediate repetition of any published Devotional.
5. WHEN a User taps the Daily Devotional notification, THE App SHALL open directly to that Devotional's full view.
6. IF the Devotional designated as the Daily Devotional is no longer in a published state at the time a User opens the home screen, THEN THE App SHALL select the next eligible published Devotional according to the rolling window rules and SHALL display it as the Daily Devotional for the remainder of that calendar day.
