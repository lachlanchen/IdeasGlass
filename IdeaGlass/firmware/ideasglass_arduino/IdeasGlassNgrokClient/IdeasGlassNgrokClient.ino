#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <algorithm>
#include "esp_camera.h"
#include "mbedtls/base64.h"
#include <math.h>
#include <ESP_I2S.h>
#include "esp_system.h"
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>
#include <freertos/task.h>
#include "../config.h"

#if __has_include("../wifi_credentials.h")
#include "../wifi_credentials.h"
#elif __has_include("../wifi_credentials.example.h")
#warning "wifi_credentials.h not found. Falling back to wifi_credentials.example.h"
#include "../wifi_credentials.example.h"
#else
#error "wifi_credentials.h missing. Copy wifi_credentials.example.h to wifi_credentials.h next to config.h."
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
// Server configuration
// ---------------------------------------------------------------------------
const char *kServerHost = "ideas.lazying.art";
const uint16_t kServerPort = 443;
const char *kDeviceId = "ideasglass-devkit-01";
#define ENABLE_PHOTO_CAPTURE 1
const char *kAudioWsPath = "/ws/audio-ingest";
const int AUDIO_SAMPLE_RATE = 16000;
const size_t AUDIO_BLOCK_SAMPLES = 4096;
static int16_t g_audioBlock[AUDIO_BLOCK_SAMPLES];
size_t g_bufferedSamples = 0;
uint32_t g_audioChunkCounter = 0;
const size_t AUDIO_QUEUE_LENGTH = 6;
const size_t AUDIO_SENDER_STACK = 8192;

struct AudioPacket
{
    int16_t *samples = nullptr;
    size_t sampleCount = 0;
    float rms = 0.0f;
    uint32_t sequence = 0;
};

