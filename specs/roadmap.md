# Roadmap

The implementation is broken down into small, iterative, and independently testable phases.

---

## Phase 1 — Project Scaffolding & Hello FastAPI
- Set up python environment and dependencies in `requirements.txt`.
- Configure `main.py` with FastAPI and a basic `/` route returning JSON.
- Add typecheck, formatting, and pytest boilerplate.
- Establish strict type check rules.

## Phase 2 — Tower of Hanoi Core Engine
- Create `game.py` containing the core game state representation (`HanoiGame`).
- Implement disk movement logic with validation rules (e.g. cannot place a larger disk on a smaller one).
- Write extensive unit tests in `tests/test_game.py` covering valid moves, invalid moves, and win conditions.

## Phase 3 — Database Schema & Setup
- Set up SQLite connection via SQLAlchemy in `database.py` and models in `models.py`.
- Define schemas for:
  - `GameRun`: Holds details about a completed/in-progress game (start/end times, disk count, solver type, total moves).
  - `GameMove`: Log of individual moves (from peg, to peg, move number, timestamp).
- Implement functions to save/query game stats.

## Phase 4 — Interactive Web UI (Playable Mode)
- Create base Jinja2 layouts with Tailwind CSS.
- Build a game dashboard where players can select disk count (3 to 8 disks) and play manually.
- Use simple drag-and-drop or click-to-move JavaScript interactions.
- Record stats and persist game results to SQLite upon win.

## Phase 5 — Classic Solvers
- Implement Recursive and Iterative solvers in `solvers/classic.py`.
- Expose APIs `/api/solve/recursive` and `/api/solve/iterative` that return the list of steps to solve a given configuration.
- Implement UI visualization that plays the steps step-by-step with play/pause controls.

## Phase 6 — Search-based Solver
- Implement A* (or BFS) pathfinding solver in `solvers/search.py` to find the shortest path from any valid intermediate game state to the win state.
- Expose search solver via `/api/solve/search`.
- Integrate into the UI visualization.

## Phase 7 — Reinforcement Learning (Q-learning) Solver
- Implement a Q-learning agent in `solvers/qlearning.py`.
- Model state representation (tuple of disk positions or string representation).
- Model action space (moves between valid pegs: 0->1, 0->2, etc.).
- Implement reward structure (positive reward for reaching target state, small negative reward for each move to encourage shortest path, large penalty for invalid moves).
- Provide API to trigger agent training session (setting episodes, alpha, gamma, epsilon).
- Visual UI for Q-learning: see training progress, explore-vs-exploit rates, and watch the trained agent solve the game.

## Phase 8 — History & Analytics Dashboard
- Create `/dashboard` route showing aggregated statistics.
- Display a leaderboard of fastest manual completions.
- Compare solver efficiency (Recursive/Iterative vs A* vs Q-learning).
- Render progress charts (e.g., Q-learning success rate / cumulative reward per episode).

## Phase 9 — UI Polish & Accessibility
- Add smooth transitions/animations for disk movements.
- Make the interface mobile-responsive.
- Add keyboard accessibility to move disks between rods.
