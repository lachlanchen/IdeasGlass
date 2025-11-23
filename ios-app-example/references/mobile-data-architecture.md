# LightMind Mobile Data Architecture (iOS/Android/PWA) — Reference

This note captures a practical, cross‑platform storage + sync approach for LightMind, suitable for iOS, Android, and PWA with a server backend.

## Core Principles
- Local‑first: write immediately to local storage; queue uploads; sync in background.
- Files vs. metadata: large binaries (audio) as files; all metadata in a small DB.
- Deterministic IDs: client‑generated UUID v7 (or ULID) for globally unique records pre‑sync.
- Idempotent sync: every upload has an idempotency key; server accepts duplicates safely.
- Incremental pull: server exposes “changes since cursor” to fetch deltas.

## Local Storage
- iOS
  - Files: Application Support (not tmp), e.g. `Library/Application Support/segments/<sha256>.opus|.wav`.
  - Protection: `NSFileProtectionCompleteUnlessOpen`; exclude from backups if desired.
  - DB: SQLite via GRDB.swift (simple, fast migrations) or Core Data if preferred.
  - Background: URLSession background uploads; BGTaskScheduler for retry/backoff/housekeeping.
- Android
  - Files: app‑specific storage.
  - DB: Room/SQLDelight; background jobs via WorkManager.
- PWA
  - Files: Blobs in Cache Storage (or IndexedDB for small media).
  - DB: IndexedDB (e.g., Dexie.js); Service Worker + Background Sync/Alarms for retries.

## Recommended Schema (shared shape across clients)
- users: id, display_name
- sessions: id, device_id, started_at, ended_at, label
- segments: id, session_id, codec, sample_rate, channels, file_sha256, file_path, size_bytes, duration_ms, state(enum), retry_count, created_at, updated_at
- uploads: id, segment_id, status(enum: queued/in_progress/completed/failed), last_error, attempts, created_at, updated_at
- kv_state: key(unique), value, updated_at (for cursors, feature flags)
- logs: id, level, message, context_json, created_at (capped by size)

State examples
- segments.state: `recorded | queued | uploading | uploaded | failed`
- uploads.status: `queued | in_progress | completed | failed`

## Record → Persist → Upload Flow
1. Record
   - Write decoded PCM/Opus to file in chunks; finalize per minute.
   - Compute sha256 on finalization; insert `segments` row (state=queued).
2. Upload
   - POST metadata (id, sha256, duration, codec, device_id) → server returns presigned URL or direct POST + server segment id.
   - PUT file to object storage with idempotency headers.
   - PATCH `segments` → uploaded; clean up local by retention policy.
3. Pull
   - GET `/changes?cursor=…` to fetch server edits (labels, features). Merge by version/E‑Tag.
4. Retry/backoff
   - Exponential backoff with jitter; user feedback only when needed.

## Conflict & Versioning
- Each record has version (int) or updated_at + ETag.
- Last‑write‑wins for simplicity; move to CRDT/per‑field merges if collaboration required.
- Use numbered migrations (SQLite PRAGMA `user_version`) for schema evolution.

## Security
- At‑rest: iOS file protection; Android app storage; PWA encrypt at rest if needed.
- In‑flight: TLS; short‑lived tokens; idempotency keys.
- Optional E2EE: encrypt file before upload; store envelope keys in Keychain/Keystore (not in DB).

## API Contract (OpenAPI preferred)
- `POST /segments` → create metadata; returns server id + upload instructions (presigned URL or form).
- `PUT /segments/{id}/content` → upload binary (or use returned presigned URL).
- `PATCH /segments/{id}` → update labels/state.
- `GET /changes?cursor=…` → delta feed.
- Optional: `POST /manifests` for batch metadata.

## Cross‑Platform Notes
- iOS: GRDB for SQLite; URLSession background tasks for uploads; BGTaskScheduler for periodic sync.
- Android: Room + WorkManager.
- PWA: IndexedDB + Service Worker; Background Sync/alarm/Push for retries.
- Share types via OpenAPI/GraphQL schema to generate clients for Swift/Kotlin/TypeScript.

## LightMind Integration Steps
1. Move segments from `temporaryDirectory` to `Application Support/segments` (content‑addressable by sha256).
2. Add SQLite (GRDB) with the schema above and migrations.
3. Build an Outbox service:
   - Select oldest queued `segments`, POST metadata, PUT file to object storage, then mark `uploaded`.
   - Use URLSession background transfers and persist upload state in `uploads`.
4. Add Pull sync using a cursor stored in `kv_state`.
5. Settings: Wi‑Fi‑only uploads, keep local copies (days), auto‑upload toggle.
6. Server: accept metadata, return presigned URL; process/transcribe; update labels and expose via `/changes`.

## Retention & Export
- Retention: delete local after confirmed upload or keep N days; configurable.
- Export: wrap PCM as WAV and share via system share sheets / PWA download.

## Background & UX
- Show an Outbox count and sync progress.
- Fail gracefully offline; retry automatically when network returns.
- Keep BLE auto‑reconnect independent from upload state.

## TL;DR
- Store audio files locally; metadata in SQLite.
- Queue uploads with idempotency and cursor‑based pull.
- Align schemas across platforms; generate clients from an API spec.
- Design for offline‑first, robust retries, and clear user controls.

