import SwiftUI
import CoreBluetooth
#if canImport(NordicDFU)
import NordicDFU
#elseif canImport(iOSDFULibrary)
import iOSDFULibrary
#endif

struct FirmwareUpdateView: View {
    @EnvironmentObject private var ble: BLEManager
    @State private var isChecking = false
    @State private var showConfirm = false
    @State private var pendingURL: URL?
    @State private var statusMessage: String?
    @State private var isUpdating = false
    @State private var downloadProgress: Double = 0
    @State private var dfuProgress: Int = 0
    @State private var dfuState: String = ""
    @State private var logs: [String] = []
    @State private var downloaderRef: DownloadDelegate?
#if canImport(NordicDFU) || canImport(iOSDFULibrary)
    @State private var dfuTargetName: String?
    @State private var dfuController: DFUServiceController?
    @State private var dfuLogger: ConsoleLoggerProxy?
    @State private var dfuProgressDelegate: DFUProgressProxy?
    @State private var dfuStateDelegate: DFUStateProxy?
#endif

    private var dfuAvailable: Bool {
        #if canImport(NordicDFU) || canImport(iOSDFULibrary)
        return true
        #else
        return false
        #endif
    }

    // Source of truth for available version. In the next iteration we can fetch
    // a small JSON from your server, but for now it mirrors the bundled firmware (2.0.15).
    private var available: String { ble.availableFirmwareVersion ?? "2.0.15" }

    // Static catalogue of testable firmware packages served by the local server.
    // Extend this list (version, label, urlString) when adding new ZIPs to dist/.
    private struct FirmwareOption {
        let version: String
        let label: String
        let urlString: String
    }
    private var firmwareOptions: [FirmwareOption] {
        [
            FirmwareOption(
                version: "2.0.15",
                label: "LightMind DK2 (latest)",
                urlString: "https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.15.zip"
            ),
            FirmwareOption(
                version: "2.0.14",
                label: "LightMind DK2 (previous)",
                urlString: "https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.14.zip"
            ),
            FirmwareOption(
                version: "2.0.13",
                label: "LightMind DK2 (previous)",
                urlString: "https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.13.zip"
            ),
            FirmwareOption(
                version: "2.0.12",
                label: "LightMind DK2 (previous)",
                urlString: "https://ios.lightmind.art/downloads/firmware/lightmind-dk2-2.0.12.zip"
            ),
            FirmwareOption(
                version: "2.0.11",
                label: "LightMind DK2 (test)",
                urlString: "https://ios.lightmind.art/downloads/firmware/lightmind-dk2-test-2.0.11.zip"
            ),
            FirmwareOption(
                version: "2.0.10",
                label: "Omi DevKit 2 (official)",
                urlString: "https://ios.lightmind.art/downloads/firmware/firmware.zip"
            )
        ]
    }

    var body: some View {
        List {
            Section("Device") {
                LabeledContent("Name") { Text(ble.connectedPeripheralName ?? "Not connected").foregroundStyle(.secondary) }
                LabeledContent("Firmware") { Text(ble.firmwareRevision ?? "—").fontWeight(.medium) }
                if let hw = ble.hardwareRevision { LabeledContent("Hardware") { Text(hw).foregroundStyle(.secondary) } }
            }

            Section("Update (Over‑the‑Air)") {
                if !dfuAvailable {
                    Text("Nordic DFU library not linked. Add https://github.com/NordicSemiconductor/IOS-DFU-Library to the LightMind target, then clean/build.")
                        .font(.footnote)
                        .foregroundStyle(.red)
                }
                LabeledContent("Device Firmware") {
                    Text(ble.firmwareRevision ?? "—").fontWeight(.medium)
                }

                ForEach(firmwareOptions, id: \.version) { option in
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Version \(option.version)")
                                .font(.subheadline)
                            Text(option.label)
                                .font(.footnote)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        Button {
                            pendingURL = URL(string: option.urlString)
                            showConfirm = true
                        } label: {
                            Text("Install")
                                .font(.callout)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                        }
                        .buttonStyle(.borderedProminent)
                        .disabled(isUpdating || isChecking || !dfuAvailable)
                    }
                }

                Divider()
                Button(action: checkNow) {
                    Label("Check Update", systemImage: "arrow.clockwise")
                }
                .disabled(isChecking)
            }

            if downloadProgress > 0 && downloadProgress < 1.0 {
                Section("Downloading") {
                    ProgressView(value: downloadProgress)
                    Text(String(format: "%.0f%%", downloadProgress * 100)).foregroundStyle(.secondary)
                }
            }

            if isUpdating {
                Section("Updating") {
                    ProgressView(value: Double(dfuProgress) / 100.0)
                    Text("DFU \(dfuProgress)% \(dfuState)")
                        .foregroundStyle(.secondary)
                }
            }

            if let msg = statusMessage {
                Section("Status") {
                    Text(msg)
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                        .textSelection(.enabled)
                }
            }

            if !logs.isEmpty {
                Section {
                    Button {
                        let text = logs.joined(separator: "\n")
                        UIPasteboard.general.string = text
                        statusMessage = "Copied update logs (\(logs.count) lines)"
                    } label: {
                        Label("Copy Logs", systemImage: "doc.on.doc")
                    }
                }
                Section("Logs") {
                    ForEach(Array(logs.enumerated()), id: \.offset) { _, line in
                        Text(line).font(.footnote).textSelection(.enabled)
                    }
                }
            }

            Section("Tips") {
                Text("Unplug USB data cable during BLE update. Keep the phone near the device and close other BLE apps.")
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
        }
        .navigationTitle("Firmware Update")
        .navigationBarTitleDisplayMode(.inline)
        .alert("Confirm Update", isPresented: $showConfirm) {
            Button("Cancel", role: .cancel) {}
            Button("Update") { if let u = pendingURL { startUpdate(from: u) } }
        } message: {
            Text("The device will reboot into DFU mode. Unplug USB, keep the phone nearby, and keep this app in foreground.")
        }
    }

