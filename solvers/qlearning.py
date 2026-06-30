import random
import time
from typing import Any, Union, Callable, Optional

# Directed move actions (from_peg, to_peg)
ACTIONS = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]


def state_to_string(
    pegs: Union[list[list[int]], tuple[tuple[int, ...], ...]], num_disks: int
) -> str:
    """Convert a Hanoi peg state representation to a compact string.

    The string is of length num_disks, where the i-th character represents
    the peg index (0, 1, or 2) of disk i+1 (from smallest to largest).
    """
    disk_pegs = [0] * num_disks
    for peg_idx, peg in enumerate(pegs):
        for disk in peg:
            if 1 <= disk <= num_disks:
                disk_pegs[disk - 1] = peg_idx
    return "".join(map(str, disk_pegs))


def string_to_pegs(state_str: str, num_disks: int) -> list[list[int]]:
    """Convert a compact state string back to peg stacks.

    Returns:
        A list of three lists, representing disk stacks on each peg.
    """
    pegs: list[list[int]] = [[], [], []]
    # Build pegs from largest disk (num_disks) down to smallest (1)
    # so they are ordered bottom-to-top correctly.
    for disk in range(num_disks, 0, -1):
        peg_idx = int(state_str[disk - 1])
        pegs[peg_idx].append(disk)
    return pegs


def step_state(
    state_str: str, action: tuple[int, int], num_disks: int
) -> tuple[str, bool, float]:
    """Transition state given an action.

    Args:
        state_str: Current state string.
        action: Move action tuple (from_peg, to_peg).
        num_disks: Number of disks in play.

    Returns:
        A tuple of (next_state_str, is_valid, reward)
    """
    from_peg, to_peg = action
    pegs = string_to_pegs(state_str, num_disks)

    # 1. Invalid move: source peg is empty
    if not pegs[from_peg]:
        return state_str, False, -10.0

    moving_disk = pegs[from_peg][-1]

    # 2. Invalid move: placing larger disk on smaller disk
    if pegs[to_peg] and pegs[to_peg][-1] < moving_disk:
        return state_str, False, -10.0

    # 3. Valid move execution
    pegs[from_peg].pop()
    pegs[to_peg].append(moving_disk)

    next_state_str = state_to_string(pegs, num_disks)

    # Solve condition check
    is_solved = next_state_str == "2" * num_disks
    reward = 100.0 if is_solved else -1.0

    return next_state_str, True, reward


