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
unsigned long lastScanMs = 0;

void printStatusReason(wl_status_t status)
{
    switch (status) {
    case WL_IDLE_STATUS:
        Serial.println("       Reason: Idle (hardware ready, no AP yet)");
        break;
    case WL_NO_SSID_AVAIL:
        Serial.println("       Reason: SSID not found (check AP visibility)");
        break;
    case WL_SCAN_COMPLETED:
        Serial.println("       Reason: Scan completed (pending connection)");
        break;
    case WL_CONNECTED:
        Serial.println("       Reason: Connected");
        break;
    case WL_CONNECT_FAILED:
        Serial.println("       Reason: Connection failed (bad password?)");
        break;
    case WL_CONNECTION_LOST:
        Serial.println("       Reason: Connection lost (AP timeout)");
        break;
    case WL_DISCONNECTED:
        Serial.println("       Reason: Disconnected (retrying)");
        break;
    default:
        Serial.println("       Reason: Unknown");
        break;
    }
}

void setup()
{
    Serial.begin(115200);
    delay(200);

    Serial.println("\n[IdeasGlass WiFi Test]");
    Serial.printf("Loaded %zu WiFi credentials\n", WIFI_NETWORK_COUNT);
    Serial.printf("Chip MAC address: %s\n", WiFi.macAddress().c_str());

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
        printStatusReason(status);
        if (millis() - lastScanMs > 10000) {
            Serial.println("       Performing a fresh scan...");
            int n = WiFi.scanNetworks(/*async=*/false, /*hidden=*/true);
            if (n <= 0) {
                Serial.println("       No networks found.");
            } else {
                Serial.printf("       %d network(s) found:\n", n);
                for (int i = 0; i < n; ++i) {
                    Serial.printf("        - %s (RSSI %d dBm, encryption %d, channel %d)\n",
                        WiFi.SSID(i).c_str(),
                        WiFi.RSSI(i),
                        WiFi.encryptionType(i),
                        WiFi.channel(i));
                }
            }
            WiFi.scanDelete();
            lastScanMs = millis();
        }
        delay(2000);
    }

    delay(250);
}