// LetsEncrypt chain for ideas.lazying.art (PEM)
static const char ideas_cert[] PROGMEM = R"(-----BEGIN CERTIFICATE-----
MIIDjzCCAxagAwIBAgISBQs7pCvOLRNhX4aYR3+lDJdHMAoGCCqGSM49BAMDMDIx
CzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQDEwJF
NzAeFw0yNTExMDgwNjQxMzdaFw0yNjAyMDYwNjQxMzZaMBwxGjAYBgNVBAMTEWlk
ZWFzLmxhenlpbmcuYXJ0MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEFyLml4as
x7t3v0YVRn2ow+H1oAjxY5m24Ncweh9hZVyE2QaLGxszgnyGkVgvf+xZcuh1HN7U
7aT1QO5juDK1VaOCAiAwggIcMA4GA1UdDwEB/wQEAwIHgDAdBgNVHSUEFjAUBggr
BgEFBQcDAQYIKwYBBQUHAwIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQUJYtWOMkl
cH2M98D5X7MuqR1qVzMwHwYDVR0jBBgwFoAUrkie3IcdRKBv2qLlYHQEeMKcAIAw
MgYIKwYBBQUHAQEEJjAkMCIGCCsGAQUFBzAChhZodHRwOi8vZTcuaS5sZW5jci5v
cmcvMBwGA1UdEQQVMBOCEWlkZWFzLmxhenlpbmcuYXJ0MBMGA1UdIAQMMAowCAYG
Z4EMAQIBMC0GA1UdHwQmMCQwIqAgoB6GHGh0dHA6Ly9lNy5jLmxlbmNyLm9yZy83
Mi5jcmwwggEFBgorBgEEAdZ5AgQCBIH2BIHzAPEAdwBJnJtp3h187Pw23s2HZKa4
W68Kh4AZ0VVS++nrKd34wwAAAZpiaIEhAAAEAwBIMEYCIQCIq/Mx+dtdHua+xGJu
s8/uPsTOD1aPjnQSGGt9aMwG2AIhALrIe4VFo0yz05+M8ET38nz9+L/q5VormES0
javdlHsqAHYAGYbUxyiqb/66A294Kk0BkarOLXIxD67OXXBBLSVMx9QAAAGaYmiB
IAAABAMARzBFAiBjmKpW0cSfwa5f5S9G/q6ciWkTE8E349T2MiQdn5RRvwIhANJ4
7rLSn4tryfHp2uF4uCLQZs1NHzYH7oA3fC09J+7FMAoGCCqGSM49BAMDA2cAMGQC
MB1gkKlhEEXTIv3lTncn/7yN/uwsnRSeX+Lx8GvTvjQUKQ3eUezpqC9C22Vhk7d+
DwIwdbLMUNd+qqSSMFtm9SwB4FuXdMSjvA6ZahjYIODpEPTjCf1xfNgYCZSBkSaH
+zpn
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIEVzCCAj+gAwIBAgIRAKp18eYrjwoiCWbTi7/UuqEwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMjQwMzEzMDAwMDAw
WhcNMjcwMzEyMjM1OTU5WjAyMQswCQYDVQQGEwJVUzEWMBQGA1UEChMNTGV0J3Mg
RW5jcnlwdDELMAkGA1UEAxMCRTcwdjAQBgcqhkjOPQIBBgUrgQQAIgNiAARB6AST
CFh/vjcwDMCgQer+VtqEkz7JANurZxLP+U9TCeioL6sp5Z8VRvRbYk4P1INBmbef
QHJFHCxcSjKmwtvGBWpl/9ra8HW0QDsUaJW2qOJqceJ0ZVFT3hbUHifBM/2jgfgw
gfUwDgYDVR0PAQH/BAQDAgGGMB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEFBQcD
ATASBgNVHRMBAf8ECDAGAQH/AgEAMB0GA1UdDgQWBBSuSJ7chx1EoG/aouVgdAR4
wpwAgDAfBgNVHSMEGDAWgBR5tFnme7bl5AFzgAiIyBpY9umbbjAyBggrBgEFBQcB
AQQmMCQwIgYIKwYBBQUHMAKGFmh0dHA6Ly94MS5pLmxlbmNyLm9yZy8wEwYDVR0g
BAwwCjAIBgZngQwBAgEwJwYDVR0fBCAwHjAcoBqgGIYWaHR0cDovL3gxLmMubGVu
Y3Iub3JnLzANBgkqhkiG9w0BAQsFAAOCAgEAjx66fDdLk5ywFn3CzA1w1qfylHUD
aEf0QZpXcJseddJGSfbUUOvbNR9N/QQ16K1lXl4VFyhmGXDT5Kdfcr0RvIIVrNxF
h4lqHtRRCP6RBRstqbZ2zURgqakn/Xip0iaQL0IdfHBZr396FgknniRYFckKORPG
yM3QKnd66gtMst8I5nkRQlAg/Jb+Gc3egIvuGKWboE1G89NTsN9LTDD3PLj0dUMr
OIuqVjLB8pEC6yk9enrlrqjXQgkLEYhXzq7dLafv5Vkig6Gl0nuuqjqfp0Q1bi1o
yVNAlXe6aUXw92CcghC9bNsKEO1+M52YY5+ofIXlS/SEQbvVYYBLZ5yeiglV6t3S
M6H+vTG0aP9YHzLn/KVOHzGQfXDP7qM5tkf+7diZe7o2fw6O7IvN6fsQXEQQj8TJ
UXJxv2/uJhcuy/tSDgXwHM8Uk34WNbRT7zGTGkQRX0gsbjAea/jYAoWv0ZvQRwpq
Pe79D/i7Cep8qWnA+7AE/3B3S/3dEEYmc0lpe1366A/6GEgk3ktr9PEoQrLChs6I
tu3wnNLB2euC8IKGLQFpGtOO/2/hiAKjyajaBP25w1jF0Wl8Bbqne3uZ2q1GyPFJ
YRmT7/OXpmOH/FVLtwS+8ng1cAmpCujPwteJZNcDG0sF2n/sc0+SQf49fdyUK0ty
+VUwFj9tmWxyR/M=
-----END CERTIFICATE-----)";

