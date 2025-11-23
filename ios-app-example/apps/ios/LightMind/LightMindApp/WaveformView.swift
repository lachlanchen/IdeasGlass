import SwiftUI

struct WaveformView: View {
    // normalized 0...1 magnitudes, already scaled
    let samples: [Float]
    var color: Color = .accentColor
    var background: Color = .clear
    var barWidth: CGFloat = 2.0
    var spacing: CGFloat = 1.0
    // Optional playhead progress (0...1)
    var progress: Double? = nil

    var body: some View {
        GeometryReader { geometry in
            Canvas { context, size in
                guard !samples.isEmpty else { return }
                let w = size.width
                let h = size.height
                let totalBar = barWidth + spacing
                let count = min(samples.count, Int((w / totalBar).rounded(.down)))
                if count == 0 { return }

                for i in 0..<count {
                    let mag = max(0, min(1, CGFloat(samples[i])))
                    let halfBar = max(1, mag * (h / 2))
                    let x = CGFloat(i) * totalBar
                    let rect = CGRect(x: x,
                                      y: (h/2 - halfBar),
                                      width: barWidth,
                                      height: halfBar * 2)
                    context.fill(Path(rect), with: .color(color.opacity(0.9)))
                }

                // Draw playhead if progress provided
                if let p = progress {
                    let clamped = max(0.0, min(1.0, p))
                    let x = CGFloat(clamped) * w
                    var path = Path()
                    path.move(to: CGPoint(x: x, y: 0))
                    path.addLine(to: CGPoint(x: x, y: h))
                    context.stroke(path, with: .color(.red.opacity(0.85)), lineWidth: 2)
                }
            }
            .background(background)
        }
        .frame(minHeight: 60)
        .accessibilityLabel("Waveform")
    }
}

enum WaveformExtractor {
    // Produces a normalized RMS waveform with per-file normalization (robust against outliers)
    static func fromPCM16LEAdaptive(data: Data, downsampleTo targetCount: Int = 512) -> [Float] {
        if data.isEmpty || targetCount <= 0 { return [] }
        let sampleCount = data.count / 2
        if sampleCount == 0 { return [] }

        var peaks: [Float] = []
        peaks.reserveCapacity(targetCount)

        let samplesPerBin = max(1, sampleCount / targetCount)
        data.withUnsafeBytes { raw in
            guard let base = raw.bindMemory(to: Int16.self).baseAddress else { return }
            var idx = 0
            while idx < sampleCount {
                let end = min(sampleCount, idx + samplesPerBin)
                var sumSquares: Double = 0
                var localMax: Int32 = 0
                var i = idx
                while i < end {
                    let s = Int32(base[i])
                    let absVal = s == Int32(Int16.min) ? Int32(Int16.max) : abs(s)
                    if absVal > localMax { localMax = absVal }
                    sumSquares += Double(s) * Double(s)
                    i += 1
                }
                // RMS to capture loudness better than peak
                let n = max(1, end - idx)
                let rms = sqrt(sumSquares / Double(n))
                let norm = Float(rms) / Float(Int16.max)
                // Keep both measures; use peak as a floor so very quiet bins still visible
                let peakNorm = Float(localMax) / Float(Int16.max)
                peaks.append(max(norm, 0.2 * peakNorm))
                idx = end
            }
        }
        // Normalize across file using 95th percentile to avoid single-sample clipping
        let sorted = peaks.sorted()
        let idx95 = min(max(0, Int(Double(sorted.count) * 0.95) - 1), sorted.count - 1)
        let scale = max(0.0001, sorted.isEmpty ? 1.0 : sorted[idx95])
        return peaks.map { min(1.0, $0 / scale) }
    }

    // Absolute scaling against Int16.max with optional gain multiplier.
    // Quiet audio stays visually quiet instead of filling full height.
    static func fromPCM16LEAbsolute(data: Data, downsampleTo targetCount: Int = 512, gain: Float = 4.0) -> [Float] {
        if data.isEmpty || targetCount <= 0 { return [] }
        let sampleCount = data.count / 2
        if sampleCount == 0 { return [] }

        var mags: [Float] = []
        mags.reserveCapacity(targetCount)

        let samplesPerBin = max(1, sampleCount / targetCount)
        data.withUnsafeBytes { raw in
            guard let base = raw.bindMemory(to: Int16.self).baseAddress else { return }
            var idx = 0
            while idx < sampleCount {
                let end = min(sampleCount, idx + samplesPerBin)
                var sumSquares: Double = 0
                var localMax: Int32 = 0
                var i = idx
                while i < end {
                    let s = Int32(base[i])
                    let absVal = s == Int32(Int16.min) ? Int32(Int16.max) : abs(s)
                    if absVal > localMax { localMax = absVal }
                    sumSquares += Double(s) * Double(s)
                    i += 1
                }
                let n = max(1, end - idx)
                let rms = sqrt(sumSquares / Double(n))
                let rmsNorm = Float(rms) / Float(Int16.max)
                let peakNorm = Float(localMax) / Float(Int16.max)
                // Blend RMS with a fraction of the peak to better reflect short transients (e.g., coughs)
                var norm = max(rmsNorm, 0.35 * peakNorm)
                norm = min(1.0, max(0.0, norm * gain))
                mags.append(norm)
                idx = end
            }
        }
        return mags
    }
}
