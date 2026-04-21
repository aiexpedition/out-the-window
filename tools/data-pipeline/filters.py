"""Objective quality filters for THC marker rows."""

from __future__ import annotations

REJECT_NO_MARKER_TEXT = "no_marker_text"
REJECT_NO_UTM = "no_utm"
REJECT_ZERO_UTM = "zero_utm"
REJECT_INVALID_ZONE = "invalid_zone"
REJECT_OUT_OF_BBOX = "out_of_bbox"
REJECT_CONVERSION_ERROR = "conversion_error"

REJECTION_REASONS = (
    REJECT_NO_MARKER_TEXT,
    REJECT_NO_UTM,
    REJECT_ZERO_UTM,
    REJECT_INVALID_ZONE,
    REJECT_OUT_OF_BBOX,
    REJECT_CONVERSION_ERROR,
)

VALID_UTM_ZONES = {13, 14, 15}

TEXAS_BBOX = {
    "lat_min": 25.8,
    "lat_max": 36.6,
    "lon_min": -106.7,
    "lon_max": -93.5,
}


def classify_utm(row: dict) -> tuple[int | None, float | None, float | None, str | None]:
    """Return (zone, easting, northing, reject_reason). Reject reason is None when row passes UTM checks."""
    zone_raw = (row.get("Utm_Zone") or "").strip()
    east_raw = (row.get("Utm_East") or "").strip()
    north_raw = (row.get("Utm_North") or "").strip()

    if not zone_raw or not east_raw or not north_raw:
        return None, None, None, REJECT_NO_UTM

    try:
        zone = int(zone_raw)
    except ValueError:
        return None, None, None, REJECT_INVALID_ZONE

    if zone not in VALID_UTM_ZONES:
        return zone, None, None, REJECT_INVALID_ZONE

    try:
        east = float(east_raw)
        north = float(north_raw)
    except ValueError:
        return zone, None, None, REJECT_NO_UTM

    if east == 0.0 or north == 0.0:
        return zone, east, north, REJECT_ZERO_UTM

    return zone, east, north, None


def in_texas_bbox(lat: float, lon: float) -> bool:
    return (
        TEXAS_BBOX["lat_min"] <= lat <= TEXAS_BBOX["lat_max"]
        and TEXAS_BBOX["lon_min"] <= lon <= TEXAS_BBOX["lon_max"]
    )
