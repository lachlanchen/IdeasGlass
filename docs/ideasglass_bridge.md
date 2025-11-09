---
title: IdeasGlass Bridge
description: End-to-end setup for the FastAPI backend, PWA, , and Arduino HTTPS client.
---

# Overview

This guide documents the exact steps we used to relay Arduino data (text + photos) to a public HTTPS endpoint (`https://localhost:8765`), persist it in Postgres, and display it in a light-themed PWA installable on Android/iOS/Desktop. The stack consists of:

- `backend/bridge` — FastAPI + WebSocket server with a PWA front-end
- `ngrok` — exposes the local server over `localhost:8765`
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` — ESP32 sketch that posts JSON payloads over TLS

# 1. Backend & PWA

1. **Activate the conda env (already created):**
   ```bash
   source ~/miniconda3/bin/activate glass
   ```
2. **Install requirements (already done but harmless to repeat):**
   ```bash
   pip install -r backend/bridge/requirements.txt
   ```
3. **Export your Postgres connection (runs migrations automatically):**
   ```bash
   export DATABASE_URL="postgresql://lachlan@localhost/ideasglass_db"
   ```
4. **Launch uvicorn on an unused port (8765 chosen to avoid collisions):**
   ```bash
   uvicorn backend.bridge.app:app \
     --host 0.0.0.0 \
     --port 8765 \
     --proxy-headers \
     --forwarded-allow-ips="*"
   ```
   - Use a different port if 8765 becomes occupied.
   - If you want end-to-end TLS locally, add `--ssl-certfile` / `--ssl-keyfile` pointing to your cert + key. Otherwise let  terminate TLS.
5. ** (maps the public domain to your local port):**
   ```bash
   ngrok http http://localhost:8765 \
     --domain=localhost:8765 \
     --host-header=rewrite
   ```
   Once  reports `Forwarding  https://localhost:8765 -> http://localhost:8765`, the public URL is live.
6. **Verify backend health:** `curl https://localhost:8765/healthz` should return `{"status":"ok","messages":...}`.
7. **Open the PWA dashboard** at `https://localhost:8765/`:
   - Shows **Backend Online / WebSocket Connected** states.
   - Live feed cards now include inline photos if the Arduino sent one.
   - Use “Add to Home Screen” (or the built-in “Add” button) to install it on Android/iOS.

# 2. Arduino HTTPS client

1. Ensure `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.h` exists (copy the `.example` if needed) with your Wi-Fi SSID/password.
2. Open `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` in Arduino IDE.
   - Defaults: `kServerHost = "localhost:8765"`, `kServerPort = 443`, `kDeviceId = "ideasglass-devkit-01"`.
   - The sketch now initializes the XIAO ESP32S3 Sense camera, captures QVGA JPEG frames, Base64-encodes them, and embeds them in the HTTPS payload (`photo_base64` + MIME type) alongside the text message.
   - **Important:** set `Tools → PSRAM → Enabled` before flashing; the framebuffer lives in PSRAM and the sketch falls back to QQVGA if memory runs low.
3. Upload to the XIAO ESP32S3. Serial monitor will show Wi-Fi status, camera activity, and repeated `POST /api/v1/messages` responses.
4. Each payload appears instantly in the PWA feed, and both the metadata + photo are stored in Postgres (`ig_messages` + `ig_photos`). The firmware flips the camera output (`set_vflip`/`set_hmirror`) so images arrive upright without server-side rotation.

# 3. Audio streaming + waveform UI

The firmware now keeps a persistent TLS WebSocket open to the bridge so audio can flow continuously with almost no sample loss:

- **ESP32 firmware**
  - Keep `Tools → PSRAM → Enabled`, then flash `IdeasGlassClient.ino`.
  - I2S reads still happen at 16 kHz, but every 4096-sample block is copied into PSRAM and pushed to a FreeRTOS queue immediately. A dedicated sender task Base64-encodes the chunk and writes a masked WebSocket frame to `wss://localhost:8765/ws/audio-ingest`, so capture never stalls while HTTPS handshakes complete.
  - Serial logs show per-chunk RMS/peak (from the capture loop) plus the final WebSocket send status (from the sender task).
