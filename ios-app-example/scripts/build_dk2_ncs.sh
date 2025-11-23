#!/usr/bin/env bash
set -euo pipefail

# Run the DK2 build inside the Nordic NCS v2.9.0 toolchain shell using --command.
# Usage:
#   bash scripts/build_dk2_ncs.sh
#
# This avoids having to manually run:
#   nrfutil toolchain-manager launch --ncs-version v2.9.0 --shell

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

echo "Launching NCS v2.9.0 toolchain to run scripts/build_dk2.sh..."

nrfutil toolchain-manager launch \
  --ncs-version v2.9.0 \
  --chdir "$REPO_ROOT" \
  -- bash scripts/build_dk2.sh

echo "DK2 build via NCS toolchain completed. Packaging DFU ZIP..."

# Run the DFU packaging step outside the NCS shell, using the lm env's adafruit-nrfutil
bash "$REPO_ROOT/scripts/package_dk2_dfu.sh"

echo "DK2 DFU ZIP packaging completed."
