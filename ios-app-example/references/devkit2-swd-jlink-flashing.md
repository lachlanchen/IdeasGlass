# DevKit2 SWD Flashing (J‑Link) and West Runners

This guide shows how to flash Omi DevKit2 (Seeed XIAO nRF52840 Sense) over SWD using a SEGGER J‑Link, and how to use west/nRF runners to program directly from your Zephyr build. Use this when you want to bypass UF2 or when developing firmware repeatedly.

Applies to firmware under `OmiReference/omi/firmware/devkit` (Zephyr RTOS on nRF52840).

---

## 0) Hardware: SWD wiring

- Programmer: SEGGER J‑Link (Base, EDU, or EDU Mini). A CMSIS‑DAP probe also works (commands differ).
- Pins (Cortex‑M 10‑pin header → target SWD pads):
  - 1 VTref → target 3V3 (sense only)
  - 2 SWDIO → SWDIO pad on XIAO nRF52840 Sense
  - 4 SWCLK → SWCLK pad on XIAO nRF52840 Sense
  - 3/5/9 GND → target GND
  - 10 nRESET (optional) → RST (optional; you can reset by command)
- Ensure VTref is present (~3.3 V) so the probe recognizes the logic level.

See Seeed XIAO nRF52840 Sense docs for exact pad locations (back side SWD pads).

---

## 1) Software prerequisites

- SEGGER J‑Link software (macOS/Windows/Linux): installs `JLinkExe` and drivers.
- Nordic nRF Command Line Tools (optional but handy): installs `nrfjprog`.
- Zephyr toolchain / nRF Connect SDK + west (for building and west flashing).

Verify:
```bash
JLinkExe -v
nrfjprog --version   # optional
west --version       # if you are building with Zephyr
```

---

## 2) Build the firmware (Zephyr)

From the project root (adjust the overlay to your DK2 config):
```bash
west init -l .
west update

# Example board/config; adjust to your tree
west build -p auto -b seeed_xiao_blesense OmiReference/omi/firmware/devkit \
  -DOVERLAY_CONFIG=OmiReference/omi/firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf
```
Artifacts:
- `build/zephyr/zephyr.hex` (application)
- If your config includes bootloader/MCUboot, the addresses will be offset accordingly.

Note on bootloader layouts:
- If the device uses Adafruit UF2 bootloader + SoftDevice, application is linked above the SoftDevice (typical app start around 0x26000/0x27000). Use the hex linked for that offset.
- If you build a pure Zephyr app without UF2/SoftDevice, it may link at 0x00000000 and replace the bootloader. Decide which layout you want before flashing.

---

## 3) Flash using west runners (simplest for Zephyr)

Use `nrfjprog` or `jlink` runner (requires the corresponding tools installed):
```bash
# Program and reset
west flash --runner nrfjprog        # or: --runner jlink

# If you need a full chip erase first (careful: removes bootloader/UF2)
west flash --erase --runner nrfjprog
```
Troubleshooting:
- If locked: `nrfjprog --recover` then `west flash` again.
- If using `--runner jlink`, ensure `JLinkExe` is on PATH.

---

## 4) Flash using nrfjprog (manual)

Manual commands using the hex from `build/zephyr/`:
```bash
# Show connected probes
nrfjprog --ids

# Optional: full erase (removes bootloader)
# nrfjprog --recover

# Program and verify
nrfjprog --program build/zephyr/zephyr.hex --verify --reset
```

If your app is linked for a non‑zero start address (UF2 layout), `nrfjprog` will respect the addresses in the hex.

---

## 5) Flash using J‑Link Commander (manual)

Interactive session:
```text
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000
J-Link> connect
J-Link> erase            # careful: full chip erase
J-Link> loadfile build/zephyr/zephyr.hex
J-Link> r                # reset
J-Link> g                # go (run)
J-Link> q
```
You can also script this via a `.jlink` command file.

---

## 6) Preserving/using the UF2 bootloader

If you want to keep the UF2 bootloader (for easy drag‑and‑drop updates):
- Do not `--recover` or `erase` the bootloader region.
- Build your application for the correct app offset (matching the UF2 bootloader + SoftDevice layout), or use the prelinked application hex from your project.
- Program only the application region (the linked hex will contain addresses above the bootloader).

If you accidentally erase the bootloader:
- Reflash SoftDevice + UF2 bootloader via SWD (bootloader projects provide `*.hex`), then program your app, or just continue without UF2 if you prefer SWD/west only.

---

## 7) Renaming the BLE device (LightMind Link 2)

See `references/devkit2-rename-and-uf2.md` for details:
- Static: set `CONFIG_BT_DEVICE_NAME="LightMind Link 2"` in the DK2 overlay .conf.
- Dynamic suffix: compute a short ID at boot, call `bt_set_name()` and `bt_le_adv_update_data()` to publish `LightMind Link 2-ABCD`.
- Optional: set DIS strings (`CONFIG_BT_DIS_*`) or add a custom GATT characteristic for a full device UUID.

---

## 8) Verify on iOS

- After flashing, open the LightMind iOS app and scan. You should see the new name.
- The app persists `CBPeripheral.identifier` for auto‑reconnect; we also display the device name in the connection page.

---

## 9) Troubleshooting

- `nrfjprog: Operation failed` → try `nrfjprog --recover`, ensure SWD wiring and VTref, update J‑Link firmware.
- Cannot connect: check GND, SWDIO/SWCLK swapped, low battery, or target not powered. You can power via USB or a bench supply.
- App won’t start: you flashed a 0x0000‑linked app over a UF2 layout (or vice versa). Rebuild with the intended layout or re‑flash bootloader + SoftDevice.
- iOS still shows old name: forget in system Bluetooth settings or power‑cycle the device; ensure advertising name was updated.

---

## 10) Which path to choose?

- Prototyping/production convenience: keep UF2 bootloader and flash prebuilt UF2 (or app hex at the correct offset). Quick updates without a probe.
- Firmware development: use west `--runner nrfjprog` or `--runner jlink` for one‑command build + flash. Consider disabling UF2 to reclaim flash and simplify layout.
