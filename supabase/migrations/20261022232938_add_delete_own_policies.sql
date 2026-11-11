-- Lets a signed-in person delete their own rows in the tables that were
-- created with a DELETE grant but no DELETE policy. Applied to the hosted
-- project on 22 Oct 2026; recorded here on 10 Nov 2026 so the repo matches it.

create policy "Delete own notes" on public.notes for delete to authenticated using (user_id = (select auth.uid()));
create policy "Delete own chapters" on public.chapters_studied for delete to authenticated using (user_id = (select auth.uid()));
create policy "Delete own plan" on public.reading_plans for delete to authenticated using (user_id = (select auth.uid()));
create policy "Delete own days" on public.study_days for delete to authenticated using (user_id = (select auth.uid()));
