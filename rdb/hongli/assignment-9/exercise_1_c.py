from typing import Any

Hypercube = list[Any]


def extract_subcube(
    hypercube: Hypercube,
    d: list[int],
    x_min: list[int],
    x_max: list[int],
    subcube: Hypercube,
) -> None:
    # Your solution goes here.

    for i in range(x_min[-1], x_max[-1]+1):
        sub_i = i - x_min[-1] + 1    # ignore 666
        if len(d) == 1:
            subcube[sub_i] = hypercube[i]
        else:
            extract_subcube(hypercube[i], d[:-1], x_min[:-1], x_max[:-1],
                            subcube[sub_i])

    return
