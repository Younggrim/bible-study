-- Reading plans: the one plan a person is following and when they started it.
-- Progress is not stored here; it is worked out from chapters_studied (any
-- chapter of the plan studied on or after started_on counts), so finishing a
-- chapter anywhere on the site moves the plan along.

create table public.reading_plans (
  user_id     uuid        primary key default auth.uid() references auth.users (id) on delete cascade,
  plan_id     text        not null check (plan_id ~ '^[a-z0-9-]{1,40}$'),
  started_on  date        not null,
  active      boolean     not null default true,
  updated_at  timestamptz not null default now()
);
comment on table public.reading_plans is
  'The reading plan each person is following. Private to the owning user (RLS).';

create trigger reading_plans_touch before insert or update on public.reading_plans
  for each row execute function public.study_touch();

alter table public.reading_plans enable row level security;
revoke all on public.reading_plans from anon;
revoke all on public.reading_plans from authenticated;
grant select, insert, update, delete on public.reading_plans to authenticated;
grant select, insert, update, delete on public.reading_plans to service_role;

create policy "Read own plan" on public.reading_plans for select to authenticated using (user_id = (select auth.uid()));
create policy "Add own plan" on public.reading_plans for insert to authenticated with check (user_id = (select auth.uid()));
create policy "Change own plan" on public.reading_plans for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
