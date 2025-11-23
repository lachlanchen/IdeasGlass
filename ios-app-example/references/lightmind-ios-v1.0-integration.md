# LightMind iOS v1.0 — Implementation Notes

This document records what we changed to make DevKit2 audio work end‑to‑end on iOS: BLE scanning/connection, Opus decoding, live waveform, 60‑second recording segments, and playback. Use it as a playbook for future features and debugging.

## Summary

- Firmware reports `Codec ID: 20` (Opus 16 kHz). We integrated an Opus decoder and routed decoded PCM16 to playback, live waveform, and recording.
- Live waveform renders the last ~2 seconds of decoded PCM using RMS bars with percentile normalization.
- Recording rotates by time (60 s) at 16 kHz mono PCM16 and plays back reliably (AVAudioSession set to `.playback`).

## BLE and Audio Data Path

- Discover and subscribe
  - Audio service `19B10000-E8F2-537E-4F6C-D104768A1214` (notify + codec read)
  - Battery `0x180F/0x2A19` (read/notify)
  - Button events `23BA7924…/…25` (notify)
  - iOS file: `apps/ios/LightMind/LightMindApp/BLEManager.swift`

- Packet framing (from firmware `transport.c`)
  - Each notification payload has a 3‑byte header: `[0..1]=uint16LE packet id, [2]=chunk index`, followed by payload bytes.
  - Reassemble per frame by concatenating chunks until the next `index==0` header.

- Codec mapping (fixed)
  - 0 → PCM16 (16 kHz)
  - 20 → Opus (16 kHz) on DevKit2
  - 21 → reserved/unused
  - iOS now treats 20 as Opus (was previously misinterpreted as PCM8).

## Opus Decoding on iOS

- Package: `https://github.com/alta/swift-opus.git` (SPM)
  - Added to the project and linked to the `LightMind` target.
  - Resolve packages once; Xcode caches thereafter.

- Bridge wrapper
  - File: `apps/ios/LightMind/LightMindApp/OpusDecodeBridge.swift`
  - Wraps `Opus.Decoder` to return PCM16 `Data` for each Opus frame.

- BLE pipeline changes
  - `BLEManager.swift`: when codec==20, decode frames on a background queue and:
    - Schedule to `AudioStreamManager` if Live playback is on
    - Append to recorder (for 60 s segments)
    - Update the live waveform buffer

- Audio session
  - File: `apps/ios/LightMind/LightMindApp/LightMindApp.swift`
  - Set `AVAudioSession` to `.playback` (with `.mixWithOthers`) and activate on launch.

## Live Waveform

- Data source
  - Keep a small rolling PCM buffer (~2 seconds) of decoded audio; downsample to ~200 bars.
  - `BLEManager.swift` maintains `liveWaveform` via `WaveformExtractor.fromPCM16LE`.

- Renderer
  - File: `apps/ios/LightMind/LightMindApp/WaveformView.swift`
  - Uses SwiftUI `Canvas` to draw RMS bars with a 95th‑percentile normalization to avoid “solid green” on outliers.

- UI
  - File: `apps/ios/LightMind/LightMindApp/ContentView.swift`
  - “Live Waveform” section shows bars when data exists.

## Recording and Playback

- 60‑second rotation (fix for earlier ~30 s rotation)
  - File: `apps/ios/LightMind/LightMindApp/AudioRecorder.swift`
  - Rotate by time: bytes per second = `sampleRate * channels * 2`. New segment every 60 s.

- Segment detail page
  - File: `apps/ios/LightMind/LightMindApp/SegmentDetailView.swift`
  - Displays waveform + Play/Pause with a progress slider. Converts PCM to `.wav` (via `AudioWAVExporter.swift`) for robust `AVAudioPlayer` playback.

- Playback engine
  - File: `apps/ios/LightMind/LightMindApp/AudioStreamManager.swift`
  - `AVAudioEngine + AVAudioPlayerNode` schedules decoded PCM; supports automatic format conversion.

## Diagnostics & UX

- Activity Log
  - Logs connection stages, codec, battery, button events, “live playback disabled” reminders, and playback diagnostics.
  - Copy Log button produces a timestamped text dump.

- Clear Segments
  - Removes older or mis‑saved (pre‑fix) files in one tap.

## Common Errors & Fixes

- “received audio frame before codec negotiated”
  - Frames arriving before codec read. Fix: buffer until codec known; log once.

- CoreAudio mismatch (e.g., `_outputFormat.channelCount == buffer.format.channelCount`)
  - Solved by using the engine’s mixer format and automatic channel conversion.

- Simulator Metal warnings (`default.metallib` / `RenderBox.framework`)
  - Benign. Caused by Canvas; BLE doesn’t work on simulator anyway. Test on device.

- Short segments (~7.5 s) when playing “1 min” files
  - Root cause: treating Opus bytes as PCM pre‑fix. Resolved by proper Opus decode; added Clear Segments.

## Performance Notes

- Decoding on a background queue to keep the main/UI thread responsive.
- For even smoother low‑latency playback, consider:
  - Batch scheduling ~40–60 ms buffers to `AVAudioPlayerNode`.
  - Set preferred I/O buffer duration to ~5–10 ms (trade CPU for latency).
  - Add an oscilloscope‑style “scrolling line” scope for lighter drawing.

## How to Build/Run (device)

1. Open `apps/ios/LightMind/LightMind.xcodeproj` in Xcode.
2. Ensure the Opus package resolves (Xcode handles this automatically now).
3. Select an iPhone device and Run.
4. In the app: Scan → Connect → Toggle Live playback → Observe live waveform and segments.

## Release

- Changelog: `CHANGELOG.md`
- Tagged: `v1.0`

## Next Steps

- Storage Service (offline SD sync): implement read/delete workflow for UUID `30295780…` with progress UI.
- Live scope variant (oscilloscope). Optional small ring buffer and `AVAudioConverter` for uniform scheduling.
- Opus quality presets and CPU/latency profile toggles.

