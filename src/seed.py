from contextlib import asynccontextmanager
from datetime import datetime, UTC

from fastapi import FastAPI

import storage
from models import BookCreate, ReadingSessionCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.create_book(BookCreate(
        title="The Pragmatic Programmer",
        author="Andrew Hunt and David Thomas",
        genre="Technology",
        status="want-to-read",
    ))
    dune = storage.create_book(BookCreate(
        title="Dune",
        author="Frank Herbert",
        genre="Science Fiction",
        status="reading",
    ))
    sapiens = storage.create_book(BookCreate(
        title="Sapiens",
        author="Yuval Noah Harari",
        genre="History",
        status="finished",
    ))
    storage.create_session(dune.id, ReadingSessionCreate(
        date=datetime(2026, 3, 10, 20, 0, tzinfo=UTC),
        minutes_read=45,
        pages_read=30,
        note="Demo: very engaging opening chapters",
    ))
    storage.create_session(dune.id, ReadingSessionCreate(
        date=datetime(2026, 3, 12, 21, 0, tzinfo=UTC),
        minutes_read=60,
        pages_read=42,
    ))
    storage.create_session(sapiens.id, ReadingSessionCreate(
        date=datetime(2026, 2, 20, 19, 0, tzinfo=UTC),
        minutes_read=90,
        pages_read=55,
        note="Finished the final section.",
    ))
    yield
