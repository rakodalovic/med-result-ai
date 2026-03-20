"""SQLAlchemy ORM models."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Base class for all models."""


class BloodTest(Base):
    """Uploaded blood test record."""

    __tablename__ = "blood_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_path: Mapped[str] = mapped_column(String(500))
    ocr_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    analyses: Mapped[list["Analysis"]] = relationship(
        back_populates="blood_test", cascade="all, delete-orphan"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="blood_test", cascade="all, delete-orphan"
    )


class Analysis(Base):
    """AI-generated analysis of a blood test."""

    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    blood_test_id: Mapped[int] = mapped_column(
        ForeignKey("blood_tests.id", ondelete="CASCADE")
    )
    ai_analysis: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    blood_test: Mapped["BloodTest"] = relationship(
        back_populates="analyses"
    )


class Message(Base):
    """Chat message related to a blood test."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    blood_test_id: Mapped[int] = mapped_column(
        ForeignKey("blood_tests.id", ondelete="CASCADE")
    )
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    blood_test: Mapped["BloodTest"] = relationship(
        back_populates="messages"
    )
