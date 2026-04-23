# CC Prompt — Phase 1: Data Pipeline (iOS Side)

**Phase:** POC-001 Phase 1
**Authored by:** Claude (Chief Architect)
**Intended executor:** CC (Claude Code) on the iMac Pro
**Authorized by:** Dan Maxwell (Product Owner)
**Date:** 2026-04-22
**Depends on:** Phase 0 (complete, closed 2026-04-22)

---

## Objective

Build the iOS-side data layer for Out the Window: a `Marker` model, a `MarkerRepository` service that loads the bundled statewide marker JSON, a bundled-resource registration for `markers-texas.json`, and a unit test that proves the full corpus loads and parses.

This phase is **data layer only**. No MapKit, no CoreLocation, no narration, no UI changes beyond what Hello World already has.

---

## Scope

### In scope
1. Swift `Marker` model (struct, `Decodable`) matching the schema emitted by `tools/data-pipeline/build.py`.
2. `MarkerRepository` service that loads `markers-texas.json` from the app bundle and exposes the parsed corpus.
3. Registration of `markers-texas.json` as a bundled Resource inside the Xcode project.
4. Unit test that loads the full corpus (expected: 13,456 markers) and spot-checks field shapes on a handful of known records.
5. `os.Logger` subsystem setup for the data layer, consistent with the conventions documented in `AGENTS.md`.

### Out of scope (do not touch)
- MapKit, CoreLocation, geofencing, location permissions
- AVSpeechSynthesizer, AVFoundation, audio session configuration
- Any narration layer (`NarrationService`, `Resources/narrations/`, `marker-*.m4a` files)
- Any UI beyond retaining the existing `ContentView.swift` Hello World
- SwiftData, GRDB, or any persistence layer (repository is a memory-backed loader for POC)
- The `@Observable` property wrappers on anything beyond the repository itself — MapView-bound state is Phase 2 work
- Route-corridor filtering, polyline matching, or any data shaping — the bundle is statewide per Decision 8
- App Store / TestFlight / distribution concerns

---

## Constraints & Invariants

### Schema contract — derive from pipeline source, do not guess

The Swift `Marker` struct must faithfully match the JSON schema emitted by the Python pipeline. **Before writing the Swift model**, CC must:

1. Read `tools/data-pipeline/build.py` to identify the output dictionary construction (look for the function that builds each marker record dict and the top-level JSON serialization).
2. Read `tools/data-pipeline/converters.py` for field-level transformations (UTM→WGS84, inscription cleaning) to understand what data types each field carries.
3. Read `tools/data-pipeline/filters.py` if present, for any field-presence guarantees (e.g., "inscription_text is never null in output" is a filter-layer invariant).
4. Optionally sample the output itself: `head -c 2000 tools/data-pipeline/out/markers-texas.json` to eyeball the first record and confirm derived field names/types match the code.

The Swift struct must use:
- `struct Marker: Decodable, Identifiable, Hashable` — value type, decodable from JSON, identifiable for SwiftUI lists later, hashable for set membership and diffing.
- `CodingKeys` enum if and only if JSON field names differ from Swift conventions. If the pipeline emits `snake_case`, use `JSONDecoder().keyDecodingStrategy = .convertFromSnakeCase` in the repository and omit per-field CodingKeys.
- Optional types (`String?`, `Double?`, etc.) for any field that the pipeline can legitimately omit. Required fields must be non-optional — if JSON is missing them, decoding should fail loudly rather than silently accepting nil.
- A natural `id` — prefer the THC marker number as `Int`. If the pipeline emits it as a string, keep it as a string but name the property `markerNumber` and make it the identifier.

**Do not invent fields that aren't in the pipeline output. Do not rename fields for Swift stylistic reasons if the pipeline emits a specific name — either use CodingKeys or the decoding strategy.**

### Repository loading strategy — async on demand

The repository must not block the calling thread on init.

Required shape:

```swift
@Observable
final class MarkerRepository {
    private(set) var markers: [Marker] = []
    private(set) var isLoaded: Bool = false

    func loadAll() async throws -> [Marker]
}
```

