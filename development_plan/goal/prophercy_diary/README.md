Prophecy Diary (Life Goal) — Design (Draft)

This folder defines a specialized “Prophecy Diary” life goal: the overarching who-I-want-to-be and what-I-want-to-do vision, with a detailed plan and metrics. It complements the general Goals feature.

Contents
- schemas/*.json — JSON Schemas for LifeGoal (prophecy diary) and its detail payload.
- db/schema.sql — PostgreSQL tables and indexes for runtime (`ig_life_goals`).
- samples/*.json — Example payload grounded in “The Art of Lazying”.
- plan.md — UX/API plan for a top‑of‑page panel in the Goals tab and a detailed page.

Notes
- Runtime code adds `ig_life_goals` and read/seed endpoints; editing is deferred.
- This design keeps plan/vision/why/metrics under the life goal itself; deeper breakdown can link normal “goals” under this life goal in the future.

