# Phase 5 Plan — Classic Solvers

This document outlines the step-by-step group tasks for implementing recursive and iterative solvers, creating endpoint routers, and designing the playback client.

---

## Group 1 — Backend Solvers

1. Create a `solvers` package directory in the project root.
2. Implement `solvers/classic.py` containing:
   - `solve_recursive` utilizing classic divide-and-conquer logic.
   - `solve_iterative` utilizing a state simulation loop based on disk count parity (even/odd) and step count modulo-3.

## Group 2 — FastAPI Routing

3. Define response models `SolverMoveResponse` and `SolverSolutionResponse` in `main.py`.
4. Implement route `GET /api/solve/recursive` validating `num_disks` and invoking `solve_recursive`.
5. Implement route `GET /api/solve/iterative` validating `num_disks` and invoking `solve_iterative`.

## Group 3 — Frontend Control Panel

6. Update `templates/index.html` with an **Auto-Solver** dashboard panel.
   - Create solver selector dropdown and `Solve & Visualize` button.
   - Build media controls (Play/Pause, Prev, Next, Stop).
   - Insert speed range input (`200ms` - `2000ms`).
   - Create step progress bar and info badge container.
7. Adapt victory card text dynamically using Javascript based on the active run mode.

## Group 4 — Clientside Visualization Logic

8. Update `static/js/game.js` to manage visualizer workflow:
   - Handle visualizer states: `isVisualizing`, `visualMoves`, `currentMoveIndex`, `isPlayingVisual`, `playbackSpeed`, `visualInterval`.
   - Implement `startVisualization(solverType)` fetching data and pausing manual mode.
   - Implement step actions `executeNextMove()` and `executePrevMove()`.
   - Guard drag-and-drop and click events when `isVisualizing` is active.
   - Bind click events for play, pause, step forward/backward, reset/stop.
   - Save completion data with correct `solver_type` (`"recursive"` or `"iterative"`) to backend database.

## Group 5 — Validation Tests

9. Create `tests/test_solvers.py` verifying mathematical solver outputs.
10. Update `tests/test_api.py` verifying `/api/solve/*` query params and return formats.
11. Run linters, type checkers, and test suites to verify system integration.
