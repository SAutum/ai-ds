from typing import Any

Column = list[Any]
Relation = dict[str, Column]


def join(relation1: Relation, relation2: Relation) -> Relation:
    # Find attributes which are common to both relations
    common_attributes = relation1.keys() & relation2.keys()

    # Combine attributes of both relations
    combined_attributes = relation1.keys() | relation2.keys()

    # create a temporary hash table to store tuples
    hash_table = {}

    relation_len1 = relation_len(relation=relation1)
    relation_len2 = relation_len(relation=relation2)

    if relation_len1 < relation_len2:
        build_input_R = relation1
    else:
        build_input_R = relation2

    # initialize the hash table, store tuples in the relation to R
    for i in range(relation_len(build_input_R)):
        """
        tuple can be hashed, so I set the common attribute values as key
        if there is no common attribute, all rows in the relation will have
        the same key: tuple()
        """
        key = tuple([build_input_R[value][i] for value in common_attributes])
        # set the combined attribute values as value
        value = tuple([build_input_R[value][i] for value in combined_attributes])
        # insert the tuple to build input R
        insert_tuple(hash_table=hash_table, key=key, value=value)
    print(hash_table)

def insert_tuple(hash_table, key, value):
    if hash_table.get(key) == None:
        hash_table[key] = [value]

    else:
        hash_table[key].append(value)



def relation_len(relation: Relation) -> int:
    # Return number of rows in a relation.

    # Return the length of any column since all should have the same length.
    for value in relation.values():
        # indeed it returns only the length of the first value
        return len(value)

    return 0
