# CC Prompt — Phase 1: THC Marker Data Pipeline

**Target agent:** CC (Claude Code)
**Execution host:** Win11 dev rig, running CC from inside WSL
**Project root:** `/mnt/c/Users/wimbl/Projects/OTW` (Windows: `C:\Users\wimbl\Projects\OTW`)
**Branch:** `main` (solo project, no PR flow)
**Related canon:** `docs/POC-001-may29-roadtrip.md`, `docs/ADR-001-mobile-framework.md`, `docs/ADR-002-dev-environment.md`, `docs/WORKFLOW.md`, `docs/AGENTS.md`

---

## Working Directory Notes

- All paths in this prompt are relative to the project root: `/mnt/c/Users/wimbl/Projects/OTW`
- Use forward-slash paths throughout (works in WSL and Python)
- Write files with LF line endings, not CRLF — Python stdlib `open()` in text mode on WSL does this by default
- `core.autocrlf` is already set to `input` on this repo — nothing to configure

---

## Repo State Snapshot (as of prompt generation)

```
/mnt/c/Users/wimbl/Projects/OTW/
├── .git/                                 (initialized, on main, tracking origin)
├── .gitignore
├── README.md
├── data/
│   └── thc/
│       ├── Historical_Marker_20260417_094710_6744924.csv   ← INPUT for this pipeline
│       ├── Cemetery_20260417_094711_0378249.csv
│       ├── Courthouse_20260417_094650_9168178.csv
│       ├── Museum_Information_20260417_094711_124138.csv
│       ├── National_Register_Listing_20260417_094709_7820436.csv
│       └── State_Antiquities_Landmark_20260417_094709_8645049.csv
└── docs/
    ├── prompts/                          (this prompt is expected to live here when CC reads it)
    ├── CONTRIBUTING.md
    ├── WORKFLOW.md
    ├── AGENTS.md
    ├── ADR-001-mobile-framework.md
    ├── ADR-002-dev-environment.md
    ├── ADR-003-ownership-legal-structure.md
    └── POC-001-may29-roadtrip.md
```

No `tools/`, no iOS scaffold, no Python — this prompt creates the first code in the repo.

---

## Objective

Build a standalone, reproducible Python pipeline that reads the THC Historical Marker CSV and produces a single bundled JSON artifact (`markers-texas.json`) suitable for shipping inside the iOS app binary. The artifact represents **every THC-documented Texas historical marker that passes objective data-quality filters** — no geographic filter, no corridor logic, no editorial curation.

This is a **decision ratified by Dan (Product Owner) on 2026-04-21**: the POC bundle is statewide, not corridor-filtered. This supersedes the "corridor filter" language in `docs/POC-001-may29-roadtrip.md` § "Route Corridor Marker Set" — Claude (Chief Architect) will amend that document in a follow-up artifact. CC does not need to touch canon in this task.

---

## Scope

### In Scope
- Create `tools/data-pipeline/` directory with a self-contained Python 3.11+ project
- Read `data/thc/Historical_Marker_20260417_094710_6744924.csv` (path relative to project root)
- Convert UTM → WGS84 (per-row zone, datum NAD83, ellipsoid GRS80)
- Apply quality filters (see below)
- Clean `MarkerText` for TTS consumption
- Emit artifacts to `tools/data-pipeline/out/`
- Extend `.gitignore` with pipeline-specific entries
- One-shot script: `python build.py` with optional `--input` and `--output` flags

