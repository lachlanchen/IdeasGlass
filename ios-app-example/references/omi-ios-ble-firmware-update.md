**Overview**
- The Omi iOS app updates device firmware over Bluetooth LE using two strategies:
  - Legacy Secure DFU (Nordic DFU for nRF52-class devices, e.g., DK2/XIAO nRF52840 Sense)
  - MCUboot + MCUmgr DFU (SMP protocol, used on newer nRF5340 builds)
- The app decides which path to use via a server flag `is_legacy_secure_dfu` bundled with the firmware manifest.

**Where In Code**
- iOS (Flutter) DFU logic: `OmiReference/app/lib/pages/home/firmware_mixin.dart:1`
  - Uses `nordic_dfu` for Legacy Secure DFU and `mcumgr_flutter` for MCUboot DFU.
- Device-side DFU trigger (DevKit2 firmware): `OmiReference/omi/firmware/devkit/src/transport.c:118`
  - Registers a Nordic Legacy DFU GATT service/control point and reboots into bootloader on write.

**Two DFU Paths**
- Legacy Secure DFU (nRF52)
  - BLE Service: 00001530-1212-EFDE-1523-785FEABCD123
  - Control Point: 00001531-1212-EFDE-1523-785FEABCD123
  - Firmware: a Nordic DFU ZIP (bin + dat) transferred by the phone.
  - iOS library: `nordic_dfu` Flutter plugin (wraps Nordic iOS DFU Library).
  - Device behavior: write to the control point triggers bootloader via GPREGRET + reset; bootloader advertises as DFU target and receives the image.
- MCUboot + MCUmgr (nRF5340)
  - BLE Service (SMP): standard MCUmgr GATT (SMP over BLE).
  - Firmware: a `firmware.zip` containing one or more image files described by `manifest.json`.
  - iOS library: `mcumgr_flutter` plugin (FirmwareUpdateManager uploads, tests, and confirms).
  - Device behavior: app’s MCUmgr service receives chunks into the secondary slot, then swap/confirm.

**Firmware Support On DevKit2 (XIAO nRF52840 Sense)**
- DFU GATT is implemented in `OmiReference/omi/firmware/devkit/src/transport.c:118`.
  - Service UUID: 00001530‑1212‑EFDE‑1523‑785FEABCD123
  - Control point UUID: 00001531‑1212‑EFDE‑1523‑785FEABCD123
  - Handler: `dfu_control_point_write_handler` reboots into bootloader when receiving 0x06 or 0x01 commands by setting `NRF_POWER->GPREGRET = 0xA8` then `NVIC_SystemReset()`.
  - The device advertises this DFU service in its advertising data so the iOS DFU library can detect it.

**iOS App Implementation (Flutter)**
- Entry points: `OmiReference/app/lib/pages/home/firmware_mixin.dart:1`
  - Decision flag: `isLegacySecureDFU` (defaults true) determines path.
  - Download: app downloads `firmware.zip` from `zip_url` to the app’s documents directory.
- Legacy Secure DFU path: `startLegacyDfu()`
  - Library: `nordic_dfu` (`pubspec.yaml` depends on `nordic_dfu: ^6.1.4+hotfix`).
  - Parameters:
    - `enableUnsafeExperimentalButtonlessServiceInSecureDfu: true` enables buttonless DFU mode.
    - iOS PRN and timeouts configured via `IosSpecialParameter`.
  - Flow:
    1) App calls `prepareDFU()` to disconnect gracefully.
    2) Library connects and writes to the DFU control point to enter bootloader.
    3) Device reboots; bootloader advertises as DFU target.
    4) Library reconnects and uploads the ZIP; progress reported via callbacks.
    5) On completion, device reboots into application.
- MCUboot DFU path: `startMCUDfu()`
  - Library: `mcumgr_flutter: ^0.4.2` (SMP over BLE).
  - The ZIP is extracted and each `file` from `manifest.json` becomes an `mcumgr.Image`.
  - `FirmwareUpdateManager` is set up with `FirmwareUpgradeConfiguration` then `update()` streams the images.
  - Progress and state (success/failure) are handled via streams; on success the device reboots into the new image and confirms.

**End‑to‑End Update Flow**
- Check for updates
  - App queries backend; receives `latestFirmwareDetails` including `zip_url`, `is_legacy_secure_dfu`, and any `ota_update_steps`.
- Prepare
  - App downloads `firmware.zip` to Documents and calls `prepareDFU()` which disconnects and pauses services.
- Enter DFU and transfer
  - Legacy path: Nordic DFU library triggers the DFU control point; device reboots to bootloader; library uploads ZIP.
  - MCUboot path: App connects to device’s SMP GATT service and performs MCUmgr image upload; bootloader swap occurs automatically.
- Finish
  - On successful completion, app marks DFU complete and the device re‑advertises normally.

**Artifacts**
- Legacy Secure DFU: Nordic DFU ZIP placed at `…/Documents/firmware.zip`.
- MCUboot DFU: Same ZIP but parsed locally; images are pushed via SMP.

**How To Reuse In LightMind**
- If targeting DK2/XIAO (nRF52840):
  - Use Nordic DFU iOS library (or the Flutter `nordic_dfu` plugin) and ensure firmware exposes the DFU control point and bootloader supports Secure DFU.
- If targeting CV1 (nRF5340 + MCUboot):
  - Use MCUmgr (SMP over BLE) via a Swift package or Flutter plugin; generate `dfu_application.zip` when building.

**Troubleshooting**
- Device never switches to DFU
  - Ensure DFU service is advertising and control point write triggers `GPREGRET`+reset on firmware.
  - If bootloader uses a different advertising name (e.g., DfuTarg), allow the library to rescan/reconnect.
- Update stalls mid‑transfer
  - Reduce PRN/pipeline depth; keep the phone screen on and in range.
  - Check for battery level and ensure the device isn’t powering down.
- “Legacy vs MCUboot” confusion
  - DK2 DevKit builds typically use Legacy Secure DFU; CV1 builds use MCUboot with MCUmgr.

**Key References**
- iOS DFU mixin: `OmiReference/app/lib/pages/home/firmware_mixin.dart:1`
- DFU GATT in firmware (DevKit2): `OmiReference/omi/firmware/devkit/src/transport.c:118`
- Build + OTA guide (CV1): `OmiReference/omi/firmware/BUILD_AND_OTA_FLASH.md:1`

