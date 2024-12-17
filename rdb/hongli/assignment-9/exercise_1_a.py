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

    # Your solution goes here.
    # debugging
    # print(hypercube)
    # print(array)
    # print(d)

    array_index = 0
    fill_cube(array_index, array, hypercube, d)

    return


# fill the cube recursively
def fill_cube(
                array_index: int,
                array: list[int],
                hypercube: Hypercube,
                d: list[int]):
    for i in range(d[-1]):
        if len(d) == 1:
            # we reached the last dimension
            hypercube[i + 1] = array[array_index + 1]
            array_index += 1
        else:
            # otherwise go deeper
            array_index = \
                    fill_cube(array_index, array, hypercube[i + 1], d[:-1])

    return array_index
