---
title: IdeasGlass Ngrok Bridge
description: End-to-end setup for the FastAPI backend, PWA, Ngrok tunnel, and Arduino HTTPS client.
---

# Overview

This guide documents the exact steps we used to relay Arduino data (text + photos) to a public HTTPS endpoint (`https://ideas.lazying.art`), persist it in Postgres, and display it in a light-themed PWA installable on Android/iOS/Desktop. The stack consists of:

- `backend/ngrok_bridge` — FastAPI + WebSocket server with a PWA front-end
- `ngrok` — exposes the local server over `ideas.lazying.art`
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient/` — ESP32 sketch that posts JSON payloads over TLS

# 1. Backend & PWA

1. **Activate the conda env (already created):**
   ```bash
   source ~/miniconda3/bin/activate glass
   ```
2. **Install requirements (already done but harmless to repeat):**
   ```bash
   pip install -r backend/ngrok_bridge/requirements.txt
   ```
3. **Export your Postgres connection (runs migrations automatically):**
   ```bash
   export DATABASE_URL="postgresql://lachlan@localhost/ideasglass_db"
   ```
4. **Launch uvicorn on an unused port (8765 chosen to avoid collisions):**
   ```bash
   uvicorn backend.ngrok_bridge.app:app \
     --host 0.0.0.0 \
     --port 8765 \
     --proxy-headers \
     --forwarded-allow-ips="*"
   ```
   - Use a different port if 8765 becomes occupied.
   - If you want end-to-end TLS locally, add `--ssl-certfile` / `--ssl-keyfile` pointing to your cert + key. Otherwise let Ngrok terminate TLS.
5. **Ngrok tunnel (maps the public domain to your local port):**
   ```bash
   ngrok http http://localhost:8765 \
     --domain=ideas.lazying.art \
     --host-header=rewrite
   ```
   Once Ngrok reports `Forwarding  https://ideas.lazying.art -> http://localhost:8765`, the public URL is live.
6. **Verify backend health:** `curl https://ideas.lazying.art/healthz` should return `{"status":"ok","messages":...}`.
7. **Open the PWA dashboard** at `https://ideas.lazying.art/`:
   - Shows **Backend Online / WebSocket Connected** states.
   - Live feed cards now include inline photos if the Arduino sent one.
   - Use “Add to Home Screen” (or the built-in “Add” button) to install it on Android/iOS.

# 2. Arduino HTTPS client

1. Ensure `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.h` exists (copy the `.example` if needed) with your Wi-Fi SSID/password.
2. Open `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient/IdeasGlassNgrokClient.ino` in Arduino IDE.
   - Defaults: `kServerHost = "ideas.lazying.art"`, `kServerPort = 443`, `kDeviceId = "ideasglass-devkit-01"`.
   - The sketch now initializes the XIAO ESP32S3 Sense camera, captures QVGA JPEG frames, Base64-encodes them, and embeds them in the HTTPS payload (`photo_base64` + MIME type) alongside the text message.
   - **Important:** set `Tools → PSRAM → Enabled` before flashing; the framebuffer lives in PSRAM and the sketch falls back to QQVGA if memory runs low.
3. Upload to the XIAO ESP32S3. Serial monitor will show Wi-Fi status, camera activity, and repeated `POST /api/v1/messages` responses.
4. Each payload appears instantly in the PWA feed, and both the metadata + photo are stored in Postgres (`ig_messages` + `ig_photos`). The firmware flips the camera output (`set_vflip`/`set_hmirror`) so images arrive upright without server-side rotation.

# 3. Audio streaming + waveform UI

The firmware now treats audio as the primary data stream:

