import SwiftUI
import AVFoundation

struct SegmentDetailView: View {
    @EnvironmentObject private var bleManager: BLEManager
    let segment: RecordedSegment

    @State private var waveform: [Float] = []
    @State private var fileSize: Int = 0
    @State private var isLoading: Bool = false
    @State private var duration: TimeInterval = 0
    @State private var player: AVAudioPlayer?
    @State private var isPlaying: Bool = false
    @State private var playProgress: Double = 0
    @State private var progressTimer: Timer?
    @State private var waveformTimer: Timer?
    @State private var currentURL: URL? = nil
    @State private var errorMessage: String?

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Group {
                    if isLoading {
                        ProgressView("Loading waveform…")
                    } else if waveform.isEmpty {
                        Text("No audio data available")
                            .foregroundStyle(.secondary)
                    } else {
                        WaveformView(samples: waveform, progress: isPlaying ? playProgress : nil)
                            .frame(height: 120)
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(.quaternary)
                            )
                    }
                }

                LabeledContent("Created") {
                    Text(segment.timestamp.formatted(date: .omitted, time: .standard))
                }
                LabeledContent("Size") {
                    Text(sizeText(bytes: fileSize))
                }
                LabeledContent("Duration") {
                    Text(String(format: "%.1f s", duration))
                }

                HStack(spacing: 12) {
                    Button {
                        togglePlay()
                    } label: {
                        Label(isPlaying ? "Pause" : "Play", systemImage: isPlaying ? "pause.fill" : "play.fill")
                    }
                    .buttonStyle(.borderedProminent)

                    Button {
                        reloadWaveform()
                    } label: {
                        Label("Refresh", systemImage: "arrow.clockwise")
                    }
                    .buttonStyle(.bordered)
                }
                // Simple progress bar
                VStack(alignment: .leading) {
                    Slider(value: Binding(get: {
                        playProgress
                    }, set: { newVal in
                        playProgress = newVal
                        if let p = player {
                            p.currentTime = newVal * (p.duration > 0 ? p.duration : duration)
                        }
                    }))
                    .disabled(player == nil)
                    if let msg = errorMessage {
                        Text(msg)
                            .font(.footnote)
                            .foregroundStyle(.red)
                    }
                }
            }
            .padding()
        }
        .navigationTitle("Recording")
        .onAppear(perform: reload)
        .onDisappear {
            stopPlayback()
            stopWaveformTimer()
        }
    }

    private func reload() {
        isLoading = true
        DispatchQueue.global(qos: .userInitiated).async {
            let url = resolveCurrentURL()
            let data = (try? Data(contentsOf: url)) ?? Data()
            // Use absolute scaling (matches live waveform visual) and same density as live
            let mags = WaveformExtractor.fromPCM16LEAbsolute(data: data, downsampleTo: 200, gain: 4.0)
            let size = data.count
            let samples = size / 2
            let dur = Double(samples) / 16_000.0
            DispatchQueue.main.async {
                self.waveform = mags
                self.fileSize = size
                self.duration = dur
                self.isLoading = false
                // If this segment is still active (growing), keep refreshing
                if bleManager.inProgressFileURL == url {
                    startWaveformTimer()
                } else {
                    stopWaveformTimer()
                }
            }
        }
    }

    private func reloadWaveform() { reload() }

    private func togglePlay() {
        if isPlaying {
            player?.pause()
            isPlaying = false
            return
        }
        let url = resolveCurrentURL()
        // Create a WAV file from the PCM segment to use AVAudioPlayer UI comfortably
        do {
            guard FileManager.default.fileExists(atPath: url.path) else {
                let msg = "Audio file not found: \(url.lastPathComponent)"
                errorMessage = msg
                bleManager.postLog(msg)
                return
            }
            let data = try Data(contentsOf: url)
            guard !data.isEmpty else {
                let msg = "Audio file is empty: \(url.lastPathComponent)"
                errorMessage = msg
                bleManager.postLog(msg)
                return
            }
            let wavURL = try AudioWAVExporter.writeWAV(fromPCM16: data,
                                                       sampleRate: 16_000,
                                                       channels: 1,
                                                       fileName: url.deletingPathExtension().lastPathComponent + ".wav")
            player = try AVAudioPlayer(contentsOf: wavURL)
            player?.prepareToPlay()
            player?.play()
            isPlaying = true
            errorMessage = nil
            startProgressTimer()
        } catch {
            let msg = "Play error for \(url.lastPathComponent): \(error.localizedDescription)"
            errorMessage = msg
            bleManager.postLog(msg)
            // fall back to BLEManager play if something goes wrong
            bleManager.play(segment: segment)
        }
    }

    private func startProgressTimer() {
        progressTimer?.invalidate()
        progressTimer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { _ in
            guard let p = player else { return }
            let dur = p.duration > 0 ? p.duration : max(0.0001, duration)
            playProgress = min(1.0, max(0.0, p.currentTime / dur))
            if !p.isPlaying { isPlaying = false }
        }
    }

    private func stopPlayback() {
        progressTimer?.invalidate()
        progressTimer = nil
        player?.stop()
        isPlaying = false
    }

    private func startWaveformTimer() {
        waveformTimer?.invalidate()
        waveformTimer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            // Recompute waveform for growing file (absolute scaling to match live)
            DispatchQueue.global(qos: .userInitiated).async {
                let url = resolveCurrentURL()
                let data = (try? Data(contentsOf: url)) ?? Data()
                let mags = WaveformExtractor.fromPCM16LEAbsolute(data: data, downsampleTo: 200, gain: 4.0)
                let size = data.count
                let samples = size / 2
                let dur = Double(samples) / 16_000.0
                DispatchQueue.main.async {
                    self.waveform = mags
                    self.fileSize = size
                    self.duration = dur
                }
            }
        }
    }

    private func stopWaveformTimer() {
        waveformTimer?.invalidate()
        waveformTimer = nil
    }

    private func sizeText(bytes: Int) -> String {
        if bytes < 1024 { return "\(bytes) B" }
        let kb = Double(bytes) / 1024.0
        if kb < 1024 { return String(format: "%.1f KB", kb) }
        return String(format: "%.2f MB", kb / 1024.0)
    }
}

