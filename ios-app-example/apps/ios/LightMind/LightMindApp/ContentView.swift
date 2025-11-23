import SwiftUI
import CoreBluetooth

struct ContentView: View {
    @EnvironmentObject private var bleManager: BLEManager
    @State private var pingPayload: String = "ping"

    @State private var navPath = NavigationPath()
    private enum NavTarget: Hashable { case connection, recordings }

    var body: some View {
        NavigationStack(path: $navPath) {
            List {
                liveWaveformSection
                recordingsSection
                logsSection
            }
            .animation(.default, value: bleManager.discoveredPeripherals)
            .navigationTitle("")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    HStack(spacing: 8) {
                        Image("BrandLogo")
                            .resizable()
                            .scaledToFit()
                            .frame(height: 20)
                            .accessibilityLabel("LightMind logo")
                        Text("LightMind Link")
                            .font(.headline)
                    }
                }
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
                    Button {
                        navPath.append(NavTarget.connection)
                    } label: {
                        Label("Devices", systemImage: "dot.radiowaves.left.and.right")
                    }
                }
            }
            .refreshable {
                bleManager.refreshScan()
            }
            .navigationDestination(for: RecordedSegment.self) { segment in
                SegmentDetailView(segment: segment)
                    .environmentObject(bleManager)
            }
            .navigationDestination(for: NavTarget.self) { target in
                switch target {
                case .connection:
                    ConnectionView().environmentObject(bleManager)
                case .recordings:
                    RecordingsListView().environmentObject(bleManager)
                }
            }
        }
    }

    private var liveWaveformSection: some View {
        Section {
            if bleManager.liveWaveform.isEmpty {
                Text("No audio yet")
                    .foregroundStyle(.secondary)
            } else {
                WaveformView(
                    samples: bleManager.liveWaveform,
                    color: .green.opacity(0.8),
                    background: .black.opacity(0.05),
                    barWidth: 2,
                    spacing: 1
                )
                .frame(height: 80)
            }
        } header: {
            HStack {
                Text("Live Waveform")
                Spacer()
                Text(bleManager.isSpeaking ? "Speaking" : "Silent")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Circle()
                    .fill(bleManager.isSpeaking ? Color.red : Color.green.opacity(0.8))
                    .frame(width: 10, height: 10)
                    .overlay(
                        Circle()
                            .stroke(Color.primary.opacity(0.1), lineWidth: 1)
                    )
                    .accessibilityLabel(bleManager.isSpeaking ? "Speaking" : "Silent")
            }
        }
    }

    // Firmware UI moved to ConnectionView

    private var logoSection: some View {
        Section {
            HStack {
                Spacer()
                Image("BrandLogo")
                    .resizable()
                    .scaledToFit()
                    .frame(maxWidth: 160)
                    .accessibilityLabel("LightMind logo")
                Spacer()
            }
            .listRowInsets(EdgeInsets(top: 16, leading: 16, bottom: 8, trailing: 16))
            .listRowBackground(Color.clear)
        }
    }

    private var statusSection: some View {
        Section("Bluetooth Status") {
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
            if bleManager.connectedPeripheralName != nil {
                Button("Disconnect", role: .destructive, action: bleManager.disconnect)
            }
            if let battery = bleManager.batteryLevel {
                LabeledContent("Battery") {
                    Text("\(battery)%")
                        .fontWeight(.medium)
                }
            }
            if let buttonEvent = bleManager.lastButtonEvent {
                LabeledContent("Button") {
                    Text(buttonEvent)
                        .foregroundStyle(.secondary)
                }
            }
            if bleManager.audioFramesCaptured > 0 {
                LabeledContent("Audio Frames") {
                    Text("\(bleManager.audioFramesCaptured)")
                        .foregroundStyle(.secondary)
                }
            }
            if let codec = bleManager.codecDescription {
                LabeledContent("Codec") {
                    Text(codec)
                        .foregroundStyle(.secondary)
                }
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

    // Ping/Pong section removed

    private var logsSection: some View {
        Section("Activity Log") {
            if bleManager.logs.isEmpty {
                HStack(spacing: 8) {
                    Button("Copy Log") { bleManager.copyLogsToPasteboard() }
                        .buttonStyle(.bordered)
                        .disabled(true)
                    Button {
                        bleManager.clearLogs()
                    } label: {
                        Label("Clear Log", systemImage: "trash")
                    }
                    .buttonStyle(.bordered)
                    .disabled(true)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                Text("No events yet")
                    .foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
            } else {
                HStack(spacing: 8) {
                    Button("Copy Log") {
                        bleManager.copyLogsToPasteboard()
                    }
                    .buttonStyle(.bordered)
                    Button {
                        bleManager.clearLogs()
                    } label: {
                        Label("Clear Log", systemImage: "trash")
                    }
                    .buttonStyle(.bordered)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                ForEach(bleManager.logs.suffix(20)) { entry in
                    Text("\(entry.timestamp, style: .time) – \(entry.message)")
                        .font(.callout)
                        .foregroundStyle(color(for: entry.kind))
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
            }
        }
    }

    private var recordingsSection: some View {
        Section("Recordings") {
            if bleManager.recordedSegments.isEmpty {
                Text("No segments yet")
                    .foregroundStyle(.secondary)
            }
            let recent = Array(bleManager.recordedSegments.prefix(3))
            ForEach(recent, id: \.id) { segment in
                HStack {
                    VStack(alignment: .leading) {
                        Text(segment.timestamp, style: .time)
                        Text(segment.fileURL.lastPathComponent)
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                    }
                    Spacer()
                    Button {
                        // Navigate to segment detail when Play is tapped
                        navPath.append(segment)
                    } label: {
                        Label("Play", systemImage: "play.fill")
                    }
                    .buttonStyle(.bordered)
                    Button {
                        // Also navigate via chevron on the far right
                        navPath.append(segment)
                    } label: {
                        Image(systemName: "chevron.right")
                            .foregroundStyle(.tertiary)
                    }
                }
            }
            if bleManager.recordedSegments.count > 3 {
                Button {
                    navPath.append(NavTarget.recordings)
                } label: {
                    Label("More", systemImage: "ellipsis.circle")
                }
            }
        }
    }

    private func toggleScan() {
        if bleManager.isScanning {
            bleManager.stopScan()
        } else {
            bleManager.startScan()
        }
    }

    private func describe(state: CBManagerState) -> String {
        switch state {
        case .unknown:
            return "Unknown"
        case .resetting:
            return "Resetting"
        case .unsupported:
            return "Unsupported"
        case .unauthorized:
            return "Unauthorized"
        case .poweredOff:
            return "Off"
        case .poweredOn:
            return "On"
        @unknown default:
            return "Unknown"
        }
    }

    private func describe(auth: CBManagerAuthorization) -> String {
        switch auth {
        case .notDetermined:
            return "Not requested"
        case .restricted:
            return "Restricted"
        case .denied:
            return "Denied"
        case .allowedAlways:
            return "Allowed"
        @unknown default:
            return "Unknown"
        }
    }

    private func color(for kind: BLEManager.LogEntry.Kind) -> Color {
        switch kind {
        case .info:
            return .primary
        case .outbound:
            return .blue
        case .inbound:
            return .green
        case .error:
            return .red
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
}

#Preview {
    ContentView()
        .environmentObject(BLEManager(profile: .nordicUART, makePreviewData: true))
}
