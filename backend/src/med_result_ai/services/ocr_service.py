"""OCR service using Tesseract for text extraction."""

import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pytesseract

from med_result_ai.services.preprocessing import preprocess_image

logger = logging.getLogger(__name__)


@dataclass
class OcrResult:
    """Structured result from OCR processing."""

    raw_text: str
    lines: list[dict[str, str | float]]


def extract_text(image_path: str) -> OcrResult:
    """Extract text from a blood test image using Tesseract.

    Runs the preprocessing pipeline first, then feeds the
    cleaned image to Tesseract.

    Args:
        image_path: Path to the original uploaded image.

    Returns:
        OcrResult with raw text and per-line confidence data.

    Raises:
        FileNotFoundError: If the image does not exist.
        RuntimeError: If OCR processing fails.
    """
    path = Path(image_path)
    if not path.exists():
        msg = f"image not found: {image_path}"
        raise FileNotFoundError(msg)

    preprocessed = preprocess_image(image_path, save_debug=True)

    try:
        data = pytesseract.image_to_data(
            preprocessed, output_type=pytesseract.Output.DICT
        )
    except pytesseract.TesseractError as e:
        msg = f"ocr processing failed: {e}"
        raise RuntimeError(msg) from e

    lines = _build_lines(data)
    raw_text = "\n".join(str(line["text"]) for line in lines)

    return OcrResult(raw_text=raw_text, lines=lines)


def _build_lines(
    data: dict[str, list],
) -> list[dict[str, str | float]]:
    """Group Tesseract word-level output into lines with confidence."""
    lines: list[dict[str, str | float]] = []
    current_line_num = -1
    current_words: list[str] = []
    current_confidences: list[float] = []

    for i, text in enumerate(data["text"]):
        text = text.strip()
        if not text:
            continue

        line_num = data["line_num"][i]
        conf = float(data["conf"][i])

        if line_num != current_line_num:
            if current_words:
                lines.append(_finalize_line(
                    current_words, current_confidences
                ))
            current_line_num = line_num
            current_words = []
            current_confidences = []

        current_words.append(text)
        current_confidences.append(conf)

    if current_words:
        lines.append(_finalize_line(current_words, current_confidences))

    return lines


def _finalize_line(
    words: list[str],
    confidences: list[float],
) -> dict[str, str | float]:
    """Create a line dict from accumulated words and confidences."""
    avg_conf = np.mean(confidences) if confidences else 0.0
    return {
        "text": " ".join(words),
        "confidence": round(float(avg_conf), 3),
    }
