# Omi Friend / LightMind BLE Endpoints

This cheat sheet lists every Bluetooth LE service and characteristic exposed by the Seeed XIAO nRF52840–based Omi Friend (LightMind) firmware (`firmware/omi`). Use it alongside `references/lightmind-ble-audio.md` for packet formats and client-side guidance.

## Custom Services

### 1. Audio Service (`19b10000-e8f2-537e-4f6c-d104768a1214`)
| Characteristic | UUID | Properties | Purpose |
| --- | --- | --- | --- |
| Audio Data | `19b10001-e8f2-537e-4f6c-d104768a1214` | `READ`, `NOTIFY` | Primary uplink. Notifications carry 3-byte transport header + Opus frame chunk. Read returns the most recent chunk. Client must enable CCC. |
| Audio Codec | `19b10002-e8f2-537e-4f6c-d104768a1214` | `READ` | Returns codec ID (current firmware: `0x15` = Opus 16 kHz mono @ 32 kbps). |
| Speaker (optional) | `19b10003-e8f2-537e-4f6c-d104768a1214` | `WRITE`, `NOTIFY` | Downlink audio path when `CONFIG_OMI_ENABLE_SPEAKER` is set. Writes feed `audio_data_write_handler`/`speak()`. |

### 2. Settings Service (`19b10010-e8f2-537e-4f6c-d104768a1214`)
| Characteristic | UUID | Properties | Notes |
| --- | --- | --- | --- |
| LED Dim Ratio | `19b10011-e8f2-537e-4f6c-d104768a1214` | `READ/WRITE` (1 byte, 0–100) | Controls LED PWM brightness, persisted via `app_settings_save_dim_ratio()`. |
| Mic Gain | `19b10012-e8f2-537e-4f6c-d104768a1214` | `READ/WRITE` (1 byte, 0–8) | Adjusts PDM front-end gain and saves to flash. |

### 3. Features Service (`19b10020-e8f2-537e-4f6c-d104768a1214`)
| Characteristic | UUID | Properties | Notes |
| --- | --- | --- | --- |
| Feature Bitmap | `19b10021-e8f2-537e-4f6c-d104768a1214` | `READ` (uint32) | Bitmask defined in `features.h`: speaker, IMU, button, battery, USB, haptic, offline storage, LED dimming, mic gain. Enables capability-driven UI. |

### 4. Button Service (`23ba7924-0000-1000-7450-346eac492e92`)
| Characteristic | UUID | Properties | Payload |
| --- | --- | --- | --- |
| Button Events | `23ba7925-0000-1000-7450-346eac492e92` | `READ`, `NOTIFY` | Two `int32` values. `value[0]` is event code (1 single tap, 2 double tap, 3 long press, 4 press, 5 release). Notifications fire at up to 25 Hz. |

## Standard Services

| Service | UUID | Characteristic(s) | Notes |
| --- | --- | --- | --- |
| Battery Service (BAS) | `0x180F` | Battery Level `0x2A19` (`READ/NOTIFY`) | Zephyr BAS helper pushes % every 3 seconds once connected (`transport.c`). |
| Device Information Service (DIS) | `0x180A` | Manufacturer, Model, FW/HW rev, PnP | Strings configured via `omi.conf` (`Omi CV 1`, `Based Hardware`, etc.). |

## Advertising / GAP

- Device name defaults to `Omi` (shipping) or `Friend` (devkits). Set via `CONFIG_BT_DEVICE_NAME` in the relevant `.conf` file.
- Advertising payload: Flags + custom audio service UUID + complete local name. Scan response adds DIS UUID (`transport.c:202-216`).

## Connection Behavior

- Firmware auto-requests 2M PHY, maximum data length (251 bytes), and an MTU exchange after connect (`transport.c:402-458`). No app-side MTU tweaks are needed on iOS; Android should call `requestMtu(247)` for parity.
- Battery and button services register after Bluetooth stack startup (`button.c`, `transport.c:980-1008`). If you don’t see them, ensure the build enables the corresponding Kconfig flags.
- Offline storage (`CONFIG_OMI_ENABLE_OFFLINE_STORAGE`) streams backlog data over the same audio characteristic before switching to live frames. Expect packet bursts right after subscribing.

## Characteristic Permissions Cheat Sheet

| Characteristic | CCC Required? | Secured? |
| --- | --- | --- |
| Audio Data | Yes (`audio_ccc_config_changed_handler`) | No extra security—Just Works unless `CONFIG_BT_SMP` is enabled. |
| Audio Codec | No | `READ` only. |
| Speaker | No (downlink) | `WRITE` allowed when speaker build flag is on. |
| Mic Gain / LED Dim | No | Both allow unauthenticated `READ/WRITE`. |
| Button Events | Yes | Notifies only when subscribed. |
| Battery Level | Yes | Standard BAS CCC. |

## Pairing & Bonding Hooks

- If `CONFIG_BT_SMP=y`, the firmware registers passkey display + pairing callbacks (`omi/src/lib/evt/ble.c`). Passkey prints via RTT. Otherwise it pairs with Just Works.
- Re-pair by clearing bonds in iOS (Forget Device) and rebooting the wearable. Firmware clears `current_conn` on disconnect and re-advertises automatically.

## Quick Reference (Copy/Paste)

```text
Service: 19b10000-e8f2-537e-4f6c-d104768a1214
  - 19b10001… Audio Data (notify)
  - 19b10002… Audio Codec (read)
  - 19b10003… Speaker (write/notify, optional)
Service: 19b10010… Settings
  - 19b10011… LED Dim Ratio (r/w)
  - 19b10012… Mic Gain (r/w)
Service: 19b10020… Features
  - 19b10021… Feature Bitmap (read)
Service: 23ba7924… Button
  - 23ba7925… Button Events (notify)
Standard BAS/DIS also enabled.
```

Use this document whenever you need to wire up a new BLE client (Swift, React Native, etc.) or validate that the firmware is exposing the expected endpoints.
