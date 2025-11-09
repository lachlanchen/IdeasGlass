#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>
#include <esp_camera.h>
#include <Adafruit_BNO08x.h>
#include <Adafruit_VEML7700.h>
#include <Adafruit_DRV2605.h>
#include <driver/i2s.h>
#include <algorithm>
#include <cstring>

#include "config.h"
#if __has_include("wifi_credentials.h")
#include "wifi_credentials.h"
#elif __has_include("wifi_credentials.example.h")
#warning "wifi_credentials.h not found. Falling back to wifi_credentials.example.h"
#include "wifi_credentials.example.h"
#else
#error "wifi_credentials.h missing. Copy wifi_credentials.example.h to wifi_credentials.h and set your SSID/passwords."
#endif

// Camera pin map for Seeed XIAO ESP32S3 Sense
#define PWDN_GPIO_NUM -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 10
#define SIOD_GPIO_NUM 40
#define SIOC_GPIO_NUM 39
#define Y9_GPIO_NUM 48
#define Y8_GPIO_NUM 11
#define Y7_GPIO_NUM 12
#define Y6_GPIO_NUM 14
#define Y5_GPIO_NUM 16
#define Y4_GPIO_NUM 18
#define Y3_GPIO_NUM 17
#define Y2_GPIO_NUM 15
#define VSYNC_GPIO_NUM 38
#define HREF_GPIO_NUM 47
#define PCLK_GPIO_NUM 13

// ---------------------------------------------------------------------------
// Globals
// ---------------------------------------------------------------------------
WiFiMulti wifiMulti;
Adafruit_BNO08x bno08x(-1);
Adafruit_VEML7700 veml7700;
Adafruit_DRV2605 drv;

BLEServer *bleServer = nullptr;
BLECharacteristic *telemetryChar = nullptr;
BLECharacteristic *commandChar = nullptr;
BLECharacteristic *photoChar = nullptr;

bool bleConnected = false;
bool captureRequested = false;
bool buttonPressed = false;
bool powerOffInitiated = false;
unsigned long buttonDownAt = 0;
bool imuReady = false;
bool ambientReady = false;
bool hapticsReady = false;
bool audioReady = false;

unsigned long lastTelemetryMs = 0;
unsigned long lastBatteryMs = 0;
unsigned long lastPhotoMs = 0;
unsigned long photoIntervalMs = kPhotoIntervalMs;

float latestQuat[4] = {0, 0, 0, 1};
float latestAccel[3] = {0, 0, 0};
float latestAmbientLux = -1.0f;
float latestMicLevel = 0.0f;
uint8_t batteryPercent = 0;
float batteryVoltage = 0.0f;

// ---------------------------------------------------------------------------
// Utility structs
// ---------------------------------------------------------------------------
struct PhotoMeta {
    String id;
    size_t size;
    uint32_t crc32;
};

struct TelemetryFrame {
    uint32_t timestamp;
    float batteryVoltage;
    uint8_t batteryPercent;
    float ambientLux;
    float micLevel;
    bool buttonState;
    float quat[4];
    float accel[3];
};

// ---------------------------------------------------------------------------
// Forward declarations
// ---------------------------------------------------------------------------
void setupCamera();
void setupWiFi();
void setupBLE();
void setupIMU();
void setupAmbientSensor();
void setupAudio();
void setupHaptics();
void readIMU();
void updateBattery();
void publishTelemetry();
void handleCommands(const std::string &payload);
void ensureWiFi();
void postTelemetryToBackend(const TelemetryFrame &frame, const PhotoMeta *photo);
PhotoMeta captureAndStreamPhoto();
float readAmbientLight();
float readMicLevel();
uint32_t calculateCRC32(const uint8_t *data, size_t len);

// ---------------------------------------------------------------------------
// BLE Callbacks
// ---------------------------------------------------------------------------
class ServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer *server) override
    {
        bleConnected = true;
    }

    void onDisconnect(BLEServer *server) override
    {
        bleConnected = false;
        server->startAdvertising();
    }
};

class CommandCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *characteristic) override
    {
        std::string payload = characteristic->getValue();
        if (!payload.empty()) {
            handleCommands(payload);
        }
    }
};

// ---------------------------------------------------------------------------
void setup()
{
    Serial.begin(115200);
    delay(200);

    pinMode(PIN_STATUS_LED, OUTPUT);
    digitalWrite(PIN_STATUS_LED, HIGH); // off (active low LED)

    pinMode(PIN_BUTTON, INPUT_PULLUP);
    analogSetPinAttenuation(PIN_BATTERY_ADC, ADC_11db);

    // Require a long press to fully boot; otherwise enter deep sleep
    // This implements: long press to start the device (not to start streaming)
    auto goDeepSleep = []() {
        // Minimal shutdown before sleep
        WiFi.disconnect(true);
        WiFi.mode(WIFI_OFF);
        // Wake on button low (PIN_BUTTON must be RTC-capable on your board)
        esp_sleep_enable_ext0_wakeup(PIN_BUTTON, 0);
        Serial.println("[IdeasGlass] Deep sleep. Hold button to start.");
        delay(50);
        esp_deep_sleep_start();
    };

    if (digitalRead(PIN_BUTTON) == LOW) {
        unsigned long t0 = millis();
        while (digitalRead(PIN_BUTTON) == LOW) {
            if (millis() - t0 >= LONG_PRESS_BOOT_MS) break;
            delay(10);
        }
        if (millis() - t0 < LONG_PRESS_BOOT_MS) {
            goDeepSleep();
        }
    } else {
        // No press at power-up → stay in deep sleep until user holds the button
        goDeepSleep();
    }

    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, 400000);

    setupCamera();
    setupIMU();
    setupAmbientSensor();
    setupAudio();
    setupHaptics();
    setupBLE();
    setupWiFi();

    Serial.println("[IdeasGlass] Boot complete");
}

// ---------------------------------------------------------------------------
void loop()
{
    unsigned long now = millis();

    // Button: short press triggers a capture; long press powers off to deep sleep
    int btn = digitalRead(PIN_BUTTON);
    if (btn == LOW && !buttonPressed) {
        buttonPressed = true;
        buttonDownAt = now;
        captureRequested = true; // preserve original behavior
    } else if (btn == LOW && buttonPressed) {
        unsigned long held = now - buttonDownAt;
        if (!powerOffInitiated && held >= LONG_PRESS_OFF_MS) {
            powerOffInitiated = true;
            if (hapticsReady) { drv.setWaveform(0, 7); drv.setWaveform(1, 0); drv.go(); }
            delay(120);
            WiFi.disconnect(true);
            WiFi.mode(WIFI_OFF);
            Serial.println("[IdeasGlass] Entering deep sleep (hold to start)");
            esp_sleep_enable_ext0_wakeup(PIN_BUTTON, 0);
            esp_deep_sleep_start();
        }
    } else if (btn == HIGH && buttonPressed) {
        buttonPressed = false;
    }

    if (now - lastTelemetryMs >= kTelemetryIntervalMs) {
        readIMU();
        latestAmbientLux = readAmbientLight();
        latestMicLevel = readMicLevel();
        publishTelemetry();
        lastTelemetryMs = now;
    }

    if (now - lastBatteryMs >= kBatterySampleIntervalMs) {
        updateBattery();
        lastBatteryMs = now;
    }

    bool dueForPhoto = now - lastPhotoMs >= photoIntervalMs;
    if (captureRequested || dueForPhoto) {
        PhotoMeta meta = captureAndStreamPhoto();
        if (meta.size > 0) {
            TelemetryFrame frame{
                .timestamp = (uint32_t)(millis() / 1000),
                .batteryVoltage = batteryVoltage,
                .batteryPercent = batteryPercent,
                .ambientLux = latestAmbientLux,
                .micLevel = latestMicLevel,
                .buttonState = buttonPressed,
                .quat = {latestQuat[0], latestQuat[1], latestQuat[2], latestQuat[3]},
                .accel = {latestAccel[0], latestAccel[1], latestAccel[2]},
            };
            postTelemetryToBackend(frame, &meta);
        }
        captureRequested = false;
        lastPhotoMs = now;
    }

    ensureWiFi();
    delay(5);
}

