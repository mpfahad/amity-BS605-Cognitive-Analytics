-- BS605 progress sync (run in Supabase SQL Editor)
-- Table + RLS for personal sync-code progress

create table if not exists public.bs605_progress (
  code_hash text primary key,
  payload jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.bs605_progress enable row level security;

-- Anon clients may read/write rows they address by code_hash.
-- Security relies on the sync code (hashed client-side), not on listing all rows.
drop policy if exists "bs605_progress_select" on public.bs605_progress;
drop policy if exists "bs605_progress_insert" on public.bs605_progress;
drop policy if exists "bs605_progress_update" on public.bs605_progress;

create policy "bs605_progress_select"
  on public.bs605_progress for select
  to anon, authenticated
  using (true);

create policy "bs605_progress_insert"
  on public.bs605_progress for insert
  to anon, authenticated
  with check (true);

create policy "bs605_progress_update"
  on public.bs605_progress for update
  to anon, authenticated
  using (true)
  with check (true);

-- Optional: deny listing abuse is acceptable for personal single-user study pack.
