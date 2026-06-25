# Phase 8 Plan — History & Analytics Dashboard

This document outlines the step-by-step group tasks for implementing the SQLite analytics tables, seeding sample runs, computing solver durations, and building the Chart.js visual dashboard.

---

## Group 1 — Database Models & CRUD

1. Implement `QLearningTrainingRun` in `models.py`.
2. Add nullable `compute_time_ms` to `GameRun` inside `models.py`.
3. In `crud.py`, implement helper query and seeding methods:
   - `get_fastest_runs(db, num_disks, limit)`
   - `get_solver_comparison(db)`
   - `save_training_run(db, ...)`
   - `get_latest_training_run(db, num_disks)`
   - `seed_database_if_empty(db)`

## Group 2 — FastAPI Routing & Startup

4. Set up startup database migration for the new column `compute_time_ms` and database seeding inside `main.py`.
5. Register pre-training for a default 3-disk agent on server startup if no trained agents exist.
6. Measure time durations using `time.perf_counter()` on all solver endpoints and include `compute_time_ms` in responses.
7. Expose API endpoint `/api/solve/qlearning/last-training`.
8. Register HTML route `/dashboard` that queries aggregate data and passes it to the template engine.

## Group 3 — UI Dashboard Template

9. Create `templates/dashboard.html` with:
   - Stats summary cards row.
   - Chart.js configuration for solver moves bar chart (logarithmic scale).
   - Chart.js configuration for reward and success rate training curves.
   - Tabbed manual scoreboards for disk counts 3 to 8.
   - Detail comparison table listing solver configurations.
10. Update `templates/base.html` navigation to link between "Play Mode" and "Dashboard", updating version badge.

## Group 4 — Verification Tests

11. Create `tests/test_dashboard.py` containing tests for:
    - Seeding database verification.
    - Sorting logic of manual best runs.
    - Solver aggregations.
    - JSON serialization of Q-tables.
    - Route responses and query filters.
12. Run the test suite using `pytest`.
