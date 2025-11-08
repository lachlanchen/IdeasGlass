#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "esp_camera.h"
#include "mbedtls/base64.h"
#include "esp32/spiram.h"

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
const unsigned long kSendIntervalMs = 30000;

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

bool capturePhotoBase64(String &outBase64)
{
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("[Camera] Failed to capture frame");
        return false;
    }
    size_t encoded_len = 4 * ((fb->len + 2) / 3) + 1;
    unsigned char *encoded = (unsigned char *)malloc(encoded_len);
    if (!encoded) {
        esp_camera_fb_return(fb);
        Serial.println("[Camera] Out of memory");
        return false;
    }
    size_t actual_len = 0;
    int result = mbedtls_base64_encode(encoded, encoded_len, &actual_len, fb->buf, fb->len);
    esp_camera_fb_return(fb);
    if (result != 0) {
        free(encoded);
        Serial.printf("[Camera] Base64 encode failed: %d\n", result);
        return false;
    }
    encoded[actual_len] = '\0';
    outBase64 = String((char *)encoded);
    free(encoded);
    Serial.printf("[Camera] Captured photo (%u bytes, %u base64)\n", fb->len, actual_len);
    return true;
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

    cameraReady = initCamera();
}

void loop()
{
    if (WiFi.status() != WL_CONNECTED) {
        connectToWiFi();
        delay(2000);
        return;
    }

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

    delay(100);
}
