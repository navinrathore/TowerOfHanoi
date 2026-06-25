# Phase 2 Requirements — Tower of Hanoi Core Engine

## Scope

Define and implement the core Tower of Hanoi game logic module (`game.py`) and its corresponding unit tests (`tests/test_game.py`). The core engine must manage the state of the puzzle, enforce all standard game rules, provide helpers for solvers, and ensure strict type hints and PEP 8 conformity.

1. **Game State Representation**:
   - Class `HanoiGame` in `game.py`.
   - Pegs must be represented using 3 pegs (numbered 0, 1, 2).
   - The disks must be numbered from `1` (smallest) to `N` (largest).
   - Initial state: All $N$ disks on Peg 0, sorted in descending order (largest disk at the bottom, smallest disk at the top).
   - Solved state: All $N$ disks on Peg 2, sorted in descending order.

2. **Core API / Methods**:
   - `__init__(self, num_disks: int = 3)`:
     - Configures the number of disks $N$.
     - Validates that $N$ is between 3 and 8 inclusive. Raises `ValueError` for invalid numbers.
     - Initializes the 3 pegs and resets the move counter.
   - `move(self, from_peg: int, to_peg: int) -> None`:
     - Moves a single disk from `from_peg` to `to_peg`.
     - Validates the move:
       - Peg numbers must be within valid range (0, 1, 2).
       - Source peg must not be empty.
       - A larger disk cannot be placed on top of a smaller disk.
       - Source and destination pegs must be different.
     - Raises a custom exception `InvalidMoveError` if the move violates any rules.
     - Updates `move_count` on successful move.
   - `get_valid_moves(self) -> list[tuple[int, int]]`:
     - Returns a list of all `(from_peg, to_peg)` move pairs that are currently legal.
   - `get_state(self) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]`:
     - Returns a hashable, immutable representation of the pegs' disks.
     - This is required for search algorithms and reinforcement learning state tracking.
   - `is_solved(self) -> bool`:
     - Returns `True` if all $N$ disks are located on Peg 2.
   - `reset(self) -> None`:
     - Resets the board back to the initial state (all disks on Peg 0) and resets `move_count` to 0.

3. **Exception Handling**:
   - A custom exception `InvalidMoveError` inheriting from `ValueError` to distinguish game rule violations from standard program errors.

4. **Testing**:
   - Comprehensive unit tests in `tests/test_game.py` covering:
     - Board initialization and constraints.
     - Valid and invalid moves (and verifying `InvalidMoveError` is raised).
     - State tracking, `get_valid_moves`, and `get_state`.
     - Game resolution / winning state check.
     - Game reset behavior.

## Out of Scope

- No FastAPI routing, HTTP endpoints, or request handling for game state (Phase 4/5).
- No database tables, logging moves to SQLite, or database models (Phase 3).
- No frontend representation, CSS styling, or JavaScript drag-and-drop mechanics (Phase 4).
- No solver algorithms like Recursion, A* Search, or Reinforcement Learning (Phases 5, 6, and 7).

## Design Decisions

### State Data Structure
- Under the hood, `pegs` will be represented internally as a list of three lists: `list[list[int]]`.
- To represent disks on a peg, the end of the list represents the top of the stack. For example, if $N=3$, peg 0 begins as `[3, 2, 1]`. Moving the top disk (size 1) to peg 1 results in peg 0 being `[3, 2]` and peg 1 being `[1]`.
- Using list operations (like `pop()` and `append()`) provides efficient and standard Pythonic stack manipulation.

### State Hashing
- `get_state` returns a tuple of tuples: `tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]`.
- This ensures the state is immutable, comparable, and hashable. It can be directly used as dictionary keys (for Q-tables in Phase 7) or nodes in a graph search (for A* search in Phase 6).

### Custom Exception
- Using `InvalidMoveError` instead of generic `ValueError` allows callers to specifically intercept rule violations and display appropriate messages to users or guide agents cleanly.

## Context

Phase 2 builds the core computational model. By separation of concerns, the core game engine contains no web or DB dependencies. This ensures it is 100% testable in a CLI/unit test environment.

## Stakeholder Notes

- **Mary** emphasizes that `get_state` must return a hashable type, as subsequent phases (A* search and Q-learning) rely heavily on state comparisons and caching.
- **Steve** wants the API to be extremely intuitive so it can be easily mapped to drag-and-drop events in the UI later.
