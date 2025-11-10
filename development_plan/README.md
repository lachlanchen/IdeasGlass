IdeasGlass Development Plan — Current App Snapshot (Nov 2025)

This document summarizes what is implemented in the current app and how it aligns with the planning folders under development_plan/.

Scope overview
- Backend: FastAPI app in backend/bridge/app.py with REST + WebSocket, Postgres persistence, and static PWA.
- Frontend: Single‑page PWA (backend/bridge/static) with tabs: Live, Ideas, Goal, Creation, Settings.
- Firmware: ESP32‑S3 client (IdeaGlass/firmware) streaming audio/photos, documented separately.

Implemented features (high‑level)
- Ideas
  - DB: ig_ideas (title, summary, language, tags, importance components, status, timestamps).
  - API: list, seed samples, get, patch (edit/archive), delete (soft).
  - UI: Ideas grid with ranked cards; detail sub‑page (edit, archive/unarchive, delete).

- Goals
  - DB: ig_goals (title, outcome, deadline, priority, status, progress).
  - API: list, seed samples, get, patch, delete.
  - UI: Goals grid (clickable); detail sub‑page (edit/delete); top “Prophecy Diary” panel.

- Prophecy Diary (Life Goal)
  - DB: ig_life_goals (title, vision, why, strategy, categories, horizon, status, progress, metrics, diary, identity, dates).
  - API: list, get, seed (sample includes narrative diary + identity).
  - UI: Goals tab shows a Prophecy panel with teaser; dedicated detail sub‑page with fancy cards for Prophecy, Who am I, Vision, Why, Strategy, Metrics.

- Creations
  - DB: ig_creations (+ sections, assets, idea links).
  - API: list, seed samples, create from idea, get detail (with sections, assets).
  - UI: Creation grid (clickable); detail sub‑page with sections and assets; quick create from idea.

- Live tab UX polish
  - Fixed, compact header (safe‑area aware); sub‑pages hide header and use back button.
  - Compact photo gallery + transcripts with detail views, play buttons, and language badges.
  - Mobile UX: disabled pinch/double‑tap zoom; inputs at 16px to prevent iOS auto‑zoom.

Notable endpoints (summary)
- Ideas: GET /api/v1/ideas, POST /api/v1/ideas/seed, GET/PATCH/DELETE /api/v1/ideas/{id}
- Goals: GET /api/v1/goals, POST /api/v1/goals/seed, GET/PATCH/DELETE /api/v1/goals/{id}
- Life Goals: GET /api/v1/life-goals, GET /api/v1/life-goals/{id}, POST /api/v1/life-goals/seed
- Creations: GET /api/v1/creations, POST /api/v1/creations/seed, POST /api/v1/creations/from-idea, GET /api/v1/creations/{id}

Where to find details
- development_plan/ideas — schemas, SQL, and plan (now includes detail/edit/delete status in plan.md).
- development_plan/goal — goals plan (updated to include Prophecy Diary panel and life‑goal endpoints).
- development_plan/goal/prophercy_diary — life‑goal design (diary + identity added; plan.md reflects implementation).
- development_plan/creation — types, schemas, SQL, and plan (updated with list/seed/detail/from‑idea status).

Next suggested steps
- Ideas: evidence timeline (transcript/photo references) on the detail page; convert to goal/creation CTA.
- Goals: optional steps/tasks UI; roll‑up progress from steps.
- Life Goals: optional editor for diary/identity/vision/strategy from the PWA.
- Creations: editable sections and asset upload; publish/outcome URL workflow.

