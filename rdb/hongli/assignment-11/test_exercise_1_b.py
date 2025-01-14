import zipme
import exercise_1_b
from test_exercise_1 import Node, Point
import os
import sys
import time
import math
import cmath
import random
import tracemalloc
from typing import Generator


def find(point: Point, node: Node) -> bool:
    # This function tries to find a given point within a node of an R-tree
    (x0, y0), (x1, y1) = node.bounds
    x, y = point

    # If the point is outside the bounds of the R-tree, it certainly does not
    # contain our point and we can stop looking.
    if x < x0 or x > x1 or y < y0 or y > y1:
        return False

    # If we have points, we check whether our query point is among them.
    if node.points is not None:
        return point in node.points

    # Otherwise, we have children.
    assert node.children is not None

    # Recursively search for the point in the child nodes of the node.
    for child in node.children:
        if find(point, child):
            return True

    return False


def spiral(n_points: int, spin: float, noise: float) -> list[Point]:
    points: list[Point] = []
    for i in range(n_points):
        r = i / n_points
        t = spin * 2 * math.pi * r
        x = r * math.cos(t) + noise * gauss()
        y = r * math.sin(t) + noise * gauss()
        points.append((x, y))

    return points


def gauss() -> float:
    return random.gauss(0.0, 1.0)


