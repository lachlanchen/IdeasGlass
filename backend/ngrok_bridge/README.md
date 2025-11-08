# IdeasGlass Ngrok Bridge

Minimal HTTPS backend + PWA dashboard for receiving Arduino telemetry over Ngrok and printing it live on web / Android / iOS (via installable PWA).

## Features

- `POST /api/v1/messages` – Arduino devices send JSON payloads (`device_id`, `message`, optional `meta`, optional `photo_base64`)
- WebSocket `/ws/stream` – pushes new entries (including photo URLs) to connected browsers in realtime
- PWA front-end (`/static/index.html`) installable on Android/iOS/Desktop with a light-themed UI
- Optional Postgres persistence (set `DATABASE_URL`), storing both message metadata and JPEG binaries (`ig_messages`, `ig_photos`)

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
