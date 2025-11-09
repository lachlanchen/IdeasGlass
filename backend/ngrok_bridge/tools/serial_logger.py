#!/usr/bin/env python3
"""
IdeasGlass Serial Logger

Captures ESP32 serial logs and writes both plain-text and JSONL with timestamps.
Defaults to /dev/ttyACM0 as requested; override with --port if needed.

Usage examples:
  pip install pyserial
  python backend/ngrok_bridge/tools/serial_logger.py --port /dev/ttyACM0 --baud 115200 --out logs/ideasglass-serial
  python backend/ngrok_bridge/tools/serial_logger.py --list
"""

import argparse
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

try:
    import serial
    from serial.tools import list_ports
except Exception as exc:
    print("pyserial is required. Install with: pip install pyserial", file=sys.stderr)
    raise


# Tag known lines we care about when analyzing photo upload behavior
PATTERNS = [
    (re.compile(r"\\[PhotoUpload\\].*WS send failed", re.I), "photo_ws_failed"),
    (re.compile(r"\\[PhotoUpload\\].*falling back to HTTPS", re.I), "photo_http_fallback"),
    (re.compile(r"\\[HTTP\\].*Response:", re.I), "http_response"),
    (re.compile(r"\\[WiFi\\].*Connected", re.I), "wifi_connected"),
    (re.compile(r"\\[WiFi\\].*Failed", re.I), "wifi_failed"),
    (re.compile(r"\\[Audio\\].*chunk", re.I), "audio_chunk"),
    (re.compile(r"\\[Camera\\].*Captured", re.I), "camera_captured"),
]


def default_port() -> str:
    # Honor the user's request: prefer /dev/ttyACM0 by default
    candidate = "/dev/ttyACM0"
    try:
        p = Path(candidate)
        if p.exists():
            return candidate
    except Exception:
        pass
    # Fallback: try to detect a likely port
    ports = list(list_ports.comports())
    for info in ports:
        if any(tok in info.device for tok in ("ACM", "USB", "tty.SLAB", "ttyUSB")):
            return info.device
    return ports[0].device if ports else candidate


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def open_logs(outdir: Path):
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    txt = outdir / f"{ts}.log"
    jsn = outdir / f"{ts}.jsonl"
    return txt.open("a", buffering=1, encoding="utf-8"), jsn.open("a", buffering=1, encoding="utf-8")


def parse_tags(line: str) -> list[str]:
    tags: list[str] = []
    for rx, tag in PATTERNS:
        if rx.search(line):
            tags.append(tag)
    bracket = re.search(r"\\[([A-Za-z0-9_\-]+)\\]", line)
    if bracket:
        tags.append(bracket.group(1))
    # De-duplicate preserving order
    seen = set()
    out: list[str] = []
    for t in tags:
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out


def main():
    ap = argparse.ArgumentParser(description="IdeasGlass serial logger")
    ap.add_argument("--port", default=default_port(), help="Serial port (default: /dev/ttyACM0 if present)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--out", type=Path, default=Path("logs/ideasglass-serial"))
    ap.add_argument("--list", action="store_true", help="List serial ports and exit")
    args = ap.parse_args()

    if args.list:
        for p in list_ports.comports():
            print(f"{p.device}\t{p.description}")
        return

    ensure_dir(args.out)
    txt, jsn = open_logs(args.out)
    print(f"[Logger] Port={args.port} baud={args.baud} → {args.out}")

    while True:
        try:
            with serial.Serial(args.port, args.baud, timeout=1) as ser:
                # Nudge DTR/RTS to prompt output on some boards
                try:
                    ser.setDTR(False); ser.setRTS(False); time.sleep(0.05)
                    ser.setDTR(True); ser.setRTS(True); time.sleep(0.1)
                except Exception:
                    pass
                # Non-blocking read loop
                while True:
                    raw = ser.readline()
                    if not raw:
                        continue
                    ts = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="milliseconds")
                    try:
                        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                    except Exception:
                        line = repr(raw)
                    tags = parse_tags(line)
                    txt.write(f"{ts} {line}\n")
                    jsn.write(json.dumps({"ts": ts, "line": line, "tags": tags}, ensure_ascii=False) + "\n")
                    print(f"{ts} {line}")
        except KeyboardInterrupt:
            print("\n[Logger] Stopped by user.")
            break
        except serial.SerialException as e:
            print(f"[Logger] Serial error: {e}. Reconnecting in 2s…")
            time.sleep(2)
        except Exception as e:
            print(f"[Logger] Unexpected error: {e}. Reconnecting in 2s…")
            time.sleep(2)


if __name__ == "__main__":
    main()
