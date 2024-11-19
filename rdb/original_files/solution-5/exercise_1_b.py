from typing import Any

Column = list[Any]
Relation = dict[str, Column]


def join(relation1: Relation, relation2: Relation) -> Relation:
    # BEGIN_SOLUTION
    from test_exercise_1_a import sorted_relation
    from typing import Any

    # Find attributes which are in both relations or at least one relation
    common_attributes = relation1.keys() & relation2.keys()
    combined_attributes = relation1.keys() | relation2.keys()

    # Sort both relations by the common attributes
    relation1 = sorted_relation(relation1, common_attributes)
    relation2 = sorted_relation(relation2, common_attributes)

    # Create a new relation with the combined attributes for output
    result: Relation = {attribute: [] for attribute in combined_attributes}

    # The key of a row i are the values of the common attributes
    def get_key(relation: Relation, i: int) -> tuple[Any, ...]:
        return tuple(relation[a][i] for a in common_attributes)

    # Step through both relations, merging them where their keys are equal
    i, j = 0, 0
    while i < relation_len(relation1) and j < relation_len(relation2):
        key1 = get_key(relation1, i)
        key2 = get_key(relation2, j)

        # Case key1 < key2 is handled automatically in loop below
        if key1 > key2:
            j += 1
        else:
            # While key in in relation2 matches key1
            for j2 in range(j, relation_len(relation2)):
                if key1 != get_key(relation2, j2): break

                # Add the combined row to the result
                for attribute in combined_attributes:

                    # Decide whether to take attribute from relation1 or relation2
                    if attribute in relation1:
                        result[attribute].append(relation1[attribute][i])
                    else:
                        result[attribute].append(relation2[attribute][j2])
            i += 1

    return result


def relation_len(relation: Relation) -> int:
    # Return number of rows in a relation.

    # Return the length of any column since all should have the same length.
    for value in relation.values():
        return len(value)

    return 0


# END_SOLUTION
