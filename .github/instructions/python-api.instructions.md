---
description: "Guidance for Python source files in the Book Library FastAPI API"
applyTo: "src/**/*.py"
---

# Python API Instructions

- Use Python 3.13 syntax and explicit type hints.
- Keep file responsibilities strict:
  - models in `src/models.py`
  - storage and derived calculations in `src/storage.py`
  - HTTP handlers in `src/api.py`
  - app creation and lifespan wiring in `src/app.py` and `src/seed.py`
- Route handlers should mostly validate HTTP concerns and delegate to storage functions.
- Preserve the current import style and module layout unless a task explicitly requires restructuring.
- Add or update type hints for any new or changed code.
- Prefer small, composable storage helpers over putting business logic in routes.
- Preserve existing API contracts unless the task explicitly asks for a breaking change.
- For missing books, use `HTTPException(status_code=404, detail="Book not found")`.
- Keep comments rare and only add them when the code would otherwise be hard to parse.