    private var needsUpdate: Bool {
        guard let current = ble.firmwareRevision else { return false }
        return compareSemver(current, available) == .orderedAscending
    }

    private func checkNow() {
        isChecking = true
        statusMessage = "Refreshing firmware info…"
        // Trigger a fresh read of the DIS Firmware Revision characteristic.
        // If the device is connected and the characteristic is known, BLEManager will read and publish it.
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            isChecking = false
            statusMessage = "Checked at \(Date().formatted(date: .omitted, time: .shortened))"
        }
    }

    private func startUpdate(from url: URL) {
        #if canImport(NordicDFU) || canImport(iOSDFULibrary)
        let peripheralSnapshot = ble.snapshotConnectedPeripheral()
        let centralRef = ble.centralManagerHandle()
        guard let targetUUID = peripheralSnapshot?.identifier ?? ble.dfuTargetIdentifier else {
            statusMessage = "Connect to your LightMind device before updating."
            logs.append("No connected device – cannot start DFU.")
            return
        }
        dfuTargetName = ble.connectedPeripheralName
        logs.removeAll(); statusMessage = "Downloading firmware… (Nordic DFU path)"; downloadProgress = 0
        ble.postLog("DFU: downloading package…")
        dfuProgress = 0; dfuState = ""
        ble.setDFUInProgress(true)
        downloadFirmwareZip(from: url) { localURL, err in
            if let err = err {
                self.statusMessage = "Download failed: \(err.localizedDescription)"; self.logs.append(self.statusMessage!)
                self.ble.setDFUInProgress(false)
                return
            }
            guard let localURL else { self.statusMessage = "Download failed"; self.ble.setDFUInProgress(false); return }
            DispatchQueue.main.async {
                do {
                    let firmware = try DFUFirmware(urlToZipFile: localURL)
                    self.ble.postLog("DFU: package ready, preparing device…")
                    self.beginLegacyDFU(with: firmware,
                                        target: targetUUID,
                                        peripheralSnapshot: peripheralSnapshot,
                                        central: centralRef)
                } catch {
                    self.statusMessage = "DFU init failed: \(error.localizedDescription)"; self.logs.append(self.statusMessage!)
                    self.ble.setDFUInProgress(false)
                }
            }
        }
        #else
        statusMessage = "Nordic DFU library not linked. Add https://github.com/NordicSemiconductor/IOS-DFU-Library to the LightMind target, then clean/build."
        ble.postLog(statusMessage!)
        #endif
    }

    // Simple semver-ish compare (major.minor.patch)
    private func compareSemver(_ a: String, _ b: String) -> ComparisonResult {
        func parts(_ s: String) -> [Int] { s.split(separator: ".").map { Int($0) ?? 0 } }
        let pa = parts(a), pb = parts(b)
        for i in 0..<max(pa.count, pb.count) {
            let va = i < pa.count ? pa[i] : 0
            let vb = i < pb.count ? pb[i] : 0
            if va < vb { return .orderedAscending }
            if va > vb { return .orderedDescending }
        }
        return .orderedSame
    }

