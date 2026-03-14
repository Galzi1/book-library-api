import pytest
from fastapi.testclient import TestClient

import storage
from api import app

client = TestClient(app)

BOOK_PAYLOAD = {"title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction", "status": "reading"}
SESSION_PAYLOAD = {
    "date": "2026-03-10T20:00:00Z",
    "minutes_read": 45,
    "pages_read": 30,
    "note": "Gripping start.",
}


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


class TestReadingSessions:
    def test_create_session_returns_session_fields(self):
        book_id = _create_book()

        resp = client.post(f"/books/{book_id}/sessions", json=SESSION_PAYLOAD)

        assert resp.status_code == 200
        data = resp.json()
        assert data["book_id"] == book_id
        assert data["minutes_read"] == SESSION_PAYLOAD["minutes_read"]
        assert data["pages_read"] == SESSION_PAYLOAD["pages_read"]
        assert data["note"] == SESSION_PAYLOAD["note"]
        assert "id" in data
        assert "date" in data

    def test_create_session_without_note(self):
        book_id = _create_book()
        payload = {**SESSION_PAYLOAD, "note": None}

        resp = client.post(f"/books/{book_id}/sessions", json=payload)

        assert resp.status_code == 200
        assert resp.json()["note"] is None

    def test_list_sessions_empty_for_new_book(self):
        book_id = _create_book()

        resp = client.get(f"/books/{book_id}/sessions")

        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_sessions_returns_all_created_sessions(self):
        book_id = _create_book()
        client.post(f"/books/{book_id}/sessions", json=SESSION_PAYLOAD)
        client.post(f"/books/{book_id}/sessions", json={
            "date": "2026-03-12T21:00:00Z",
            "minutes_read": 60,
            "pages_read": 42,
        })

        resp = client.get(f"/books/{book_id}/sessions")

        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["minutes_read"] == 45
        assert data[1]["minutes_read"] == 60

    def test_sessions_are_scoped_per_book(self):
        book_a = _create_book({"title": "Book A", "author": "A", "genre": "Fiction", "status": "reading"})
        book_b = _create_book({"title": "Book B", "author": "B", "genre": "Fiction", "status": "reading"})
        client.post(f"/books/{book_a}/sessions", json=SESSION_PAYLOAD)

        resp = client.get(f"/books/{book_b}/sessions")

        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_session_returns_404_for_missing_book(self):
        resp = client.post("/books/no-such-book/sessions", json=SESSION_PAYLOAD)

        assert resp.status_code == 404
        assert resp.json() == {"detail": "Book not found"}

    def test_list_sessions_returns_404_for_missing_book(self):
        resp = client.get("/books/no-such-book/sessions")

        assert resp.status_code == 404
        assert resp.json() == {"detail": "Book not found"}

    def test_delete_book_removes_its_sessions(self):
        book_id = _create_book()
        client.post(f"/books/{book_id}/sessions", json=SESSION_PAYLOAD)
        client.delete(f"/books/{book_id}")

        # Sessions dict should no longer contain this book's key
        assert book_id not in storage.sessions

    def test_stats_includes_session_aggregates(self):
        book_id = _create_book()
        client.post(f"/books/{book_id}/sessions", json=SESSION_PAYLOAD)
        client.post(f"/books/{book_id}/sessions", json={
            "date": "2026-03-12T21:00:00Z",
            "minutes_read": 60,
            "pages_read": 42,
        })

        resp = client.get("/stats")

        assert resp.status_code == 200
        data = resp.json()
        assert data["sessions_count"] == 2
        assert data["total_minutes_read"] == 105
        assert data["total_pages_read"] == 72

    def test_stats_session_totals_are_zero_with_no_sessions(self):
        resp = client.get("/stats")

        assert resp.status_code == 200
        data = resp.json()
        assert data["sessions_count"] == 0
        assert data["total_minutes_read"] == 0
        assert data["total_pages_read"] == 0
