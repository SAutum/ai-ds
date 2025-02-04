from test_exercise_1 import Node, Point
import random

def make_tree(points: list[Point]) -> Node:
    # the inserting algorithm in the original paper is fairly complex
    # so I will just make a better bad tree
    dim = len(points[0])

    # sort the points by the first dimension
    points.sort(key=lambda p: p[0])

    return make_child(points, dim)


def make_child(points: list[Point], dim: int) -> Node:
    # the input points are already sorted by the first dimension
    x_min = tuple([min(p[d] for p in points) for d in range(dim)])
    x_max = tuple([max(p[d] for p in points) for d in range(dim)])
    bounds = (x_min, x_max)

    # if there are less than 120 points, just make a leaf node
    if len(points) < 100:
        return Node(points=points, children=None, bounds=bounds)

    # sort the points by the dimension with the most variance
    var = [(xmax - xmin) ** 2 for xmin, xmax in zip(x_min, x_max)]
    max_var_dim = var.index(max(var))
    # sort the points by the dimension with the most variance
    points.sort(key=lambda p: p[max_var_dim])

    # split the points in half
    first_half = points[: len(points) // 2]
    second_half = points[len(points) // 2:]
    child1 = make_child(first_half, dim)
    child2 = make_child(second_half, dim)

    return Node(points=None, children=[child1, child2], bounds=bounds)
