# Phase 3 Plan — SQLite Database & SQLAlchemy Schemas

This document outlines the step-by-step implementation plan for setting up the SQLite database and SQLAlchemy schemas.

---

## Group 1 — Dependency Setup

1. Add `sqlalchemy` to `requirements.txt`:
   ```text
   sqlalchemy==2.0.31
   ```
2. Install new dependencies in the virtual environment.

## Group 2 — Database Configuration

3. Create `database.py` in the root directory.
4. Implement standard SQLAlchemy setup in `database.py`:
   - Connection URL: `sqlite:///hanoi.db`.
   - Create engine with `connect_args={"check_same_thread": False}` (required for SQLite to work with FastAPI).
   - Create `SessionLocal` class using `sessionmaker(autocommit=False, autoflush=False, bind=engine)`.
   - Define a `Base` class using `declarative_base()` (or subclassing `DeclarativeBase`).
   - Implement a generator helper for FastAPI routes:
     ```python
     def get_db():
         db = SessionLocal()
         try:
             yield db
         finally:
             db.close()
     ```

## Group 3 — SQLAlchemy Models

5. Create `models.py` in the root directory.
6. Implement the `GameRun` model class inheriting from `Base`:
   - `__tablename__ = "game_runs"`
   - `id`: `Mapped[int]` primary key.
   - `num_disks`: `Mapped[int]` field, nullable=False.
   - `solver_type`: `Mapped[str]` field, nullable=False (e.g. `'manual'`, `'recursive'`, etc.).
   - `start_time`: `Mapped[datetime]` field, nullable=False, default to UTC.
   - `end_time`: `Mapped[datetime | None]` field, nullable=True.
   - `total_moves`: `Mapped[int]` field, nullable=False, default=0.
   - `is_completed`: `Mapped[bool]` field, nullable=False, default=False.
   - `moves`: `Mapped[list["GameMove"]]` relationship referencing `GameMove` with cascade delete.
7. Implement the `GameMove` model class inheriting from `Base`:
   - `__tablename__ = "game_moves"`
   - `id`: `Mapped[int]` primary key.
   - `game_run_id`: `Mapped[int]` foreign key pointing to `game_runs.id`, nullable=False.
   - `move_number`: `Mapped[int]` field, nullable=False (tracks which move number this is).
   - `from_peg`: `Mapped[int]` field, nullable=False.
   - `to_peg`: `Mapped[int]` field, nullable=False.
   - `timestamp`: `Mapped[datetime]` field, nullable=False, default to UTC.
   - `game_run`: `Mapped["GameRun"]` relationship back to `GameRun`.

## Group 4 — CRUD Utilities

8. Create `crud.py` in the root directory.
9. Implement CRUD helper functions:
   - `create_game_run(db: Session, num_disks: int, solver_type: str) -> models.GameRun`:
     - Create model, add to `db`, commit, refresh, return.
   - `add_game_move(db: Session, game_run_id: int, move_number: int, from_peg: int, to_peg: int) -> models.GameMove`:
     - Validate `from_peg` and `to_peg` are in `(0, 1, 2)`.
     - Create model, add to `db`, commit, refresh, return.
   - `complete_game_run(db: Session, game_run_id: int, total_moves: int) -> models.GameRun | None`:
     - Find run by ID. Update `end_time` to UTC now, set `total_moves`, set `is_completed` to `True`. Commit, refresh, return.
   - `get_game_run(db: Session, game_run_id: int) -> models.GameRun | None`:
     - Query `GameRun` by primary key.
   - `get_all_game_runs(db: Session, limit: int = 100) -> list[models.GameRun]`:
     - Query all `GameRun` sorted by `start_time` descending, limited by `limit`.
   - `get_game_moves(db: Session, game_run_id: int) -> list[models.GameMove]`:
     - Query all moves for a game run, sorted by `move_number` ascending.

## Group 5 — Database Hook in FastAPI

10. In `main.py`, add startup table creation:
    ```python
    import models
    from database import engine
    models.Base.metadata.create_all(bind=engine)
    ```
    This ensures that when the app starts, the SQLite tables are automatically created if they don't already exist.

## Group 6 — Testing Setup & Implementation

11. Create a test file `tests/test_database.py`.
12. Configure in-memory SQLite engine and session for pytest:
    - Create a session fixture with clean tables before/after each test.
13. Write tests:
    - `test_db_creation`: Verify tables can be created on the in-memory engine.
    - `test_crud_game_run_lifecycle`: Start a game, verify DB state, add some moves, query moves, complete game run, verify values are saved.
    - `test_cascade_delete`: Verify that deleting a `GameRun` cascades and deletes all associated `GameMove` rows.
    - `test_query_limits_and_sorting`: Write multiple game runs and verify `get_all_game_runs` returns them sorted descending and limits correctly.

## Group 7 — Validation

14. Lint check: run `ruff check .`
15. Format check: run `ruff format --check .`
16. Type check: run `mypy .`
17. Run tests: run `pytest`
