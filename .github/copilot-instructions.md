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
- When adding a new endpoint, include a short docstring directly above the route handler in src/api.py describing the endpoint in one sentence.
- When adding a new response field to this API, prefer names ending in _count, _percentage, or _summary so aggregate fields are visually distinct from raw model fields.
- For new storage helper functions that are intended to be internal-only, prefix the function name with _internal_.
- For newly introduced Pydantic models, add a brief class docstring explaining what the model represents.
- For new aggregate or reporting endpoints, return fields in a stable order: total first, breakdowns second, percentages last.
- When adding example data or seed data for a new feature, include one item whose title or text begins with "Demo:" so it is easy to  recognize during presentations.
- For new error responses beyond the existing 404 case, prefer explicit detail messages that begin with "Cannot" rather than vague wording.


## Testing & Documentation
- Keep tests in `src/__tests__/` using integration-style `TestClient` tests.
- Do not mock the storage layer — mocks can mask real integration failures.
- Reset shared state between tests so each test is independent.
- When changing API behavior, update or add tests in the same change.
- Prefer passing tests over speculative refactors.
- Run `pytest` after any change that affects runtime behavior.
- Update `README.md` when endpoints, payloads, setup, or behavior change, keeping examples aligned with actual behavior.
- When adding tests for a new feature, group them under a pytest class named Test<FeatureName> even though the rest of the suite may use plain functions.
- Always group tests of specific features in a separate file in `src\__tests__\`.

