Point = tuple[float, ...]


class Node:
    def __init__(
        self,
        points: list[Point] | None,
        children: list["Node"] | None,
        bounds: tuple[Point, Point],
    ) -> None:
        assert (
            points or children
        ), f'Either children or points must be provided, but points "{points}" and children "{children}" were given.'

        if points is not None:
            assert isinstance(
                points, list
            ), f"points must be a list, but it is of type {type(points)}"
            for p in points:
                assert isinstance(
                    p, tuple
                ), f"Each point must be a tuple, but {p} is of type {type(p)}"
        else:
            assert isinstance(
                children, list
            ), f"children must be a list, but it is of type {type(children)}"
            for c in children:
                assert isinstance(
                    c, Node
                ), f"Each child must be a Node, but {c} is of type {type(c)}"

        self.points = points
        self.children = children
        self.bounds = bounds

# 41562440023000000000
