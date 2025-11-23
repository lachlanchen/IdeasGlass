#!/usr/bin/env bash
set -euo pipefail

# Package the latest DK2 build into a Nordic Legacy DFU ZIP and copy it to dist/.
# Requires:
#   - DK2 firmware built via scripts/build_dk2.sh
#   - adafruit-nrfutil on PATH (e.g. in your lm env or .venv)

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

HEX="$REPO_ROOT/firmware/zephyr-workspace/build-dk2/zephyr/zephyr.hex"
CONF_FILE="$REPO_ROOT/firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf"
DIST_DIR="$REPO_ROOT/dist/firmware"

if [ ! -f "$HEX" ]; then
  echo "ERROR: $HEX not found."
  echo "Run scripts/build_dk2.sh inside the Nordic toolchain shell first."
  exit 1
fi

if [ ! -f "$CONF_FILE" ]; then
  echo "ERROR: Kconfig file not found at $CONF_FILE"
  exit 1
fi

# Derive firmware version from CONFIG_BT_DIS_FW_REV_STR to keep ZIP naming in sync.
VERSION=$(grep -E '^CONFIG_BT_DIS_FW_REV_STR=' "$CONF_FILE" | sed -E 's/.*"([^"]+)".*/\1/' || true)
if [ -z "$VERSION" ]; then
  echo "WARNING: Could not parse CONFIG_BT_DIS_FW_REV_STR; falling back to 'unknown'."
  VERSION="unknown"
fi

ZIP_PATH="$DIST_DIR/lightmind-dk2-${VERSION}.zip"

mkdir -p "$DIST_DIR"

# Prefer the adafruit-nrfutil installed in the lm conda env, but fall back to PATH.
LM_NRFUTIL="/Users/lachlanchen/miniconda3/envs/lm/bin/adafruit-nrfutil"
if [ -x "$LM_NRFUTIL" ]; then
  NRFUTIL="$LM_NRFUTIL"
else
  NRFUTIL="adafruit-nrfutil"
fi

echo "Packaging DK2 DFU ZIP..."
echo "  HEX:   $HEX"
echo "  ZIP:   $ZIP_PATH"
echo "  VER:   $VERSION"

"$NRFUTIL" dfu genpkg \
  --dev-type 0x52 \
  --dev-revision 0xFFFF \
  --sd-req 0xFFFE \
  --application "$HEX" \
  "$ZIP_PATH"

echo
echo "DFU package created:"
echo "  $ZIP_PATH"