// MARK: - Resolve moved file paths
extension SegmentDetailView {
    private func resolveCurrentURL() -> URL {
        // If we already have a working URL and it exists, keep it.
        if let u = currentURL, FileManager.default.fileExists(atPath: u.path) { return u }

        // Start with the original
        var candidate = segment.fileURL
        if FileManager.default.fileExists(atPath: candidate.path) {
            currentURL = candidate
            return candidate
        }

        // Try to find the segment by timestamp among recordedSegments (accounts for moved file)
        let targetTs = segment.timestamp
        if let match = bleManager.recordedSegments.first(where: { abs($0.timestamp.timeIntervalSince(targetTs)) < 2.0 }) {
            candidate = match.fileURL
            if FileManager.default.fileExists(atPath: candidate.path) {
                currentURL = candidate
                return candidate
            }
        }

        // Fallback: scan disk for most recent file near the timestamp
        if let url = try? findFileNear(timestamp: targetTs) {
            currentURL = url
            return url
        }
        // As a last resort, return original
        currentURL = segment.fileURL
        return segment.fileURL
    }

    private func findFileNear(timestamp: Date) throws -> URL? {
        let root = try Paths.segmentsRoot()
        let fm = FileManager.default
        guard let enumerator = fm.enumerator(at: root, includingPropertiesForKeys: [.contentModificationDateKey, .isRegularFileKey], options: [.skipsHiddenFiles]) else { return nil }
        var best: (url: URL, dt: TimeInterval)?
        for case let url as URL in enumerator {
            guard let values = try? url.resourceValues(forKeys: [.isRegularFileKey, .contentModificationDateKey]), values.isRegularFile == true else { continue }
            let mtime = values.contentModificationDate ?? .distantPast
            let dt = abs(mtime.timeIntervalSince(timestamp))
            if best == nil || dt < best!.dt { best = (url, dt) }
        }
        return best?.url
    }
}
