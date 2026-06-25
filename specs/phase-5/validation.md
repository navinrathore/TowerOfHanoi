# Phase 5 Validation — Classic Solvers

## Definition of Done

All checks in this document must pass before Phase 5 is considered complete.

### 1. Code Quality & Format Checks

#### Linting
```bash
ruff check .
```
Must exit with code 0 and report no linting errors.

#### Formatting
```bash
ruff format --check .
```
Must exit with code 0 and report no formatting violations.

#### Type Checking
```bash
mypy .
```
Must exit with code 0 and report success with no type errors. The newly implemented solver functions, router schemas, endpoints, and unit test files must be fully type-hinted.

### 2. Unit & Integration Tests Pass

```bash
pytest
```
Must exit with code 0 and pass all tests, including new solver validation tests.

### 3. Solver Verification Script

To verify that the recursive and iterative solvers compute valid, optimal steps, run:

```bash
python -c "
from solvers.classic import solve_recursive, solve_iterative
from game import HanoiGame

# Test Recursive
moves_rec = solve_recursive(3)
assert len(moves_rec) == 7
game_rec = HanoiGame(3)
for move in moves_rec:
    game_rec.move(move['from_peg'], move['to_peg'])
assert game_rec.is_solved()

# Test Iterative
moves_iter = solve_iterative(4)
assert len(moves_iter) == 15
game_iter = HanoiGame(4)
for move in moves_iter:
    game_iter.move(move['from_peg'], move['to_peg'])
assert game_iter.is_solved()

print('Solver Verification Script Succeeded!')
"
```
Must print `Solver Verification Script Succeeded!` and execute without throwing exceptions.
