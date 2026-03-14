from fastapi import HTTPException

import storage
from models import Book, BookCreate, Review, ReviewCreate, ReadingSession, ReadingSessionCreate
from app import app


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


@app.get("/books/{book_id}/reviews", response_model=list[Review])
def get_reviews(book_id: str) -> list[Review]:
    book_reviews = storage.list_reviews(book_id)
    if book_reviews is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_reviews


@app.post("/books/{book_id}/reviews", response_model=Review)
def add_review(book_id: str, data: ReviewCreate) -> Review:
    review = storage.create_review(book_id, data)
    if review is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return review


@app.get("/books/{book_id}/sessions", response_model=list[ReadingSession])
def list_sessions(book_id: str) -> list[ReadingSession]:
    """List all reading sessions recorded for a book."""
    result = storage.list_sessions(book_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


@app.post("/books/{book_id}/sessions", response_model=ReadingSession)
def add_session(book_id: str, data: ReadingSessionCreate) -> ReadingSession:
    """Record a new reading session for a book."""
    session = storage.create_session(book_id, data)
    if session is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return session


@app.get("/stats")
def get_stats() -> dict:
    return storage.get_reading_stats()
