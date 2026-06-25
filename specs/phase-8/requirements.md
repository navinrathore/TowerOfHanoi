# Phase 8 Requirements — History & Analytics Dashboard

## Scope

Define and implement the backend aggregates, SQLite persistence, and UI dashboard visualization to provide historical analytics, leaderboard rankings, and performance comparisons of the Tower of Hanoi solvers.

1. **Database Schema & Aggregates**:
   - Create `QLearningTrainingRun` model in `models.py` to persist training hyperparameters, execution time, success rates, training metrics, and serialization of trained Q-table weights (policy weights JSON mapping compact state string keys to action float values).
   - Implement queries in `crud.py`:
     - `get_fastest_runs()`: Query and sort manual game runs by elapsed duration (end time - start time) and total moves for a specific disk count.
     - `get_solver_comparison()`: Retrieve move efficiency and execution compute time groupings for all solver types.
     - `save_training_run()` and `get_latest_training_run()`: Store and load Q-learning agent policies.
     - `seed_database_if_empty()`: Populate initial sample runs if the database is blank on server start.

2. **Backend API Endpoints**:
   - Measure and include `compute_time_ms` for all solvers (`/api/solve/recursive`, `/api/solve/iterative`, `/api/solve/search`, `/api/solve/qlearning`).
   - Expose `/dashboard` HTML render endpoint passing stats card variables, tabbed leaderboard metrics, and comparison stats.
   - Expose `/api/solve/qlearning/last-training` endpoint to serve metrics from the last training run for line charts.

3. **Frontend UI/UX**:
   - Create `templates/dashboard.html` showing total game runs, manual personal best duration, best manual move count, and average solver compute time.
   - Embed **Chart.js Bar Chart** comparing average solver moves to optimal baselines (3–8 disks).
   - Embed **Chart.js Line Charts** visualizing Q-agent training rewards and goal success rates.
   - Design tabbed leaderboard listings for 3–8 disks manual completions.

4. **Testing**:
   - Write unit tests in `tests/test_dashboard.py` covering model schemas, CRUD functions, HTML route status codes, and endpoint payloads.

## Design Decisions

- **SQLite Database Seeding**: Pre-populate database with realistic dummy entries on startup to prevent empty charts and guide UI rendering.
- **Q-learning Weights Serialization**: Store policies as string-keyed dictionaries (`"000": {"0->1": 0.5}`) inside JSON fields for simple, schema-flexible persistence.
- **Logarithmic Scale**: Apply logarithmic scale to solver moves comparison chart to comfortably fit disk counts ranging from 3 to 8.
