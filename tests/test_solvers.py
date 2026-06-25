from game import HanoiGame
from solvers.classic import solve_iterative, solve_recursive


def test_recursive_solver_correctness() -> None:
    # Test with 3 disks (odd number of disks)
    moves_3 = solve_recursive(3)
    assert len(moves_3) == 7

    game_3 = HanoiGame(3)
    for move in moves_3:
        game_3.move(move["from_peg"], move["to_peg"])
    assert game_3.is_solved()

    # Test with 4 disks (even number of disks)
    moves_4 = solve_recursive(4)
    assert len(moves_4) == 15

    game_4 = HanoiGame(4)
    for move in moves_4:
        game_4.move(move["from_peg"], move["to_peg"])
    assert game_4.is_solved()


def test_iterative_solver_correctness() -> None:
    # Test with 3 disks
    moves_3 = solve_iterative(3)
    assert len(moves_3) == 7

    game_3 = HanoiGame(3)
    for move in moves_3:
        game_3.move(move["from_peg"], move["to_peg"])
    assert game_3.is_solved()

    # Test with 4 disks
    moves_4 = solve_iterative(4)
    assert len(moves_4) == 15

    game_4 = HanoiGame(4)
    for move in moves_4:
        game_4.move(move["from_peg"], move["to_peg"])
    assert game_4.is_solved()


def test_solvers_empty_or_invalid() -> None:
    assert solve_recursive(0) == []
    assert solve_recursive(-1) == []
    assert solve_iterative(0) == []
    assert solve_iterative(-1) == []
