# IdeasGlass Ngrok Bridge

Minimal HTTPS backend + PWA dashboard for receiving Arduino telemetry over Ngrok and printing it live on web / Android / iOS (via installable PWA).

## Features

- `POST /api/v1/messages` – Arduino devices send JSON payloads (`device_id`, `message`, optional `meta`)
- WebSocket `/ws/stream` – pushes new entries to connected browsers in realtime
- PWA front-end (`/static/index.html`) installable on Android/iOS/Desktop, showing message feed
- Works behind Ngrok with your custom TLS certificate (`ideas.lazying.art`)

## Quickstart

1. **Install dependencies**
   ```bash
   cd backend/ngrok_bridge
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run the server (TLS)**
   ```bash
   uvicorn app:app \
     --host 0.0.0.0 --port 8443 \
     --ssl-certfile ../private/ideas.lazying.art_raw_pem.pem \
     --ssl-keyfile /path/to/ideas.lazying.art.key
   ```
   > Replace the `--ssl-keyfile` path with your actual private key. If Ngrok terminates TLS for you, you can skip the `--ssl-*` flags locally and let Ngrok handle HTTPS.

3. **Expose via Ngrok**
   ```bash
   ngrok http https://localhost:8443 --domain=ideas.lazying.art --host-header=rewrite
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
