# IdeasGlass Bridge

Minimal HTTPS backend + PWA dashboard for receiving Arduino telemetry and printing it live on web / Android / iOS (via installable PWA).

## Features

- `POST /api/v1/messages` – text + metadata + optional `photo_base64`
- `POST /api/v1/audio` – Base64 PCM audio blocks (16 kHz mono) with RMS metadata, WebRTC VAD flag, and the active segment’s elapsed time
- WebSocket `/ws/audio-ingest` – accepts the same JSON payload as `/api/v1/audio` for low-latency chunk streaming (used by the ESP32 firmware)
- WebSocket `/ws/stream` – typed events (`history_messages`, `message`, `history_audio`, `audio_chunk`, `audio_segment`) for the dashboard
- Background audio segmentation: chunks stream to disk immediately, and deterministic ~15 s WAV files (default overlap 2 s) are emitted continuously with per-clip gain (`ig_audio_segments`)
- Streaming openai-whisper transcripts broadcast every few seconds (defaults 3 s/6 s/15 s) so the waveform shows “typing” updates while recording; backend VAD skips pure-silence windows, and final updates arrive when the 15 s segment seals. Final transcripts are persisted in Postgres (`ig_audio_transcripts`) and exposed via `GET /api/v1/audio/segments/{segment_id}/transcript` for the dashboard popup.
- PWA front-end installable on Android/iOS/Desktop with a polished neon waveform, live SILENCE/SPEAKING badge, lazy-loading feed, a recorder progress bar, and a “Recent recordings” panel with download links
- Optional Postgres persistence (`DATABASE_URL`) for metadata (`ig_messages`), photos (`ig_photos`), audio chunks (`ig_audio_chunks`), and WAV segments (`ig_audio_segments`). Without Postgres, uploaded photos are written to `backend/bridge/static/photos/` and served directly.
- Automatic cuDNN path detection so CUDA-based Whisper streaming works even when cuDNN is installed via pip

## Quickstart

1. **Install dependencies**
   ```bash
   cd backend/bridge
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run the server**
   ```bash
   export DATABASE_URL="postgresql://lachlan@localhost/ideasglass_db"
   uvicorn backend.bridge.app:app \
     --host 0.0.0.0 \
     --port 8765 \
     --proxy-headers \
     --forwarded-allow-ips="*"
   ```
   > If Ngrok terminates TLS for you, plain HTTP locally is fine. Add `--ssl-*` flags if you want end-to-end TLS.

4. **Open the dashboard**
   - Browser/PWA: https://localhost:8765/  (install on Android/iOS via browser menu)
   - Healthcheck: https://localhost:8765/healthz

5. **Send a test message**
   ```bash
   curl -X POST https://localhost:8765/api/v1/messages \
     -H 'Content-Type: application/json' \
     -d '{"device_id":"dev-001","message":"hello from curl"}'
   ```
6. **Send a test photo**
   ```bash
   curl -X POST https://localhost:8765/api/v1/messages \
     -H 'Content-Type: application/json' \
     -d '{
       "device_id":"dev-001",
       "message":"photo demo",
       "photo_base64":"'"$(base64 -w0 sample.jpg)"'",
       "photo_mime":"image/jpeg"
     }'
   ```
7. **Send a test audio chunk**
   ```bash
   rec --bits 16 --channels 1 --rate 16000 -c 1 -b 16 -e signed-integer temp.raw trim 0 0.25
   curl -X POST https://localhost:8765/api/v1/audio \
     -H 'Content-Type: application/json' \
     -d '{
       "device_id":"dev-001",
       "sample_rate":16000,
       "bits_per_sample":16,
       "duration_ms":250,
       "rms":0.05,
       "audio_base64":"'"$(base64 -w0 temp.raw)"'"
     }'
   ```
8. **List audio segments & download WAV**
   ```bash
   curl https://localhost:8765/api/v1/audio/segments | jq '.[0]'
   curl -o latest.wav https://localhost:8765/api/v1/audio/segments/<segment-id>
   ```

## Arduino integration

- Use the provided example sketch `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient/IdeasGlassNgrokClient.ino`
- The sketch loads Wi-Fi credentials from `wifi_credentials.h`, connects to your AP, then uses `WiFiClientSecure` with the LetsEncrypt PEM (embedded) to POST JSON to `/api/v1/messages`
- Audio capture uses a FreeRTOS queue plus a tiny WebSocket client that keeps a persistent TLS connection to `/ws/audio-ingest`, so 16 kHz PCM blocks keep flowing even while uploads happen in the background
- Update `kServerHost`, `kServerPort` (default `localhost:8765:443`) and `kDeviceId` as needed

## Folder structure

```
backend/bridge/
├── app.py                # FastAPI app + websocket broadcaster
├── requirements.txt
├── README.md
└── static/
    ├── index.html        # PWA shell
    ├── app.js            # WebSocket client & UI logic
    ├── styles.css
    ├── manifest.webmanifest
    ├── sw.js             # service worker for offline install
    └── icons/            # PWA icons (192px / 512px)
```

Happy building!
- **Audio gain controls** – the backend normalizes each chunk toward `IDEASGLASS_GAIN_TARGET` (default `0.032` RMS) but clamps amplification to `IDEASGLASS_GAIN_MAX` (`1.8`). Silence below `IDEASGLASS_GAIN_MIN_RMS` (`0.008`) stays untouched. Speech detection now requires `IDEASGLASS_SPEECH_RMS` (`0.03`) and will only fall back to RMS when the WebRTC VAD can’t run, using the margin `IDEASGLASS_SPEECH_MARGIN` (`0.005`). Tune these env vars if you need louder or quieter recordings.
- **Streaming segments** – partial PCM is appended to `backend/bridge/audio_segments/in_progress/` as chunks arrive. Completed segments are promoted to `.wav` files under `backend/bridge/audio_segments/` and exposed via `/api/v1/audio/segments`.
- **Segment windows** – clip length/overlap/final gain are controlled via `IDEASGLASS_SEGMENT_TARGET_MS` (default 15000 ms), `IDEASGLASS_SEGMENT_OVERLAP_MS` (default 2000 ms), and `IDEASGLASS_SEGMENT_GAIN_TARGET` (defaults to the chunk gain target). `/healthz` reports the active target so the recorder progress bar in the PWA stays aligned with the backend.
- **Transcription** – set `IDEASGLASS_TRANSCRIBE=1` (default) with `openai-whisper` installed. Tweak `IDEASGLASS_WHISPER_MODEL`, `IDEASGLASS_WHISPER_DEVICE`, `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`, and `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` (comma-separated millisecond values, default `3000,6000,15000`) to control latency; disable via `IDEASGLASS_TRANSCRIBE=0` if GPU resources are tight.
