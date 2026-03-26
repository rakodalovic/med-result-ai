"""Blood test image upload endpoint."""

import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from med_result_ai.config import settings
from med_result_ai.database import DbSession
from med_result_ai.models import BloodTest

router = APIRouter(prefix="/api", tags=["upload"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
def upload_blood_test(
    file: UploadFile,
    db: DbSession,
) -> dict[str, int]:
    """Upload a blood test image.

    Accepts JPEG or PNG files up to 10 MB.
    Returns the blood test record ID.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="invalid file type. only jpeg and png are allowed.",
        )

    contents = file.file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="file too large. maximum size is 10 mb.",
        )

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "image.png").suffix
    filename = f"{uuid.uuid4()}{extension}"
    file_path = upload_dir / filename
    file_path.write_bytes(contents)

    blood_test = BloodTest(image_path=str(file_path))
    db.add(blood_test)
    db.commit()
    db.refresh(blood_test)

    return {"id": blood_test.id}
