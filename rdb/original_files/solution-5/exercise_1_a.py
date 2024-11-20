from typing import Any

Column = list[Any]
Relation = dict[str, Column]


def join(relation1: Relation, relation2: Relation) -> Relation:
    # BEGIN_SOLUTION

    # Make sure that relation1 is the smaller relation to keep index small
    if relation_len(relation1) > relation_len(relation2):
        return join(relation2, relation1)

    assert relation_len(relation1) <= relation_len(relation2)

    # Find attributes which are common to both relations
    common_attributes = list(relation1.keys() & relation2.keys())

    # Combine attributes of both relations
    combined_attributes = relation1.keys() | relation2.keys()

    # Create a new relation with the combined attributes
    result: Relation = {a: [] for a in combined_attributes}

    # Create a hash index for the smaller relation
    IndexType = dict[tuple[Any, ...], list[int]]
    index: IndexType = {}
    for i in range(relation_len(relation1)):
        key = tuple(relation1[a][i] for a in common_attributes)
        index.setdefault(key, []).append(i)

    # For each row in the larger relation
    for i in range(relation_len(relation2)):
        key = tuple(relation2[a][i] for a in common_attributes)

        # For each row in the smaller relation with the same key
        for j in index.get(key, []):

            # Add the combined row to the result
            for attribute in combined_attributes:

                # Decide whether to take attribute from relation1 or relation2
                if attribute in relation1:
                    result[attribute].append(relation1[attribute][j])
                else:
                    result[attribute].append(relation2[attribute][i])

    return result


def relation_len(relation: Relation) -> int:
    # Return number of rows in a relation.

    # Return the length of any column since all should have the same length.
    for value in relation.values():
        return len(value)

    return 0


# END_SOLUTION
