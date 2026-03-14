from datetime import datetime, UTC
from uuid import uuid4

from models import Book, BookCreate, BookStatus, Review, ReviewCreate, ReadingSession, ReadingSessionCreate

books: dict[str, Book] = {}
reviews: dict[str, list[Review]] = {}
sessions: dict[str, list[ReadingSession]] = {}


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
    reviews.pop(book_id, None)
    sessions.pop(book_id, None)
    return True


def list_reviews(book_id: str) -> list[Review] | None:
    if book_id not in books:
        return None
    return reviews.get(book_id, [])


def create_review(book_id: str, data: ReviewCreate) -> Review | None:
    if book_id not in books:
        return None
    review = Review(
        id=str(uuid4()),
        book_id=book_id,
        created_at=datetime.now(UTC),
        **data.model_dump(),
    )
    reviews.setdefault(book_id, []).append(review)
    return review


def get_reading_stats() -> dict:
    total = len(books)
    by_status: dict[str, int] = {status.value: 0 for status in BookStatus}
    for book in books.values():
        by_status[book.status.value] += 1
    finished = by_status[BookStatus.finished.value]
    finished_percentage = round(finished / total * 100, 1) if total > 0 else 0.0
    all_reviews = [review for book_reviews in reviews.values() for review in book_reviews]
    average_rating = round(
        sum(review.rating for review in all_reviews) / len(all_reviews),
        1,
    ) if all_reviews else None
    all_sessions = [s for book_sessions in sessions.values() for s in book_sessions]
    return {
        "total": total,
        "by_status": by_status,
        "finished_percentage": finished_percentage,
        "average_rating": average_rating,
        "sessions_count": len(all_sessions),
        "total_minutes_read": sum(s.minutes_read for s in all_sessions),
        "total_pages_read": sum(s.pages_read for s in all_sessions),
    }


def list_sessions(book_id: str) -> list[ReadingSession] | None:
    if book_id not in books:
        return None
    return sessions.get(book_id, [])


def create_session(book_id: str, data: ReadingSessionCreate) -> ReadingSession | None:
    if book_id not in books:
        return None
    session = ReadingSession(
        id=str(uuid4()),
        book_id=book_id,
        **data.model_dump(),
    )
    sessions.setdefault(book_id, []).append(session)
    return session

# Search books by author or title, case-insensitive returning a list of matching books
def search_books(query: str) -> list[Book]:
    query_lower = query.lower()
    return [
        book for book in books.values()
        if query_lower in book.title.lower() or query_lower in book.author.lower()
    ]
