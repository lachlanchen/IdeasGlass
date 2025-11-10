**Concept**
- A “Prophecy Diary” life goal sits above regular goals: who you want to be, what you want to do, and a gentle plan to realize it.

**Model**
- Runtime table `ig_life_goals` (see db/schema.sql) with vision/why/strategy and optional metrics.
- One active record per user (typical), but multiple are allowed.

**API (runtime)**
- GET /api/v1/life-goals — list active life goals (top 1–3).
- GET /api/v1/life-goals/{id} — detail with all fields.
- POST /api/v1/life-goals/seed — insert “Prophecy Diary — The Art of Lazying” sample.

**UI**
- Goals tab → top panel “Prophecy Diary” with title and vision teaser; clicking opens a Life Goal detail page.
- Detail page shows: title, badges, vision, why, strategy, metrics, progress.

**Sample**
- Based on “The Art of Lazying”: a happy life without unnecessary effort; automate, compound, delegate; build assets that work while resting.

