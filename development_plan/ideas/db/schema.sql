-- Draft SQL DDL for Ideas/Goals/Creation
-- Namespaced with ig_* to align with existing tables (ig_users, ig_device_bindings).

create extension if not exists pgcrypto; -- for gen_random_uuid()

-- Tags
create table if not exists ig_tags (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  name text not null,
  color varchar(7), -- #RRGGBB
  created_at timestamptz not null default now(),
  unique (user_id, name)
);

-- Ideas
create table if not exists ig_ideas (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  title text not null,
  summary text,
  language varchar(16),
  status smallint not null default 0, -- 0=active,1=archived,2=deleted
  occurrence_count integer not null default 0,
  urgency numeric(6,3) default 0,
  recency_score numeric(10,4) default 0,
  importance_score numeric(10,4) default 0,
  evidence_count integer not null default 0,
  latest_occurrence_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz,
  idea_search tsvector
);

create index if not exists idx_ig_ideas_user_status on ig_ideas(user_id, status);
create index if not exists idx_ig_ideas_importance on ig_ideas(user_id, status, importance_score desc);
create index if not exists idx_ig_ideas_latest_occurrence on ig_ideas(user_id, latest_occurrence_at desc);
create index if not exists idx_ig_ideas_search on ig_ideas using gin(idea_search);

-- Idea <-> Tags
create table if not exists ig_idea_tags (
  idea_id uuid not null references ig_ideas(id) on delete cascade,
  tag_id uuid not null references ig_tags(id) on delete cascade,
  primary key (idea_id, tag_id)
);

-- Evidence for ideas (references to transcripts/photos/etc.)
create table if not exists ig_idea_references (
  id uuid primary key default gen_random_uuid(),
  idea_id uuid not null references ig_ideas(id) on delete cascade,
  source_type smallint not null, -- 0=transcript,1=photo,2=note,3=external
  source_id text,
  snippet_text text,
  language varchar(16),
  device_id text,
  audio_segment_id uuid,
  transcript_start_ms integer,
  transcript_end_ms integer,
  occurred_at timestamptz not null,
  link_url text,
  lat numeric(9,6),
  lon numeric(9,6),
  place text,
  created_at timestamptz not null default now()
);

create index if not exists idx_ig_idea_refs_idea on ig_idea_references(idea_id);
create index if not exists idx_ig_idea_refs_when on ig_idea_references(occurred_at desc);
create index if not exists idx_ig_idea_refs_type on ig_idea_references(source_type);

-- Goals
create table if not exists ig_goals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
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

-- Goal steps (tasks)
create table if not exists ig_goal_steps (
  id uuid primary key default gen_random_uuid(),
  goal_id uuid not null references ig_goals(id) on delete cascade,
  title text not null,
  description text,
  status smallint not null default 0, -- 0=todo,1=doing,2=done,3=blocked,4=canceled
  order_index integer not null default 0,
  due_at timestamptz,
  effort smallint, -- 0=XS,1=S,2=M,3=L,4=XL
  blocking boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_ig_goal_steps_goal_order on ig_goal_steps(goal_id, order_index);

-- Idea ↔ Goal mapping (many-to-many)
create table if not exists ig_idea_goals (
  idea_id uuid not null references ig_ideas(id) on delete cascade,
  goal_id uuid not null references ig_goals(id) on delete cascade,
  primary key (idea_id, goal_id)
);

-- Creations
create table if not exists ig_creations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  title text not null,
  content_type smallint not null, -- 0=article,1=video,2=script,3=music,4=photo_set,5=other
  status smallint not null default 0, -- 0=draft,1=in_progress,2=review,3=published,4=archived
  outcome_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);

create index if not exists idx_ig_creations_user_status on ig_creations(user_id, status);

-- Creation assets
create table if not exists ig_creation_assets (
  id uuid primary key default gen_random_uuid(),
  creation_id uuid not null references ig_creations(id) on delete cascade,
  asset_type smallint not null, -- 0=image,1=audio,2=video,3=document,4=other
  url text not null,
  mime_type text,
  created_at timestamptz not null default now()
);

-- Creation ↔ Ideas (many-to-many)
create table if not exists ig_creation_ideas (
  creation_id uuid not null references ig_creations(id) on delete cascade,
  idea_id uuid not null references ig_ideas(id) on delete cascade,
  primary key (creation_id, idea_id)
);

-- Helper: maintain tsvector on ideas (title+summary)
create or replace function ig_ideas_update_search() returns trigger as $$
begin
  new.idea_search :=
    setweight(to_tsvector('simple', coalesce(new.title,'')), 'A') ||
    setweight(to_tsvector('simple', coalesce(new.summary,'')), 'B');
  return new;
end; $$ language plpgsql;

drop trigger if exists trg_ig_ideas_search_insupd on ig_ideas;
create trigger trg_ig_ideas_search_insupd
before insert or update of title, summary on ig_ideas
for each row execute function ig_ideas_update_search();

