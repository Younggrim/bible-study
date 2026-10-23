# Supabase (accounts and saved study)

Project "Bible Study", ref `vqgumrfjxlhkzzzfgejl`, free plan, US East (N. Virginia),
in the same organization as Upheld but a separate project and database.

The site is static. Signing in is optional: `docs/site/account.js` holds the
project URL and publishable key (both public by design) and the sign-in dialog.
Every table has Row Level Security so a signed-in person reaches only their own
rows. Never commit a service-role or secret key.

Tables: `memory_verses` (Memory tab), `verse_marks` (highlights and
bookmarks), `reading_position`, `chapters_studied` and `study_days` (streaks),
`notes`, `reading_plans`, and for Friends `friend_profiles`, `friendships`,
`friend_stats`, `shared_items` with the functions `friend_request`,
`friend_respond`, `friend_remove`, `friends_list` and `friends_feed`.
`delete_my_account()` removes a person's account and, by cascade, all of it.

    migrations/   schema and RLS policies, in order (already applied to the hosted project)
    tests/        friends_test.sql: three fake users; friends see each other only after both accept.
                  rls_privacy_test.sql: signs in as two fake users and checks neither can
                  read, change, delete or take over the other's rows. Runs in a
                  transaction that always rolls back.

Run the privacy test against the hosted project:

    psql "$DATABASE_URL" -f supabase/tests/rls_privacy_test.sql

It prints `PRIVACY_TEST ALL PASSED` (as an error message, which is what rolls it
back) or lists what failed.

## Sign-in email (dashboard settings, not in this repo)

Sign-in is passwordless: email, then a 6-digit code typed into the page.
In the Supabase dashboard for this project:

1. Authentication > Emails > SMTP Settings: enable custom SMTP with the Resend
   account Upheld uses (host smtp.resend.com, port 465, user `resend`, password =
   a Resend API key). Without this, Supabase only emails the project's own team,
   two messages an hour.
2. Authentication > Emails > Templates: both **Magic Link** and **Confirm signup**
   must show the code, `{{ .Token }}`, not only a link. (A first-time sign-in can
   be sent with the Confirm signup template.) Copying Upheld's templates works.
3. Authentication > Sign In / Providers > Email: OTP length 6.

## Free plan pauses the project

On the free plan Supabase pauses a project after about a week with no
traffic. While paused, sign-in and syncing fail quietly (pages keep working
from what is saved on the device). It was found paused and restored on
21 Oct 2026. If sign-in stops working, check the project status first.

## Edge Function: bible-audio (Listen button)

`functions/bible-audio` finds an official recording of a chapter for the
Listen button (`docs/site/audio.js`). It returns the publisher's MP3 URL, never
audio bytes, and holds the API keys so the static site never sees them.

    ESV          ESV API /v3/passage/audio/ (the redirect target is returned)
    everything   Bible Brain (Faith Comes By Hearing), only for translations
    else         mapped in BIBLE_BRAIN in handler.ts to the same edition
    no match     {"source":"none"}: the page uses the device's speech voice

Secrets (Dashboard > Edge Functions > Secrets, or the CLI):

    supabase secrets set --project-ref vqgumrfjxlhkzzzfgejl ESV_API_TOKEN=...    # same token as esv-proxy-worker
    supabase secrets set --project-ref vqgumrfjxlhkzzzfgejl BIBLE_BRAIN_KEY=...  # optional; without it, no Bible Brain audio

Deploy (JWT verification off, see config.toml):

    supabase functions deploy bible-audio --no-verify-jwt --project-ref vqgumrfjxlhkzzzfgejl

Before relying on Bible Brain, confirm the ID table against the real catalogue:

    BIBLE_BRAIN_KEY=... python3 find_bible_brain_audio.py

Tests (Node 22, no keys or network):

    node --experimental-strip-types --test supabase/functions/bible-audio/handler.test.mjs