- **ESP32 firmware** — set `Tools → PSRAM → Enabled`, then flash `IdeasGlassNgrokClient.ino`. It samples the onboard PDM microphone at 16 kHz, logs per-chunk RMS/peaks, and posts ~250 ms PCM blocks to `/api/v1/audio`.
- **Backend** — runs WebRTC VAD (`webrtcvad`), normalizes each chunk toward `IDEASGLASS_GAIN_TARGET` (default 0.032 RMS, capped by `IDEASGLASS_GAIN_MAX`), streams every chunk to disk immediately, and finalizes WAV segments roughly every 15 s (with a ~2 s overlap) so playback feels continuous. Raw chunks still land in `ig_audio_chunks`, while referenced WAVs live in `ig_audio_segments`.
- **Storage** — in-progress PCM lives under `backend/ngrok_bridge/audio_segments/in_progress/` and is promoted to `backend/ngrok_bridge/audio_segments/<segment-id>.wav` once sealed. The Postgres row stores both the blob and the relative path so `/api/v1/audio/segments/{id}` can stream straight from disk.
- **PWA** — the recorder panel now mimics a neon VU meter (with a speaking glow), and a “Recent recordings” list surfaces the latest WAV segments with download links.

API quick reference:

```http
POST /api/v1/audio
{
  "device_id": "ideasglass-devkit-01",
  "sample_rate": 16000,
  "bits_per_sample": 16,
  "duration_ms": 256,
  "rms": 0.0312,
  "audio_base64": "...."
}

GET /api/v1/audio?limit=60&before=2025-11-08T09:00:00Z
GET /api/v1/audio/{chunk_id}  -> audio/wav
GET /api/v1/audio/segments
GET /api/v1/audio/segments/{segment_id} -> audio/wav (buffered ~15 s clip with overlap)
```

Every `/api/v1/audio` response now echoes `speech_detected`, and the websocket stream includes this flag in both the historical payload and live `audio_chunk` events. The front-end keeps the last 72 normalized levels to animate the waveform while the backend quietly aggregates WAV segments (with gain applied) for later download/analysis. Use `IDEASGLASS_GAIN_TARGET`, `IDEASGLASS_GAIN_MAX`, `IDEASGLASS_GAIN_MIN_RMS`, `IDEASGLASS_SPEECH_RMS`, or `IDEASGLASS_SPEECH_MARGIN` to tune loudness/silence thresholds without reflashing firmware.

For debugging, the PWA logs `[IdeasGlass][wave] …` entries to the browser console every time it receives history batches, live chunks, or finalized segments, so you can confirm data is flowing even before the visualization animates.

# 4. Useful commands

- **Manual photo test via curl:**
  ```bash
  curl -X POST https://ideas.lazying.art/api/v1/messages \
    -H 'Content-Type: application/json' \
    -d '{
      "device_id":"curl-test",
      "message":"hello from CLI",
      "photo_base64":"'"$(base64 -w0 sample.jpg)"'",
      "photo_mime":"image/jpeg"
    }'
  ```
- **List stored messages (served from Postgres when `DATABASE_URL` is set):**
  ```bash
  curl https://ideas.lazying.art/api/v1/messages | jq
  ```
- **Local access (without Ngrok):** open `http://localhost:8765` while uvicorn runs.

# 5. Troubleshooting

- **Port already in use:** pick another port (`--port 9123`) and update the Ngrok command to match.
- **SSL key missing:** either provide the real private key path via `--ssl-keyfile` or omit the SSL flags and let Ngrok handle TLS.
- **Postgres offline:** the server logs `[DB] Failed to initialize Postgres...` and falls back to in-memory mode (photos unavailable). Fix `DATABASE_URL` and restart uvicorn.
- **Arduino cannot connect:** ensure Ngrok is running, host is reachable, and the Wi-Fi credentials are correct. Serial logs will show HTTP responses; status code `200` confirms success.
- **PWA offline:** check `https://ideas.lazying.art/healthz`; if offline, restart uvicorn/Ngrok.

The logs shown earlier confirm the full pipeline works: Arduino sends `"Hello from IdeasGlass @ {n}s"` every ~20s, backend persists/broadcasts it, and the PWA shows the live feed. Keep both uvicorn and Ngrok terminals open for continuous testing.
