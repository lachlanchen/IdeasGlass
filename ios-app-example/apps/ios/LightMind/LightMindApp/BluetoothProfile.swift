import CoreBluetooth

struct LightMindBluetoothProfile {
    let serviceUUID: CBUUID
    let writeCharacteristicUUID: CBUUID
    let notifyCharacteristicUUID: CBUUID

    static let nordicUART = LightMindBluetoothProfile(
        serviceUUID: CBUUID(string: "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"),
        writeCharacteristicUUID: CBUUID(string: "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        notifyCharacteristicUUID: CBUUID(string: "6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
    )

    // Ancillary services surfaced by firmware
    static let audioServiceUUID = CBUUID(string: "19B10000-E8F2-537E-4F6C-D104768A1214")
    static let audioDataCharacteristicUUID = CBUUID(string: "19B10001-E8F2-537E-4F6C-D104768A1214")
    static let audioCodecCharacteristicUUID = CBUUID(string: "19B10002-E8F2-537E-4F6C-D104768A1214")

    static let batteryServiceUUID = CBUUID(string: "180F")
    static let batteryLevelCharacteristicUUID = CBUUID(string: "2A19")

    static let buttonServiceUUID = CBUUID(string: "23BA7924-0000-1000-7450-346EAC492E92")
    static let buttonCharacteristicUUID = CBUUID(string: "23BA7925-0000-1000-7450-346EAC492E92")

    // Device Information Service (for firmware revision reading)
    static let deviceInformationServiceUUID = CBUUID(string: "180A")
    static let firmwareRevisionCharacteristicUUID = CBUUID(string: "2A26")
    static let hardwareRevisionCharacteristicUUID = CBUUID(string: "2A27")
    static let manufacturerNameCharacteristicUUID = CBUUID(string: "2A29")

    // Nordic Legacy DFU (buttonless trigger + DFU transfer handled by Nordic library)
    static let legacyDFUServiceUUID = CBUUID(string: "00001530-1212-EFDE-1523-785FEABCD123")
    static let legacyDFUControlPointUUID = CBUUID(string: "00001531-1212-EFDE-1523-785FEABCD123")
}