WiFiClientSecure secure_client;
bool cameraReady = false;
framesize_t cameraFrameSize = FRAMESIZE_QQVGA;
const size_t AUDIO_TEMP_SAMPLES = 512;
static int16_t g_audioTemp[AUDIO_TEMP_SAMPLES];
static I2SClass pdmI2S;
bool audioInitialized = false;
static QueueHandle_t g_audioQueue = nullptr;
static TaskHandle_t g_audioSenderHandle = nullptr;

void initAudioStreamer();
void audioSenderTask(void *param);
#if ENABLE_PHOTO_CAPTURE
static TaskHandle_t g_photoTaskHandle = nullptr;
void startPhotoTask();
void photoTask(void *param);
struct PhotoUploadJob
{
    String message;
    String rssi;
    String photoBase64;
};
static QueueHandle_t g_photoUploadQueue = nullptr;
static TaskHandle_t g_photoUploadTaskHandle = nullptr;
void startPhotoUploadTask();
void photoUploadTask(void *param);
bool enqueuePhotoUploadJob(const String &message, const String &rssi, const String &photoBase64);
#endif

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

bool initCamera()
{
    if (!psramFound()) {
        Serial.println("[Camera] PSRAM not detected. Enable PSRAM in Tools > PSRAM to capture photos.");
        return false;
    }

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
    config.fb_count = 2;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_LATEST;
    config.frame_size = FRAMESIZE_QQVGA;
    framesize_t priorities[] = {FRAMESIZE_QQVGA};
    int qualities[] = {34};

    for (size_t idx = 0; idx < sizeof(priorities) / sizeof(priorities[0]); ++idx) {
        config.frame_size = priorities[idx];
        config.jpeg_quality = qualities[idx];
        esp_err_t err = esp_camera_init(&config);
        if (err == ESP_OK) {
            cameraFrameSize = priorities[idx];
            sensor_t *s = esp_camera_sensor_get();
            if (s) {
                s->set_framesize(s, priorities[idx]);
                s->set_quality(s, qualities[idx]);
                s->set_vflip(s, 1);    // device is worn upside down
                s->set_hmirror(s, 1);  // mirror for natural POV
            }
            Serial.printf("[Camera] Ready (framesize=%d quality=%d)\n", priorities[idx], qualities[idx]);
            return true;
        }
        Serial.printf("[Camera] init failed for framesize %d (0x%x), retrying smaller frame...\n", priorities[idx], err);
        esp_camera_deinit();
        delay(200);
    }

    Serial.println("[Camera] Unable to initialize camera with available memory.");
    return false;
}

bool encodeBase64(const uint8_t *data, size_t length, String &outString)
{
    size_t encoded_len = 4 * ((length + 2) / 3) + 1;
    unsigned char *encoded = (unsigned char *)malloc(encoded_len);
    if (!encoded) {
        Serial.println("[Base64] Out of memory");
        return false;
    }
    size_t actual_len = 0;
    int result = mbedtls_base64_encode(encoded, encoded_len, &actual_len, data, length);
    if (result != 0) {
        free(encoded);
        Serial.printf("[Base64] encode failed: %d\n", result);
        return false;
    }
    encoded[actual_len] = '\0';
    outString = String((char *)encoded);
    free(encoded);
    return true;
}

class SimpleWebSocketClient
{
public:
    void begin(const char *host, uint16_t port, const char *path, const char *caCert)
    {
        _host = host;
        _port = port;
        _path = path;
        if (caCert) {
            _client.setCACert(caCert);
        }
        _client.setTimeout(8000);
        close();
    }

    bool ensureConnected()
    {
        if (_connected && _client.connected()) {
            return true;
        }
        close();
        if (!_client.connect(_host, _port)) {
            return false;
        }
        if (!handshake()) {
            close();
            return false;
        }
        _connected = true;
        return true;
    }

    bool sendText(const String &payload)
    {
        if (!ensureConnected()) {
            return false;
        }
        if (!writeFrame(payload)) {
            close();
            return false;
        }
        return true;
    }

