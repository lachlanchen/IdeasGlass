**Concept**
- Prophecy Diary: users state life goals, decompose them into goal-level plans and ordered steps, and the app captures daily "done / next" evidence from conversations as diary entries. Prophecy entries record intended actions with a due time and confidence, and can be fulfilled or missed.

**Entities**
- LifeGoal: long-horizon objective (life/decade/year/quarter/month) with vision/why and success metrics.
- Goal: specific outcome aligned to a LifeGoal (deadline, priority, progress).
- GoalPlan: strategy and metrics for how to achieve a Goal.
- GoalPlanStep: ordered tasks with optional dependencies and due dates.
- GoalDiaryEntry: entries auto-extracted from transcripts or manually added (done, todo, insight, decision, obstacle, reflection, review).
- ProphecyEntry: intent/commitment with confidence; status evolves from planned → in_progress → fulfilled/missed.

**JSON Schemas**
- See schemas/ for life_goal, goal, plan, plan_step, diary_entry, prophecy_entry.
- All include `user_id` and timestamps; foreign keys link entries to goals/plans/steps.

**Database (Postgres)**
- ig_life_goals: life-horizon objectives.
- ig_goals: actionable goals; `parent_life_goal_id` links to ig_life_goals.
- ig_goal_plans: strategy per goal.
- ig_goal_plan_steps: ordered steps with dependencies.
- ig_goal_diary: daily entries (done/todo/insight/etc.) with source backreferences.
- ig_prophecy_entries: intended actions with confidence and outcomes.
- Indexes cover user scoping, status, deadlines, and recency.

**Flow**
1) User creates LifeGoal(s) and near-term Goal(s) under them.
2) For each Goal, define a Plan and initial Steps.
3) As conversations happen, the system extracts diary entries (e.g., "done", "todo", "insight") with links to transcript segments/photos.
4) User adds Prophecy entries ("I will do X by Y" with confidence). System tracks fulfillment vs. missed.
5) Progress rolls up: steps → plan → goal → life goal (via progress_percent fields).

**UI Outline (current)**
- Goals tab top: Prophecy Diary card (clickable) showing diary/vision teaser.
- Prophecy Diary detail: fancy cards for Prophecy, Who am I, Vision, Why, Strategy, Metrics.
- Goals grid: clickable cards → detail with edit (outcome, deadline, priority, status, progress).
- Steps/Diary/Prophecy entries: planned (not yet implemented).

**API (implemented subset)**
- Life goals (Prophecy Diary):
  - GET /api/v1/life-goals — list
  - GET /api/v1/life-goals/{id} — detail (vision, why, strategy, metrics, diary, identity)
  - POST /api/v1/life-goals/seed — seed sample
- Goals:
  - GET /api/v1/goals, POST /api/v1/goals/seed
  - GET /api/v1/goals/{id}, PATCH /api/v1/goals/{id}, DELETE /api/v1/goals/{id}

**Extraction from conversations**
- Map transcript segments to diary entries:
  - phrases like "I did …" → type=done
  - "I will …"/"need to …" → type=todo and/or ProphecyEntry (with inferred due if mentioned)
  - decision/obstacle/insight keywords populate those types
- Entries link to source_id (audio segment/photo) for playback and context.

**Rollout**
- Phase A (MVP): db tables, CRUD for LifeGoal/Goal/Plan/Step; diary ingest from manual + minimal transcript rules.
- Phase B: Prophecy entries + confidence, due reminders; convert diary TODO to Step.
- Phase C: Progress rollups, dashboards, and search.

**Samples**
- See samples/ for a life goal, a month goal + plan + steps, diary entries from transcripts, and a prophecy entry.