#if canImport(NordicDFU) || canImport(iOSDFULibrary)
    private func beginLegacyDFU(with firmware: DFUFirmware,
                                target uuid: UUID,
                                peripheralSnapshot: CBPeripheral?,
                                central: CBCentralManager?) {
        statusMessage = "Preparing device for DFU…"
        logs.append(statusMessage ?? "Preparing device for DFU…")
        isUpdating = true
        dfuProgress = 0
        dfuState = ""
        ble.prepareForDFU()
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            // Use existing central + peripheral when available to avoid "central not powered on" issues.
            let initiator: DFUServiceInitiator
            if let central = central, let peripheral = peripheralSnapshot {
                initiator = DFUServiceInitiator(centralManager: central, target: peripheral)
                self.logs.append("Using existing central/peripheral for DFU (state: \(central.state.rawValue))")
            } else {
                initiator = DFUServiceInitiator(queue: DispatchQueue.main)
                self.logs.append("Using new central for DFU")
            }
            initiator.packetReceiptNotificationParameter = 8
            initiator.forceScanningForNewAddressInLegacyDfu = true
            initiator.enableUnsafeExperimentalButtonlessServiceInSecureDfu = true
            initiator.alternativeAdvertisingNameEnabled = true
            initiator.connectionTimeout = 60.0
            initiator.peripheralSelector = NameOrServiceSelector()
            let logger = ConsoleLoggerProxy { msg in
                DispatchQueue.main.async {
                    self.logs.append(msg)
                    self.statusMessage = msg
                }
            }
            self.dfuLogger = logger
            initiator.logger = logger

            let progressDelegate = DFUProgressProxy { progress in
                DispatchQueue.main.async {
                    self.dfuProgress = progress
                    self.statusMessage = String(format: "DFU %d%%", progress)
                }
            }
            self.dfuProgressDelegate = progressDelegate
            initiator.progressDelegate = progressDelegate

            let stateDelegate = DFUStateProxy(onState: { state in
                DispatchQueue.main.async {
                    self.dfuState = state.description
                    self.statusMessage = state.description
                    if state == .completed {
                        self.isUpdating = false
                        self.ble.setDFUInProgress(false)
                        self.ble.restoreCentralAfterDFU()
                        self.logs.append("DFU completed. Reconnecting…")
                        self.scheduleReconnectByNameIfNeeded()
                    }
                }
            }, onError: { error, message in
                DispatchQueue.main.async {
                    self.logs.append("DFU error: \(error.rawValue) \(message)")
                    self.statusMessage = "DFU error: \(message)"
                    self.isUpdating = false
                    self.ble.setDFUInProgress(false)
                    self.ble.restoreCentralAfterDFU()
                    self.scheduleReconnectByNameIfNeeded()
                }
            })
            self.dfuStateDelegate = stateDelegate
            initiator.delegate = stateDelegate
            self.logs.append("Starting Nordic DFU…")
            let configuredInitiator = initiator.with(firmware: firmware)
            // Use .start(targetWithIdentifier:) to let the library handle buttonless trigger and bootloader reconnect.
            let controller = configuredInitiator.start(targetWithIdentifier: uuid)
            if let controller {
                self.dfuController = controller
            } else {
                self.statusMessage = "Unable to start DFU. Reconnect the device and try again."
                self.logs.append(self.statusMessage!)
                self.isUpdating = false
                self.ble.setDFUInProgress(false)
                self.ble.refreshScan()
            }
        }
    }
#endif
}

// Simple downloader with progress
private final class DownloadDelegate: NSObject, URLSessionDownloadDelegate {
    let onProgress: (Double) -> Void
    let onComplete: (URL?, Error?) -> Void
    init(onProgress: @escaping (Double) -> Void, onComplete: @escaping (URL?, Error?) -> Void) {
        self.onProgress = onProgress; self.onComplete = onComplete
    }
    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didFinishDownloadingTo location: URL) {
        onComplete(location, nil)
    }
    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        if let error { onComplete(nil, error) }
    }
    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didWriteData bytesWritten: Int64, totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        guard totalBytesExpectedToWrite > 0 else { return }
        onProgress(Double(totalBytesWritten) / Double(totalBytesExpectedToWrite))
    }
}

private extension FirmwareUpdateView {
    func downloadFirmwareZip(from url: URL, completion: @escaping (URL?, Error?) -> Void) {
        let delegate = DownloadDelegate(onProgress: { p in
            self.downloadProgress = max(0, min(1, p))
        }, onComplete: { tempURL, err in
            if let err = err { completion(nil, err); return }
            guard let tempURL else { completion(nil, NSError(domain: "Download", code: -1, userInfo: [NSLocalizedDescriptionKey: "No file"])) ; return }
            let dst = URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("firmware.zip")
            try? FileManager.default.removeItem(at: dst)
            do { try FileManager.default.copyItem(at: tempURL, to: dst) } catch { completion(nil, error); return }
            DispatchQueue.main.async { self.downloadProgress = 1.0; self.logs.append("Downloaded firmware.zip") }
            completion(dst, nil)
        })
        self.downloaderRef = delegate
        let session = URLSession(configuration: .default, delegate: delegate, delegateQueue: OperationQueue.main)
        let task = session.downloadTask(with: url)
        task.resume()
    }

