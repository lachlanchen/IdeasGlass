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
├── IdeasGlassClient/   # HTTPS client demo posting to backend
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
4. Select the board **Seeed XIAO ESP32S3** and flash the sketch.

### Power UX (long‑press)

- Hold the button ~0.8s at power‑on to boot. If not held, the device enters deep sleep and waits for the next hold.
- While running, hold ~2.5s to enter deep sleep. A short press still triggers a capture.

Timings can be tuned in `config.h`:

```
constexpr uint32_t LONG_PRESS_BOOT_MS = 800;   // hold on boot to start
constexpr uint32_t LONG_PRESS_OFF_MS  = 2500;  // hold during run to sleep
```

### Build & Upload (Arduino IDE)

1. Board: Tools → Board → ESP32 → XIAO_ESP32S3
2. PSRAM: Tools → PSRAM → OPI PSRAM (required for camera)
3. Partition: Tools → Partition Scheme → Default with spiffs (3MB APP/1.5MB SPIFFS)
   - Or choose “Maximum APP (7.9MB No OTA/No FS)” if you don’t need a filesystem.
4. Port: select your serial device (e.g., `/dev/ttyACM0` on Linux)
5. Upload

If the serial port is missing or permission‑denied on Linux:
- Add your user to `dialout` and re‑login: `sudo usermod -aG dialout $USER`
- Or temporarily: `sudo chmod a+rw /dev/ttyACM0`

If the port is busy: close any serial monitor, or `fuser -k /dev/ttyACM0`

### Build & Upload (Arduino CLI)

The repo includes a local CLI binary at `bin/arduino-cli`. You can also install your own.

1) Install board core + libs (first time)

```
bin/arduino-cli core update-index
bin/arduino-cli core install esp32:esp32
bin/arduino-cli lib install "ArduinoJson" "Adafruit BNO08x" "Adafruit BusIO" "Adafruit Unified Sensor" "Adafruit VEML7700 Library" "Adafruit DRV2605 Library"
```

2) Compile (XIAO_ESP32S3 + PSRAM OPI + default 8MB partitions)

```
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
```

3) Upload (adjust port as needed)

```
PORT=/dev/ttyACM0
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

Notes
- XIAO ESP32S3 valid PSRAM options are `PSRAM=opi` or `PSRAM=disabled`. Use `opi` for the Sense camera.
- Valid partition schemes include `default_8MB` and `max_app_8MB` (no FS). `huge_app` is not defined for this board.
- If upload fails with “port busy”, free it: `fuser -k /dev/ttyACM0` and retry.
- If you prefer the full firmware instead of the HTTPS client demo, open or point the CLI to `IdeasGlassFirmware.ino` and use the same board options.

## Controls & Indicators

On the Seeed XIAO ESP32S3 Sense we use the single on‑board button and status LED:

- Button (GPIO1, `PIN_BUTTON`):
  - Hold ~0.8s at power‑on to boot the device.
  - Hold ~2.5s while running to enter deep sleep.
  - Short press while running triggers an immediate photo capture in the full firmware.
  - Electrical: internal pull‑up; active‑low; RTC‑capable so it can wake from deep sleep via EXT0.
- Status LED (GPIO21, `PIN_STATUS_LED`):
  - Active‑low (LOW = on, HIGH = off).
  - Fast blink during the boot‑hold window; triple‑blink on stop/sleep.

Haptics (optional)
- DRV2605 on I²C signals; `PIN_HAPTIC_INT = GPIO6` for the device interrupt (optional), configured in code.

## Pin Map (quick reference)

These are the key interfaces used by the firmware (see `config.h` for the authoritative mapping):

- Camera (OV2640 on Sense):
  - XCLK GPIO10, PCLK GPIO13, VSYNC GPIO38, HREF GPIO47
  - D0..D7 ⇒ GPIO15,17,18,16,14,12,11,48 (see `IdeasGlass*` sketches)
  - SCCB (I²C to camera): SDA GPIO40, SCL GPIO39
- Microphone (PDM on Sense): CLK GPIO42, DATA GPIO41
- I²C bus (shared): SDA GPIO41, SCL GPIO40 (camera SCCB and DRV2605 can coexist)
- Battery ADC: GPIO2 via voltage divider (see `kVoltageDividerRatio`)
- Button: GPIO1 (active‑low, RTC wake)
- Status LED: GPIO21 (active‑low)
- Haptic INT (optional): GPIO6

Spare IO considerations
- Many pins are occupied by camera and PDM mic on the Sense board. If you add external buttons/LEDs, prefer unused pads on an expansion base (e.g., XIAO ESP32S3 Plus Base) and avoid camera/mic pins.
- For wake‑from‑sleep via button, ensure the button uses an RTC‑capable GPIO and EXT0/EXT1 is configured appropriately.

See also
- Seeed Studio XIAO ESP32S3 (Sense) docs and schematics under `seeed_studio_xiao_esp32s3_dev/`
- BasedHardware OmiGlass firmware wiring (reference): `OmiGlassReference/omiGlass/firmware/ideasglass_arduino/`

### Wi-Fi test sketch

`WifiTest/WifiTest.ino` is a standalone sketch that only verifies Wi-Fi credentials:

1. Copy `wifi_credentials.example.h` to `wifi_credentials.h` in the **parent** folder (`ideasglass_arduino/`), or edit the example file directly if you prefer (the sketch auto-detects whichever exists).
2. Open `WifiTest/WifiTest.ino` in Arduino IDE – it auto-detects `wifi_credentials.h` or falls back to the example file.
3. Upload to the XIAO ESP32S3 and watch the serial monitor for connection / RSSI logs.

### HTTPS client + Photo capture

`IdeasGlassClient/IdeasGlassClient.ino` demonstrates how to:

1. Load Wi-Fi credentials from `wifi_credentials.h`
2. Initialize the XIAO ESP32S3 Sense camera, capture a QVGA JPEG, encode it in Base64 (guarded by `#define ENABLE_PHOTO_CAPTURE 1`)
3. Sample the onboard I²S microphone at 16 kHz, compute an RMS value, and post 256 ms PCM blocks to `https://ideas.lazying.art/api/v1/audio`
4. Trust the LetsEncrypt certificate for `ideas.lazying.art` (embedded in the sketch) for both message + audio requests

Update `kServerHost`, `kServerPort`, and `kDeviceId` if you expose the backend on a different hostname/port. Photos are sent every ~30 seconds by default.

> **Camera note:** In Arduino IDE ensure `Tools → PSRAM → Enabled` before flashing the XIAO ESP32S3 Sense. The sketch automatically falls back to a smaller frame size (QQVGA) if PSRAM is exhausted, and `set_vflip`/`set_hmirror` keep the photo orientation correct without backend processing.

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
