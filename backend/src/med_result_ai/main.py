"""Main FastAPI application module."""

from fastapi import FastAPI

app = FastAPI(
    title="MedResult AI",
    description="Blood test result analyst.",
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Return health status of the application."""
    return {"status": "ok"}
