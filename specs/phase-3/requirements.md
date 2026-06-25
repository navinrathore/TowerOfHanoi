# Phase 3 Requirements — SQLite Database & SQLAlchemy Schemas

## Scope

Define and implement the persistence layer for the Tower of Hanoi application. This includes configuring SQLite database connectivity using SQLAlchemy, defining database models, and implementing CRUD functions to log and query game runs and their individual moves.

1. **Database Setup**:
   - SQLite database connection defined in `database.py`.
   - SQLite database file named `hanoi.db` stored in the project root.
   - Declarative base `Base` and `SessionLocal` class configured for dependency injection.
   - A thread-safe, auto-closing session helper / dependency generator `get_db()`.

2. **SQLAlchemy Models (`models.py`)**:
   - `GameRun` model:
     - `id`: Integer primary key.
     - `num_disks`: Integer representing the number of disks (must be between 3 and 8 inclusive).
     - `solver_type`: String representing who/what played the game (e.g., `"manual"`, `"recursive"`, `"iterative"`, `"search"`, `"qlearning"`).
     - `start_time`: DateTime representing when the game run started. Defaults to current UTC time.
     - `end_time`: DateTime representing when the game run ended (nullable, set when completed).
     - `total_moves`: Integer count of moves made. Defaults to 0.
     - `is_completed`: Boolean flag indicating if the game was completed. Defaults to False.
     - `moves`: One-to-many relationship with `GameMove` (with cascade delete).
   - `GameMove` model:
     - `id`: Integer primary key.
     - `game_run_id`: Integer foreign key referencing `GameRun.id` (nullable=False).
     - `move_number`: Integer tracking the step index of the move (1-indexed).
     - `from_peg`: Integer rod index (0, 1, or 2).
     - `to_peg`: Integer rod index (0, 1, or 2).
     - `timestamp`: DateTime representing when the individual move was made. Defaults to current UTC time.

3. **CRUD Operations (`crud.py`)**:
   - `create_game_run(db: Session, num_disks: int, solver_type: str) -> models.GameRun`:
     - Creates and persists a new `GameRun` entry in the database.
   - `add_game_move(db: Session, game_run_id: int, move_number: int, from_peg: int, to_peg: int) -> models.GameMove`:
     - Creates and persists a new `GameMove` entry, associated with the specified `game_run_id`.
   - `complete_game_run(db: Session, game_run_id: int, total_moves: int) -> models.GameRun | None`:
     - Updates a `GameRun` entry, setting `end_time` to current UTC time, updating `total_moves`, and marking `is_completed` as True.
   - `get_game_run(db: Session, game_run_id: int) -> models.GameRun | None`:
     - Fetches a single game run by its ID.
   - `get_all_game_runs(db: Session, limit: int = 100) -> list[models.GameRun]`:
     - Retrieves all game runs up to `limit` sorted by `start_time` descending.
   - `get_game_moves(db: Session, game_run_id: int) -> list[models.GameMove]`:
     - Retrieves all moves associated with a game run, sorted by `move_number`.

4. **Testing**:
   - Set up test database fixtures in `tests/test_database.py` using an in-memory SQLite database (`sqlite:///:memory:`).
   - Test tables creation and tear down.
   - Test CRUD helper functions: starting a run, adding moves, completing a run, retrieving runs, and cascading deletion.

## Out of Scope

- No FastAPI HTTP routers or schemas (Pydantic models) mapped to endpoints (Phase 4).
- No Jinja2 template integration or interactive frontend controls (Phase 4).
- No algorithmic solvers generating moves to write to the DB (Phase 5/6/7).

## Design Decisions

### SQLite & SQLAlchemy Choice
- SQLite is embedded and requires no server installation, which perfectly matches our requirement for a lightweight local platform.
- Using standard SQLAlchemy (v2.0+) Declarative Base allows us to write modern type-annotated models (e.g. `Mapped[int] = mapped_column(primary_key=True)`), ensuring type safety with Mypy.

### In-Memory Testing
- To avoid cluttering the workspace and leaking state between test runs, tests must run against an in-memory database instance.

## Context

Phase 3 establishes the data schema and persistence layer. The outputs of this phase are critical because future phases (manual gameplay and automated solvers) will query/save statistics and history to these schemas.

## Stakeholder Notes

- **Mary** wants SQLAlchemy type declarations to be fully compliant with PEP 484 via SQLAlchemy's newer Mapped types, so `mypy` strict type checking continues to pass with 0 errors.
- **Steve** requested that `solver_type` be a flexible string to allow new experimental solvers to be added without modifying the database schema later.
