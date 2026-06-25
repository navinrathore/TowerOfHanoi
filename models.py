from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class GameRun(Base):
    """Represents a single play/run of a Tower of Hanoi game."""

    __tablename__ = "game_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    num_disks: Mapped[int] = mapped_column(Integer, nullable=False)
    solver_type: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    total_moves: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # One-to-many relationship with GameMove with cascade delete
    moves: Mapped[list["GameMove"]] = relationship(
        "GameMove", back_populates="game_run", cascade="all, delete-orphan"
    )


class GameMove(Base):
    """Represents an individual disk movement step within a game run."""

    __tablename__ = "game_moves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_run_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("game_runs.id"), nullable=False
    )
    move_number: Mapped[int] = mapped_column(Integer, nullable=False)
    from_peg: Mapped[int] = mapped_column(Integer, nullable=False)
    to_peg: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    # Many-to-one relationship back to the GameRun
    game_run: Mapped["GameRun"] = relationship("GameRun", back_populates="moves")
