#!/usr/bin/env bash
set -euo pipefail

# Build Omi DevKit2 (Seeed XIAO nRF52840 Sense) firmware using Zephyr/NCS
# Requires: run inside the Nordic Toolchain Manager shell (nrfutil ... --shell)

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
# Prefer root firmware unless missing; fallback to OmiReference mirror
if [ -f "$REPO_ROOT/firmware/devkit/CMakeLists.txt" ]; then
  APP_DIR="$REPO_ROOT/firmware/devkit"
else
  APP_DIR="$REPO_ROOT/OmiReference/omi/firmware/devkit"
fi
CONF_FILE="$APP_DIR/prj_xiao_ble_sense_devkitv2-adafruit.conf"
OVERLAY_FILE="$APP_DIR/overlay/xiao_ble_sense_devkitv2-adafruit.overlay"
WS_DIR="$REPO_ROOT/firmware/zephyr-workspace"
BUILD_DIR="$WS_DIR/build-dk2"

mkdir -p "$WS_DIR" "$BUILD_DIR"

echo "Building DK2 firmware..."
cd "$WS_DIR"

# -s (source/app), -d (build dir)
west build -p auto -b xiao_ble_sense -s "$APP_DIR" -d "$BUILD_DIR" -- \
  -DCONF_FILE="$CONF_FILE" \
  -DDTC_OVERLAY_FILE="$OVERLAY_FILE"

echo
echo "Build complete. Artifacts:"
echo "  HEX: $BUILD_DIR/zephyr/zephyr.hex"
echo "  BIN: $BUILD_DIR/zephyr/zephyr.bin"
echo
echo "To flash via UF2: double-tap reset on DK2 to mount XIAO-SENSE, then run scripts/flash_dk2_uf2.sh"
