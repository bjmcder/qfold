"""Conformation module for lattice and path representations."""

from qfold.conformation.conformation import Conformation
from qfold.conformation.lattice import (
    HexagonalLattice,
    Lattice,
    SquareLattice,
    TriangularLattice,
)
from qfold.conformation.path import Path

__all__ = [
    "Conformation",
    "HexagonalLattice",
    "Lattice",
    "Path",
    "SquareLattice",
    "TriangularLattice",
]

