from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

import models


def create_game_run(db: Session, num_disks: int, solver_type: str) -> models.GameRun:
    """Create a new game run in the database.

    Args:
        db: SQLAlchemy database session.
        num_disks: Number of disks used (3 to 8).
        solver_type: The type of solver (e.g. 'manual', 'recursive', etc.).

    Returns:
        The created GameRun object.

    Raises:
        ValueError: If num_disks is not within range.
    """
    if not (3 <= num_disks <= 8):
        raise ValueError("Number of disks must be between 3 and 8 inclusive.")

    db_run = models.GameRun(
        num_disks=num_disks,
        solver_type=solver_type,
        start_time=datetime.now(UTC),
        total_moves=0,
        is_completed=False,
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def add_game_move(
    db: Session,
    game_run_id: int,
    move_number: int,
    from_peg: int,
    to_peg: int,
) -> models.GameMove:
    """Log an individual move within a game run.

    Args:
        db: SQLAlchemy database session.
        game_run_id: The ID of the game run.
        move_number: The sequential move number.
        from_peg: Source peg index (0, 1, or 2).
        to_peg: Destination peg index (0, 1, or 2).

    Returns:
        The created GameMove object.

    Raises:
        ValueError: If move_number or peg indices are invalid.
    """
    if from_peg not in (0, 1, 2) or to_peg not in (0, 1, 2):
        raise ValueError(
            f"Invalid peg selection: from_peg={from_peg}, to_peg={to_peg}. "
            "Pegs must be 0, 1, or 2."
        )
    if move_number <= 0:
        raise ValueError("Move number must be a positive integer.")

    db_move = models.GameMove(
        game_run_id=game_run_id,
        move_number=move_number,
        from_peg=from_peg,
        to_peg=to_peg,
        timestamp=datetime.now(UTC),
    )
    db.add(db_move)
    db.commit()
    db.refresh(db_move)
    return db_move


def complete_game_run(
    db: Session, game_run_id: int, total_moves: int
) -> models.GameRun | None:
    """Mark a game run as completed, updating end time and total moves.

    Args:
        db: SQLAlchemy database session.
        game_run_id: The ID of the game run.
        total_moves: The total count of moves.

    Returns:
        The updated GameRun object, or None if not found.
    """
    db_run = db.get(models.GameRun, game_run_id)
    if db_run:
        db_run.end_time = datetime.now(UTC)
        db_run.total_moves = total_moves
        db_run.is_completed = True
        db.commit()
        db.refresh(db_run)
    return db_run


def get_game_run(db: Session, game_run_id: int) -> models.GameRun | None:
    """Retrieve a single game run by its ID.

    Args:
        db: SQLAlchemy database session.
        game_run_id: The ID of the game run.

    Returns:
        The GameRun object, or None if not found.
    """
    return db.get(models.GameRun, game_run_id)


def get_all_game_runs(db: Session, limit: int = 100) -> list[models.GameRun]:
    """Retrieve all game runs, sorted by start time descending.

    Args:
        db: SQLAlchemy database session.
        limit: Maximum number of runs to return.

    Returns:
        A list of GameRun objects.
    """
    stmt = (
        select(models.GameRun).order_by(models.GameRun.start_time.desc()).limit(limit)
    )
    return list(db.scalars(stmt).all())


def get_game_moves(db: Session, game_run_id: int) -> list[models.GameMove]:
    """Retrieve all moves logged for a given game run, sorted by move number.

    Args:
        db: SQLAlchemy database session.
        game_run_id: The ID of the game run.

    Returns:
        A list of GameMove objects.
    """
    stmt = (
        select(models.GameMove)
        .where(models.GameMove.game_run_id == game_run_id)
        .order_by(models.GameMove.move_number.asc())
    )
    return list(db.scalars(stmt).all())
