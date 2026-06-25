# Phase 6 Requirements — Search-based Solver

## Scope

Define and implement a search-based pathfinding solver using A* algorithm to compute the shortest solution path from any valid intermediate game state to the win state, expose a FastAPI endpoint to retrieve this solution, and integrate the solver into the visualizer dashboard.

1. **Backend Integration**:
   - Implement an A* search solver in `solvers/search.py` finding the shortest path to target Peg 2.
   - Implement an exact, admissible, and perfect $O(N)$ distance heuristic based on the recursive structure of the Tower of Hanoi.
   - Expose endpoint `GET /api/solve/search` taking `num_disks` (3 to 8) and an optional `state` parameter representing the current configuration.
   - Standardize JSON response schema to match other solvers: `{ "solver_type": "search", "num_disks": int, "moves": [{ "from_peg": int, "to_peg": int }] }`.

2. **Frontend UI/UX**:
   - Add dropdown option `A* Search Solver` inside the Auto-Solver panel.
   - Update `game.js` to avoid resetting the board configuration to standard initial layout if `A* Search` is selected (unless the game is already won).
   - Encode the current peg lists as JSON and pass it in the `state` query parameter of the solve request.
   - Support step-by-step playback controls (Play, Pause, Step Forward/Backward, Stop).

3. **Testing**:
   - Write unit tests in `tests/test_solvers.py` validating that A* outputs are legal and optimal from standard and random intermediate configurations.
   - Write API tests in `tests/test_api.py` validating boundary constraints, custom start state parameters, and error responses for invalid configurations.

## Design Decisions

- **Arbitrary Configuration Solving**: Unlike classic solvers, the search solver must find the path from any intermediate state (e.g. disk layout in the middle of a manual play).
- **Exact Linear Heuristic**: Leverage the recursive distance function to serve as a perfect $O(N)$ heuristic, preventing A* from expanding unnecessary states and improving computation speed.
- **Save stats**: Search runs are logged to SQLite like other solvers.
