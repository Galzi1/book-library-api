from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

import storage
from models import Book, BookCreate


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


app = FastAPI(title="Book Library API", lifespan=lifespan)


@app.get("/books", response_model=list[Book])
def list_books() -> list[Book]:
    return storage.get_all_books()


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: str) -> Book:
    book = storage.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=Book)
def create_book(data: BookCreate) -> Book:
    return storage.create_book(data)


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: str, data: BookCreate) -> Book:
    book = storage.update_book(book_id, data)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: str) -> dict:
    deleted = storage.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"deleted": True}


@app.get("/stats")
def get_stats() -> dict:
    return storage.get_reading_stats()
