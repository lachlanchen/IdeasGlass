# DK2 (XIAO nRF52840 Sense) Flashing Without Double‑Tap

This note lists ways to flash firmware without physically double‑tapping the reset button.

Options

- 1200 bps USB trigger (UF2 bootloader)
  - Many nRF52 UF2 bootloaders (including Seeed XIAO BLE Sense) enter bootloader when their CDC serial port is opened at 1200 baud and DTR is toggled.
  - Use our helper to trigger bootloader and copy the UF2 automatically:
    - Ensure the device is connected via USB‑C.
    - Find the serial port (macOS): `ls /dev/cu.usbmodem*`
    - Install dependency in your Python env: `pip install pyserial`
    - Run:
      - `scripts/flash_dk2_uf2_auto.sh --port /dev/cu.usbmodem141201`
      - or directly: `python3 scripts/auto_flash_uf2.py --port /dev/cu.usbmodem141201 --uf2 firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2`
  - The script:
    1) Opens the serial port at 1200 bps (DTR toggle) to enter bootloader
    2) Waits for `/Volumes/XIAO-SENSE`
    3) Copies the UF2 and waits for the auto‑eject (reboot)

- SWD/J‑Link (no bootloader required)
  - If you have a J‑Link connected to the SWD pads, you can flash directly with west:
    - `west flash -d firmware/zephyr-workspace/build-dk2 --runner jlink`
  - This bypasses the bootloader entirely and programs the addresses contained in `zephyr.hex` (e.g., 0x27000). Use with care; keep the bootloader region intact if you want to retain UF2 updates later.

- OTA/DFU (if firmware supports it)
  - Some builds support OTA updates via BLE or MCUboot/DFU. See `firmware/BUILD_AND_OTA_FLASH.md` for project‑specific details. This method requires the device to be running compatible firmware and is not covered by the UF2 helper.

Notes

- The UF2 volume label is typically `XIAO-SENSE` on DK2; if yours differs, pass `--label` to the Python helper.
- If multiple `/dev/cu.usbmodem*` ports exist, pass `--port` explicitly.
- If the UF2 copy completes but the volume does not unmount automatically, power‑cycle the device to boot into the new firmware.

