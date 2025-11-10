---
title: IdeasGlass Firmware Hardening Plan
description: Non‑breaking improvements to robustness, latency, and power without changing external behavior.
---

# Scope & Constraints

- Device: Seeed XIAO ESP32S3 Sense (camera + PDM mic, 8 MB PSRAM)
- Keep all external behavior identical (protocols, payloads, UX, timing). No breaking changes.
- Goal: smoother audio/photo under imperfect networks, fewer drops, and lower power draw.

# Guiding Principles

- Preserve current APIs: `/ws/audio-ingest`, `/ws/photo-ingest`, `/api/v1/audio`, `/api/v1/messages`.
- Avoid blocking the capture loops; isolate I/O on sender tasks.
- Prefer resource reuse (buffers, TLS sessions) to reduce CPU and fragmentation.
- Make all tunings feature‑flagged and off by default; enable gradually.

# Work Packages (No Functional Change)

## 1) Networking stability

- WSS reconnect/backoff (non‑blocking):
  - Exponential backoff with jitter; cap at 3–5 s.
  - Ensure sender task never blocks on reconnect.
- HTTPS keep‑alive pooling:
  - Maintain a single `WiFiClientSecure` for audio/photo POSTs; reuse connection if alive; reconnect on first failure.
  - Fast status‑line read then close (avoid reading full body when not needed).
- Preflight connectivity:
  - Check `WiFi.status()` and (optionally) `ping`/DNS resolve before expensive Base64 work; skip encode if offline.

## 2) Audio pipeline efficiency

- Preallocated buffer pool (ring of N blocks) to avoid malloc/free per chunk.
- Optional smaller chunk size (e.g., 2048 samples) to reduce per‑chunk latency (flag‑gated, default off).
- Integer/fast RMS path that matches current float result within tolerance (flag‑gated, default off).
- Maintain current sample rate/format and JSON fields exactly.

## 3) Photo pipeline resilience

- Camera re‑init policy:
  - Backoff on repeated failures; limit retries per minute.
- Power gating:
  - Use PWDN/reset between shots to save mA; only if sensor responds reliably (flag‑gated, default off).
- Encode in PSRAM; preallocate Base64 staging buffer sized from last frame.

## 4) Power usage improvements

- Wi‑Fi modem sleep: keep enabled; evaluate dynamic TX power reduction when RSSI > −55 dBm (flag‑gated, default off).
- Logging throttling: keep existing info logs; reduce debug spam under a build‑time flag.
- Optional CPU freq scaling during idle (no change by default).

## 5) Error handling & observability

- Bounded timeouts everywhere (already applied for HTTP); add per‑send timers to detect stalls.
- Lightweight counters exposed in serial (periodic):
  - `net.ws_audio_ok`, `net.ws_audio_fail`, `http.audio_ok/fail`, `photo_ok/fail`, `audio_queue_drop`.
- Watchdog:
  - Ensure FreeRTOS tasks yield; add optional task WDT hooks (flag‑gated).

# Rollout Plan (Stages)

1. Stage A (low‑risk wins):
   - HTTPS keep‑alive pooling; preflight connectivity; minimal serial counters.
2. Stage B (allocation):
   - Preallocated audio buffer pool + ring queue; PSRAM Base64 staging for photos.
3. Stage C (backoff):
   - Non‑blocking WSS reconnect with jitter; bounded timeouts everywhere.
4. Stage D (power):
   - Optional TX power tune + camera PWDN between shots (flags default off).
5. Stage E (polish):
   - Optional smaller audio chunks behind a build flag; verify identical server behavior.

# Validation & Metrics

- Benchmarks (before/after; same network):
  - Audio drops per minute (`audio_queue_drop`).
  - Average and p95 chunk send time (WSS/HTTP). 
  - Photo success rate and median send time.
  - Device current draw idle vs. capture (USB inline meter).
- Scenarios:
  - Stable LAN; WAN via ngrok; Wi‑Fi with weak RSSI.
- Success criteria:
  - ≥50% reduction in audio drops under WAN jitter.
  - No regressions in payloads or backend processing.

# Flags & Safety Switches

- All new behavior behind `#define IG_TUNE_*` flags in `config.h` (default off):
  - `IG_TUNE_HTTP_KEEPALIVE`, `IG_TUNE_PREALLOC_AUDIO`, `IG_TUNE_SMALL_AUDIO_CHUNK`,
    `IG_TUNE_WS_BACKOFF`, `IG_TUNE_TX_POWER_ADAPT`, `IG_TUNE_CAMERA_PWDN`, `IG_TUNE_DEBUG_COUNTERS`.
- Single‑commit rollback possible if any regression is observed.

# Risks & Mitigations

- PSRAM fragmentation or pool exhaustion → mitigate by fixed ring sizes and clear on low‑memory.
- TX power reduction harming range → flag‑gated; auto‑disable below RSSI threshold.
- Smaller audio chunks increasing overhead → keep default off; measure before enabling.

# Deliverables

- PR series with small, focused commits for each stage.
- Updates to `docs/ideasglass_bridge.md` with measurements and toggles once each stage is validated.

---

## Implementation status and how to enable

The following Stage A–C items are implemented behind flags in `IdeaGlass/firmware/ideasglass_arduino/config.h` and OFF by default. Enabling them does not change external behavior (protocols/payloads); they only improve robustness and efficiency.

- Stage A
  - `IG_TUNE_HTTP_KEEPALIVE` (0/1): reuse TLS connections for HTTP fallbacks (`/api/v1/audio`, `/api/v1/messages`).
  - `IG_TUNE_BATTERY_FILTER` (0/1): average a few ADC samples, cache ≥30 s to reduce reads.
  - `IG_TUNE_DEBUG_COUNTERS` (0/1): print periodic counters (every 30 s) for ws/http ok/fail and queue drops.

- Stage B
  - `IG_TUNE_PREALLOC_AUDIO` (0/1): preallocate a small pool of PCM buffers to avoid malloc/free churn.
  - `IG_TUNE_QUEUE_DROP_OLDEST` (0/1): on queue full, drop oldest pending and enqueue the newest (reduces burstiness).

- Stage C
  - `IG_TUNE_WS_BACKOFF` (0/1): non‑blocking WS reconnect with exponential backoff + jitter; sender never stalls.

### Recommended initial toggles

Turn these on first in `config.h`, rebuild, and upload:

```c++
#define IG_TUNE_HTTP_KEEPALIVE 1
#define IG_TUNE_BATTERY_FILTER 1
//#define IG_TUNE_DEBUG_COUNTERS 1  // enable temporarily when testing
```

If network jitter causes bursts, add:

```c++
#define IG_TUNE_WS_BACKOFF 1
#define IG_TUNE_PREALLOC_AUDIO 1
#define IG_TUNE_QUEUE_DROP_OLDEST 1
```

### Build & upload (Arduino‑CLI)

```bash
FQBN=esp32:esp32:XIAO_ESP32S3
bin/arduino-cli compile --fqbn $FQBN --board-options PSRAM=opi IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient
bin/arduino-cli upload  -p /dev/ttyACM0 --fqbn $FQBN --board-options PSRAM=opi IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient
```

### Quick verification

- Serial should still show identical functional logs, with fewer stalls under jitter.
- If `IG_TUNE_DEBUG_COUNTERS=1`:
  - `[Stats] ws_audio_ok=… ws_audio_fail=… http_audio_ok=… http_audio_fail=… photo_ok=… photo_fail=… audio_queue_drop=…`
  - Expect `audio_queue_drop` to decline after enabling WS backoff + drop‑oldest.