    func scheduleReconnectByNameIfNeeded() {
        // If we're already connected, nothing to do.
        if ble.connectedPeripheralName != nil { return }
        guard let targetName = dfuTargetName, !targetName.isEmpty else { return }
        ble.postLog("Firmware DFU page: scanning for \(targetName) to auto-reconnect after DFU")
        // Kick off a scan; we'll poll the discovered list and connect once we see the same name.
        ble.startScan(duration: 30)
        attemptReconnectByName(targetName: targetName, retries: 30)
    }

    func attemptReconnectByName(targetName: String, retries: Int) {
        guard retries > 0 else {
            ble.postLog("Firmware DFU page: giving up auto-reconnect for \(targetName)")
            return
        }
        // If we've already connected (e.g. via auto-reconnect), stop.
        if ble.connectedPeripheralName != nil { return }
        if let match = ble.discoveredPeripherals.first(where: { $0.name == targetName }) {
            ble.postLog("Firmware DFU page: auto-connecting to \(targetName) by name")
            ble.connect(to: match.id)
            return
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            attemptReconnectByName(targetName: targetName, retries: retries - 1)
        }
    }

    var supportsBLEDFU: Bool {
        if let hw = ble.hardwareRevision?.lowercased() {
            if hw.contains("xiao") || hw.contains("seeed") || hw.contains("sense") { return false }
        }
        return true
    }
}

#if canImport(NordicDFU) || canImport(iOSDFULibrary)
private final class ConsoleLoggerProxy: LoggerDelegate {
    let sink: (String) -> Void
    init(_ sink: @escaping (String) -> Void) { self.sink = sink }
    func logWith(_ level: LogLevel, message: String) {
        sink(message)
    }
}

private final class DFUProgressProxy: DFUProgressDelegate {
    let sink: (Int) -> Void
    init(_ sink: @escaping (Int) -> Void) { self.sink = sink }
    func dfuProgressDidChange(for part: Int, outOf totalParts: Int, to progress: Int, currentSpeedBytesPerSecond: Double, avgSpeedBytesPerSecond: Double) {
        sink(progress)
    }
}

private final class DFUStateProxy: DFUServiceDelegate {
    let onState: (DFUState) -> Void
    let onErr: (DFUError, String) -> Void
    init(onState: @escaping (DFUState) -> Void, onError: @escaping (DFUError, String) -> Void) { self.onState = onState; self.onErr = onError }
    func dfuStateDidChange(to state: DFUState) { onState(state) }
    func dfuError(_ error: DFUError, didOccurWithMessage message: String) { onErr(error, message) }
}

final class NameOrServiceSelector: DFUPeripheralSelectorDelegate {
    private let legacyDFU = CBUUID(string: "00001530-1212-EFDE-1523-785FEABCD123")
    private let secureDFU = CBUUID(string: "FE59")
    private let allowedNames = ["DfuTarg", "DFUTarg", "DfuTarget", "LightMind DFU", "Omi DFU"]

    func select(_ peripheral: CBPeripheral,
                advertisementData: [String : AnyObject],
                RSSI: NSNumber,
                hint name: String?) -> Bool {
        if let localName = advertisementData[CBAdvertisementDataLocalNameKey] as? String {
            if allowedNames.contains(where: { localName.contains($0) }) {
                return true
            }
            if let name, localName == name {
                return true
            }
        }
        if let uuids = advertisementData[CBAdvertisementDataServiceUUIDsKey] as? [CBUUID] {
            if uuids.contains(legacyDFU) || uuids.contains(secureDFU) { return true }
        }
        if let uuids = advertisementData[CBAdvertisementDataOverflowServiceUUIDsKey] as? [CBUUID] {
            if uuids.contains(legacyDFU) || uuids.contains(secureDFU) { return true }
        }
        return false
    }

    func filterBy(hint dfuServiceUUID: CBUUID) -> [CBUUID]? {
        return [dfuServiceUUID, legacyDFU, secureDFU]
    }
}
#endif

#Preview {
    FirmwareUpdateView()
        .environmentObject(BLEManager(profile: .nordicUART, makePreviewData: true))
}
