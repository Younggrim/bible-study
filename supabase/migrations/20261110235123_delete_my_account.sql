-- "Delete my account": lets a signed-in person remove their own account and
-- everything saved with it, from the site, without asking anyone.
--
-- Deleting the auth.users row removes their memory_verses, verse_marks and
-- reading_position rows too (every table references auth.users with
-- ON DELETE CASCADE), along with their sign-in sessions.
--
-- security definer is what lets the function reach auth.users, which the
-- authenticated role cannot touch directly. It only ever acts on
-- auth.uid(), the caller's own id, so nobody can delete anyone else.

create function public.delete_my_account() returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
begin
  if me is null then
    raise exception 'Not signed in.' using errcode = 'insufficient_privilege';
  end if;
  delete from auth.users where id = me;
end;
$$;

comment on function public.delete_my_account() is
  'Deletes the calling user''s account and, by cascade, all of their saved study. Acts only on auth.uid().';

revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
