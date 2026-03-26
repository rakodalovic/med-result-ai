"""AI service for medical text analysis via OpenRouter."""

import logging

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from med_result_ai.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a medical laboratory result analyst. Your role is to:

1. Analyze blood test results extracted via OCR.
2. Identify values that are outside normal reference ranges.
3. Explain what each biomarker measures and why it matters.
4. Provide a clear, structured summary of the findings.
5. Suggest possible follow-up actions in general terms.

Important:
- Always state that this is not a medical diagnosis.
- Recommend consulting a healthcare professional.
- Use plain language that a non-medical person can understand.
- If OCR text is unclear or incomplete, note which parts are uncertain.
"""


def get_client() -> OpenAI:
    """Create an OpenRouter-compatible OpenAI client."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )


def analyze_blood_test(ocr_text: str) -> str:
    """Send OCR text to the LLM for medical analysis.

    Args:
        ocr_text: Raw text extracted from a blood test image.

    Returns:
        The LLM's analysis as a string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client()

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Please analyze the following blood test"
                f" results:\n\n{ocr_text}"
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=messages,
        )
    except Exception as e:
        msg = f"llm api call failed: {e}"
        raise RuntimeError(msg) from e

    return response.choices[0].message.content or ""


CHAT_SYSTEM_PROMPT = """\
You are a medical laboratory result assistant. The user has uploaded a \
blood test and you are helping them understand the results through \
conversation.

You have access to the following blood test data:

--- OCR TEXT ---
{ocr_text}
--- END OCR TEXT ---

{analysis_section}

Rules:
- Answer follow-up questions based on the blood test results above.
- Always state that this is not a medical diagnosis.
- Recommend consulting a healthcare professional for any concerns.
- Use plain language that a non-medical person can understand.
- If you cannot answer a question from the available data, say so.
"""


def chat(
    ocr_text: str,
    ai_analysis: str | None,
    history: list[ChatCompletionMessageParam],
    user_message: str,
) -> str:
    """Generate a chat response with blood test context.

    Args:
        ocr_text: OCR text from the blood test.
        ai_analysis: Previous AI analysis, if available.
        history: Prior chat messages as [{"role": ..., "content": ...}].
        user_message: The new user message.

    Returns:
        The assistant's reply.

    Raises:
        RuntimeError: If the API call fails.
    """
    analysis_section = (
        f"--- PREVIOUS ANALYSIS ---\n{ai_analysis}\n--- END ANALYSIS ---"
        if ai_analysis
        else "No analysis has been run yet."
    )

    system = CHAT_SYSTEM_PROMPT.format(
        ocr_text=ocr_text,
        analysis_section=analysis_section,
    )

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system},
        *history,
        {"role": "user", "content": user_message},
    ]

    client = get_client()

    try:
        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=messages,
        )
    except Exception as e:
        msg = f"llm api call failed: {e}"
        raise RuntimeError(msg) from e

    return response.choices[0].message.content or ""
