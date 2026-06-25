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


def test_search_solver_correctness() -> None:
    from solvers.search import solve_search

    # Test A* search with 3 disks (standard start state)
    moves_3 = solve_search(3)
    assert len(moves_3) == 7

    game_3 = HanoiGame(3)
    for move in moves_3:
        game_3.move(move["from_peg"], move["to_peg"])
    assert game_3.is_solved()

    # Test A* search with custom intermediate state
    # Starting state: disk 3 & 2 on Peg 0, disk 1 on Peg 1
    # Standard optimal first move for 3 disks moves disk 1 to Peg 2.
    # But if disk 1 is on Peg 1, it's a valid intermediate state.
    start_state = ((3, 2), (1,), ())
    moves_int = solve_search(3, start_state=start_state)
    
    # Path to win from this state:
    # move 2 to 2 (impossible since 1 is on 1), wait:
    # 1 to 2, 2 to 1 (no, 3 and 2 are on 0, 1 is on 1)
    # let's verify that playing search solver moves solves it:
    game_int = HanoiGame(3)
    game_int.pegs = [list(peg) for peg in start_state]
    for move in moves_int:
        game_int.move(move["from_peg"], move["to_peg"])
    assert game_int.is_solved()


def test_qlearning_utilities_and_agent() -> None:
    from solvers.qlearning import (
        QLearningAgent,
        state_to_string,
        string_to_pegs,
        step_state,
    )

    # 1. Test state representation string translations
    pegs = [[3, 2], [1], []]
    state_str = state_to_string(pegs, 3)
    assert state_str == "100"  # disk 1 on peg 1, disk 2 on peg 0, disk 3 on peg 0

    decoded_pegs = string_to_pegs("100", 3)
    assert decoded_pegs == [[3, 2], [1], []]

    # 2. Test Q-learning state step transitions
    # move disk 1 from peg 1 to peg 2 (valid)
    next_state, is_valid, reward = step_state("100", (1, 2), 3)
    assert is_valid is True
    assert next_state == "200"
    assert reward == -1.0

    # move disk 2 from peg 0 to peg 1 (invalid since disk 1 is on peg 1, and 1 < 2)
    next_state_inv, is_valid_inv, reward_inv = step_state("100", (0, 1), 3)
    assert is_valid_inv is False
    assert next_state_inv == "100"
    assert reward_inv == -10.0

    # 3. Test Q-learning training and solving (3 disks)
    agent = QLearningAgent(3)
    train_results = agent.train(episodes=500, alpha=0.1, gamma=0.9, epsilon=0.2)
    assert train_results["num_disks"] == 3
    assert train_results["episodes"] == 500
    assert "training_time_ms" in train_results

    # Solve from initial state
    solution = agent.solve("000")
    assert len(solution) > 0
    
    # Verify solution solves the game
    game = HanoiGame(3)
    for move in solution:
        game.move(move["from_peg"], move["to_peg"])
    assert game.is_solved()

