# IdeasGlass Tornado API

Lightweight ingestion and fan-out layer for the redesigned Arduino firmware. It accepts telemetry over HTTPS, writes to Postgres, and pushes live updates to Flutter (Android/iOS/Web) clients via WebSockets.

## Features

- Async Tornado server (`app/server.py`) with modular handlers
- Postgres persistence powered by `asyncpg`
- Device authentication via `X-Device-Secret` headers
- WebSocket hub for live updates to the IdeasGlass PWA
- SQL migrations for `ideasglass_db`

## Quickstart

```bash
cd backend/tornado_app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export POSTGRES_DSN="postgresql://lachlan@localhost/ideasglass_db"
export DEVICE_SECRETS='{"ideasglass-001":"replace-me"}'
python main.py
```

The server listens on `0.0.0.0:8081` by default. Override with `LISTEN_PORT`.

### Telemetry ingest

```bash
curl -X POST http://localhost:8081/api/v1/ingest \
  -H 'Content-Type: application/json' \
  -H 'X-Device-Secret: replace-me' \
  -d '{
    "device_id": "ideasglass-001",
    "ts": 1736382300,
    "battery": 84,
    "voltage": 3.98,
    "ambient_lux": 120.5,
    "mic_level": 0.28,
    "quat": [0.9, 0.02, 0.01, 0.43],
    "accel": [0.01, 0.03, 1.02],
    "photo": {"id": "pic-1736382300", "size": 24312}
  }'
```

Response:

```json
{
  "telemetry_id": 42,
  "recorded_at": "2025-01-08T15:25:00+00:00",
  "upload_url": "https://ideasglass.local/uploads/pic-1736382300"
}
```

### WebSocket stream

Clients subscribe with `wss://host/ws/devices/<device_id>` and receive envelopes such as:

```json
{
  "type": "telemetry",
  "payload": {
    "device_id": "ideasglass-001",
    "ts": 1736382300,
    "battery": 84,
    "ambient_lux": 120.5,
    "mic_level": 0.28,
    "photo": {
      "id": "pic-1736382300",
      "size": 24312,
      "crc32": 1234554321
    }
  }
}
```

## Database migrations

```
psql -d ideasglass_db -f migrations/001_init.sql
```

See `migrations/001_init.sql` for the schema covering `devices`, `telemetry_events`, and `photos`.
