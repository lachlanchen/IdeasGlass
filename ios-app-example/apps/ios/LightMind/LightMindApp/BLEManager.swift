import Foundation
import CoreBluetooth
import UIKit

final class BLEManager: NSObject, ObservableObject {
    struct PeripheralSummary: Identifiable, Equatable {
        let id: UUID
        var name: String
        var rssi: Int
        var isTarget: Bool
    }

    enum ConnectionStatus: Equatable {
        case idle
        case scanning
        case connecting(String)
        case connected(String)
        case failed(String)

        var displayText: String {
            switch self {
            case .idle:
                return "Idle"
            case .scanning:
                return "Scanning"
            case .connecting(let name):
                return "Connecting to \(name)…"
            case .connected(let name):
                return "Connected to \(name)"
            case .failed(let reason):
                return "Failed (\(reason))"
            }
        }
    }

    struct LogEntry: Identifiable {
        enum Kind {
            case info
            case outbound
            case inbound
            case error
        }

        let id = UUID()
        let timestamp = Date()
        let message: String
        let kind: Kind
    }

    @Published private(set) var authorization: CBManagerAuthorization = CBCentralManager.authorization
    @Published private(set) var powerState: CBManagerState = .unknown
    @Published private(set) var discoveredPeripherals: [PeripheralSummary] = []
    @Published private(set) var connectionStatus: ConnectionStatus = .idle
    @Published private(set) var logs: [LogEntry] = []
    @Published private(set) var isScanning: Bool = false
    @Published private(set) var lastPongDate: Date?
    @Published private(set) var batteryLevel: UInt8?
    @Published private(set) var lastButtonEvent: String?
    @Published private(set) var audioFramesCaptured: Int = 0
    @Published private(set) var codecDescription: String?
    @Published private(set) var recordedSegments: [RecordedSegment] = []
    @Published private(set) var firmwareRevision: String?
    @Published private(set) var hardwareRevision: String?
    @Published private(set) var availableFirmwareVersion: String? = "2.0.15"
    @Published var dfuInProgress: Bool = false
    @Published var isPlaybackEnabled: Bool = false
    @Published private(set) var isSpeaking: Bool = false
    @Published private(set) var liveWaveform: [Float] = []

    var connectedPeripheralName: String? {
        if case let .connected(name) = connectionStatus {
            return name
        }
        return nil
    }

    var connectedPeripheralIdentifier: UUID? {
        return connectedPeripheral?.identifier
    }

    private var central: CBCentralManager?
    private let profile: LightMindBluetoothProfile
    private var peripheralCache: [UUID: CBPeripheral] = [:]
    private var connectedPeripheral: CBPeripheral?
    private var writeCharacteristic: CBCharacteristic?
    private var notifyCharacteristic: CBCharacteristic?
    private var batteryCharacteristic: CBCharacteristic?
    private var buttonCharacteristic: CBCharacteristic?
    private var firmwareRevisionCharacteristic: CBCharacteristic?
    private var hardwareRevisionCharacteristic: CBCharacteristic?
    private var dfuControlPointCharacteristic: CBCharacteristic?
    private var detectedCodec: UInt8?
    private var pendingAudioFrame = Data()
    private var lastLoggedBatteryLevel: UInt8?
    private var lastLoggedButtonEvent: String?
    private var lastLoggedCodecId: UInt8?
    private let audioPlayer = AudioStreamManager(sampleRate: 16_000)
    private let recorder = AudioRecorder()
    private let liveWaveformQueue = DispatchQueue(label: "live-waveform-queue")
    private let audioProcessingQueue = DispatchQueue(label: "audio-processing-queue")
    private var livePCMBuffer = Data()
    private let livePCMLimitBytes = 2 * 16_000 * 2 // 2 seconds of mono PCM16 at 16kHz
    private let opusDecoder = OpusDecodeService()
    private var missingCodecLogged = false
    private var playbackDisabledLogged = false
    private var vadLevel: Float = 0.0
    private var scanTimeoutTask: DispatchWorkItem?
    private var lastPingDate: Date?
    private var lastKnownRecorderSegmentCount: Int = 0
    private let logLimit = 200
    private let isPreview: Bool
    private let lastPeripheralKey = "LightMind.LastPeripheralUUID"
    private let autoReconnectKey = "LightMind.AutoReconnectEnabled"
    private var targetReconnectUUID: UUID?
    private var autoReconnectEnabled: Bool {
        get { UserDefaults.standard.object(forKey: autoReconnectKey) as? Bool ?? true }
        set { UserDefaults.standard.set(newValue, forKey: autoReconnectKey) }
    }
    var dfuTargetIdentifier: UUID? {
        connectedPeripheral?.identifier ?? loadLastPeripheralUUID()
    }
    
