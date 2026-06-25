# Phase 1 Plan — Project Scaffolding & Hello FastAPI

## Group 1 — Environment Setup

1. Create `requirements.txt` listing:
   - `fastapi`
   - `uvicorn`
   - `pytest`
   - `httpx` (for test client async calls)
   - `ruff`
   - `mypy`
2. Create `pyproject.toml` with default configuration for:
   - `ruff` (linter/formatter rules)
   - `mypy` (strict type-checking settings)

## Group 2 — Application Scaffold

3. Create `main.py` with:
   - FastAPI app instance.
   - An asynchronous `GET /` endpoint returning `{"status": "ok", "message": "MyTowerOfHanoi API is open"}`.
   - Standard FastAPI lifespan hooks if needed (none required for Phase 1).

## Group 3 — Testing & Quality Verification

4. Create `tests/` directory.
5. Create `tests/__init__.py` to make it a package.
6. Create `tests/test_main.py` using `fastapi.testclient.TestClient` to verify:
   - `GET /` returns status 200.
   - Response JSON matches `{"status": "ok", "message": "MyTowerOfHanoi API is open"}`.

## Group 4 — Execution & Validation

7. Check linting: run `ruff check .`
8. Check formatting: run `ruff format --check .`
9. Check types: run `mypy .`
10. Run tests: run `pytest`
11. Run development server: run `uvicorn main:app --port 8000 --reload`
