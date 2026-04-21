"""Entry point for the THC marker data pipeline.

Reads the Historical Marker CSV, filters to objective quality rules,
converts UTM to WGS84, cleans inscriptions for TTS, and writes:

  out/markers-texas.json
  out/markers-texas.summary.md
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from converters import build_record, utm_to_latlon
from filters import (
    REJECT_CONVERSION_ERROR,
    REJECT_NO_MARKER_TEXT,
    REJECT_OUT_OF_BBOX,
    classify_utm,
    in_texas_bbox,
)
from report import render_summary

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

DEFAULT_INPUT = (
    REPO_ROOT
    / "data"
    / "thc"
    / "Historical Marker_20260417_094710_6744924.csv"
)
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "out"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to Historical Marker CSV (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run(input_path: Path, output_dir: Path) -> int:
    if not input_path.exists():
        print(f"ERROR: input CSV not found: {input_path}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / "markers-texas.json"
    output_summary = output_dir / "markers-texas.summary.md"

    print(f"Reading: {input_path}")
    source_sha = sha256_file(input_path)
    print(f"SHA-256: {source_sha}")

    rejections: Counter = Counter()
    records: list[dict] = []
    by_zone: dict[int, list[dict]] = defaultdict(list)
    input_rows = 0

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            input_rows += 1

            marker_text = (row.get("MarkerText") or "").strip()
            if not marker_text:
                rejections[REJECT_NO_MARKER_TEXT] += 1
                continue

            zone, east, north, utm_reject = classify_utm(row)
            if utm_reject is not None:
                rejections[utm_reject] += 1
                continue

            try:
                lat, lon = utm_to_latlon(zone, east, north)
            except Exception:
                rejections[REJECT_CONVERSION_ERROR] += 1
                continue

            if not in_texas_bbox(lat, lon):
                rejections[REJECT_OUT_OF_BBOX] += 1
                continue

            record = build_record(row, lat, lon)
            records.append(record)
            by_zone[zone].append(record)

    print(f"Input rows:  {input_rows:,}")
    print(f"Output rows: {len(records):,}")
    for reason, count in sorted(rejections.items()):
        print(f"  rejected [{reason}]: {count:,}")

    with output_json.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(records, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")

    summary = render_summary(
        source_csv=input_path,
        source_sha256=source_sha,
        input_rows=input_rows,
        output_records=records,
        rejections=rejections,
        records_by_zone=by_zone,
        output_json_path=output_json,
    )
    with output_summary.open("w", encoding="utf-8", newline="\n") as f:
        f.write(summary)

    print(f"Wrote: {output_json}")
    print(f"Wrote: {output_summary}")
    return 0


def main() -> int:
    args = parse_args()
    return run(args.input, args.output)


if __name__ == "__main__":
    sys.exit(main())
