import Foundation

struct RecordedSegment: Identifiable, Hashable {
    let id = UUID()
    let timestamp: Date
    var fileURL: URL
}

final class AudioRecorder {
    private(set) var segments: [RecordedSegment] = []
    private var writer: FileHandle?
    private var currentURL: URL?
    private var bytesWrittenInCurrent: Int = 0

    // Rotation based on time at 16kHz mono PCM16: bytes/sec = 16000 * 2
    private let sampleRate: Int
    private let channels: Int
    private let segmentDurationSec: Int

    private var rotateThresholdBytes: Int { sampleRate * channels * 2 * segmentDurationSec }

    // Persistence context
    private var deviceId: String = "unknown"
    private let userId: String = "local_user"

    init(sampleRate: Int = 16_000, channels: Int = 1, segmentDurationSec: Int = 60) {
        self.sampleRate = sampleRate
        self.channels = channels
        self.segmentDurationSec = segmentDurationSec
    }

    func setDeviceContext(deviceId: String) {
        self.deviceId = deviceId
    }

    func currentInProgressSegment() -> RecordedSegment? {
        guard writer != nil, let url = currentURL, let last = segments.last else { return nil }
        return last.fileURL == url ? last : nil
    }

    func append(frame data: Data) {
        rotateFileIfNeeded()
        guard let fileHandle = writer else { return }
        fileHandle.write(data)
        bytesWrittenInCurrent += data.count
    }

    func reset(finalizeCurrent: Bool = true) {
        if finalizeCurrent { finalizeCurrentSegment() }
        writer?.closeFile()
        writer = nil
        currentURL = nil
        bytesWrittenInCurrent = 0
        segments.removeAll()
    }

    private func rotateFileIfNeeded() {
        if writer == nil || bytesWrittenInCurrent >= rotateThresholdBytes {
            // Finalize the last segment (move, hash, persist)
            finalizeCurrentSegment()
            bytesWrittenInCurrent = 0
        }
        if writer == nil {
            let url = FileManager.default.temporaryDirectory.appendingPathComponent("lightmind_\(Date().timeIntervalSince1970).pcm")
            FileManager.default.createFile(atPath: url.path, contents: nil)
            writer = try? FileHandle(forWritingTo: url)
            currentURL = url
            segments.append(RecordedSegment(timestamp: Date(), fileURL: url))
        }
    }

    private func finalizeCurrentSegment() {
        guard let url = currentURL else { return }
        // Ensure pending data is flushed and file is closed before hashing/moving
        writer?.closeFile()
        writer = nil
        // No-op if file is empty
        let size = (try? url.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0
        if size == 0 { return }
        // Compute sha256 and move into Application Support/segments
        do {
            let sha = try Hashing.sha256Hex(ofFile: url)
            let ext = url.pathExtension.isEmpty ? "pcm" : url.pathExtension
            let dest = try Paths.contentAddressedPath(for: sha, ext: ext)
            if FileManager.default.fileExists(atPath: dest.path) {
                // Already finalized earlier; ensure our in-memory record points to dest
                if var last = segments.last, last.fileURL == url {
                    last.fileURL = dest
                    segments[segments.count - 1] = last
                }
                try? FileManager.default.removeItem(at: url)
            } else {
                try FileManager.default.moveItem(at: url, to: dest)
                if var last = segments.last, last.fileURL == url {
                    last.fileURL = dest
                    segments[segments.count - 1] = last
                }
            }

            // Build metadata and upsert into repository
            let durationSec = Double(size) / Double(sampleRate * channels * 2)
            let meta = SegmentMeta(
                id: SegmentId.make(deviceId: deviceId, timestamp: segments.last?.timestamp ?? Date(), fileSha256: sha),
                userId: userId,
                deviceId: deviceId,
                timestamp: segments.last?.timestamp ?? Date(),
                durationMs: Int(durationSec * 1000.0),
                codec: "pcm16",
                sampleRate: sampleRate,
                channels: channels,
                fileSha256: sha,
                fileExt: ext,
                sizeBytes: size,
                filePath: dest.path,
                state: SegmentState.recorded.rawValue
            )
            try? Repositories.segments.upsert(meta)
        } catch {
            // Best effort: keep temp file and log via print; UI log path can be added later
            print("Finalize segment failed: \(error)")
        }
    }
}