def make_bad_tree(points: list[Point]) -> Node:
    first_half = points[: len(points) // 2]
    second_half = points[len(points) // 2 :]

    dim = len(points[0])

    x_min = tuple(-float("inf") for _ in range(dim))
    x_max = tuple(float("inf") for _ in range(dim))

    bounds = (x_min, x_max)

    child1 = Node(points=first_half, children=None, bounds=bounds)
    child2 = Node(points=second_half, children=None, bounds=bounds)

    return Node(points=None, children=[child1, child2], bounds=bounds)


def clusters(
    n_clusters: int,
    points_per_cluster: int,
    noise: float,
    scale: float,
    num_attempts: int = 10,
) -> list[Point]:
    points: list[Point] = []
    centers: list[Point] = []
    for _ in range(n_clusters):
        # Try to place centers far away from each other7
        max_center_dist = -float("inf")
        cx_max = 0.0
        cy_max = 0.0
        for _ in range(num_attempts):
            cx = scale * (random.random() * 2 - 1)
            cy = scale * (random.random() * 2 - 1)

            center_dist = min(
                (math.hypot(cx - x, cy - y) for x, y in centers), default=0.0
            )

            if center_dist > max_center_dist:
                max_center_dist = center_dist
                cx_max = cx
                cy_max = cy

        centers.append((cx_max, cy_max))

        for _ in range(points_per_cluster):
            x = cx_max + noise * gauss()
            y = cy_max + noise * gauss()
            points.append((x, y))

    return points


def gaussian(n_points: int) -> list[Point]:
    points: list[Point] = []
    for _ in range(n_points):
        x = gauss()
        y = gauss()
        points.append((x, y))

    return points


def uniform(n_points: int) -> list[Point]:
    points: list[Point] = []
    for _ in range(n_points):
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        points.append((x, y))

    return points


def random_walker(n_points: int, step_size: float) -> list[Point]:
    x = 0.0
    y = 0.0
    points: list[Point] = []
    for _ in range(n_points):
        x += step_size * gauss()
        y += step_size * gauss()
        points.append((x, y))

    return points


def nextpot(n: int) -> int:
    return 1 << (n - 1).bit_length() if n > 0 else 1


def cool_turkey(z: list[complex]) -> list[complex]:
    n = len(z)
    if n == 1:
        return z

    even = cool_turkey(z[::2])
    odd = cool_turkey(z[1::2])

    result: list[complex] = [0] * n
    for i in range(n // 2):
        t = cmath.exp(-2j * math.pi * i / n) * odd[i]
        result[i] = even[i] + t
        result[i + n // 2] = even[i] - t

    return result


def batman(n_points: int, noise: float) -> list[Point]:
    n_points = nextpot(n_points)
    c = [
        0,
        0,
        0,
        0,
        -2551,
        -255,
        -913,
        91,
        -57,
        282,
        -36,
        -179,
        -433,
        -133,
        50,
        -15,
        -56,
        133,
        9,
        21,
        -324,
        -176,
        188,
        -102,
        0,
        0,
        -19,
        -29,
        -18,
        -15,
        -173,
        145,
        -24,
        24,
        -16,
        -16,
        16,
        20,
        -38,
        48,
        -21,
        13,
        54,
        35,
        29,
        57,
        28,
        -54,
        38,
        -15,
        -86,
        -34,
        -10,
        -35,
        14,
        -49,
        -21,
        0,
        49,
        9,
        0,
        -24,
        0,
        22,
        14,
        0,
        -12,
        0,
        0,
        0,
        0,
        42,
        0,
        0,
        0,
        0,
        0,
        0,
        -6,
        -18,
        0,
        0,
        0,
        0,
        -11,
        19,
        0,
        0,
        -6,
        0,
        6,
        0,
        0,
        -6,
        -7,
        -9,
        8,
        9,
        -7,
        7,
    ]
    z: list[complex] = [0] * n_points
    for i in range(len(c) // 4):
        p, q, r, s = c[i * 4 : i * 4 + 4]
        z[i] = p + 1j * q
        z[-i] = r + 1j * s

    points: list[Point] = []
    for zi in cool_turkey(z):
        x = zi.real / 2048 + noise * gauss()
        y = zi.imag / 2048 + noise * gauss()
        points.append((x, y))

    return points


def all_points(node: Node) -> Generator[Point, None, None]:
    if node.points is not None:
        yield from node.points
    else:
        assert node.children is not None
        for child in node.children:
            yield from all_points(child)


def test(benchmark: bool = True) -> None:
    filename = "exercise_1_b.png"

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    for min_speedup, n in [(4, 2048), (9, 4096)]:
        for points in [
            spiral(n, 3, 0.03),
            clusters(20, n // 20, 0.5, 10.0),
            gaussian(n),
            uniform(n),
            random_walker(n, 10.0),
            batman(n, 0.003),
        ]:
            points = list(set(points))
            random.seed(0)
            random.shuffle(points)

            original_points = list(points)

            root = exercise_1_b.make_tree(points)

            bad_tree = make_bad_tree(points)

            points_set = set(all_points(root))

            assert len(points_set) == len(
                original_points
            ), f"You were given {len(original_points)} points, but you somehow returned a tree with {len(points_set)} points"

            for i, p in enumerate(original_points):
                assert p in points_set, f"{i}th Point {p} not found in tree"

            start_time = time.perf_counter()

            for p in original_points:
                assert find(p, bad_tree), f"Point {p} not found in tree"

            elapsed_time_bad_tree = time.perf_counter() - start_time

            start_time = time.perf_counter()

            for p in original_points:
                assert find(p, root), f"Point {p} not found in tree"

            elapsed_time = time.perf_counter() - start_time

            if benchmark:
                speedup = elapsed_time_bad_tree / elapsed_time - 1

                print(
                    f"Time to find all points in your tree: {elapsed_time:.6f} seconds"
                )
                print(
                    f"Time to find all points in  bad tree: {elapsed_time_bad_tree:.6f} seconds"
                )
                print(f"Speedup: {speedup:.2f} times faster")

                if speedup < min_speedup:
                    print_red(
                        f"Searching your tree is only {speedup:.2f} times faster than searching a bad tree, but it should be at least {min_speedup} times faster"
                    )

                    import exercise_1_a

                    exercise_1_a.draw_tree(root, filename)

                    print_red(
                        f"A visual representation of your tree has been saved as {filename} to help you debug why your tree is slow"
                    )

                    sys.exit(1)


def print_red(msg: str) -> None:
    print("\033[91m" + msg + "\033[0m")


if __name__ == "__main__":
    # Disable tracemalloc for benchmark because it interfers with performance measurements.
    tracemalloc.stop()
    test(benchmark=True)
    tracemalloc.start()

    # Run tests again to ensure memory limit is enforced
    test(benchmark=False)
    zipme.finish(__file__)

# 50120056301000000000
