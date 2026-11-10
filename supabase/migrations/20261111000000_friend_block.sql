-- Blocking: stop one person from sending you friend requests.
--
-- A block is private to the person who made it. The blocked person is not
-- told: their later requests answer 'sent' like any other and simply never
-- arrive. Blocking also ends a friendship or a waiting request between the
-- two. You can only block someone you have had a request or friendship
-- with, so nobody can be blocked (or probed) by a guessed id.
--
-- Blocks live in their own table rather than on friendships, because both
-- people can read their friendships row and the blocked person must not be
-- able to see the block.

create table public.friend_blocks (
  blocker     uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  blocked     uuid        not null references auth.users (id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (blocker, blocked),
  check (blocker <> blocked)
);
comment on table public.friend_blocks is 'People someone has blocked from sending friend requests. Private to the blocker; changed only through friend_block() and friend_unblock().';
create index friend_blocks_blocked on public.friend_blocks (blocked);

alter table public.friend_blocks enable row level security;
revoke all on public.friend_blocks from anon;
revoke all on public.friend_blocks from authenticated;
grant select on public.friend_blocks to authenticated;
grant select, insert, update, delete on public.friend_blocks to service_role;

create policy "Own blocks read" on public.friend_blocks for select to authenticated
  using (blocker = (select auth.uid()));

-- Block someone I have a request or friendship with (now or in the past).
-- Returns 'blocked', 'self' or 'none' (no history with that person).
create function public.friend_block(other uuid) returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
begin
  if me is null then raise exception 'Not signed in.' using errcode = 'insufficient_privilege'; end if;
  if other is null then return 'none'; end if;
  if other = me then return 'self'; end if;
  if not exists (select 1 from public.friendships
                  where user_a = least(me, other) and user_b = greatest(me, other)) then
    return 'none';
  end if;
  insert into public.friend_blocks (blocker, blocked) values (me, other) on conflict do nothing;
  update public.friendships set status = 'removed'
   where user_a = least(me, other) and user_b = greatest(me, other) and status <> 'removed';
  return 'blocked';
end;
$$;

-- Undo a block. They can send a request again; nothing else is restored.
create function public.friend_unblock(other uuid) returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
begin
  if me is null then raise exception 'Not signed in.' using errcode = 'insufficient_privilege'; end if;
  delete from public.friend_blocks where blocker = me and blocked = other;
  return case when found then 'unblocked' else 'none' end;
end;
$$;

-- The people I have blocked, so I can unblock them.
create function public.friends_blocked()
returns table (friend uuid, display_name text, blocked_at timestamptz)
language sql
stable
security definer
set search_path = ''
as $$
  select b.blocked, coalesce(p.display_name, ''), b.created_at
    from public.friend_blocks b
    left join public.friend_profiles p on p.user_id = b.blocked
   where b.blocker = auth.uid()
   order by b.created_at desc;
$$;

-- friend_request, as before, with two additions: a request to someone who
-- has blocked me answers 'sent' and does nothing, and a request to someone
-- I have blocked answers 'blocked' (unblock them first).
create or replace function public.friend_request(friend_code text) returns text
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
  if exists (select 1 from public.friend_blocks where blocker = me and blocked = them) then return 'blocked'; end if;
  if exists (select 1 from public.friend_blocks where blocker = them and blocked = me) then return 'sent'; end if;
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

revoke all on function public.friend_block(uuid), public.friend_unblock(uuid), public.friends_blocked() from public, anon;
grant execute on function public.friend_block(uuid), public.friend_unblock(uuid), public.friends_blocked() to authenticated;