    func snapshotConnectedPeripheral() -> CBPeripheral? {
        return connectedPeripheral
    }
    
    func centralManagerHandle() -> CBCentralManager? {
        return central
    }

    // Expose current in-progress recording URL for views that want to live-refresh
    var inProgressFileURL: URL? { recorder.currentInProgressSegment()?.fileURL }

    override init() {
        self.profile = .nordicUART
        self.isPreview = false
        super.init()
        central = CBCentralManager(delegate: self, queue: nil, options: [CBCentralManagerOptionRestoreIdentifierKey: "com.lmcognition.LightMind.central"]) 
        authorization = CBCentralManager.authorization
    }

    init(profile: LightMindBluetoothProfile = .nordicUART, makePreviewData: Bool) {
        self.profile = profile
        self.isPreview = makePreviewData
        super.init()
        if makePreviewData {
            populatePreviewData()
        } else {
            central = CBCentralManager(delegate: self, queue: nil, options: [CBCentralManagerOptionRestoreIdentifierKey: "com.lmcognition.LightMind.central"]) 
            authorization = CBCentralManager.authorization
        }
    }

    func startScan(duration: TimeInterval = 12) {
        guard !isPreview else { return }
        guard central?.state == .poweredOn else {
            log("Bluetooth radio is not powered on", kind: .error)
            return
        }
        stopScan()
        discoveredPeripherals.removeAll()
        connectionStatus = .scanning
        central?.scanForPeripherals(withServices: nil, options: [CBCentralManagerScanOptionAllowDuplicatesKey: false])
        isScanning = true
        scheduleScanTimeout(duration: duration)
        log("Scanning for peripherals (target \(profile.serviceUUID.uuidString))")
    }

    func stopScan() {
        guard isScanning else { return }
        scanTimeoutTask?.cancel()
        scanTimeoutTask = nil
        central?.stopScan()
        isScanning = false
        if case .scanning = connectionStatus {
            connectionStatus = .idle
        }
        log("Stopped scanning")
    }

    func refreshScan() {
        startScan()
    }

    func connect(to peripheralID: UUID) {
        guard let peripheral = peripheralCache[peripheralID] else {
            log("Selected peripheral is no longer available", kind: .error)
            return
        }
        guard !isPreview else { return }
        stopScan()
        connectionStatus = .connecting(peripheral.sanitizedName)
        connectedPeripheral = peripheral
        peripheral.delegate = self
        central?.connect(peripheral, options: nil)
        log("Attempting connection to \(peripheral.sanitizedName)")
    }

    func disconnect() {
        guard let peripheral = connectedPeripheral else { return }
        central?.cancelPeripheralConnection(peripheral)
        log("Disconnect requested")
    }

    func sendPing(text: String = "ping") {
        guard let peripheral = connectedPeripheral, let characteristic = writeCharacteristic else {
            log("Cannot send ping – no connected peripheral", kind: .error)
            return
        }
        guard let data = text.data(using: .utf8) else { return }
        lastPingDate = Date()
        peripheral.writeValue(data, for: characteristic, type: .withResponse)
        log("TX: \(text)", kind: .outbound)
    }

    func clearLogs() {
        logs.removeAll()
    }

    // DFU: Enter legacy buttonless DFU mode by writing 0x06 to the control point.
    // The Nordic iOS DFU library is recommended to handle the transfer after reboot.
    func enterLegacyDFUMode() {
        guard let peripheral = connectedPeripheral, let cp = dfuControlPointCharacteristic else {
            log("DFU control point not available (connect to the device first)", kind: .error)
            return
        }
        dfuInProgress = true
        let cmd = Data([0x06])
        peripheral.writeValue(cmd, for: cp, type: .withResponse)
        log("Requested DFU mode (buttonless)")
    }