- `loadAll()` is `async throws`. It reads the bundled JSON, decodes it, stores to `self.markers`, sets `isLoaded = true`, and returns the decoded array.
- Decoding happens via `Task.detached(priority: .userInitiated)` or equivalent so the ~26 MiB parse does not run on whatever actor called it.
- If called a second time after successful load, return the cached `markers` without re-decoding.
- No error swallowing. Propagate decoding errors with enough context to diagnose a schema mismatch (include the file URL and the underlying `DecodingError` in a wrapped `MarkerRepositoryError`).

**Why async and not synchronous:** the bundle is ~26 MiB. A synchronous decoder on `init()` is a footgun that will eventually land on the main actor and stall the UI. Phase 2's MapView will call this from a `.task { }` modifier, which aligns naturally.

### Bundled resource registration

1. Create directory `ios/OutTheWindow/OutTheWindow/Resources/` if it does not exist.
2. Copy `tools/data-pipeline/out/markers-texas.json` into `ios/OutTheWindow/OutTheWindow/Resources/markers-texas.json`. (This is a **copy**, not a symlink — the Xcode build system needs the file to physically exist under the app target.)
3. Add the file to the Xcode project's `OutTheWindow` app target so it gets bundled at build time. In the project file (`project.pbxproj`), the file must appear in the `Resources` build phase of the `OutTheWindow` target.
4. Verify the bundling by running a build and checking that `markers-texas.json` appears in the resulting `.app` bundle. `Bundle.main.url(forResource: "markers-texas", withExtension: "json")` must return non-nil at runtime.

**Important:** `markers-texas.json` is ~26 MiB. This increases the app binary size materially. That is expected and accepted per Decision 8.

**Git:** the bundled copy at `ios/OutTheWindow/OutTheWindow/Resources/markers-texas.json` **must be committed** to the repo. The gitignore rule on `tools/data-pipeline/out/` is for the pipeline's output artifact; the bundled resource is a separate, tracked file. Verify that `.gitignore` does not accidentally catch the bundled path.

### Logging

Use `os.Logger` with subsystem `com.theaiexpedition.OutTheWindow` and category `data`. Document the subsystem/category convention in `AGENTS.md` if it isn't already there.

Log at `.info` on successful load with the marker count. Log at `.error` on any decoding failure with the underlying error description. Do not log per-record.

### Swift conventions

Follow the conventions in `AGENTS.md` "Stack-Specific CC Guidelines" (Swift/SwiftUI section). If that section is still a placeholder, treat the following as authoritative for this prompt:

- `@Observable` (iOS 17+ Observation framework), not `ObservableObject`.
- Services as `final class`. Models as `struct`.
- File-per-type except for tightly coupled small types.
- `os.Logger` over `print`. One logger per subsystem+category pair.
- XCTest. Async tests via `async throws` test methods.

---

## File Targets

### New files
- `ios/OutTheWindow/OutTheWindow/Models/Marker.swift`
- `ios/OutTheWindow/OutTheWindow/Services/MarkerRepository.swift`
- `ios/OutTheWindow/OutTheWindow/Services/MarkerRepositoryError.swift` (if error enum warrants its own file; otherwise nested in `MarkerRepository.swift`)
- `ios/OutTheWindow/OutTheWindow/Resources/markers-texas.json` (copy from `tools/data-pipeline/out/markers-texas.json`)
- `ios/OutTheWindow/OutTheWindowTests/MarkerRepositoryTests.swift`

### Modified files
- `ios/OutTheWindow/OutTheWindow.xcodeproj/project.pbxproj` — register the new Swift files against the `OutTheWindow` target, register the test file against the `OutTheWindowTests` target, and register `markers-texas.json` as a Resource of the `OutTheWindow` target.
- (No changes required to `ContentView.swift` or `OutTheWindowApp.swift` in this phase.)

---

## Acceptance Criteria

All of the following must pass before reporting this phase complete.

