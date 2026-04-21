# THC Marker Data Pipeline

Reads the Texas Historical Commission Historical Marker CSV, converts UTM
coordinates to WGS84 lat/long, applies objective quality filters, cleans
inscription text for TTS narration, and emits a bundled JSON artifact for
the iOS app.

No editorial curation. No geographic corridor filter. Statewide, mechanical,
reproducible: same input CSV + same script = byte-identical output.

## Setup

From the project root:

```bash
cd tools/data-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python build.py
```

Optional flags:

- `--input PATH` — override default CSV path
  (default: `../../data/thc/Historical Marker_20260417_094710_6744924.csv`)
- `--output DIR` — override default output directory
  (default: `./out/`)

## Outputs

Written to `out/` (gitignored):

- `markers-texas.json` — array of marker records, pretty-printed, 2-space indent
- `markers-texas.summary.md` — auditable human-readable run report

## Filter Rules

A marker is included if and only if all of these hold:

1. `MarkerText` is non-empty after trimming
2. `Utm_Zone` parses as integer in {13, 14, 15}
3. `Utm_East` and `Utm_North` parse as numeric and are both non-zero
4. Converted lat/long falls inside the Texas bounding box
   (lat 25.8–36.6, lon -106.7 to -93.5)

Private-property, missing, damaged, in-storage, and
replacement-in-progress markers are **kept** — access restriction is a
visit concern, not a narration concern. The iOS layer decides display
treatment.

## UTM → WGS84

- Source datum: NAD83 (THC convention)
- EPSG codes: Zone 13 = 26913, Zone 14 = 26914, Zone 15 = 26915
- Target: WGS84 lat/long (EPSG:4326)
- Output rounded to 6 decimal places (~11 cm precision)

## Layout

```
tools/data-pipeline/
├── README.md              # this file
├── requirements.txt       # pyproj pinned
├── build.py               # entry point, argparse, orchestration
├── converters.py          # UTM transformers, inscription cleaner, row builder
├── filters.py             # filter predicates, rejection reasons
├── report.py              # summary report generation
└── out/                   # generated artifacts (gitignored)
```
