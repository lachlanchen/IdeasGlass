#pragma once

#include <Arduino.h>

// ---------------------------------------------------------------------------
// Device identity
// ---------------------------------------------------------------------------
constexpr char kDeviceName[] = "IdeasGlass";
constexpr char kFirmwareVersion[] = "0.1.0-dev";
constexpr char kHardwareRevision[] = "arduino-xiao-sense";

// ---------------------------------------------------------------------------
// BLE UUIDs (UART-like service + control + photo stream)
// ---------------------------------------------------------------------------
constexpr char kBleServiceUuid[] = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E";
constexpr char kBleTelemetryCharUuid[] = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E";
constexpr char kBleCommandCharUuid[] = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E";
constexpr char kBlePhotoCharUuid[] = "19B10005-E8F2-537E-4F6C-D104768A1214";
// BLE pairing mode configuration
#ifndef ENABLE_BLE_PAIRING
#define ENABLE_BLE_PAIRING 0
#endif
constexpr uint32_t kBlePairingAdvertiseMs = 120000; // auto-stop adverts after 2 min
constexpr bool kBleStopAdvertiseOnConnect = true;    // stop advertising while connected

// ---------------------------------------------------------------------------
// Pins (Seeed XIAO ESP32S3 Sense)
// ---------------------------------------------------------------------------
constexpr gpio_num_t PIN_STATUS_LED = GPIO_NUM_21;
constexpr gpio_num_t PIN_BUTTON = GPIO_NUM_1;
constexpr gpio_num_t PIN_BATTERY_ADC = GPIO_NUM_2;

constexpr gpio_num_t PIN_I2C_SDA = GPIO_NUM_41;
constexpr gpio_num_t PIN_I2C_SCL = GPIO_NUM_40;

// Sense expansion board routes the on-board PDM microphone to IO42 (CLK) and IO41 (DATA)
constexpr gpio_num_t PIN_MIC_SCK = GPIO_NUM_42;
constexpr gpio_num_t PIN_MIC_WS = GPIO_NUM_42;  // reused for compatibility, unused in PDM mode
constexpr gpio_num_t PIN_MIC_SD = GPIO_NUM_41;

constexpr gpio_num_t PIN_HAPTIC_INT = GPIO_NUM_6;

// Long-press UX (milliseconds)
constexpr uint32_t LONG_PRESS_BOOT_MS = 800;   // hold on boot to continue startup
constexpr uint32_t LONG_PRESS_OFF_MS  = 2500;  // hold during run to enter deep sleep

// Require hold-to-start on boot? Set to true for wearable UX, false for dev/charging.
constexpr bool REQUIRE_LONG_PRESS_ON_BOOT = false;

// ---------------------------------------------------------------------------
// Battery sensing
// ---------------------------------------------------------------------------
constexpr float kBatteryMaxVoltage = 4.2f;
constexpr float kBatteryMinVoltage = 3.2f;
constexpr float kVoltageDividerRatio = 6.086f;
constexpr unsigned long kBatterySampleIntervalMs = 30'000;

// ---------------------------------------------------------------------------
// Capture cadence
// ---------------------------------------------------------------------------
constexpr unsigned long kTelemetryIntervalMs = 2'000;
constexpr unsigned long kPhotoIntervalMs = 15'000;

// Suppress verbose audio logs on firmware (per-chunk prints)
constexpr bool kAudioLogSuppress = true;

// ---------------------------------------------------------------------------
// Optional hardening flags (off by default; enable after validation)
// ---------------------------------------------------------------------------
// Keep-Alive pooled HTTPS clients for audio/photo POST fallbacks
#ifndef IG_TUNE_HTTP_KEEPALIVE
#define IG_TUNE_HTTP_KEEPALIVE 1
#endif
// Smoothed and cached battery ADC reading (reduces ADC/CPU usage)
#ifndef IG_TUNE_BATTERY_FILTER
#define IG_TUNE_BATTERY_FILTER 1
#endif
// Lightweight periodic counters for network/path observability
#ifndef IG_TUNE_DEBUG_COUNTERS
#define IG_TUNE_DEBUG_COUNTERS 0
#endif
// Preallocate a small pool of audio buffers to reduce malloc/free churn
#ifndef IG_TUNE_PREALLOC_AUDIO
#define IG_TUNE_PREALLOC_AUDIO 1
#endif
// When audio queue is full, drop the oldest pending packet instead of the newest
#ifndef IG_TUNE_QUEUE_DROP_OLDEST
#define IG_TUNE_QUEUE_DROP_OLDEST 1
#endif
// Non-blocking WS reconnect with exponential backoff + jitter
#ifndef IG_TUNE_WS_BACKOFF
#define IG_TUNE_WS_BACKOFF 1
#endif

// ---------------------------------------------------------------------------
// Wi-Fi / Backend
// ---------------------------------------------------------------------------
constexpr char kBackendHost[] = "ideasglass.local";
constexpr uint16_t kBackendPort = 8000;
constexpr char kBackendIngestPath[] = "/api/v1/ingest";
constexpr char kBackendApiKey[] = "replace-with-device-secret";

// ---------------------------------------------------------------------------
// Helper macros
// ---------------------------------------------------------------------------
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))