    void close()
    {
        if (_client.connected()) {
            _client.stop();
        }
        _connected = false;
    }

private:
    bool handshake()
    {
        uint8_t randomKey[16];
        for (size_t i = 0; i < sizeof(randomKey); ++i) {
            randomKey[i] = static_cast<uint8_t>(esp_random() & 0xFF);
        }
        String key;
        if (!encodeBase64(randomKey, sizeof(randomKey), key)) {
            return false;
        }
        _client.printf(
            "GET %s HTTP/1.1\r\n"
            "Host: %s\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "Sec-WebSocket-Key: %s\r\n"
            "Sec-WebSocket-Protocol: ideasglass-audio\r\n\r\n",
            _path,
            _host,
            key.c_str());
        String status = _client.readStringUntil('\n');
        if (!status.startsWith("HTTP/1.1 101")) {
            return false;
        }
        unsigned long start = millis();
        while (_client.connected() && millis() - start < 2000) {
            String line = _client.readStringUntil('\n');
            if (line.length() == 0 || line == "\r") {
                break;
            }
        }
        return true;
    }

    bool writeFrame(const String &payload)
    {
        const size_t len = payload.length();
        if (len == 0) {
            return true;
        }
        uint8_t header[14];
        size_t headerLen = 0;
        header[0] = 0x81;
        if (len <= 125) {
            header[1] = 0x80 | static_cast<uint8_t>(len);
            headerLen = 2;
        } else if (len <= 65535) {
            header[1] = 0x80 | 126;
            header[2] = (len >> 8) & 0xFF;
            header[3] = len & 0xFF;
            headerLen = 4;
        } else {
            header[1] = 0x80 | 127;
            for (int i = 0; i < 8; ++i) {
                header[2 + i] = (len >> ((7 - i) * 8)) & 0xFF;
            }
            headerLen = 10;
        }
        uint8_t mask[4];
        for (int i = 0; i < 4; ++i) {
            mask[i] = static_cast<uint8_t>(esp_random() & 0xFF);
        }
        memcpy(header + headerLen, mask, 4);
        headerLen += 4;
        if (_client.write(header, headerLen) != headerLen) {
            return false;
        }
        uint8_t buffer[256];
        size_t offset = 0;
        while (offset < len) {
            size_t chunk = std::min(sizeof(buffer), len - offset);
            for (size_t i = 0; i < chunk; ++i) {
                buffer[i] = payload[offset + i] ^ mask[(offset + i) % 4];
            }
            if (_client.write(buffer, chunk) != chunk) {
                return false;
            }
            offset += chunk;
        }
        return true;
    }

    WiFiClientSecure _client;
    const char *_host = nullptr;
    const char *_path = nullptr;
    uint16_t _port = 0;
    bool _connected = false;
};

static SimpleWebSocketClient g_audioWsClient;

bool capturePhotoBase64(String &outBase64)
{
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("[Camera] Failed to capture frame");
        esp_camera_deinit();
        cameraReady = false;
        vTaskDelay(pdMS_TO_TICKS(50));
        return false;
    }
    bool ok = encodeBase64(fb->buf, fb->len, outBase64);
    esp_camera_fb_return(fb);
    if (ok) {
        Serial.printf("[Camera] Captured photo (%u bytes)\n", fb->len);
        return true;
    }
    Serial.println("[Camera] Failed to encode frame, resetting camera");
    esp_camera_deinit();
    cameraReady = false;
    vTaskDelay(pdMS_TO_TICKS(50));
    return false;
}

