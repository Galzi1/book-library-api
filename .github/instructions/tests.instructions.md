---
description: "Guidance for pytest integration tests in this repository"
applyTo: "src/__tests__/**/*.py"
---

# Test Instructions

- Write endpoint tests with `pytest` and `TestClient`.
- Treat tests as integration tests for the FastAPI app, not isolated unit tests.
- Do not mock `storage` for normal API tests.
- Reset `storage.books` between tests so test order never matters.
- Assert both HTTP status codes and meaningful response body details.
- Cover happy paths and error paths together when behavior changes.
- Keep tests readable and direct; this project favors simple assertions over heavy abstraction.
