# Phase 10 Plan — Feature Enhancements

This document outlines the tasks required to implement Player Profiles, Local Storage Persistence, and Asynchronous Q-Learning Training.

---

## Group 1 — Database & API Contracts

1. Verify `models.py` has `player_name` mapped correctly on `GameRun`.
2. Confirm Pydantic schemas in `main.py` (`GameRunBatchCreate`, `GameRunResponse`) have `player_name: Optional[str] = None`.
3. In `main.py`, ensure the startup migration block:
   - Inspector column check adds `player_name` if missing in SQLite.
4. Modify `crud.py`'s `seed_database_if_empty()` to assign mock player names (e.g. "Ada Lovelace", "Alan Turing", "Grace Hopper") to manual runs.

---

## Group 2 — UI & Gameplay Winning Modal

5. In `templates/index.html`, add a modal dialog overlay `#scoreSubmissionModal`:
   - Backdrop styling (glassmorphism/blur overlay).
   - Form field for `playerNameInput`.
   - Submit Button and Skip Button.
6. In `static/js/game.js`, edit the `checkWin()` or completion logic:
   - If `solverType === 'manual'`, prevent immediate POST.
   - Show the `#scoreSubmissionModal`.
   - On clicking submit/skip, package the final JSON payload (including `player_name`) and post to `/api/runs`.
   - Hide the modal.

---

## Group 3 — Local Storage Resume Flow

7. In `static/js/game.js`, implement helper functions:
   - `saveToLocalStorage()`: Serializes `numDisks`, current rod configuration arrays, total move counter, and start timestamp, then saves them to `localStorage.setItem('hanoi_saved_game', ...)`.
   - `clearLocalStorage()`: Removes the key on game completion or reset.
8. Call `saveToLocalStorage()` on every valid disk movement.
9. In `templates/index.html`, add `#resumeGameModal` overlay asking if the player wants to resume.
10. In `static/js/game.js` init method:
    - Check if a saved game exists in `localStorage`.
    - If found, open `#resumeGameModal`.
    - If user chooses **Resume**: Load state variables, recreate the visual disk layout, restore elapsed timer, and update the UI move count.
    - If user chooses **New Game** (or closes the modal): Clear localStorage and initialize default state.

---

## Group 4 — Asynchronous Q-Learning Core

11. In `main.py`, define a global thread-safe tasks dictionary:
    ```python
    TRAINING_STATUS: dict[str, dict] = {}
    ```
12. Modify the Q-Learning agent's training loop in `solvers/qlearning.py` to support progress reporting. We can pass a callback function to `train(..., progress_callback=...)`.
13. Implement the background trainer function in `main.py`:
    ```python
    def run_training_background(task_id: str, num_disks: int, episodes: int, alpha: float, gamma: float, epsilon: float, db_session_maker):
        # Callback updates TRAINING_STATUS[task_id]["progress"]
        # On complete, saves results to database via session maker and sets status to COMPLETED
    ```
14. Rewrite `@app.post("/api/solve/qlearning/train")`:
    - Generate a unique task UUID `task_id`.
    - Initialize task record in `TRAINING_STATUS`.
    - Spawn `run_training_background` via FastAPI `BackgroundTasks`.
    - Return `{"task_id": task_id, "status": "PENDING"}` immediately.
15. Implement `@app.get("/api/solve/qlearning/train/status/{task_id}")`:
    - Check task record in `TRAINING_STATUS`.
    - Return task details including progress percentage (0.0 to 1.0) and final results if done.

---

## Group 5 — Frontend Training Progress UI

16. In `templates/index.html` (Q-learning tab / card section), add:
    - A progress bar overlay element.
    - Status labels ("Initiating...", "Training: 45%", "Finalizing...").
17. In `static/js/game.js`, update the Q-Learning training form submit handler:
    - On POST to train, capture the returned `task_id`.
    - Disable training configuration controls.
    - Start an interval that calls `fetch('/api/solve/qlearning/train/status/' + taskId)` every 500ms.
    - Update progress bar width and labels dynamically.
    - When status is `COMPLETED`, update charts, re-enable buttons, and refresh the dashboard.
