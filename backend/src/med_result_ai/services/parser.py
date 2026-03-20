"""Parse blood test values from OCR text into structured data."""

import json
import re

# pattern matches lines like "Hemoglobin: 14.5 g/dL" or "WBC 6.2 10^3/uL"
_VALUE_PATTERN = re.compile(
    r"(?P<name>[A-Za-z\s\(\)]+?)\s*[:=]?\s*"
    r"(?P<value>\d+\.?\d*)\s*"
    r"(?P<unit>[A-Za-z/%\^·\d]+(?:/[A-Za-z]+)?)?",
)


def parse_blood_test_values(
    ocr_text: str,
) -> list[dict[str, str | float]]:
    """Extract biomarker name, value, and unit from OCR text.

    Args:
        ocr_text: Raw text from OCR.

    Returns:
        List of dicts with name, value, and unit keys.
    """
    results: list[dict[str, str | float]] = []
    seen: set[str] = set()

    for line in ocr_text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = _VALUE_PATTERN.search(line)
        if not match:
            continue

        name = match.group("name").strip()
        if len(name) < 2 or name.lower() in seen:  # noqa: PLR2004
            continue

        seen.add(name.lower())
        results.append({
            "name": name,
            "value": float(match.group("value")),
            "unit": (match.group("unit") or "").strip(),
        })

    return results


def parsed_values_to_json(
    values: list[dict[str, str | float]],
) -> str:
    """Serialize parsed values to a JSON string for db storage."""
    return json.dumps(values)
