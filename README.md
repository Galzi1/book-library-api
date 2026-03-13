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
