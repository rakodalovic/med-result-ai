"""OCR processing endpoint for blood test images."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from med_result_ai.database import DbSession
from med_result_ai.models import BloodTest
from med_result_ai.services.ocr_service import extract_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["ocr"])


@router.post("/blood-tests/{blood_test_id}/ocr")
def run_ocr(
    blood_test_id: int,
    db: DbSession,
) -> dict[str, Any]:
    """Run OCR on an uploaded blood test image.

    Preprocesses the image, extracts text via Tesseract,
    and stores the result in the database.
    """
    blood_test = db.get(BloodTest, blood_test_id)
    if not blood_test:
        raise HTTPException(
            status_code=404,
            detail="blood test not found.",
        )

    if blood_test.ocr_text:
        return {
            "id": blood_test.id,
            "ocr_text": blood_test.ocr_text,
            "message": "ocr already completed.",
        }

    try:
        result = extract_text(blood_test.image_path)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="image file not found on disk.",
        ) from e
    except RuntimeError as e:
        logger.exception("ocr failed for blood_test %d", blood_test_id)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e

    blood_test.ocr_text = result.raw_text
    db.commit()

    return {
        "id": blood_test.id,
        "ocr_text": result.raw_text,
        "lines": result.lines,
    }
