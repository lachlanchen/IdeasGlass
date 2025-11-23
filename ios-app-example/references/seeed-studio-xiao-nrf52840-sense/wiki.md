# Getting Started with Seeed Studio XIAO nRF52840 Series

XIAO nRF52840    XIAO nRF52840 Sense    XIAO nRF52840 Plus    XIAO nRF52840 Sense Plus

Get One Now 🖱
Get One Now 🖱
Get One Now 🖱
Get One Now 🖱
As the first wireless product in the Seeed Studio XIAO family, Seeed Studio XIAO nRF52840 is equipped with a powerful Nordic nRF52840 MCU which integrates Bluetooth 5.0 connectivity. Meanwhile, it has a small and exquisite form-factor which can be used for wearable devices and Internet of Things projects. The single-sided surface-mountable design and the onboard Bluetooth antenna can greatly facilitate the rapid deployment of IoT projects.

In addition, there is an advanced version of this board, Seeed Studio XIAO nRF52840 Sense. It is integrated with two extra onboard sensors. One of them is a Pulse Density Modulation (PDM) Digital Microphone. It can receive audio data in real-time which allows it to be used for audio recognition. The other one is a 6-axis Inertial Measurement Unit (IMU), this IMU can be very useful in TinyML projects like gesture recognition. These onboard sensors provide a great convenience for users while the board is ultra-small.

The newly upgraded XIAO nRF52840 Plus and XIAO nRF52840 Sense Plus provide considerable increases in functionality and usability. The number of multifunctional pins has been increased to 20, I2S and SPI resources have been added to support more complex projects, NFC pins have been exposed for easier integration into IoT and smart card applications, and the BAT pin has been repositioned for better soldering convenience, resulting in a more user-friendly hardware experience.

Compared to Seeed Studio XIAO RP2040, Seeed Studio XIAO nRF52840 contains richer interfaces. The first thing to note is that the Near Field Communication (NFC) interface is functional on the board. Secondly, there is a tiny reset button on the side of the Type-C interface. On the other side, there is a 3-in-one LED (User LED) along with a Charge LED to indicate the charging status when a battery is connected. There are 11 digital I/O that can be used as PWM pins and 6 analog I/O that can be used as ADC pins. It supports all three common serial interfaces such as UART, I2C, and SPI. Same as Seeed Studio XIAO RP2040, it has an onboard 2 MB flash which means it can also be programmed using Arduino, MicroPython, CircuitPython, or other programming languages.

Seeed Studio XIAO nRF52840 Sense is compatible to the Seeed Studio XIAO expansion board.

Get One Now 🖱️
Features

Powerful wireless capabilities: Bluetooth 5.0 with onboard antenna
Powerful CPU: Nordic nRF52840, ARM® Cortex®-M4 32-bit processor with FPU, 64 MHz
Ultra-Low Power: Standby power consumption is less than 5μA
Battery charging chip: Supports lithium battery charge and discharge management
Onboard 2 MB flash
Onboard PDM microphone (only in Seeed Studio XIAO nRF52840 Sense)
Onboard 6-axis LSM6DS3TR-C IMU (only in Seeed Studio XIAO nRF52840 Sense)
Ultra Small Size: 21 x 17.8mm, Seeed Studio XIAO series classic form-factor for wearable devices
Rich interfaces: 1xUART, 1xI2C, 1xSPI, 1xNFC, 1xSWD, 11xGPIO(PWM), 6xADC in XIAO nRF52840 (Sense); and 2xUART, 1xI2C, 2xSPI, 1xI2S, 1xNFC, 1xSWD, 18xGPIO(PWM), 6xADC in XIAO nRF52840 (Sense) Plus
Single-sided components, surface mounting design
Specifications comparison

