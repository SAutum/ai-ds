from typing import Any

Hypercube = list[Any]


def hypercube2array(hypercube: Hypercube, array: list[int], d: list[int]) -> None:
    # BEGIN_SOLTUION
    # Well, this was easy
    from exercise_1_a import convert

    convert(hypercube, array, d, False)
    # END_SOLUTION