### Out of Scope
- No polyline, no corridor filter, no radius logic
- No Swift code, no iOS integration (the `ios/` directory does not exist yet; don't create it)
- No database, no PostGIS, no API server
- No AI enrichment, no hook/snapshot generation (production-phase)
- No copying output into an iOS project directory (iOS scaffold does not yet exist; artifact stays in `tools/data-pipeline/out/`)
- No unit-test framework — a handful of assertions inline in the conversion function is enough. This is build-time tooling; correctness is verified by the summary report, not by test coverage.
- No modifications to `docs/` — canon is Claude's responsibility

---

## Constraints & Invariants

### Data Integrity
- Filter rules are mechanical and reproducible. Same input CSV + same script = same output. No randomness, no sampling.
- No editorial curation. If a marker passes the quality filter, it is in.
- Preserve `MarkerNum` and `Atlas_Number` as stable IDs — the iOS layer will use them for geofence identity and cooldown tracking.

### Dependencies
- `pyproj` for UTM → WGS84 conversion
- Python stdlib: `csv`, `json`, `re`, `pathlib`, `argparse`, `hashlib`, `datetime`
- **No pandas.** Keep this tool lightweight and auditable.
- Pin versions in `requirements.txt`.
- Use a virtual environment: `python3 -m venv .venv && source .venv/bin/activate` (Linux-style in WSL).

### UTM Conversion
- THC uses **NAD83 datum** for UTM. EPSG codes:
  - Zone 13 NAD83: `EPSG:26913`
  - Zone 14 NAD83: `EPSG:26914`
  - Zone 15 NAD83: `EPSG:26915`
- Target CRS: WGS84 lat/long (`EPSG:4326`)
- Use a `Transformer` per zone, cached at module scope (avoid re-constructing in a hot loop)
- Round output to 6 decimal places (~11 cm precision — ample for geofencing)

### Condition & Privacy Flags
- Keep `PrivateProperty` and `ConditionText` fields in the output — the iOS app can surface them at display time
- Do NOT filter out private-property markers. A traveler driving past still experiences the narration; access restriction is a visit concern, not a narration concern.
- Do NOT filter out `Missing` / `In Storage` / `Replacement In Progress`. The documented location and inscription text remain valuable POIs even when the plaque isn't physically present.

---

## Filter Rules (the ONLY filters applied)

A marker is included in `markers-texas.json` if and only if ALL of the following are true:

1. `MarkerText` is non-empty after trimming whitespace
2. `Utm_Zone` parses as integer in {13, 14, 15}
3. `Utm_East` and `Utm_North` parse as numeric and are both non-zero
4. UTM → WGS84 conversion produces a lat/long within the Texas bounding box:
   - Latitude: 25.8 to 36.6
   - Longitude: -106.7 to -93.5
   - Any marker outside this box is logged as `out_of_bbox` and dropped (sanity check against conversion errors)

**Expected pass count:** ~13,497 markers (measured against current CSV on 2026-04-21). Summary report must surface actual count and any delta from this expectation.

---

## Inscription Cleaning for TTS

Apply these transforms in order to `MarkerText`, producing `narrationText`. Preserve the original as `markerText`.

1. Strip leading/trailing whitespace
2. Collapse runs of whitespace (including newlines) to a single space
3. Expand common abbreviations from an `ABBREVIATIONS` dict (easy to extend later):
   - `Co.` → `County` (when followed by space+capital or end-of-word — be careful not to mangle "Coca-Cola Co." into "Coca-Cola County")
   - `Capt.` → `Captain`
   - `Gen.` → `General`
   - `Lt.` → `Lieutenant`
   - `Col.` → `Colonel`
   - `Rev.` → `Reverend`
   - `Dr.` → `Doctor` (only when preceded by whitespace and followed by capital letter — avoid "Dr." in addresses)
   - `Mt.` → `Mount`
   - `Ft.` → `Fort`
   - `St.` → `Saint` (context-dependent; accept imperfection here — flag ambiguous cases in summary, don't block)
   - `No.` → `Number`
4. Remove bracketed editorial notes: pattern `\[.*?\]`
5. Normalize smart quotes (`" " ' '`) to straight quotes (`" '`)
6. Leave sentence punctuation intact — AVSpeechSynthesizer uses it for cadence

**Conservatism principle:** when in doubt, leave the text alone. Over-aggressive cleaning creates worse problems than it solves.

---

## Output Artifacts

### `tools/data-pipeline/out/markers-texas.json`

A JSON **array** (not object). Each element has this shape — omit fields that are empty strings in the source:

```json
{
  "markerNum": 1,
  "atlasNumber": 5023000001,
  "title": "Early Community Building",
  "indexName": "Community Building, Early",
  "county": "Baylor",
  "countyId": 12,
  "city": "Seymour",
  "address": "210 N East St",
  "year": 1969,
  "locationDesc": "S. East and E. Morris streets, Seymour",
  "latitude": 33.594432,
  "longitude": -99.259810,
  "privateProperty": false,
  "conditionText": "In Situ",
  "markerText": "Built 1877 by Charles Holman...",
  "narrationText": "Built 1877 by Charles Holman..."
}
```

Field notes:
- `year` is an Int if parseable, otherwise omitted
- `privateProperty` is a Bool
- Omit any string field whose source value is empty
- Pretty-print with 2-space indent for git-diffability
- Preserve JSON key order as shown (use `json.dumps(..., indent=2, sort_keys=False)` with dict insertion order matching the example)

### `tools/data-pipeline/out/markers-texas.summary.md`

Human-readable markdown report with at minimum:

- Generation timestamp (ISO 8601, UTC)
- Source CSV filename and SHA-256 hash
- Total input rows
- Total output rows
- Delta from expected (~13,497)
- Rejection breakdown with counts: `no_marker_text`, `no_utm`, `zero_utm`, `invalid_zone`, `out_of_bbox`, `conversion_error`
- County distribution (top 20 by marker count)
- Condition distribution (all values with counts)
- Private property count
- UTM zone distribution
- Output file size (bytes, human-readable)
- Three spot-check markers with converted coordinates:
  - Marker #1 (Baylor County, Zone 14) — should land near Seymour, TX
  - One randomly-selected Zone 13 marker (West Texas)
  - One randomly-selected Zone 15 marker (East Texas)

This report is the auditable record that the pipeline ran honestly against the full dataset.

---

## File Targets

### Create

```
tools/data-pipeline/
├── README.md              # How to run, what it produces, where output goes
├── requirements.txt       # pyproj pinned to a specific version
├── build.py               # Entry point — argparse, orchestrates the pipeline
├── converters.py          # UTM→WGS84 transformers, inscription cleaner, row builder
├── filters.py             # Filter predicates and rejection-reason enum/constants
└── report.py              # Summary report generation
```

### Extend `.gitignore` (append if not already present)

```
# Data pipeline
tools/**/out/
tools/**/.venv/
tools/**/__pycache__/
tools/**/*.pyc
```

(The root `.gitignore` may already cover some of these — verify and don't duplicate.)

---

## Acceptance Criteria

1. From project root:
   ```bash
   cd tools/data-pipeline
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python build.py
   ```
   Completes with exit code 0 and no unhandled exceptions.

2. Output `out/markers-texas.json` contains **13,497 ± 50** records.

3. Output `out/markers-texas.summary.md` includes every section listed above, readable top-to-bottom without errors.

4. Spot-check in the summary:
   - Marker #1 (Early Community Building, Baylor County) appears with latitude ~33.59, longitude ~-99.26
   - A Zone 13 marker converts to a lat/long in West Texas (roughly longitude < -103)
   - A Zone 15 marker converts to a lat/long in East Texas (roughly longitude > -97)

5. Running the script twice in a row produces byte-identical output (deterministic).

6. No hard-coded absolute paths anywhere. All paths resolve relative to the script location or are passed via `--input` / `--output`.

---

## Git Discipline

Working on `main`. No feature branch for this task. Commit structure:

**Option A (preferred):** one commit with everything:
```
Add Phase 1 data pipeline: statewide THC marker extraction to JSON
```

**Option B:** if changes feel naturally separable, split into small logical commits — but all on `main`, no branch. Each commit message imperative, scoped.

**Do not push.** Dan reviews local commits before pushing to `origin`.

---

## Report Back to Claude

When execution is complete, provide a summary including:

1. **What was created** — list of files with line counts
2. **What the pipeline produced** — actual record count, rejection breakdown
3. **Any deviations from the prompt** — conservative choices made where the prompt was ambiguous
4. **Any anomalies in the data** — unexpected rejections, edge cases in inscription cleaning, condition values not previously documented
5. **Git status** — list of commits made, confirmation that nothing is pushed
6. **Next step recommendation** — "ready to review" or specific blockers

Dan will share this summary back with Claude for review before anything is pushed to `origin`.

---

## If CC Encounters Ambiguity

- Do not invent behavior. Stop and flag in the summary.
- Make the conservative choice (preserve more data, filter less, match the source more closely) when the prompt is silent.
- Canon (`docs/`) is the source of truth. If this prompt and canon disagree, canon wins and CC should flag the discrepancy.
