# Omi DevKit 2 ↔ iOS Dataflow (Deep Dive)

This document explains, end to end, how the Omi DevKit 2 firmware communicates with the iOS app: how live audio is streamed, how offline audio is buffered to SD when Bluetooth is unavailable, how that offline audio is synced to the phone, and when files are deleted on the device. It is based on the DevKit v2 Kconfig (`OmiReference/omi/firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf`) and the core transport/storage sources under `OmiReference/omi/firmware/omi/src/lib/core/`.

## BLE Profile (what the iOS app sees)

- Device name: `Omi DevKit 2` (CONFIG_BT_DEVICE_NAME)
- Services:
  - Audio service `19b10000-e8f2-537e-4f6c-d104768a1214`
    - `19b10001…` Audio Data (READ/NOTIFY) – live stream
    - `19b10002…` Audio Codec (READ) – codec ID
    - `19b10003…` Speaker (optional, WRITE/NOTIFY) – downlink audio
  - Settings service `19b10010…`
    - `19b10011…` LED dim ratio (READ/WRITE, 0–100)
    - `19b10012…` Mic gain (READ/WRITE, 0–8)
  - Features service `19b10020…`
    - `19b10021…` feature bitmap (READ)
  - Button service `23ba7924…`
    - `23ba7925…` button events (READ/NOTIFY)
  - Battery service (BAS) `0x180F` → level `0x2A19` (READ/NOTIFY)
  - Device Info (DIS) `0x180A` (READ) – model/manuf/FW/HW
  - Storage service (DevKit/offline) `30295780-4301-EABD-2904-2849ADFEAE43`
    - `30295781…` storage write/notify (client writes commands, device notifies status and data)
    - `30295782…` storage read/notify (client reads file sizes; can also subscribe)

DevKit v2 negotiates optimal link settings automatically after connect: 2M PHY, maximum data length, and an MTU exchange.

## Live Audio Streaming

- Firmware stack: PDM mic (16 kHz mono) → `codec.c` (Opus encoder) → `transport.c` ring buffer → `push_to_gatt()` notifications.
- Notification payload on `19b10001…` has a 3‑byte transport header (see `transport.c`):
  - Byte 0–1: packet index (uint16 LE, increments per notification)
  - Byte 2: chunk index within a single frame (`0` = first chunk; `1..n` subsequent chunks)
  - Byte 3..N: codec bytes
- Reassembly on iOS:
  - Start a new accumulator when `chunk == 0`. If you already have bytes, emit the previous frame first.
  - Append subsequent chunks until you see another `chunk == 0`, then decode the completed frame.
- Codec:
  - DevKit v2 Kconfig sets `CONFIG_OMI_CODEC_OPUS=y`. `Audio Codec` characteristic reports the codec id (21 for Opus). Some builds may report 20 (PCM8) or 0 (PCM16) for test streams.

## Offline Storage (no Bluetooth)

When not connected or not subscribed to audio notifications, the firmware writes encoded audio to the SD card (see `transport.c` / `storage.c`).

- Enabled by `CONFIG_OMI_ENABLE_OFFLINE_STORAGE=y`.
- Packets are batched and written in 440‑byte chunks (`MAX_WRITE_SIZE`, see `transport.c` around `write_to_storage`).
- Files rotate with a max size (`MAX_AUDIO_FILE_SIZE = 300000` bytes). A directory cap is enforced via `MAX_STORAGE_BYTES = 0x1E000000` (480 MB).
- The `file_num_array[]` metadata tracks current file sizes and counts.

## Syncing Offline Audio to iOS (Storage Service)

DevKit v2 exposes a separate storage GATT service with a simple command protocol (see `storage.c`). This is how the phone requests a download and cleans up files.

- UUIDs:
  - Service: `30295780-4301-EABD-2904-2849ADFEAE43`
  - Write/Notify: `30295781-4301-EABD-2904-2849ADFEAE43`
  - Read/Notify:  `30295782-4301-EABD-2904-2849ADFEAE43`

- Read sizes/counts (`storage_read_characteristic`):
  - Reading `…82` returns two little‑endian `uint32_t` values (first two entries from `file_num_array`), used to know how many files and their sizes.

