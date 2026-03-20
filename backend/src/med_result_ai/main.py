"""Main FastAPI application module."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from med_result_ai.database import engine
from med_result_ai.models import Base
from med_result_ai.routers import preprocess, upload


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


app.include_router(preprocess.router)
app.include_router(upload.router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Return health status of the application."""
    return {"status": "ok"}
