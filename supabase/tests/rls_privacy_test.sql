-- Privacy test for memory_verses. Signs in as two fake users and checks that
-- neither can read, change, delete or take over the other's rows, and that
-- signed-out visitors get nothing. Everything is rolled back: the final
-- RAISE carries the verdict and undoes the whole block.
--
--   psql "$DATABASE_URL" -f supabase/tests/rls_privacy_test.sql
do $$
declare
  a uuid := gen_random_uuid();
  b uuid := gen_random_uuid();
  n int;
  failed text := '';
begin
  insert into auth.users (id, instance_id, aud, role, email) values
    (a, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'sample-a@example.invalid'),
    (b, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'sample-b@example.invalid');

  -- User A adds a verse
  perform set_config('request.jwt.claims', json_build_object('sub', a, 'role', 'authenticated')::text, true);
  set local role authenticated;
  insert into public.memory_verses (id, ref, text) values ('v1', 'Sample 1:1', 'Sample verse text.');
  select count(*) into n from public.memory_verses; if n <> 1 then failed := failed || ' A-cannot-read-own;'; end if;

  -- A cannot insert a row owned by B
  begin
    insert into public.memory_verses (user_id, id, ref, text) values (b, 'v2', 'Sample 1:2', 'x');
    failed := failed || ' A-inserted-as-B;';
  exception when insufficient_privilege or check_violation then null; end;

  -- User B sees nothing of A's, and cannot change or delete it
  perform set_config('request.jwt.claims', json_build_object('sub', b, 'role', 'authenticated')::text, true);
  select count(*) into n from public.memory_verses; if n <> 0 then failed := failed || ' B-reads-A;'; end if;
  update public.memory_verses set text = 'changed' where id = 'v1'; get diagnostics n = row_count; if n <> 0 then failed := failed || ' B-updates-A;'; end if;
  delete from public.memory_verses where id = 'v1'; get diagnostics n = row_count; if n <> 0 then failed := failed || ' B-deletes-A;'; end if;
  -- B can use the same verse id for their own row
  insert into public.memory_verses (id, ref, text) values ('v1', 'Sample 1:1', 'B copy');

  -- A cannot hand a row to B
  perform set_config('request.jwt.claims', json_build_object('sub', a, 'role', 'authenticated')::text, true);
  begin
    update public.memory_verses set user_id = b where id = 'v1';
    get diagnostics n = row_count; if n <> 0 then failed := failed || ' A-reassigned-row;'; end if;
  exception when insufficient_privilege or check_violation or unique_violation then null; end;
  select count(*) into n from public.memory_verses where text = 'Sample verse text.'; if n <> 1 then failed := failed || ' A-row-changed;'; end if;

  -- Signed-out visitors get nothing
  reset role;
  set local role anon;
  begin
    select count(*) into n from public.memory_verses;
    failed := failed || ' anon-can-select(' || n || ');';
  exception when insufficient_privilege then null; end;
  reset role;

  raise exception 'PRIVACY_TEST %', case when failed = '' then 'ALL PASSED' else 'FAILED:' || failed end;
end $$;
