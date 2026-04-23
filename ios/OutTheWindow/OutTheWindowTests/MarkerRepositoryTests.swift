import XCTest
@testable import OutTheWindow

final class MarkerRepositoryTests: XCTestCase {

    // MARK: - Full corpus load

    func testLoadAllMarkers() async throws {
        let repository = MarkerRepository()
        let markers = try await repository.loadAll()

        // Exact count from pipeline output
        XCTAssertEqual(markers.count, 13_456, "Expected 13,456 markers in the statewide corpus")
        XCTAssertTrue(repository.isLoaded)

        // Spot-check: Marker #4831 — Site of McLaurin Massacre (Real County)
        // Emotional anchor of the May 29 POC trip
        let marker4831 = markers.first { $0.markerNum == 4831 }
        XCTAssertNotNil(marker4831, "Marker #4831 (McLaurin Massacre) must be present")
        if let m = marker4831 {
            XCTAssertEqual(m.title, "Site of McLaurin Massacre")
            XCTAssertEqual(m.county, "Real")
            XCTAssertFalse(m.markerText.isEmpty)
            XCTAssertNotEqual(m.latitude, 0)
            XCTAssertNotEqual(m.longitude, 0)
        }

        // Spot-check: Marker #76 — Abston Cemetery (Collin County, starting county)
        let marker76 = markers.first { $0.markerNum == 76 }
        XCTAssertNotNil(marker76, "Marker #76 (Abston Cemetery, Collin County) must be present")
        if let m = marker76 {
            XCTAssertEqual(m.title, "Abston Cemetery")
            XCTAssertEqual(m.county, "Collin")
            XCTAssertFalse(m.markerText.isEmpty)
            XCTAssertNotEqual(m.latitude, 0)
            XCTAssertNotEqual(m.longitude, 0)
        }

        // Spot-check: Marker #760 — Catherine McLauren (Real County, destination county)
        let marker760 = markers.first { $0.markerNum == 760 }
        XCTAssertNotNil(marker760, "Marker #760 (Catherine McLauren, Real County) must be present")
        if let m = marker760 {
            XCTAssertEqual(m.title, "Catherine McLauren")
            XCTAssertEqual(m.county, "Real")
            XCTAssertFalse(m.markerText.isEmpty)
            XCTAssertNotEqual(m.latitude, 0)
            XCTAssertNotEqual(m.longitude, 0)
        }

        // Spot-check: Marker #1 — Early Community Building (first record, Baylor County)
        let marker1 = markers.first { $0.markerNum == 1 }
        XCTAssertNotNil(marker1, "Marker #1 must be present")
        if let m = marker1 {
            XCTAssertEqual(m.title, "Early Community Building")
            XCTAssertFalse(m.narrationText.isEmpty)
            XCTAssertNotEqual(m.latitude, 0)
            XCTAssertNotEqual(m.longitude, 0)
        }
    }

    // MARK: - Cached second load

    func testSecondLoadReturnsCached() async throws {
        let repository = MarkerRepository()

        let first = try await repository.loadAll()
        XCTAssertTrue(repository.isLoaded)

        let start = CFAbsoluteTimeGetCurrent()
        let second = try await repository.loadAll()
        let elapsed = CFAbsoluteTimeGetCurrent() - start

        XCTAssertEqual(first.count, second.count)
        // Second load should return cached data nearly instantly (< 10ms)
        // vs the initial decode which takes hundreds of ms for 26 MiB
        XCTAssertLessThan(elapsed, 0.01, "Second loadAll() should return cached data without re-decoding")
    }
}
