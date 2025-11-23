import Foundation
import AVFoundation

#if canImport(Opus)
import Opus

final class OpusDecodeService {
    private let decoder: Opus.Decoder
    private let outputFormat: AVAudioFormat

    init?() {
        guard let fmt = AVAudioFormat(commonFormat: .pcmFormatInt16, sampleRate: 16_000, channels: 1, interleaved: true) else {
            return nil
        }
        outputFormat = fmt
        do {
            decoder = try Opus.Decoder(format: fmt)
        } catch {
            return nil
        }
    }

    func decode(_ packet: Data) -> Data? {
        do {
            let buffer = try decoder.decode(packet)
            let frameCount = Int(buffer.frameLength)
            var data = Data(count: frameCount * 2)
            data.withUnsafeMutableBytes { outRaw in
                if let dst = outRaw.bindMemory(to: Int16.self).baseAddress,
                   let src = buffer.int16ChannelData?[0] {
                    dst.update(from: src, count: frameCount)
                }
            }
            return data
        } catch {
            return nil
        }
    }
}
#else
final class OpusDecodeService {
    init?() { return nil }
    func decode(_ packet: Data) -> Data? { return nil }
}
#endif
