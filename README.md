# book-library-api

REST API for managing a personal book library, built with FastAPI.

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
uvicorn src.api:app --reload
```

## Testing

```bash
pytest
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/books` | List all books |
| `POST` | `/books` | Add a book |
| `GET` | `/books/{id}` | Get a book |
| `PUT` | `/books/{id}` | Update a book |
| `DELETE` | `/books/{id}` | Delete a book |
| `GET` | `/books/{id}/reviews` | List reviews for a book |
| `POST` | `/books/{id}/reviews` | Add a review for a book |
| `GET` | `/books/{id}/sessions` | List reading sessions for a book |
| `POST` | `/books/{id}/sessions` | Record a reading session for a book |
| `GET` | `/stats` | Reading statistics |

## Book schema

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "genre": "Science Fiction",
  "status": "reading"
}
```

Valid `status` values: `want-to-read`, `reading`, `finished`

## Review schema

```json
{
  "author": "Alice",
  "body": "Excellent world-building.",
  "rating": 5
}
```

Valid `rating` values: integers from `1` to `5`

## Reading session schema

```json
{
  "date": "2026-03-10T20:00:00Z",
  "minutes_read": 45,
  "pages_read": 30,
  "note": "Optional note about the session"
}
```

`note` is optional and may be omitted or set to `null`.

## Stats response

`GET /stats` returns:

```json
{
  "total": 2,
  "by_status": {
    "want-to-read": 0,
    "reading": 1,
    "finished": 1
  },
  "finished_percentage": 50.0,
  "average_rating": 4.5,
  "sessions_count": 3,
  "total_minutes_read": 195,
  "total_pages_read": 127
}
```

When there are no reviews, `average_rating` is `null`. Session totals are `0` when no sessions have been recorded.