    func prepareForDFU() {
        stopScan()
        if let peripheral = connectedPeripheral {
            log("Disconnecting before DFU…")
            central?.cancelPeripheralConnection(peripheral)
        }
    }

    func setDFUInProgress(_ on: Bool) {
        if Thread.isMainThread {
            dfuInProgress = on
        } else {
            DispatchQueue.main.async { self.dfuInProgress = on }
        }
    }

    // After Nordic DFU finishes (success or error) and has used our CBCentralManager,
    // restore this object as the central delegate so scans and auto-reconnect work again.
    func restoreCentralAfterDFU() {
        guard !isPreview else { return }
        central?.delegate = self
        log("Restored BLE central delegate after DFU")
        autoReconnectIfPossible()
    }

    private func scheduleScanTimeout(duration: TimeInterval) {
        scanTimeoutTask?.cancel()
        let task = DispatchWorkItem { [weak self] in
            self?.stopScan()
        }
        scanTimeoutTask = task
        DispatchQueue.main.asyncAfter(deadline: .now() + duration, execute: task)
    }

    private func handle(value data: Data) {
        let text = String(data: data, encoding: .utf8) ?? data.map { String(format: "%02hhX", $0) }.joined()
        log("RX: \(text)", kind: .inbound)
        lastPongDate = Date()
        if let lastPingDate {
            let latency = lastPongDate!.timeIntervalSince(lastPingDate)
            log(String(format: "Round-trip %.0f ms", latency * 1000), kind: .info)
        }
    }

    private func handleAudioPacket(_ data: Data) {
        guard data.count > 3 else { return }
        let chunkIndex = data[2]
        let payload = data.subdata(in: 3..<data.count)

        if chunkIndex == 0 {
            if !pendingAudioFrame.isEmpty {
                finalizeAudioFrame()
            }
            pendingAudioFrame = Data(payload)
        } else {
            guard !pendingAudioFrame.isEmpty else {
                log("Audio desync – missing frame header", kind: .error)
                return
            }
            pendingAudioFrame.append(payload)
        }
    }

    private func finalizeAudioFrame() {
        guard !pendingAudioFrame.isEmpty else { return }
        let frame = pendingAudioFrame
        pendingAudioFrame = Data()
        audioFramesCaptured += 1

        guard let codec = detectedCodec else {
            if !missingCodecLogged {
                log("Awaiting codec negotiation before streaming audio", kind: .error)
                missingCodecLogged = true
            }
            return
        }
        missingCodecLogged = false

        switch codec {
        case 0: // PCM16
            if isPlaybackEnabled {
                audioPlayer?.play(pcmData: frame)
                playbackDisabledLogged = false
            } else if !playbackDisabledLogged {
                playbackDisabledLogged = true
                log("Live playback disabled – enable toggle to hear audio")
            }
            appendFrameToRecorder(frame)
            appendFrameToLivePCM(frame)
            updateVoiceActivity(with: frame)
        case 20:
            // Opus frame: decode off the main thread for smooth UI/audio
            audioProcessingQueue.async { [weak self] in
                guard let self else { return }
                if let pcm = self.opusDecoder?.decode(frame) {
                    if self.isPlaybackEnabled { self.audioPlayer?.play(pcmData: pcm); self.playbackDisabledLogged = false }
                    else if !self.playbackDisabledLogged { self.playbackDisabledLogged = true; self.log("Live playback disabled – enable toggle to hear audio") }
                    self.appendFrameToRecorder(pcm)
                    self.appendFrameToLivePCM(pcm)
                    self.updateVoiceActivity(with: pcm)
                } else if codec != self.lastLoggedCodecId {
                    self.lastLoggedCodecId = codec
                    self.log("Opus frame \(frame.count) bytes (decoder not installed)")
                }
            }
        default:
            if codec != lastLoggedCodecId {
                lastLoggedCodecId = codec
                log("Unhandled codec id \(codec)")
            }
        }
        // Do not overwrite the UI list from the in-memory buffer; persistence drives the list
    }

