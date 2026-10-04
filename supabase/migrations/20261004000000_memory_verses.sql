-- Scripture Memory: one row per verse a signed-in person is memorizing.
-- The client keeps the same shape in localStorage (see docs/memory.html) and
-- syncs to this table when signed in. Rows are never shared between users.

create table public.memory_verses (
  user_id        uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  id             text        not null check (id ~ '^[A-Za-z0-9_-]{1,40}$'),
  ref            text        not null check (char_length(ref) between 1 and 120),
  text           text        not null check (char_length(text) between 1 and 6000),
  translation    text        not null default 'ESV' check (char_length(translation) between 1 and 12),
  stage          text        not null default 'learning' check (stage in ('learning', 'review')),
  fade_step      smallint    not null default 0 check (fade_step between 0 and 5),
  interval_days  smallint    not null default 0 check (interval_days between 0 and 180),
  ease           numeric(4,2) not null default 2.5 check (ease between 1.3 and 4),
  reps           integer     not null default 0 check (reps >= 0),
  lapses         integer     not null default 0 check (lapses >= 0),
  due            date,
  last_reviewed  date,
  added_at       timestamptz not null default now(),
  updated_at     timestamptz not null default now(),
  -- Soft delete, so a verse removed on one device is also removed on the others.
  deleted_at     timestamptz,
  primary key (user_id, id)
);

comment on table public.memory_verses is
  'Scripture Memory verses and their review schedule, one row per user per verse. Private to the owning user (RLS).';

-- updated_at is always the server''s clock, so devices never argue about time.
create function public.memory_verses_touch() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

create trigger memory_verses_touch
  before insert or update on public.memory_verses
  for each row execute function public.memory_verses_touch();

-- Keep one account from filling the database: at most 1,000 verses each.
create function public.memory_verses_cap() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.memory_verses where user_id = new.user_id) >= 1000 then
    raise exception 'Verse limit reached (1000 per account).' using errcode = 'check_violation';
  end if;
  return new;
end;
$$;

create trigger memory_verses_cap
  before insert on public.memory_verses
  for each row execute function public.memory_verses_cap();

alter table public.memory_verses enable row level security;

revoke all on public.memory_verses from anon;
revoke all on public.memory_verses from authenticated;
grant select, insert, update, delete on public.memory_verses to authenticated;

create policy "Read own verses" on public.memory_verses
  for select to authenticated using (user_id = (select auth.uid()));

create policy "Add own verses" on public.memory_verses
  for insert to authenticated with check (user_id = (select auth.uid()));

create policy "Change own verses" on public.memory_verses
  for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

create policy "Delete own verses" on public.memory_verses
  for delete to authenticated using (user_id = (select auth.uid()));
