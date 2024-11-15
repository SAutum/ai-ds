from typing import Any

Column = list[Any]
Relation = dict[str, Column]


def example_from_assignment() -> None:
    relation1: Relation = {
        "a": [1, 2],
        "b": [3, 4],
    }

    relation2: Relation = {
        "b": [3, 3, 4],
        "c": [5, 5, 7],
    }

    # This should be the result of the natural join of relation1 with relation2
    expected_result: Relation = {
        "a": [1, 1, 2],
        "b": [3, 3, 4],
        "c": [5, 5, 7],
    }

    result = join(relation1, relation2)

    # We don't really care about the order of the tuples.
    # This unsophisticated comparison is just for simplicity.
    assert result == expected_result

    print("example_from_assignment ok")


def example_without_common_attributes() -> None:

    relation1: Relation = {
        "a": [1, 2],
        "b": [3, 4],
    }

    relation2: Relation = {
        "c": [5, 6, 7],
        "d": [10, 100, 1000],
    }

    expected_result: Relation = {
        "a": [1, 1, 1, 2, 2, 2],
        "b": [3, 3, 3, 4, 4, 4],
        "c": [5, 6, 7, 5, 6, 7],
        "d": [10, 100, 1000, 10, 100, 1000],
    }

    result = join(relation1, relation2)

    assert result == expected_result

    print("example_without_common_attributes ok")


def join(relation1: Relation, relation2: Relation) -> Relation:
    # Find attributes which are common to both relations
    common_attributes = relation1.keys() & relation2.keys()

    # Combine attributes of both relations
    combined_attributes = relation1.keys() | relation2.keys()

    # N new relation with the combined attributes
    result: Relation = {attribute: [] for attribute in combined_attributes}

    # For each pair of rows in both relations
    for i in range(relation_len(relation1)):
        for j in range(relation_len(relation2)):

            # If all common attributes are equal
            if all(relation1[attribute][i] == relation2[attribute][j] for attribute in common_attributes):
                # Add the combined row to the result
                for attribute in combined_attributes:
                    # Decide whether to take attribute from relation1 or relation2
                    if attribute in relation1:
                        result[attribute].append(relation1[attribute][i])
                    else:
                        result[attribute].append(relation2[attribute][j])

    return result


def relation_len(relation: Relation) -> int:
    # Return number of rows in a relation.

    # Return the length of any column since all should have the same length.
    for value in relation.values():
        return len(value)

    return 0


if __name__ == "__main__":
    example_from_assignment()
    example_without_common_attributes()
