"""Image preprocessing endpoint for blood test images."""

import logging

import cv2
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from med_result_ai.database import get_db
from med_result_ai.models import BloodTest
from med_result_ai.services.preprocessing import preprocess_image

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["preprocess"])


@router.post("/blood-tests/{blood_test_id}/preprocess")
def run_preprocessing(
    blood_test_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """Preprocess a blood test image for OCR.

    Returns the preprocessed image as a PNG.
    Also saves a debug copy next to the original.
    """
    blood_test = db.get(BloodTest, blood_test_id)
    if not blood_test:
        raise HTTPException(
            status_code=404,
            detail="blood test not found.",
        )

    try:
        result = preprocess_image(
            blood_test.image_path, save_debug=True
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="image file not found on disk.",
        )

    _, encoded = cv2.imencode(".png", result)

    return Response(
        content=encoded.tobytes(),
        media_type="image/png",
    )
