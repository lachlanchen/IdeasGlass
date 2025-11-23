# Omi DevKit2 (Seeed XIAO nRF52840 Sense)
# Rename Bluetooth device + add unique ID and flash via UF2

This note explains how to change the BLE device name shown on iOS/Android to “LightMind Link 2”, attach a short unique ID to the name (or expose it via GATT), and re‑flash the DevKit2 over USB using the UF2 bootloader.

Applies to: DevKit2 firmware in `OmiReference/omi/firmware/devkit` (Zephyr RTOS on nRF52840, Seeed XIAO nRF52840 Sense).

---

## 1) Where the name comes from today

- The advertising data includes the GAP name via `BT_DATA_NAME_COMPLETE`.
- In Zephyr, the name is sourced from `CONFIG_BT_DEVICE_NAME` (Kconfig) unless you change it at runtime with `bt_set_name()`.
- In the DevKit2 firmware, the advertising payload is built in `transport.c`:

```
// transport.c (simplified)
static const struct bt_data bt_ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA(BT_DATA_UUID128_ALL, audio_service_uuid.val, sizeof(audio_service_uuid.val)),
    BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};
```

You will often also see DIS (Device Information Service) enabled; its strings come from Kconfig (`CONFIG_BT_DIS_*`).

---

## 2) Easiest static rename (no code changes)

If a fixed name is sufficient:

1) Open the DevKit2 Kconfig overlay you build with (for example):
   - `OmiReference/omi/firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf`
2) Add or change:

```
CONFIG_BT_DEVICE_NAME="LightMind Link 2"
CONFIG_BT_DEVICE_NAME_MAX=32
```

3) (Optional) Set DIS fields for UI/device management:
```
CONFIG_BT_DIS_MANUF="LightMind"
CONFIG_BT_DIS_MODEL="Link 2"
CONFIG_BT_DIS_SERIAL_NUMBER="lightmind-link-2-0000"   # can be refined later
```

4) Rebuild and flash (see section 5).

Pros: trivial; Cons: no per‑unit uniqueness in the name.

---

## 3) Add a short unique ID suffix to the name (dynamic)

To display something like `LightMind Link 2-ABCD`, compute a short ID from the BLE identity or SoC ID and update the GAP name and advertising at boot.

1) In `transport.c`, add a helper to compute a 4‑hex suffix from the device identity address:

```
#include <zephyr/bluetooth/hci.h>

static void lm_short_id(char out[5]) {
    bt_addr_le_t addrs[CONFIG_BT_ID_MAX];
    size_t cnt = bt_id_get(addrs, ARRAY_SIZE(addrs));
    uint16_t tail = 0x0000;
    if (cnt > 0) {
        const bt_addr_t *a = &addrs[0].a;
        // last two bytes of address
        tail = ((uint16_t)a->val[1] << 8) | a->val[0];
    }
    snprintf(out, 5, "%04X", tail);
}
```

2) Build a dynamic name at initialization and publish it:

```
static char adv_name[32];

static void lm_update_adv_name(void) {
    char suffix[5];
    lm_short_id(suffix);
    snprintk(adv_name, sizeof(adv_name), "LightMind Link 2-%s", suffix);

    /* Update GAP name (GATT Device Name) */
    bt_set_name(adv_name);

    /* Update advertising payload to include the dynamic name */
    struct bt_data ad[] = {
        BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
        BT_DATA(BT_DATA_UUID128_ALL, audio_service_uuid.val, sizeof(audio_service_uuid.val)),
        BT_DATA(BT_DATA_NAME_COMPLETE, adv_name, (uint8_t)strlen(adv_name)),
    };
    extern const struct bt_data bt_sd[]; /* keep your original scan response */
    bt_le_adv_update_data(ad, ARRAY_SIZE(ad), bt_sd, ARRAY_SIZE(bt_sd));
}
```

3) Call `lm_update_adv_name()` once BLE is enabled (e.g., after `bt_enable()` and before starting advertising).

