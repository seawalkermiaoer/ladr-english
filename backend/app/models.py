from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class WordCreate(BaseModel):
    """Request model to create a word."""

    text: str = Field(min_length=1, max_length=256)
    definition: Optional[str] = Field(default=None, max_length=2048)
    source: Optional[str] = Field(default=None, max_length=1024)


class WordUpdate(BaseModel):
    """Request model to update a word."""

    text: Optional[str] = Field(default=None, min_length=1, max_length=256)
    definition: Optional[str] = Field(default=None, max_length=2048)
    source: Optional[str] = Field(default=None, max_length=1024)


class WordOut(BaseModel):
    """Response model for a word."""

    id: int
    text: str
    definition: Optional[str]
    source: Optional[str]
    created_at: datetime
    last_reviewed: Optional[datetime]
    review_count: int
    easiness: float
    due_date: Optional[datetime]

    class Config:
        from_attributes = True


class WordListOut(BaseModel):
    """Paginated word list response."""

    total: int
    items: list[WordOut]


class ReviewIn(BaseModel):
    """Review request payload."""

    quality: int = Field(ge=0, le=5)


class StatsOut(BaseModel):
    """Statistics response model."""

    total: int
    reviewed: int
    due_today: int

