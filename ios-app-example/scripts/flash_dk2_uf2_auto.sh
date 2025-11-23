#!/usr/bin/env bash
set -euo pipefail

# Auto-enter UF2 bootloader (1200 bps touch) and copy UF2.
# Usage:
#   scripts/flash_dk2_uf2_auto.sh [--port /dev/cu.usbmodemXXXX] [--uf2 path]

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
UF2_DEFAULT="$REPO_ROOT/firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2"
PORT=""
UF2="$UF2_DEFAULT"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      PORT="$2"; shift 2 ;;
    --uf2)
      UF2="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [ ! -f "$UF2" ]; then
  echo "UF2 not found: $UF2"
  echo "Build first or pass --uf2 path to an existing UF2."
  exit 1
fi

PY_SCRIPT="$REPO_ROOT/scripts/auto_flash_uf2.py"
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found in PATH."
  exit 1
fi

set -x
if [ -n "$PORT" ]; then
  python3 "$PY_SCRIPT" --port "$PORT" --uf2 "$UF2"
else
  python3 "$PY_SCRIPT" --uf2 "$UF2"
fi
set +x

echo "Done. If the device rebooted, the new firmware should now advertise."

