#!/usr/bin/env bash
set -euo pipefail

# Flash DK2 via UF2 runner (requires device in UF2 mode mounted as mass storage)

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
WS_DIR="$REPO_ROOT/firmware/zephyr-workspace"
BUILD_DIR="$WS_DIR/build-dk2"

if [ ! -d "$BUILD_DIR/zephyr" ]; then
  echo "Build directory not found: $BUILD_DIR/zephyr"
  echo "Run scripts/build_dk2.sh first."
  exit 1
fi

echo "Ensure the DK2 is in UF2 mode (double-tap reset; XIAO-SENSE drive mounted)."
read -p "Press Enter to continue and flash..."

cd "$WS_DIR"
west flash -d "$BUILD_DIR" --runner uf2

echo "Flashing requested. If the drive disappears, the device is rebooting into the new firmware."