- Commands (write 2 or 6 bytes to `…81`):
  - `READ (0x00)` + `file_num` + `size (4 bytes, optional)`: start a transfer. The device sets `offset` to `size` rounded down to the nearest 440 and begins notifying file data on the same characteristic.
  - `DELETE (0x01)` + `file_num`: delete a file when finished; device responds with result 200.
  - `NUKE (0x02)` + `file_num`: delete entire directory (dev feature).
  - `STOP (0x03)` + `file_num`: stop current transfer; device saves `offset` to flash so you can resume later.
  - `HEARTBEAT (0x32 / 50)` + `file_num`: keep the transfer alive; device resets its inactivity counter.

- Transfer format for storage data:
  - The device emits raw bytes in 440‑byte chunks (no 3‑byte header) via notifications on `…81`. The app should append in order until a single‑byte stop code `100` arrives, indicating completion of one file.
  - You can subscribe to `…81` CCC to receive the stream and status codes.

- Typical app flow:
  1. Discover storage service. Read `…82` to get file counts/sizes (or subscribe to `…82` for updates).
  2. For each `file_num` (1..count): write `READ` with `size = 0` to download from beginning (or resume from a known offset).
  3. Collect `…81` notifications into a local file until you see stop code `100`.
  4. Verify the received size equals the reported size, then write `DELETE` for that `file_num`. Wait for 200 ack.
  5. Loop to next file.

- Notes:
  - The firmware tracks `remaining_length` and will push the next chunk on each iteration of `storage_write()` (kthread). If the connection drops, it saves the `offset` and you can resume later.
  - You may periodically send `HEARTBEAT` to keep the transfer alive through mobile OS power constraints.

## Live vs Offline: Which path wins?

- If you are subscribed to the audio service notifications (`19b10001…`), the live stream takes priority (`valid == true` in `transport.c`), and the SD write thread is idle.
- If you are not subscribed or not connected, the storage writer batches frames to SD.
- The storage reader is only activated upon commands written to the storage service.

## Deletion & Cleanup

- The app controls deletion explicitly via `DELETE` (0x01) to avoid losing data mid‑transfer.
- The device acknowledges deletes with a single‑byte result 200 and updates `file_num_array`.
- A hard reset command `NUKE` removes all files (dev/test only).

## iOS App Checklist

1. Connect & discover services: Audio (`19b1…`), Storage (`3029…`), BAS, Button, Settings.
2. Read Audio Codec (`…02`), log id: 21 = Opus, 20 = PCM8, 0 = PCM16.
3. Live mode: subscribe to `…01` (audio) and reassemble per 3‑byte header. Decode Opus on-device or forward to backend.
4. Offline sync mode:
   - Read `…82` (file counts/sizes).
   - For each file: WRITE `READ` (file_num, size=0), collect 440B chunks from `…81` notifications until stop code 100.
   - Verify size, WRITE `DELETE` (file_num) and wait for 200.
5. Button / Battery:
   - Subscribe to `23ba7925…` for tap/press/long events.
   - Subscribe to BAS `2A19`. Zephyr emits ~every 3 s after connect.
6. Settings:
   - Optional UI to write LED dim (0–100) and Mic gain (0–8).
7. Link health:
   - Let the firmware negotiate 2M PHY and data length; avoid manual MTU hacks on iOS.
   - If streaming stalls, consider sending storage `HEARTBEAT` during long transfers.

## Practical Tips

- For Opus playback on iOS, embed libopus and decode each reassembled frame; output PCM16 at 16 kHz mono.
- Avoid driving CoreAudio directly from every BLE callback; buffer frames and schedule playback in a steady cadence to prevent HAL overloads.
- Use the storage service when you need guaranteed delivery of long recordings; the live audio path is optimized for low‑latency streaming.
- Firmware toggles like `CONFIG_CONSOLE`, `CONFIG_LOG`, and `CONFIG_UART_CONSOLE` materially affect throughput; keep them off on DevKit 2 unless debugging.

With these details, you can implement both low‑latency live audio and robust offline sync between Omi DevKit 2 and the LightMind iOS app.
