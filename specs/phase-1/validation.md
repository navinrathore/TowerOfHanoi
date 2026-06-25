# Phase 1 Validation — Project Scaffolding & Hello FastAPI

## Definition of Done

All of the following must be true before this phase is considered complete.

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
Must exit with code 0 and report success with no type errors.

### 2. Unit Tests Pass
```bash
pytest
```
Must exit with code 0 and pass all tests.

### 3. Server Runs & Responds Correctly

#### Dev Run
```bash
uvicorn main:app --port 8000
```
Must start successfully without any stack traces or errors.

#### API Response Check
```bash
curl -s http://localhost:8000/
```
Must return HTTP 200 with the exact body:
```json
{"status": "ok", "message": "MyTowerOfHanoi API is open"}
```
