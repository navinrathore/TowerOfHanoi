# Phase 6 Validation — Search-based Solver

## Definition of Done

All checks in this document must pass before Phase 6 is considered complete.

### 1. Code Quality & Format Checks

#### Linting & Formatting
```bash
ruff check solvers/search.py main.py
ruff format --check solvers/search.py main.py
```
Must report success.

#### Type Checking
```bash
mypy solvers/search.py main.py
```
Must report success with no type errors.

### 2. Unit & Integration Tests Pass

```bash
pytest tests/test_solvers.py -k search
pytest tests/test_api.py -k search
```
Must exit with code 0.

### 3. Solver Verification Script

To verify that the search solver computes valid steps from standard and arbitrary intermediate configurations, run:

```bash
python -c "
from solvers.search import solve_search
from game import HanoiGame

# Test Standard Initial State
moves_std = solve_search(3)
assert len(moves_std) == 7
game_std = HanoiGame(3)
for move in moves_std:
    game_std.move(move['from_peg'], move['to_peg'])
assert game_std.is_solved()

# Test Arbitrary State
# pegs: [[3, 2], [1], []]
start_state = ((3, 2), (1,), ())
moves_custom = solve_search(3, start_state=start_state)
game_custom = HanoiGame(3)
game_custom.pegs = [list(p) for p in start_state]
for move in moves_custom:
    game_custom.move(move['from_peg'], move['to_peg'])
assert game_custom.is_solved()

print('Search Solver Verification Script Succeeded!')
"
```
Must print `Search Solver Verification Script Succeeded!`.
