from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


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
