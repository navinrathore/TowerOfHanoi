# Phase 7 Validation — Reinforcement Learning Solver

## Definition of Done

All checks in this document must pass before Phase 7 is considered complete.

### 1. Code Quality & Format Checks

#### Linting & Formatting
```bash
ruff check solvers/qlearning.py main.py
ruff format --check solvers/qlearning.py main.py
```
Must report success.

#### Type Checking
```bash
mypy solvers/qlearning.py main.py
```
Must report success with no type errors.

### 2. Unit & Integration Tests Pass

```bash
pytest tests/test_solvers.py -k qlearning
pytest tests/test_api.py -k qlearning
```
Must exit with code 0.

### 3. Solver Verification Script

To verify that the Q-learning solver converges and computes valid moves, run:

```bash
python -c "
from solvers.qlearning import QLearningAgent, state_to_string
from game import HanoiGame

# Train Q-agent for 3 disks
agent = QLearningAgent(3)
results = agent.train(episodes=500, alpha=0.1, gamma=0.9, epsilon=0.2)
assert results['final_success_rate'] > 0.8
assert results['training_time_ms'] < 1000

# Solve using greedy policy
moves = agent.solve('000')
assert len(moves) > 0

# Apply to game and verify solution
game = HanoiGame(3)
for move in moves:
    game.move(move['from_peg'], move['to_peg'])
assert game.is_solved()

print('RL Solver Verification Script Succeeded!')
"
```
Must print `RL Solver Verification Script Succeeded!`.
