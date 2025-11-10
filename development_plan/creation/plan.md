**Concept**
- Creation is the output workspace: research proposals, business plans, media projects, posts, novels, scripts, music, and small files. Each creation has a type, a status workflow, sections (structured content), assets (media), and links to upstream Ideas and Goals.

**Types**
- research_proposal: academic structure (abstract/background/method/results/discussion/conclusion) with authorship and funding meta.
- business_plan: exec summary, market, product, model, GTM, financials.
- video_project: duration, aspect ratio, platform; script section; media assets.
- story_post: Medium/blog style; category and read time.
- novel_project: chapters; genre and target word count.
- script_project: scenes; format and duration.
- music_track: genre, bpm, key, length; audio assets.
- small_file: arbitrary uploaded doc; file_kind and size.

**JSON Schemas**
- creation.schema.json — base record with type, status, tags, language, meta, sections, assets, idea_ids, goal_ids.
- creation_meta.schema.json — oneOf dispatch to type-specific meta schemas under schemas/meta/.
- section.schema.json — ordered content blocks (title/kind/body).
- asset.schema.json — media/document attachments.

**Database (Postgres)**
- ig_creations — base record; `creation_type` smallint; `meta` jsonb stores typed metadata.
- ig_creation_sections — ordered content sections.
- ig_creation_assets — attached media/documents.
- ig_creation_links — many-to-many links to ig_ideas or ig_goals.

**UI & UX**
- Grid of square blocks per type (cards): icon + title + status; tap to open detail.
- Detail: header (title/tags/status), type meta panel, sections editor (reorderable), assets gallery, links (ideas/goals), publish URL.
- Templates: pre-seed sections based on type; quick add sections.

**API (proposed)**
- Creations: GET/POST /api/v1/creations; GET/PATCH /api/v1/creations/{id}
- Sections:  GET/POST /api/v1/creations/{id}/sections; PATCH /api/v1/creations/{id}/sections/{sid}
- Assets:    POST /api/v1/creations/{id}/assets
- Links:     POST /api/v1/creations/{id}/link-idea/{idea_id}; /link-goal/{goal_id}

**Rollout**
- Phase 1: DB + CRUD + list/detail UI with templates for the main types (research, business, video, post).
- Phase 2: Sections editor, assets upload, and links to ideas/goals.
- Phase 3: Export/publish flows (PDF/HTML), status transitions, and search.

**Samples**
- See samples/ for examples across all types.

