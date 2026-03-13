from contextlib import asynccontextmanager

from fastapi import FastAPI

import storage
from models import BookCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.create_book(BookCreate(
        title="The Pragmatic Programmer",
        author="David Thomas",
        genre="Technology",
        status="want-to-read",
    ))
    storage.create_book(BookCreate(
        title="Dune",
        author="Frank Herbert",
        genre="Science Fiction",
        status="reading",
    ))
    storage.create_book(BookCreate(
        title="Sapiens",
        author="Yuval Noah Harari",
        genre="History",
        status="finished",
    ))
    yield