- **Backend**
  - Accepts the same JSON payload via HTTP (`POST /api/v1/audio`) or WebSocket (`/ws/audio-ingest`) and runs WebRTC VAD (`webrtcvad`) + gain staging on every chunk.
  - Segments now close deterministically when `IDEASGLASS_SEGMENT_TARGET_MS` (default **15 000 ms**) is reached. A trailing window (`IDEASGLASS_SEGMENT_OVERLAP_MS`, default 2000 ms) is copied into the next clip, guaranteeing overlap but no gaps.
  - When a segment is sealed we apply a second-stage gain (`IDEASGLASS_SEGMENT_GAIN_TARGET`, defaults to the per-chunk target) before emitting the WAV so every clip lands at a consistent loudness.
  - A background openai-whisper worker performs rolling transcription every few seconds (default 3 s) so you see live text appear beneath the waveform. Tweak `IDEASGLASS_WHISPER_MODEL`, `IDEASGLASS_WHISPER_DEVICE`, `IDEASGLASS_TRANSCRIBE`, and `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` to suit your hardware. Final transcripts are cached and replayed via `history_audio_transcripts`.
  - `/healthz` reports `segment_target_ms`, and every chunk broadcast includes `segment_duration_ms` + `active_segment_id`, letting the UI show exact recorder progress.
  - PCM buffers stream straight to `backend/bridge/audio_segments/in_progress/` during capture, then promote to `audio_segments/<segment>.wav` (with the Postgres row pointing at the file).
  - Photo uploads hit `/api/v1/messages`; when Postgres is unavailable, the backend writes the decoded image to `backend/bridge/static/photos/` and serves it at `/static/photos/<photo-id>.jpg`, so the dashboard continues to display images without a database.
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
GET /api/v1/audio/segments/{segment_id}/transcript -> JSON transcript payload
WS  wss://localhost:8765/ws/audio-ingest (send the same JSON payload as POST /api/v1/audio)
```
- WebSocket events also include `audio_transcript` payloads with `{segment_id, chunks: [{speaker, text, start, end}], is_final}`, plus a `history_audio_transcripts` bootstrap so the UI can show the latest block on refresh.

Use these knobs to tune the pipeline without reflashing:

- `IDEASGLASS_GAIN_TARGET`, `IDEASGLASS_GAIN_MAX`, `IDEASGLASS_GAIN_MIN_RMS`, `IDEASGLASS_SPEECH_RMS`, `IDEASGLASS_SPEECH_MARGIN` — per-chunk gain + VAD
- `IDEASGLASS_SEGMENT_TARGET_MS`, `IDEASGLASS_SEGMENT_OVERLAP_MS`, `IDEASGLASS_SEGMENT_GAIN_TARGET` — recorder window length, overlap, and clip-level gain
- `IDEASGLASS_TRANSCRIBE`, `IDEASGLASS_WHISPER_MODEL`, `IDEASGLASS_WHISPER_DEVICE`, `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`, `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` — control the live Whisper streamer (default thresholds `3000,6000,15000` ms, silence chunks skipped via backend VAD); set `IDEASGLASS_TRANSCRIBE=0` to disable if resources are tight

For debugging, the PWA still logs `[IdeasGlass][wave] …` entries to the browser console for history batches, live chunks, and finalized segments, so you can verify the stream at a glance.

For debugging, the PWA logs `[IdeasGlass][wave] …` entries to the browser console every time it receives history batches, live chunks, or finalized segments, so you can confirm data is flowing even before the visualization animates.

# 4. Useful commands

- **Manual photo test via curl:**
  ```bash
  curl -X POST https://localhost:8765/api/v1/messages \
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
  curl https://localhost:8765/api/v1/messages | jq
  ```
- **Local access (without ):** open `http://localhost:8765` while uvicorn runs.

# 5. Troubleshooting

- **Port already in use:** pick another port (`--port 9123`) and update the  command to match.
- **SSL key missing:** either provide the real private key path via `--ssl-keyfile` or omit the SSL flags and let  handle TLS.
- **Postgres offline:** the server logs `[DB] Failed to initialize Postgres...` and falls back to in-memory mode (photos unavailable). Fix `DATABASE_URL` and restart uvicorn.
- **Arduino cannot connect:** ensure  is running, host is reachable, and the Wi-Fi credentials are correct. Serial logs will show HTTP responses; status code `200` confirms success.
- **PWA offline:** check `https://localhost:8765/healthz`; if offline, restart uvicorn/.

