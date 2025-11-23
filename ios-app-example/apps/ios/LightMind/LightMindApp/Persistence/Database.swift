import Foundation

#if canImport(GRDB)
import GRDB
#endif

enum Persistence {
    static func bootstrap() {
        // Ensure folders exist
        _ = try? Paths.applicationSupportRoot()
        _ = try? Paths.segmentsRoot()
        #if canImport(GRDB)
        _ = try? DatabaseManager.shared.open()
        _ = try? DatabaseManager.shared.migrate()
        _ = try? DatabaseManager.shared.ensureDefaultUser()
        #endif
    }
}

#if canImport(GRDB)
final class DatabaseManager {
    static let shared = DatabaseManager()
    private init() {}

    private var dbQueue: DatabaseQueue?

    func open() throws {
        if dbQueue != nil { return }
        let dbURL = try Paths.applicationSupportRoot().appendingPathComponent("lightmind.sqlite")
        let config = Configuration()
        dbQueue = try DatabaseQueue(path: dbURL.path, configuration: config)
    }

    func migrate() throws {
        guard let dbQueue else { return }
        var migrator = DatabaseMigrator()
        migrator.registerMigration("v1_init") { db in
            try db.create(table: "users") { t in
                t.column("id", .text).primaryKey()
                t.column("display_name", .text).notNull()
                t.column("created_at", .date).notNull()
                t.column("updated_at", .date).notNull()
            }

            try db.create(table: "devices") { t in
                t.column("id", .text).primaryKey() // device_id
                t.column("name", .text)
                t.column("platform_identifier", .text) // CBPeripheral.identifier
                t.column("fw_rev", .text)
                t.column("hw_rev", .text)
                t.column("last_seen_at", .date)
            }

            try db.create(table: "segments") { t in
                t.column("id", .text).primaryKey()
                t.column("user_id", .text).indexed()
                t.column("device_id", .text).indexed()
                t.column("timestamp", .date).indexed()
                t.column("duration_ms", .integer)
                t.column("codec", .text)
                t.column("sample_rate", .integer)
                t.column("channels", .integer)
                t.column("file_sha256", .text).unique()
                t.column("file_ext", .text)
                t.column("size_bytes", .integer)
                t.column("file_path", .text)
                t.column("state", .text)
                t.column("retry_count", .integer).defaults(to: 0)
                t.column("created_at", .date).notNull()
                t.column("updated_at", .date).notNull()
            }

            try db.execute(sql: "CREATE INDEX segments_device_time ON segments(device_id, timestamp DESC)")

            try db.create(table: "uploads") { t in
                t.column("id", .text).primaryKey()
                t.column("segment_id", .text).unique().indexed()
                t.column("status", .text).notNull()
                t.column("attempts", .integer).defaults(to: 0)
                t.column("last_error", .text)
                t.column("created_at", .date).notNull()
                t.column("updated_at", .date).notNull()
            }

            try db.create(table: "kv_state") { t in
                t.column("key", .text).primaryKey()
                t.column("value", .text)
                t.column("updated_at", .date).notNull()
            }
        }
        try migrator.migrate(dbQueue)
    }

    func ensureDefaultUser() throws {
        guard let dbQueue else { return }
        try dbQueue.write { db in
            let exists = try Bool.fetchOne(db, sql: "SELECT 1 FROM users WHERE id = ?", arguments: ["local_user"]) ?? false
            if !exists {
                let now = Date()
                try db.execute(sql: "INSERT INTO users (id, display_name, created_at, updated_at) VALUES (?, ?, ?, ?)", arguments: ["local_user", "lachlan", now, now])
            }
        }
    }

    func queue() throws -> DatabaseQueue {
        if dbQueue == nil {
            try open(); try migrate()
        }
        guard let dbQueue else { throw PersistenceError.notAvailable }
        return dbQueue
    }
}
#endif
