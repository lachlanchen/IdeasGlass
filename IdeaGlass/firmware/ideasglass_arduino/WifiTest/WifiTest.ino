#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>

#if __has_include("../wifi_credentials.h")
#include "../wifi_credentials.h"
#elif __has_include("../wifi_credentials.example.h")
#warning "wifi_credentials.h not found. Falling back to wifi_credentials.example.h"
#include "../wifi_credentials.example.h"
#else
#error "wifi_credentials.h missing. Copy wifi_credentials.example.h to wifi_credentials.h next to config.h."
#endif

WiFiMulti wifiMulti;
unsigned long lastStatusPrint = 0;

void setup()
{
    Serial.begin(115200);
    delay(200);

    Serial.println("\n[IdeasGlass WiFi Test]");
    Serial.printf("Loaded %zu WiFi credentials\n", WIFI_NETWORK_COUNT);

    WiFi.mode(WIFI_MODE_STA);
    WiFi.setSleep(true);

    for (size_t i = 0; i < WIFI_NETWORK_COUNT; ++i) {
        const auto &entry = WIFI_NETWORKS[i];
        Serial.printf(" -> adding network #%zu: %s\n", i + 1, entry.ssid);
        wifiMulti.addAP(entry.ssid, entry.password);
    }
}

void loop()
{
    wl_status_t status = static_cast<wl_status_t>(wifiMulti.run());

    if (status == WL_CONNECTED) {
        if (millis() - lastStatusPrint > 3000) {
            Serial.println("[WiFi] Connected!");
            Serial.printf("       SSID: %s\n", WiFi.SSID().c_str());
            Serial.printf("       RSSI: %d dBm\n", WiFi.RSSI());
            Serial.printf("       IP:   %s\n\n", WiFi.localIP().toString().c_str());
            lastStatusPrint = millis();
        }
    } else {
        Serial.printf("[WiFi] Not connected (status=%d). Retrying...\n", status);
        delay(2000);
    }

    delay(250);
}
