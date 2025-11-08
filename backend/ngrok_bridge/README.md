# IdeasGlass Ngrok Bridge

Minimal HTTPS backend + PWA dashboard for receiving Arduino telemetry over Ngrok and printing it live on web / Android / iOS (via installable PWA).

## Features

- `POST /api/v1/messages` – text + metadata + optional `photo_base64`
- `POST /api/v1/audio` – Base64 PCM audio blocks (16 kHz mono) with RMS metadata + WebRTC VAD flag
- WebSocket `/ws/stream` – typed events (`history_messages`, `message`, `history_audio`, `audio_chunk`)
- Background audio segmentation: chunks are buffered (~60s target) until the VAD detects trailing silence, converted to WAV on disk (`backend/ngrok_bridge/audio_segments/`) and referenced via `ig_audio_segments`
- PWA front-end installable on Android/iOS/Desktop with a polished neon waveform, live SILENCE/SPEAKING badge, lazy-loading feed, and Add-to-Home-Screen prompt
- Optional Postgres persistence (`DATABASE_URL`) for metadata (`ig_messages`), photos (`ig_photos`), audio chunks (`ig_audio_chunks`), and WAV segments (`ig_audio_segments`)

## Quickstart

1. **Install dependencies**
   ```bash
   cd backend/ngrok_bridge
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run the server**
   ```bash
   export DATABASE_URL="postgresql://lachlan@localhost/ideasglass_db"
   uvicorn backend.ngrok_bridge.app:app \
     --host 0.0.0.0 \
     --port 8765 \
     --proxy-headers \
     --forwarded-allow-ips="*"
   ```
   > If Ngrok terminates TLS for you, plain HTTP locally is fine. Add `--ssl-*` flags if you want end-to-end TLS.

3. **Expose via Ngrok**
   ```bash
   ngrok http http://localhost:8765 --domain=ideas.lazying.art --host-header=rewrite
   ```

4. **Open the dashboard**
   - Browser/PWA: https://ideas.lazying.art/  (install on Android/iOS via browser menu)
   - Healthcheck: https://ideas.lazying.art/healthz

5. **Send a test message**
   ```bash
   curl -X POST https://ideas.lazying.art/api/v1/messages \
     -H 'Content-Type: application/json' \
     -d '{"device_id":"dev-001","message":"hello from curl"}'
   ```
6. **Send a test photo**
   ```bash
   curl -X POST https://ideas.lazying.art/api/v1/messages \
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
   curl -X POST https://ideas.lazying.art/api/v1/audio \
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
   curl https://ideas.lazying.art/api/v1/audio/segments | jq '.[0]'
   curl -o latest.wav https://ideas.lazying.art/api/v1/audio/segments/<segment-id>
   ```

## Arduino integration

- Use the provided example sketch `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient/IdeasGlassNgrokClient.ino`
- The sketch loads Wi-Fi credentials from `wifi_credentials.h`, connects to your AP, then uses `WiFiClientSecure` with the LetsEncrypt PEM (embedded) to POST JSON to `/api/v1/messages`
- Update `kServerHost`, `kServerPort` (default `ideas.lazying.art:443`) and `kDeviceId` as needed

## Folder structure

```
backend/ngrok_bridge/
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
