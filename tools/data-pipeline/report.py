"""Summary report generation for the pipeline."""

from __future__ import annotations

import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from filters import REJECTION_REASONS

EXPECTED_PASS_COUNT = 13_497


def _human_bytes(n: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB"):
        if n < 1024:
            return f"{n:,.0f} {unit}" if unit == "B" else f"{n:,.2f} {unit}"
        n /= 1024
    return f"{n:,.2f} TiB"


def _pick_spot_check(records: list[dict], predicate) -> dict | None:
    matches = [r for r in records if predicate(r)]
    if not matches:
        return None
    rng = random.Random(42)
    return rng.choice(matches)


def _fmt_record(r: dict) -> str:
    lines = [
        f"- Marker #{r.get('markerNum', '?')} — {r.get('title', '(untitled)')}",
        f"  - County: {r.get('county', '?')}",
        f"  - Lat/Lon: {r['latitude']:.6f}, {r['longitude']:.6f}",
    ]
    return "\n".join(lines)


def render_summary(
    source_csv: Path,
    source_sha256: str,
    input_rows: int,
    output_records: list[dict],
    rejections: Counter,
    records_by_zone: dict[int, list[dict]],
    output_json_path: Path,
) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    output_count = len(output_records)
    delta = output_count - EXPECTED_PASS_COUNT

    county_counter: Counter = Counter(
        r.get("county", "(unknown)") for r in output_records
    )
    condition_counter: Counter = Counter(
        r.get("conditionText", "(unset)") for r in output_records
    )
    private_count = sum(1 for r in output_records if r.get("privateProperty"))

    zone_counter: Counter = Counter(
        {zone: len(recs) for zone, recs in records_by_zone.items()}
    )

    first_marker = next(
        (r for r in output_records if r.get("markerNum") == 1), None
    )
    zone13_pick = _pick_spot_check(
        records_by_zone.get(13, []),
        lambda r: True,
    )
    zone15_pick = _pick_spot_check(
        records_by_zone.get(15, []),
        lambda r: True,
    )

    json_size = output_json_path.stat().st_size if output_json_path.exists() else 0

    lines: list[str] = []
    lines.append("# THC Marker Pipeline — Run Summary")
    lines.append("")
    lines.append(f"- Generated: `{generated_at}`")
    lines.append(f"- Source CSV: `{source_csv.name}`")
    lines.append(f"- Source SHA-256: `{source_sha256}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- Input rows: **{input_rows:,}**")
    lines.append(f"- Output records: **{output_count:,}**")
    lines.append(
        f"- Expected pass count: {EXPECTED_PASS_COUNT:,} "
        f"(delta: {delta:+,})"
    )
    lines.append("")
    lines.append("## Rejection Breakdown")
    lines.append("")
    lines.append("| Reason | Count |")
    lines.append("|---|---:|")
    for reason in REJECTION_REASONS:
        lines.append(f"| `{reason}` | {rejections.get(reason, 0):,} |")
    total_rejected = sum(rejections.values())
    lines.append(f"| **Total rejected** | **{total_rejected:,}** |")
    lines.append("")
    lines.append("## UTM Zone Distribution (kept records)")
    lines.append("")
    lines.append("| Zone | Count |")
    lines.append("|---:|---:|")
    for zone in sorted(zone_counter):
        lines.append(f"| {zone} | {zone_counter[zone]:,} |")
    lines.append("")
    lines.append("## Top 20 Counties")
    lines.append("")
    lines.append("| County | Markers |")
    lines.append("|---|---:|")
    for county, count in county_counter.most_common(20):
        lines.append(f"| {county} | {count:,} |")
    lines.append("")
    lines.append("## Condition Distribution")
    lines.append("")
    lines.append("| Condition | Count |")
    lines.append("|---|---:|")
    for condition, count in sorted(
        condition_counter.items(), key=lambda kv: (-kv[1], kv[0])
    ):
        lines.append(f"| {condition} | {count:,} |")
    lines.append("")
    lines.append("## Private Property")
    lines.append("")
    lines.append(f"- Records flagged `privateProperty = true`: **{private_count:,}**")
    lines.append("")
    lines.append("## Output Artifact")
    lines.append("")
    lines.append(f"- Path: `{output_json_path.name}`")
    lines.append(f"- Size: **{_human_bytes(json_size)}** ({json_size:,} bytes)")
    lines.append("")
    lines.append("## Spot Checks")
    lines.append("")
    if first_marker:
        lines.append("### Marker #1 — expected near Seymour, TX (Zone 14)")
        lines.append("")
        lines.append(_fmt_record(first_marker))
        lines.append("")
    if zone13_pick:
        lines.append("### Random Zone 13 marker — expected West Texas (lon < -103)")
        lines.append("")
        lines.append(_fmt_record(zone13_pick))
        lines.append("")
    if zone15_pick:
        lines.append("### Random Zone 15 marker — expected East Texas (lon > -97)")
        lines.append("")
        lines.append(_fmt_record(zone15_pick))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
