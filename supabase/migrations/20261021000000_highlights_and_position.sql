-- Highlights, bookmarks and "pick up where you left off".
-- The client keeps the same data in localStorage (see docs/site/study.js) so
-- it works with no account and offline, and syncs here when signed in.
-- Rows are never shared between users.

-- One row per verse a person has marked. A highlight is a colour, a bookmark
-- is a flag; a row with neither is a cleared mark, kept (instead of deleted)
-- so the clearing reaches the person's other devices on their next sync.
create table public.verse_marks (
  user_id     uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  book        text        not null check (book ~ '^[1-3]?[a-z]{2,20}$'),
  chapter     smallint    not null check (chapter between 1 and 150),
  verse       smallint    not null check (verse between 1 and 176),
  color       text        check (color in ('yellow', 'green', 'blue', 'pink')),
  bookmarked  boolean     not null default false,
  updated_at  timestamptz not null default now(),
  primary key (user_id, book, chapter, verse)
);

comment on table public.verse_marks is
  'Verse highlights and bookmarks, one row per user per verse. Private to the owning user (RLS).';

create index verse_marks_user_updated on public.verse_marks (user_id, updated_at);

-- The last place a person was reading, one row per person.
create table public.reading_position (
  user_id     uuid        primary key default auth.uid() references auth.users (id) on delete cascade,
  page        text        not null check (page ~ '^[1-3]?[a-z]{2,20}[0-9]{1,3}$'),
  verse       smallint    check (verse between 1 and 176),
  updated_at  timestamptz not null default now()
);

comment on table public.reading_position is
  'Where each person last left off reading. Private to the owning user (RLS).';

-- updated_at is always the server's clock, so devices never argue about time.
create function public.study_touch() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

create trigger verse_marks_touch before insert or update on public.verse_marks
  for each row execute function public.study_touch();
create trigger reading_position_touch before insert or update on public.reading_position
  for each row execute function public.study_touch();

-- Keep one account from filling the database: at most 20,000 marked verses
-- (more than every verse of the New Testament twice over).
create function public.verse_marks_cap() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.verse_marks where user_id = new.user_id) >= 20000 then
    raise exception 'Highlight limit reached (20000 per account).' using errcode = 'check_violation';
  end if;
  return new;
end;
$$;

create trigger verse_marks_cap before insert on public.verse_marks
  for each row execute function public.verse_marks_cap();

alter table public.verse_marks enable row level security;
alter table public.reading_position enable row level security;

revoke all on public.verse_marks, public.reading_position from anon;
revoke all on public.verse_marks, public.reading_position from authenticated;
grant select, insert, update, delete on public.verse_marks, public.reading_position to authenticated;

create policy "Read own marks" on public.verse_marks
  for select to authenticated using (user_id = (select auth.uid()));
create policy "Add own marks" on public.verse_marks
  for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Change own marks" on public.verse_marks
  for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));
create policy "Delete own marks" on public.verse_marks
  for delete to authenticated using (user_id = (select auth.uid()));

create policy "Read own position" on public.reading_position
  for select to authenticated using (user_id = (select auth.uid()));
create policy "Add own position" on public.reading_position
  for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Change own position" on public.reading_position
  for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));
create policy "Delete own position" on public.reading_position
  for delete to authenticated using (user_id = (select auth.uid()));
