-- Creation module (Draft DDL)
-- Namespace aligns with existing ig_* tables.

create extension if not exists pgcrypto; -- gen_random_uuid()

-- Creations (typed outputs)
create table if not exists ig_creations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  title text not null,
  creation_type smallint not null, -- 0=research_proposal,1=business_plan,2=video_project,3=story_post,4=novel_project,5=script_project,6=music_track,7=small_file,8=other
  status smallint not null default 0, -- 0=draft,1=in_progress,2=review,3=published,4=archived
  summary text,
  language varchar(16),
  tags text[],
  meta jsonb, -- type-specific structured metadata
  outcome_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);
create index if not exists idx_ig_creations_user_status on ig_creations(user_id, status);
create index if not exists idx_ig_creations_type on ig_creations(user_id, creation_type, status);

-- Creation sections (ordered content blocks)
create table if not exists ig_creation_sections (
  id uuid primary key default gen_random_uuid(),
  creation_id uuid not null references ig_creations(id) on delete cascade,
  title text not null,
  kind smallint not null default 10, -- enum mirror of section kinds
  order_index integer not null default 0,
  body text,
  language varchar(16),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_ig_creation_sections_creation_order on ig_creation_sections(creation_id, order_index);

-- Creation assets (media attachments)
create table if not exists ig_creation_assets (
  id uuid primary key default gen_random_uuid(),
  creation_id uuid not null references ig_creations(id) on delete cascade,
  asset_type smallint not null, -- 0=image,1=audio,2=video,3=document,4=other
  url text not null,
  mime_type text,
  caption text,
  created_at timestamptz not null default now()
);
create index if not exists idx_ig_creation_assets_creation on ig_creation_assets(creation_id);

-- Links to Ideas and Goals (many-to-many)
create table if not exists ig_creation_links (
  creation_id uuid not null references ig_creations(id) on delete cascade,
  idea_id uuid,
  goal_id uuid,
  constraint one_target check ((idea_id is not null) <> (goal_id is not null)),
  primary key (creation_id, idea_id, goal_id)
);

