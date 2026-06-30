# Phase 10 Requirements — Feature Enhancements

## Scope
This phase introduces feature enhancements to the Tower of Hanoi application to improve user engagement, gameplay robustness, and training scalability.

---

## 1. Player Profiles & Leaderboard Submissions (A1)
- **Objective:** Track individual user attempts on the dashboard's manual leaderboard.
- **Workflow:**
  - When a user wins a manual game (represented by solver type `manual`), do not save the game run immediately.
  - Show a modal popup prompting the user for their name.
  - The modal will have:
    - A text input field for the player's name (max 50 characters).
    - A "Submit Score" button.
    - A "Skip / Anonymous" button.
  - On submission, POST the game run and its moves payload to `/api/runs` with the entered `player_name` (or `Anonymous` if skipped).
  - The leaderboard query must show the player name alongside their completion time and move count.

---

## 2. Browser Local Storage Game Persistence (A7)
- **Objective:** Prevent loss of in-progress manual games due to browser refreshes or closure.
- **Workflow:**
  - On every valid disk move or game state update (such as changing the disk count), store the current state in browser `localStorage`.
  - The stored schema inside `localStorage` under key `hanoi_saved_game` must include:
    - `num_disks`: Integer (3 to 8).
    - `pegs`: Array of arrays (e.g. `[[3, 2, 1], [], []]`) representing the disk positions.
    - `moves`: Array of moves made so far (e.g. `[{from_peg: 0, to_peg: 2}, ...]`).
    - `start_time`: ISO string of when the game run started.
  - On page load, if a valid `hanoi_saved_game` exists:
    - Display a modal dialog immediately: **"Resume saved game or start a new game?"**
    - Clicking **"Resume"** restores the saved disk setup, move counter, and timer.
    - Clicking **"New Game"** clears the storage and initializes the default configuration.

---

## 3. Asynchronous Q-Learning Training (B2)
- **Objective:** Move reinforcement learning training off the main web thread to prevent timeouts and blocking ASGI workers on large episode counts.
- **Workflow:**
  - Replace the blocking `/api/solve/qlearning/train` behavior.
  - The endpoint will initiate training asynchronously using FastAPI `BackgroundTasks`.
  - The endpoint must immediately return a `task_id` (a UUID string) and current status `PENDING` / `RUNNING`.
  - Expose a new progress polling endpoint `/api/solve/qlearning/train/status/{task_id}` that returns:
    - `task_id`: String.
    - `status`: String (`PENDING` | `RUNNING` | `COMPLETED` | `FAILED`).
    - `progress`: Float (value from 0.0 to 1.0 representing percentage of episodes completed).
    - `results`: Optional object containing the final metrics and success rates when status is `COMPLETED`.
  - The frontend must poll this status endpoint every 500ms while training is in progress, updating a linear progress bar and status text in real time.
