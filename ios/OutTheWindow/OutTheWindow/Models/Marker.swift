import Foundation

/// A Texas Historical Commission marker record, decoded from the bundled statewide corpus.
///
/// Fields derived from `converters.py:build_record()`. Required fields are those present
/// in all 13,456 pipeline output records; optional fields are omitted by `put_str`/`put_int`
/// when the source CSV value is empty.
struct Marker: Decodable, Identifiable, Hashable {

    // MARK: - Required fields (always present in pipeline output)

    let markerNum: Int
    let atlasNumber: Int
    let title: String
    let county: String
    let countyId: Int
    let latitude: Double
    let longitude: Double
    let privateProperty: Bool
    let markerText: String
    let narrationText: String

    // MARK: - Optional fields (omitted when source CSV value is empty)

    let indexName: String?
    let city: String?
    let address: String?
    let year: Int?
    let locationDesc: String?
    let conditionText: String?

    // MARK: - Identifiable

    var id: Int { markerNum }
}
