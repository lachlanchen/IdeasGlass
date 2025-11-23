#!/usr/bin/env python3
"""
Generate a LightMind device name and a QR code image in a local folder.

Default device name template: "LightMind-<UID>"
Where UID is an 8‑character uppercase letters + digits string.

Usage:
  python3 scripts/generate_lightmind_qr.py
  python3 scripts/generate_lightmind_qr.py --length 10 --outdir assets/qrcodes
  python3 scripts/generate_lightmind_qr.py --uid ABCD1234  # use a provided UID

The script tries to import the 'qrcode' package and will attempt to install
qrcode[pil] + pillow automatically if missing.
"""
import argparse
import os
import sys
import secrets
import string
from datetime import datetime


def ensure_qrcode():
    try:
        import qrcode  # noqa: F401
        return
    except ModuleNotFoundError:
        pass
    # Try to install dependencies automatically
    print("qrcode not found; attempting to install qrcode[pil] + pillow...", file=sys.stderr)
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]", "pillow"])  # noqa: S603,S607
    except Exception as e:  # noqa: BLE001
        print(f"Auto-install failed: {e}", file=sys.stderr)
        print("Please install manually: pip install 'qrcode[pil]' pillow", file=sys.stderr)
        sys.exit(1)


def generate_uid(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def make_qr_png(data: str, out_path: str) -> None:
    ensure_qrcode()
    import qrcode

    qr = qrcode.QRCode(
        version=None,  # automatic
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)


def main():
    parser = argparse.ArgumentParser(description="Generate LightMind device name + QR image.")
    parser.add_argument("--prefix", default="LightMind-", help="Device name prefix (default: LightMind-)")
    parser.add_argument("--uid", default=None, help="Provide a specific UID (uppercase letters+digits)")
    parser.add_argument("--length", type=int, default=8, help="UID length if auto-generating (default: 8)")
    parser.add_argument("--outdir", default=os.path.join("scripts", "qr_out"), help="Output directory for QR files")
    parser.add_argument("--basename", default=None, help="Base filename (without extension). Default derives from device name.")
    args = parser.parse_args()

    uid = args.uid or generate_uid(args.length)
    # Normalize provided uid: uppercase and restrict to A–Z0–9
    uid = "".join(ch for ch in uid.upper() if ch in (string.ascii_uppercase + string.digits))
    if len(uid) == 0:
        print("Error: UID is empty after normalization.", file=sys.stderr)
        sys.exit(2)

    device_name = f"{args.prefix}{uid}"

    os.makedirs(args.outdir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = args.basename or device_name.replace(" ", "_")
    png_path = os.path.join(args.outdir, f"{base}-{timestamp}.png")

    # Generate QR for the device name text
    make_qr_png(device_name, png_path)

    # Also persist a small metadata file for convenience
    meta_path = os.path.join(args.outdir, f"{base}-{timestamp}.txt")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"device_name={device_name}\n")
        f.write(f"uid={uid}\n")
        f.write(f"generated_at={timestamp}\n")

    print(f"Device Name: {device_name}")
    print(f"QR saved:    {png_path}")
    print(f"Meta saved:  {meta_path}")


if __name__ == "__main__":
    main()

