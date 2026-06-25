class InvalidMoveError(ValueError):
    """Raised when a move violates the Tower of Hanoi rules."""

    pass


class HanoiGame:
    """Core game engine for the Tower of Hanoi puzzle."""

    def __init__(self, num_disks: int = 3) -> None:
        """Initialize the game with a specified number of disks.

        Args:
            num_disks: The number of disks (must be between 3 and 8 inclusive).

        Raises:
            ValueError: If num_disks is not within the valid range.
        """
        if not (3 <= num_disks <= 8):
            raise ValueError("Number of disks must be between 3 and 8 inclusive.")

        self.num_disks: int = num_disks
        self.move_count: int = 0
        # Initialize pegs: peg 0 has all disks from num_disks down to 1
        # peg 1 is empty, peg 2 is empty
        self.pegs: list[list[int]] = [
            list(range(num_disks, 0, -1)),
            [],
            [],
        ]

    def reset(self) -> None:
        """Reset the game to the initial state."""
        self.move_count = 0
        self.pegs = [
            list(range(self.num_disks, 0, -1)),
            [],
            [],
        ]

    def get_state(self) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        """Return a hashable, immutable representation of the pegs' state.

        Returns:
            A tuple of three tuples, each representing the disks on a peg
            from bottom to top.
        """
        return (
            tuple(self.pegs[0]),
            tuple(self.pegs[1]),
            tuple(self.pegs[2]),
        )

    def is_solved(self) -> bool:
        """Check if the game is successfully solved.

        The game is solved when all disks are placed on Peg 2.

        Returns:
            True if all disks are on Peg 2, False otherwise.
        """
        return len(self.pegs[2]) == self.num_disks

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Find all legally allowed moves from the current state.

        Returns:
            A list of (from_peg, to_peg) tuples.
        """
        valid_moves: list[tuple[int, int]] = []
        for from_peg in range(3):
            if not self.pegs[from_peg]:
                continue
            top_disk = self.pegs[from_peg][-1]
            for to_peg in range(3):
                if from_peg == to_peg:
                    continue
                # Valid if destination peg is empty, or has a larger top disk
                if not self.pegs[to_peg] or self.pegs[to_peg][-1] > top_disk:
                    valid_moves.append((from_peg, to_peg))
        return valid_moves

    def move(self, from_peg: int, to_peg: int) -> None:
        """Move a single disk from one peg to another.

        Args:
            from_peg: Source peg index (0, 1, or 2).
            to_peg: Destination peg index (0, 1, or 2).

        Raises:
            InvalidMoveError: If the move is invalid under Tower of Hanoi rules.
        """
        if from_peg not in (0, 1, 2) or to_peg not in (0, 1, 2):
            raise InvalidMoveError(
                f"Invalid peg selection: from_peg={from_peg}, to_peg={to_peg}. "
                "Pegs must be 0, 1, or 2."
            )
        if from_peg == to_peg:
            raise InvalidMoveError("Source and destination pegs must be different.")
        if not self.pegs[from_peg]:
            raise InvalidMoveError(f"Source peg {from_peg} is empty.")

        disk_to_move = self.pegs[from_peg][-1]

        if self.pegs[to_peg] and self.pegs[to_peg][-1] < disk_to_move:
            raise InvalidMoveError(
                f"Cannot place disk of size {disk_to_move} on top of a smaller disk "
                f"of size {self.pegs[to_peg][-1]}."
            )

        # Execute move
        self.pegs[from_peg].pop()
        self.pegs[to_peg].append(disk_to_move)
        self.move_count += 1
