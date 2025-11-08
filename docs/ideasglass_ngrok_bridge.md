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
3. Upload to the XIAO ESP32S3. Serial monitor will show Wi-Fi status, camera activity, and repeated `POST /api/v1/messages` responses.
4. Each payload appears instantly in the PWA feed, and both the metadata + photo are stored in Postgres (`ig_messages` + `ig_photos` tables).

# 3. Useful commands

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

# 4. Troubleshooting

- **Port already in use:** pick another port (`--port 9123`) and update the Ngrok command to match.
- **SSL key missing:** either provide the real private key path via `--ssl-keyfile` or omit the SSL flags and let Ngrok handle TLS.
- **Postgres offline:** the server logs `[DB] Failed to initialize Postgres...` and falls back to in-memory mode (photos unavailable). Fix `DATABASE_URL` and restart uvicorn.
- **Arduino cannot connect:** ensure Ngrok is running, host is reachable, and the Wi-Fi credentials are correct. Serial logs will show HTTP responses; status code `200` confirms success.
- **PWA offline:** check `https://ideas.lazying.art/healthz`; if offline, restart uvicorn/Ngrok.

The logs shown earlier confirm the full pipeline works: Arduino sends `"Hello from IdeasGlass @ {n}s"` every ~20s, backend persists/broadcasts it, and the PWA shows the live feed. Keep both uvicorn and Ngrok terminals open for continuous testing.
