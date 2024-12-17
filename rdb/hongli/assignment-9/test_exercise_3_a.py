import bisect
import zipme
from exercise_3_a import get_keys

# MAX_KEYS = 2 corresponds to a B+ tree with degree 3
MAX_KEYS = 2


class Node:
    def __init__(
        self,
        keys: list[int],
        children: list["Node"] | None = None,
        values: list[str] | None = None,
    ):
        self.keys = keys
        self.children = children
        self.values = values
        # For simplicity, this B+ tree does not link leaf nodes, but
        # technically, a "real" B+ tree should have such links.


def find(node: Node, key: int) -> Node:
    # Walk down tree until leaf node is reached
    while node.children is not None:
        i = bisect.bisect(node.keys, key)
        node = node.children[i]

    # Find key in leaf node
    i = bisect.bisect_left(node.keys, key)
    if i < len(node.keys) and node.keys[i] == key:
        return node.values[i]

    raise ValueError(f"Could not find {key}")


def insert(node: Node, key: int, value: str) -> Node:
    # Return new leaf node if tree is empty
    if not node:
        return Node([key], None, [value])

    # Find path to leaf node
    path = []
    while node.children is not None:
        i = bisect.bisect(node.keys, key)
        path.append((node, i))
        node = node.children[i]

    i = bisect.bisect_left(node.keys, key)

    # If key already exists, overwrite old value with new value
    if i < len(node.keys) and node.keys[i] == key:
        node.values[i] = value
    else:
        # Insert key and value into leaf node
        node.keys.insert(i, key)
        node.values.insert(i, value)

        # Split if node is too fat
        while len(node.keys) > MAX_KEYS:
            middle = len(node.keys) // 2

            key_for_parent = node.keys[middle]

            if node.values is not None:
                # Split leaf nodes in the middle
                left_keys = node.keys[:middle]
                right_keys = node.keys[middle:]

                left_values = node.values[:middle]
                right_values = node.values[middle:]

                left_children = None
                right_children = None
            else:
                # Unlike leaf nodes, non-leaf nodes spill the middle key into the parent
                left_keys = node.keys[:middle]
                right_keys = node.keys[middle + 1 :]

                left_values = None
                right_values = None

                left_children = node.children[: middle + 1]
                right_children = node.children[middle + 1 :]

            left = Node(left_keys, left_children, left_values)
            right = Node(right_keys, right_children, right_values)

            # Insert key and split nodes into parent node if there is one
            if path:
                parent, parent_index = path.pop()
                parent.keys.insert(parent_index, key_for_parent)
                # Delete old node from parent
                del parent.children[parent_index]
                # Insert new nodes into parent
                parent.children.insert(parent_index, left)
                parent.children.insert(parent_index + 1, right)
                node = parent
            else:
                # Create new node if there is no parent node
                node = Node([key_for_parent], [left, right])

    # Return root node if there is one, or new node
    return path[0][0] if path else node


def print_node(node: Node, depth: int = 0, indent: str = " " * 4) -> None:
    if node.children is not None:
        print_node(node.children[0], depth + 1)
        for key, child in zip(node.keys, node.children[1:]):
            print(indent * depth, f"{key:4d}", "-" * (50 - depth * 4))
            print_node(child, depth + 1)

    if node.values is not None:
        for key, value in zip(node.keys, node.values):
            print(indent * depth, f"{key:4d}", "->", value)


def count_nodes(node: Node) -> int:
    if node.children is None:
        return 1
    else:
        return 1 + sum(count_nodes(child) for child in node.children)


def test() -> None:
    keys = get_keys()

    assert isinstance(keys, list), f"get_keys should return a list, not {type(keys)}"

    tree = None

    for key in keys:
        assert isinstance(
            key, int
        ), f"Values in the list should be of type int, not {type(key)}"

        value = f"Value for key {key}"

        tree = insert(tree, key, value)

    print("Tree 🌳:")

    print_node(tree)

    assert len(keys) == 18, f"You should have 18 keys, but you have {len(keys)}"

    assert (
        count_nodes(tree) == 13
    ), f"The tree should have 13 nodes, but it has {count_nodes(tree)}"


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 01044061623000000000
