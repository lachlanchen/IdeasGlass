# DevKit2: Build “LightMind Link 2” firmware and Flash via UF2

This is the exact recipe (with file locations) to build the DK2 firmware with the BLE name set to “LightMind Link 2” and flash it over USB/UF2.

## What’s already changed
- Name + DIS fields are set in: `OmiReference/omi/firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf`
  - `CONFIG_BT_DEVICE_NAME="LightMind Link 2"`
  - `CONFIG_BT_DIS_MODEL="LightMind Link 2"`
  - `CONFIG_BT_DIS_MANUF="LightMind"`

## Prerequisites (one‑time)
- Nordic Toolchain Manager installed (done)
- Zephyr/NCS workspace initialized at `firmware/zephyr-workspace` (done)

## Build (inside the NCS shell)
1) Launch the NCS shell (you already did):
   - `nrfutil toolchain-manager launch --ncs-version v2.9.0 --shell`
2) From the repo root:
   - `bash scripts/build_dk2.sh`

Outputs:
- HEX: `firmware/zephyr-workspace/build-dk2/zephyr/zephyr.hex`
- BIN: `firmware/zephyr-workspace/build-dk2/zephyr/zephyr.bin`

## Flash via UF2 (auto‑copy)
1) Put the DK2 into UF2 mode: double‑tap reset → a drive named `XIAO-SENSE` appears.
2) From the repo root (still inside the NCS shell):
   - `bash scripts/flash_dk2_uf2.sh`

The west UF2 runner copies the image to the mounted drive; it auto‑ejects and reboots.

### USB‑C UF2 Flashing — who does what
- What you do
  - Double‑tap the board’s reset button so `XIAO-SENSE` mounts.
  - Run `bash scripts/flash_dk2_uf2.sh` (or tell me it’s mounted and I run it for you), or simply copy the UF2 file manually.
- What I can do
  - Build the firmware (done).
  - Run the flash script once `XIAO-SENSE` is mounted.
  - Provide the exact UF2 file path if you prefer manual copy.

### Manual copy (no west runner)
- UF2 artifact path:
  - `firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2`
- Copy:
  - `cp firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2 /Volumes/XIAO-SENSE`

### Optional: auto‑enter UF2 mode (hands‑free)
If your UF2 bootloader supports the 1200‑bps “touch” trick (common on Adafruit bootloaders):
- I can provide a small Python/bash helper that opens the board’s serial port at 1200 bps to trigger UF2 mode, waits for `XIAO-SENSE` to mount, and then copies the UF2 automatically.
- What I need from you: the serial port path (e.g., `/dev/tty.usbmodemXXXX`).

## Optional: produce a UF2 file explicitly
If you want a UF2 file to drag‑drop manually:

```bash
# Install the UF2 converter once
python3 -m pip install uf2tool  # provides uf2conv.py

# Convert the built HEX to UF2
python3 -m uf2conv -c -o app.uf2 -f 0xADA52840 \
  firmware/zephyr-workspace/build-dk2/zephyr/zephyr.hex
```

Then double‑tap reset and copy `app.uf2` to the `XIAO-SENSE` drive.

## Verify on iOS
- Open the LightMind app → Devices page → Scan
- You should see: `LightMind Link 2` as the device name
- Connect and confirm battery/audio

## Notes / Next steps
- If you want a per‑device suffix (e.g., `LightMind Link 2‑ABCD`) or a GATT‑exposed Device UUID, see `references/devkit2-rename-and-uf2.md` and ask to enable it before building.
- SWD/J‑Link flashing and west runners are documented in `references/devkit2-swd-jlink-flashing.md`.
