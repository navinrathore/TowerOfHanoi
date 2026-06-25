# Phase 7 Requirements — Reinforcement Learning Solver

## Scope

Define and implement a Reinforcement Learning (tabular Q-learning) agent to solve the Tower of Hanoi problem, expose FastAPI endpoints to trigger agent training and retrieve solutions, and build a training configuration panel with an SVG reward metrics chart.

1. **Backend Integration**:
   - Implement Q-learning agent in `solvers/qlearning.py`.
   - State representation: Compact string indicating disk peg locations (e.g. `"210"`).
   - Actions: 6 possible moves represented as integer indices 0-5.
   - Reward structure: $+100$ for reaching target state (`"2" * N`), $-1$ for valid moves, and $-10$ penalty for invalid moves.
   - Endpoint `POST /api/solve/qlearning/train` taking episodes count, alpha, gamma, and epsilon, returning training speed (ms), convergence rate, and metrics.
   - Endpoint `GET /api/solve/qlearning` returning greedy moves, falling back to A* pathfinder if unvisited states or cycles are hit.

2. **Frontend UI/UX**:
   - Add dropdown option `Q-learning Solver` inside the Auto-Solver panel.
   - Add a toggleable **Q-learning Training Panel** displaying input fields for Episodes, Alpha, Gamma, and Epsilon, and a `Train Q-Agent` action button.
   - Add training progress overlays and metrics stats (training duration, success rate).
   - Draw a custom, lightweight **SVG line chart** mapping the average reward per episode chunk, showing convergence progress.
   - Support solving from the current state (passing JSON pegs string) during playback.

3. **Testing**:
   - Write unit tests in `tests/test_solvers.py` validating state translation strings, step transitions, penalties, training, and solution convergence.
   - Write API tests in `tests/test_api.py` validating training endpoint boundaries, parameters, and solve falls.

## Design Decisions

- **Epsilon Decay**: Exploration rate $\epsilon$ decays exponentially during training to reach its minimum value near the end, letting the policy stabilize.
- **A\* Fallback**: Ensures a robust solution path is always provided to the client even if Q-learning has not explored or trained on the given state configuration.
- **Dependency-Free Plots**: SVG drawings in Javascript avoid large charting library bundles, keeping templates loading fast.