// ---------------------------------------------------------------------------
void setupCamera()
{
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 6000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 25;
    config.fb_count = 2;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_LATEST;

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("[IdeasGlass] Camera init failed: 0x%x\n", err);
    }
}

// ---------------------------------------------------------------------------
void setupIMU()
{
    if (!bno08x.begin_I2C()) {
        Serial.println("[IdeasGlass] BNO08X not detected");
        return;
    }
    bno08x.enableReport(SH2_ARVR_STABILIZED_RV, 5000);
    bno08x.enableReport(SH2_ACCELEROMETER, 5000);
    imuReady = true;
}

// ---------------------------------------------------------------------------
void setupAmbientSensor()
{
    if (veml7700.begin()) {
        veml7700.setGain(VEML7700_GAIN_1_8);
        veml7700.setIntegrationTime(VEML7700_IT_100MS);
        ambientReady = true;
    } else {
        Serial.println("[IdeasGlass] VEML7700 not detected - ambient lux disabled");
    }
}

// ---------------------------------------------------------------------------
void setupAudio()
{
    i2s_config_t config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = 16000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = 128,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0,
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = PIN_MIC_SCK,
        .ws_io_num = PIN_MIC_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = PIN_MIC_SD,
        .mck_io_num = I2S_PIN_NO_CHANGE,
    };

    if (i2s_driver_install(I2S_NUM_0, &config, 0, nullptr) == ESP_OK) {
        i2s_set_pin(I2S_NUM_0, &pin_config);
        audioReady = true;
    } else {
        Serial.println("[IdeasGlass] I2S init failed");
    }
}

// ---------------------------------------------------------------------------
void setupHaptics()
{
    if (drv.begin()) {
        drv.selectLibrary(1);
        drv.setMode(DRV2605_MODE_INTTRIG);
        hapticsReady = true;
    } else {
        Serial.println("[IdeasGlass] DRV2605 not detected");
    }
}

// ---------------------------------------------------------------------------
void setupWiFi()
{
    WiFi.mode(WIFI_MODE_STA);
    WiFi.setSleep(true);
    for (size_t i = 0; i < WIFI_NETWORK_COUNT; ++i) {
        wifiMulti.addAP(WIFI_NETWORKS[i].ssid, WIFI_NETWORKS[i].password);
    }
    ensureWiFi();
}

