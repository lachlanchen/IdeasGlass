-- Runtime DDL for Prophecy Diary life goals (ig_life_goals)

create table if not exists ig_life_goals (
  id text primary key,
  user_id text not null,
  title text not null,
  vision text,
  why text,
  strategy text,
  categories jsonb,
  horizon smallint not null default 0, -- 0=life,1=decade,2=year,3=quarter,4=month
  status smallint not null default 0,  -- 0=active,1=archived,2=deleted
  progress_percent numeric(5,2) default 0,
  metrics jsonb,
  start_date date,
  target_date date,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);

create index if not exists idx_ig_life_goals_user_status on ig_life_goals(user_id, status);
