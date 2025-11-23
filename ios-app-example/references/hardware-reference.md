# Hardware Reference

## DevKit 1 (Zephyr + Seeed XIAO nRF52840 Sense)
- Necklace form factor with Seeed Studio XIAO nRF52840 Sense core, onboard mic/IMU, USB-C, rechargeable battery.
- Enumerates as Nordic `2fe3:0100` CDC-ACM (`ZEPHYR USB-DEV`); verify via `lsusb` or `/dev/serial/by-id` symlink before flashing.
- Firmware updated via Omi app or manual UF2 drop from releases (`release_firmware+DK1`).
- Source: `OmiBH/docs/doc/hardware/DevKit1.mdx`.

## DevKit 2 (Upgraded necklace)
- Builds on DevKit1: still XIAO nRF52840 but adds 8 GB storage, onboard speaker, programmable button for standalone recording.
- Order assembled kits from omi.me; firmware workflow mirrors DK1 (`release_firmware+DK2`).
- Source: `OmiBH/docs/doc/hardware/DevKit2.mdx`.

## Omi Consumer V1 (CV1)
- Daily-wear version powered by dual-core Nordic nRF5340 + nRF7002 Wi-Fi 6; dual T5838 PDM mics for high-quality capture.
- Updated via mobile app or CV1 firmware releases.
- Source: `OmiBH/docs/doc/hardware/OmiConsumer.mdx`.

## omiGlass DevKit
- Open-source glasses platform using Seeed XIAO ESP32-S3 Sense, 6×150 mAh + 1×250 mAh cells, Ollama + Arduino toolchain.
- Requires 3D-printed frame, Expo web/app frontend, Arduino firmware (`omiGlass/firmware`).
- Lacks hardware power switch (contribution opportunity); follow doc for PSRAM config and component list.
- Source: `OmiBH/docs/doc/hardware/omiGlass.mdx`.

## Seeed Studio XIAO nRF52840 Family
- Core module powering DevKit1/2: 64 MHz Cortex-M4F, BLE 5.2 + NFC, 256 KB RAM, 1 MB internal + 2 MB external flash, battery charger with 50/100 mA modes.
- Sense variants add LSM6DS3TR-C IMU + PDM mic; Plus boards expose up to 20 PWM pins, dual UART/SPI, I2S.
- Arduino setup via Seeed board packages; LED is active-low; includes deep-sleep sample for current validation.
- Source: `OmiBH/docs/doc/hardware/Seeed_XIAO_nRF52840.mdx`.

## Troubleshooting Checklist
- USB identification: `lsusb` for `2fe3:0100` (DevKits) or board-specific descriptors; confirm `/dev/serial/by-id` path before flashing.
- Firmware delivery: prefer Omi app, fall back to UF2 copy on XIAO bootloader drive (`/Volumes/XIAO-SENSE`).
- Tooling: Zephyr for DevKits, Arduino CLI/IDE for omiGlass, Expo app integration for user flows.