    private func appendFrameToRecorder(_ frame: Data) {
        recorder.append(frame: frame)
        // When a new segment starts, recorder.segments.count increases. That means the previous
        // segment was just finalized (moved + persisted). Reload from store once.
        let currentCount = recorder.segments.count
        if currentCount > lastKnownRecorderSegmentCount {
            lastKnownRecorderSegmentCount = currentCount
            if let p = connectedPeripheral {
                reloadSegmentsFromStore(for: p.identifier)
                if let latest = recorder.segments.last,
                   let size = try? latest.fileURL.resourceValues(forKeys: [.fileSizeKey]).fileSize {
                    let kb = Double(size) / 1024.0
                    log(String(format: "New segment at %@ (%.1f KB)", latest.timestamp.formatted(date: .omitted, time: .standard), kb))
                }
            }
        }
    }

    private func reloadSegmentsFromStore(for deviceUUID: UUID, limit: Int = 500) {
        let deviceId = deviceUUID.uuidString
        let inProg = self.recorder.currentInProgressSegment()
        DispatchQueue.global().async {
            var items: [RecordedSegment] = []
            let metas = (try? Repositories.segments.recentSegments(for: deviceId, limit: limit)) ?? []
            if !metas.isEmpty {
                items = metas.map { meta in
                    RecordedSegment(timestamp: meta.timestamp, fileURL: URL(fileURLWithPath: meta.filePath))
                }
            } else {
                // Fallback: scan disk for content-addressed files if DB returns nothing
                if let diskItems = try? self.scanSegmentsFromDisk(limit: limit) { items = diskItems }
            }
            if let inProg {
                let exists = items.contains { $0.fileURL.path == inProg.fileURL.path }
                if !exists { items.insert(inProg, at: 0) }
            }
            DispatchQueue.main.async {
                self.recordedSegments = items
                self.log("Loaded \(items.count) segment(s) for device")
            }
        }
    }

    private func scanSegmentsFromDisk(limit: Int) throws -> [RecordedSegment] {
        let root = try Paths.segmentsRoot()
        let fm = FileManager.default
        guard let enumerator = fm.enumerator(at: root, includingPropertiesForKeys: [.contentModificationDateKey, .isRegularFileKey], options: [.skipsHiddenFiles]) else { return [] }
        var files: [(url: URL, mtime: Date)] = []
        for case let url as URL in enumerator {
            let values = try? url.resourceValues(forKeys: [.isRegularFileKey, .contentModificationDateKey])
            if values?.isRegularFile == true { files.append((url, values?.contentModificationDate ?? Date.distantPast)) }
        }
        files.sort { $0.mtime > $1.mtime }
        let chosen = files.prefix(limit)
        return chosen.map { RecordedSegment(timestamp: $0.mtime, fileURL: $0.url) }
    }

    private func resetConnectionContext() {
        writeCharacteristic = nil
        notifyCharacteristic = nil
        batteryCharacteristic = nil
        buttonCharacteristic = nil
        firmwareRevisionCharacteristic = nil
        dfuControlPointCharacteristic = nil
        pendingAudioFrame = Data()
        detectedCodec = nil
        audioFramesCaptured = 0
        batteryLevel = nil
        lastButtonEvent = nil
        lastLoggedBatteryLevel = nil
        lastLoggedButtonEvent = nil
        lastLoggedCodecId = nil
        lastPingDate = nil
        lastPongDate = nil
        liveWaveform = []
        livePCMBuffer.removeAll(keepingCapacity: false)
        firmwareRevision = nil
        hardwareRevision = nil
    }

    private func log(_ message: String, kind: LogEntry.Kind = .info) {
        DispatchQueue.main.async {
            self.logs.append(LogEntry(message: message, kind: kind))
            if self.logs.count > self.logLimit {
                self.logs.removeFirst(self.logs.count - self.logLimit)
            }
        }
    }

    // Public helper so other views can surface important status into the BLE log panel.
    func postLog(_ message: String) {
        log(message, kind: .info)
    }

    private func persistLastPeripheral(_ uuid: UUID) {
        UserDefaults.standard.set(uuid.uuidString, forKey: lastPeripheralKey)
    }

    private func loadLastPeripheralUUID() -> UUID? {
        if let s = UserDefaults.standard.string(forKey: lastPeripheralKey) {
            return UUID(uuidString: s)
        }
        return nil
    }

