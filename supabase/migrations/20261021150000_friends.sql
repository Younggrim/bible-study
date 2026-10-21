-- Friends: connect by a private friend code, both sides accept, then see
-- each other's streak and progress (if they choose to share it) and
-- anything they share one item at a time.
--
-- The tables are private to their owner. Everything a person sees about a
-- friend comes through the security definer functions below, which check
-- for an accepted friendship first, so no table is ever readable by
-- another user directly. Removing a friend or unsharing sets a status
-- rather than deleting rows. Grants are explicit (Supabase, Oct 2026).

-- The friend profile: the name friends see and the code that finds you.
create table public.friend_profiles (
  user_id         uuid        primary key default auth.uid() references auth.users (id) on delete cascade,
  code            text        not null unique check (code ~ '^[A-HJ-NP-Z2-9]{8}$'),
  display_name    text        not null check (char_length(btrim(display_name)) between 1 and 40),
  share_progress  boolean     not null default true,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
comment on table public.friend_profiles is 'Friend code and display name. Private to the owner; friends see the name through friends_list().';

-- One row per pair of people, smaller id first.
create table public.friendships (
  user_a        uuid        not null references auth.users (id) on delete cascade,
  user_b        uuid        not null references auth.users (id) on delete cascade,
  requested_by  uuid        not null references auth.users (id) on delete cascade,
  status        text        not null check (status in ('pending', 'accepted', 'removed')),
  updated_at    timestamptz not null default now(),
  primary key (user_a, user_b),
  check (user_a < user_b),
  check (requested_by in (user_a, user_b))
);
comment on table public.friendships is 'Friend requests and friendships. Changed only through the friend functions.';

-- What a person shares about their study with friends.
create table public.friend_stats (
  user_id       uuid        primary key default auth.uid() references auth.users (id) on delete cascade,
  streak        integer     not null default 0 check (streak between 0 and 100000),
  chapters      integer     not null default 0 check (chapters between 0 and 1189),
  current_page  text        check (current_page is null or current_page ~ '^[1-3]?[a-z]{2,20}[0-9]{1,3}$'),
  updated_at    timestamptz not null default now()
);
comment on table public.friend_stats is 'Streak and progress a person shows their friends. Private to the owner; friends read it through friends_list().';

-- Highlights and notes shared with friends, one at a time.
create table public.shared_items (
  id          uuid        primary key default gen_random_uuid(),
  owner       uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  kind        text        not null check (kind in ('verse', 'note')),
  ref         text        check (ref is null or ref ~ '^[1-3]?[a-z]{2,20}[0-9]{1,3}(:[0-9]{1,3})?$'),
  title       text        not null default '' check (char_length(title) <= 200),
  body        text        not null default '' check (char_length(body) <= 2000),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  removed     boolean     not null default false
);
comment on table public.shared_items is 'Items a person shared with their friends. Private to the owner; friends read them through friends_feed().';
create index shared_items_owner_created on public.shared_items (owner, created_at desc);

create trigger friend_profiles_touch before insert or update on public.friend_profiles for each row execute function public.study_touch();
create trigger friendships_touch before insert or update on public.friendships for each row execute function public.study_touch();
create trigger friend_stats_touch before insert or update on public.friend_stats for each row execute function public.study_touch();
create trigger shared_items_touch before insert or update on public.shared_items for each row execute function public.study_touch();

alter table public.friend_profiles enable row level security;
alter table public.friendships enable row level security;
alter table public.friend_stats enable row level security;
alter table public.shared_items enable row level security;

revoke all on public.friend_profiles, public.friendships, public.friend_stats, public.shared_items from anon;
revoke all on public.friend_profiles, public.friendships, public.friend_stats, public.shared_items from authenticated;
grant select, insert, update on public.friend_profiles, public.friend_stats, public.shared_items to authenticated;
grant select on public.friendships to authenticated;
grant select, insert, update, delete on public.friend_profiles, public.friendships, public.friend_stats, public.shared_items to service_role;

create policy "Own profile read" on public.friend_profiles for select to authenticated using (user_id = (select auth.uid()));
create policy "Own profile add" on public.friend_profiles for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Own profile change" on public.friend_profiles for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy "Own friendships read" on public.friendships for select to authenticated
  using ((select auth.uid()) in (user_a, user_b));

create policy "Own stats read" on public.friend_stats for select to authenticated using (user_id = (select auth.uid()));
create policy "Own stats add" on public.friend_stats for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Own stats change" on public.friend_stats for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy "Own shares read" on public.shared_items for select to authenticated using (owner = (select auth.uid()));
create policy "Own shares add" on public.shared_items for insert to authenticated with check (owner = (select auth.uid()));
create policy "Own shares change" on public.shared_items for update to authenticated
  using (owner = (select auth.uid())) with check (owner = (select auth.uid()));

-- Shares are capped so one account cannot fill the database.
create function public.shared_items_cap() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.shared_items where owner = new.owner) >= 2000 then
    raise exception 'Share limit reached (2000 per account).' using errcode = 'check_violation';
  end if;
  return new;
