# Phase 3 Validation — SQLite Database & SQLAlchemy Schemas

## Definition of Done

All checks in this document must pass before Phase 3 is considered complete.

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
Must exit with code 0 and report success with no type errors. The SQLAlchemy model mapping and CRUD functions must be fully type-hinted.

### 2. Unit Tests Pass
```bash
pytest tests/test_database.py
```
Must exit with code 0 and pass all tests. At least 4 distinct test cases should be covered, covering:
- Table creation
- Full game run and move logging lifecycle
- Retrieve operations (filtering, limits, sorting)
- Cascade deletion behavior

### 3. Database Schema Verification Script

To verify that the database creates tables, commits entries, and retrieves them correctly, run:

```bash
python -c "
from database import engine, SessionLocal
import models
import crud

# Create tables
models.Base.metadata.create_all(bind=engine)

# Open session
db = SessionLocal()
try:
    # Create GameRun
    run = crud.create_game_run(db, num_disks=4, solver_type='manual')
    assert run.id is not None
    assert run.num_disks == 4
    assert run.is_completed is False

    # Add Moves
    crud.add_game_move(db, game_run_id=run.id, move_number=1, from_peg=0, to_peg=1)
    crud.add_game_move(db, game_run_id=run.id, move_number=2, from_peg=0, to_peg=2)

    # Verify moves exist
    moves = crud.get_game_moves(db, run.id)
    assert len(moves) == 2
    assert moves[0].from_peg == 0 and moves[0].to_peg == 1
    assert moves[1].from_peg == 0 and moves[1].to_peg == 2

    # Complete GameRun
    completed_run = crud.complete_game_run(db, game_run_id=run.id, total_moves=2)
    assert completed_run is not None
    assert completed_run.is_completed is True
    assert completed_run.total_moves == 2

    # Clean up test records
    db.delete(completed_run)
    db.commit()
    print('Database Validation Succeeded!')
finally:
    db.close()
"
```
Must print `Database Validation Succeeded!` and execute without throwing exceptions.
