-- Chapters studied, study streaks and notes.
-- The client keeps the same data in localStorage (docs/site/study.js and
-- docs/notes.html) and syncs here when signed in. Private to each user.
-- Grants are explicit, as Supabase requires for tables made after 30 Oct 2026.

-- One row per chapter a person has marked studied. Unmarking sets removed
-- rather than deleting, so the change reaches their other devices.
create table public.chapters_studied (
  user_id     uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  page        text        not null check (page ~ '^[1-3]?[a-z]{2,20}[0-9]{1,3}$'),
  studied_on  date        not null,
  removed     boolean     not null default false,
  updated_at  timestamptz not null default now(),
  primary key (user_id, page)
);
comment on table public.chapters_studied is
  'Chapters each person has marked studied. Private to the owning user (RLS).';
create index chapters_studied_user_updated on public.chapters_studied (user_id, updated_at);

-- One row per day a person studied (their own local date). The streak is
-- the run of consecutive days ending today or yesterday. Days are only ever
-- added, so a streak is never lost by unmarking a chapter.
create table public.study_days (
  user_id     uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  day         date        not null,
  updated_at  timestamptz not null default now(),
  primary key (user_id, day)
);
comment on table public.study_days is
  'Days each person studied, for streaks. Private to the owning user (RLS).';
create index study_days_user_updated on public.study_days (user_id, updated_at);

-- Notes. ref is an optional passage the note is about, e.g. "luke6:20".
-- Soft delete (deleted_at) so a note removed on one device goes everywhere.
create table public.notes (
  user_id     uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  id          text        not null check (id ~ '^[A-Za-z0-9_-]{1,40}$'),
  ref         text        check (ref is null or ref ~ '^[1-3]?[a-z]{2,20}[0-9]{1,3}(:[0-9]{1,3})?$'),
  title       text        not null default '' check (char_length(title) <= 200),
  body        text        not null default '' check (char_length(body) <= 20000),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  deleted_at  timestamptz,
  primary key (user_id, id)
);
comment on table public.notes is
  'Personal study notes. Private to the owning user (RLS).';
create index notes_user_updated on public.notes (user_id, updated_at);

create trigger chapters_studied_touch before insert or update on public.chapters_studied
  for each row execute function public.study_touch();
create trigger study_days_touch before insert or update on public.study_days
  for each row execute function public.study_touch();
create trigger notes_touch before insert or update on public.notes
  for each row execute function public.study_touch();

-- Size limits per account.
create function public.notes_cap() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.notes where user_id = new.user_id) >= 5000 then
    raise exception 'Note limit reached (5000 per account).' using errcode = 'check_violation';
  end if;
  return new;
end;
$$;
create trigger notes_cap before insert on public.notes
  for each row execute function public.notes_cap();

alter table public.chapters_studied enable row level security;
alter table public.study_days enable row level security;
alter table public.notes enable row level security;

revoke all on public.chapters_studied, public.study_days, public.notes from anon;
revoke all on public.chapters_studied, public.study_days, public.notes from authenticated;
grant select, insert, update, delete on public.chapters_studied, public.study_days, public.notes to authenticated;
grant select, insert, update, delete on public.chapters_studied, public.study_days, public.notes to service_role;

create policy "Read own chapters" on public.chapters_studied for select to authenticated using (user_id = (select auth.uid()));
create policy "Add own chapters" on public.chapters_studied for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Change own chapters" on public.chapters_studied for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy "Read own days" on public.study_days for select to authenticated using (user_id = (select auth.uid()));
create policy "Add own days" on public.study_days for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Change own days" on public.study_days for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy "Read own notes" on public.notes for select to authenticated using (user_id = (select auth.uid()));
create policy "Add own notes" on public.notes for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Change own notes" on public.notes for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