Item    Seeed Studio XIAO nRF52840    Seeed Studio XIAO nRF52840 Sense    Seeed Studio XIAO nRF52840 Plus    Seeed Studio XIAO nRF52840 Sense Plus
Processor    Nordic nRF52840, ARM® Cortex®-M4 32-bit processor with FPU, 64 MHz
Wireless Connectivity    Bluetooth LE 5.2/NFC
Memory    256 KB RAM,1MB Flash 2MB onboard Flash
Built-in Sensors    N/A    6 DOF IMU (LSM6DS3TR-C), PDM Microphone    N/A    6 DOF IMU (LSM6DS3TR-C), PDM Microphone
Interfaces    1xI2C, 1xUART, 1xSPI    1xI2C, 2xUART, 2xSPI, 1xI2S
PWM/Analog Pins    11/6    20/6
Onboard Buttons    Reset Button
Onboard LEDs    3-in-one LED/ Charge LED
Battery Charge Chip    BQ25101
Programming Languages    Arduino/ MicroPython/ CircuitPython
Hardware overview

XIAO nRF52840/XIAO nRF52840 Sense
XIAO nRF52840 Plus/XIAO nRF52840 Sense Plus
XIAO nRF52840/XIAO nRF52840 Sense front indication diagram

XIAO nRF52840/XIAO nRF52840 Sense back indication diagram

XIAO nRF52840/XIAO nRF52840 Sense Pin List

Two Arduino Libraries

Seeed Studio XIAO nRF52840 assembles many functions in one tiny board and sometimes may not perform the best of them. Hence, Seeed has published two Arduino libraries to let it maximum the power of each function. Therefore:

It is recommanded to use the Seeed nRF52 Boards library if you want to apply Bluetooth function and "Low Energy Cost Function".
It is recommanded to use the Seeed nRF52 mbed-enabled Boards library if you want to use it in embedded Machine Learning Applications or apply "IMU & PDM advanced function".
Both libraries support very well when it comes to the basic usage, such as LED, Digital, Analog, Serial, I2C, SPI.
The Pin definition supported by these two libraries might be a little different and Seeed will keep update the wiki until it is clear.

TIP
If you use the onboard package of Seeed nRF52 Boards, the Serial function may not compile. The solution is to add the line #include <Adafruit_TinyUSB.h> in your code. You can download this package from: https://github.com/adafruit/Adafruit_TinyUSB_Arduino

If you prefer a simpler approach, you can choose Seeed nRF52 mbed-enabled Boards from the beginning. It supports the compilation of the Serial function without the need for additional modifications.

Getting started

First, we are going to connect the Seeed Studio XIAO nRF52840 (Sense) to the computer and upload a simple code from Arduino IDE to check whether the board is functioning well.

Hardware setup

You need to prepare the following:

1 x Seeed Studio XIAO nRF52840 or Studio XIAO nRF52840 Sense
1 x Computer
1 x USB Type-C cable
TIP
Some USB cables can only supply power and cannot transfer data. If you don't have a USB cable or don't know if your USB cable can transmit data, you can check Seeed USB Type-C support USB 3.1.
Connect the Seeed Studio XIAO nRF52840 (Sense) to your computer via a USB Type-C cable.

pir

Software setup

Step 1. Download and Install the latest version of Arduino IDE according to your operating system
pir

Step 2. Launch the Arduino application

Step 3. Add Seeed Studio XIAO nRF52840 (Sense) board package to your Arduino IDE

Navigate to File > Preferences, and fill "Additional Boards Manager URLs" with the url below: https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json

pir

Navigate to Tools > Board > Boards Manager..., type the keyword "seeed nrf52" in the search box, select the latest version of the board you want, and install it. You can install both.

pir

Step 4. Select your board and port
Board

After installing the board package, navigate to Tools > Board and choose the board you want, continue to select "Seeed XIAO nRF52840 Sense". Now we have finished setting up the Seeed Studio XIAO nRF52840 (Sense) for Arduino IDE.

pir

Port

Navigate to Tools > Port and select the serial port name of the connected Seeed Studio XIAO nRF52840 (Sense). This is likely to be COM3 or higher (COM1 and COM2 are usually reserved for hardware serial ports). The serial port of the connected Seeed Studio XIAO nRF52840 (Sense) usually contains parentheses that are written Seeed Studio XIAO nRF52840 for Seeed Studio XIAO nRF52840 or Seeed Studio XIAO nRF52840 Sense for Seeed Studio XIAO nRF52840 Sense.

pir

Step 5. Navigate to File > Examples > 01.Basics > Blink to open Blink example
pir

