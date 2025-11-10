Prophecy Diary — Goals, Plans, and Daily Evidence (Draft)

This folder defines the data model and plan for the Prophecy Diary feature: users set life goals, break them into action plans and steps, and the system captures daily “done/next” evidence from conversations as diary entries. Prophecy entries capture intended actions (commitments) with confidence and deadlines.

Contents
- schemas/*.json — JSON Schemas for life goals, plans, steps, diary entries, and prophecy entries.
- db/schema.sql — PostgreSQL tables and indexes (ig_* namespace) with user scoping.
- samples/*.json — Example payloads.
- plan.md — Product/UX and API plan for phased rollout.

Notes
- Documentation-only; no backend runtime changes yet.
- Names align with earlier ig_goals tables and extend them for life-goal hierarchy and diary capture.

