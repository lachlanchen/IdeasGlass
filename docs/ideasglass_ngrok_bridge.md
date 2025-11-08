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

The firmware now keeps a persistent TLS WebSocket open to the bridge so audio can flow continuously with almost no sample loss:

- **ESP32 firmware**
  - Keep `Tools → PSRAM → Enabled`, then flash `IdeasGlassNgrokClient.ino`.
  - I2S reads still happen at 16 kHz, but every 4096-sample block is copied into PSRAM and pushed to a FreeRTOS queue immediately. A dedicated sender task Base64-encodes the chunk and writes a masked WebSocket frame to `wss://ideas.lazying.art/ws/audio-ingest`, so capture never stalls while HTTPS handshakes complete.
  - Serial logs show per-chunk RMS/peak (from the capture loop) plus the final WebSocket send status (from the sender task).
- **Backend**
  - Accepts the same JSON payload via HTTP (`POST /api/v1/audio`) or WebSocket (`/ws/audio-ingest`) and runs WebRTC VAD (`webrtcvad`) + gain staging on every chunk.
  - Segments now close deterministically when `IDEASGLASS_SEGMENT_TARGET_MS` (default **15 000 ms**) is reached. A trailing window (`IDEASGLASS_SEGMENT_OVERLAP_MS`, default 2000 ms) is copied into the next clip, guaranteeing overlap but no gaps.
  - When a segment is sealed we apply a second-stage gain (`IDEASGLASS_SEGMENT_GAIN_TARGET`, defaults to the per-chunk target) before emitting the WAV so every clip lands at a consistent loudness.
  - Each finalized clip is pushed through WhisperX (default `large-v2` on CUDA) for aligned, speaker-diarized transcripts. Provide `HUGGINGFACE_TOKEN` (or `IDEASGLASS_HF_TOKEN`) to enable pyannote diarization. Toggle via `IDEASGLASS_TRANSCRIBE=0` if you need to disable it.
  - `/healthz` reports `segment_target_ms`, and every chunk broadcast includes `segment_duration_ms` + `active_segment_id`, letting the UI show exact recorder progress.
  - PCM buffers stream straight to `backend/ngrok_bridge/audio_segments/in_progress/` during capture, then promote to `audio_segments/<segment>.wav` (with the Postgres row pointing at the file).
- **PWA**
  - The waveform still uses 72 neon bars with the speaking glow, but the timer now shows `Recording X.X s / 15.0 s` with a progress bar that fills as the backend reports `segment_duration_ms`.
  - The “Last chunk” label includes RMS plus the current segment’s elapsed time; the list of recordings updates immediately because clips finalize as soon as they cross the target duration (no more waiting for silence).
  - A transcript tray under the waveform shows the diarized sentences for the most recent segment (cleared as soon as the next 15 s block starts).

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
GET /api/v1/audio/{chunk_id}              -> audio/wav
GET /api/v1/audio/segments
GET /api/v1/audio/segments/{segment_id}   -> audio/wav (~15 s clip with overlap)
WS  wss://ideas.lazying.art/ws/audio-ingest (send the same JSON payload as POST /api/v1/audio)
```
- WebSocket events also include `audio_transcript` payloads with `{segment_id, chunks: [{speaker, text, start, end}]}`, plus a `history_audio_transcripts` bootstrap so the UI can show the latest diarized block on refresh.

Use these knobs to tune the pipeline without reflashing:

- `IDEASGLASS_GAIN_TARGET`, `IDEASGLASS_GAIN_MAX`, `IDEASGLASS_GAIN_MIN_RMS`, `IDEASGLASS_SPEECH_RMS`, `IDEASGLASS_SPEECH_MARGIN` — per-chunk gain + VAD
- `IDEASGLASS_SEGMENT_TARGET_MS`, `IDEASGLASS_SEGMENT_OVERLAP_MS`, `IDEASGLASS_SEGMENT_GAIN_TARGET` — recorder window length, overlap, and clip-level gain
- `IDEASGLASS_TRANSCRIBE`, `IDEASGLASS_WHISPERX_*`, `IDEASGLASS_HF_TOKEN` — control WhisperX model/device/batch size and provide the Hugging Face token required for pyannote diarization

For debugging, the PWA still logs `[IdeasGlass][wave] …` entries to the browser console for history batches, live chunks, and finalized segments, so you can verify the stream at a glance.

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
