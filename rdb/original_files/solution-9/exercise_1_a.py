from typing import Any

Hypercube = list[Any]


def array2hypercube(array: list[int], hypercube: Hypercube, d: list[int]) -> None:
    # For your convenience, the array and hypercube are padded with a leading
    # unused value of 666, so you can use 1-based indexing as in the lecture.
    # The dimensions `d` use 0-based indexing as usual, but if you prefer,
    # you can also use 1-based indexing with d = ["unused"] + d.
    # The hypercube is given as a list of lists of lists of lists ... and so on
    # until the last dimension, which is a list of integers. Technically,
    # this is not really a hypercube, since the sides can have different length,
    # but the term "hyperrectangle" never really caught on.

    # BEGIN_SOLTUION
    convert(hypercube, array, d, True)

    # Alternative solution
    """
    import itertools

    counter = 1
    ranges = [range(1, di + 1) for di in reversed(d)]
    for indices in itertools.product(*ranges):
        row = hypercube
        for i in range(len(indices) - 1):
            row = row[indices[i]]
        row[indices[-1]] = array[counter]
        counter += 1
    """


def index(x: list[int], d: list[int]) -> int:
    # Compute index as seen in lecture 3
    idx = x[-1]

    for i in range(len(x) - 2, -1, -1):
        idx = x[i] + (idx - 1) * d[i]

    return idx


def convert(
    hypercube: Hypercube, array: list[int], d: list[int], array2cube: bool
) -> None:
    # Convert an array to hypercube or the other way round

    # Technically, the index function is not really needed since we can access
    # all values sequentially, but it would be necessary if we wanted to access
    # individual values at random coordinates in the cube.

    # Have to reverse d because itertools.product is iterating over the last dimension first
    import itertools

    ranges = [range(1, 1 + di) for di in reversed(d)]
    for x in itertools.product(*ranges):

        idx = index(list(x[::-1]), d)

        # Find deepest array in hypercube
        current = hypercube
        for i in range(len(d) - 1):
            current = current[x[i]]

        if array2cube:
            current[x[-1]] = array[idx]
        else:
            array[idx] = current[x[-1]]
    # END_SOLUTION
