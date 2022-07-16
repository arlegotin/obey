from obey import command


@command
def vector_product(a: tuple[float, float, float], b: tuple[float, float, float]):
    """
    Calculates vector product of two vectors
    """
    a1, a2, a3 = a
    b1, b2, b3 = b

    c = [a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1]

    return f"a × b = {c}"