1. **Build succeeds** for the `OutTheWindow` scheme targeting iPhone 14 Pro simulator (iOS 18.6) on the iMac Pro.
2. **`Bundle.main.url(forResource: "markers-texas", withExtension: "json")` returns non-nil** at runtime when the app launches in the simulator. (A quick `Logger().info()` at app startup to verify this is acceptable for this phase; it can be removed or kept as a startup sanity check — Dan's preference.)
3. **Unit test `MarkerRepositoryTests.testLoadAllMarkers` passes** and asserts:
   - `try await repository.loadAll()` returns an array with exactly **13,456** markers.
   - `repository.isLoaded == true` after the call.
   - A spot-check of 3–5 known markers by marker number finds them in the loaded corpus. **Marker #4831 (McLauren Massacre)** must be one of them — this is the emotional anchor of the May 29 trip and its presence in the bundle is the proof-of-no-curation. Other spot-check markers: one from Collin County (Dan's starting county) and one from Real County (Dan's destination county).
   - For each spot-checked marker: `markerNumber`, title/name, inscription text, and lat/long are all present and non-empty / non-zero.
4. **Unit test `MarkerRepositoryTests.testSecondLoadReturnsCached` passes:** two consecutive calls to `loadAll()` return the same array instance (or equal contents without re-decoding). Acceptable to verify by measuring elapsed time on the second call, or by adding a decode-count counter behind `#if DEBUG`.
5. **No force-unwraps** (`!`) in `Marker.swift` or `MarkerRepository.swift`. Optional handling via `guard let`, `if let`, or proper `throws`.
6. **No warnings** from the Swift compiler on the new files at the project's current warning level.
7. **Working tree after commit:** clean, nothing staged, nothing untracked beyond normal Xcode artifacts already covered by `.gitignore`.

### Not required for this phase
- Performance benchmarks. (Load time observation is informational; no threshold enforced.)
- UI integration. `ContentView.swift` does not need to call the repository yet.
- Integration tests. Unit test coverage is sufficient for this phase.

---

## Execution Notes

### Reading the pipeline source
The pipeline lives at `tools/data-pipeline/` relative to repo root. On the iMac Pro that's `~/Projects/out-the-window/tools/data-pipeline/`. CC has filesystem access to it. The pipeline is Python; CC does not need to execute it — just read it to derive the schema.

### Copying the JSON
`markers-texas.json` at `tools/data-pipeline/out/markers-texas.json` was placed there by Dan before this prompt was authorized. If it is missing at execution time, **fail loudly** with a clear message: "Expected `tools/data-pipeline/out/markers-texas.json` to exist. It is generated by the Python pipeline on Win11 WSL and distributed via NAS. See Phase 0 closure capsule and `thc-data-pipeline-v2` for the workflow." Do not attempt to regenerate it.

### Xcode project file editing
`project.pbxproj` edits are the most fragile part of this prompt. Prefer to open the project in Xcode and add files via the navigator (right-click target → Add Files to "OutTheWindow"…) if that's available in CC's execution environment. If CC must edit `project.pbxproj` directly, verify the result by running `xcodebuild -list` and then a full build before reporting success. A malformed project file will fail the build; an accidentally-omitted target membership will fail the runtime bundle lookup.

### Ambiguity handling
If CC encounters ambiguity in the pipeline's output schema (field names, types, nullability) that cannot be resolved by reading `build.py` / `converters.py` / `filters.py` and a sample of the JSON: **stop and report**. Do not guess. Phase 1 is the foundation layer; a wrong field name here propagates into Phase 2 (MapView) and Phase 3 (Location) and is expensive to fix later.

---

## Git Commit Message

```
Add Marker model and MarkerRepository with bundled statewide corpus (Phase 1)
```

---

## Reporting

On completion, report:

1. **Schema derived from pipeline:** the final `Marker` struct definition, with a one-line note on the source (e.g., "fields derived from `build.py:build_marker_record()` and `converters.py:clean_inscription()`").
2. **Files created/modified:** paths and brief purpose of each.
3. **Test results:** pass/fail for each of the two unit tests, with the actual marker count returned.
4. **Build verification:** simulator build result, and the result of the `Bundle.main.url(…)` startup check if added.
5. **Binary size impact:** approximate size of the built `.app` before and after bundling `markers-texas.json`.
6. **Anything weird:** any ambiguity encountered, any shortcut taken, any follow-up that Claude should know about before Phase 2.

Claude will review and either approve or request changes before Dan commits and pushes.
