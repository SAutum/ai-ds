import json
import zipme
import random
from exercise_2_a import one_dim_to_n_dim


def test_point(
    i: int, grid_size: int, dim: int, expected_point: tuple[int, ...]
) -> None:
    point = one_dim_to_n_dim(i, grid_size, dim)

    error_message = f"""ERROR:

Incorrect result for

    one_dim_to_n_dim(i={i}, grid_size={grid_size}, dim={dim})

Result should be: {expected_point}
But you returned: {point}"""

    assert point == expected_point, error_message


def test() -> None:
    random.seed(0)

    with open("data/expected_exercise_2.json", encoding="utf-8") as f:
        for expected in json.load(f):
            grid_size = expected["grid_size"]
            dim = expected["dim"]

            expected_points = list(enumerate(expected["points"]))

            random.shuffle(expected_points)

            for i, expected_point_list in expected_points:
                expected_point = tuple(expected_point_list)

                test_point(i, grid_size, dim, expected_point)

    for dim in [10, 20, 40, 80, 100, 1000, 4000]:
        for grid_size in [2, 4, 8]:
            for i, expected_point in [
                (0, (0,) * dim),
                (grid_size**dim - 1, (grid_size - 1,) * dim),
            ]:
                test_point(i, grid_size, dim, expected_point)


if __name__ == "__main__":
    test()
    zipme.finish(__file__, allowed_imports=set())

# 20546556122000000000