Step 6. Click the Upload button to upload the Blink example code to the board
pir

Once uploaded, you will see the built-in red LED blinking with a 1-second delay between each blink. This means the connection is successful and now you can explore more projects with the Seeed Studio XIAO nRF52840 (Sense)!

Playing with the built-in 3-in-one LED

Seeed Studio XIAO nRF52840 (Sense) has an onboard 3-in-one LED which is user-programmable. Now you will learn how to control the RGB colors one-by-one using Arduino!

You first have to understand that the behavior of this LED is not as usual when controlled by the code. The LED turns ON when we give a LOW signal and it turns OFF when we give a HIGH signal. This is because this LED is controlled by a common anode and will light up only with a low-level signal.

An example code would be:

```
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   
}
```

Here, even though HIGH is used, the LED will be OFF. You need to replace HIGH with LOW to turn ON the LED.

Refer to the following pin mappings of the LEDs and use them in your codes:

Red LED = LED_BUILTIN or LED_RED
Blue LED = LED_BLUE
Green LED = LED_GREEN

Power Consumption Verification

The Seeed Studio XIAO nRF52840 is low power consumption and here we provide a method to verify. It is highly recommend to use the Seeed nRF52 Boards library here.

Step 1. Use JLink Downloader to flash the bootloader firmware for Seeed Studio XIAO nRF52840 (Sense).
NOTE
If you are using the factory firmware of the Seeed Studio XIAO nRF52840 or have never made changes to the firmware of the Seeed Studio XIAO nRF52840, you can skip this step.
Step 2. Use theSeeed nRF52 Boards library here.
pir

Step 3. Upload the deep_sleep demo here and run it with Arduino
```
// The MIT License (MIT)
// Copyright (c) 2019 Ha Thach for Adafruit Industries

#include "SdFat.h"
#include "Adafruit_SPIFlash.h"

// Uncomment to run example with custom SPI and SS e.g with FRAM breakout
// #define CUSTOM_CS   A5
// #define CUSTOM_SPI  SPI

#if defined(CUSTOM_CS) && defined(CUSTOM_SPI)
  Adafruit_FlashTransport_SPI flashTransport(CUSTOM_CS, CUSTOM_SPI);

#elif defined(ARDUINO_ARCH_ESP32)
  // ESP32 use same flash device that store code.
  // Therefore there is no need to specify the SPI and SS
  Adafruit_FlashTransport_ESP32 flashTransport;

#else
  // On-board external flash (QSPI or SPI) macros should already
  // defined in your board variant if supported
  // - EXTERNAL_FLASH_USE_QSPI
  // - EXTERNAL_FLASH_USE_CS/EXTERNAL_FLASH_USE_SPI
  #if defined(EXTERNAL_FLASH_USE_QSPI)
    Adafruit_FlashTransport_QSPI flashTransport;

  #elif defined(EXTERNAL_FLASH_USE_SPI)
    Adafruit_FlashTransport_SPI flashTransport(EXTERNAL_FLASH_USE_CS, EXTERNAL_FLASH_USE_SPI);

  #else
    #error No QSPI/SPI flash are defined on your board variant.h !
  #endif
#endif

Adafruit_SPIFlash flash(&flashTransport);

// ... rest of example code ...
```

TIP
Here , We would like to express our special thanks to the author for providing the code → daCoder ←
If you want to know about this example more detail information, click here.

Battery Charging current

The battery charging current is selectable as 50mA or 100mA, where you can set Pin13 as high or low to change it to 50mA or 100mA. The low current charging current is at the input model set up as HIGH LEVEL and the high current charging current is at the output model set up as LOW LEVEL.

```
void setup(){
pinMode (P0_13, OUTPUT);
}
void loop() {
digitalWrite(P0_13, HIGH);
}
```

High Charging Current

```
void setup(){
pinMode (P0_13, OUTPUT);
}
void loop() {
digitalWrite(P0_13, LOW);
}
```

Access the SWD Pins for Debugging and Reflashing Bootloader

Hardware Required

- Seeed Studio XIAO nRF52840
- Jlink

Software Required

It is required to download the Segger software from the website.

