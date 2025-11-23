# Omi Friend Firmware Deep Dive

This tutorial-style note aggregates everything learned from `firmware/omi` so you can reason about the hardware interfaces, BLE APIs, build/flash flows, and debugging knobs when extending LightMind firmware or writing companion apps.

## 1. Build & Flash Basics

| Step | Command / File | Notes |
| --- | --- | --- |
| Toolchain | nRF Connect SDK (Zephyr) | Follow `firmware/readme.md` and Nordic docs. Use `west` or nRF Connect VS Code extension. |
| Presets | `firmware/omi/CMakePresets.json` | Defines configs for consumer vs. devkit hardware. Select preset (e.g., `omi-v1`) when configuring. |
| Build | `west build -b seeed_xiao_blesense` with appropriate overlay | `CONFIG_OMI_ENABLE_*` options live in `omi.conf`. |
| Flash (USB) | `west flash --bossac` or nRF Connect | Bootloader enumerates as UF2 when reset twice; drop `zephyr.uf2`. |
| OTA | `firmware/BUILD_AND_OTA_FLASH.md` | Uses MCUboot + MCUmgr over BLE. Requires enabling secure boot flag and building `mcuboot`. |

### Debug / Logging
- `CONFIG_CONSOLE=y`, `CONFIG_LOG=y`, `CONFIG_UART_CONSOLE=y` allow RTT/USB logs (`firmware/devkit` configs show toggles).
- Serial logging conflicts with offline storage; disable `CONFIG_OMI_ENABLE_OFFLINE_STORAGE` when profiling audio throughput.
- USB CDC defined in `devkit/src/usb.c` (guarded by `CONFIG_UART_CONSOLE`).

## 2. Hardware Blocks & Drivers

| Module | File(s) | Key APIs |
| --- | --- | --- |
| **Microphone** | `firmware/omi/src/lib/core/mic.c` | PDM input at 16 kHz, double-buffered (100 ms chunks). Writes PCM into `codec_ring_buf` via `codec_receive_pcm`. Gain adjustable via `mic_set_gain()`. |
| **Codec** | `lib/core/codec.c` + `lib/opus-1.2.1` | Opus encoder configured for 32 kbps restricted low delay. Callback `_callback` feeds bytes to transport. VBR + complexity 3. |
| **Transport (BLE + SD + battery)** | `lib/core/transport.c` | Registers BLE services, manages connection callbacks, handles MTU/PHY updates, writes backlog to SD, broadcasts battery state, schedules data pusher thread. Exposes `transport_on/off`. |
| **Button FSM** | `lib/core/button.c` | GPIO polling at 25 Hz, emits events (press, release, tap variants) over custom characteristic. Uses Zephyr work queue for debouncing. |
| **LED/Haptic** | `led.c`, `haptic.c` | Map `settings_dim_ratio` to PWM, vibrate via BLE triggers. |
| **Battery** | `battery.c` + Zephyr BAS | Reads ADC, converts to %, updates BAS characteristic every 3 s. |
| **SD / Offline Storage** | `sd_card.c`, `storage.c` | Maintains `file_num_array`, writes Opus chunks when BLE idle, streams backlog on next connection (guarded by `CONFIG_OMI_ENABLE_OFFLINE_STORAGE`). |
| **USB (serial & power)** | `devkit/src/usb.c` | Handles USB enable/disable and prevents logs from wedging when USB is absent. |

### Interrupt Pins / GPIO
See `config.h` for pin maps (PDM DIN/CLK/PWR). Buttons defined via devicetree alias `buttons`. LED/H-bridge pins pulled from `DT_NODELABEL` macros.

## 3. BLE Interfaces Recap

- **Audio Service**: `19b1…` (data, codec, optional speaker). Notifications use header `[packetIndexLE16, chunkIndex, payload]`.
- **Settings Service**: dim ratio & mic gain writes.
- **Features Service**: capability bitmask (speaker, accelerometer, battery, offline storage, LED dimming, mic gain).
- **Button Service**: event notifications (press/release/tap/long/double).
- **Battery Service**: standard BAS.
- **Device Info**: manufacturer/model/firmware revision strings from `omi.conf`.

Detailed UUID table is in `references/omi-friend-ble-endpoints.md`.

## 4. Audio Pipeline (Capture → BLE → Offline Storage)

```
PDM mic (16 kHz, mono) → mic.c buffers (1600 samples)
    → codec_ring_buf (16k samples)
    → codec thread (reads 320-sample blocks)
        → Opus encode (<=160 bytes frame)
        → codec callback → transport_write()
            → ring buffer `tx_queue`
            → pusher thread
                → chunk + notify via `bt_gatt_notify`
                → (optional) write_to_storage when BLE unsubscribed
```

Important constants (`lib/core/config.h`):
- `CODEC_PACKAGE_SAMPLES = 320`, `CODEC_OUTPUT_MAX_BYTES = 160`.
- `NETWORK_RING_BUF_SIZE = 32` frames.
- `MINIMAL_PACKET_SIZE = 100` ensures we don’t notify with tiny payloads.

## 5. Offline Playback Logic

When offline storage is enabled:
1. If BLE not connected, `write_to_storage()` packs 80-byte Opus chunks (`MAX_WRITE_SIZE = 440`) to SD card (5 frames per write) with per-file cap `MAX_AUDIO_FILE_SIZE = 300 KB` (`transport.c:784`).
2. `storage.c` keeps `file_num_array` metadata. On next connection, `storage_temp_data` is drained before live streaming resumes (watch `storage_is_on`).
3. Files deleted after streaming to keep space under `MAX_STORAGE_BYTES = 480 MB`.

## 6. Button / Power / Sleep

- Button events trigger both BLE notifications and local actions (power toggles). `check_button_level()` identifies single/double/long taps based on timed windows (300 ms tap, 600 ms double, 1 s long press).
- `button.c` interacts with `mic` (pause/resume recording) and `speaker` (future features).
- Power management uses Zephyr `sys/poweroff.h`; long press may trigger deep sleep depending on build.

## 7. USB & Charging

- `usb.c` ensures console logging doesn’t crash when USB is removed. USB enable is tied to `CONFIG_UART_CONSOLE`.
- Charging/power rails managed by board-specific definitions in `boards/`. BQ25101 charger setpoints stored there.

## 8. OTA & Recovery

- `firmware/BUILD_AND_OTA_FLASH.md` documents building MCUmgr-enabled images, signing, and pushing via BLE.
- Bootloader files live under `bootloader/` and `FLASH_3.0.8/`. For field updates, use the MCUmgr CLI or the companion mobile app (Flutter) to push `.bin` payloads.

## 9. Companion App Hooks

When writing the LightMind iOS app, you now know:
- Which UUIDs to use (audio, settings, buttons, battery).
- How to reassemble Opus frames (`references/lightmind-ble-audio.md`).
- How to send control writes (LED dimming, mic gain) and interpret feature flags.
- That backlog streaming happens automatically; add UX hints for “Syncing older audio…”

## 10. Future Work Checklist

- Swap UUID root (currently Intel sample) to LightMind-owned root per TODO in `transport.c`.
- Harden SMP/passkey flow (maybe quick display on LED). `ble.c` currently logs passkeys but doesn’t show on-device.
- Optimize ring buffer copies (`write_to_tx_queue` double copies). Consider zero-copy notifications.
- Expand speaker downlink (currently stub). Need DSP path opposite of `codec`. 
- Document CLI commands (`firmware/test/README.md`) if using Zephyr shell.

With this file + the BLE endpoint table you can onboard firmware contributors, write client SDKs, or plan OTA/battery/button features without spelunking the entire codebase each time.