end;
$$;
create trigger shared_items_cap before insert on public.shared_items for each row execute function public.shared_items_cap();

-- Send a request to the person with this code, or accept theirs if they
-- already asked. Returns 'sent', 'accepted', 'already', 'self' or 'not_found'.
create function public.friend_request(friend_code text) returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
  them uuid;
  a uuid;
  b uuid;
  f public.friendships%rowtype;
begin
  if me is null then raise exception 'Not signed in.' using errcode = 'insufficient_privilege'; end if;
  if not exists (select 1 from public.friend_profiles where user_id = me) then
    raise exception 'Set up your friend profile first.' using errcode = 'check_violation';
  end if;
  select user_id into them from public.friend_profiles where code = upper(regexp_replace(coalesce(friend_code, ''), '[^A-Za-z0-9]', '', 'g'));
  if them is null then return 'not_found'; end if;
  if them = me then return 'self'; end if;
  a := least(me, them); b := greatest(me, them);
  select * into f from public.friendships where user_a = a and user_b = b;
  if not found then
    insert into public.friendships (user_a, user_b, requested_by, status) values (a, b, me, 'pending');
    return 'sent';
  end if;
  if f.status = 'accepted' then return 'already'; end if;
  if f.status = 'pending' and f.requested_by = them then
    update public.friendships set status = 'accepted' where user_a = a and user_b = b;
    return 'accepted';
  end if;
  if f.status = 'pending' then return 'already'; end if;
  update public.friendships set status = 'pending', requested_by = me where user_a = a and user_b = b;
  return 'sent';
end;
$$;

-- Accept or decline a request someone sent me.
create function public.friend_respond(other uuid, accept boolean) returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
begin
  if me is null then raise exception 'Not signed in.' using errcode = 'insufficient_privilege'; end if;
  update public.friendships
     set status = case when accept then 'accepted' else 'removed' end
   where user_a = least(me, other) and user_b = greatest(me, other)
     and status = 'pending' and requested_by = other;
  if not found then return 'none'; end if;
  return case when accept then 'accepted' else 'declined' end;
end;
$$;

-- Remove a friend, or cancel a request I sent.
create function public.friend_remove(other uuid) returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
begin
  if me is null then raise exception 'Not signed in.' using errcode = 'insufficient_privilege'; end if;
  update public.friendships set status = 'removed'
   where user_a = least(me, other) and user_b = greatest(me, other) and status <> 'removed';
  return case when found then 'removed' else 'none' end;
end;
$$;

-- My friends and requests, with each accepted friend's shared progress.
create function public.friends_list()
returns table (friend uuid, display_name text, status text, incoming boolean,
               streak integer, chapters integer, current_page text, stats_at timestamptz)
language sql
stable
security definer
set search_path = ''
as $$
  select o.other, p.display_name, f.status, (f.status = 'pending' and f.requested_by = o.other),
         case when f.status = 'accepted' and p.share_progress then s.streak end,
         case when f.status = 'accepted' and p.share_progress then s.chapters end,
         case when f.status = 'accepted' and p.share_progress then s.current_page end,
         case when f.status = 'accepted' and p.share_progress then s.updated_at end
    from public.friendships f
    cross join lateral (select case when f.user_a = auth.uid() then f.user_b else f.user_a end as other) o
    join public.friend_profiles p on p.user_id = o.other
    left join public.friend_stats s on s.user_id = o.other
   where auth.uid() in (f.user_a, f.user_b) and f.status in ('pending', 'accepted')
   order by f.status, p.display_name;
$$;

-- What my accepted friends have shared, newest first.
create function public.friends_feed(max_items integer default 50)
returns table (id uuid, owner uuid, display_name text, kind text, ref text, title text, body text, created_at timestamptz)
language sql
stable
security definer
set search_path = ''
as $$
  select i.id, i.owner, p.display_name, i.kind, i.ref, i.title, i.body, i.created_at
    from public.shared_items i
    join public.friend_profiles p on p.user_id = i.owner
   where not i.removed
     and exists (select 1 from public.friendships f
                  where f.status = 'accepted'
                    and f.user_a = least(auth.uid(), i.owner) and f.user_b = greatest(auth.uid(), i.owner))
   order by i.created_at desc
   limit least(greatest(coalesce(max_items, 50), 1), 200);
$$;

revoke all on function public.friend_request(text), public.friend_respond(uuid, boolean), public.friend_remove(uuid),
                       public.friends_list(), public.friends_feed(integer) from public, anon;
grant execute on function public.friend_request(text), public.friend_respond(uuid, boolean), public.friend_remove(uuid),
                       public.friends_list(), public.friends_feed(integer) to authenticated;