    private func autoReconnectIfPossible() {
        guard !isPreview else { return }
        guard !dfuInProgress else { return }
        guard autoReconnectEnabled else { return }
        guard central?.state == .poweredOn else { return }
        guard let uuid = loadLastPeripheralUUID() else { return }

        // Try to retrieve from cache
        if let peripherals = central?.retrievePeripherals(withIdentifiers: [uuid]), let p = peripherals.first {
            peripheralCache[uuid] = p
            connectionStatus = .connecting(p.sanitizedName)
            connectedPeripheral = p
            p.delegate = self
            central?.connect(p, options: nil)
            log("Auto-connecting to \(p.sanitizedName)")
            return
        }

        // Fallback: scan for the target device and connect when seen
        targetReconnectUUID = uuid
        connectionStatus = .scanning
        central?.scanForPeripherals(withServices: [LightMindBluetoothProfile.audioServiceUUID], options: [CBCentralManagerScanOptionAllowDuplicatesKey: false])
        isScanning = true
        scheduleScanTimeout(duration: 12)
        log("Scanning for last device (\(uuid.uuidString.prefix(8)))")
    }

    private func updateDiscovered(summary: PeripheralSummary) {
        // Update by peripheral ID if we've seen it before
        if let index = discoveredPeripherals.firstIndex(where: { $0.id == summary.id }) {
            discoveredPeripherals[index] = summary
        } else {
            discoveredPeripherals.append(summary)
        }
        discoveredPeripherals.sort { lhs, rhs in
            if lhs.isTarget == rhs.isTarget {
                return lhs.name < rhs.name
            }
            return lhs.isTarget && !rhs.isTarget
        }
    }

    private func describeButtonEvent(_ data: Data) -> String? {
        guard data.count >= 4 else { return nil }
        let code = Int(Int32(littleEndian: data.withUnsafeBytes { $0.load(as: Int32.self) }))
        switch code {
        case 1: return "Single tap"
        case 2: return "Double tap"
        case 3: return "Long press"
        case 4: return "Press"
        case 5: return "Release"
        default: return "Event code \(code)"
        }
    }

    private func codecName(from id: UInt8) -> String {
        switch id {
        case 0: return "(PCM16 16 kHz)"
        case 20: return "(Opus 16 kHz)"
        case 21: return "(Reserved)"
        default: return ""
        }
    }
    
    private func convertPCM8ToPCM16(_ data: Data) -> Data {
        var output = Data(capacity: data.count * 2)
        data.forEach { byte in
            let sample = Int16(Int8(bitPattern: byte)) << 8
            var littleEndianSample = sample.littleEndian
            withUnsafeBytes(of: &littleEndianSample) { output.append(contentsOf: $0) }
        }
        return output
    }

    func play(segment: RecordedSegment) {
        do {
            let data = try Data(contentsOf: segment.fileURL)
            guard !data.isEmpty else {
                log("Segment \(segment.fileURL.lastPathComponent) is empty", kind: .error)
                return
            }
            audioPlayer?.play(pcmData: data)
            log(String(format: "Playing %@ (%.1f KB, PCM16)", segment.timestamp.formatted(date: .omitted, time: .standard), Double(data.count)/1024.0))
        } catch {
            log("Failed to play segment: \(error.localizedDescription)", kind: .error)
        }
    }

    func copyLogsToPasteboard() {
        let formatter = DateFormatter()
        formatter.timeStyle = .medium
        formatter.dateStyle = .none
        let text = logs.map { entry in
            "\(formatter.string(from: entry.timestamp)) – \(entry.message)"
        }.joined(separator: "\n")
        UIPasteboard.general.string = text
        log("Copied \(logs.count) log entries to clipboard")
    }

    func clearSegments() {
        for seg in recorder.segments {
            try? FileManager.default.removeItem(at: seg.fileURL)
        }
        recorder.reset()
        recordedSegments = []
        log("Cleared recorded segments")
    }

    private func populatePreviewData() {
        discoveredPeripherals = [
            PeripheralSummary(id: UUID(), name: "LightMind Alpha", rssi: -48, isTarget: true),
            PeripheralSummary(id: UUID(), name: "LightMind Beta", rssi: -71, isTarget: true)
        ]
        connectionStatus = .connected("LightMind Alpha")
        logs = [
            LogEntry(message: "Preview log", kind: .info),
            LogEntry(message: "TX: ping", kind: .outbound),
            LogEntry(message: "RX: pong", kind: .inbound)
        ]
    }

