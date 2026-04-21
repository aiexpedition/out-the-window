"""UTM→WGS84 conversion, inscription cleaning, output row assembly."""

from __future__ import annotations

import re
from functools import lru_cache

from pyproj import Transformer

NAD83_UTM_EPSG = {
    13: "EPSG:26913",
    14: "EPSG:26914",
    15: "EPSG:26915",
}
WGS84 = "EPSG:4326"


@lru_cache(maxsize=None)
def _transformer(zone: int) -> Transformer:
    return Transformer.from_crs(NAD83_UTM_EPSG[zone], WGS84, always_xy=True)


def utm_to_latlon(zone: int, easting: float, northing: float) -> tuple[float, float]:
    """Convert NAD83 UTM to WGS84 lat/long, rounded to 6 decimal places.

    always_xy=True means the transformer takes (x=easting, y=northing) and
    returns (lon, lat). Returning (lat, lon) to match the rest of the code.
    """
    lon, lat = _transformer(zone).transform(easting, northing)
    return round(lat, 6), round(lon, 6)


SMART_QUOTES = {
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "«": '"',
    "»": '"',
}

_WHITESPACE_RE = re.compile(r"\s+")
_BRACKETED_RE = re.compile(r"\[.*?\]")


ABBREVIATIONS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bCapt\."), "Captain"),
    (re.compile(r"\bGen\."), "General"),
    (re.compile(r"\bLt\."), "Lieutenant"),
    (re.compile(r"\bCol\."), "Colonel"),
    (re.compile(r"\bRev\."), "Reverend"),
    (re.compile(r"\bMt\."), "Mount"),
    (re.compile(r"\bFt\."), "Fort"),
    (re.compile(r"\bNo\."), "Number"),
    # Context-guarded rules — only expand when next token is a capitalized word
    # (typical "Co. Dallas", "St. Mary", "Dr. Smith"). Avoids mangling
    # "Coca-Cola Co." trailing sentence, street addresses like "205 Main St.",
    # or "Dr." in "1215 Dr. Pepper Ln".
    (re.compile(r"\bCo\.(?=\s+[A-Z])"), "County"),
    (re.compile(r"\bSt\.(?=\s+[A-Z])"), "Saint"),
    (re.compile(r"(?<=\s)Dr\.(?=\s+[A-Z])"), "Doctor"),
]


def clean_narration(text: str) -> str:
    """Return MarkerText transformed for TTS consumption."""
    if not text:
        return ""

    out = text.strip()
    out = _WHITESPACE_RE.sub(" ", out)

    for pattern, replacement in ABBREVIATIONS:
        out = pattern.sub(replacement, out)

    out = _BRACKETED_RE.sub("", out)

    for smart, straight in SMART_QUOTES.items():
        out = out.replace(smart, straight)

    out = _WHITESPACE_RE.sub(" ", out).strip()
    return out


def parse_year(raw: str) -> int | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def parse_bool(raw: str) -> bool:
    return (raw or "").strip().lower() == "true"


def build_record(row: dict, lat: float, lon: float) -> dict:
    """Assemble the output record. Omit string fields whose source value is empty.

    Insertion order here is the authoritative JSON key order — matches the
    shape documented in the prompt.
    """
    record: dict = {}

    def put_str(key: str, value: str) -> None:
        trimmed = (value or "").strip()
        if trimmed:
            record[key] = trimmed

    def put_int(key: str, value: str) -> None:
        trimmed = (value or "").strip()
        if not trimmed:
            return
        try:
            record[key] = int(trimmed)
        except ValueError:
            pass

    put_int("markerNum", row.get("MarkerNum", ""))
    put_int("atlasNumber", row.get("Atlas_Number", ""))
    put_str("title", row.get("Title", ""))
    put_str("indexName", row.get("IndexName", ""))
    put_str("county", row.get("County", ""))
    put_int("countyId", row.get("CountyId", ""))
    put_str("city", row.get("City", ""))
    put_str("address", row.get("Address", ""))

    year = parse_year(row.get("Year", ""))
    if year is not None:
        record["year"] = year

    put_str("locationDesc", row.get("Loc_Desc", ""))

    record["latitude"] = lat
    record["longitude"] = lon

    record["privateProperty"] = parse_bool(row.get("PrivateProperty", ""))

    put_str("conditionText", row.get("ConditionText", ""))

    marker_text = (row.get("MarkerText") or "").strip()
    record["markerText"] = marker_text
    record["narrationText"] = clean_narration(marker_text)

    return record
