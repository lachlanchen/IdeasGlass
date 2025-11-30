#!/usr/bin/env python3
"""
Backend logger: runs uvicorn for backend.ngrok_bridge.app and records a timestamped log
to a separate folder (defaults to logs/ideasglass-backend).

Example:
  source ~/miniconda3/bin/activate glass
  python backend/ngrok_bridge/tools/backend_logger.py --port 8765 --out logs/ideasglass-backend

Pass-through env like DATABASE_URL is inherited from the current shell.
"""

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Run backend with logging")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--reload", action="store_true", help="Enable uvicorn --reload")
    ap.add_argument("--out", type=Path, default=Path("logs/ideasglass-backend"))
    ap.add_argument(
        "--extra",
        nargs=argparse.REMAINDER,
        help="Extra args after -- (passed to uvicorn)",
    )
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = args.out / f"uvicorn-{ts}.log"

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.ngrok_bridge.app:app",
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--proxy-headers",
        "--forwarded-allow-ips",
        "*",
    ]
    if args.reload:
        cmd.append("--reload")
    if args.extra:
        # Strip a leading '--' if present
        extra = args.extra
        if extra and extra[0] == "--":
            extra = extra[1:]
        cmd.extend(extra)

    print(f"[BackendLogger] writing logs to {log_path}")
    print("[BackendLogger] command:", " ".join(cmd))

    # Run uvicorn and tee to file with timestamps
    with log_path.open("a", buffering=1, encoding="utf-8") as f:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=os.environ.copy(),
        )
        try:
            for line in proc.stdout:  # type: ignore[attr-defined]
                ts_line = f"{dt.datetime.now().isoformat(timespec='milliseconds')} {line.rstrip()}\n"
                sys.stdout.write(ts_line)
                f.write(ts_line)
        except KeyboardInterrupt:
            print("\n[BackendLogger] Interrupted, terminating uvicorn…")
            proc.terminate()
        finally:
            try:
                proc.wait(timeout=10)
            except Exception:
                proc.kill()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

