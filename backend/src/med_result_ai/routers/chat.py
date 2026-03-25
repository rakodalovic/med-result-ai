"""Chat endpoint for follow-up questions about blood test results."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from med_result_ai.database import get_db
from med_result_ai.models import BloodTest, Message
from med_result_ai.services.ai_service import chat

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    blood_test_id: int
    message: str


@router.post("/chat")
def send_message(
    body: ChatRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Send a follow-up question about a blood test.

    Builds context from the blood test data, any existing analysis,
    and the full conversation history, then generates an AI reply.
    Both user and assistant messages are persisted.
    """
    blood_test = db.get(BloodTest, body.blood_test_id)
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

    latest_analysis = (
        blood_test.analyses[-1].ai_analysis
        if blood_test.analyses
        else None
    )

    history = [
        {"role": msg.role, "content": msg.content}
        for msg in sorted(blood_test.messages, key=lambda m: m.created_at)
    ]

    try:
        ai_reply = chat(
            ocr_text=blood_test.ocr_text,
            ai_analysis=latest_analysis,
            history=history,
            user_message=body.message,
        )
    except RuntimeError as e:
        logger.exception(
            "chat failed for blood_test %d", body.blood_test_id
        )
        raise HTTPException(status_code=500, detail=str(e))

    user_msg = Message(
        blood_test_id=blood_test.id,
        role="user",
        content=body.message,
    )
    assistant_msg = Message(
        blood_test_id=blood_test.id,
        role="assistant",
        content=ai_reply,
    )
    db.add_all([user_msg, assistant_msg])
    db.commit()
    db.refresh(assistant_msg)

    return {
        "id": assistant_msg.id,
        "blood_test_id": blood_test.id,
        "role": "assistant",
        "content": ai_reply,
    }
