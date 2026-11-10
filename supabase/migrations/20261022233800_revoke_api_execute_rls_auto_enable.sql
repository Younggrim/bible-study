-- rls_auto_enable() is a helper on the hosted project (it is not created by
-- any migration in this repo). Nobody should be able to call it through the
-- API. Applied to the hosted project on 22 Oct 2026; recorded here on
-- 10 Nov 2026 so the repo matches it. On a database built only from these
-- migrations the function does not exist, so skip this file there.

revoke execute on function public.rls_auto_enable() from public, anon, authenticated;
