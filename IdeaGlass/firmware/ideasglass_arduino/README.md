# IdeasGlass Arduino Firmware

Reference firmware for the Arduino-friendly IdeasGlass hardware described in `docs/ideasglass_arduino_hardware.md`. It targets the Seeed XIAO ESP32S3 Sense (Arduino core 2.0.17+) and provides:

1. **Multi-sensor telemetry** (IMU, ambient light, battery, buttons, haptics)
2. **BLE service** exposing telemetry + command characteristics compatible with the Flutter app
3. **Wi-Fi/HTTPS uplink** that posts signed JSON payloads to the Tornado ingestion API
4. **Snapshot camera support** using the onboard OV2640

## Directory structure

```
ideasglass_arduino/
├── IdeasGlassFirmware.ino   # Main Arduino sketch
├── config.h                 # Central pin assignments + BLE UUIDs
├── wifi_credentials.h       # (gitignored) user Wi-Fi list
├── WifiTest/                # Standalone Wi-Fi connectivity sketch
└── README.md
```

## Arduino setup

1. Install board support:
   ```bash
   arduino-cli config add board_manager.additional_urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
   arduino-cli core update-index
   arduino-cli core install esp32:esp32@2.0.17
   ```
2. Install required libraries (from Library Manager or `arduino-cli lib install`):
   - `Adafruit BNO08x`
   - `Adafruit Unified Sensor`
   - `Adafruit_DRV2605`
   - `ArduinoJson`
   - `ESP32 BLE Arduino`
3. Copy `wifi_credentials.example.h` to `wifi_credentials.h` and fill in one or more SSIDs + passwords. (If you skip this step, the sketches will fall back to the example file, which you can also edit directly, but keeping a separate `wifi_credentials.h` prevents accidental commits of secrets.)
4. Select the board **Seeed XIAO ESP32S3** (PSRAM enabled) and flash the sketch.

### Wi-Fi test sketch

`WifiTest/WifiTest.ino` is a standalone sketch that only verifies Wi-Fi credentials:

1. Copy `wifi_credentials.example.h` to `wifi_credentials.h` in the **parent** folder (`ideasglass_arduino/`), or edit the example file directly if you prefer (the sketch auto-detects whichever exists).
2. Open `WifiTest/WifiTest.ino` in Arduino IDE – it auto-detects `wifi_credentials.h` or falls back to the example file.
3. Upload to the XIAO ESP32S3 and watch the serial monitor for connection / RSSI logs.

## BLE profile

| Characteristic | UUID | Direction | Notes |
| --- | --- | --- | --- |
| Telemetry | `6E400003-B5A3-F393-E0A9-E50E24DCCA9E` | Notify | Sends JSON frames w/ imu, battery, ambient light, button state |
| Command | `6E400002-B5A3-F393-E0A9-E50E24DCCA9E` | Write | Mobile app sends capture/haptic/tuning commands |
| Photo chunk | `19B10005-E8F2-537E-4F6C-D104768A1214` | Notify | Streams JPEG chunks |

## Tornado uplink contract

Payloads are HTTPS `POST /api/v1/ingest` with header `X-Device-Secret` and body:

```json
{
  "device_id": "ideasglass-001",
  "ts": 1736381153,
  "battery": 86,
  "imu": {"quat":[0.12,-0.02,0.98,0.10],"accel":[0.01,0.00,1.02]},
  "ambient_lux": 146,
  "mic_level": 0.32,
  "photo": {
    "id": "pic-20250108-153755",
    "size": 24312,
    "crc32": 143625123
  }
}
```

The Tornado app stores metadata in Postgres and requests the binary asset via the `/api/v1/upload/{photo_id}` presigned URL exposed in the HTTP response.

## Next steps

- Extend the HAL if you target different Arduino-class boards (Nano ESP32, Nicla Vision, etc.).
- Plug in OTA via `ESP32httpUpdate` once the Tornado server surfaces firmware manifests.
- Tie BLE characteristics to the Flutter app’s new IdeasGlass tab so configuration stays in sync.
