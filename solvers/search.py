from __future__ import annotations
import heapq


def compute_hanoi_distance(
    state: tuple[tuple[int, ...], ...], target_peg: int = 2
) -> int:
    """Compute the exact minimum number of moves to reach the goal state
    where all disks are on the target peg.

    This runs in O(N) where N is the number of disks, using the recurrence
    relations of the Tower of Hanoi graph.

    Args:
        state: A tuple of three tuples representing the disks on Peg 0, 1, and 2.
        target_peg: The peg index where all disks should end up (usually 2).

    Returns:
        The exact shortest path distance (minimum number of moves) to the goal.
    """
    # Count total disks
    num_disks = sum(len(peg) for peg in state)
    if num_disks == 0:
        return 0

    # Map disk size to its current peg index
    disk_peg: dict[int, int] = {}
    for peg_idx, peg in enumerate(state):
        for disk in peg:
            disk_peg[disk] = peg_idx

    # Recursive distance calculation from largest disk down to 1
    def get_dist(d: int, target: int) -> int:
        if d == 0:
            return 0
        current_peg = disk_peg.get(d)
        if current_peg is None:
            # Safe fallback if disk size is missing or invalid
            return 0

        if current_peg == target:
            return get_dist(d - 1, target)
        else:
            # The auxiliary peg is the one that is neither current_peg nor target
            aux = 3 - current_peg - target
            return get_dist(d - 1, aux) + (1 << (d - 1))

    return get_dist(num_disks, target_peg)


from typing import Optional

def solve_search(
    num_disks: int, start_state: Optional[tuple[tuple[int, ...], ...]] = None
) -> list[dict[str, int]]:
    """Solve the Tower of Hanoi problem using A* pathfinding from any start state.

    Args:
        num_disks: Number of disks.
        start_state: Optional start state. If None, defaults to the standard
                     initial configuration where all disks are on Peg 0.

    Returns:
        List of moves as dictionaries with 'from_peg' and 'to_peg'.
    """
    if num_disks <= 0:
        return []

    # 1. Establish the start state if not provided
    if start_state is None:
        start_state = (
            tuple(range(num_disks, 0, -1)),
            (),
            (),
        )

    # 2. Check if already solved
    # A state is solved when all num_disks are on Peg 2
    if len(start_state[2]) == num_disks:
        return []

    # 3. A* Search Initialization
    # Element: (f_score, tie_breaker, state, path)
    tie_breaker = 0
    start_h = compute_hanoi_distance(start_state, target_peg=2)

    # Priority Queue
    pq: list[tuple[int, int, tuple[tuple[int, ...], ...], list[dict[str, int]]]] = [
        (start_h, tie_breaker, start_state, [])
    ]

    # Keep track of minimum g_score to reach each state
    g_scores: dict[tuple[tuple[int, ...], ...], int] = {start_state: 0}

    while pq:
        f_score, _, current_state, path = heapq.heappop(pq)

        # Check goal condition
        if len(current_state[2]) == num_disks:
            return path

        # If we popped a state that has a better path recorded already, skip it
        current_g = g_scores.get(current_state, float("inf"))
        if len(path) > current_g:
            continue

        # Explore neighbors
        for from_peg in range(3):
            peg_from = current_state[from_peg]
            if not peg_from:
                continue

            top_disk = peg_from[-1]
            for to_peg in range(3):
                if from_peg == to_peg:
                    continue

                peg_to = current_state[to_peg]
                # Valid move if destination is empty or top disk is larger
                if not peg_to or peg_to[-1] > top_disk:
                    # Construct neighbor state
                    new_pegs = list(current_state)
                    new_pegs[from_peg] = peg_from[:-1]
                    new_pegs[to_peg] = (*peg_to, top_disk)
                    neighbor_state = tuple(new_pegs)

                    new_g = len(path) + 1
                    if (
                        neighbor_state not in g_scores
                        or new_g < g_scores[neighbor_state]
                    ):
                        g_scores[neighbor_state] = new_g
                        h = compute_hanoi_distance(neighbor_state, target_peg=2)
                        new_f = new_g + h
                        tie_breaker += 1

                        heapq.heappush(
                            pq,
                            (
                                new_f,
                                tie_breaker,
                                neighbor_state,
                                [*path, {"from_peg": from_peg, "to_peg": to_peg}],
                            ),
                        )

    return []