#if ENABLE_PHOTO_CAPTURE
void photoTask(void *param)
{
    const TickType_t delayTicks = pdMS_TO_TICKS(kPhotoIntervalMs);
    TickType_t lastWake = xTaskGetTickCount();
    while (true) {
        if (WiFi.status() == WL_CONNECTED) {
            String payload = "Hello from IdeasGlass @ " + String(millis() / 1000) + "s";
            String photoBase64;
            if (!cameraReady) {
                Serial.println("[Photo] Camera offline, attempting reinit...");
                cameraReady = initCamera();
                if (!cameraReady) {
                    Serial.println("[Photo] Camera reinit failed, will retry next interval");
                }
            }
            if (cameraReady && capturePhotoBase64(photoBase64)) {
                Serial.printf("[Photo] Captured %u bytes\n", photoBase64.length());
            } else if (!cameraReady) {
                Serial.println("[Photo] Camera not ready, skipping capture");
            } else {
                Serial.println("[Photo] Capture failed, sending text-only heartbeat");
            }
            String rssi = String(WiFi.RSSI());
            if (!enqueuePhotoUploadJob(payload, rssi, photoBase64)) {
                Serial.println("[Photo] Upload queue full or unavailable, dropping frame");
            }
        }
        vTaskDelayUntil(&lastWake, delayTicks);
    }
}

void startPhotoTask()
{
    if (g_photoTaskHandle == nullptr) {
        BaseType_t ok = xTaskCreatePinnedToCore(photoTask, "PhotoTask", 8192, nullptr, 1, &g_photoTaskHandle, 1);
        if (ok != pdPASS) {
            Serial.println("[Photo] Failed to start photo task");
            g_photoTaskHandle = nullptr;
        }
    }
}

bool enqueuePhotoUploadJob(const String &message, const String &rssi, const String &photoBase64)
{
    if (!g_photoUploadQueue) {
        return false;
    }
    auto *job = new PhotoUploadJob{message, rssi, photoBase64};
    if (xQueueSend(g_photoUploadQueue, &job, 0) != pdPASS) {
        delete job;
        return false;
    }
    return true;
}

void photoUploadTask(void *param)
{
    while (true) {
        PhotoUploadJob *job = nullptr;
        if (xQueueReceive(g_photoUploadQueue, &job, portMAX_DELAY) != pdPASS || !job) {
            continue;
        }
        const String *photoPtr = job->photoBase64.length() > 0 ? &job->photoBase64 : nullptr;
        bool ok = sendPayload(job->message, job->rssi, photoPtr);
        Serial.printf("[PhotoUpload] send result: %s (%d chars)\n", ok ? "OK" : "FAILED", photoPtr ? photoPtr->length() : 0);
        delete job;
    }
}

void startPhotoUploadTask()
{
    if (g_photoUploadTaskHandle == nullptr) {
        BaseType_t ok = xTaskCreatePinnedToCore(photoUploadTask, "PhotoUploadTask", 8192, nullptr, 1, &g_photoUploadTaskHandle, 1);
        if (ok != pdPASS) {
            Serial.println("[Photo] Failed to start photo upload task");
            g_photoUploadTaskHandle = nullptr;
        }
    }
}
#endif

void setupAudio()
{
    pdmI2S.setPinsPdmRx(PIN_MIC_SCK, PIN_MIC_SD);
    if (!pdmI2S.begin(I2S_MODE_PDM_RX, AUDIO_SAMPLE_RATE, I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO)) {
        Serial.println("[Audio] Failed to init PDM RX");
        return;
    }
    if (!pdmI2S.configureRX(AUDIO_SAMPLE_RATE, I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO, I2S_RX_TRANSFORM_NONE)) {
        Serial.println("[Audio] Failed to configure PDM RX");
        return;
    }
    audioInitialized = true;
    initAudioStreamer();
    Serial.println("[Audio] PDM microphone ready");
}

float computeRms(const int16_t *samples, size_t count)
{
    double sum = 0.0;
    for (size_t i = 0; i < count; ++i) {
        double norm = samples[i] / 32768.0;
        sum += norm * norm;
    }
    return sqrt(sum / count);
}

