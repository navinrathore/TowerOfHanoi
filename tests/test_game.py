import pytest

from game import HanoiGame, InvalidMoveError


def test_game_initialization() -> None:
    # Test valid initialization
    game = HanoiGame(3)
    assert game.num_disks == 3
    assert game.move_count == 0
    assert game.pegs == [[3, 2, 1], [], []]
    assert not game.is_solved()

    # Test parameter validation bounds
    with pytest.raises(ValueError, match="must be between 3 and 8"):
        HanoiGame(2)
    with pytest.raises(ValueError, match="must be between 3 and 8"):
        HanoiGame(9)


def test_valid_move() -> None:
    game = HanoiGame(3)
    game.move(0, 1)
    assert game.pegs == [[3, 2], [1], []]
    assert game.move_count == 1

    game.move(0, 2)
    assert game.pegs == [[3], [1], [2]]
    assert game.move_count == 2


def test_invalid_moves() -> None:
    game = HanoiGame(3)
    # Moving from empty peg
    with pytest.raises(InvalidMoveError, match="empty"):
        game.move(1, 2)

    # Moving to same peg
    with pytest.raises(InvalidMoveError, match="different"):
        game.move(0, 0)

    # Placing larger disk on smaller disk
    game.move(0, 1)  # Move 1 to peg 1
    # State is [[3, 2], [1], []]
    # Try to move 2 to peg 1 (where 1 is)
    with pytest.raises(InvalidMoveError, match="smaller disk"):
        game.move(0, 1)

    # Invalid peg index
    with pytest.raises(InvalidMoveError, match="Invalid peg selection"):
        game.move(-1, 0)
    with pytest.raises(InvalidMoveError, match="Invalid peg selection"):
        game.move(0, 3)


def test_get_valid_moves() -> None:
    game = HanoiGame(3)
    # Initial state: [[3, 2, 1], [], []]
    # Allowed moves: size 1 disk from peg 0 to peg 1 or 2
    assert set(game.get_valid_moves()) == {(0, 1), (0, 2)}

    # Move 1 to peg 1
    game.move(0, 1)  # State: [[3, 2], [1], []]
    # Top of 0 is 2. Top of 1 is 1. Top of 2 is None (empty).
    # Allowed:
    # 2 can move to empty peg 2: (0, 2)
    # 1 can move to peg 0 (top 2 > 1): (1, 0)
    # 1 can move to peg 2 (empty): (1, 2)
    assert set(game.get_valid_moves()) == {(0, 2), (1, 0), (1, 2)}


def test_get_state_immutability() -> None:
    game = HanoiGame(3)
    state = game.get_state()
    assert state == ((3, 2, 1), (), ())

    # Verify state is hashable
    d = {state: "initial"}
    assert d[state] == "initial"

    # Verify mutating game doesn't mutate previously returned state tuple
    game.move(0, 1)
    assert state == ((3, 2, 1), (), ())
    assert game.get_state() == ((3, 2), (1,), ())


def test_is_solved() -> None:
    game = HanoiGame(3)
    assert not game.is_solved()

    # Manually configure a solved state
    game.pegs = [[], [], [3, 2, 1]]
    assert game.is_solved()

    # Verify not solved if disks are on peg 1
    game.pegs = [[], [3, 2, 1], []]
    assert not game.is_solved()


def test_reset() -> None:
    game = HanoiGame(3)
    game.move(0, 1)
    game.move(0, 2)
    assert game.move_count == 2
    assert game.pegs != [[3, 2, 1], [], []]

    game.reset()
    assert game.move_count == 0
    assert game.pegs == [[3, 2, 1], [], []]
    assert game.get_state() == ((3, 2, 1), (), ())
