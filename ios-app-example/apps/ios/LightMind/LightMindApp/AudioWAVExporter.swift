import Foundation

enum AudioWAVExporter {
    // Writes a WAV file for PCM16 LE mono data at given sampleRate
    // Returns the URL of the written file
    static func writeWAV(fromPCM16 data: Data, sampleRate: Int = 16_000, channels: Int = 1, fileName: String? = nil) throws -> URL {
        let bytesPerSample = 2
        let byteRate = sampleRate * channels * bytesPerSample
        let blockAlign = channels * bytesPerSample
        let dataSize = UInt32(data.count)
        let riffChunkSize = UInt32(36) + dataSize

        var wav = Data(capacity: Int(44 + data.count))
        func append(_ s: String) { wav.append(s.data(using: .ascii)!) }
        func appendLE32(_ v: UInt32) { var x = v.littleEndian; withUnsafeBytes(of: &x) { wav.append(contentsOf: $0) } }
        func appendLE16(_ v: UInt16) { var x = v.littleEndian; withUnsafeBytes(of: &x) { wav.append(contentsOf: $0) } }

        append("RIFF")
        appendLE32(riffChunkSize)
        append("WAVE")
        append("fmt ")
        appendLE32(16)                        // PCM header size
        appendLE16(1)                         // PCM format
        appendLE16(UInt16(channels))
        appendLE32(UInt32(sampleRate))
        appendLE32(UInt32(byteRate))
        appendLE16(UInt16(blockAlign))
        appendLE16(16)                        // bits per sample
        append("data")
        appendLE32(dataSize)
        wav.append(data)

        let name = fileName ?? "lightmind_\(Int(Date().timeIntervalSince1970)).wav"
        let url = FileManager.default.temporaryDirectory.appendingPathComponent(name)
        try wav.write(to: url, options: .atomic)
        return url
    }
}