// ---------------------------------------------------------------------------
void ensureWiFi()
{
    static unsigned long lastAttempt = 0;
    if (WiFi.status() == WL_CONNECTED)
        return;

    unsigned long now = millis();
    if (now - lastAttempt < 10'000)
        return;

    lastAttempt = now;
    wl_status_t status = wifiMulti.run();
    Serial.printf("[IdeasGlass] WiFi status: %d\n", status);
}

// ---------------------------------------------------------------------------
void setupBLE()
{
    BLEDevice::init(kDeviceName);
    BLEDevice::setPower(ESP_PWR_LVL_P0);

    bleServer = BLEDevice::createServer();
    bleServer->setCallbacks(new ServerCallbacks());

    BLEService *service = bleServer->createService(kBleServiceUuid);
    telemetryChar = service->createCharacteristic(kBleTelemetryCharUuid, BLECharacteristic::PROPERTY_NOTIFY);
    telemetryChar->addDescriptor(new BLE2902());

    commandChar = service->createCharacteristic(kBleCommandCharUuid, BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_WRITE_NR);
    commandChar->setCallbacks(new CommandCallbacks());

    photoChar = service->createCharacteristic(kBlePhotoCharUuid, BLECharacteristic::PROPERTY_NOTIFY);
    photoChar->addDescriptor(new BLE2902());

    service->start();

    BLEAdvertising *advertising = BLEDevice::getAdvertising();
    advertising->addServiceUUID(kBleServiceUuid);
    advertising->setScanResponse(true);
    advertising->start();
}

// ---------------------------------------------------------------------------
void readIMU()
{
    if (!imuReady)
        return;
    sh2_SensorValue_t sensorValue;
    while (bno08x.getSensorEvent(&sensorValue)) {
        switch (sensorValue.sensorId) {
        case SH2_ARVR_STABILIZED_RV:
            latestQuat[0] = sensorValue.un.arvrStabilizedRV.real;
            latestQuat[1] = sensorValue.un.arvrStabilizedRV.i;
            latestQuat[2] = sensorValue.un.arvrStabilizedRV.j;
            latestQuat[3] = sensorValue.un.arvrStabilizedRV.k;
            break;
        case SH2_ACCELEROMETER:
            latestAccel[0] = sensorValue.un.accelerometer.x;
            latestAccel[1] = sensorValue.un.accelerometer.y;
            latestAccel[2] = sensorValue.un.accelerometer.z;
            break;
        default:
            break;
        }
    }
}

// ---------------------------------------------------------------------------
float readAmbientLight()
{
    if (!ambientReady)
        return -1.0f;
    return veml7700.readLux();
}

// ---------------------------------------------------------------------------
float readMicLevel()
{
    if (!audioReady)
        return 0.0f;
    const size_t samples = 128;
    int32_t buffer[samples];
    size_t bytesRead = 0;
    if (i2s_read(I2S_NUM_0, buffer, sizeof(buffer), &bytesRead, 10) != ESP_OK || bytesRead == 0) {
        return 0.0f;
    }

    uint32_t count = bytesRead / sizeof(int32_t);
    double sum = 0;
    for (uint32_t i = 0; i < count; ++i) {
        const double sample = buffer[i] / 2147483648.0; // normalize 32-bit
        sum += sample * sample;
    }
    double rms = sqrt(sum / count);
    return (float)rms;
}

// ---------------------------------------------------------------------------
void updateBattery()
{
    uint16_t raw = analogRead(PIN_BATTERY_ADC);
    float voltage = (raw / 4095.0f) * 3.3f * kVoltageDividerRatio;
    batteryVoltage = voltage;
    float percent = (voltage - kBatteryMinVoltage) / (kBatteryMaxVoltage - kBatteryMinVoltage);
    percent = constrain(percent, 0.0f, 1.0f);
    batteryPercent = (uint8_t)(percent * 100);
}

// ---------------------------------------------------------------------------
TelemetryFrame buildTelemetryFrame()
{
    TelemetryFrame frame;
    frame.timestamp = (uint32_t)(millis() / 1000);
    frame.batteryVoltage = batteryVoltage;
    frame.batteryPercent = batteryPercent;
    frame.ambientLux = latestAmbientLux;
    frame.micLevel = latestMicLevel;
    frame.buttonState = buttonPressed;
    memcpy(frame.quat, latestQuat, sizeof(latestQuat));
    memcpy(frame.accel, latestAccel, sizeof(latestAccel));
    return frame;
}

// ---------------------------------------------------------------------------
void publishTelemetry()
{
    TelemetryFrame frame = buildTelemetryFrame();

    StaticJsonDocument<384> doc;
    doc["ts"] = frame.timestamp;
    doc["battery"] = frame.batteryPercent;
    doc["voltage"] = frame.batteryVoltage;
    doc["ambient_lux"] = frame.ambientLux;
    doc["mic"] = frame.micLevel;
    doc["button"] = frame.buttonState;

    JsonArray quat = doc.createNestedArray("quat");
    for (int i = 0; i < 4; ++i)
        quat.add(frame.quat[i]);

    JsonArray accel = doc.createNestedArray("accel");
    for (int i = 0; i < 3; ++i)
        accel.add(frame.accel[i]);

    char payload[400];
    size_t len = serializeJson(doc, payload);

    if (bleConnected && telemetryChar) {
        telemetryChar->setValue((uint8_t *)payload, len);
        telemetryChar->notify();
    }

    postTelemetryToBackend(frame, nullptr);
}

// ---------------------------------------------------------------------------
PhotoMeta captureAndStreamPhoto()
{
    PhotoMeta meta{.id = "", .size = 0, .crc32 = 0};
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("[IdeasGlass] Camera capture failed");
        return meta;
    }

    meta.size = fb->len;
    meta.crc32 = calculateCRC32(fb->buf, fb->len);
    meta.id = String("pic-") + String((uint32_t)(millis() / 1000));

    if (bleConnected && photoChar) {
        const size_t chunk = 480;
        size_t sent = 0;
        while (sent < fb->len) {
            size_t n = std::min(chunk, fb->len - sent);
            photoChar->setValue(fb->buf + sent, n);
            photoChar->notify();
            sent += n;
            delay(5);
        }
    }

    esp_camera_fb_return(fb);
    return meta;
}

