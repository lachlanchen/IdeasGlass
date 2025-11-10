# Release Notes

## 2025-11-10 — Audio WebSocket Stability Rollback

- Restored `IdeasGlassClient` firmware to commit `cd4525e` after the experimental WebSocket rewrite caused repeated connect/close cycles. The rewrite attempted to hand-roll the WebSocket framing pipeline (for better battery bounds), but the low-level `WiFiClientSecure` writes were not 100 % reliable under ngrok latency, so the backend would only see very short-lived `/ws/audio-ingest` sessions and audio fell back to HTTP.
- Original implementation (now reinstated) keeps the socket alive through a simpler, proven code path and was tuned together with the backend when /ws/audio-ingest was first launched. Audio latency returns to normal and photos remain unaffected.
- BLE pairing remains disabled by default so there are no RF conflicts with the audio path.

Next steps:
- Re-attempt WS optimisations only after we have an integration test against the backend and can simulate ngrok-level latency. Any future changes should be hidden behind `#define IG_TUNE_*` flags so the stable codepath stays untouched by default.
