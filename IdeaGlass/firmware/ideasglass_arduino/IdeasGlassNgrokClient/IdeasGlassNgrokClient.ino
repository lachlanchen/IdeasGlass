#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>

#if __has_include("../wifi_credentials.h")
#include "../wifi_credentials.h"
#elif __has_include("../wifi_credentials.example.h")
#warning "wifi_credentials.h not found. Falling back to wifi_credentials.example.h"
#include "../wifi_credentials.example.h"
#else
#error "wifi_credentials.h missing. Copy wifi_credentials.example.h to wifi_credentials.h next to config.h."
#endif

// ---------------------------------------------------------------------------
// Server configuration
// ---------------------------------------------------------------------------
const char *kServerHost = "ideas.lazying.art";
const uint16_t kServerPort = 443; // forwarded by ngrok
const char *kDeviceId = "ideasglass-devkit-01";

// LetsEncrypt cert chain for ideas.lazying.art (public). Required for TLS pinning.
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

void connectToWiFi()
{
    Serial.print("[WiFi] Connecting");
    for (size_t i = 0; i < WIFI_NETWORK_COUNT; ++i) {
        const auto &cred = WIFI_NETWORKS[i];
        Serial.printf("\n -> SSID %s\n", cred.ssid);
        WiFi.begin(cred.ssid, cred.password);

        unsigned long start = millis();
        while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
            Serial.print(".");
            delay(500);
        }

        if (WiFi.status() == WL_CONNECTED) {
            Serial.printf("\n[WiFi] Connected (%s, RSSI %d)\n", WiFi.SSID().c_str(), WiFi.RSSI());
            Serial.printf("IP: %s\n", WiFi.localIP().toString().c_str());
            return;
        }
        Serial.println("\n[WiFi] Failed, trying next credential...");
    }
}

bool sendPayload(const String &message, const String &metaValue = "")
{
    secure_client.setCACert(ideas_cert);
    secure_client.setTimeout(15000);

    Serial.printf("[HTTP] Connecting to %s:%u ...\n", kServerHost, kServerPort);
    if (!secure_client.connect(kServerHost, kServerPort)) {
        Serial.println("[HTTP] Connection failed");
        return false;
    }

    const String body = String("{\"device_id\":\"") + kDeviceId + "\","
                        "\"message\":\"" + message + "\","
                        "\"meta\":{\"signal\":\"" + metaValue + "\"}}";

    secure_client.printf(
        "POST /api/v1/messages HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n",
        kServerHost,
        body.length());
    secure_client.print(body);

    // Read response status line
    String response = secure_client.readString();
    Serial.println("[HTTP] Response:");
    Serial.println(response);
    secure_client.stop();
    return response.indexOf("200") != -1;
}

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
}

void loop()
{
    if (WiFi.status() != WL_CONNECTED) {
        connectToWiFi();
        delay(2000);
        return;
    }

    if (millis() - lastSend > 5000) {
        String payload = "Hello from IdeasGlass @ " + String(millis() / 1000) + "s";
        String meta = String(WiFi.RSSI());
        bool ok = sendPayload(payload, meta);
        Serial.printf("[HTTP] send result: %s\n", ok ? "OK" : "FAILED");
        lastSend = millis();
    }

    delay(100);
}
