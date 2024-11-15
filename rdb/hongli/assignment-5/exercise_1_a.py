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

    # pick the one with smaller num of rows to
    if relation_len1 < relation_len2:
        build_input_R = relation1
        probe_input_S = relation2
    else:
        build_input_R = relation2
        probe_input_S = relation1

    # initialize the hash table, store tuples in the relation as python dictionary
    # to the hash table
    for i in range(relation_len(build_input_R)):
        """
        tuple can be hashed, so I set the common attribute values as key
        if there is no common attribute, all rows in the relation will have
        the same key: tuple()
        """
        key = tuple([build_input_R[value][i] for value in common_attributes])
        """
        set the value as list of dictionaries. I tried tuple, but the
        attribute-value pair doesn't really match anymore (because the attributes are
        stored as set)
        """
        value = {}
        for attribute in build_input_R.keys():
            value[attribute] = build_input_R[attribute][i]
        # insert the tuple to build input R
        insert_tuple(hash_table=hash_table, key=key, value=value)

    # create an empty result relation
    result: Relation = {attribute: [] for attribute in combined_attributes}

    # iterate through S
    for i in range(relation_len(probe_input_S)):
        key = tuple([probe_input_S[value][i] for value in common_attributes])

        # if we can find the key in the hash table, do a cross join
        if hash_table.get(key) != None:
            for r_value in hash_table[key]:
                for attribute in combined_attributes:
                    if r_value.get(attribute) != None:
                        result[attribute].append(r_value[attribute])
                    else:
                        result[attribute].append(probe_input_S[attribute][i])
    return result


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
