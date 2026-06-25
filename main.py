from datetime import datetime
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

import crud
import models
from database import Base, engine, get_db
from solvers.classic import solve_iterative, solve_recursive
from solvers.qlearning import QLearningAgent
from solvers.search import solve_search

# In-memory store for trained Q-learning agents
TRAINED_Q_TABLES: dict[int, QLearningAgent] = {}

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


class SolverMoveResponse(BaseModel):
    """Schema for individual moves in a solver response."""

    from_peg: int = Field(..., ge=0, le=2, description="Source peg index (0, 1, or 2).")
    to_peg: int = Field(
        ..., ge=0, le=2, description="Destination peg index (0, 1, or 2)."
    )


class SolverSolutionResponse(BaseModel):
    """Response schema for a generated game solution."""

    solver_type: str = Field(..., description="The type of solver used.")
    num_disks: int = Field(..., ge=3, le=8, description="Number of disks.")
    moves: list[SolverMoveResponse] = Field(
        ..., description="Chronological list of solution moves."
    )


class QLearningTrainRequest(BaseModel):
    """Schema for requesting a Q-learning agent training session."""

    num_disks: int = Field(
        ..., ge=3, le=8, description="Number of disks (3 to 8 inclusive)."
    )
    episodes: int = Field(
        1000, ge=100, le=10000, description="Number of training episodes."
    )
    alpha: float = Field(0.1, ge=0.01, le=1.0, description="Learning rate (alpha).")
    gamma: float = Field(0.9, ge=0.0, le=1.0, description="Discount factor (gamma).")
    epsilon: float = Field(
        0.2, ge=0.0, le=1.0, description="Initial exploration rate (epsilon)."
    )


class QLearningMetrics(BaseModel):
    """Binned training metrics for visualization."""

    episodes: list[int] = Field(..., description="Episode indices.")
    avg_rewards: list[float] = Field(
        ..., description="Binned average reward per episode."
    )
    avg_steps: list[float] = Field(
        ..., description="Binned average steps to completion."
    )
    success_rates: list[float] = Field(
        ..., description="Binned goal-completion success rates."
    )
    epsilons: list[float] = Field(..., description="Binned exploration rates.")


class QLearningTrainResponse(BaseModel):
    """Response schema returned after Q-agent training completes."""

    num_disks: int
    episodes: int
    training_time_ms: float
    final_success_rate: float
    metrics: QLearningMetrics


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


@app.get("/api/solve/recursive", response_model=SolverSolutionResponse)
async def get_solve_recursive(
    num_disks: int = Query(
        ..., ge=3, le=8, description="Number of disks (3 to 8 inclusive)."
    ),
) -> dict[str, Any]:
    """Compute step-by-step solution using the recursive solver."""
    moves = solve_recursive(num_disks)
    return {
        "solver_type": "recursive",
        "num_disks": num_disks,
        "moves": moves,
    }


@app.get("/api/solve/iterative", response_model=SolverSolutionResponse)
async def get_solve_iterative(
    num_disks: int = Query(
        ..., ge=3, le=8, description="Number of disks (3 to 8 inclusive)."
    ),
) -> dict[str, Any]:
    """Compute step-by-step solution using the iterative solver."""
    moves = solve_iterative(num_disks)
    return {
        "solver_type": "iterative",
        "num_disks": num_disks,
        "moves": moves,
    }


@app.get("/api/solve/search", response_model=SolverSolutionResponse)
async def get_solve_search(
    num_disks: int = Query(
        ..., ge=3, le=8, description="Number of disks (3 to 8 inclusive)."
    ),
    state: str | None = Query(
        None,
        description="Optional current state encoded as JSON (e.g. [[3,2,1],[],[]])",
    ),
) -> dict[str, Any]:
    """Compute step-by-step solution using the A* search solver."""
    start_state = None
    if state:
        import json

        try:
            parsed = json.loads(state)
            if not isinstance(parsed, list) or len(parsed) != 3:
                raise ValueError("State must be a list of 3 pegs.")
            # Convert list of lists to tuple of tuples
            start_state = tuple(tuple(int(x) for x in peg) for peg in parsed)

            # Validate start state disk count matches num_disks
            total_disks = sum(len(peg) for peg in start_state)
            if total_disks != num_disks:
                raise ValueError(
                    f"Disk count {total_disks} does not match {num_disks}."
                )

            # Validate that disks on each peg are in ascending order
            for peg in start_state:
                for i in range(len(peg) - 1):
                    if peg[i] < peg[i + 1]:
                        raise ValueError("Larger disk placed on top of smaller disk.")
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid state parameter: {e!s}"
            ) from e

    moves = solve_search(num_disks, start_state=start_state)
    return {
        "solver_type": "search",
        "num_disks": num_disks,
        "moves": moves,
    }


@app.post("/api/solve/qlearning/train", response_model=QLearningTrainResponse)
async def post_train_qlearning(payload: QLearningTrainRequest) -> dict[str, Any]:
    """Train a tabular Q-learning agent with the specified parameters."""
    agent = QLearningAgent(payload.num_disks)
    results = agent.train(
        episodes=payload.episodes,
        alpha=payload.alpha,
        gamma=payload.gamma,
        epsilon=payload.epsilon,
    )
    TRAINED_Q_TABLES[payload.num_disks] = agent
    return results


@app.get("/api/solve/qlearning", response_model=SolverSolutionResponse)
async def get_solve_qlearning(
    num_disks: int = Query(
        ..., ge=3, le=8, description="Number of disks (3 to 8 inclusive)."
    ),
    state: str | None = Query(
        None,
        description="Optional current state encoded as JSON (e.g. [[3,2,1],[],[]])",
    ),
) -> dict[str, Any]:
    """Compute step-by-step solution using the Q-learning solver (trained agent)."""
    agent = TRAINED_Q_TABLES.get(num_disks)
    if not agent:
        # Train default agent on the fly if not already trained
        agent = QLearningAgent(num_disks)
        agent.train(episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.2)
        TRAINED_Q_TABLES[num_disks] = agent

    start_state_str = "0" * num_disks
    if state:
        import json

        try:
            parsed = json.loads(state)
            if not isinstance(parsed, list) or len(parsed) != 3:
                raise ValueError("State must be a list of 3 pegs.")
            # Convert list of lists to pegs structure
            start_pegs = [[int(x) for x in peg] for peg in parsed]

            # Validate start state disk count
            total_disks = sum(len(peg) for peg in start_pegs)
            if total_disks != num_disks:
                raise ValueError(
                    f"Disk count {total_disks} does not match {num_disks}."
                )

            # Validate order
            for peg in start_pegs:
                for i in range(len(peg) - 1):
                    if peg[i] < peg[i + 1]:
                        raise ValueError("Larger disk placed on top of smaller disk.")

            # Convert pegs to state string representation
            from solvers.qlearning import state_to_string

            start_state_str = state_to_string(start_pegs, num_disks)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid state parameter: {e!s}"
            ) from e

    moves = agent.solve(start_state_str)
    return {
        "solver_type": "qlearning",
        "num_disks": num_disks,
        "moves": moves,
    }
