# Live Status Verification (Audio, Photos, DB)

This note captures how to verify that incoming audio/photo uploads are healthy, how to read backend + device logs, and what a “correct” database stream looks like.

## 1) Backend runtime check

- Start backend with logging (reload optional):
  ```bash
  source ~/miniconda3/bin/activate glass
  python backend/bridge/tools/backend_logger.py --reload --port 8765
  ```
- Healthy signs:
  - `[ThreadPool] Default executor workers set to …`
  - `[DB] Connected to Postgres…`
  - `WebSocket /ws/audio-ingest [accepted]`
  - `WebSocket /ws/photo-ingest [accepted]`
  - `GET /api/v1/photos/<id> 200 OK` repeatedly as photos arrive.

## 2) Device (ESP32) serial logging

- Quick capture (e.g., 60–180 s):
  ```bash
  source ~/miniconda3/bin/activate glass
  python backend/bridge/tools/serial_logger.py --port /dev/ttyACM0 --baud 115200 --out logs/ideasglass-serial
  ```
- Healthy signs:
  - `WiFi Connected …`
  - `Audio] PDM microphone ready`
  - `Camera] Captured photo …` every ~15 s
  - `PhotoUpload] send result: OK (… chars)` when WS/HTTP succeeds
- Notes:
  - Suppressed per‑chunk audio prints by default to reduce noise.
  - If you see `WS Connect failed…` the device couldn’t open TLS; fallback HTTP then tries `POST /api/v1/messages`.

## 3) Database verification

Run the following from the repo root:

```bash
# Current time + total messages
psql ideasglass_db -c "SELECT now() as now, count(*) FROM ig_messages;"

# Last 5 messages
psql ideasglass_db -c "SELECT received_at, device_id, message FROM ig_messages ORDER BY received_at DESC LIMIT 5;"

# Cadence (15 s target, occasional multiples OK during reconnect)
psql ideasglass_db -c "WITH msgs AS (
  SELECT received_at,
         substring(message from '@ (\\d+)s')::int AS uptime_s
  FROM ig_messages WHERE device_id='ideasglass-devkit-01'
  ORDER BY received_at DESC LIMIT 40
), ord AS (
  SELECT received_at, uptime_s,
         received_at - lag(received_at) OVER (ORDER BY received_at)  AS wall_delta,
         uptime_s   - lag(uptime_s)   OVER (ORDER BY received_at)  AS uptime_delta
  FROM msgs ORDER BY received_at
)
SELECT received_at, wall_delta, uptime_delta
FROM ord ORDER BY received_at DESC LIMIT 12;"

# Recent photos (size + timing)
psql ideasglass_db -c "SELECT p.created_at, m.device_id, OCTET_LENGTH(p.data) AS bytes
FROM ig_photos p JOIN ig_messages m ON m.id=p.message_id
ORDER BY p.created_at DESC LIMIT 10;"
```

- Healthy signs:
  - wall_delta ~ 00:00:15 (± a few seconds jitter).
  - uptime_delta ~ 15 most of the time (multiples like 30/45/60 show a missed tick that recovered).
  - Each message with a photo should have a corresponding row in `ig_photos` within a few ms of `received_at`.
  - Photo sizes steady (low‑res QVGA typically ~7–9 KB in this setup).

## 4) What to look for when something’s off

- Device serial shows `WS Connect failed …` and `HTTP Connection failed` repeatedly:
  - The device cannot open a TLS/HTTP connection to the host at that moment (tunnel offline or CA/trust mismatch). Audio may still look fine if its WS stayed connected; photo, which connects intermittently, will miss ticks.
- Backend shows `Failed to process payload: Invalid photo_base64 …`:
  - Indicates malformed/empty base64; after the decode fix, this should not occur.
- Occasional cadence gaps (30/45/60 s):
  - Normal reconnect blips; audio keeps streaming, photo arrives on the next tick.

## 5) Expected “good” profile (example)

- Messages arriving roughly every 15 s.
- Photo rows for each message with sizes ~7.8–8.2 KB.
- Backend logs: WS accepted for audio+photo; `GET /api/v1/photos/<id> 200 OK` repeatedly.
- Serial logs: camera capture ~15 s, `send result: OK` lines present; no device panics.

## 6) Optional: dashboards

Use the provided Grafana + Loki stack in `ops/observability/` to aggregate backend + serial logs and query in one UI. See `docs/observability_stack.md` for setup.
