from exercise_1_b import hypercube2array
from test_exercise_1_a import Hypercube, hyperprint, make_array, make_testcases
import zipme
import sys


def test_hypercube2array(
    d: list[int], hypercube: Hypercube, expected_array: list[int]
) -> None:
    array = make_array(d)

    hypercube2array(hypercube, array, d)

    if array != expected_array:
        print_red("Expected array:")
        hyperprint(expected_array)
        print_red("Your array:")
        hyperprint(array)
        print_red("Test failed!")
        sys.exit(1)


def test() -> None:
    for d, array, hypercube in make_testcases():
        test_hypercube2array(d, hypercube, array)


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[00m")


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 53353451322000000000
