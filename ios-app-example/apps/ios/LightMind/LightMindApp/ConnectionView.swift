import SwiftUI
import CoreBluetooth

struct ConnectionView: View {
    @EnvironmentObject private var bleManager: BLEManager

    var body: some View {
        List {
            statusSection
            firmwareSection
            devicesSection
        }
        .navigationTitle("Bluetooth")
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                if let battery = bleManager.batteryLevel {
                    HStack(spacing: 4) {
                        Image(systemName: batterySymbol(for: battery))
                            .foregroundStyle(batteryColor(for: battery))
                        Text("\(battery)%")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    .accessibilityLabel("Battery \(battery) percent")
                }
            }
            ToolbarItem(placement: .topBarTrailing) {
                if bleManager.isScanning {
                    Button("Stop") { bleManager.stopScan() }
                }
            }
        }
    }

    private var firmwareSection: some View {
        Section("Firmware Update") {
            HStack(alignment: .center) {
                VStack(alignment: .leading, spacing: 4) {
                    Text("Current: \(bleManager.firmwareRevision ?? "—")")
                        .font(.subheadline)
                    if let avail = bleManager.availableFirmwareVersion {
                        Text("Available: \(avail)")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                }
                Spacer()
                NavigationLink {
                    FirmwareUpdateView().environmentObject(bleManager)
                } label: {
                    Text("Check Update")
                        .font(.callout)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(Color.green.opacity(0.15))
                        .clipShape(Capsule())
                }
                .disabled(bleManager.connectedPeripheralName == nil)
                .help(bleManager.connectedPeripheralName == nil ? "Connect a device first" : "")
            }
        }
    }

    private var statusSection: some View {
        Section("Status") {
            LabeledContent("Radio") {
                Text(describe(state: bleManager.powerState))
                    .foregroundStyle(bleManager.powerState == .poweredOn ? .green : .secondary)
            }
            LabeledContent("Authorization") {
                Text(describe(auth: bleManager.authorization))
                    .foregroundStyle(.secondary)
            }
            LabeledContent("Connection") {
                Text(bleManager.connectionStatus.displayText)
                    .fontWeight(.semibold)
            }
            if let battery = bleManager.batteryLevel {
                LabeledContent("Battery") { Text("\(battery)%").fontWeight(.medium) }
            }
            if let buttonEvent = bleManager.lastButtonEvent {
                LabeledContent("Button") { Text(buttonEvent).foregroundStyle(.secondary) }
            }
            if bleManager.audioFramesCaptured > 0 {
                LabeledContent("Audio Frames") { Text("\(bleManager.audioFramesCaptured)").foregroundStyle(.secondary) }
            }
            if let codec = bleManager.codecDescription {
                LabeledContent("Codec") { Text(codec).foregroundStyle(.secondary) }
            }
            HStack {
                if let name = bleManager.connectedPeripheralName {
                    Label("Connected to \(name)", systemImage: "checkmark.circle.fill")
                        .foregroundStyle(.green)
                } else {
                    Label("Not connected", systemImage: "circle")
                        .foregroundStyle(.secondary)
                }
            }
            if bleManager.connectedPeripheralName != nil {
                Button("Disconnect", role: .destructive) { bleManager.disconnect() }
                    .buttonStyle(.bordered)
            }
            Toggle("Live playback", isOn: $bleManager.isPlaybackEnabled)
        }
    }

    private var devicesSection: some View {
        Section("Discovered Devices") {
            if bleManager.discoveredPeripherals.isEmpty {
                if bleManager.isScanning {
                    HStack(spacing: 8) {
                        ProgressView()
                        Text("Scanning…")
                            .foregroundStyle(.secondary)
                    }
                } else {
                    Button { bleManager.startScan() } label: {
                        Text("Tap to search")
                            .frame(maxWidth: .infinity)
                    }
                    .controlSize(.large)
                    .buttonStyle(.borderedProminent)
                }
            } else {
                ForEach(bleManager.discoveredPeripherals) { peripheral in
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(peripheral.name)
                                .font(.headline)
                            if peripheral.isTarget {
                                Label("LightMind service", systemImage: "bolt.horizontal.fill")
                                    .font(.caption2)
                                    .foregroundStyle(.green)
                            }
                            Text("RSSI: \(peripheral.rssi) dBm")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        Button(action: { bleManager.connect(to: peripheral.id) }) {
                            Text("Connect")
                        }
                        .buttonStyle(.borderedProminent)
                    }
                }
            }
        }
    }

    private func describe(state: CBManagerState) -> String {
        switch state {
        case .unknown: return "Unknown"
        case .resetting: return "Resetting"
        case .unsupported: return "Unsupported"
        case .unauthorized: return "Unauthorized"
        case .poweredOff: return "Off"
        case .poweredOn: return "On"
        @unknown default: return "Unknown"
        }
    }

    private func describe(auth: CBManagerAuthorization) -> String {
        switch auth {
        case .notDetermined: return "Not requested"
        case .restricted: return "Restricted"
        case .denied: return "Denied"
        case .allowedAlways: return "Allowed"
        @unknown default: return "Unknown"
        }
    }
}

private func batterySymbol(for level: UInt8) -> String {
    switch level {
    case 0..<10: return "battery.0"
    case 10..<35: return "battery.25"
    case 35..<65: return "battery.50"
    case 65..<90: return "battery.75"
    default: return "battery.100"
    }
}

private func batteryColor(for level: UInt8) -> Color {
    switch level {
    case 0..<20: return .red
    case 20..<40: return .orange
    case 40..<70: return .yellow
    default: return .green
    }
}
