---
title: IdeasGlass Arduino Hardware Blueprint
description: Reference design that adapts the OmiGlass object to an Arduino-friendly wearable stack.
---

# Overview

This blueprint reuses the ergonomics documented in `omiGlass/hardware/` but swaps in an Arduino-centric electronics stack that can be assembled, debugged, and manufactured with readily available modules. The goal is to create a **thin temples + bridge** assembly that houses:

- Imaging + inertial sensing for idea capture and head-tracking
- Low-power BLE/Wi-Fi connectivity for phone + cloud sync
- Battery telemetry, haptics, and a tactile control surface
- Expansion headroom for future biosignal or interaction modules

# Core modules

| Function | Recommended part | Rationale |
| --- | --- | --- |
| Compute + connectivity | **Seeed Studio XIAO ESP32-S3 Sense** (Arduino-compatible) | ESP32-S3 dual-core with BLE/Wi-Fi, 8 MB PSRAM, integrated OV2640 connector; natively supported by Arduino IDE. |
| Vision | **OV2640 camera module** (bundled with the XIAO Sense) | Matches existing `esp_camera` driver and enclosure optics; 640×480 MJPEG meets low-latency needs. |
| IMU | **BNO085 (BNO080/BNO086)** on Qwiic/STEMMA breakout | Fused orientation & activity classification accessible via I²C @ 3.3 V. |
| Ambient light / RGB | **LTR-303 or VEML7700** I²C sensor | Provides exposure data for camera tuning and scene understanding. |
| Microphone | **ICS-43434** (or SPH0645 I²S MEMS mic) | Beam toward the wearer’s mouth; pairs with ESP32 I²S peripheral for audio journaling. |
| Touch/Haptic | **DRV2605L** haptic driver + coin ERM | Enables quiet confirmations w/out LEDs. |
| Battery | Dual **250–300 mAh LiPo** cells with protection + JST 1.25 mm connectors | Mirrors weight distribution from the original design while fitting inside each temple. |
| Power management | **XIAO battery PMIC** + **INA219** inline current monitor (optional) | Built-in charger handles USB-C; INA219 feeds accurate telemetry if needed. |
| User controls | Custom pogo button on GPIO1 + RGB LED on GPIO21 | Same UX cues as current firmware; LED sits behind a light pipe in the right temple. |

# Wiring map

| Signal | XIAO ESP32S3 pin | Peripheral |
| --- | --- | --- |
| `I2C_SDA` | GPIO41 | BNO085 SDA, light sensor SDA, DRV2605L SDA |
| `I2C_SCL` | GPIO40 | BNO085 SCL, light sensor SCL, DRV2605L SCL |
| `MIC_SD` | GPIO9 (I²S data in) | ICS-43434 DOUT |
| `MIC_WS` | GPIO8 | ICS-43434 WS |
| `MIC_SCK` | GPIO7 | ICS-43434 SCK |
| `BATT_SENSE` | GPIO2 / A1 | Voltage divider tap (169 kΩ / 110 kΩ) |
| `BUTTON` | GPIO1 / A0 (pull-up) | Momentary switch to ground |
| `LED_R/G/B` | GPIO21/33/34 (through 1 kΩ) | Common anode RGB LED (optional) |
| `HAPTIC_INT` | GPIO6 | DRV2605L trigger |
| `CAM_PINS` | GPIOs 10–48 | Ribbon connector from OV2640 per `config.h` |

> Keep I²C runs under 10 cm; place the IMU on the bridge flex to minimize motion noise.

# Power architecture

1. **Battery pack:** Each temple houses a 250–300 mAh cell; cells are paralleled via a flex harness to the XIAO battery pads.
2. **Protection/charging:** The XIAO sense board provides LiPo charging (up to 500 mA) when USB-C is attached. Add a **thermal fuse** (Polyfuse 500 mA) inline for safety.
3. **Voltage monitoring:** The firmware expects the 169 kΩ/110 kΩ divider. If resistor values change, update `VOLTAGE_DIVIDER_RATIO`.
4. **Boost (optional):** For accessories needing 5 V (e.g., haptics), use a TPS61230 boost and route enable control to GPIO5.

# Mechanical integration

- **Right temple**: Camera board + button + RGB LED; use the existing `Right Leg cover.STL.stl` and add bosses for the flex harness.
- **Left temple**: Battery, haptic driver, MEMS mic pointed toward the wearer.
- **Bridge**: Host the IMU board and light sensor directly above the nose to minimize drift; adapt `front.step.stl` to include a 12 mm×12 mm pocket plus conformal foam.
- **Cable routing**: Run a 6-pin flex cable across the brow channel (I²C, power, ground) and shield it with conductive tape tied to system ground to reduce EMI from the Wi-Fi antenna.

# Bill of materials (prototype)

| Item | Qty | Unit cost (USD) | Notes |
| --- | --- | --- | --- |
| Seeed XIAO ESP32S3 Sense | 1 | 18.90 | Includes OV2640 + microphone breakout |
| OV2640 cable (70 mm) | 1 | 2.00 | Replacement ribbon for better routing |
| BNO085 breakout (Qwiic) | 1 | 24.95 | SparkFun SEN-15112 or Adafruit 4754 |
| VEML7700 light sensor | 1 | 5.95 | Optional if IMU board lacks ALS |
| ICS-43434 mic breakout | 1 | 6.95 | SparkFun SEN-14662 |
| DRV2605L haptic driver + 10 mm ERM | 1 | 7.50 | Board + actuator |
| LiPo 3.7 V 300 mAh (curved) | 2 | 8.00 | Match dimensions to temple cavities |
| JST 1.25 mm harness | 2 | 1.00 | Battery connectors |
| Polyfuse 500 mA | 1 | 0.60 | Battery protection |
| Flex cable (6-pin) | 1 | 3.00 | Custom-length FFC for temple link |

# Bring-up checklist

1. **Programmer setup** – Install ESP32 board package in Arduino IDE (`https://espressif.github.io/arduino-esp32/package_esp32_index.json`) and select `Seeed XIAO ESP32S3`.
2. **Power test** – Plug USB-C, verify ~4.2 V at the battery pads and <10 mV drop across the fuse.
3. **Peripherals** – Flash the provided `IdeasGlassFirmware.ino`, monitor serial at 115200 baud, confirm:
   - IMU / ALS values stream every second.
   - Battery percentage updates ~90 s.
   - BLE service `IdeasGlass` advertises with the telemetry + command characteristics.
   - (Optional) Wi-Fi connection to your network for Tornado ingestion.
4. **Mechanical fit** – Dry-fit boards inside the STLs, adjust channel widths in `working files/*.step` if ribbon pinch occurs.

# Expansion notes

- Add an **edge-LED light pipe** for status without direct LED exposure.
- Reserve pogo pads for debugging (TX, RX, GND, 3V3, RST) under the right temple cover.
- Consider swapping to **Seeed XIAO ESP32S3 Sense with LoRa** or upcoming Arduino **Nano ESP32 with camera shield** for additional radio options.

With this hardware baseline, the accompanying Arduino firmware can drive the sensors, push data over BLE/Wi-Fi, and hand off multi-modal packets to the Tornado + Postgres infrastructure.
