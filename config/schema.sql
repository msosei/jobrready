-- Core schema for Supabase (Postgres)
create table if not exists users (
  id uuid primary key,
  name text,
  email text unique not null,
  role text default 'user',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists profiles (
  user_id uuid primary key references users(id) on delete cascade,
  resume_profile_id uuid,
  metadata jsonb default '{}'::jsonb
);

create table if not exists resume_profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  resume_json jsonb not null,
  parsed_date timestamptz default now()
);

create table if not exists jobs_index (
  job_id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  company text,
  source text,
  date_posted timestamptz
);

create table if not exists applications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  job_id uuid references jobs_index(job_id) on delete cascade,
  status text default 'pending',
  cover_letter text,
  logs jsonb default '[]'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  plan_type text not null,
  start_date date,
  end_date date,
  quota_limits jsonb default '{"applications":50,"cover_letters":50,"ai_requests":200}'::jsonb
);

create table if not exists usage_counters (
  user_id uuid primary key references users(id) on delete cascade,
  applications_sent int default 0,
  cover_letters_generated int default 0,
  ai_requests int default 0
);

-- New tables for Q-V microservices
create table if not exists interview_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  job_title text,
  difficulty text default 'medium',
  questions jsonb default '[]'::jsonb,
  answers jsonb default '[]'::jsonb,
  score int,
  feedback text,
  created_at timestamptz default now(),
  completed_at timestamptz
);

create table if not exists gap_narratives (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  gap_start date,
  gap_end date,
  narrative text,
  is_public boolean default false,
  created_at timestamptz default now()
);

create table if not exists portfolio_projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  title text not null,
  description text,
  tech_stack text[],
  github_url text,
  demo_url text,
  status text default 'planned',
  created_at timestamptz default now()
);

create table if not exists user_websites (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  domain text,
  vercel_url text,
  template text,
  content jsonb default '{}'::jsonb,
  status text default 'draft',
  deployed_at timestamptz,
  created_at timestamptz default now()
);

create table if not exists bulk_apply_queue (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  job_filters jsonb not null,
  status text default 'pending',
  applications_sent int default 0,
  applications_failed int default 0,
  settings jsonb default '{"max_daily": 10, "pause_between": 30}'::jsonb,
  created_at timestamptz default now(),
  started_at timestamptz,
  completed_at timestamptz
);

create table if not exists application_versions (
  id uuid primary key default gen_random_uuid(),
  application_id uuid references applications(id) on delete cascade,
  resume_json jsonb,
  cover_letter text,
  version int default 1,
  created_at timestamptz default now()
);

create index if not exists idx_jobs_title on jobs_index using gin (to_tsvector('simple', coalesce(title,'') || ' ' || coalesce(company,'')));
create index if not exists idx_jobs_date on jobs_index(date_posted);
create index if not exists idx_interview_sessions_user on interview_sessions(user_id);
create index if not exists idx_gap_narratives_user on gap_narratives(user_id);
create index if not exists idx_portfolio_projects_user on portfolio_projects(user_id);
create index if not exists idx_user_websites_user on user_websites(user_id);
create index if not exists idx_bulk_apply_user on bulk_apply_queue(user_id);


