import re
import sys
import math
import json
import random
from typing import Any
from exercise_1_a import array2hypercube
import zipme

Hypercube = list[Any]

# Placeholder for array index 0
# If you see this value somewhere, you are probably
# using 0-based indexing instead of 1-based indexing.
DONT_USE = 666


def make_hypercube(d: list[int]) -> Hypercube:
    d = list(d)
    size = d.pop()
    return [DONT_USE] + [make_hypercube(d) if d else 0 for _ in range(size)]


def make_array(d: list[int]) -> list[int]:
    return [DONT_USE] + [0] * math.prod(d)


def hyperprint(hypercube: Hypercube) -> None:
    s = json.dumps(hypercube, indent=4).replace(f"{DONT_USE},", "")
    s = re.sub(
        r"\[\s*\d+(\s*,\s*\d+)*\s*\]",
        lambda m: json.dumps(json.loads(m.group())),
        s,
        flags=re.MULTILINE,
    )
    print("\n".join(x for x in s.split("\n") if x.strip()))


def test_array2hypercube(
    d: list[int], array: list[int], expected_hypercube: Hypercube
) -> None:
    hypercube = make_hypercube(d)

    array2hypercube(array, hypercube, d)

    if hypercube != expected_hypercube:
        print("Expected hypercube including 0-based index values:")
        print(expected_hypercube)
        print("Your hypercube including 0-based index values:")
        print(hypercube)
        print("Input array including 0-based index values:")
        print(array)
        print_red("Expected hypercube:")
        hyperprint(expected_hypercube)
        print_red("Your hypercube:")
        hyperprint(hypercube)
        print_red("Test failed!")
        sys.exit(1)


def make_testcases() -> list[tuple[list[int], list[int], Hypercube]]:
    random.seed(0)
    z = list(range(24))
    random.shuffle(z)

    testcases = [
        (
            [5],
            [DONT_USE, 1, 2, 3, 4, 5],
            [DONT_USE, 1, 2, 3, 4, 5],
        ),
        (
            [2, 2],
            [DONT_USE, 1, 2, 3, 4],
            [
                DONT_USE,
                [DONT_USE, 1, 2],
                [DONT_USE, 3, 4],
            ],
        ),
        (
            [2, 2, 2],
            [DONT_USE, 1, 2, 3, 4, 5, 6, 7, 8],
            [
                DONT_USE,
                [DONT_USE, [DONT_USE, 1, 2], [DONT_USE, 3, 4]],
                [DONT_USE, [DONT_USE, 5, 6], [DONT_USE, 7, 8]],
            ],
        ),
        (
            [2, 3],
            [DONT_USE, 1, 2, 3, 4, 5, 6],
            [
                DONT_USE,
                [DONT_USE, 1, 2],
                [DONT_USE, 3, 4],
                [DONT_USE, 5, 6],
            ],
        ),
        (
            [3, 2],
            [DONT_USE, 1, 2, 3, 4, 5, 6],
            [
                DONT_USE,
                [DONT_USE, 1, 2, 3],
                [DONT_USE, 4, 5, 6],
            ],
        ),
        (
            [2, 3, 4],
            [
                DONT_USE,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
            ],
            [
                DONT_USE,
                [DONT_USE, [DONT_USE, 1, 2], [DONT_USE, 3, 4], [DONT_USE, 5, 6]],
                [DONT_USE, [DONT_USE, 7, 8], [DONT_USE, 9, 10], [DONT_USE, 11, 12]],
                [DONT_USE, [DONT_USE, 13, 14], [DONT_USE, 15, 16], [DONT_USE, 17, 18]],
                [DONT_USE, [DONT_USE, 19, 20], [DONT_USE, 21, 22], [DONT_USE, 23, 24]],
            ],
        ),
        (
            [4, 3, 2],
            [
                DONT_USE,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
            ],
            [
                DONT_USE,
                [
                    DONT_USE,
                    [DONT_USE, 1, 2, 3, 4],
                    [DONT_USE, 5, 6, 7, 8],
                    [DONT_USE, 9, 10, 11, 12],
                ],
                [
                    DONT_USE,
                    [DONT_USE, 13, 14, 15, 16],
                    [DONT_USE, 17, 18, 19, 20],
                    [DONT_USE, 21, 22, 23, 24],
                ],
            ],
        ),
        (
            [2, 3, 4],
            [DONT_USE] + z,
            [
                DONT_USE,
                [
                    DONT_USE,
                    [DONT_USE, z[0], z[1]],
                    [DONT_USE, z[2], z[3]],
                    [DONT_USE, z[4], z[5]],
                ],
                [
                    DONT_USE,
                    [DONT_USE, z[6], z[7]],
                    [DONT_USE, z[8], z[9]],
                    [DONT_USE, z[10], z[11]],
                ],
                [
                    DONT_USE,
                    [DONT_USE, z[12], z[13]],
                    [DONT_USE, z[14], z[15]],
                    [DONT_USE, z[16], z[17]],
                ],
                [
                    DONT_USE,
                    [DONT_USE, z[18], z[19]],
                    [DONT_USE, z[20], z[21]],
                    [DONT_USE, z[22], z[23]],
                ],
            ],
        ),
        (
            [4, 3, 2],
            [DONT_USE] + z,
            [
                DONT_USE,
                [
                    DONT_USE,
                    [DONT_USE, z[0], z[1], z[2], z[3]],
                    [DONT_USE, z[4], z[5], z[6], z[7]],
                    [DONT_USE, z[8], z[9], z[10], z[11]],
                ],
                [
                    DONT_USE,
                    [DONT_USE, z[12], z[13], z[14], z[15]],
                    [DONT_USE, z[16], z[17], z[18], z[19]],
                    [DONT_USE, z[20], z[21], z[22], z[23]],
                ],
            ],
        ),
        (
            [3, 1, 1, 1, 1, 1, 1],
            [DONT_USE, 1, 2, 3],
            [
                DONT_USE,
                [
                    DONT_USE,
                    [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, 1, 2, 3]]]]],
                ],
            ],
        ),
        (
            [1, 1, 1, 1, 1, 1, 3],
            [DONT_USE, 1, 2, 3],
            [
                DONT_USE,
                [
                    DONT_USE,
                    [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, 1]]]]],
                ],
                [
                    DONT_USE,
                    [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, 2]]]]],
                ],
                [
                    DONT_USE,
                    [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, [DONT_USE, 3]]]]],
                ],
            ],
        ),
        (
            [1, 1, 2, 1, 1, 3, 1],
            [DONT_USE, 1, 2, 3, 4, 5, 6],
            [
                DONT_USE,
                [
                    DONT_USE,
                    [
                        DONT_USE,
                        [
                            DONT_USE,
                            [
                                DONT_USE,
                                [DONT_USE, [DONT_USE, 1]],
                                [DONT_USE, [DONT_USE, 2]],
                            ],
                        ],
                    ],
                    [
                        DONT_USE,
                        [
                            DONT_USE,
                            [
                                DONT_USE,
                                [DONT_USE, [DONT_USE, 3]],
                                [DONT_USE, [DONT_USE, 4]],
                            ],
                        ],
                    ],
                    [
                        DONT_USE,
                        [
                            DONT_USE,
                            [
                                DONT_USE,
                                [DONT_USE, [DONT_USE, 5]],
                                [DONT_USE, [DONT_USE, 6]],
                            ],
                        ],
                    ],
                ],
            ],
        ),
    ]

    return testcases


def test() -> None:
    for d, array, hypercube in make_testcases():
        test_array2hypercube(d, array, hypercube)


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[00m")


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 23645156321000000000
