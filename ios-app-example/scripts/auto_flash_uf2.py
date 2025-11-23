#!/usr/bin/env python3
"""
Auto-enter UF2 bootloader (1200 bps touch) and copy a UF2 file.

Tested with Seeed XIAO nRF52840 Sense (UF2 bootloader). Many nRF52 UF2
bootloaders support entering bootloader when the CDC ACM port is opened at
1200 baud and DTR is toggled. This script does that and then copies the UF2
once the XIAO-SENSE volume mounts.

Usage:
  python3 scripts/auto_flash_uf2.py --uf2 path/to/zephyr.uf2 \
    --port /dev/cu.usbmodem141201 [--label XIAO-SENSE] [--timeout 30]

Requires:
  pip install pyserial
"""
import argparse
import os
import time
import shutil
from glob import glob

def find_default_port():
    candidates = sorted(glob('/dev/cu.usbmodem*'))
    if len(candidates) == 1:
        return candidates[0]
    return None

def enter_bootloader_1200bps(port: str):
    try:
        import serial  # pyserial
    except ImportError:
        raise SystemExit("pyserial not installed. Run: pip install pyserial")

    # Open at 1200 bps, toggle DTR, close.
    ser = serial.Serial(port, 1200)
    try:
        ser.setDTR(False)
        time.sleep(0.05)
        ser.setDTR(True)
        time.sleep(0.05)
    finally:
        ser.close()

def wait_for_volume(label: str, timeout: float) -> str:
    mount_path = f"/Volumes/{label}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.isdir(mount_path):
            return mount_path
        time.sleep(0.2)
    raise TimeoutError(f"Timed out waiting for volume {mount_path}")

def copy_uf2(uf2_path: str, mount_path: str):
    dst = os.path.join(mount_path, os.path.basename(uf2_path))
    shutil.copy(uf2_path, dst)
    return dst

def wait_for_unmount(label: str, timeout: float = 20.0):
    mount_path = f"/Volumes/{label}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not os.path.isdir(mount_path):
            return True
        time.sleep(0.2)
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--uf2', required=True, help='Path to UF2 firmware file')
    ap.add_argument('--port', default=None, help='Serial port (e.g. /dev/cu.usbmodem141201)')
    ap.add_argument('--label', default='XIAO-SENSE', help='Expected volume label when in UF2 mode')
    ap.add_argument('--timeout', type=float, default=30.0, help='Seconds to wait for the UF2 volume to mount')
    args = ap.parse_args()

    uf2_path = os.path.abspath(args.uf2)
    if not os.path.isfile(uf2_path):
        raise SystemExit(f"UF2 not found: {uf2_path}")

    port = args.port or find_default_port()
    if not port:
        raise SystemExit("No serial port provided and none auto-detected. Pass --port /dev/cu.usbmodemXXXX")

    print(f"Triggering bootloader via 1200bps on {port}...")
    enter_bootloader_1200bps(port)

    print(f"Waiting for /Volumes/{args.label}...")
    mount_path = wait_for_volume(args.label, args.timeout)
    print(f"Mounted: {mount_path}")

    print(f"Copying UF2: {uf2_path}")
    dst = copy_uf2(uf2_path, mount_path)
    print(f"Copied to: {dst}")

    if wait_for_unmount(args.label):
        print("Device rebooted (volume unmounted). Flash complete.")
    else:
        print("Warning: Volume did not unmount automatically. Verify device reboot.")

if __name__ == '__main__':
    main()

