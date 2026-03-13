# GitHub Copilot Instructions

## Project Overview
This repository is a small **Book Library REST API** built with **FastAPI** and **Python 3.13**.
It manages a personal reading list with CRUD endpoints and a small statistics endpoint.

## Architecture
- `src/app.py` creates the FastAPI app instance.
- `src/api.py` defines endpoints on the shared `app`.
- `src/models.py` contains Pydantic models and the `BookStatus` enum.
- `src/storage.py` owns the in-memory store and business logic.
- `src/seed.py` seeds sample data through the FastAPI lifespan hook.
- `src/__tests__/test_app.py` contains integration-style pytest coverage.

## Repository Rules
- Keep route handlers thin. Put business logic, mutations, and aggregate calculations in `src/storage.py`.
- Keep data models in `src/models.py`.
- Preserve the current in-memory storage approach unless a task explicitly asks for persistence.
- Use modern Python syntax and type hints everywhere.
- Follow the existing import style used by the project (`import storage`, `from models import ...`, `from app import app`).
- Use `BookStatus` values exactly as defined: `want-to-read`, `reading`, `finished`.
- Book IDs should remain string UUIDs generated with `str(uuid4())`.

## API Behavior
- Missing books should raise `HTTPException(status_code=404, detail="Book not found")`.
- Preserve existing response shapes unless the task explicitly changes the API contract.
- `/stats` currently returns `total`, `by_status`, and `finished_percentage`.

## Testing Expectations
- Keep tests in `src/__tests__/`.
- Prefer integration-style tests with `TestClient`.
- Do not mock the storage layer for normal endpoint tests.
- Reset shared state between tests so each test stays independent.
- When changing API behavior, update or add tests in the same change.

## Documentation Expectations
- Update `README.md` when endpoints, payloads, setup, or behavior change.
- Keep examples aligned with the actual API and current test coverage.

## Working Style
- Read the related model, storage, route, and test files before editing.
- Make surgical changes that match the current structure.
- Run `pytest` after changes that affect code or runtime behavior.
