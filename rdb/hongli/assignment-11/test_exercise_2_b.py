import json
import zipme
import random
from exercise_2_b import n_dim_to_one_dim


def test_index(
    point: tuple[int, ...], grid_size: int, dim: int, expected_index: int
) -> None:
    index = n_dim_to_one_dim(point, grid_size, dim)

    error_message = f"""ERROR:

Incorrect result for

    n_dim_to_one_dim(point={point}, grid_size={grid_size}, dim={dim})

Result should be: {expected_index}
But you returned: {index}"""

    assert index == expected_index, error_message


def test() -> None:
    random.seed(0)

    with open("data/expected_exercise_2.json", encoding="utf-8") as f:
        for expected in json.load(f):
            grid_size = expected["grid_size"]
            dim = expected["dim"]

            expected_points = list(enumerate(expected["points"]))

            random.shuffle(expected_points)

            for expected_index, point_list in expected_points:
                point = tuple(point_list)

                test_index(point, grid_size, dim, expected_index)

    for dim in [10, 20, 40, 80, 100, 1000, 4000]:
        for grid_size in [2, 4, 8]:
            for expected_index, point in [
                (0, (0,) * dim),
                (grid_size**dim - 1, (grid_size - 1,) * dim),
            ]:
                test_index(point, grid_size, dim, expected_index)


if __name__ == "__main__":
    test()
    zipme.finish(__file__, allowed_imports=set())

# 71065255643000000000
