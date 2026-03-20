"""AI service for medical text analysis via OpenRouter."""

import logging

from openai import OpenAI

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

    try:
        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Please analyze the following blood test"
                        f" results:\n\n{ocr_text}"
                    ),
                },
            ],
        )
    except Exception as e:
        msg = f"llm api call failed: {e}"
        raise RuntimeError(msg) from e

    return response.choices[0].message.content or ""
