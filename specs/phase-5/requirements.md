# Phase 5 Requirements — Classic Solvers

## Scope

Define and implement algorithmic solvers to compute the step-by-step solution for the Tower of Hanoi problem, expose FastAPI endpoints to retrieve these solutions, and construct a premium visualizer dashboard with playback controls.

1. **Backend Integration**:
   - Implement a recursive divide-and-conquer solver in `solvers/classic.py`.
   - Implement an iterative/modulo-3 solver in `solvers/classic.py`.
   - Expose endpoint `GET /api/solve/recursive` taking `num_disks` (3 to 8) and returning the full sequence of moves.
   - Expose endpoint `GET /api/solve/iterative` taking `num_disks` (3 to 8) and returning the full sequence of moves.
   - Standardize JSON response schema: `{ "solver_type": str, "num_disks": int, "moves": [{ "from_peg": int, "to_peg": int }] }`.

2. **Frontend UI/UX**:
   - Create an **Auto-Solver** panel on the dashboard.
   - Add a dropdown selector to choose between `Recursive` and `Iterative` solvers.
   - Implement a primary control button: `Solve & Visualize`.
   - Include simulation controls: Play/Pause toggle, Step Forward (`>|`), Step Backward (`|<`), and Stop/Reset (`■`).
   - Add a playback speed slider to adjust move delays dynamically between `200ms` and `2000ms` (default `500ms`).
   - Render a visual progress bar and step indicator text (`Step X of Y`) to display visualization progress.

3. **Simulation Mechanics**:
   - Upon clicking `Solve & Visualize`, fetch steps from the API, stop manual stopwatch, reset board state to standard initial state, and lock manual interaction (drag-and-drop / click-to-move).
   - Sequentially execute moves at the specified speed interval.
   - Dynamically update move counters, simulated timer, and efficiency stats (always 100% for optimal solvers).
   - Allow user to pause/resume playback, or step through moves one-by-one using step buttons.
   - Display a customized victory card ("Solver Completed!") upon finishing, and log the completed run to the database via `POST /api/runs` with `solver_type="recursive"` or `"iterative"`.

4. **Testing**:
   - Write unit tests in `tests/test_solvers.py` validating that solver outputs are legal (never place larger disk on smaller disk) and optimal ($2^n - 1$ moves).
   - Write API tests in `tests/test_api.py` validating query parameter boundary checks and response schemas.

## Out of Scope

- Heuristic search solvers (e.g. A* pathfinding from arbitrary configurations) (Phase 6).
- Reinforcement learning training session interfaces (Phase 7).

## Design Decisions

- **Standard State Solving**: Classic solvers assume a standard starting state of all `n` disks on Peg 0 (Peg A) and solve towards Peg 2 (Peg C).
- **Interaction Locking**: Disabling mouse drag-and-drop/clicking prevents conflicts between automated animations and manual actions.
- **Benching Logs**: Solver runs are stored in the database so that we can compare manual player performance against recursive/iterative solvers in the Phase 8 analytics view.