The logs shown earlier confirm the full pipeline works: Arduino sends `"Hello from IdeasGlass @ {n}s"` every ~20s, backend persists/broadcasts it, and the PWA shows the live feed. Keep both uvicorn and ngrok terminals open for continuous testing.

---

## 6. ESP32 connectivity + TLS checklist (what we fixed)

This subsection documents the issues we saw in the field and the exact firmware/back‑end settings that resolved them.

### Symptoms

- ESP32 serial showed repeated `[WS] Connect failed … /ws/photo-ingest` and `[Audio] Send queue full, dropping chunk`.
- Occasional lwIP assert after NTP attempts: `assert failed: udp_new_ip_type … Required to lock TCPIP core functionality!` (reboot loop).
- ngrok console reported intermittent `422 Unprocessable Entity` on `POST /api/v1/messages`.

### Root causes

- TLS time not set yet on cold boot: cert validation fails until NTP sets the RTC.
- SNTP initialized from the wrong thread context: calling into lwIP from the app thread can trip UDP pcb asserts on ESP‑IDF.
- Photo payload `meta` typed as numbers: backend schema expects `Dict[str, str]`.
- Access point friction for 2.4 GHz joins: re‑begin while associating and random BSSID choice cause flakiness on some routers.

### Firmware fixes (already applied)

- NTP on the TCP/IP core: SNTP init is posted via `tcpip_callback`, with Cloudflare/Google/pool servers; falls back to the LAN gateway IP if available. Logs show `[Time] SNTP synced: …` when ready.
- Robust Wi‑Fi association: fully reset the radio between attempts, scan and prefer the strongest BSSID/channel for the target SSID, then re‑enable Wi‑Fi sleep once connected.
- WS pings gated while offline: avoid noisy reconnect spam when STA is down.
- Photo meta as strings: `battery_v` and `battery_pct` are sent as strings to satisfy Pydantic’s `Dict[str, str]`.
- Autostart on upload/charge: `REQUIRE_LONG_PRESS_ON_BOOT=false` so flashing or charging boots normally; long‑press to deep sleep still works in run mode.

Relevant files:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`
- `IdeaGlass/firmware/ideasglass_arduino/config.h`

### Router/AP settings (dd‑wrt)

- 2.4 GHz SSID must be enabled (ESP32 is 2.4 GHz only).
- Security: WPA2‑Personal (AES). Disable WPA3‑SAE and set PMF to Disabled/Optional.
- Channel: fixed 1/6/11 at 20 MHz; avoid channels 12/13 unless the regulatory domain requires them.
- SSID broadcast enabled; MAC filter off (or allow the device MAC).
- For public domain access from LAN: enable NAT loopback (a.k.a. hairpin NAT).
- Allow outbound UDP/123 (NTP) to the Internet or provide an NTP service on the gateway.

### ngrok/edge observations

- ngrok showed `GET /ws/audio-ingest 101 Switching Protocols` ⇒ WSS reachable end‑to‑end.
- `422 Unprocessable Entity` on `/api/v1/messages` was caused by meta typing; fixed as above.
- If WSS from ESP32 becomes unstable on the WAN path, photos continue via HTTP fallback. Audio currently prefers WS only; you can optionally enable HTTP fallback to `/api/v1/audio` to eliminate rare stalls.

### Verify end‑to‑end

1) Backend

- `uvicorn backend.bridge.app:app --host 0.0.0.0 --port 8765 --proxy-headers --forwarded-allow-ips="*"`
- `curl http://localhost:8765/healthz` returns 200.
- Logs show `/ws/stream` and, when device connects, `/ws/audio-ingest`.

2) Firmware build/upload (Arduino CLI)

```bash
FQBN=esp32:esp32:XIAO_ESP32S3
bin/arduino-cli compile --fqbn $FQBN --board-options PSRAM=opi IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient
bin/arduino-cli upload  -p /dev/ttyACM0 --fqbn $FQBN --board-options PSRAM=opi IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient
```

