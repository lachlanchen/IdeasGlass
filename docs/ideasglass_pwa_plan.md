---
title: IdeasGlass App Delivery Plan
description: Making the IdeasGlass app work across PWA / iOS / Android while syncing with the Tornado backend.
---

# Goals

1. Ship a single Flutter codebase that builds cleanly for Android, iOS, desktop, and the Flutter web target (PWA).
2. Subscribe to the new Tornado WebSocket (`/ws/devices/:id`) so captured data appears instantly in the client.
3. Capture + replay telemetry/photos using the Tornado REST API regardless of platform.

# PWA enablement (Flutter web)

1. **Manifest** – update `app/web/manifest.json` with IdeasGlass branding, theme color, and `"display": "standalone"`. Provide 192/512 icons in `app/web/icons/`.
2. **Service worker** – enable offline caching by running `flutter build web --pwa-strategy=offline-first`. This writes the `flutter-service-worker.js` file used by browsers to install the app.
3. **HTTPS** – host the Tornado API (and WebSocket) on TLS so that BLE/Web APIs remain accessible when the PWA is installed.
4. **Install prompts** – add a Flutter `InstallPromptBanner` (web only) that listens to the `beforeinstallprompt` JS event so creators can pin the IdeasGlass dashboard easily.

# BLE + data flow

- **Android/iOS** – continue to use `flutter_blue_plus` for pairing and streaming raw photos. Post telemetry to `http(s)://<tornado-host>/api/v1/ingest` with the same payload the Arduino firmware sends.
- **Web/PWA** – Web Bluetooth is experimental, so the PWA focuses on consuming the Tornado data feed. Creators can review memory reels, command the wearable, and annotate transcripts even when the glasses are not nearby.
- **Data vending** – the Tornado server forwards each ingest to the WebSocket topic so all clients (mobile + PWA) stay in sync without polling.

# Flutter integration snippet

Add `app/lib/ideasglass_sync_service.dart` (see repository) and register it with your dependency locator. Example usage:

```dart
final sync = IdeasGlassSyncService(
  baseUrl: Uri.parse('https://ideasglass.local:8081'),
  deviceId: 'ideasglass-001',
  deviceSecret: 'replace-me',
);

await sync.initialSync();      // Fetch latest telemetry list from Postgres (REST endpoint to be added)
sync.deviceStream.listen((event) {
  // Update Provider / Riverpod state with live telemetry
});
```

On the native platforms, continue to call `sync.publishTelemetry()` after every BLE transfer so the new Tornado pipeline remains the source of truth.

# iOS/Android build flags

| Platform | Key steps |
| --- | --- |
| Android | Set `android:usesCleartextTraffic="false"` in `AndroidManifest.xml` (PWA requires HTTPS). Add `INTERNET`, `BLUETOOTH_CONNECT`, `NEARBY_WIFI_DEVICES`. |
| iOS | Update `Info.plist` with `NSBluetoothAlwaysUsageDescription` + `NSBluetoothPeripheralUsageDescription`. Add Tornado domain to `NSAppTransportSecurity` `NSAllowsArbitraryLoadsInMedia`. |

# Testing matrix

1. **Hardware loop** – run the Arduino firmware + Flutter Android build + Tornado API locally (`flutter run -d android`, `python backend/tornado_app/main.py`).
2. **Web install** – `flutter run -d chrome --web-renderer canvaskit`, install the PWA, and verify WebSocket updates.
3. **Offline** – disconnect network; confirm cached shell loads and displays last received telemetry.

Once those steps pass, the IdeasGlass experience will feel identical on mobile and the installed web app, satisfying the “PWA / iOS / Android” ask.
