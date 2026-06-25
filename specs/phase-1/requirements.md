# Phase 1 Requirements — Project Scaffolding & Hello FastAPI

## Scope

Establish the initial Python environment, install essential libraries, and set up a minimal FastAPI application. Ensure the dev server runs, type checking is functional, linting passes, and unit tests can execute.

1. **Python Dependencies**:
   - `requirements.txt` containing FastAPI, Uvicorn, pytest, Ruff, Mypy.
2. **FastAPI Scaffold**:
   - `main.py` initialized.
   - A single endpoint `GET /` returning a JSON greeting `{"message": "MyTowerOfHanoi API is open"}` and server status.
3. **Quality & Validation Scripts**:
   - Basic test suite skeleton in `tests/test_main.py` verifying the `GET /` response.
   - Strict static type-checking setup with a configured `mypy` check.
   - Linting and formatting setup with `ruff`.

## Out of Scope

- No game state engine or rules logic (Phase 2).
- No database tables, SQLAlchemy models, or SQLite connections (Phase 3).
- No web templates, Jinja2 layouts, or CSS/JS static files (Phase 4).
- No solver algorithms (Phase 5).

## Design Decisions

### Python Version & Dependencies
- Pin exact versions (or minimal compatible versions) in `requirements.txt`.
- Target Python 3.10 or higher.

### Code Quality Rules
- PEP 8 compliance checked via Ruff.
- Strict type hinting checked via Mypy (typecheck command must run cleanly).
- Automated tests using pytest to ensure the server starts and serves correct endpoints.

## Context

This phase ensures the core runtime environment is configured correctly. Once Phase 1 is validated, we have a functional base to implement the game logic engine (Phase 2).

## Stakeholder Notes

- **Mary** wants reliable type-hints and linting rules enforced from the start.
- **Steve** needs a running endpoint that we can easily verify.
