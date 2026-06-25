# Phase 2 Plan — Tower of Hanoi Core Engine

This document outlines the step-by-step implementation plan for building the Tower of Hanoi game state engine.

---

## Group 1 — Setup and Exceptions

1. Create a new file `game.py` in the root directory.
2. In `game.py`, define the custom exception class:
   ```python
   class InvalidMoveError(ValueError):
       """Raised when a move violates the Tower of Hanoi rules."""
       pass
   ```
3. Include standard type hints (`from typing import List, Tuple` if targeting older Python, or use modern syntax `list[tuple[int, int]]` since we are on Python 3.12).

## Group 2 — HanoiGame Class Structure & Initialization

4. Define the `HanoiGame` class.
5. Implement the constructor `__init__(self, num_disks: int = 3)`:
   - Validate $3 \le \text{num\_disks} \le 8$. Raise `ValueError` if out of bounds.
   - Store `self.num_disks = num_disks`.
   - Store `self.move_count = 0`.
   - Initialize `self.pegs: list[list[int]]` where:
     - Peg 0 contains `list(range(num_disks, 0, -1))` (e.g., `[3, 2, 1]` for $N=3$).
     - Peg 1 is `[]`.
     - Peg 2 is `[]`.

## Group 3 — Core Game Logic Methods

6. Implement `reset(self) -> None`:
   - Reset `self.pegs` to the initial configuration.
   - Reset `self.move_count` to 0.
7. Implement `get_state(self) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]`:
   - Convert `self.pegs` list representation into a tuple of tuples.
   - Ensure the return type matches `tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]`.
8. Implement `is_solved(self) -> bool`:
   - Return `True` if `len(self.pegs[2]) == self.num_disks` (this implies all disks are on peg 2, because other pegs must be empty, and rules prevent smaller disks below larger ones, guaranteeing the order is correct).
9. Implement `get_valid_moves(self) -> list[tuple[int, int]]`:
   - Iterate over all pairs of rods `(from_peg, to_peg)` where $0 \le \text{from\_peg, to\_peg} \le 2$ and $\text{from\_peg} \ne \text{to\_peg}$.
   - For each pair, check if moving is valid:
     - Peg `from_peg` must not be empty.
     - Peg `to_peg` is empty, OR the top disk of `from_peg` (last element) is smaller than the top disk of `to_peg` (last element).
   - Return list of valid move pairs.
10. Implement `move(self, from_peg: int, to_peg: int) -> None`:
    - Perform bounds check: validation that `from_peg` and `to_peg` are in `{0, 1, 2}`. Raise `InvalidMoveError` if not.
    - Check if source and destination pegs are the same. Raise `InvalidMoveError` if so.
    - Check if source peg `self.pegs[from_peg]` is empty. Raise `InvalidMoveError` if so.
    - Check if the top disk of source peg `self.pegs[from_peg][-1]` is larger than the top disk of destination peg `self.pegs[to_peg][-1]` (if destination peg is not empty). Raise `InvalidMoveError` if so.
    - If all validations pass:
      - Pop disk from source peg: `disk = self.pegs[from_peg].pop()`.
      - Append disk to destination peg: `self.pegs[to_peg].append(disk)`.
      - Increment `self.move_count` by 1.

## Group 4 — Testing

11. Create a test file `tests/test_game.py`.
12. Write unit tests:
    - `test_game_initialization`: Verify state, default disk count, disk layout, move count, and bounds validation on disk counts (test $N=2$ and $N=9$ raise errors).
    - `test_valid_move`: Perform a valid move (0 to 1) and verify state changes, pegs content, and `move_count` increment.
    - `test_invalid_moves`: Test all failure modes (empty source, placing larger on smaller, invalid peg index, moving to same peg) and verify `InvalidMoveError` is raised.
    - `test_is_solved`: Set up a winning configuration manually and verify `is_solved()` returns `True`. Also verify it returns `False` for initial state and intermediate states.
    - `test_get_valid_moves`: Verify that list of valid moves matches expected rules for various board configurations.
    - `test_get_state_immutability`: Verify `get_state()` returns hashable tuple-of-tuples representation and doesn't mutate or share references.
    - `test_reset`: Perform some moves, then call `reset()` and check that the pegs and move count revert to initial state.

## Group 5 — Validation

13. Verify code quality using linting/formatting:
    - Run `ruff check .`
    - Run `ruff format --check .`
14. Verify type safety:
    - Run `mypy .`
15. Run test suite:
    - Run `pytest`
