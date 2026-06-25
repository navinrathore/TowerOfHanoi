from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

import crud
import models
from database import Base, engine, get_db

# Create the SQLite database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyTowerOfHanoi")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# --- Pydantic Schemas ---


class MoveSchema(BaseModel):
    """Schema for individual moves in a batch upload."""

    from_peg: int = Field(..., ge=0, le=2, description="Source peg index (0, 1, or 2).")
    to_peg: int = Field(
        ..., ge=0, le=2, description="Destination peg index (0, 1, or 2)."
    )


class GameRunBatchCreate(BaseModel):
    """Schema for batch logging a completed game run with moves."""

    num_disks: int = Field(
        ..., ge=3, le=8, description="Number of disks (3 to 8 inclusive)."
    )
    solver_type: str = Field(
        ..., max_length=50, description="Solver type (e.g. 'manual')."
    )
    start_time: datetime = Field(..., description="Timestamp of game start.")
    end_time: datetime = Field(..., description="Timestamp of game completion.")
    total_moves: int = Field(
        ..., ge=0, description="Total number of moves made in the session."
    )
    moves: list[MoveSchema] = Field(
        ..., description="Chronological list of disk moves."
    )


class GameMoveResponse(BaseModel):
    """Response schema for a single game move."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    game_run_id: int
    move_number: int
    from_peg: int
    to_peg: int
    timestamp: datetime


class GameRunResponse(BaseModel):
    """Response schema for a completed game run, including its moves."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    num_disks: int
    solver_type: str
    start_time: datetime
    end_time: datetime | None
    total_moves: int
    is_completed: bool
    moves: list[GameMoveResponse] = []


# --- Routes ---


@app.get("/", response_class=HTMLResponse)
async def read_dashboard(
    request: Request,
    db: Session = Depends(get_db),  # noqa: B008
) -> HTMLResponse:
    """Render the game dashboard, pre-populated with recent runs."""
    runs = crud.get_all_game_runs(db, limit=10)
    return templates.TemplateResponse(request, "index.html", {"runs": runs})


@app.post("/api/runs", response_model=GameRunResponse, status_code=201)
async def create_completed_run(
    payload: GameRunBatchCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> models.GameRun:
    """Log a completed game run and its moves in a database transaction."""
    try:
        # Create GameRun entry
        db_run = models.GameRun(
            num_disks=payload.num_disks,
            solver_type=payload.solver_type,
            start_time=payload.start_time,
            end_time=payload.end_time,
            total_moves=payload.total_moves,
            is_completed=True,
        )
        db.add(db_run)
        db.flush()  # Generate db_run.id

        # Insert moves
        for idx, move in enumerate(payload.moves):
            db_move = models.GameMove(
                game_run_id=db_run.id,
                move_number=idx + 1,
                from_peg=move.from_peg,
                to_peg=move.to_peg,
            )
            db.add(db_move)

        db.commit()
        db.refresh(db_run)
        return db_run
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Failed to save game run: {e!s}"
        ) from e


@app.get("/api/runs", response_model=list[GameRunResponse])
async def read_recent_runs(
    limit: int = 10,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[models.GameRun]:
    """Retrieve the recent game runs, sorted by start time descending."""
    return crud.get_all_game_runs(db, limit=limit)
