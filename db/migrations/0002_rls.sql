-- Enable RLS
alter table users enable row level security;
alter table profiles enable row level security;
alter table resume_profiles enable row level security;
alter table applications enable row level security;
alter table subscriptions enable row level security;
alter table usage_counters enable row level security;
alter table interview_sessions enable row level security;
alter table gap_narratives enable row level security;
alter table portfolio_projects enable row level security;
alter table user_websites enable row level security;
alter table bulk_apply_queue enable row level security;
alter table application_versions enable row level security;

-- Policies: users can access their own rows
create policy if not exists users_self_select on users
for select using (auth.uid() = id);

create policy if not exists users_self_update on users
for update using (auth.uid() = id);

create policy if not exists profiles_self on profiles
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists resume_profiles_self on resume_profiles
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists applications_self on applications
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists subscriptions_self on subscriptions
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists usage_counters_self on usage_counters
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- RLS policies for new tables
create policy if not exists interview_sessions_self on interview_sessions
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists gap_narratives_self on gap_narratives
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists portfolio_projects_self on portfolio_projects
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists user_websites_self on user_websites
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists bulk_apply_queue_self on bulk_apply_queue
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy if not exists application_versions_self on application_versions
for all using (auth.uid() = (select user_id from applications where id = application_id)) with check (auth.uid() = (select user_id from applications where id = application_id));
