"""Path class for protein folding conformations."""

from dataclasses import dataclass
from typing import List


@dataclass
class Path:
    """
    Represents a path as a sequence of moves on a lattice.

    Each move is an integer index corresponding to a basis direction
    in the lattice's canonical indexing scheme.

    Attributes:
        moves: List of integer indices representing moves in the
              canonical basis direction order of the lattice.
    """

    moves: List[int]

    def __post_init__(self) -> None:
        """
        Validate the path after initialization.

        Raises:
            ValueError: If moves contains invalid values (e.g., negative
                       indices).
        """
        if not isinstance(self.moves, list):
            raise TypeError("moves must be a list")
        if not all(isinstance(move, int) for move in self.moves):
            raise TypeError("All moves must be integers")
        if any(move < 0 for move in self.moves):
            raise ValueError("Move indices must be non-negative")

