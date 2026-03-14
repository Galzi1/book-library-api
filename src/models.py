from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class BookStatus(StrEnum):
    want_to_read = "want-to-read"
    reading = "reading"
    finished = "finished"


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    status: BookStatus


class Book(BookCreate):
    id: str
    created_at: datetime


class ReviewCreate(BaseModel):
    author: str
    body: str
    rating: int = Field(ge=1, le=5)


class Review(ReviewCreate):
    id: str
    book_id: str
    created_at: datetime


class ReadingSessionCreate(BaseModel):
    """Payload for logging a reading session against a book."""

    date: datetime
    minutes_read: int = Field(ge=1)
    pages_read: int = Field(ge=1)
    note: str | None = None

    @field_validator("date", mode="before")
    @classmethod
    def _require_timezone(cls, v: object) -> object:
        if isinstance(v, datetime) and v.tzinfo is None:
            raise ValueError("date must include timezone information")
        return v


class ReadingSession(ReadingSessionCreate):
    """A logged reading session associated with a specific book."""

    id: str
    book_id: str
