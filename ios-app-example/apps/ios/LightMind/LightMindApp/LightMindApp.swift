import SwiftUI
import AVFoundation

@main
struct LightMindApp: App {
    @StateObject private var bleManager = BLEManager()

    var body: some Scene {
        WindowGroup {
            RootTabView()
                .environmentObject(bleManager)
        }
    }

    init() {
        // Initialize local persistence (folders, DB if available)
        Persistence.bootstrap()
        // Configure audio session for playback to ensure audibility
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default, options: [.mixWithOthers])
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Audio session setup failed: \(error)")
        }
    }
}
