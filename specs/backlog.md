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
