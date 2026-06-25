# Phase 7 Plan — Reinforcement Learning Solver

This document outlines the step-by-step group tasks for implementing the tabular Q-learning agent, registering training routes, and building the interactive progress plotting dashboard.

---

## Group 1 — Backend Solvers

1. Implement `solvers/qlearning.py` containing:
   - State/peg conversion methods (`state_to_string`, `string_to_pegs`).
   - `step_state` transitions applying rewards ($+100$, $-1$, $-10$).
   - `QLearningAgent` class with an epsilon-greedy choice policy, a decay training loop, and a greedy solver with A* search fallback.
2. Update `solvers/__init__.py` to export `QLearningAgent`.

## Group 2 — FastAPI Routing & Cache

3. Register in-memory cache `TRAINED_Q_TABLES` in `main.py`.
4. Define schemas `QLearningTrainRequest`, `QLearningTrainResponse`, and `QLearningMetrics`.
5. Register route `POST /api/solve/qlearning/train` returning performance curves.
6. Register route `GET /api/solve/qlearning` that runs Q-solver (and trains a default one on-the-fly if not cached).

## Group 3 — Frontend Control Panel & Charting Client

7. Integrate dropdown option `Q-learning Solver` inside `templates/index.html`.
8. Add training form fields (episodes, alpha, gamma, epsilon), train button, status indicators, stats metrics, and chart container `#qRewardSvgChart`.
9. Modify `game.js` to:
   - Handle solver method change, showing/hiding training panel.
   - Implement `trainQAgent()` invoking training POST API and rendering metrics.
   - Implement `drawRewardChart(metrics)` which generates and injects a custom SVG line plot of rewards.
   - Support state-based solving query arguments.

## Group 4 — Validation Tests

10. Add `test_qlearning_utilities_and_agent()` in `tests/test_solvers.py`.
11. Add `test_qlearning_api_endpoints()` in `tests/test_api.py`.
12. Run final tests (`pytest`, `ruff`, `mypy`).
