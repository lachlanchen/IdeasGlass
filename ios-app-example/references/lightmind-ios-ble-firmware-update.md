**Overview**
- LightMind iOS updates DevKit2 (XIAO nRF52840 Sense) firmware over Bluetooth using Nordic’s Legacy Secure DFU.
- The same DK2 hardware keeps its UF2 USB bootloader; BLE DFU is an additional path, not a replacement.
- The flow mirrors the Omi reference app but is implemented in SwiftUI with the `NordicDFU` Swift Package.

**Where It Lives**
- iOS app:
  - DFU UI and logic: `apps/ios/LightMind/LightMindApp/FirmwareUpdateView.swift`
  - BLE transport, DFU control point, auto‑reconnect: `apps/ios/LightMind/LightMindApp/BLEManager.swift`
  - DFU UUIDs (Legacy DFU service + control point): `apps/ios/LightMind/LightMindApp/BluetoothProfile.swift`
- Firmware (DevKit2):
  - Legacy DFU GATT service and control point: `firmware/devkit/src/transport.c`
    - Service UUID: `00001530-1212-EFDE-1523-785FEABCD123`
    - Control Point UUID: `00001531-1212-EFDE-1523-785FEABCD123`
    - Handler sets `NRF_POWER->GPREGRET = 0xA8` and resets into the AdaFruit / Nordic DFU bootloader (`AdaDFU`).

**Firmware Artifacts (DK2)**
- Omi DevKit2 reference (2.0.10):
  - UF2 (USB): `dev-kit-2-firmware/Omi_DK2_v2.0.10.uf2`
  - Legacy DFU ZIP (BLE): `dist/firmware/firmware.zip`
- LightMind DK2:
  - 2.0.11 test: `dist/firmware/lightmind-dk2-test-2.0.11.zip`
  - 2.0.12: `dist/firmware/lightmind-dk2-2.0.12.zip`
  - 2.0.13: `dist/firmware/lightmind-dk2-2.0.13.zip`
- Public server (served by `scripts/serve_pwa_and_firmware.py`, root `dist`):
  - `https://ios.lightmind.art/downloads/firmware/…` for each ZIP above.

**iOS DFU Flow**
- From the “Firmware Update” screen:
  1. User taps “Install” for a specific version; `FirmwareUpdateView.startUpdate(from:)` downloads the ZIP.
  2. It creates `DFUFirmware(urlToZipFile:)` and snapshots central + peripheral from `BLEManager`.
  3. It calls `beginLegacyDFU(with:target:peripheralSnapshot:central:)`.
- `beginLegacyDFU`:
  - Calls `ble.prepareForDFU()` to stop scan and disconnect cleanly.
  - Builds `DFUServiceInitiator` with:
    - `packetReceiptNotificationParameter = 8`
    - `forceScanningForNewAddressInLegacyDfu = true`
    - `enableUnsafeExperimentalButtonlessServiceInSecureDfu = true`
    - `alternativeAdvertisingNameEnabled = true`
    - `connectionTimeout = 60.0`
    - `peripheralSelector = NameOrServiceSelector()` (matches `AdaDFU`, DFU UUIDs).
  - Wires logger, progress, and state delegates with strong references so they are not deallocated.
  - Starts DFU via `.start(targetWithIdentifier: uuid)`, where `uuid` is the original app‑mode peripheral ID.

**Auto‑Reconnect After DFU**
- During DFU: `BLEManager.dfuInProgress` is set to `true` so auto‑reconnect does not fight Nordic DFU.
- On completion or error:
  - `setDFUInProgress(false)` runs synchronously on the main thread.
  - `restoreCentralAfterDFU()` restores `CBCentralManager`’s delegate to `BLEManager` and calls `autoReconnectIfPossible()`.
  - `autoReconnectIfPossible()`:
    - Tries `retrievePeripherals(withIdentifiers:)` using the last persisted UUID.
    - If that fails, starts a scan for the last audio service, auto‑connecting when seen.
- Firmware page fallback:
  - `FirmwareUpdateView` remembers `dfuTargetName` and, after DFU, runs a short name‑based scan:
    - Logs “Firmware DFU page: scanning for <name> to auto‑reconnect after DFU”.
    - When it sees a discovered peripheral with that name, it calls `ble.connect(to:)` automatically and logs “auto‑connecting by name”.

**Build & Packaging (Do Not Change Lightly)**
- Build DK2 app from `firmware/devkit` using NCS v2.9.0:
  - `cd firmware/zephyr-workspace`
  - `bash ../../scripts/build_dk2.sh`
- Generate DFU ZIP with `adafruit-nrfutil` (via `scripts/package_dk2_dfu.sh`):
  - Uses the FW version from `CONFIG_BT_DIS_FW_REV_STR` in `firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf`.
  - Produces `dist/firmware/lightmind-dk2-<version>.zip` with `zephyr.bin`, `zephyr.dat` and `manifest.json`.
- Do **not** hand‑edit init packets; always regenerate ZIPs via the script.

**UX Notes**
- Keep the phone close to the device and avoid other BLE apps during DFU.
- UF2 remains available via double‑tap reset -> `XIAO‑SENSE` mass‑storage and dragging a UF2.
- iOS logs (Firmware Update screen + Bluetooth logs) are the source of truth for diagnosing DFU behavior; auto‑reconnect events are explicitly logged.
