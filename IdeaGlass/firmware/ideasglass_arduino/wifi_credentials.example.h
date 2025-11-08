#pragma once

struct WifiCredential {
    const char *ssid;
    const char *password;
};

// Copy this file to wifi_credentials.h and edit the values.
static const WifiCredential WIFI_NETWORKS[] = {
    {"dd-wrt", "512cmmmm"},
};

static constexpr size_t WIFI_NETWORK_COUNT = sizeof(WIFI_NETWORKS) / sizeof(WIFI_NETWORKS[0]);
