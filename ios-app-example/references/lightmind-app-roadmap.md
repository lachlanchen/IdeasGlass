# LightMind iOS Companion Roadmap

This plan outlines how to evolve the current LightMind SwiftUI prototype into a feature-complete experience on par with the shipping Omi iOS app. It stitches together the existing firmware capabilities (see `references/omi-firmware-overview.md`) with the app features needed for recording, syncing, transcription, and analytics.

## Phase 0 – Foundations (Done / In progress)
- ✅ SwiftUI shell with CoreBluetooth scanner (`BLEManager.swift`).
- ✅ App + in-app branding aligned with LightMind design system.
- ⬜️ Document BLE protocol (see `lightmind-ble-audio.md`, `omi-friend-ble-endpoints.md`).

## Phase 1 – BLE Feature Parity
1. **Connection lifecycle**
   - Add background reconnect logic (cache `CBPeripheral` identifiers in Keychain, attempt `connect` when app resumes).
   - Surface passkey pairing UX if firmware prints codes (tie into `peripheral:didRequestMTU`).
2. **Audio subscription**
   - Implement chunk reassembly + Opus decode in Swift (bridge libopus or use `AudioConverter`).
   - Provide live waveform / VU meter and optional transcription hook (e.g., Deepgram SDK).
3. **Settings + controls**
   - Mic gain slider → write to `19b10012…`.
   - LED brightness slider → write to `19b10011…`.
   - Feature detection to enable/disable UI based on `19b10021…` bitmask.
4. **Button & battery listeners**
   - Subscribe to `23ba7925…` for tap/press events, mapping to app actions (start/stop recording, favorites, etc.).
   - Subscribe to BAS (`0x2A19`) for persistent battery card.

## Phase 2 – Offline Storage & Sync
1. **Backlog awareness**
   - Detect when firmware is flushing SD backlog (monitor sustained notifications + `storage_is_on`). Show “Syncing offline audio…” banner.
   - Give the user a toggle to skip backlog playback (write a control flag via new characteristic if needed).
2. **Local caching**
   - Write decoded PCM/Opus chunks to `FileManager` with metadata (timestamp, packet ids). Use Core Data / SQLite for indexes.
   - Provide manual delete/resync controls.
3. **Server sync**
   - Mirror Omi’s pipeline: upload audio chunks to backend (S3) + webhook to processing service (Deepgram/Whisper). 
   - Maintain job status in the app; show when transcription completes.

## Phase 3 – Cloud Processing & Insights
1. **Transcription workflow**
   - Integrate chosen STT service (Deepgram, Whisper, Speechmatics) with retry + cost tracking.
   - Attach transcripts back to sessions, surface search/keywords UI.
2. **Analytics**
   - Build timeline view: raw waveform, transcript, tags (button events, manual highlights).
   - Add summary generation (LLM) and snippet export.
3. **Notifications**
   - Push local + remote notifications when new transcription/analysis arrives.

## Phase 4 – OTA & Device Management
1. **Firmware update flow**
   - Integrate MCUmgr BLE transport in-app, reuse `BUILD_AND_OTA_FLASH.md` instructions.
   - Add version check vs. backend.
2. **Device settings**
   - Manage multiple wearables: rename, forget, view feature matrix.
   - Expose advanced controls (speaker enable, LED patterns, offline storage toggle).
3. **Diagnostics**
   - Live log streaming over NUS shell (Zephyr `shell_bt_nus`).
   - Upload crash logs / telemetry to backend.

## Dependencies / Open Questions
- **Opus decoding on iOS**: need to embed libopus (C) or use AudioToolbox once Apple adds Opus decode API.
- **Backend alignment**: confirm server API for audio upload/transcription; reference Flutter app for existing endpoints.
- **Security**: Decide on bonding requirements for production (pairing passkey vs. Just Works). Update firmware accordingly.
- **Offline storage control**: Firmware currently auto-flushes; consider adding a characteristic to pause/resume streaming backlog.

## Milestones
| Milestone | Goals |
| --- | --- |
| M1 – BLE MVP | Connect, monitor battery, view feature flags, send mic gain/LED controls, decode live audio. |
| M2 – Sync | Detect offline backlog, store audio locally, upload to backend, show sync progress. |
| M3 – Transcribe | STT integration, transcript UI, search. |
| M4 – Analytics/OTA | Insights UI, OTA updates, multi-device management, diagnostics. |

Use this roadmap to break Sprint tickets and ensure firmware + app changes stay aligned.
