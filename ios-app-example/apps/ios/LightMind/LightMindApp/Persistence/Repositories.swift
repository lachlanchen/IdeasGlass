import Foundation
#if canImport(CryptoKit)
import CryptoKit
#endif

struct SegmentMeta {
    let id: String
    let userId: String
    let deviceId: String
    let timestamp: Date
    let durationMs: Int
    let codec: String
    let sampleRate: Int
    let channels: Int
    let fileSha256: String
    let fileExt: String
    let sizeBytes: Int
    let filePath: String
    let state: String
}

enum SegmentState: String { case recorded, queued, uploading, uploaded, failed }

enum PersistenceError: Error { case notAvailable }

protocol SegmentRepositoryType {
    func upsert(_ meta: SegmentMeta) throws
    func recentSegments(for deviceId: String, limit: Int) throws -> [SegmentMeta]
}

protocol DeviceRepositoryType {
    func upsert(id: String, name: String?, platformIdentifier: String?, fw: String?, hw: String?, lastSeen: Date) throws
}

protocol SettingsRepositoryType {
    func ensureDefaultUser() throws
}

/// Unified façade returning GRDB-backed implementations if available, otherwise no-op stubs.
enum Repositories {
    static var segments: SegmentRepositoryType { _segments }
    static var devices: DeviceRepositoryType { _devices }
    static var settings: SettingsRepositoryType { _settings }

    #if canImport(GRDB)
    private static let _segments: SegmentRepositoryType = GRDBSegmentRepository()
    private static let _devices: DeviceRepositoryType = GRDBDeviceRepository()
    private static let _settings: SettingsRepositoryType = GRDBSettingsRepository()
    #else
    private static let _segments: SegmentRepositoryType = StubSegmentRepository()
    private static let _devices: DeviceRepositoryType = StubDeviceRepository()
    private static let _settings: SettingsRepositoryType = StubSettingsRepository()
    #endif
}

#if canImport(GRDB)
import GRDB

struct GRDBSegmentRepository: SegmentRepositoryType {
    func upsert(_ meta: SegmentMeta) throws {
        let dbq = try DatabaseManager.shared.queue()
        try dbq.write { db in
            let now = Date()
            try db.execute(sql: """
INSERT INTO segments (id,user_id,device_id,timestamp,duration_ms,codec,sample_rate,channels,file_sha256,file_ext,size_bytes,file_path,state,created_at,updated_at)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
ON CONFLICT(id) DO UPDATE SET
user_id=excluded.user_id, device_id=excluded.device_id, timestamp=excluded.timestamp,
duration_ms=excluded.duration_ms, codec=excluded.codec, sample_rate=excluded.sample_rate,
channels=excluded.channels, file_sha256=excluded.file_sha256, file_ext=excluded.file_ext,
size_bytes=excluded.size_bytes, file_path=excluded.file_path, state=excluded.state,
updated_at=?
""",
                           arguments: [meta.id, meta.userId, meta.deviceId, meta.timestamp, meta.durationMs,
                                       meta.codec, meta.sampleRate, meta.channels, meta.fileSha256, meta.fileExt,
                                       meta.sizeBytes, meta.filePath, meta.state, now, now, now])
        }
    }

    func recentSegments(for deviceId: String, limit: Int) throws -> [SegmentMeta] {
        let dbq = try DatabaseManager.shared.queue()
        return try dbq.read { db in
            let rows = try Row.fetchAll(db, sql: "SELECT * FROM segments WHERE device_id = ? ORDER BY timestamp DESC LIMIT ?", arguments: [deviceId, limit])
            return rows.map { row in
                SegmentMeta(id: row["id"],
                            userId: row["user_id"],
                            deviceId: row["device_id"],
                            timestamp: row["timestamp"],
                            durationMs: row["duration_ms"],
                            codec: row["codec"],
                            sampleRate: row["sample_rate"],
                            channels: row["channels"],
                            fileSha256: row["file_sha256"],
                            fileExt: row["file_ext"],
                            sizeBytes: row["size_bytes"],
                            filePath: row["file_path"],
                            state: row["state"]) }
        }
    }
}

struct GRDBDeviceRepository: DeviceRepositoryType {
    func upsert(id: String, name: String?, platformIdentifier: String?, fw: String?, hw: String?, lastSeen: Date) throws {
        let dbq = try DatabaseManager.shared.queue()
        try dbq.write { db in
            try db.execute(sql: """
INSERT INTO devices (id,name,platform_identifier,fw_rev,hw_rev,last_seen_at)
VALUES (?,?,?,?,?,?)
ON CONFLICT(id) DO UPDATE SET name=excluded.name, platform_identifier=excluded.platform_identifier,
fw_rev=excluded.fw_rev, hw_rev=excluded.hw_rev, last_seen_at=excluded.last_seen_at
""", arguments: [id, name, platformIdentifier, fw, hw, lastSeen])
        }
    }
}

struct GRDBSettingsRepository: SettingsRepositoryType {
    func ensureDefaultUser() throws { try DatabaseManager.shared.ensureDefaultUser() }
}

#else

// Minimal stubs so the app compiles and runs without GRDB.
final class StubSegmentRepository: SegmentRepositoryType {
    private var items: [SegmentMeta] = []
    func upsert(_ meta: SegmentMeta) throws {
        if let idx = items.firstIndex(where: { $0.id == meta.id }) { items[idx] = meta } else { items.append(meta) }
    }
    func recentSegments(for deviceId: String, limit: Int) throws -> [SegmentMeta] {
        return items.filter { $0.deviceId == deviceId }.sorted { $0.timestamp > $1.timestamp }.prefix(limit).map { $0 }
    }
}

final class StubDeviceRepository: DeviceRepositoryType {
    func upsert(id: String, name: String?, platformIdentifier: String?, fw: String?, hw: String?, lastSeen: Date) throws {}
}

struct StubSettingsRepository: SettingsRepositoryType { func ensureDefaultUser() throws {} }

#endif

// Helpers
enum SegmentId {
    static func make(deviceId: String, timestamp: Date, fileSha256: String) -> String {
        // Deterministic, simple: sha256 of concatenation, hex
        let s = "\(deviceId)|\(Int(timestamp.timeIntervalSince1970 * 1000))|\(fileSha256)"
        if let d = s.data(using: .utf8) {
            let hex = d.sha256Hex()
            return hex
        }
        return UUID().uuidString
    }
}

private extension Data {
    func sha256Hex() -> String {
        #if canImport(CryptoKit)
        let digest = SHA256.hash(data: self)
        return digest.map { String(format: "%02x", $0) }.joined()
        #else
        return UUID().uuidString.replacingOccurrences(of: "-", with: "")
        #endif
    }
}
