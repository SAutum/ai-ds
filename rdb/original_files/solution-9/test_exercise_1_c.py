from test_exercise_1_a import make_hypercube, hyperprint, DONT_USE, print_red, Hypercube
from exercise_1_c import extract_subcube
import sys
import zipme


def testcase(
    hypercube: Hypercube,
    d_hypercube: list[int],
    x_min: list[int],
    x_max: list[int],
    expected_subcube: Hypercube,
) -> None:
    d_subcube = [b - a + 1 for a, b in zip(x_min, x_max)]

    subcube = make_hypercube(d_subcube)

    extract_subcube(hypercube, d_hypercube, x_min, x_max, subcube)

    if subcube != expected_subcube:
        print("Expected subcube including 0-based index values:")
        print(expected_subcube)
        print("Your subcube including 0-based index values:")
        print(subcube)
        print_red("Expected subcube:")
        hyperprint(expected_subcube)
        print_red("Your subcube:")
        hyperprint(subcube)
        print_red("Test failed!")
        sys.exit(1)


def test() -> None:
    d = [4, 2]

    hypercube = [
        DONT_USE,
        [DONT_USE, 1, 2, 3, 4],
        [DONT_USE, 5, 6, 7, 8],
    ]

    x_min = [3, 2]
    x_max = [4, 2]

    expected_subcube = [
        DONT_USE,
        [DONT_USE, 7, 8],
    ]

    testcase(hypercube, d, x_min, x_max, expected_subcube)

    d = [2, 2]

    hypercube = [
        DONT_USE,
        [DONT_USE, 1, 2],
        [DONT_USE, 3, 4],
    ]

    expected_subcube = [
        DONT_USE,
        [DONT_USE, 1, 2],
        [DONT_USE, 3, 4],
    ]

    x_min = [1, 1]
    x_max = [2, 2]

    testcase(hypercube, d, x_min, x_max, expected_subcube)

    d = [5]

    hypercube = [DONT_USE, 1, 2, 3, 4, 5]

    expected_subcube = [DONT_USE, 3, 4]

    x_min = [3]
    x_max = [4]

    testcase(hypercube, d, x_min, x_max, expected_subcube)

    d = [4, 3]

    hypercube = [
        DONT_USE,
        [DONT_USE, 1, 2, 3, 4],
        [DONT_USE, 5, 6, 7, 8],
        [DONT_USE, 9, 10, 11, 12],
    ]

    expected_subcube = [
        DONT_USE,
        [DONT_USE, 5, 6, 7],
        [DONT_USE, 9, 10, 11],
    ]

    x_min = [1, 2]
    x_max = [3, 3]

    testcase(hypercube, d, x_min, x_max, expected_subcube)

    d = [3, 4]

    hypercube = [
        DONT_USE,
        [DONT_USE, 1, 2, 3],
        [DONT_USE, 5, 6, 7],
        [DONT_USE, 8, 9, 10],
        [DONT_USE, 11, 12, 13],
    ]

    expected_subcube = [
        DONT_USE,
        [DONT_USE, 7],
        [DONT_USE, 10],
        [DONT_USE, 13],
    ]

    x_min = [3, 2]
    x_max = [3, 4]

    testcase(hypercube, d, x_min, x_max, expected_subcube)

    d = [2, 3, 4]

    hypercube = [
        DONT_USE,
        [DONT_USE, [DONT_USE, 1, 2], [DONT_USE, 3, 4], [DONT_USE, 5, 6]],
        [DONT_USE, [DONT_USE, 7, 8], [DONT_USE, 9, 10], [DONT_USE, 11, 12]],
        [DONT_USE, [DONT_USE, 13, 14], [DONT_USE, 15, 16], [DONT_USE, 17, 18]],
        [DONT_USE, [DONT_USE, 19, 20], [DONT_USE, 21, 22], [DONT_USE, 23, 24]],
    ]

    x_min = [1, 3, 3]
    x_max = [2, 3, 4]

    expected_subcube = [
        DONT_USE,
        [DONT_USE, [DONT_USE, 17, 18]],
        [DONT_USE, [DONT_USE, 23, 24]],
    ]

    testcase(hypercube, d, x_min, x_max, expected_subcube)


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 02040626122200000000
