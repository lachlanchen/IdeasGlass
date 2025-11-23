import SwiftUI

struct RecordingsListView: View {
    @EnvironmentObject private var bleManager: BLEManager
    @State private var visibleCount: Int = 20

    var body: some View {
        List {
            if !bleManager.recordedSegments.isEmpty {
                Section {
                    Button(role: .destructive) {
                        bleManager.clearSegments()
                    } label: {
                        Label("Clear Segments", systemImage: "trash")
                    }
                }
            }
            Section("Recordings") {
                if bleManager.recordedSegments.isEmpty {
                    Text("No segments yet")
                        .foregroundStyle(.secondary)
                } else {
                    let segments = Array(bleManager.recordedSegments.prefix(visibleCount))
                    ForEach(segments, id: \.id) { segment in
                        NavigationLink(value: segment) {
                            HStack {
                                VStack(alignment: .leading) {
                                    Text(segment.timestamp, style: .time)
                                    Text(segment.fileURL.lastPathComponent)
                                        .font(.caption2)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                                Label("Play", systemImage: "play.fill")
                                    .font(.callout)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.blue.opacity(0.1))
                                    .clipShape(Capsule())
                            }
                        }
                    }
                    if bleManager.recordedSegments.count > visibleCount {
                        Button {
                            loadMore()
                        } label: {
                            Label("More", systemImage: "ellipsis.circle")
                                .frame(maxWidth: .infinity, alignment: .center)
                        }
                        .onAppear {
                            // Auto lazy-load when the More button scrolls into view.
                            loadMore()
                        }
                    }
                }
            }
        }
        .navigationTitle("Recordings")
    }

    private func loadMore() {
        let total = bleManager.recordedSegments.count
        guard visibleCount < total else { return }
        let step = 20
        visibleCount = min(total, visibleCount + step)
    }
}

#Preview {
    NavigationStack {
        RecordingsListView()
            .environmentObject(BLEManager(profile: .nordicUART, makePreviewData: true))
    }
}
