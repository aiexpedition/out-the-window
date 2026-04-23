# Phase 1 Completion Report — Data Pipeline (iOS Side)

**Phase:** POC-001 Phase 1
**Executed by:** CC (Claude Code)
**Date:** 2026-04-22
**Status:** Complete — awaiting review before commit

---

## 1. Schema Derived from Pipeline

Fields derived from `converters.py:build_record()`, with nullability verified by scanning all 13,456 output records:

```swift
struct Marker: Decodable, Identifiable, Hashable {
    // Required (present in all 13,456 records)
    let markerNum: Int          // THC marker number, used as Identifiable id
    let atlasNumber: Int
    let title: String
    let county: String
    let countyId: Int
    let latitude: Double
    let longitude: Double
    let privateProperty: Bool
    let markerText: String      // Raw inscription
    let narrationText: String   // TTS-cleaned via clean_narration()

    // Optional (omitted by put_str/put_int when CSV value is empty)
    let indexName: String?      // 13,260/13,456
    let city: String?           // 13,248/13,456
    let address: String?        //  9,458/13,456
    let year: Int?              // 13,305/13,456
    let locationDesc: String?   // 11,591/13,456
    let conditionText: String?  // 12,820/13,456

    var id: Int { markerNum }
}
```

No `CodingKeys` needed — pipeline emits camelCase matching Swift property names. Standard `JSONDecoder` decodes without configuration.

---

## 2. Files Created/Modified

| File | Purpose |
|------|---------|
| `ios/OutTheWindow/OutTheWindow/Models/Marker.swift` | Value-type model, `Decodable + Identifiable + Hashable` |
| `ios/OutTheWindow/OutTheWindow/Services/MarkerRepository.swift` | `@Observable` service with async loader, caching, and `MarkerRepositoryError` enum |
| `ios/OutTheWindow/OutTheWindow/Resources/markers-texas.json` | Bundled 26 MiB statewide corpus (copy from `tools/data-pipeline/out/`) |
| `ios/OutTheWindow/OutTheWindowTests/MarkerRepositoryTests.swift` | Two unit tests: full corpus load + cached second load |

**No `project.pbxproj` edits required.** Xcode 16's `PBXFileSystemSynchronizedRootGroup` auto-discovers files in the synced `OutTheWindow/` and `OutTheWindowTests/` directories.

---

## 3. Test Results

| Test | Result | Duration |
|------|--------|----------|
| `testLoadAllMarkers` | PASSED | 0.506s |
| `testSecondLoadReturnsCached` | PASSED | 0.759s |

**`testLoadAllMarkers`** returned **13,456** markers. Spot-checked:

- **#4831** "Site of McLaurin Massacre" (Real County) — present, all fields non-empty/non-zero
- **#76** "Abston Cemetery" (Collin County) — present, all fields non-empty/non-zero
- **#760** "Catherine McLauren" (Real County) — present, all fields non-empty/non-zero
- **#1** "Early Community Building" (Baylor County) — present, all fields non-empty/non-zero

**`testSecondLoadReturnsCached`** confirmed second call returns instantly (<10ms threshold) without re-decoding.

---

## 4. Build Verification

- `xcodebuild build` succeeded targeting iPhone 16 Pro simulator (iOS 18.5) with **zero warnings**.
- `markers-texas.json` confirmed present in built `.app` bundle (verified via filesystem inspection of `DerivedData` output).

---

## 5. Binary Size Impact

| Measurement | Size |
|-------------|------|
| Built `.app` bundle (Phase 1) | ~43 MB |
| `markers-texas.json` in bundle | ~26 MB |
| Pre-Phase-1 app (Hello World) | ~17 MB |

The 26 MB increase is expected and accepted per Decision 8 (no curation, statewide corpus ships bundled).

---

## 6. Notes and Observations

- **Error type kept inline:** `MarkerRepositoryError` is defined in `MarkerRepository.swift` rather than a separate file — only two cases, per the prompt's allowance.
- **Gitignore clean:** the `tools/**/out/` rule correctly catches the pipeline output artifact but does not reach `ios/…/Resources/markers-texas.json`. Verified with `git check-ignore`.
- **No ambiguity encountered:** all field names, types, and nullability were unambiguously derivable from `build.py`, `converters.py`, `filters.py`, and a full-corpus scan of the JSON output.
- **Logging:** `os.Logger` configured with subsystem `com.theaiexpedition.OutTheWindow`, category `data`. Logs at `.info` on successful load, `.error` on decode failure.

---

## Acceptance Criteria Checklist

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Build succeeds for OutTheWindow scheme on iPhone simulator | PASS |
| 2 | `Bundle.main.url(forResource:withExtension:)` returns non-nil | PASS |
| 3 | `testLoadAllMarkers` passes with 13,456 markers + spot-checks | PASS |
| 4 | `testSecondLoadReturnsCached` passes | PASS |
| 5 | No force-unwraps in Marker.swift or MarkerRepository.swift | PASS |
| 6 | No compiler warnings on new files | PASS |
| 7 | Working tree clean after commit (pending) | PENDING |
