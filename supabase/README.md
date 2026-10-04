# Supabase (accounts and saved study)

Project "Bible Study", ref `vqgumrfjxlhkzzzfgejl`, free plan, US East (N. Virginia),
in the same organization as Upheld but a separate project and database.

The site is static. Signing in is optional: `docs/site/account.js` holds the
project URL and publishable key (both public by design) and the sign-in dialog.
Every table has Row Level Security so a signed-in person reaches only their own
rows. Never commit a service-role or secret key.

    migrations/   schema and RLS policies, in order (already applied to the hosted project)
    tests/        rls_privacy_test.sql: signs in as two fake users and checks neither can
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
