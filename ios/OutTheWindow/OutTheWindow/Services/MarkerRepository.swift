import Foundation
import Observation
import os

/// Errors thrown by ``MarkerRepository`` during corpus loading.
enum MarkerRepositoryError: Error, LocalizedError {
    case bundleResourceNotFound(resource: String, extension: String)
    case decodingFailed(fileURL: URL, underlying: Error)

    var errorDescription: String? {
        switch self {
        case let .bundleResourceNotFound(resource, ext):
            "Bundle resource not found: \(resource).\(ext)"
        case let .decodingFailed(fileURL, underlying):
            "Failed to decode \(fileURL.lastPathComponent): \(underlying.localizedDescription)"
        }
    }
}

/// Loads and caches the bundled statewide marker corpus from `markers-texas.json`.
///
/// Usage:
/// ```swift
/// let repo = MarkerRepository()
/// let markers = try await repo.loadAll()
/// ```
@Observable
final class MarkerRepository {

    private(set) var markers: [Marker] = []
    private(set) var isLoaded: Bool = false

    private static let logger = Logger(
        subsystem: "com.theaiexpedition.OutTheWindow",
        category: "data"
    )

    /// Loads and decodes the full marker corpus from the app bundle.
    ///
    /// On first call, reads `markers-texas.json` from the bundle, decodes it on a
    /// background thread, caches the result, and returns the array. Subsequent calls
    /// return the cached array without re-decoding.
    ///
    /// - Returns: The decoded array of ``Marker`` values.
    /// - Throws: ``MarkerRepositoryError`` if the bundle resource is missing or decoding fails.
    func loadAll() async throws -> [Marker] {
        if isLoaded {
            return markers
        }

        guard let fileURL = Bundle.main.url(forResource: "markers-texas", withExtension: "json") else {
            Self.logger.error("markers-texas.json not found in app bundle")
            throw MarkerRepositoryError.bundleResourceNotFound(resource: "markers-texas", extension: "json")
        }

        let decoded: [Marker] = try await Task.detached(priority: .userInitiated) {
            let data = try Data(contentsOf: fileURL)
            do {
                return try JSONDecoder().decode([Marker].self, from: data)
            } catch {
                Self.logger.error("Decoding markers-texas.json failed: \(error.localizedDescription)")
                throw MarkerRepositoryError.decodingFailed(fileURL: fileURL, underlying: error)
            }
        }.value

        markers = decoded
        isLoaded = true
        Self.logger.info("Loaded \(decoded.count) markers from bundle")
        return decoded
    }
}
