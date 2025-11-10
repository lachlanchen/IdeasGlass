-- Prophecy Diary: Goals, Plans, Diary, and Prophecy entries (Draft DDL)
-- Namespace: ig_* to align with existing tables.

create extension if not exists pgcrypto; -- gen_random_uuid()

-- Life Goals (long-horizon objectives)
create table if not exists ig_life_goals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  title text not null,
  vision text,
  why text,
  categories text[],
  horizon smallint not null default 0, -- 0=life,1=decade,2=year,3=quarter,4=month
  status smallint not null default 0, -- 0=active,1=archived,2=deleted
  start_date date,
  target_date date,
  progress_percent numeric(5,2) default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);
create index if not exists idx_ig_life_goals_user_status on ig_life_goals(user_id, status);

-- Goals (shorter-horizon goals; can belong to a life goal)
-- If an ig_goals table already exists, consider ALTER TABLE to add parent_life_goal_id and progress fields.
create table if not exists ig_goals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  parent_life_goal_id uuid references ig_life_goals(id) on delete set null,
  title text not null,
  outcome text,
  deadline timestamptz,
  priority smallint default 0,
  status smallint not null default 0, -- 0=not_started,1=in_progress,2=blocked,3=done,4=canceled
  progress_percent numeric(5,2) default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);
create index if not exists idx_ig_goals_user_status on ig_goals(user_id, status);
create index if not exists idx_ig_goals_deadline on ig_goals(user_id, deadline);

-- Plans (per-goal action plan)
create table if not exists ig_goal_plans (
  id uuid primary key default gen_random_uuid(),
  goal_id uuid not null references ig_goals(id) on delete cascade,
  title text not null,
  strategy text,
  assumptions text,
  risks text,
  metrics jsonb, -- optional structured metrics array
  status smallint not null default 0, -- 0=draft,1=active,2=paused,3=done,4=archived
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_ig_goal_plans_goal on ig_goal_plans(goal_id);

-- Plan Steps (ordered tasks)
create table if not exists ig_goal_plan_steps (
  id uuid primary key default gen_random_uuid(),
  plan_id uuid not null references ig_goal_plans(id) on delete cascade,
  title text not null,
  description text,
  status smallint not null default 0, -- 0=todo,1=doing,2=done,3=blocked,4=canceled
  order_index integer not null default 0,
  due_at timestamptz,
  effort smallint, -- 0=XS,1=S,2=M,3=L,4=XL
  blocking boolean not null default false,
  depends_on uuid[],
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_ig_goal_plan_steps_plan_order on ig_goal_plan_steps(plan_id, order_index);

-- Diary Entries (auto-captured or manual)
create table if not exists ig_goal_diary (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  goal_id uuid references ig_goals(id) on delete set null,
  plan_id uuid references ig_goal_plans(id) on delete set null,
  step_id uuid references ig_goal_plan_steps(id) on delete set null,
  type smallint not null, -- 0=done,1=todo,2=insight,3=decision,4=obstacle,5=reflection,6=review
  text text,
  language varchar(16),
  occurred_at timestamptz not null,
  source smallint not null default 0, -- 0=transcript,1=photo,2=manual,3=external
  source_id text,
  tags text[],
  created_at timestamptz not null default now()
);
create index if not exists idx_ig_goal_diary_user_when on ig_goal_diary(user_id, occurred_at desc);
create index if not exists idx_ig_goal_diary_goal_type on ig_goal_diary(goal_id, type, occurred_at desc);

-- Prophecy Entries (intent + confidence; fulfilled/missed)
create table if not exists ig_prophecy_entries (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  goal_id uuid references ig_goals(id) on delete set null,
  plan_id uuid references ig_goal_plans(id) on delete set null,
  step_id uuid references ig_goal_plan_steps(id) on delete set null,
  intent_text text not null,
  due_at timestamptz,
  confidence numeric(4,3) default 0,
  commitment_level smallint not null default 0, -- 0=considering,1=planning,2=committed
  status smallint not null default 0, -- 0=planned,1=in_progress,2=fulfilled,3=missed,4=canceled
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  realized_at timestamptz
);
create index if not exists idx_ig_prophecy_user_status on ig_prophecy_entries(user_id, status);
create index if not exists idx_ig_prophecy_due on ig_prophecy_entries(user_id, due_at);

