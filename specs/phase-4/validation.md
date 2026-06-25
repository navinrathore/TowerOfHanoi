# Phase 4 Validation — Interactive Web UI (Playable Mode)

## Definition of Done

All checks in this document must pass before Phase 4 is considered complete.

### 1. Code Quality & Format Checks

#### Linting
```bash
ruff check .
```
Must exit with code 0 and report no linting errors.

#### Formatting
```bash
ruff format --check .
```
Must exit with code 0 and report no formatting violations.

#### Type Checking
```bash
mypy .
```
Must exit with code 0 and report success with no type errors. The newly implemented Pydantic schemas, endpoint routes, and test clients must be fully type-hinted.

### 2. Unit & Integration Tests Pass

```bash
pytest
```
Must exit with code 0 and pass all 17 tests. This includes verifying:
- `/` HTML rendering (`tests/test_main.py` and `tests/test_api.py`).
- Batch game run transactions with moves lists (`tests/test_api.py`).
- boundary validation rules for out of bounds parameters (`tests/test_api.py`).
- Recent runs retrieval and order sorting (`tests/test_api.py`).

### 3. API Transaction Verification Script

To verify that the database correctly logs a batch game run and its moves in a transaction, run:

```bash
python -c "
from fastapi.testclient import TestClient
from main import app
from datetime import datetime, UTC

client = TestClient(app)
payload = {
    'num_disks': 3,
    'solver_type': 'manual',
    'start_time': datetime.now(UTC).isoformat(),
    'end_time': datetime.now(UTC).isoformat(),
    'total_moves': 3,
    'moves': [
        {'from_peg': 0, 'to_peg': 2},
        {'from_peg': 0, 'to_peg': 1},
        {'from_peg': 2, 'to_peg': 1}
    ]
}

response = client.post('/api/runs', json=payload)
assert response.status_code == 201
data = response.json()
assert data['is_completed'] is True
assert len(data['moves']) == 3
print('API Transaction Validation Succeeded!')
"
```
Must print `API Transaction Validation Succeeded!` and execute without throwing exceptions.
