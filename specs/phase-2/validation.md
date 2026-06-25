# Phase 2 Validation — Tower of Hanoi Core Engine

## Definition of Done

All of the following checks must pass before Phase 2 is considered complete and ready for database integration.

### 1. Code Quality & Format Checks

#### Linting
```bash
ruff check .
```
Must exit with code 0 and report no linting errors in `game.py` or `tests/test_game.py`.

#### Formatting
```bash
ruff format --check .
```
Must exit with code 0 and report no formatting violations.

#### Type Checking
```bash
mypy .
```
Must exit with code 0 and report success with no type errors (verifying full type safety in `game.py` and `tests/test_game.py`).

### 2. Unit Tests Pass
```bash
pytest tests/test_game.py
```
Must exit with code 0 and pass all tests. At least 6 distinct test cases should be covered.

### 3. API Contract and Interactive Session Validation

To verify the game engine behaves exactly as specified, you can run a quick interactive Python check.

```bash
python -c "
from game import HanoiGame, InvalidMoveError
game = HanoiGame(3)
assert game.get_state() == ((3, 2, 1), (), ())
game.move(0, 2)
assert game.get_state() == ((3, 2), (), (1,))
assert game.move_count == 1
assert not game.is_solved()
try:
    game.move(0, 2)  # Invalid: placing 2 on top of 1
    assert False, 'Expected InvalidMoveError'
except InvalidMoveError:
    pass
print('API Validation Succeeded!')
"
```
Must print `API Validation Succeeded!` and execute without throwing assertions.
