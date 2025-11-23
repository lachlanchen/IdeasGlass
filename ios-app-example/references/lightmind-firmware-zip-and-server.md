**Purpose**
- Package a firmware ZIP and serve it locally over HTTPS via ngrok on port 8787.
- Serves your PWA and exposes simple API endpoints to build and list downloadable ZIPs.

**What’s Included**
- Server: `scripts/serve_pwa_and_firmware.py` (Tornado)
- Packager CLI: `scripts/package_zip.py`
- Requirements: `scripts/requirements-server.txt`

**Install**
- pip install -r scripts/requirements-server.txt

**Run the server**
- Default port: 8787 (matches your ngrok forwarder)
- Static root auto-detection order:
  1) `LightMind/pwa_app`
  2) `apps/pwa_app`
  3) `apps/lightmind/pwa_app`
  4) `OmiReference/web`
  5) Fallback simple index

Command:
- python3 scripts/serve_pwa_and_firmware.py --port 8787

Endpoints
- GET `/api/health` → { ok: true }
- GET `/api/list`   → { files: [{ name, bytes, modified, url }] }
- POST `/api/zip`   → { ok: true, zip: "/downloads/<name>.zip" }
  - Body JSON: { "source": "/full/path/to/file/or/dir", "name": "firmware.zip" }
- Static downloads: `/downloads/<file>` from `./dist`
- PWA: `/app/`

**Create a ZIP (CLI)**
- python3 scripts/package_zip.py firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2 --name lightmind-dk2-uf2.zip
- Output: `dist/lightmind-dk2-uf2.zip`

**Create a ZIP (API)**
- curl -X POST http://127.0.0.1:8787/api/zip \
  -H 'Content-Type: application/json' \
  -d '{"source":"/Users/<you>/Local/LMCognition/firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2","name":"lightmind-dk2-uf2.zip"}'
- Response includes the public path under `/downloads/...`

**Use With ngrok**
- ngrok points to `http://localhost:8787` → your public URL becomes `https://ios.lightmind.art`
- Example public download URL: `https://ios.lightmind.art/downloads/lightmind-dk2-uf2.zip`

**Important DFU Note**
- For Bluetooth DFU:
  - DK2 (nRF52840) uses Nordic Legacy DFU. The required package is a Nordic DFU ZIP (bin+dat), not a UF2.
  - CV1 (nRF5340 + MCUboot) uses MCUmgr over BLE. The required package is the build’s `dfu_application.zip` with a `manifest.json`.
- The scripts above produce a generic ZIP for hosting. Replace its contents with the proper DFU package when performing BLE updates.

**Create a Legacy DFU ZIP (DK2 – LightMind flow)**
- Prereqs:
  - Nordic NCS toolchain (for `west build`) and a working DK2 build via `scripts/build_dk2.sh`.
  - `adafruit-nrfutil` installed in the `lm` conda env.
- Recommended script:
  - `bash scripts/package_dk2_dfu.sh`
  - Inputs:
    - `firmware/zephyr-workspace/build-dk2/zephyr/zephyr.hex`
    - Version from `CONFIG_BT_DIS_FW_REV_STR` in `firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf` (e.g. `2.0.13`, `2.0.14`, `2.0.15`).
  - Output:
    - `dist/firmware/lightmind-dk2-<version>.zip`
    - Contents: `zephyr.bin`, `zephyr.dat`, `manifest.json` (Nordic Legacy DFU format, app‑only image).
- Typical public URLs via ngrok:
  - `https://ios.lightmind.art/downloads/firmware/firmware.zip` (Omi DK2 2.0.10 legacy DFU)
  - `https://ios.lightmind.art/downloads/firmware/lightmind-dk2-test-2.0.11.zip`
  - `https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.12.zip`
  - `https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.13.zip`
  - `https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.14.zip`
  - `https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.15.zip`

Notes
- The DK2 uses a Legacy DFU bootloader (AdaDFU). The generated packages use app‑only parameters (e.g. `--sd-req 0xFFFE`) that have been verified in the LightMind iOS DFU flow.
- For USB/UF2 flashing, continue to use `firmware/zephyr-workspace/build-dk2/zephyr/zephyr.uf2` or `dist/lightmind-dk2-uf2.zip`; these are independent of the DFU ZIPs used by iOS.

Notes
- The DFU ZIP uses `hw_version=52`, `app_version=2011`, `sd_req=[0x00]`. Most secure DFU bootloaders accept `sd_req=0x00` or `0xFFFE` for app‑only images. If your bootloader requires a specific SoftDevice ID, regenerate with that value.
