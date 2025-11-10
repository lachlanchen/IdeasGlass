**Purpose**
- Capture ideas from everyday conversations, rank them by importance (occurrence × urgency × recency), and help users turn them into actionable goals and finished creations.

**Core Entities**
- Idea: A candidate opportunity distilled from transcripts/photos/notes.
- IdeaReference (Evidence): The where/when/what/how that supports an Idea.
- Goal: An objective formed from one or more Ideas.
- GoalStep: Steps/tasks that achieve a Goal.
- Creation: A piece of output (article, video, script, etc.) that realizes Ideas.

**Ranking (Importance)**
- Inputs
  - occurrence_count: how many distinct mentions/evidence items.
  - urgency: manual 0–1 slider or inferred from language (“today”, “ASAP”).
  - recency_score: exponential decay on the latest occurrences.
- Example score
  - score = min(1, 0.5·sigmoid(occurrence_count) + 0.3·urgency + 0.2·recency_score).
  - Store all components; compute server-side for sorting. Keep fields in `importance` for UI display.

**UX Model (current)**
- Ideas (list)
  - Ranked cards: title, summary, score pill, tags, latest time. Tap → detail.
- Idea detail
  - Edit: title, summary, language, tags. Actions: archive/unarchive, delete. Importance shown as score + metrics text. Evidence timeline planned (not yet implemented).
- Goals (list)
  - Card: title, progress bar, due date, priority. Tap → detail.
  - Detail: steps in order; add/edit; quick filters (blocked, due soon).
- Creations (list)
  - Card: title, type, status; last updated time. Detail: linked ideas, assets, publish URL.

**API (implemented)**
- GET /api/v1/ideas?limit=50 — list active ideas (ranked)
- POST /api/v1/ideas/seed — seed sample ideas
- GET /api/v1/ideas/{id} — idea detail
- PATCH /api/v1/ideas/{id} — edit
- DELETE /api/v1/ideas/{id} — soft delete
- Goals
  - GET /api/v1/goals
  - POST /api/v1/goals {Goal}
  - GET /api/v1/goals/{id}
  - PATCH /api/v1/goals/{id}
  - POST /api/v1/goals/{id}/steps {GoalStep}
  - PATCH /api/v1/goals/{id}/steps/{step_id}
  - POST /api/v1/ideas/{idea_id}/attach-goal/{goal_id}
- Creations
  - GET /api/v1/creations
  - POST /api/v1/creations {Creation}
  - GET /api/v1/creations/{id}
  - PATCH /api/v1/creations/{id}
  - POST /api/v1/creations/{id}/assets

**Storage**
- See db/schema.sql for normalized tables under `ig_*` (ideas, evidence, tags, goals/steps, creations/assets, and linking tables).
- Full-text search: `ig_ideas.idea_search` (tsvector) over title+summary; GIN index.

**Extraction flow (from transcripts)**
1) Ingest transcript segments (existing).
2) Lightweight keyword/co-occurrence mining to propose Idea seeds (out of scope for now).
3) On user confirm/edit, create Idea; attach initial IdeaReference to the source segment.
4) Future: auto-merge duplicates by fuzzy title similarity and shared references.

**Privacy & Scope**
- All records scoped by `user_id` and filtered by bound devices (existing binding rules apply for evidence).
- Soft delete everywhere; archived items excluded by default.

**MVP Rollout**
- Phase 1: Backend tables, Pydantic models, CRUD for Ideas and References; list+detail UI in the PWA.
- Phase 2: Goals and Steps; attach Ideas to Goals; simple progress.
- Phase 3: Creations; attach media; publish link field.

**Open Questions**
- Speaker attribution: keep generic ("Speaker") until diarization lands; store optional `speaker_label` in references if available.
- Location metadata: optional and rare; included in schema.
- Prioritization formula tuning: keep weights configurable per user later.

**Examples**
- See samples/*.json for representative payloads grounded in the shared Weixin topics (writing, video editing, AI journaling, strategy, daily review).
