-- Friends test: three fake users. Checks that a request needs both sides,
-- that nothing about a friend is visible before acceptance or after removal,
-- that a stranger sees nothing, that "share progress" off hides the numbers,
-- and that nobody reads another person's friend tables directly.
-- Everything is rolled back by the final RAISE.
--
--   psql "$DATABASE_URL" -f supabase/tests/friends_test.sql
do $$
declare
  a uuid := gen_random_uuid(); b uuid := gen_random_uuid(); c uuid := gen_random_uuid();
  n int; r text; failed text := '';
begin
  insert into auth.users (id, instance_id, aud, role, email) values
    (a, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'fa@example.invalid'),
    (b, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'fb@example.invalid'),
    (c, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'fc@example.invalid');
  set local role authenticated;
  perform set_config('request.jwt.claims', json_build_object('sub', b, 'role', 'authenticated')::text, true);
  insert into public.friend_profiles (code, display_name) values ('BBBBBBBB', 'Bee');
  insert into public.friend_stats (streak, chapters, current_page) values (7, 40, 'john3');
  insert into public.shared_items (kind, ref, title, body) values ('note', 'john3:16', 'Love', 'So loved');
  perform set_config('request.jwt.claims', json_build_object('sub', c, 'role', 'authenticated')::text, true);
  insert into public.friend_profiles (code, display_name) values ('CCCCCCCC', 'Cee');
  perform set_config('request.jwt.claims', json_build_object('sub', a, 'role', 'authenticated')::text, true);
  begin r := public.friend_request('BBBBBBBB'); failed := failed || ' request-without-profile;';
  exception when check_violation then null; end;
  insert into public.friend_profiles (code, display_name) values ('AAAAAAAA', 'Ay');
  r := public.friend_request('bbbb-bbbb'); if r <> 'sent' then failed := failed || ' send:' || r || ';'; end if;
  r := public.friend_request('ZZZZZZZZ'); if r <> 'not_found' then failed := failed || ' notfound:' || r || ';'; end if;
  r := public.friend_request('AAAAAAAA'); if r <> 'self' then failed := failed || ' self:' || r || ';'; end if;
  select count(*) into n from public.friends_list() where status = 'pending' and not incoming; if n <> 1 then failed := failed || ' A-outgoing;'; end if;
  select count(*) into n from public.friends_list() where streak is not null; if n <> 0 then failed := failed || ' stats-before-accept;'; end if;
  select count(*) into n from public.friends_feed(); if n <> 0 then failed := failed || ' feed-before-accept;'; end if;
  r := public.friend_respond(b, true); if r <> 'none' then failed := failed || ' self-accept;'; end if;
  select count(*) into n from public.friend_stats; if n <> 0 then failed := failed || ' A-reads-stats-table;'; end if;
  select count(*) into n from public.shared_items; if n <> 0 then failed := failed || ' A-reads-shares-table;'; end if;
  select count(*) into n from public.friend_profiles; if n <> 1 then failed := failed || ' A-reads-profiles;'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', b, 'role', 'authenticated')::text, true);
  select count(*) into n from public.friends_list() where incoming; if n <> 1 then failed := failed || ' B-incoming;'; end if;
  r := public.friend_respond(a, true); if r <> 'accepted' then failed := failed || ' accept:' || r || ';'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', a, 'role', 'authenticated')::text, true);
  select count(*) into n from public.friends_list() where status = 'accepted' and streak = 7 and chapters = 40 and display_name = 'Bee'; if n <> 1 then failed := failed || ' A-sees-B-stats;'; end if;
  select count(*) into n from public.friends_feed() where title = 'Love'; if n <> 1 then failed := failed || ' A-feed;'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', c, 'role', 'authenticated')::text, true);
  select count(*) into n from public.friends_list(); if n <> 0 then failed := failed || ' C-list;'; end if;
  select count(*) into n from public.friends_feed(); if n <> 0 then failed := failed || ' C-feed;'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', b, 'role', 'authenticated')::text, true);
  update public.friend_profiles set share_progress = false;
  perform set_config('request.jwt.claims', json_build_object('sub', a, 'role', 'authenticated')::text, true);
  select count(*) into n from public.friends_list() where display_name = 'Bee' and streak is null; if n <> 1 then failed := failed || ' share-off;'; end if;
  r := public.friend_remove(b);
  select count(*) into n from public.friends_feed(); if n <> 0 then failed := failed || ' feed-after-remove;'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', b, 'role', 'authenticated')::text, true);
  select count(*) into n from public.friends_list(); if n <> 0 then failed := failed || ' B-list-after-remove;'; end if;
  reset role;
  set local role anon;
  begin perform public.friends_list(); failed := failed || ' anon-list;'; exception when insufficient_privilege then null; end;
  begin select count(*) into n from public.friend_profiles; failed := failed || ' anon-profiles;'; exception when insufficient_privilege then null; end;
  reset role;
  raise exception 'FRIENDS_TEST %', case when failed = '' then 'ALL PASSED' else 'FAILED:' || failed end;
end $$;
