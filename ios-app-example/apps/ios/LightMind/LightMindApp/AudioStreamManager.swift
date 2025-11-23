import Foundation
import AVFoundation

final class AudioStreamManager {
    private let engine = AVAudioEngine()
    private let player = AVAudioPlayerNode()
    private let inputFormat: AVAudioFormat
    private let playbackFormat: AVAudioFormat
    private let queue = DispatchQueue(label: "audio-playback-queue")

    init?(sampleRate: Double, channels: AVAudioChannelCount = 1) {
        guard let format = AVAudioFormat(commonFormat: .pcmFormatInt16,
                                         sampleRate: sampleRate,
                                         channels: channels,
                                         interleaved: true) else {
            return nil
        }
        self.inputFormat = format
        engine.attach(player)
        engine.connect(player, to: engine.mainMixerNode, format: nil)
        do {
            try engine.start()
        } catch {
            print("Audio engine failed to start: \(error)")
            return nil
        }
        self.playbackFormat = player.outputFormat(forBus: 0)
    }

    func play(pcmData: Data) {
        queue.async {
            let bytesPerFrame = max(1, Int(self.inputFormat.streamDescription.pointee.mBytesPerFrame))
            let frameCount = UInt32(pcmData.count / bytesPerFrame)
            guard frameCount > 0 else { return }
            guard let buffer = AVAudioPCMBuffer(pcmFormat: self.playbackFormat, frameCapacity: frameCount) else { return }
            buffer.frameLength = frameCount

            pcmData.withUnsafeBytes { rawBuffer in
                guard let src = rawBuffer.bindMemory(to: Int16.self).baseAddress else { return }
                switch self.playbackFormat.commonFormat {
                case .pcmFormatFloat32:
                    guard let dest = buffer.floatChannelData else { return }
                    let scale: Float = 1.0 / Float(Int16.max)
                    for frame in 0..<Int(frameCount) {
                        let sample = Float(src[frame]) * scale
                        for channel in 0..<Int(self.playbackFormat.channelCount) {
                            dest[channel][frame] = sample
                        }
                    }
                case .pcmFormatInt16:
                    guard let dest = buffer.int16ChannelData else { return }
                    for channel in 0..<Int(self.playbackFormat.channelCount) {
                        dest[channel].update(from: src, count: Int(frameCount))
                    }
                default:
                    return
                }
            }

            self.player.scheduleBuffer(buffer, completionHandler: nil)
            if !self.player.isPlaying {
                self.player.play()
            }
        }
    }
}