class QLearningAgent:
    """Tabular Q-learning agent for solving the Tower of Hanoi."""

    def __init__(self, num_disks: int) -> None:
        """Initialize the Q-learning agent for a specific number of disks."""
        self.num_disks: int = num_disks
        self.ACTIONS: list[tuple[int, int]] = ACTIONS
        # Mapping: state_str -> {action: Q-value}
        self.q_table: dict[str, dict[tuple[int, int], float]] = {}

    def get_q_values(self, state_str: str) -> dict[tuple[int, int], float]:
        """Retrieve or initialize Q-values for a state."""
        if state_str not in self.q_table:
            self.q_table[state_str] = {a: 0.0 for a in self.ACTIONS}
        return self.q_table[state_str]

    def choose_action(self, state_str: str, epsilon: float) -> tuple[int, int]:
        """Choose an action using epsilon-greedy strategy."""
        if random.random() < epsilon:
            return random.choice(self.ACTIONS)

        q_vals = self.get_q_values(state_str)
        max_q = max(q_vals.values())
        # Break ties randomly to ensure thorough exploration
        best_actions = [a for a, q in q_vals.items() if q == max_q]
        return random.choice(best_actions)

    def train(
        self,
        episodes: int = 1000,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.2,
        min_epsilon: float = 0.01,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> dict[str, Any]:
        """Train the Q-agent.

        Args:
            episodes: Number of episodes to train.
            alpha: Learning rate.
            gamma: Discount factor.
            epsilon: Starting exploration rate.
            min_epsilon: Minimum exploration rate.
            progress_callback: Optional callback receiving float progress (0.0 to 1.0).

        Returns:
            Dictionary containing metrics and metadata about training progress.
        """
        start_time = time.time()

        episode_rewards: list[float] = []
        episode_steps: list[int] = []
        episode_success: list[int] = []

        initial_state = "0" * self.num_disks
        goal_state = "2" * self.num_disks

        # Exponential decay to hit min_epsilon around 85% of training
        decay_steps = max(1, int(episodes * 0.85))
        decay_factor = (
            (min_epsilon / epsilon) ** (1.0 / decay_steps)
            if epsilon > min_epsilon
            else 1.0
        )
        current_epsilon = epsilon

        # Maximum steps per episode to prevent endless loops in early exploration
        max_steps = 100 + 25 * self.num_disks

        for episode in range(episodes):
            state = initial_state
            total_reward = 0.0
            steps = 0
            done = False

            while not done and steps < max_steps:
                action = self.choose_action(state, current_epsilon)
                next_state, is_valid, reward = step_state(state, action, self.num_disks)

                # Q-learning Bellman update
                q_vals = self.get_q_values(state)
                next_q_vals = self.get_q_values(next_state)
                max_next_q = max(next_q_vals.values())

                q_vals[action] += alpha * (reward + gamma * max_next_q - q_vals[action])

                state = next_state
                total_reward += reward
                steps += 1

                if state == goal_state:
                    done = True

            # Epsilon decay
            if current_epsilon > min_epsilon:
                current_epsilon *= decay_factor

            episode_rewards.append(total_reward)
            episode_steps.append(steps)
            episode_success.append(1 if done else 0)

            # Report progress via callback
            if progress_callback and (episode % max(1, episodes // 100) == 0 or episode == episodes - 1):
                progress_callback(float(episode + 1) / episodes)

        end_time = time.time()
        training_time_ms = (end_time - start_time) * 1000

        # Downsample metrics into 50 clean bins for UI visualization
        num_bins = min(50, episodes)
        bin_size = max(1, episodes // num_bins)

        binned_rewards = []
        binned_steps = []
        binned_success = []
        binned_epsilons = []

        for i in range(0, len(episode_rewards), bin_size):
            chunk_rewards = episode_rewards[i : i + bin_size]
            chunk_steps = episode_steps[i : i + bin_size]
            chunk_success = episode_success[i : i + bin_size]

            # Approximate decayed epsilon at this step
            approx_epsilon = epsilon * (
                decay_factor ** min(episodes - 1, i + bin_size // 2)
            )
            approx_epsilon = max(min_epsilon, approx_epsilon)

            binned_rewards.append(sum(chunk_rewards) / len(chunk_rewards))
            binned_steps.append(sum(chunk_steps) / len(chunk_steps))
            binned_success.append(sum(chunk_success) / len(chunk_success))
            binned_epsilons.append(approx_epsilon)

        final_success_rate = (
            sum(episode_success[-100:]) / min(100, len(episode_success))
            if episode_success
            else 0.0
        )

        return {
            "num_disks": self.num_disks,
            "episodes": episodes,
            "training_time_ms": training_time_ms,
            "final_success_rate": final_success_rate,
            "metrics": {
                "episodes": [i * bin_size for i in range(len(binned_rewards))],
                "avg_rewards": binned_rewards,
                "avg_steps": binned_steps,
                "success_rates": binned_success,
                "epsilons": binned_epsilons,
            },
        }

    def solve(self, start_state_str: str) -> list[dict[str, int]]:
        """Find the solution sequence from any start state using the Q-table policy.

        Falls back to A* search if the policy gets stuck, goes in cycles,
        or hits unvisited states.
        """
        moves: list[dict[str, int]] = []
        state = start_state_str
        goal_state = "2" * self.num_disks
        visited = {state}

        # Allow at most 2^N + 50 moves to prevent infinite loops
        limit = (1 << self.num_disks) + 50

        while state != goal_state and len(moves) < limit:
            q_vals = self.q_table.get(state)
            if not q_vals:
                # Unvisited state, fallback to A* pathfinder
                break

            # Sort actions by Q-value descending
            sorted_actions = sorted(q_vals.items(), key=lambda x: x[1], reverse=True)

            best_action = None
            for action, q_val in sorted_actions:
                next_state, is_valid, _ = step_state(state, action, self.num_disks)
                # Ensure move is valid and state was not visited in this solve path
                if is_valid and next_state not in visited:
                    # Valid move with a learned Q-value (exclude invalid penalty values)
                    if q_val > -9.0:
                        best_action = action
                        state = next_state
                        visited.add(state)
                        break

            if not best_action:
                # Trap/cycle or untargeted state, fallback to A*
                break

            from_peg, to_peg = best_action
            moves.append({"from_peg": from_peg, "to_peg": to_peg})

        # Fallback implementation
        if state != goal_state:
            pegs = string_to_pegs(state, self.num_disks)
            peg_tuple = tuple(tuple(peg) for peg in pegs)
            from solvers.search import solve_search

            remaining_moves = solve_search(self.num_disks, start_state=peg_tuple)
            moves.extend(remaining_moves)

        return moves
