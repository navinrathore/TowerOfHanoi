# Backlog & Nice-To-Have Features

This document tracks future feature enhancements, design iterations, and database schema updates to be implemented after the core requirements are completed.

## Game Statistics & Historical Tracking

- **Player Names / User Profiles**:
  - Add a `player_name` (or `user_id` relation) field to `GameRun` to track who played each game (for leadboard personalization).
- **Solver Configurations & Hyperparameters**:
  - Add fields or a JSON column to `GameRun` to record hyperparameters (e.g. training episodes, learning rate `alpha`, discount factor `gamma`, exploration rate `epsilon` for the Q-learning solver; or heuristic type for A* search).
- **Error / Interruption Logging**:
  - Log reason for failures or mid-game resets if a user starts a run but cancels/fails it.
- **Detailed Solver Metrics**:
  - Track metrics like peak memory usage, CPU/GPU training time, or number of states explored.
- **Live Move Logging**:
  - Transition from batch logging at the end of a game run to real-time live logging of moves (sending a POST request on every valid move) to allow tracing of active in-progress game states.

## Architectural & Offline Improvements

- **Asynchronous Q-Agent Training**:
  - Run reinforcement learning training sessions asynchronously (using FastAPI `BackgroundTasks` or Celery workers) instead of blocking the main ASGI server thread on large episode sizes.
- **Formal Database Migration Framework**:
  - Integrate Alembic rather than checking column lists manually with SQLAlchemy inspection to perform safe local database upgrades.
- **Bundled Assets for Offline Play**:
  - Download and host client dependencies (such as Tailwind CSS, Chart.js, Google Fonts) locally in `static/` to enable fully isolated offline execution.

