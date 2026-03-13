from datetime import datetime, UTC
from uuid import uuid4

from models import Book, BookCreate, BookStatus

books: dict[str, Book] = {}


def get_all_books() -> list[Book]:
    return list(books.values())


def get_book(book_id: str) -> Book | None:
    return books.get(book_id)


def create_book(data: BookCreate) -> Book:
    book = Book(
        id=str(uuid4()),
        created_at=datetime.now(UTC),
        **data.model_dump(),
    )
    books[book.id] = book
    return book


def update_book(book_id: str, data: BookCreate) -> Book | None:
    existing = books.get(book_id)
    if existing is None:
        return None
    updated = Book(
        id=existing.id,
        created_at=existing.created_at,
        **data.model_dump(),
    )
    books[book_id] = updated
    return updated


def delete_book(book_id: str) -> bool:
    if book_id not in books:
        return False
    del books[book_id]
    return True


def get_reading_stats() -> dict:
    total = len(books)
    by_status: dict[str, int] = {status.value: 0 for status in BookStatus}
    for book in books.values():
        by_status[book.status.value] += 1
    finished = by_status[BookStatus.finished.value]
    finished_percentage = round(finished / total * 100, 1) if total > 0 else 0.0
    return {
        "total": total,
        "by_status": by_status,
        "finished_percentage": finished_percentage,
    }
