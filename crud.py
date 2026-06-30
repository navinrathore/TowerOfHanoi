from __future__ import annotations
from datetime import timezone, datetime
import json

from sqlalchemy import func, select
from typing import Optional

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
        start_time=datetime.now(timezone.utc),
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
        timestamp=datetime.now(timezone.utc),
    )
    db.add(db_move)
    db.commit()
    db.refresh(db_move)
    return db_move


def complete_game_run(
    db: Session, game_run_id: int, total_moves: int
) -> Optional[models.GameRun]:
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
        db_run.end_time = datetime.now(timezone.utc)
        db_run.total_moves = total_moves
        db_run.is_completed = True
        db.commit()
        db.refresh(db_run)
    return db_run


def get_game_run(db: Session, game_run_id: int) -> Optional[models.GameRun]:
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


def get_fastest_runs(db: Session, num_disks: int = 3, limit: int = 10) -> list[models.GameRun]:
    """Retrieve the fastest completed manual runs for a specific disk count.

    Sorted by duration in seconds, then total_moves.
    """
    stmt = (
        select(models.GameRun)
        .where(
            models.GameRun.solver_type == "manual",
            models.GameRun.is_completed == True,
            models.GameRun.num_disks == num_disks,
            models.GameRun.end_time.isnot(None),
        )
    )
    runs = list(db.scalars(stmt).all())
    runs.sort(
        key=lambda r: (
            (r.end_time - r.start_time).total_seconds() if r.end_time else float("inf"),
            r.total_moves,
        )
    )
    return runs[:limit]


def get_solver_comparison(db: Session) -> list[dict]:
    """Calculate aggregate statistics comparing solver types and disk counts."""
    stmt = (
        select(
            models.GameRun.solver_type,
            models.GameRun.num_disks,
            func.avg(models.GameRun.total_moves).label("avg_moves"),
            func.avg(models.GameRun.compute_time_ms).label("avg_compute_time"),
            func.count(models.GameRun.id).label("total_runs"),
        )
        .where(models.GameRun.is_completed == True)
        .group_by(models.GameRun.solver_type, models.GameRun.num_disks)
    )
    results = db.execute(stmt).all()
    return [
        {
            "solver_type": r.solver_type,
            "num_disks": r.num_disks,
            "avg_moves": float(r.avg_moves) if r.avg_moves else 0.0,
            "avg_compute_time": float(r.avg_compute_time) if r.avg_compute_time else 0.0,
            "total_runs": r.total_runs,
        }
        for r in results
    ]


def save_training_run(
    db: Session,
    num_disks: int,
    episodes: int,
    alpha: float,
    gamma: float,
    epsilon: float,
    training_time_ms: float,
    final_success_rate: float,
    metrics: dict,
    q_table: dict,
) -> models.QLearningTrainingRun:
    """Save a Q-learning training run and its serialized weights to the database."""
    # Convert tuple actions to stringified keys "from_peg->to_peg" for JSON
    q_table_serializable = {}
    for state_str, actions_dict in q_table.items():
        q_table_serializable[state_str] = {
            f"{from_peg}->{to_peg}": weight
            for (from_peg, to_peg), weight in actions_dict.items()
        }

    db_run = models.QLearningTrainingRun(
        num_disks=num_disks,
        episodes=episodes,
        alpha=alpha,
        gamma=gamma,
        epsilon=epsilon,
        training_time_ms=training_time_ms,
        final_success_rate=final_success_rate,
        metrics_json=json.dumps(metrics),
        q_table_json=json.dumps(q_table_serializable),
        timestamp=datetime.now(timezone.utc),
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def get_latest_training_run(db: Session, num_disks: int) -> Optional[models.QLearningTrainingRun]:
    """Retrieve the most recent Q-learning training run for a given disk count."""
    stmt = (
        select(models.QLearningTrainingRun)
        .where(models.QLearningTrainingRun.num_disks == num_disks)
        .order_by(models.QLearningTrainingRun.timestamp.desc())
        .limit(1)
    )
    return db.scalars(stmt).first()


def seed_database_if_empty(db: Session) -> None:
    """Populate the database with mock manual and solver runs if empty."""
    count = db.scalar(select(func.count(models.GameRun.id)))
    if count is not None and count > 0:
        return

    import random
    from datetime import timedelta

    now = datetime.now(timezone.utc)

    # 1. Manual completions
    # 3 Disks (Optimal: 7 moves)
    manual_3_disk_runs = [
        (7, 10.5, "Ada Lovelace"),  # optimal, fast
        (9, 15.2, "Alan Turing"),  # slightly sub-optimal
        (15, 30.1, "Grace Hopper"),  # very sub-optimal
    ]
    for total_moves, duration_sec, player_name in manual_3_disk_runs:
        start = now - timedelta(hours=2)
        end = start + timedelta(seconds=duration_sec)
        db_run = models.GameRun(
            num_disks=3,
            solver_type="manual",
            player_name=player_name,
            start_time=start,
            end_time=end,
            total_moves=total_moves,
            is_completed=True,
            compute_time_ms=0.0,
        )
        db.add(db_run)

    # 4 Disks (Optimal: 15 moves)
    manual_4_disk_runs = [
        (15, 35.8, "Margaret Hamilton"),
        (21, 62.4, "Donald Knuth"),
    ]
    for total_moves, duration_sec, player_name in manual_4_disk_runs:
        start = now - timedelta(hours=1)
        end = start + timedelta(seconds=duration_sec)
        db_run = models.GameRun(
            num_disks=4,
            solver_type="manual",
            player_name=player_name,
            start_time=start,
            end_time=end,
            total_moves=total_moves,
            is_completed=True,
            compute_time_ms=0.0,
        )
        db.add(db_run)

    # 5 Disks (Optimal: 31 moves)
    manual_5_disk_runs = [
        (31, 85.0, "Claude Shannon"),
        (45, 142.0, "Grace Hopper"),
    ]
    for total_moves, duration_sec, player_name in manual_5_disk_runs:
        start = now - timedelta(minutes=30)
        end = start + timedelta(seconds=duration_sec)
        db_run = models.GameRun(
            num_disks=5,
            solver_type="manual",
            player_name=player_name,
            start_time=start,
            end_time=end,
            total_moves=total_moves,
            is_completed=True,
            compute_time_ms=0.0,
        )
        db.add(db_run)

    # 2. Solver runs
    solvers = ["recursive", "iterative", "search"]
    for num_disks in [3, 4, 5]:
        optimal = (1 << num_disks) - 1
        for solver in solvers:
            start = now - timedelta(hours=3)
            end = start + timedelta(seconds=num_disks * 1.5)  # simulated visualization playback
            db_run = models.GameRun(
                num_disks=num_disks,
                solver_type=solver,
                start_time=start,
                end_time=end,
                total_moves=optimal,
                is_completed=True,
                compute_time_ms=float(num_disks) * 0.12 + random.uniform(0.01, 0.05),
            )
            db.add(db_run)

    db.commit()
