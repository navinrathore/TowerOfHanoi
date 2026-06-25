def solve_recursive(
    num_disks: int, from_peg: int = 0, to_peg: int = 2, aux_peg: int = 1
) -> list[dict[str, int]]:
    """Solve the Tower of Hanoi problem using recursion.

    Args:
        num_disks: Number of disks.
        from_peg: Source peg index.
        to_peg: Destination peg index.
        aux_peg: Auxiliary peg index.

    Returns:
        List of moves as dictionaries with 'from_peg' and 'to_peg'.
    """
    moves: list[dict[str, int]] = []

    def _helper(n: int, src: int, dst: int, aux: int) -> None:
        if n == 1:
            moves.append({"from_peg": src, "to_peg": dst})
            return
        _helper(n - 1, src, aux, dst)
        moves.append({"from_peg": src, "to_peg": dst})
        _helper(n - 1, aux, dst, src)

    if num_disks > 0:
        _helper(num_disks, from_peg, to_peg, aux_peg)
    return moves


def solve_iterative(
    num_disks: int, from_peg: int = 0, to_peg: int = 2, aux_peg: int = 1
) -> list[dict[str, int]]:
    """Solve the Tower of Hanoi problem iteratively.

    Args:
        num_disks: Number of disks.
        from_peg: Source peg index.
        to_peg: Destination peg index.
        aux_peg: Auxiliary peg index.

    Returns:
        List of moves as dictionaries with 'from_peg' and 'to_peg'.
    """
    if num_disks <= 0:
        return []

    pegs: list[list[int]] = [[] for _ in range(3)]
    # Initialize the starting peg with disks from largest to smallest
    pegs[from_peg] = list(range(num_disks, 0, -1))

    total_moves = 2**num_disks - 1
    moves: list[dict[str, int]] = []

    src = from_peg
    dst = to_peg
    aux = aux_peg

    # If the number of disks is even, swap the destination and auxiliary pegs
    if num_disks % 2 == 0:
        dst, aux = aux, dst

    def get_legal_move(p1: int, p2: int) -> tuple[int, int]:
        if not pegs[p1]:
            return p2, p1
        if not pegs[p2]:
            return p1, p2
        if pegs[p1][-1] < pegs[p2][-1]:
            return p1, p2
        return p2, p1

    for i in range(1, total_moves + 1):
        mod = i % 3
        if mod == 1:
            u, v = get_legal_move(src, dst)
        elif mod == 2:
            u, v = get_legal_move(src, aux)
        else:
            u, v = get_legal_move(aux, dst)

        disk = pegs[u].pop()
        pegs[v].append(disk)
        moves.append({"from_peg": u, "to_peg": v})

    return moves
