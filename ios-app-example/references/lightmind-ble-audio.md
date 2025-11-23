# LightMind BLE Audio Integration Guide

This note distills how the Seeed XIAO nRF52840–based LightMind/"Omi Friend" firmware streams audio over Bluetooth LE and how an iOS client (e.g., the LightMind SwiftUI app) should connect, pair, and decode packets. The material below is taken from the Zephyr firmware (`firmware/omi`), dev scripts, and the public Omi SDK (`../omi`).

## Hardware & Firmware Overview

- **MCU / radio:** Nordic nRF52840 running Zephyr RTOS and nRF Connect SDK peripherals (`firmware/omi/omi.conf`).
- **Audio front end:** PDM mic sampled at 16 kHz, 16-bit mono. Data flows through `mic.c` → `codec.c` → `transport.c`.
- **Codec:** Opus `OPUS_APPLICATION_RESTRICTED_LOWDELAY`, 32 kbps VBR, complexity 3 (`firmware/omi/src/lib/core/config.h:17-36`, `codec.c:62-105`). Each encoder call consumes 320 PCM samples (20 ms) and produces ≤160 bytes.
- **Transport:** Custom BLE GATT service with notification-only uplink, optional downlink for a speaker, and Zephyr BAS/DIS for battery/device metadata (`transport.c:108-220`).

## Pairing & Re-pairing

| Mode | Details |
| --- | --- |
| Default | Advertising name defaults to `Omi` (`CONFIG_BT_DEVICE_NAME` in `omi.conf:169`). Devkit builds may use `Friend` or `Omi DevKit`. The advertising payload exposes the 128-bit audio service UUID plus the GAP name (`transport.c:202-210`). |
| Security | If the build enables `CONFIG_BT_SMP`, the firmware registers passkey-display callbacks (`firmware/omi/src/lib/evt/ble.c:53-103`). The passkey is printed to the RTT/VS Code console via `LOG_INF`, so pairing requires watching logs. Shipping builds typically disable SMP to allow Just Works pairing. |
| Re-pair | If iOS cached stale keys, open *Settings ▸ Bluetooth ▸ (i) ▸ Forget This Device*, reboot the wearable, and reconnect. When SMP is enabled you must re-read the passkey in the console. |

## GATT Map

| Service | UUID | Characteristics | Properties | Notes |
| --- | --- | --- | --- | --- |
| **Audio Service** | `19b10000-e8f2-537e-4f6c-d104768a1214` | `19b10001…` Audio Data | `READ, NOTIFY` | Notifications carry encoded audio packets, described below. Client must enable CCC on attr[1]. |
|  |  | `19b10002…` Audio Codec ID | `READ` | Returns `0x15` (`21`) for Opus (see `config.h`). Value can be used to branch per codec. |
|  |  | `19b10003…` Speaker (optional) | `WRITE, NOTIFY` | Compiled when `CONFIG_OMI_ENABLE_SPEAKER`; downlink audio via `audio_data_write_handler` → `speak()` (currently stubbed). |
| **Settings Service** | `19b10010…` | `19b10011…` Dim ratio | `READ/WRITE` | UI brightness percentage (0–100). `settings_dim_ratio_*` handlers persist to flash (`transport.c:228-266`). |
|  |  | `19b10012…` Mic gain | `READ/WRITE` | Accepts gain level 0–8 and immediately calls `mic_set_gain()` (`transport.c:268-309`). |
| **Features Service** | `19b10020…` | `19b10021…` Feature bitmap | `READ` | Bitmask defined in `features.h`: bits advertise speaker, IMU, button, offline storage, LED dimming, etc. Useful to conditionally show UI. |
| **Button Service** | `23ba7924-0000-1000-7450-346eac492e92` | `23ba7925-…` Button stream | `READ, NOTIFY` | Payload is two `int32_t` values; `value[0]` is event code (`1` single tap, `2` double tap, `3` long, `4` press, `5` release). Firmware debounces at 25 Hz (`button.c:68-205`). |
| **Battery Service** | `0x180F` (standard BAS) | `0x2A19` level | `READ, NOTIFY` | Zephyr BAS helper polls every 3 s (`transport.c:356-390`). |
| **Device Info Service** | `0x180A` | Various | `READ` | Model (`Omi CV 1`), manufacturer (`Based Hardware`), FW/HW rev strings are set in `omi.conf:162-176`. |

The advertising payload also includes the 16-bit Device Information Service UUID (scan response) so generic BLE scanner apps can discover the device.

## Audio Notification Format

Each notification sent on `19b10001` is prepended with a 3-byte transport header before the Opus payload (`transport.c:654-704`):

| Byte | Meaning |
| --- | --- |
| 0-1 | **Packet index** (`packet_next_index`), uint16 little-endian incrementing per notification. Wraps at 65,535. Use this to detect drops/resets. |
| 2 | **Chunk index** within a single Opus frame. `0` marks the start of a new frame; `1..n` are subsequent chunks when the frame is larger than the negotiated MTU. |
| 3..N | Raw Opus bytes (size = `min(MTU-3, remaining_frame_bytes)`). |

Because frames (≤160 bytes) often exceed the notification payload (MTU-3), you must reassemble chunks until you see the next chunk with `chunkIndex == 0`. A reliable pattern is implemented in `firmware/scripts/devkit/local_client.py`:

```python
index = data[0] | (data[1] << 8)
chunk = data[2]
payload = data[3:]
```

- Keep `pending` bytes for the current frame.
- When `chunk == 0` and `pending` already holds data, emit the previous frame and start a new `pending` buffer.
- If packet index or chunk order skips, drop the partial frame and resync.

