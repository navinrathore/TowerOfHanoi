from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

import crud
import models
from database import Base


@pytest.fixture(name="db")
def fixture_db() -> Generator[Session, None, None]:
    """Fixture to provide a clean, isolated in-memory database session."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_game_run(db: Session) -> None:
    """Verify that create_game_run persists a GameRun correctly."""
    # Test valid creation
    run = crud.create_game_run(db, num_disks=3, solver_type="manual")
    assert run.id is not None
    assert run.num_disks == 3
    assert run.solver_type == "manual"
    assert run.is_completed is False
    assert run.total_moves == 0
    assert run.start_time is not None
    assert run.end_time is None

    # Verify retrieval
    retrieved = crud.get_game_run(db, run.id)
    assert retrieved is not None
    assert retrieved.id == run.id

    # Test parameter bounds validation
    with pytest.raises(ValueError, match="must be between 3 and 8"):
        crud.create_game_run(db, num_disks=2, solver_type="manual")
    with pytest.raises(ValueError, match="must be between 3 and 8"):
        crud.create_game_run(db, num_disks=9, solver_type="manual")


def test_add_game_move(db: Session) -> None:
    """Verify that add_game_move logs moves correctly and enforces peg bounds."""
    run = crud.create_game_run(db, num_disks=3, solver_type="manual")
    move = crud.add_game_move(
        db, game_run_id=run.id, move_number=1, from_peg=0, to_peg=2
    )

    assert move.id is not None
    assert move.game_run_id == run.id
    assert move.move_number == 1
    assert move.from_peg == 0
    assert move.to_peg == 2
    assert move.timestamp is not None

    # Check database retrieval
    retrieved_moves = crud.get_game_moves(db, run.id)
    assert len(retrieved_moves) == 1
    assert retrieved_moves[0].id == move.id

    # Test error handling for invalid pegs
    with pytest.raises(ValueError, match="Invalid peg selection"):
        crud.add_game_move(db, game_run_id=run.id, move_number=2, from_peg=-1, to_peg=0)
    with pytest.raises(ValueError, match="Invalid peg selection"):
        crud.add_game_move(db, game_run_id=run.id, move_number=2, from_peg=0, to_peg=3)
    with pytest.raises(ValueError, match="positive integer"):
        crud.add_game_move(db, game_run_id=run.id, move_number=0, from_peg=0, to_peg=1)


def test_complete_game_run(db: Session) -> None:
    """Verify that completing a game run updates its duration and completion flag."""
    run = crud.create_game_run(db, num_disks=3, solver_type="manual")
    assert run.end_time is None

    completed_run = crud.complete_game_run(db, game_run_id=run.id, total_moves=7)
    assert completed_run is not None
    assert completed_run.id == run.id
    assert completed_run.is_completed is True
    assert completed_run.total_moves == 7
    assert completed_run.end_time is not None

    # Test non-existent run completion
    non_existent = crud.complete_game_run(db, game_run_id=999, total_moves=5)
    assert non_existent is None


def test_cascade_delete(db: Session) -> None:
    """Verify that deleting a GameRun cascades and deletes all associated GameMoves."""
    run = crud.create_game_run(db, num_disks=3, solver_type="manual")
    crud.add_game_move(db, game_run_id=run.id, move_number=1, from_peg=0, to_peg=2)
    crud.add_game_move(db, game_run_id=run.id, move_number=2, from_peg=0, to_peg=1)

    moves = crud.get_game_moves(db, run.id)
    assert len(moves) == 2

    # Delete run and verify moves are cascaded
    db.delete(run)
    db.commit()

    # Query moves directly to ensure they were cascadingly deleted
    stmt = select(models.GameMove).where(models.GameMove.game_run_id == run.id)
    db_moves = db.scalars(stmt).all()
    assert len(db_moves) == 0


def test_get_all_game_runs_sorting_and_limiting(db: Session) -> None:
    """Verify sorting and limit logic when fetching all game runs."""
    # Create multiple game runs
    run1 = crud.create_game_run(db, num_disks=3, solver_type="manual")
    run2 = crud.create_game_run(db, num_disks=4, solver_type="recursive")
    run3 = crud.create_game_run(db, num_disks=5, solver_type="iterative")

    # Fetch with limit
    runs = crud.get_all_game_runs(db, limit=2)
    assert len(runs) == 2
    # First retrieved should be the most recently created (run3)
    assert runs[0].id == run3.id
    assert runs[1].id == run2.id

    # Fetch all
    all_runs = crud.get_all_game_runs(db)
    assert len(all_runs) == 3
    assert all_runs[2].id == run1.id
