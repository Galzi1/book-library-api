# GitHub Copilot Instructions

## Project Overview
This repository is a small **Book Library REST API** built with FastAPI and Python 3.13.
It manages a personal reading list with CRUD endpoints and a statistics endpoint.

## Tech Stack
- **Runtime**: Python 3.13
- **Framework**: FastAPI
- **Models/Validation**: Pydantic v2
- **Testing**: pytest with FastAPI's `TestClient`
- **Storage**: In-memory (no database)

## Project Structure
- `src/app.py` — creates the FastAPI app instance
- `src/api.py` — defines all route handlers on the shared `app`
- `src/models.py` — Pydantic models and the `BookStatus` enum
- `src/storage.py` — in-memory store and all business logic
- `src/seed.py` — seeds sample data via the FastAPI lifespan hook
- `src/__tests__/test_app.py` — integration-style pytest coverage

## Coding Guidelines
- Keep route handlers thin. All business logic, mutations, and aggregate calculations belong in `src/storage.py`.
- Keep data models in `src/models.py`.
- Use modern Python syntax and type hints everywhere.
- Follow the existing import style: `import storage`, `from models import ...`, `from app import app`.
- Use `BookStatus` values exactly as defined: `want-to-read`, `reading`, `finished`.
- Generate book IDs with `str(uuid4())`.
- Missing books must raise `HTTPException(status_code=404, detail="Book not found")`.
- Preserve existing response shapes unless the task explicitly changes the API contract.
- `/stats` returns `total`, `by_status`, and `finished_percentage`.
- Preserve the in-memory storage design unless the task explicitly asks for persistence.

## Testing & Documentation
- Keep tests in `src/__tests__/` using integration-style `TestClient` tests.
- Do not mock the storage layer — mocks can mask real integration failures.
- Reset shared state between tests so each test is independent.
- When changing API behavior, update or add tests in the same change.
- Prefer passing tests over speculative refactors.
- Run `pytest` after any change that affects runtime behavior.
- Update `README.md` when endpoints, payloads, setup, or behavior change, keeping examples aligned with actual behavior.
