# Backlog & Nice-To-Have Features

This document tracks future feature enhancements, design iterations, and database schema updates to be implemented after the core requirements are completed.

## A. Game Statistics & Historical Tracking

- **A1. Player Names / User Profiles**:
  - Add a `player_name` (or `user_id` relation) field to `GameRun` to track who played each game (for leaderboard personalization).
- **A2. Solver Configurations & Hyperparameters**:
  - Add fields or a JSON column to `GameRun` to record hyperparameters (e.g. training episodes, learning rate `alpha`, discount factor `gamma`, exploration rate `epsilon` for the Q-learning solver; or heuristic type for A* search).
- **A3. Error / Interruption Logging**:
  - Log reason for failures or mid-game resets if a user starts a run but cancels/fails it.
- **A4. Detailed Solver Metrics**:
  - Track metrics like peak memory usage, CPU/GPU training time, or number of states explored.
- **A5. Live Move Logging**:
  - Transition from batch logging at the end of a game run to real-time live logging of moves (sending a POST request on every valid move) to allow tracing of active in-progress game states.
- **A6. Interactive Trajectory Replay**:
  - Save computed solver runs (classical, A*, or Q-learning paths) in the database so users can browse historical runs in the dashboard and replay them visually step-by-step.
- **A7. Local Storage Game State Persistence**:
  - Store the active manual game state in the browser's localStorage so that users can resume their current game progress after a page refresh or accidental window closure.

## B. Architectural & Offline Improvements

- **B1. Compressed Binary Q-Table Serialization**:
  - Store serialized Q-tables in a compressed binary format (e.g., zlib-compressed BLOBs) rather than raw JSON strings in the SQLite database to prevent DB bloat and improve startup loading performance for larger disk counts (7+ disks).
- **B2. Asynchronous Q-Agent Training**:
  - Run reinforcement learning training sessions asynchronously (using FastAPI `BackgroundTasks` or Celery workers) instead of blocking the main ASGI server thread on large episode sizes.
- **B3. Formal Database Migration Framework**:
  - Integrate Alembic rather than checking column lists manually with SQLAlchemy inspection to perform safe local database upgrades.
- **B4. SQLite WAL Mode & Connection Pool Optimization**:
  - Configure Write-Ahead Logging (WAL) and optimize the connection pool settings in SQLAlchemy to prevent concurrent write locks during intensive RL training sessions or multi-user runs.
- **B5. Bundled Assets for Offline Play**:
  - Download and host client dependencies (such as Tailwind CSS, Chart.js, Google Fonts) locally in `static/` to enable fully isolated offline execution.

## C. Testing & Verification (Nice-to-Have)

- **C1. Mock UI / Headless Browser Verification**:
  - Implement mock browser testing (such as a simulated DOM test client or JSDOM integration) to verify interactive click and drag-and-drop gameplay flows in headless CI/CD environments without relying on real browser CDP connections.

## D. Game Variants & Solver Enhancements

- **D1. Multi-Peg Support (Reve's Puzzle)**:
  - Extend the core engine and solvers to support 4-peg Tower of Hanoi variations (Reve's Puzzle), which introduces more complex state transitions and optimization heuristics (e.g., Frame-Stewart algorithm).
- **D2. Classic Solver Step Pagination or Streaming**:
  - Paginate or stream steps for recursive and iterative solvers in the API to prevent high response load or memory bottlenecks when computing solutions for high disk counts ($N > 8$).

## E. Reinforcement Learning & Solver Insights

- **E1. Q-Agent Training Visualization Enhancements**:
  - Add real-time visual insights for the Q-learning agent during training, including:
    - *State Space Coverage*: Percentage of total valid game states visited/updated in the Q-table.
    - *Exploration vs. Exploitation Ratio*: A real-time line chart tracking the decay of epsilon (exploration rate).
    - *Q-value State Transitions*: Heatmap overlay showing the strength of Q-value pathways on the pegs.

## F. User Interface & Sound Effects

- **F1. Audio/Haptic Feedback**:
  - Add optional click/whoosh sound effects or haptic visual feedback on peg placement to enhance the tactile feel of the drag-and-drop gameplay.

## G. Educational & Lore Content

- **G1. History and Origins Page**:
  - Add a dedicated page on the web interface detailing the history and backstory of the Tower of Hanoi.
  - Explain the origins of the game, invented by French mathematician Édouard Lucas in 1883.
  - Detail the fictional "Indian connection"—the mythical legend of the "Tower of Brahma" in a temple in Kashi (Varanasi), India, where Brahmin priests are supposedly moving 64 golden disks, whose completion would signal the end of the universe.
  - Clarify the relationship with the actual city of Hanoi, Vietnam: Explain that the game has no historical or cultural connection to the city, and the name "Hanoi" was simply used for 19th-century exotic marketing.
  - Briefly describe modern-day Hanoi to show the contrast and confirm there are no temples or artifacts related to the game there.
