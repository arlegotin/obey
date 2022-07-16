"""
This module performs operations on vectors
"""

from obey import command
from typing import Optional, Literal
from math import sqrt


@command
@command.help("norm", "l1 for Manhattan, l2 for Euclidean, max for max")
def norm(
    coords: list[float], norm: Optional[Literal["l1", "l2", "max"]] = "l2"
) -> float:
    """
    Calculates vector norm
    """
    if norm == "l1":
        return sum([abs(x) for x in coords])
    elif norm == "l2":
        return sqrt(sum([x**2 for x in coords]))
    elif norm == "max":
        return max([abs(x) for x in coords])

    raise ValueError(f'Unknown norm "{norm}"')


@command
def dot_product(a: Optional[list[float]], b: Optional[list[float]]):
    """
    Calculates dot-product of two vectors
    """
    if len(a) != len(b):
        raise ValueError(f"Vectors should have same dimensions")

    return sum([x * y for x, y in zip(a, b)])


@command
def vector_product(a: tuple[float, float, float], b: tuple[float, float, float]):
    """
    Calculates vector product of two 3D-vectors
    """
    a1, a2, a3 = a
    b1, b2, b3 = b

    c = [a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1]

    return c