    private func appendFrameToLivePCM(_ frame: Data) {
        liveWaveformQueue.async {
            // Append and trim to last 2 seconds
            self.livePCMBuffer.append(frame)
            if self.livePCMBuffer.count > self.livePCMLimitBytes {
                let excess = self.livePCMBuffer.count - self.livePCMLimitBytes
                self.livePCMBuffer.removeFirst(excess)
            }
            let mags = WaveformExtractor.fromPCM16LEAbsolute(data: self.livePCMBuffer, downsampleTo: 200, gain: 4.0)
            DispatchQueue.main.async {
                self.liveWaveform = mags
            }
        }
    }

    private func updateVoiceActivity(with frame: Data) {
        guard frame.count >= 2 else { return }
        frame.withUnsafeBytes { raw in
            guard let base = raw.bindMemory(to: Int16.self).baseAddress else { return }
            let sampleCount = frame.count / 2
            if sampleCount == 0 { return }
            var sumSquares: Double = 0
            for i in 0..<sampleCount {
                let s = Int32(base[i])
                sumSquares += Double(s * s)
            }
            let rms = sqrt(sumSquares / Double(sampleCount))
            let norm = min(1.0, max(0.0, Float(rms) / Float(Int16.max)))

            // Simple exponential smoothing to avoid flicker
            let alpha: Float = 0.9
            vadLevel = alpha * vadLevel + (1 - alpha) * norm
            let speaking = vadLevel > 0.03
            DispatchQueue.main.async {
                self.isSpeaking = speaking
            }
        }
    }
}

extension BLEManager {
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        DispatchQueue.main.async {
            self.powerState = central.state
            self.authorization = CBCentralManager.authorization
        }
        switch central.state {
        case .poweredOn:
            log("Bluetooth ready")
            // Show previously recorded segments for the last device immediately
            if let uuid = loadLastPeripheralUUID() { reloadSegmentsFromStore(for: uuid) }
            autoReconnectIfPossible()
        case .poweredOff:
            log("Bluetooth is powered off", kind: .error)
        case .resetting:
            log("Bluetooth is resetting")
        case .unsupported:
            log("Bluetooth unsupported", kind: .error)
        case .unauthorized:
            log("Bluetooth unauthorized", kind: .error)
        case .unknown:
            fallthrough
        @unknown default:
            log("Bluetooth state unknown")
        }
    }

    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        let nameFromAd = (advertisementData[CBAdvertisementDataLocalNameKey] as? String)?.trimmingCharacters(in: .whitespacesAndNewlines)
        peripheralCache[peripheral.identifier] = peripheral
        let advertisedServices = (advertisementData[CBAdvertisementDataServiceUUIDsKey] as? [CBUUID] ?? []) +
        (advertisementData[CBAdvertisementDataSolicitedServiceUUIDsKey] as? [CBUUID] ?? [])
        let matchesProfile = advertisedServices.contains(LightMindBluetoothProfile.audioServiceUUID)
        let cleanName = nameFromAd?.isEmpty == false ? nameFromAd! : peripheral.sanitizedName
        guard matchesProfile else { return }
        let summary = PeripheralSummary(id: peripheral.identifier,
                                        name: cleanName,
                                        rssi: RSSI.intValue,
                                        isTarget: matchesProfile)
        // Auto-connect to target UUID if we're looking for it. After DFU the identifier may change,
        // so fall back to connecting to the first matching audio device.
        if let target = targetReconnectUUID {
            if peripheral.identifier == target {
                stopScan()
                connectionStatus = .connecting(cleanName)
                connectedPeripheral = peripheral
                peripheral.delegate = self
                central.connect(peripheral, options: nil)
                log("Auto-connecting to \(cleanName)")
            } else if connectedPeripheral == nil {
                stopScan()
                connectionStatus = .connecting(cleanName)
                connectedPeripheral = peripheral
                peripheral.delegate = self
                targetReconnectUUID = nil
                central.connect(peripheral, options: nil)
                log("Auto-connecting to \(cleanName) (new identifier after DFU)")
            }
        }

        DispatchQueue.main.async {
            self.updateDiscovered(summary: summary)
        }
    }

    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        log("Connected to \(peripheral.sanitizedName)")
        connectionStatus = .connected(peripheral.sanitizedName)
        persistLastPeripheral(peripheral.identifier)
        targetReconnectUUID = nil
        // Update recorder device context for persistence
        recorder.setDeviceContext(deviceId: peripheral.identifier.uuidString)
        lastKnownRecorderSegmentCount = recorder.segments.count
        // Load any previously recorded segments for this device from storage/DB
        reloadSegmentsFromStore(for: peripheral.identifier)
        let servicesToDiscover: [CBUUID] = [profile.serviceUUID,
                                            LightMindBluetoothProfile.audioServiceUUID,
                                            LightMindBluetoothProfile.batteryServiceUUID,
                                            LightMindBluetoothProfile.buttonServiceUUID,
                                            LightMindBluetoothProfile.deviceInformationServiceUUID,
                                            LightMindBluetoothProfile.legacyDFUServiceUUID]
        peripheral.discoverServices(servicesToDiscover)
    }

    func centralManager(_ central: CBCentralManager, didFailToConnect peripheral: CBPeripheral, error: Error?) {
        let reason = error?.localizedDescription ?? "Unknown error"
        connectionStatus = .failed(reason)
        log("Failed to connect: \(reason)", kind: .error)
        resetConnectionContext()
    }

    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        let reason = error?.localizedDescription ?? "User initiated"
        log("Disconnected: \(reason)")
        connectionStatus = .idle
        resetConnectionContext()
        // Finalize current file, but keep previously recorded segments visible (reload from store)
        recorder.reset()
        lastKnownRecorderSegmentCount = recorder.segments.count
        reloadSegmentsFromStore(for: peripheral.identifier)
        // Keep lastPeripheral persisted for future auto-reconnect
    }
}

