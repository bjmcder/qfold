"""Conformation class for protein folding conformations."""

import numpy as np

from qfold.conformation.lattice import Lattice
from qfold.conformation.path import Path


class Conformation:
    """
    Represents a conformation as a path mapped to a lattice.

    A conformation combines a Path (sequence of moves) with a Lattice
    (structure definition) to represent a specific protein folding
    conformation.

    Attributes:
        path: The Path object representing the sequence of moves.
        lattice: The Lattice object defining the structure.
    """

    def __init__(self, path: Path, lattice: Lattice) -> None:
        """
        Initialize a conformation from a path and lattice.

        Args:
            path: Path object containing the sequence of moves.
            lattice: Lattice object defining the structure.

        Raises:
            TypeError: If path or lattice are not of the correct types.
        """
        if not isinstance(path, Path):
            raise TypeError("path must be a Path instance")
        if not isinstance(lattice, Lattice):
            raise TypeError("lattice must be a Lattice instance")

        self.path = path
        self.lattice = lattice

    def __repr__(self) -> str:
        """
        Return string representation of the conformation.

        Returns:
            String representation showing path and lattice information.
        """
        return (
            f"Conformation(path={self.path!r}, "
            f"lattice={type(self.lattice).__name__})"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another conformation.

        Args:
            other: Object to compare with.

        Returns:
            True if both path and lattice are equal, False otherwise.
        """
        if not isinstance(other, Conformation):
            return False
        # Compare paths
        if self.path != other.path:
            return False
        # Compare lattices by type and basis vectors to avoid
        # lattpy.Lattice.__eq__ issues with uninitialized lattices
        if type(self.lattice) != type(other.lattice):
            return False
        if self.lattice.dimension != other.lattice.dimension:
            return False
        if not np.array_equal(
            self.lattice.basis_vectors, other.lattice.basis_vectors
        ):
            return False
        return True