3) Serial monitor (pyserial)

```bash
python3 - <<'PY'
import serial, sys
s=serial.Serial('/dev/ttyACM0',115200,timeout=0.5)
try:
  while True:
    line=s.readline()
    if line: sys.stdout.buffer.write(line); sys.stdout.flush()
except KeyboardInterrupt:
  pass
finally:
  s.close()
PY
```

Expect to see (in order):

- `[WiFi] Connected (dd-wrt, RSSI -XX)` and `IP: …`
- `[Time] SNTP synced: …`
- `[PhotoUpload] send result: OK (… chars)`
- For audio: backend shows `/ws/audio-ingest 101`; the PWA waveform and “Recent transcripts” update in near‑real‑time.

### Known limitations / options

- If corporate or campus networks block UDP/123, NTP sync will timeout; use the gateway fallback or open NTP.
- If WSS still hiccups on the WAN path, enable audio HTTP fallback in firmware to POST chunks to `/api/v1/audio` when WS send fails.
- The device remembers the last email for the PWA login overlay; session auth uses HTTP‑only cookies.

## 7. Live observations: photos smooth, audio occasional lag

With the current setup, we observed the following behavior during extended runs behind ngrok on a home router (dd‑wrt):

- Photos are smooth and reliable.
  - Reason: the firmware already has an HTTP fallback. If the `/ws/photo-ingest` socket stalls, it posts the same JSON to `POST /api/v1/messages`, which the backend accepts immediately. You’ll see consistent `200 OK` for `/api/v1/photos/<id>` in server logs and in the ngrok dashboard.

- Audio can feel bursty/laggy at times.
  - Reason: audio currently prefers the persistent WSS path `/ws/audio-ingest`. Short WAN or proxy stalls can block the sender briefly, causing the FreeRTOS audio queue to fill and print `Send queue full, dropping chunk`. The connection is then re‑established and chunks resume, so the PWA shows transcriptions in small bursts. Backend logs show `/ws/audio-ingest 101` followed by occasional disconnect/reconnect (expected during short drops).

What you can do to minimize lag:

1) Add audio HTTP fallback (recommended if WAN is flaky)
   - Mirror the photo strategy: when a WSS `send` fails or times out, `POST` the chunk to `/api/v1/audio`. The backend already supports this endpoint. This removes stalls at the cost of a small per‑request overhead.

2) Network and router
   - Ensure hairpin NAT (NAT loopback) is enabled so LAN devices can reliably reach the public domain.
   - Keep 2.4 GHz radio at 20 MHz on channel 1/6/11; WPA2‑AES only; PMF disabled/optional.
   - If you can, A/B test by temporarily pointing the firmware at the backend’s LAN IP; if WSS is rock‑solid on LAN but not over the domain, the edge/proxy path is the bottleneck.

3) Firmware tunables (optional)
   - Increase `AUDIO_QUEUE_LENGTH` (e.g., 6 → 12) to absorb brief network hiccups.
   - Reduce `AUDIO_BLOCK_SAMPLES` (e.g., 4096 → 2048) for lower per‑chunk latency.
   - Keep WSS ping at 1 s; consider shorter socket timeouts and quicker reconnect backoff.

4) Backend/PWA
   - Keep `IDEASGLASS_WHISPER_DEVICE=cuda` and a model your GPU can handle in real‑time (you’re using `large-v3-turbo`, which is good with CUDA).
   - `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` near 3000 ms keeps live text responsive without overloading the GPU.

Verification cues in logs:

- Backend shows:
  - `('...') - "WebSocket /ws/audio-ingest" [accepted]`
  - `Detected language: …` each time a segment is finalized
  - Occasional `connection closed` followed by a new `accepted` ⇒ short network blips recovered
- Firmware serial shows:
  - `[Time] SNTP synced: …` after Wi‑Fi connects
  - `[PhotoUpload] send result: OK (…)` regularly
  - If lag happens: a burst of `[Audio] Send queue full, dropping chunk` lines, then recovery

Note: We already fixed intermittent `422` on `/api/v1/messages` by sending `meta` values as strings from the firmware; ngrok should no longer show those.
