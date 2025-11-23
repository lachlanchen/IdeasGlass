# LightMind Persistence + Sync Plan (Local‑first, Idempotent, Cache‑friendly)

This plan codifies how LightMind will persist data locally, cache for performance, and sync to a server later in a way that is easy to maintain and reason about. It is designed to be idempotent, resilient, and portable across iOS/Android/PWA.

## Objectives
- Local‑first UX: record and access data instantly, even offline.
- Idempotent sync: the same upload can be retried without duplication.
- Cache friendly: fast local queries and file reads, minimal repeated work.
- Simple and stable: small schema, explicit migrations, robust error handling.
- Cross‑platform: shared data shapes for iOS/Android/PWA.

## Storage Strategy
- Files: store large binaries (audio) under Application Support in content‑addressable paths.
- Database: store all metadata in a small SQLite DB via GRDB (iOS) with explicit migrations.
- Separation of concerns: UI talks to a Repository API, not to SQLite directly.

## File Layout
- Root: `Library/Application Support/LightMind/`
  - `segments/<sha256_prefix>/<sha256>.<ext>` (e.g., `.opus` or `.wav`) to keep directories shallow.
- Compute sha256 on finalize. Optionally mark files as “do not back up”.

## Database Schema (initial)
- `segments`
  - `id` (UUID v7 or v4), `timestamp`, `duration_ms`, `codec`, `sample_rate`, `channels`
  - `file_sha256`, `file_ext`, `size_bytes`, `file_path`
  - `state` (recorded|queued|uploading|uploaded|failed), `retry_count`
  - `created_at`, `updated_at`
- `uploads`
  - `id`, `segment_id` (FK), `status` (queued|in_progress|completed|failed), `attempts`, `last_error`
  - `created_at`, `updated_at`
- `devices`
  - `id` (UUID), `name` (last seen), `platform_identifier` (e.g., iOS CBPeripheral UUID), `last_connected_at`, `notes`
  - Used for auto‑reconnect and display. When connected, show: `Device: <name> (<short id>)`.
- `kv_state`
  - `key` (unique), `value`, `updated_at` (for cursors, feature flags)
- `logs` (optional, capped)
  - `id`, `level`, `message`, `context_json`, `created_at`

Note: Use explicit, numbered migrations for schema evolution.

## Recorder Integration (runtime)
- Write active audio chunks to a temporary staging file.
- On rotation/finalize (~60s):
  1) fsync + close
  2) compute sha256 and determine final path; move to `segments/`
  3) stat file (size) and infer duration
  4) insert `segments` row (state = `recorded`)
- This order is crash‑safe and idempotent.

## Device Identity & UI
- Persist the last connected device in `devices` and UserDefaults (CBPeripheral UUID on iOS).
- Attempt auto‑reconnect on app start:
  - `retrievePeripherals(withIdentifiers:)` → connect; fallback to a targeted scan.
- Show in Bluetooth status: `Device: <name> (<short uuid>)` when connected.

## Sync Flow (future)
1) Outbox (push): select `segments` where `state = recorded` → POST metadata (id, sha256, codec, durations) → server returns presigned URL (or direct upload contract). PUT the file idempotently. Mark `uploaded` on success.
2) Pull (fetch): `GET /changes?cursor=…` returns labels/edits; merge by version/E‑Tag into `segments`.
3) Retry/backoff: exponential backoff with jitter, persist attempts in `uploads`.

## Idempotency
- Client‑generated `id` per segment; include `idempotency-key` on metadata POSTs.
- Content address (sha256) + server constraints prevent duplicates.
- All client actions can be retried safely without creating multiple records.

## Caching & Performance
- Read UI from the DB (Repository layer), not from the filesystem.
- Keep recent segments in memory for quick list rendering.
- Batch operations (e.g., compute waveform lazily or cache per‑file peaks).

## Bootstrapping & Reconciliation
- On launch: open DB, run migrations, scan `segments/` for orphan files (backfill DB entries) to ensure disk/DB consistency.
- Rebuild the Recordings list from DB so data survives restarts.

## Cross‑Platform Parity
- iOS: GRDB + URLSession background tasks + BGTaskScheduler.
- Android: Room/SQLDelight + WorkManager.
- PWA: IndexedDB (Dexie.js) + Service Worker + Background Sync/alarms.
- Share types via OpenAPI/GraphQL; generate clients for Swift/Kotlin/TypeScript.

## Next Steps (implementation)
- Add `Persistence/Paths`, `Hashing`, `Database` (GRDB), `Models/SegmentRecord`, `Repositories/SegmentRepository`.
- Switch `AudioRecorder` to write finalized segments into Application Support and insert DB rows.
- Load segments from DB at app start; update UI bindings.
- (Optional) Add an Outbox skeleton that transitions `recorded → queued` to prepare for server sync.

This plan is minimal yet scalable: it gives us reliable local persistence, a clean path to add sync, and a UI that remains responsive and robust.
