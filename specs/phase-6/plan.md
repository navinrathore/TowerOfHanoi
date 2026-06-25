# Phase 6 Plan — Search-based Solver

This document outlines the step-by-step group tasks for implementing the A* search solver, registering endpoints, and building the interactive client layout.

---

## Group 1 — Backend Solvers

1. Implement `solvers/search.py` containing:
   - `compute_hanoi_distance`: Recursive perfect linear-time heuristic.
   - `solve_search`: A* pathfinding using `heapq` with tie-breaker sorting.
2. Update `solvers/__init__.py` to export `solve_search`.

## Group 2 — FastAPI Routing

3. Update `main.py` to import `solve_search`.
4. Register `GET /api/solve/search` taking `num_disks` and optional `state` parameter.
5. Parse `state` JSON list-of-lists, validate peg disk sizes order constraints, and execute `solve_search`.

## Group 3 — Frontend Control Panel & Javascript Client

6. Add select option for `A* Search Solver` inside `#solverType` in `templates/index.html`.
7. Modify `startVisualization()` in `static/js/game.js`:
   - Identify if `solverType === 'search'`.
   - Preserve current board pegs (avoid resetting) unless already solved.
   - Stringify `this.pegs` to JSON and pass it in the `state` parameter of the fetch URL.

## Group 4 — Validation Tests

8. Add `test_search_solver_correctness()` in `tests/test_solvers.py`.
9. Add `test_solve_search_api()` in `tests/test_api.py`.
10. Execute code verifications (`pytest`, `ruff`, `mypy`).
