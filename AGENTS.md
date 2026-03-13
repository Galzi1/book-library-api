# Agent Guide

Use this repository's Copilot agents and instructions with a bias toward small, verifiable changes.

## Before editing
- Read `.github/copilot-instructions.md`.
- Read the relevant source and test files together:
  - `src/models.py`
  - `src/storage.py`
  - `src/api.py`
  - `src/__tests__/test_app.py`

## Implementation rules
- Keep routes thin and move business logic into `src/storage.py`.
- Keep models in `src/models.py`.
- Preserve the in-memory storage design unless the task explicitly asks for a new persistence layer.
- Preserve response shapes unless the task explicitly changes the contract.
- Update tests and `README.md` when behavior changes.

## Validation
- Run `pytest` after code changes.
- Prefer finishing with passing tests over speculative refactors.
