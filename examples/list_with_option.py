from obey import command
from typing import Optional, Literal
from math import sqrt


@command
def vector_norm(coords: list[float], norm: Optional[Literal["l1", "l2"]] = "l2"):
    """
    Calculates vector norm
    """
    if norm == "l1":
        return sum([abs(x) for x in coords])
    elif norm == "l2":
        return sqrt(sum([x**2 for x in coords]))

    return 0
