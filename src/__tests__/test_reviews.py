import pytest
from fastapi.testclient import TestClient

import storage
from api import app

client = TestClient(app)

BOOK_PAYLOAD = {"title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction", "status": "reading"}


@pytest.fixture(autouse=True)
def clear_state():
    storage.books.clear()
    storage.reviews.clear()
    storage.sessions.clear()
    yield
    storage.books.clear()
    storage.reviews.clear()
    storage.sessions.clear()


def _create_book(payload=None) -> str:
    resp = client.post("/books", json=payload or BOOK_PAYLOAD)
    assert resp.status_code == 200
    return resp.json()["id"]


# ── Moved from test_app.py ────────────────────────────────────────────────────

def test_create_review_for_book():
    book_id = _create_book()

    review_payload = {"author": "Alice", "body": "Excellent world-building.", "rating": 5}
    response = client.post(f"/books/{book_id}/reviews", json=review_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["author"] == review_payload["author"]
    assert data["body"] == review_payload["body"]
    assert data["rating"] == review_payload["rating"]
    assert "id" in data
    assert "created_at" in data


def test_list_reviews_for_book():
    book_id = _create_book({"title": "Sapiens", "author": "Yuval Noah Harari", "genre": "History", "status": "finished"})

    client.post(f"/books/{book_id}/reviews", json={"author": "Alice", "body": "Thought-provoking.", "rating": 4})
    client.post(f"/books/{book_id}/reviews", json={"author": "Bob", "body": "Dense but worth it.", "rating": 5})

    response = client.get(f"/books/{book_id}/reviews")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert [r["author"] for r in data] == ["Alice", "Bob"]


def test_reviews_return_404_for_missing_book():
    response = client.get("/books/missing-book/reviews")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

    create_response = client.post(
        "/books/missing-book/reviews",
        json={"author": "Alice", "body": "Cannot exist.", "rating": 3},
    )
    assert create_response.status_code == 404
    assert create_response.json() == {"detail": "Book not found"}


def test_get_stats_includes_average_rating():
    first_book_id = _create_book({"title": "Clean Code", "author": "Robert Martin", "genre": "Technology", "status": "reading"})
    second_book_id = _create_book({"title": "Refactoring", "author": "Martin Fowler", "genre": "Technology", "status": "finished"})

    client.post(f"/books/{first_book_id}/reviews", json={"author": "Alice", "body": "Helpful.", "rating": 4})
    client.post(f"/books/{second_book_id}/reviews", json={"author": "Bob", "body": "Classic.", "rating": 5})

    response = client.get("/stats")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["average_rating"] == 4.5


def test_delete_book_removes_reviews_from_stats():
    book_id = _create_book({"title": "The Pragmatic Programmer", "author": "Andy Hunt", "genre": "Technology", "status": "finished"})

    client.post(f"/books/{book_id}/reviews", json={"author": "Alice", "body": "Great advice.", "rating": 5})

    assert client.get("/stats").json()["average_rating"] == 5.0

    assert client.delete(f"/books/{book_id}").status_code == 200

    reviews_response = client.get(f"/books/{book_id}/reviews")
    assert reviews_response.status_code == 404
    assert reviews_response.json() == {"detail": "Book not found"}

    after_delete = client.get("/stats")
    assert after_delete.status_code == 200
    assert after_delete.json()["average_rating"] is None


# ── New tests ─────────────────────────────────────────────────────────────────

def test_get_reviews_for_book_with_no_reviews():
    book_id = _create_book()

    response = client.get(f"/books/{book_id}/reviews")

    assert response.status_code == 200
    assert response.json() == []


def test_get_reviews_validates_all_fields_with_three_or_more_reviews():
    book_id = _create_book()
    review_inputs = [
        {"author": "Alice", "body": "Visionary.", "rating": 5},
        {"author": "Bob", "body": "Slow start but rewarding.", "rating": 3},
        {"author": "Carol", "body": "A timeless classic.", "rating": 4},
    ]
    for payload in review_inputs:
        client.post(f"/books/{book_id}/reviews", json=payload)

    response = client.get(f"/books/{book_id}/reviews")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for review, expected in zip(data, review_inputs):
        assert review["author"] == expected["author"]
        assert review["body"] == expected["body"]
        assert review["rating"] == expected["rating"]
        assert review["book_id"] == book_id
        assert isinstance(review["id"], str) and review["id"]
        assert isinstance(review["created_at"], str) and review["created_at"]


def test_create_review_for_missing_book_then_create_book_and_retry():
    review_payload = {"author": "Alice", "body": "Initially missing.", "rating": 4}

    missing_response = client.post("/books/nonexistent-id/reviews", json=review_payload)
    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Book not found"}

    book_id = _create_book()
    success_response = client.post(f"/books/{book_id}/reviews", json=review_payload)

    assert success_response.status_code == 200
    data = success_response.json()
    assert data["book_id"] == book_id
    assert data["author"] == review_payload["author"]
    assert data["body"] == review_payload["body"]
    assert data["rating"] == review_payload["rating"]


def test_get_reviews_of_missing_book_returns_404():
    response = client.get("/books/nonexistent-id/reviews")

    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
