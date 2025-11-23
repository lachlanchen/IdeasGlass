import SwiftUI

struct RootTabView: View {
    @EnvironmentObject private var bleManager: BLEManager

    var body: some View {
        TabView {
            ContentView()
                .environmentObject(bleManager)
                .tabItem {
                    Label("Live", systemImage: "waveform.path.ecg")
                }

            PlaceholderScreen(title: "Memory",
                              subtitle: "Memory view coming soon.")
                .tabItem {
                    Label("Memory", systemImage: "archivebox")
                }

            PlaceholderScreen(title: "Command",
                              subtitle: "Command view coming soon.")
                .tabItem {
                    Label("Command", systemImage: "terminal")
                }

            PlaceholderScreen(title: "Settings",
                              subtitle: "Settings view coming soon.")
                .tabItem {
                    Label("Settings", systemImage: "gearshape")
                }
        }
    }
}

private struct PlaceholderScreen: View {
    let title: String
    let subtitle: String

    var body: some View {
        NavigationStack {
            VStack(spacing: 12) {
                Text(title)
                    .font(.title2.bold())
                Text(subtitle)
                    .font(.body)
                    .foregroundStyle(.secondary)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(Color(.systemGroupedBackground))
            .navigationTitle(title)
        }
    }
}

#Preview {
    RootTabView()
        .environmentObject(BLEManager(profile: .nordicUART, makePreviewData: true))
}

