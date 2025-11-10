Ideas/Goals/Creation — Data Design (Draft)

This folder contains a proposed data model, JSON Schemas, SQL DDL, and a product plan for Ideas, Goals, and Creations. It is documentation only — no backend changes are made yet.

Contents
- schemas/*.json — JSON Schemas for API payloads and storage.
- db/schema.sql — PostgreSQL tables and indexes (ig_* names to match existing tables).
- samples/*.json — Example payloads used by the UI and backend.
- plan.md — Product/UX plan, scoring, endpoints, and rollout notes.

Scope
- Focuses on representing ideas extracted from daily conversations, ranking them by importance (occurrence, urgency, recency), and letting users turn ideas into goals and finished creations.
- Respects existing user/device scoping: every record includes `user_id`; device-specific evidence is referenced from transcript/audio/photo sources.

Status
- Draft for review. Safe to iterate independently of backend runtime.