Notes:
- This appends a short stable suffix. By default Zephyr uses a static random address across boots, so the suffix is device‑stable.
- iOS doesn’t expose MAC addresses to apps, but this logic runs on the firmware.

### Alternative/extra: expose a full unique ID over GATT

- Use DIS Serial Number (simple) by setting `CONFIG_BT_DIS_SERIAL_NUMBER` at build time.
- For a dynamic runtime ID:
  - Add a custom “LightMind Info” service with a `Device UUID` characteristic that returns a 36‑char UUID or a 64‑char hex.
  - The iOS app can read/cache this and show “Device: Name (abcd1234)”.

---

## 4) Show device in iOS app (current behavior)

- We already display the GAP name, and we persist `CBPeripheral.identifier` (an app‑stable UUID) for auto‑reconnect and UI.
- With the dynamic suffix above, the list will show: `LightMind Link 2-ABCD`.
- Optionally, read DIS Serial Number or your custom characteristic to display a longer ID.

---

## 5) Quick flash prebuilt DK2 v2.0.10 (USB/UF2)

- As of now, the latest DK2 firmware in releases is: Omi DK2 v2.0.10 (asset: `Omi_DK2_v2.0.10.uf2`).
- Steps:
  1) Double‑tap the reset button → mount `/Volumes/XIAO-SENSE` (macOS) or a new USB drive (Windows).
  2) Drag‑drop `Omi_DK2_v2.0.10.uf2` onto the drive.
  3) The drive auto‑ejects and the device reboots.

If you need to update the bootloader first, flash the `bootloader*.uf2`, re‑enter DFU, then flash the app UF2.

---

## 6) Build and flash your own UF2 (USB)

DevKit2 uses the Seeed XIAO nRF52840 Sense UF2 bootloader.

A) One‑time toolchain (Zephyr):
- Install nRF Connect SDK/Zephyr and West, or use the Omi project’s documented build container/scripts.

B) Build:

```
# From the Omi firmware root
west init -l .
west update

# Example board + config (adjust to your project structure)
west build -p auto -b seeed_xiao_blesense firmware/omi/firmware/devkit \
  -DOVERLAY_CONFIG=firmware/omi/firmware/devkit/prj_xiao_ble_sense_devkitv2-adafruit.conf

# Output: build/zephyr/zephyr.hex (and zephyr.bin)
```

C) Convert HEX→UF2 (if your build doesn’t already emit UF2):

```
# Use uf2conv.py (Adafruit UF2 tool) — family ID for nRF52840 is 0xADA52840
python3 uf2conv.py -c -o app.uf2 -f 0xADA52840 build/zephyr/zephyr.hex
```

D) Flash via UF2:
- Connect USB‑C to the DevKit2.
- Double‑tap the reset button; a drive named `/Volumes/XIAO-SENSE` appears (macOS). On Windows, a new mass‑storage device.
- Drag‑drop `app.uf2` onto the drive.
- The drive auto‑ejects; the device reboots into your new firmware.

Tips:
- If you also need to update the bootloader: drag the provided `bootloader‑*.uf2` first, re‑enter UF2 mode, then flash your firmware UF2.
- If the OS shows “transfer incomplete”, wait ~30 s; the device may still be finishing the update.

---

## 7) Verifying on iOS

- After flashing, restart the LightMind app.
- The scan list and the header should show `LightMind Link 2‑ABCD`.
- The status page can also display `Device: <name> (<short id>)`; the app persists `CBPeripheral.identifier` for auto‑reconnect.

---

## 8) Rollback

- Keep a copy of the last known‑good UF2; re‑enter UF2 mode and drag it back to restore.

---

## 9) Summary

- Static rename: set `CONFIG_BT_DEVICE_NAME="LightMind Link 2"` and rebuild.
- Unique ID suffix: compute from BLE identity; call `bt_set_name()` and `bt_le_adv_update_data()` to publish `LightMind Link 2‑ABCD`.
- Optional: expose a longer device UUID via DIS Serial Number or a custom GATT characteristic.
- Flash by UF2: double‑tap reset → copy `*.uf2`.
