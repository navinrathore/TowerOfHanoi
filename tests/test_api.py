from collections.abc import Generator
from datetime import timezone, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

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


def test_read_dashboard(client: TestClient) -> None:
    """Verify that GET / returns the dashboard HTML page successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Antigravity Hanoi" in response.text
    assert "Disks" in response.text


def test_create_completed_run_batch(client: TestClient, db_session: Session) -> None:
    """Verify that a completed game run with moves can be successfully batch logged."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(seconds=12)

    payload = {
        "num_disks": 3,
        "solver_type": "manual",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_moves": 7,
        "moves": [
            {"from_peg": 0, "to_peg": 2},
            {"from_peg": 0, "to_peg": 1},
            {"from_peg": 2, "to_peg": 1},
            {"from_peg": 0, "to_peg": 2},
            {"from_peg": 1, "to_peg": 0},
            {"from_peg": 1, "to_peg": 2},
            {"from_peg": 0, "to_peg": 2},
        ],
    }

    response = client.post("/api/runs", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["num_disks"] == 3
    assert data["solver_type"] == "manual"
    assert data["total_moves"] == 7
    assert data["is_completed"] is True
    assert len(data["moves"]) == 7
    assert data["moves"][0]["from_peg"] == 0
    assert data["moves"][0]["to_peg"] == 2
    assert data["moves"][6]["from_peg"] == 0
    assert data["moves"][6]["to_peg"] == 2


def test_create_run_validation_errors(client: TestClient) -> None:
    """Verify that API validates payload constraints (disk count, peg index bounds)."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(seconds=5)

    # Disk count out of range (lower bound 3)
    payload_too_few = {
        "num_disks": 2,
        "solver_type": "manual",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_moves": 3,
        "moves": [{"from_peg": 0, "to_peg": 2}],
    }
    response = client.post("/api/runs", json=payload_too_few)
    assert response.status_code == 422

    # Disk count out of range (upper bound 8)
    payload_too_many = {
        "num_disks": 9,
        "solver_type": "manual",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_moves": 3,
        "moves": [{"from_peg": 0, "to_peg": 2}],
    }
    response = client.post("/api/runs", json=payload_too_many)
    assert response.status_code == 422

    # Peg index out of bounds (peg 3 doesn't exist)
    payload_bad_peg = {
        "num_disks": 3,
        "solver_type": "manual",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_moves": 1,
        "moves": [{"from_peg": 0, "to_peg": 3}],
    }
    response = client.post("/api/runs", json=payload_bad_peg)
    assert response.status_code == 422


def test_get_recent_runs(client: TestClient, db_session: Session) -> None:
    """Verify that retrieving runs returns lists in correct descending order."""
    # Ensure empty list initially
    response = client.get("/api/runs")
    assert response.status_code == 200
    assert response.json() == []

    # Inject run directly
    run = models.GameRun(
        num_disks=5,
        solver_type="manual",
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        total_moves=31,
        is_completed=True,
    )
    db_session.add(run)
    db_session.commit()

    # Query endpoint
    response = client.get("/api/runs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["num_disks"] == 5
    assert data[0]["total_moves"] == 31
    assert data[0]["solver_type"] == "manual"


def test_solve_recursive_api(client: TestClient) -> None:
    """Verify recursive solver API validation and output."""
    # Valid call
    response = client.get("/api/solve/recursive?num_disks=3")
    assert response.status_code == 200
    data = response.json()
    assert data["solver_type"] == "recursive"
    assert data["num_disks"] == 3
    assert len(data["moves"]) == 7
    assert data["moves"][0]["from_peg"] == 0
    assert data["moves"][0]["to_peg"] == 2

    # Under minimum bounds check
    response_low = client.get("/api/solve/recursive?num_disks=2")
    assert response_low.status_code == 422

    # Over maximum bounds check
    response_high = client.get("/api/solve/recursive?num_disks=9")
    assert response_high.status_code == 422


def test_solve_iterative_api(client: TestClient) -> None:
    """Verify iterative solver API validation and output."""
    # Valid call
    response = client.get("/api/solve/iterative?num_disks=4")
    assert response.status_code == 200
    data = response.json()
    assert data["solver_type"] == "iterative"
    assert data["num_disks"] == 4
    assert len(data["moves"]) == 15

    # Under minimum bounds check
    response_low = client.get("/api/solve/iterative?num_disks=2")
    assert response_low.status_code == 422


def test_solve_search_api(client: TestClient) -> None:
    """Verify search solver API with default and custom start states."""
    # Standard call
    response = client.get("/api/solve/search?num_disks=3")
    assert response.status_code == 200
    data = response.json()
    assert data["solver_type"] == "search"
    assert data["num_disks"] == 3
    assert len(data["moves"]) == 7

    # Custom intermediate state call
    response_custom = client.get(
        "/api/solve/search?num_disks=3&state=%5B%5B3%2C2%5D%2C%5B1%5D%2C%5B%5D%5D"
    )
    assert response_custom.status_code == 200
    data_custom = response_custom.json()
    assert data_custom["solver_type"] == "search"
    assert data_custom["num_disks"] == 3

    # Invalid state format (larger disk on smaller disk)
    response_invalid = client.get(
        "/api/solve/search?num_disks=3&state=%5B%5B2%2C3%5D%2C%5B1%5D%2C%5B%5D%5D"
    )
    assert response_invalid.status_code == 400
    assert "Invalid state parameter" in response_invalid.json()["detail"]


def test_qlearning_api_endpoints(client: TestClient) -> None:
    """Verify Q-learning agent training and solve API endpoints."""
    # 1. Train agent
    payload = {
        "num_disks": 3,
        "episodes": 200,
        "alpha": 0.1,
        "gamma": 0.9,
        "epsilon": 0.2,
    }
    response_train = client.post("/api/solve/qlearning/train", json=payload)
    assert response_train.status_code == 200
    train_data = response_train.json()
    assert train_data["num_disks"] == 3
    assert train_data["episodes"] == 200
    assert "metrics" in train_data
    assert len(train_data["metrics"]["avg_rewards"]) > 0

    # Invalid training parameter
    payload_bad = {
        "num_disks": 3,
        "episodes": 50,  # Below limit of 100
        "alpha": 0.1,
        "gamma": 0.9,
        "epsilon": 0.2,
    }
    response_train_bad = client.post("/api/solve/qlearning/train", json=payload_bad)
    assert response_train_bad.status_code == 422

    # 2. Solve with Q-learning (greedy path with fallback)
    response_solve = client.get("/api/solve/qlearning?num_disks=3")
    assert response_solve.status_code == 200
    solve_data = response_solve.json()
    assert solve_data["solver_type"] == "qlearning"
    assert solve_data["num_disks"] == 3
    assert len(solve_data["moves"]) > 0