Once an Opus frame is complete, decode it with an Opus decoder configured for 16 kHz mono and a 20 ms frame size (320 samples). The Python sample uses `opuslib.Decoder(16000, 1)` and `decode(frame, 320)` (`local_client.py:18-71`). In Swift you can use a libopus binding or AudioToolbox’s `AudioConverter` with Opus support.

### Throughput & Timing

- Encoder produces ~100 frames per second (20 ms windows). The ring buffer (`NETWORK_RING_BUF_SIZE` = 32) can hold ~3 seconds of audio before dropping.
- The firmware immediately requests 2M PHY, maximum data length, and an MTU exchange (`transport.c:402-458`). iOS 16+ automatically honors these requests; you don’t need to manually set MTU but you *can* call `CBPeripheral.setNotifyValue` only after `peripheral(_:didUpdateNotificationStateFor:)` confirms success.
- If the device wasn’t connected, audio was written to SD (when `CONFIG_OMI_ENABLE_OFFLINE_STORAGE` is on). On the next connection the firmware streams backlog files first, then live audio (`transport.c:820-865`). Expect a burst of packets after connecting.

### Downlink Audio (Speaker)

If `CONFIG_OMI_ENABLE_SPEAKER` is enabled, writes to `19b10003…` flow into `audio_data_write_handler` → `speak()`. The handler currently just echoes `len` and calls a stub; treat it as experimental.

## Buttons, Battery, and Settings

- **Button notifications:** `button.c` sends event arrays. The LightMind iOS app can subscribe to `23ba7925…` to drive recording, status LEDs, etc.
- **Mic gain control:** Write 1 byte (`0–8`) to `19b10012…` to boost or attenuate the PDM front end (`transport.c:287-309`). Changes persist to flash via `app_settings_save_mic_gain()`.
- **LED dimming:** Write 0–100 to `19b10011…` to control LED brightness (`transport.c:238-266`).
- **Feature detection:** Read `19b10021…` and mask against `omi_feature_t` bits (`features.h:8-20`) to learn what peripherals are baked into the current firmware.
- **Battery:** Subscribe to the standard BAS characteristic; Zephyr sends updates every ~3 seconds once connected.

## iOS Integration Checklist

1. **Scan** using `CBCentralManager` with no service filter (firmware advertises only its custom UUID) or filter on `19B1…` once discovered. Consider showing RSSI to help the user pick the closest unit.
2. **Connect** and wait for `didConnect`. The firmware auto-negotiates PHY/data length/MTU, but you can still request `peripheral.readRSSI()` or `discoverServices` once `didDiscoverServices` fires.
3. **Discover GATT**: look for service `19b10000…`, then characteristics `…01`, `…02`, optionally `…03`. Also discover the button service and BAS if you need them.
4. **Pairing**: if the OS prompts for a PIN, open the RTT/VS Code console to view the 6-digit passkey emitted from `auth_passkey_display()` (`ble.c:63-78`). For a clean re-pair, forget the bonding in both iOS settings and `bt_unpair_all()` (hold the hardware button while powering on, or flash firmware) – bonding caches in flash.
5. **Enable notifications** on `…01` (audio) and optionally `23ba7925…` (buttons) and `2A19` (battery). Wait for the CCC write to succeed before assuming data will flow.
6. **Read codec** (`…02`). If the value is `21`, set up an Opus decoder at 16 kHz mono, 20 ms frames, 32 kbps VBR. The codec ID may change in future firmware, so keep a lookup table.
7. **Reassemble audio frames** as described above. Track packet indices to skip duplicates and recover from drops.
8. **Decode** using libopus (C), opusfile, or a native Swift wrapper. Output PCM16, feed it to `AVAudioEngine` or your transcription SDK.
9. **Handle backlog**: on initial connection you may receive a flood of historical frames. You can detect the switchover when packet indices reset or when the device finishes deleting SD segments (watch for fewer notifications). If you only want live audio, discard frames until `file_num_array` drains or wait a fixed grace period (~1–2 s) before feeding your pipeline.
10. **Mic gain / LED dimming**: expose optional UI to write to the settings characteristics for user control.

## Reference Scripts & SDKs

- `firmware/scripts/devkit/local_client.py` – Minimal Bleak client showing packet parsing and Opus decode, saving WAV files.
- `../omi/sdks/react-native` – React Native implementation (see `src/OmiConnection.ts`) that negotiates connections, sets MTU to 512 on Android, and exposes JS hooks for audio, buttons, and battery.
- `../omi/app/lib/services/devices` – Flutter code used by the production app, useful for real-world reconnection/backoff logic.

## Appendix: Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| **App icon didn’t change** | iOS cached the old bundle | Delete the app from the device and reinstall; ensure `AppIcon.appiconset` only contains the new `lightmind_icon_*` files. |
| **BLE notifications stop after a few seconds** | CCC not enabled or MTU too small | Verify you call `setNotifyValue(true)` and wait for success. iOS sets MTU automatically; on Android call `requestMtu(247)` and `requestConnectionPriority(CONNECTION_PRIORITY_HIGH)`. |
| **Audio frames corrupt / Opus decode errors** | Dropped notification or incorrect reassembly | Use packet index + chunk index to detect gaps. Reset your accumulator when a gap occurs. |
| **Pairing fails** | SMP enabled but no one reads the passkey | Connect over USB/RTT to read logs or disable `CONFIG_BT_SMP` in `omi.conf`. |
| **No audio until several seconds after connect** | Offline storage replaying backlog | Let the flush finish or disable offline storage (`CONFIG_OMI_ENABLE_OFFLINE_STORAGE=n`). |

With this map you can finish the LightMind iOS audio client: scan, connect, subscribe, reassemble, decode, and control device settings/mic gain safely.
