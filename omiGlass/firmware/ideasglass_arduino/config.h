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

// ---------------------------------------------------------------------------
// Pins (Seeed XIAO ESP32S3 Sense)
// ---------------------------------------------------------------------------
constexpr gpio_num_t PIN_STATUS_LED = GPIO_NUM_21;
constexpr gpio_num_t PIN_BUTTON = GPIO_NUM_1;
constexpr gpio_num_t PIN_BATTERY_ADC = GPIO_NUM_2;

constexpr gpio_num_t PIN_I2C_SDA = GPIO_NUM_41;
constexpr gpio_num_t PIN_I2C_SCL = GPIO_NUM_40;

constexpr gpio_num_t PIN_MIC_SCK = GPIO_NUM_7;
constexpr gpio_num_t PIN_MIC_WS = GPIO_NUM_8;
constexpr gpio_num_t PIN_MIC_SD = GPIO_NUM_9;

constexpr gpio_num_t PIN_HAPTIC_INT = GPIO_NUM_6;

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
constexpr unsigned long kPhotoIntervalMs = 30'000;

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
