from collections.abc import Generator
from datetime import UTC, datetime, timedelta
import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import crud
import models
from database import Base, get_db
from main import app

# Configure isolated test database with StaticPool
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db_session")
def fixture_db_session() -> Generator[Session, None, None]:
    """Provide an isolated database session for each test run."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def fixture_client(db_session: Session) -> Generator[TestClient, None, None]:
    """Test client with database session overrides."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_seed_database_if_empty(db_session: Session) -> None:
    """Verify that seed_database_if_empty seeds when empty and does not when not empty."""
    # Assert database is empty initially
    assert len(crud.get_all_game_runs(db_session)) == 0

    # Run seed
    crud.seed_database_if_empty(db_session)
    runs_after_seed = crud.get_all_game_runs(db_session)
    assert len(runs_after_seed) > 0

    # Ensure seeding again does not add more runs
    total_runs_before = len(runs_after_seed)
    crud.seed_database_if_empty(db_session)
    assert len(crud.get_all_game_runs(db_session)) == total_runs_before


def test_get_fastest_runs(db_session: Session) -> None:
    """Verify that get_fastest_runs correctly filters and sorts manual completions."""
    # Seed custom runs
    now = datetime.now(UTC)
    run1 = models.GameRun(
        num_disks=3,
        solver_type="manual",
        start_time=now,
        end_time=now + timedelta(seconds=20),
        total_moves=10,
        is_completed=True,
    )
    run2 = models.GameRun(
        num_disks=3,
        solver_type="manual",
        start_time=now,
        end_time=now + timedelta(seconds=10),
        total_moves=7,
        is_completed=True,
    )
    run3 = models.GameRun(
        num_disks=3,
        solver_type="recursive",  # not manual
        start_time=now,
        end_time=now + timedelta(seconds=5),
        total_moves=7,
        is_completed=True,
    )
    db_session.add_all([run1, run2, run3])
    db_session.commit()

    fastest = crud.get_fastest_runs(db_session, num_disks=3, limit=5)
    assert len(fastest) == 2
    # run2 is faster (10 seconds vs 20 seconds)
    assert fastest[0].id == run2.id
    assert fastest[1].id == run1.id


def test_get_solver_comparison(db_session: Session) -> None:
    """Verify that get_solver_comparison groups and averages runs correctly."""
    now = datetime.now(UTC)
    r1 = models.GameRun(
        num_disks=3,
        solver_type="recursive",
        start_time=now,
        end_time=now + timedelta(seconds=5),
        total_moves=7,
        is_completed=True,
        compute_time_ms=1.2,
    )
    r2 = models.GameRun(
        num_disks=3,
        solver_type="recursive",
        start_time=now,
        end_time=now + timedelta(seconds=5),
        total_moves=9,
        is_completed=True,
        compute_time_ms=1.8,
    )
    db_session.add_all([r1, r2])
    db_session.commit()

    comp = crud.get_solver_comparison(db_session)
    assert len(comp) == 1
    assert comp[0]["solver_type"] == "recursive"
    assert comp[0]["num_disks"] == 3
    assert comp[0]["avg_moves"] == 8.0
    assert comp[0]["avg_compute_time"] == 1.5
    assert comp[0]["total_runs"] == 2


def test_save_and_get_qlearning_run(db_session: Session) -> None:
    """Verify Q-learning run serialization, saving, and retrieval."""
    metrics = {
        "episodes": [0, 10],
        "avg_rewards": [-100.0, -10.0],
        "avg_steps": [50.0, 7.0],
        "success_rates": [0.0, 1.0],
        "epsilons": [0.2, 0.1],
    }
    q_table = {
        "000": {(0, 1): 0.5, (0, 2): -1.0},
        "001": {(1, 2): 2.0},
    }

    saved = crud.save_training_run(
        db_session,
        num_disks=3,
        episodes=10,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.2,
        training_time_ms=45.5,
        final_success_rate=0.8,
        metrics=metrics,
        q_table=q_table,
    )
    assert saved.id is not None
    assert saved.num_disks == 3
    assert saved.episodes == 10

    loaded = crud.get_latest_training_run(db_session, num_disks=3)
    assert loaded is not None
    assert loaded.id == saved.id
    assert json.loads(loaded.metrics_json) == metrics

    # Verify action key conversion
    q_table_loaded = json.loads(loaded.q_table_json)
    assert "000" in q_table_loaded
    assert q_table_loaded["000"]["0->1"] == 0.5
    assert q_table_loaded["000"]["0->2"] == -1.0


def test_dashboard_route(client: TestClient) -> None:
    """Verify that GET /dashboard renders HTML page correctly."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Analytics" in response.text
    assert "Manual Leaderboard" in response.text
    assert "Solver Efficiency Comparison" in response.text


def test_qlearning_last_training_endpoint(client: TestClient, db_session: Session) -> None:
    """Verify that GET /api/solve/qlearning/last-training returns correct data or 404."""
    # Expect 404 when no runs exist
    response_404 = client.get("/api/solve/qlearning/last-training?num_disks=4")
    assert response_404.status_code == 404

    # Seed a training run
    metrics = {
        "episodes": [0, 1],
        "avg_rewards": [-10.0],
        "avg_steps": [7.0],
        "success_rates": [1.0],
        "epsilons": [0.1],
    }
    crud.save_training_run(
        db_session,
        num_disks=4,
        episodes=500,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.2,
        training_time_ms=10.0,
        final_success_rate=1.0,
        metrics=metrics,
        q_table={},
    )

    response = client.get("/api/solve/qlearning/last-training?num_disks=4")
    assert response.status_code == 200
    data = response.json()
    assert data["num_disks"] == 4
    assert data["episodes"] == 500
    assert data["metrics"] == metrics


def test_solvers_compute_time(client: TestClient) -> None:
    """Verify that solver endpoints measure and return compute_time_ms."""
    endpoints = [
        "/api/solve/recursive?num_disks=3",
        "/api/solve/iterative?num_disks=3",
        "/api/solve/search?num_disks=3",
        "/api/solve/qlearning?num_disks=3",
    ]
    for url in endpoints:
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert "compute_time_ms" in data
        assert isinstance(data["compute_time_ms"], float)
        assert data["compute_time_ms"] >= 0.0
