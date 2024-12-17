from typing import Any

Hypercube = list[Any]


def extract_subcube(
    hypercube: Hypercube,
    d: list[int],
    x_min: list[int],
    x_max: list[int],
    subcube: Hypercube,
) -> None:
    # BEGIN_SOLUTION

    # Alternative recursive solution without indices
    """
    nx = x_max[-1] - x_min[-1] + 1

    if len(d) == 1:
        # Copy nx ints if the hypercube is 1-dimensional
        subcube[1:1 + nx] = hypercube[x_min[-1]:x_min[-1] + nx]
    else:
        # Recursively copy nx subcubes
        for x in range(nx):
            extract_subcube(hypercube[x_min[-1] + x],
                d[:-1], x_min[:-1], x_max[:-1], subcube[1 + x])
    """
    import itertools

    # Iterate over range of subcube
    x_min, x_max = x_min[::-1], x_max[::-1]
    ranges = [range(a, b + 1) for a, b in zip(x_min, x_max)]
    for x in itertools.product(*ranges):
        # Find deepest array in hypercube
        current = hypercube
        for i in range(len(d) - 1):
            current = current[x[i]]
        value = current[x[-1]]

        # Update deepest array in subcube
        current = subcube
        for i in range(len(d) - 1):
            current = current[x[i] - x_min[i] + 1]
        current[x[-1] - x_min[-1] + 1] = value
    # END_SOLUTION
