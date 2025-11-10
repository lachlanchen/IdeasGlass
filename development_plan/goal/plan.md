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

**UI Outline**
- Life Goals list → detail (vision/why, metrics, linked goals).
- Goals list → detail (plan, steps, diary, prophecies).
- Steps: swipe to mark done/blocked; reorder; show dependencies.
- Diary: timeline with source badges; quick add; convert a TODO diary entry into a step.
- Prophecy: list with confidence bars; due soon surface; fulfillment toggle.

**API (proposed)**
- LifeGoals: GET/POST/PATCH /api/v1/life-goals
- Goals:     GET/POST/PATCH /api/v1/goals
- Plans:     GET/POST/PATCH /api/v1/goals/{id}/plans
- Steps:     GET/POST/PATCH /api/v1/plans/{id}/steps
- Diary:     GET/POST      /api/v1/diary  (filter by goal/plan/step/date)
- Prophecy:  GET/POST/PATCH /api/v1/prophecies

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

