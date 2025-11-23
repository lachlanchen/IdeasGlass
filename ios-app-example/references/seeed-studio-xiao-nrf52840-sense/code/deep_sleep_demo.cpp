#include "SdFat.h"
#include "Adafruit_SPIFlash.h"
#include <bluefruit.h>

Adafruit_FlashTransport_QSPI flashTransport;
Adafruit_SPIFlash flash(&flashTransport);

bool deepPowerDown(Adafruit_SPIFlash& flash, Adafruit_FlashTransport& transport) {
  uint32_t id_before = flash.getJEDECID();
  transport.begin();
  transport.runCommand(0xB9);  // SPI deep power-down command
  delay(10);
  uint32_t id_after = flash.getJEDECID();
  return (id_after == 0xFFFFFF || id_after == 0xFFFFFFFF);
}

void setup() {
  flash.begin();
  Bluefruit.begin();

  if (!deepPowerDown(flash, flashTransport)) {
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    while (true) {
      yield();
    }
  }

  flash.end();
  sd_power_system_off();
}

void loop() {
  // intentionally empty
}