// Background restoration hook (optional)
extension BLEManager: CBCentralManagerDelegate {
    func centralManager(_ central: CBCentralManager, willRestoreState dict: [String : Any]) {
        if let peripherals = dict[CBCentralManagerRestoredStatePeripheralsKey] as? [CBPeripheral], let p = peripherals.first {
            peripheralCache[p.identifier] = p
            connectedPeripheral = p
            p.delegate = self
            connectionStatus = .connecting(p.sanitizedName)
            central.connect(p, options: nil)
            log("Restoring connection to \(p.sanitizedName)")
        }
    }
}

extension BLEManager: CBPeripheralDelegate {
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if let error {
            log("Service discovery error: \(error.localizedDescription)", kind: .error)
            connectionStatus = .failed(error.localizedDescription)
            return
        }
        guard let services = peripheral.services else { return }
        for service in services {
            switch service.uuid {
            case profile.serviceUUID:
                peripheral.discoverCharacteristics([profile.writeCharacteristicUUID, profile.notifyCharacteristicUUID], for: service)
            case LightMindBluetoothProfile.audioServiceUUID:
                peripheral.discoverCharacteristics([LightMindBluetoothProfile.audioDataCharacteristicUUID,
                                                    LightMindBluetoothProfile.audioCodecCharacteristicUUID],
                                                   for: service)
            case LightMindBluetoothProfile.batteryServiceUUID:
                peripheral.discoverCharacteristics([LightMindBluetoothProfile.batteryLevelCharacteristicUUID], for: service)
            case LightMindBluetoothProfile.buttonServiceUUID:
                peripheral.discoverCharacteristics([LightMindBluetoothProfile.buttonCharacteristicUUID], for: service)
            case LightMindBluetoothProfile.deviceInformationServiceUUID:
                peripheral.discoverCharacteristics([
                    LightMindBluetoothProfile.firmwareRevisionCharacteristicUUID,
                    LightMindBluetoothProfile.hardwareRevisionCharacteristicUUID
                ], for: service)
            case LightMindBluetoothProfile.legacyDFUServiceUUID:
                peripheral.discoverCharacteristics([LightMindBluetoothProfile.legacyDFUControlPointUUID], for: service)
            default:
                break
            }
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        if let error {
            log("Characteristic discovery error: \(error.localizedDescription)", kind: .error)
            connectionStatus = .failed(error.localizedDescription)
            return
        }
        guard let characteristics = service.characteristics else { return }
        for characteristic in characteristics {
            switch characteristic.uuid {
            case profile.writeCharacteristicUUID:
                writeCharacteristic = characteristic
                log("Write characteristic ready")
            case profile.notifyCharacteristicUUID:
                notifyCharacteristic = characteristic
                peripheral.setNotifyValue(true, for: characteristic)
                log("Listening for notifications")
            case LightMindBluetoothProfile.audioDataCharacteristicUUID:
                notifyCharacteristic = characteristic
                peripheral.setNotifyValue(true, for: characteristic)
                log("Listening for audio stream")
            case LightMindBluetoothProfile.audioCodecCharacteristicUUID:
                peripheral.readValue(for: characteristic)
                log("Reading audio codec info")
            case LightMindBluetoothProfile.batteryLevelCharacteristicUUID:
                batteryCharacteristic = characteristic
                peripheral.readValue(for: characteristic)
                peripheral.setNotifyValue(true, for: characteristic)
                log("Subscribed to battery level")
            case LightMindBluetoothProfile.buttonCharacteristicUUID:
                buttonCharacteristic = characteristic
                peripheral.setNotifyValue(true, for: characteristic)
                log("Listening for button events")
            case LightMindBluetoothProfile.firmwareRevisionCharacteristicUUID:
                firmwareRevisionCharacteristic = characteristic
                peripheral.readValue(for: characteristic)
                log("Reading firmware revision")
            case LightMindBluetoothProfile.hardwareRevisionCharacteristicUUID:
                hardwareRevisionCharacteristic = characteristic
                peripheral.readValue(for: characteristic)
                log("Reading hardware revision")
            case LightMindBluetoothProfile.legacyDFUControlPointUUID:
                dfuControlPointCharacteristic = characteristic
                log("DFU control point available")
            default:
                break
            }
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        if let error {
            log("Value update error: \(error.localizedDescription)", kind: .error)
            return
        }
        guard let data = characteristic.value else { return }

        switch characteristic.uuid {
        case profile.notifyCharacteristicUUID:
            handle(value: data)
        case LightMindBluetoothProfile.audioDataCharacteristicUUID:
            handleAudioPacket(data)
        case LightMindBluetoothProfile.batteryLevelCharacteristicUUID:
            let level = data.first
            batteryLevel = level
            if let level, level != lastLoggedBatteryLevel {
                lastLoggedBatteryLevel = level
                log("Battery: \(level)%")
            }
        case LightMindBluetoothProfile.buttonCharacteristicUUID:
            if let event = describeButtonEvent(data) {
                lastButtonEvent = event
                if event != lastLoggedButtonEvent {
                    lastLoggedButtonEvent = event
                    log("Button: \(event)")
                }
            }
        case LightMindBluetoothProfile.audioCodecCharacteristicUUID:
            if let codecId = data.first {
                detectedCodec = codecId
                codecDescription = codecName(from: codecId)
                if codecId != lastLoggedCodecId {
                    lastLoggedCodecId = codecId
                    log("Codec ID: \(codecId) \(codecDescription ?? "")")
                }
            }
        case LightMindBluetoothProfile.firmwareRevisionCharacteristicUUID:
            if let s = String(data: data, encoding: .utf8) {
                firmwareRevision = s.trimmingCharacters(in: .whitespacesAndNewlines)
                log("Firmware: \(firmwareRevision!)")
            }
        case LightMindBluetoothProfile.hardwareRevisionCharacteristicUUID:
            if let s = String(data: data, encoding: .utf8) {
                hardwareRevision = s.trimmingCharacters(in: .whitespacesAndNewlines)
                log("Hardware: \(hardwareRevision!)")
            }
        default:
            break
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didWriteValueFor characteristic: CBCharacteristic, error: Error?) {
        if let error {
            log("Write failed: \(error.localizedDescription)", kind: .error)
        } else {
            log("Write acknowledged")
        }
    }
}

private extension CBPeripheral {
    var sanitizedName: String {
        name?.isEmpty == false ? name! : "LightMind"
    }
}