bool sendAudioChunkPacket(const AudioPacket &packet)
{
    if (!packet.samples || packet.sampleCount == 0) {
        return false;
    }
    if (!WiFi.isConnected()) {
        g_audioWsClient.close();
        return false;
    }
    if (!g_audioWsClient.ensureConnected()) {
        return false;
    }

    String encoded;
    const size_t byteCount = packet.sampleCount * sizeof(int16_t);
    if (!encodeBase64(reinterpret_cast<const uint8_t *>(packet.samples), byteCount, encoded)) {
        Serial.println("[Audio] Failed to encode PCM16 chunk");
        return false;
    }

    const uint32_t durationMs = (packet.sampleCount * 1000) / AUDIO_SAMPLE_RATE;
    String body = String("{\"device_id\":\"") + kDeviceId + "\","
                   "\"sample_rate\":" + AUDIO_SAMPLE_RATE + ","
                   "\"bits_per_sample\":16,"
                   "\"duration_ms\":" + durationMs + ","
                   "\"rms\":" + String(packet.rms, 4) + ","
                   "\"audio_base64\":\"" + encoded + "\"}";

    return g_audioWsClient.sendText(body);
}

void audioSenderTask(void *param)
{
    AudioPacket packet;
    while (true) {
        if (g_audioQueue && xQueueReceive(g_audioQueue, &packet, portMAX_DELAY) == pdTRUE) {
            bool ok = sendAudioChunkPacket(packet);
            Serial.printf("[Audio] chunk #%u %s (rms=%.3f)\n", packet.sequence, ok ? "sent" : "FAILED", packet.rms);
            if (packet.samples) {
                free(packet.samples);
                packet.samples = nullptr;
            }
            vTaskDelay(pdMS_TO_TICKS(5));
        } else {
            vTaskDelay(pdMS_TO_TICKS(20));
        }
    }
}

void initAudioStreamer()
{
    if (g_audioQueue) {
        return;
    }
    g_audioQueue = xQueueCreate(AUDIO_QUEUE_LENGTH, sizeof(AudioPacket));
    if (!g_audioQueue) {
        Serial.println("[Audio] Failed to allocate audio queue");
        return;
    }
    g_audioWsClient.begin(kServerHost, kServerPort, kAudioWsPath, ideas_cert);
    BaseType_t ok = xTaskCreatePinnedToCore(audioSenderTask, "AudioSender", AUDIO_SENDER_STACK, nullptr, 1, &g_audioSenderHandle, 0);
    if (ok != pdPASS) {
        Serial.println("[Audio] Failed to start audio sender task");
    }
}

void handleAudioStreaming()
{
    if (!audioInitialized)
        return;

    size_t bytesRead = pdmI2S.readBytes(reinterpret_cast<char *>(g_audioTemp), sizeof(g_audioTemp));
    if (bytesRead == 0) {
        return;
    }
    size_t samplesRead = bytesRead / sizeof(int16_t);
    for (size_t i = 0; i < samplesRead; ++i) {
        if (g_bufferedSamples < AUDIO_BLOCK_SAMPLES) {
            g_audioBlock[g_bufferedSamples++] = g_audioTemp[i];
        } else {
            break;
        }
    }

    if (g_bufferedSamples >= AUDIO_BLOCK_SAMPLES) {
        float rms = computeRms(g_audioBlock, g_bufferedSamples);
        uint32_t chunkIndex = g_audioChunkCounter++;
        int16_t peak = 0;
        for (size_t i = 0; i < g_bufferedSamples; ++i) {
            int16_t sample = g_audioBlock[i];
            int16_t absVal = sample >= 0 ? sample : -sample;
            if (absVal > peak) {
                peak = absVal;
            }
        }
        if (chunkIndex < 4 || peak == 0 || (chunkIndex % 25 == 0)) {
            Serial.printf("[Audio] chunk #%u stats: peak=%d rms=%.4f first=%d samples=%u\n",
                          chunkIndex,
                          peak,
                          rms,
                          g_audioBlock[0],
                          (unsigned)g_bufferedSamples);
        }
        if (!g_audioQueue) {
            Serial.println("[Audio] Queue not ready, dropping audio chunk");
            g_bufferedSamples = 0;
            return;
        }
        int16_t *chunkCopy = (int16_t *)malloc(g_bufferedSamples * sizeof(int16_t));
        if (!chunkCopy) {
            Serial.println("[Audio] Out of memory allocating audio chunk");
            g_bufferedSamples = 0;
            return;
        }
        memcpy(chunkCopy, g_audioBlock, g_bufferedSamples * sizeof(int16_t));
        AudioPacket packet;
        packet.samples = chunkCopy;
        packet.sampleCount = g_bufferedSamples;
        packet.rms = rms;
        packet.sequence = chunkIndex;
        if (xQueueSend(g_audioQueue, &packet, 0) != pdTRUE) {
            Serial.println("[Audio] Send queue full, dropping chunk");
            free(chunkCopy);
        }
        g_bufferedSamples = 0;
    }
}