// ---------------------------------------------------------------------------
void handleCommands(const std::string &payload)
{
    StaticJsonDocument<256> doc;
    auto err = deserializeJson(doc, payload);
    if (err) {
        Serial.println("[IdeasGlass] Failed to parse BLE command");
        return;
    }

    const char *type = doc["type"] | "";
    if (strcmp(type, "capture_photo") == 0) {
        captureRequested = true;
    } else if (strcmp(type, "haptic") == 0) {
        if (hapticsReady) {
            uint8_t effect = doc["effect"] | 1;
            drv.setWaveform(0, effect);
            drv.setWaveform(1, 0);
            drv.go();
        }
    } else if (strcmp(type, "set_interval") == 0) {
        unsigned long interval = doc["ms"] | kPhotoIntervalMs;
        // Guard against unrealistic values
        if (interval >= 5'000 && interval <= 120'000) {
            photoIntervalMs = interval;
            Serial.printf("[IdeasGlass] Photo interval override: %lu\n", interval);
        }
    }
}

// ---------------------------------------------------------------------------
void postTelemetryToBackend(const TelemetryFrame &frame, const PhotoMeta *photo)
{
    if (WiFi.status() != WL_CONNECTED)
        return;

    HTTPClient http;
    String url = String("http://") + kBackendHost + ":" + String(kBackendPort) + kBackendIngestPath;
    if (!http.begin(url)) {
        Serial.println("[IdeasGlass] HTTP init failed");
        return;
    }
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Device-Secret", kBackendApiKey);

    StaticJsonDocument<512> doc;
    doc["device_id"] = kHardwareRevision;
    doc["ts"] = frame.timestamp;
    doc["battery"] = frame.batteryPercent;
    doc["voltage"] = frame.batteryVoltage;
    doc["ambient_lux"] = frame.ambientLux;
    doc["mic_level"] = frame.micLevel;
    doc["button"] = frame.buttonState;

    JsonArray quat = doc.createNestedArray("quat");
    for (float value : frame.quat)
        quat.add(value);

    JsonArray accel = doc.createNestedArray("accel");
    for (float value : frame.accel)
        accel.add(value);

    if (photo) {
        JsonObject photoObj = doc.createNestedObject("photo");
        photoObj["id"] = photo->id;
        photoObj["size"] = photo->size;
        photoObj["crc32"] = photo->crc32;
    }

    String body;
    serializeJson(doc, body);

    int code = http.POST(body);
    Serial.printf("[IdeasGlass] POST %s -> %d\n", url.c_str(), code);
    http.end();
}

// ---------------------------------------------------------------------------
uint32_t calculateCRC32(const uint8_t *data, size_t len)
{
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; ++i) {
        uint8_t byte = data[i];
        crc ^= byte;
        for (uint8_t j = 0; j < 8; ++j) {
            uint32_t mask = -(crc & 1u);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
    }
    return ~crc;
}
