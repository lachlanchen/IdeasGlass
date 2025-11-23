# LightMind iOS App

A lightweight SwiftUI iOS app that pairs with the Seeed Studio XIAO nRF52840 Sense ("LightMind" wearable) over Bluetooth Low Energy. It scans for the Nordic UART service, connects, subscribes to notifications, and exposes a "ping/pong" workflow for round-trip latency checks.

## Features
- CoreBluetooth central manager with configurable service/characteristic UUIDs (`BluetoothProfile.swift`).
- On-device log that highlights radio state, authorization, inbound/outbound packets, and latency measurements.
- Background-safe scanning (auto stops after 12s) and reconnect helpers.
- Pre-generated universal app icons and accent colors so the target can build immediately.

## Requirements
- Xcode 15 or newer
- iOS 15+ device (Bluetooth permissions required)
- A signed Seeed Studio XIAO nRF52840 Sense firmware that exposes the Nordic UART service, or adjust the UUIDs in `BluetoothProfile.swift`.

## Building & Deploying
1. Open `apps/ios/LightMind/LightMind.xcodeproj` in Xcode.
2. Select the `LightMind` target and set your `Team` and, if needed, update `Bundle Identifier` under **Signing & Capabilities**.
3. Plug in your iPhone, trust the Mac, and pick it as the run destination.
4. Tap **Run** (⌘R). The first build may prompt for Bluetooth permissions on-device.
5. In the app, tap **Scan** to discover the LightMind wearable. Hit **Connect** to pair, type a payload (defaults to `ping`), and tap **Send Ping** to write to the device. Replies that arrive on the notify characteristic are shown as `RX` entries with computed round-trip time.

### Deploying with a Free Apple ID
1. **Add your Apple ID to Xcode:** `Xcode › Settings › Accounts › + › Apple ID`. Select your personal team when prompted.
2. **Enable signing:** In the LightMind target's Signing & Capabilities tab, ensure “Automatically manage signing” is on and the bundle identifier is unique (e.g., `com.<you>.LightMind`).
3. **Connect and trust your iPhone:** Plug it in via USB, unlock it, and tap **Trust** when iOS asks.
4. **Enable Developer Mode (iOS 16+):** After the first deploy attempt, go to `Settings › Privacy & Security › Developer Mode`, toggle it on, and reboot if requested.
5. **Run the app:** Choose your iPhone in Xcode’s device picker and press ⌘R. If iOS shows an “Untrusted Developer” warning (older OS versions), approve it under `Settings › General › VPN & Device Management`.
6. **Rebuild weekly:** Free provisioning certificates expire every 7 days—just rerun from Xcode to refresh the signature.

> **Note:** I cannot push directly to your physical iPhone from this environment. After opening the project in Xcode locally, follow the steps above to deploy.

## Customizing the Bluetooth Profile
Edit `BluetoothProfile.swift` if your firmware advertises custom UUIDs. For dual-characteristic designs (write+notify), update the three constants accordingly. If your device echoes back on the same characteristic you write to, point both UUIDs at the same value.

## Next Steps
- Wire additional characteristics (battery level, IMU streaming, etc.) by extending `BLEManager`.
- Gate sensitive commands behind explicit pairing / bonding requirements if your firmware enforces MITM protection.
- Add automated UI tests inside a new `LightMindUITests` target if you need regression coverage.
