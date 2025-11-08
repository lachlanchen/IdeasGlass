#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "esp_camera.h"
#include "mbedtls/base64.h"
#include <math.h>
#include "driver/i2s.h"

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
#define ENABLE_PHOTO_CAPTURE 0
const unsigned long kSendIntervalMs = 30000;
const int AUDIO_SAMPLE_RATE = 16000;
const size_t AUDIO_BLOCK_SAMPLES = 4096;
static int16_t g_audioBlock[AUDIO_BLOCK_SAMPLES];
size_t g_bufferedSamples = 0;
uint32_t g_audioChunkCounter = 0;

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
unsigned long lastSend = 0;
bool cameraReady = false;
framesize_t cameraFrameSize = FRAMESIZE_QVGA;
const size_t AUDIO_TEMP_SAMPLES = 512;
static int16_t g_audioTemp[AUDIO_TEMP_SAMPLES];
bool audioInitialized = false;

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
    config.xclk_freq_hz = 10000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    config.frame_size = FRAMESIZE_QVGA;
    framesize_t priorities[] = {FRAMESIZE_QVGA, FRAMESIZE_QQVGA};
    int qualities[] = {22, 24};

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

bool capturePhotoBase64(String &outBase64)
{
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("[Camera] Failed to capture frame");
        return false;
    }
    bool ok = encodeBase64(fb->buf, fb->len, outBase64);
    esp_camera_fb_return(fb);
    if (ok) {
        Serial.printf("[Camera] Captured photo (%u bytes)\n", fb->len);
    }
    return ok;
}

void setupAudio()
{
    i2s_config_t config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = AUDIO_SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 256,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0,
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = 7,
        .ws_io_num = 8,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = 9,
        .mck_io_num = I2S_PIN_NO_CHANGE,
    };

    if (i2s_driver_install(I2S_NUM_0, &config, 0, nullptr) != ESP_OK) {
        Serial.println("[Audio] Failed to install I2S driver");
        return;
    }
    if (i2s_set_pin(I2S_NUM_0, &pin_config) != ESP_OK) {
        Serial.println("[Audio] Failed to set I2S pins");
        return;
    }
    i2s_zero_dma_buffer(I2S_NUM_0);
    audioInitialized = true;
    Serial.println("[Audio] I2S microphone ready");
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

bool sendAudioChunk(const String &encoded, float rms)
{
    if (!WiFi.isConnected())
        return false;

    secure_client.setCACert(ideas_cert);
    if (!secure_client.connect(kServerHost, kServerPort)) {
        Serial.println("[Audio] HTTPS connect failed");
        return false;
    }

    const uint32_t durationMs = (AUDIO_BLOCK_SAMPLES * 1000) / AUDIO_SAMPLE_RATE;
    String body = String("{\"device_id\":\"") + kDeviceId + "\","
                   "\"sample_rate\":" + AUDIO_SAMPLE_RATE + ","
                   "\"bits_per_sample\":16,"
                   "\"duration_ms\":" + durationMs + ","
                   "\"rms\":" + String(rms, 4) + ","
                   "\"audio_base64\":\"" + encoded + "\"}";

    secure_client.printf(
        "POST /api/v1/audio HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n",
        kServerHost,
        body.length());
    secure_client.print(body);

    String response = secure_client.readString();
    secure_client.stop();
    bool ok = response.indexOf("200") != -1;
    Serial.printf("[Audio] chunk #%u %s (rms=%.3f)\n", g_audioChunkCounter++, ok ? "sent" : "FAILED", rms);
    return ok;
}

void handleAudioStreaming()
{
    if (!audioInitialized)
        return;

    size_t bytesRead = 0;
    if (i2s_read(I2S_NUM_0, g_audioTemp, sizeof(g_audioTemp), &bytesRead, 1) != ESP_OK) {
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
        String encoded;
        if (encodeBase64(reinterpret_cast<uint8_t *>(g_audioBlock), g_bufferedSamples * sizeof(int16_t), encoded)) {
            sendAudioChunk(encoded, rms);
        }
        g_bufferedSamples = 0;
    }
}

void connectToWiFi()
{
    Serial.println("[WiFi] Connecting...");
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
    secure_client.setCACert(ideas_cert);
    secure_client.setTimeout(15000);

    Serial.printf("[HTTP] Connecting to %s:%u ...\n", kServerHost, kServerPort);
    if (!secure_client.connect(kServerHost, kServerPort)) {
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

    secure_client.printf(
        "POST /api/v1/messages HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n",
        kServerHost,
        body.length());
    secure_client.print(body);

    String response = secure_client.readString();
    Serial.println("[HTTP] Response:");
    Serial.println(response);
    secure_client.stop();
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
}

void loop()
{
    if (WiFi.status() != WL_CONNECTED) {
        connectToWiFi();
        delay(2000);
        return;
    }

#if ENABLE_PHOTO_CAPTURE
    if (millis() - lastSend > kSendIntervalMs) {
        String payload = "Hello from IdeasGlass @ " + String(millis() / 1000) + "s";
        String photoBase64;
        String *photoPtr = nullptr;
        if (cameraReady && capturePhotoBase64(photoBase64)) {
            photoPtr = &photoBase64;
        }
        bool ok = sendPayload(payload, String(WiFi.RSSI()), photoPtr);
        Serial.printf("[HTTP] send result: %s\n", ok ? "OK" : "FAILED");
        lastSend = millis();
    }
#endif

    handleAudioStreaming();
}
