#!/usr/bin/env python3
"""
Generate a stable device ID and an optional QR code PNG.

Usage:
  source ~/miniconda3/bin/activate glass
  python backend/bridge/tools/generate_device_id.py                # prints ID
  python backend/bridge/tools/generate_device_id.py --out device.png
  python backend/bridge/tools/generate_device_id.py --id my-device-123 --out my.png

The QR encodes the literal device ID string.
"""
import argparse
import os
import sys
import uuid


def make_id() -> str:
    # Short, URL-safe ID
    raw = uuid.uuid4().hex[:12]
    return f"ideasglass-{raw}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a device ID and optional QR code")
    ap.add_argument("--id", default=None, help="Explicit device ID to encode (default: generate)")
    ap.add_argument("--out", default=None, help="Write QR PNG to this path (optional)")
    args = ap.parse_args()

    dev_id = args.id or make_id()
    print(dev_id)

    if args.out:
        try:
            import qrcode  # type: ignore
        except Exception:
            print("qrcode not installed; run: pip install qrcode[pil]", file=sys.stderr)
            return 0
        img = qrcode.make(dev_id)
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        img.save(args.out)
        print(f"QR written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

