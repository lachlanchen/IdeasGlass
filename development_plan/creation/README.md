Creation — Research, Business, Media, Writing, Music (Draft)

This folder defines the data model and plan for the Creation module. Creations are typed outputs (research proposals, business plans, videos, stories/blog posts, novels, scripts, music, small files). Each creation supports assets, sections, status workflow, and links back to ideas/goals.

Contents
- schemas/*.json — Base Creation schema, Section and Asset schemas, and typed metadata (oneOf by creation_type).
- db/schema.sql — PostgreSQL tables (ig_creations, ig_creation_sections, ig_creation_assets, ig_creation_links) and indexes.
- samples/*.json — Example payloads for key creation types.
- plan.md — Product/UX plan, templates, API outline, and rollout notes.

Notes
- Documentation-only; no backend runtime changes yet.
- Matches existing naming (ig_*). Type-specific metadata is stored in `meta` (jsonb) but validated via JSON Schema.

