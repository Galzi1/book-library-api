import pytest
from fastapi.testclient import TestClient

import storage
from app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_books():
    storage.books.clear()
    yield
    storage.books.clear()


def test_create_book():
    payload = {"title": "Clean Code", "author": "Robert Martin", "genre": "Technology", "status": "reading"}
    response = client.post("/books", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert data["genre"] == payload["genre"]
    assert data["status"] == payload["status"]
    assert "id" in data
    assert "created_at" in data


def test_get_book():
    payload = {"title": "Refactoring", "author": "Martin Fowler", "genre": "Technology", "status": "finished"}
    create_resp = client.post("/books", json=payload)
    book_id = create_resp.json()["id"]

    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == book_id
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]


def test_delete_book():
    payload = {"title": "The Mythical Man-Month", "author": "Fred Brooks", "genre": "Technology", "status": "want-to-read"}
    create_resp = client.post("/books", json=payload)
    book_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/books/{book_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"deleted": True}

    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 404


def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "by_status" in data
    assert "finished_percentage" in data
