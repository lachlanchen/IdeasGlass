# Firmware: Arduino CLI, Upload, and Logging

This guide documents a repeatable workflow to compile, flash, and debug the IdeasGlass firmware using Arduino CLI, plus serial logging and DB correlation for end‑to‑end photo/audio diagnostics.

## 1) Environment

- Activate the `glass` env (recommended for tooling alignment):

```bash
source ~/miniconda3/bin/activate glass
```

- Install Arduino CLI (one‑time):

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH="$PWD/bin:$PATH"      # add to PATH for this repo checkout
arduino-cli version
```

- Initialize CLI and install ESP32 core (one‑time):

```bash
arduino-cli config init || true
arduino-cli core update-index
arduino-cli core install esp32:esp32
```

## 2) Board detection and FQBN

Identify the connected board/port and Full Qualified Board Name (FQBN):

```bash
arduino-cli board list
arduino-cli board listall | rg -i xiao
arduino-cli board details -b esp32:esp32:XIAO_ESP32S3
```

For Seeed XIAO ESP32S3 (with PSRAM enabled), the FQBN options used here are:

```text
esp32:esp32:XIAO_ESP32S3:PSRAM=opi,USBMode=hwcdc,CDCOnBoot=default,UploadSpeed=921600
```

## 3) Compile and upload

Set variables as needed and run compile + upload:

```bash
export PATH="$PWD/bin:$PATH"
PORT=/dev/ttyACM0
SKETCH=IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient
FQBN=esp32:esp32:XIAO_ESP32S3:PSRAM=opi,USBMode=hwcdc,CDCOnBoot=default,UploadSpeed=921600

# Compile
arduino-cli compile --fqbn "$FQBN" "$SKETCH"

# Upload
arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

Notes
- If upload fails with permissions, add your user to the serial group (Linux): `sudo usermod -a -G dialout $USER` and re‑login.
- If you see a different serial device, adjust `PORT` (e.g., `/dev/ttyACM1`, `/dev/ttyUSB0`).

## 4) Serial logging (Python)

Use the built‑in logger to capture firmware logs with timestamps and tags:

```bash
pip install pyserial
python backend/ngrok_bridge/tools/serial_logger.py --list
python backend/ngrok_bridge/tools/serial_logger.py --port /dev/ttyACM0 --baud 115200 --out logs/ideasglass-serial
```

- Output files: `logs/ideasglass-serial/*.log` (text), `*.jsonl` (structured).
- The logger tags lines like:
  - `photo_ws_failed` for `[PhotoUpload] WS send failed`
  - `audio_chunk` for audio sender activity
  - `camera_captured` for camera events
  - `wifi_connected` for Wi‑Fi state changes

Quick 3‑minute capture (non‑interactive):

```bash
timeout 185s python backend/ngrok_bridge/tools/serial_logger.py --port /dev/ttyACM0 --baud 115200 --out logs/ideasglass-serial || true
```

## 5) Backend DB correlation (optional)

Verify photo cadence and persist latency using `psql` against `ideasglass_db`:

```sql
-- Photo interval and device uptime deltas (recent 20)
WITH msgs AS (
  SELECT received_at,
         (meta->>'rssi')::int AS rssi,
         substring(message from '@ (\\d+)s')::int AS uptime_s
  FROM ig_messages
  WHERE device_id='ideasglass-devkit-01'
  ORDER BY received_at DESC
  LIMIT 50
), ordered AS (
  SELECT received_at, rssi, uptime_s,
         received_at - lag(received_at) OVER (ORDER BY received_at) AS wall_delta,
         uptime_s - lag(uptime_s)       OVER (ORDER BY received_at) AS uptime_delta
  FROM msgs
  ORDER BY received_at
)
SELECT received_at, rssi, uptime_delta, wall_delta
FROM ordered
ORDER BY received_at DESC
LIMIT 20;

-- DB write latency for photos (message arrival → photo row write)
SELECT m.received_at, p.created_at,
       (p.created_at - m.received_at) AS db_write_delay,
       OCTET_LENGTH(p.data) AS bytes
FROM ig_messages m
JOIN ig_photos   p ON p.message_id = m.id
WHERE m.device_id='ideasglass-devkit-01'
ORDER BY m.received_at DESC
LIMIT 20;
```

Interpretation
- `wall_delta` near 00:00:15 means ~15 s cadence is being respected.
- `db_write_delay` ~3–7 ms indicates the backend stores photos immediately after receipt; delays originate before the server sees the request.

## 6) Current photo send policy (cadence over fallback)

- The firmware uses a dedicated WebSocket for photos and drops a frame if a WS send fails (no HTTP fallback), to ensure the next 15 s capture isn’t blocked by TLS/HTTP. Audio continues on its separate persistent WebSocket.
- Serial lines to watch:
  - Success: `[PhotoUpload] send result: OK (NNNN chars)`
  - Transient drop: `[PhotoUpload] WS send failed — dropping frame (no fallback)`

## 7) One‑liners

Compile, upload, then log for 3 minutes:

```bash
export PATH="$PWD/bin:$PATH" && \
FQBN=esp32:esp32:XIAO_ESP32S3:PSRAM=opi,USBMode=hwcdc,CDCOnBoot=default,UploadSpeed=921600 && \
arduino-cli compile --fqbn "$FQBN" "IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient" && \
arduino-cli upload -p /dev/ttyACM0 --fqbn "$FQBN" "IdeaGlass/firmware/ideasglass_arduino/IdeasGlassNgrokClient" && \
timeout 185s python backend/ngrok_bridge/tools/serial_logger.py --port /dev/ttyACM0 --baud 115200 --out logs/ideasglass-serial || true
```

## 8) Troubleshooting

- No serial output captured:
  - Verify port with `--list`; check permissions; press the reset button; DTR/RTS is toggled automatically by the logger.
- Upload issues:
  - Try a slower upload speed: `UploadSpeed=460800`.
  - Confirm PSRAM option matches your board: `PSRAM=opi` vs `PSRAM=disabled`.
- Gaps in photo cadence with continuous audio:
  - Look for `photo_ws_failed` tags; short bursts imply transient WS/TLS hitches. Frames are dropped to keep timing; cadence should recover by the next 15 s tick.