void connectToWiFi()
{
    Serial.println("[WiFi] Connecting...");
    g_audioWsClient.close();
    for (size_t i = 0; i < WIFI_NETWORK_COUNT; ++i) {
        const auto &cred = WIFI_NETWORKS[i];
        Serial.printf(" -> SSID %s\n", cred.ssid);
        WiFi.begin(cred.ssid, cred.password);
        unsigned long start = millis();
        while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
            Serial.print(".");
            delay(400);
        }
        if (WiFi.status() == WL_CONNECTED) {
            Serial.printf("\n[WiFi] Connected (%s, RSSI %d)\n", WiFi.SSID().c_str(), WiFi.RSSI());
            Serial.printf("IP: %s\n", WiFi.localIP().toString().c_str());
            return;
        }
        Serial.println("\n[WiFi] Failed, trying next credential...");
    }
}

bool sendPayload(const String &message, const String &metaValue, const String *photoBase64)
{
    WiFiClientSecure messageClient;
    messageClient.setCACert(ideas_cert);
    messageClient.setTimeout(15000);

    Serial.printf("[HTTP] Connecting to %s:%u ...\n", kServerHost, kServerPort);
    if (!messageClient.connect(kServerHost, kServerPort)) {
        Serial.println("[HTTP] Connection failed");
        return false;
    }

    String body = String("{\"device_id\":\"") + kDeviceId + "\","
                   "\"message\":\"" + message + "\","
                   "\"meta\":{\"rssi\":\"" + metaValue + "\"}";
    if (photoBase64 && photoBase64->length() > 0) {
        body += ",\"photo_base64\":\"" + *photoBase64 + "\",\"photo_mime\":\"image/jpeg\"";
    }
    body += "}";

    messageClient.printf(
        "POST /api/v1/messages HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n",
        kServerHost,
        body.length());
    messageClient.print(body);

    String response = messageClient.readString();
    Serial.println("[HTTP] Response:");
    Serial.println(response);
    messageClient.stop();
    return response.indexOf("200") != -1;
}

// ---------------------------------------------------------------------------
// Arduino lifecycle
// ---------------------------------------------------------------------------

void setup()
{
    Serial.begin(115200);
    delay(200);

    Serial.println("\nIdeasGlass Ngrok Client");
    Serial.printf("Device ID: %s\n", kDeviceId);
    Serial.printf("Chip MAC: %s\n", WiFi.macAddress().c_str());

    WiFi.mode(WIFI_MODE_STA);
    WiFi.setSleep(true);
    connectToWiFi();

#if ENABLE_PHOTO_CAPTURE
    cameraReady = initCamera();
#endif
    setupAudio();
#if ENABLE_PHOTO_CAPTURE
    if (!g_photoUploadQueue) {
        g_photoUploadQueue = xQueueCreate(4, sizeof(PhotoUploadJob *));
        if (!g_photoUploadQueue) {
            Serial.println("[Photo] Failed to create upload queue");
        }
    }
    if (g_photoUploadQueue) {
        startPhotoUploadTask();
        startPhotoTask();
    }
#endif
}

void loop()
{
    if (WiFi.status() != WL_CONNECTED) {
        connectToWiFi();
        delay(2000);
        return;
    }

    handleAudioStreaming();
}