1. Use Jlink to connect pins below.
2. Start the J-Flash and search nRF52840, creating a new project.
3. Click "Target" and then select "Connect".
4. Drag the bin or hex file to software. Then press F4 and F5 in that order. The reflashing is done.

FAQ

Q1: My Arduino IDE is stuck when uploading code to the board

You can first try to reset the board by clicking the "Reset Button" once. If that does not work, rapidly click it twice to enter bootloader mode. If that also doesn't work, disconnect the board from the PC, and connect the board again.

Q2: My board is not showing up as a serial device on Arduino IDE

You can first try to reset the board by clicking the "Reset Button" once. If that does not work, rapidly click it twice to enter bootloader mode.

Q3: What are the considerations when using XIAO nRF52840 (Sense) for battery charging?

When P0.14 (D14) turns off the ADC function at a high level of 3.3V, P0.31 will be at the input voltage limit of 3.6V. There is a risk of burning out the P0.31 pin.

Currently for this issue, we recommend that users do not turn off the ADC function of P0.14 (D14) or set P0.14 (D14) to high during battery charging.

Q4: How does the green light behave when powered on?

The P0.17 pin is used to control the green indicator light behavior, indicating the charging status:

- Low level: when charging is in progress.
- High level: when the battery is either not charging or fully charged.

When it is at a low level, the RED_CHG LED will light up.

For more details, check the PMIC datasheet: BQ25100 and XIAO nRF52840 datasheet.

Resources

### Seeed Studio XIAO nRF52840

- [Ebook] XIAO: Big Power, Small Board Mastering Arduino and TinyML
- [PDF] nRF52840 datasheet
- [PDF] Seeed Studio XIAO nRF52840 Schematic
- [ZIP] Seeed Studio XIAO nRF52840 KiCAD file
- [ZIP] Seeed Studio XIAO nRF52840 Eagle file
- [DXF] Seeed Studio XIAO nRF52840 Dimension in DXF
- [LBR] Seeed Studio XIAO nRF52840 Eagle footprint
- [XLSX] Seeed Studio XIAO nRF52840 pinout sheet
- 🔗 [Kicad] Seeed Studio XIAO nRF52840 FootPrint

### Seeed Studio XIAO nRF52840 Sense

- [PDF] nRF52840 datasheet
- [PDF] Seeed Studio XIAO nRF52840 Sense Schematic
- [ZIP] Seeed Studio XIAO nRF52840 KiCAD file
- [ZIP] Seeed Studio XIAO nRF52840 Eagle file
- [DXF] Seeed Studio XIAO nRF52840 Sense Dimension in DXF
- [LBR] Seeed Studio XIAO nRF52840 Sense Eagle footprint
- [XLSX] Seeed Studio XIAO nRF52840 Sense pinout sheet
- [STEP] Seeed Studio XIAO nRF52840 Sense 3D Model
- 🔗 [Kicad] Seeed Studio XIAO nRF52840 Sense FootPrint

### Seeed Studio XIAO nRF52840 (Sense) Plus

- [PDF] nRF52840 datasheet
- [ZIP] Seeed Studio XIAO nRF52840 (Sense) Plus Schematic
- [ZIP] Seeed Studio XIAO nRF52840 (Sense) Plus KiCAD file
- [DXF] Seeed Studio XIAO nRF52840 Sense Dimension in DXF
- [ZIP] Seeed Studio XIAO Plus Base with bottom pad lead out
- [ZIP] Seeed Studio XIAO Plus Base without bottom pad lead out
- [Kicad] Seeed Studio XIAO nRF52840 (Sense) Plus FootPrint
- [Kicad] Seeed Studio XIAO nRF52840 (Sense) Plus Symbol

Course Resources

- [Ebook] XIAO: Big Power, Small Board Mastering Arduino and TinyML

Tech Support & Product Discussion

Thank you for choosing our products! We are here to provide you with different support to ensure that your experience with our products is as smooth as possible. We offer several communication channels to cater to different preferences and needs.

_Last updated on Nov 28, 2024 by Clara_  
Previous: XIAO RP2350 with PlatformIO  
Next: XIAO nRF52840(sense) With NuttX(RTOS)
