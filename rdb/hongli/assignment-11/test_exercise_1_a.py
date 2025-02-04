import zipme
import os
import json
from test_exercise_1 import Node
import exercise_1_a


def load_tree(tree_data: dict) -> Node:
    x_min, x_max = tree_data["bounds"]

    bounds = (tuple(x_min), tuple(x_max))

    if "children" in tree_data:
        children = [load_tree(child) for child in tree_data["children"]]
        return Node(None, children, bounds)
    else:
        points = [tuple(p) for p in tree_data["points"]]
        return Node(points, None, bounds)


def test() -> None:
    for i_tree in range(3):
        json_filename = f"data/tree_{i_tree}.json"
        filename = f"exercise_1_a_{i_tree}.png"

        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        with open(json_filename, encoding="utf-8") as f:
            tree_data = json.load(f)

        tree = load_tree(tree_data)

        exercise_1_a.draw_tree(tree, filename)

        assert os.path.isfile(
            filename
        ), f"draw_tree should have saved the tree as {filename}, but file does not exist."

    print("Images of trees will be visually inspected manually after the deadline.")


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 74266724720200000000
