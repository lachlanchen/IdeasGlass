import Foundation

enum Paths {
    static let appFolderName = "LightMind"

    static func applicationSupportRoot() throws -> URL {
        let base = try FileManager.default.url(for: .applicationSupportDirectory,
                                               in: .userDomainMask,
                                               appropriateFor: nil,
                                               create: true)
        let root = base.appendingPathComponent(appFolderName, isDirectory: true)
        if !FileManager.default.fileExists(atPath: root.path) {
            try FileManager.default.createDirectory(at: root, withIntermediateDirectories: true)
        }
        return root
    }

    static func segmentsRoot() throws -> URL {
        let root = try applicationSupportRoot().appendingPathComponent("segments", isDirectory: true)
        if !FileManager.default.fileExists(atPath: root.path) {
            try FileManager.default.createDirectory(at: root, withIntermediateDirectories: true)
        }
        return root
    }

    static func tmpRoot() -> URL {
        // Use per-app tmp; no need to create explicitly.
        return FileManager.default.temporaryDirectory
    }

    static func contentAddressedPath(for sha256Hex: String, ext: String) throws -> URL {
        let prefix = String(sha256Hex.prefix(2))
        let dir = try segmentsRoot().appendingPathComponent(prefix, isDirectory: true)
        if !FileManager.default.fileExists(atPath: dir.path) {
            try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        }
        return dir.appendingPathComponent("\(sha256Hex).\(ext)")
    }
}

