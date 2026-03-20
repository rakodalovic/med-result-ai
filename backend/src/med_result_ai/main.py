"""Main FastAPI application module."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from med_result_ai.database import engine
from med_result_ai.models import Base


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MedResult AI",
    description="Blood test result analyst.",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Return health status of the application."""
    return {"status": "ok"}
