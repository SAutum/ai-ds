from typing import Any

Hypercube = list[Any]


def hypercube2array(hypercube: Hypercube, array: list[int], d: list[int]) -> None:
    # Your solution goes here.
    array_index = 0
    fill_array(array_index, array, hypercube, d)

    return


def fill_array(
                array_index: int,
                array: list[int],
                hypercube: Hypercube,
                d: list[int]):
    # exact the opposite update
    for i in range(d[-1]):
        if len(d) == 1:
            # we reached the last dimension
            # change the assignment arrow as oppose to fill cube
            array[array_index + 1] = hypercube[i + 1]
            array_index += 1
        else:
            # otherwise go deeper
            array_index = \
                    fill_array(array_index, array, hypercube[i + 1], d[:-1])

    return array_index
