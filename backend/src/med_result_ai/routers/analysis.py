"""Blood test analysis endpoint."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from med_result_ai.database import get_db
from med_result_ai.models import Analysis, BloodTest
from med_result_ai.services.ai_service import analyze_blood_test
from med_result_ai.services.parser import (
    parse_blood_test_values,
    parsed_values_to_json,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/blood-tests/{blood_test_id}/analyze")
def run_analysis(
    blood_test_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Analyze a blood test using the LLM.

    Parses biomarker values from OCR text, sends them to the
    LLM for interpretation, and stores both in the database.
    Requires OCR to have been run first.
    """
    blood_test = db.get(BloodTest, blood_test_id)
    if not blood_test:
        raise HTTPException(
            status_code=404,
            detail="blood test not found.",
        )

    if not blood_test.ocr_text:
        raise HTTPException(
            status_code=400,
            detail="ocr has not been run yet. run ocr first.",
        )

    parsed_values = parse_blood_test_values(blood_test.ocr_text)

    blood_test.parsed_data = parsed_values_to_json(parsed_values)

    try:
        ai_result = analyze_blood_test(blood_test.ocr_text)
    except RuntimeError as e:
        logger.exception(
            "analysis failed for blood_test %d", blood_test_id
        )
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    analysis = Analysis(
        blood_test_id=blood_test.id,
        ai_analysis=ai_result,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
        "id": analysis.id,
        "blood_test_id": blood_test.id,
        "parsed_values": parsed_values,
        "ai_analysis": ai_result,
    }
