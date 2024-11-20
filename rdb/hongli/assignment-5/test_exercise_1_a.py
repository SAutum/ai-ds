import random
import sqlite3
import zipme
from typing import Callable, Any
import exercise_1_a

Column = list[Any]
Relation = dict[str, Column]
NaturalJoinFunc = Callable[[Relation, Relation], Relation]


def relation_len(relation: Relation) -> int:
    # Return number of rows in a relation.
    # All columns should have the same length.
    for value in relation.values():
        return len(value)
    return 0


def check_relation(relation: Relation) -> None:
    assert isinstance(relation, dict), "Relation must be a dictionary"

    for attribute, column in relation.items():
        assert isinstance(attribute, str), "Attribute names must be strings"
        assert isinstance(column, list), "Columns must be lists"

    column_lengths = [len(column) for column in relation.values()]

    assert all(
        length == column_lengths[0] for length in column_lengths
    ), f"All columns should have the same length, but lengths are {column_lengths} for attributes {relation.keys()}"


def sorted_relation(relation: Relation, attributes: list[str]) -> Relation:
    keys: list[tuple[Any, ...]] = [
        tuple(relation[attribute][i] for attribute in attributes) for i in range(relation_len(relation))
    ]

    indices = list(range(len(keys)))

    indices.sort(key=lambda i: keys[i])

    return {attribute: [relation[attribute][i] for i in indices] for attribute in sorted(relation)}


def test_natural_join_relations(
    natural_join: NaturalJoinFunc,
    relation1: Relation,
    relation2: Relation,
    expected_result: Relation,
    sort_attributes: list[str],
) -> None:
    check_relation(relation1)
    check_relation(relation2)
    check_relation(expected_result)

    result = natural_join(relation1, relation2)

    check_relation(result)

    sorted_result = sorted_relation(result, attributes=sort_attributes)

    assert (
        sorted_result == expected_result
    ), f"Expected:\n{expected_result}\nbut got:\n{sorted_result}\n(after sorting by {sort_attributes})."


def test_simple_natural_join(natural_join: NaturalJoinFunc) -> None:
    # Test joining of "duck" and "yellow" over "animal_id" attribute with value 1
    relation1: Relation = {
        "animal_id": [1],
        "animal_name": ["duck"],
    }

    relation2: Relation = {
        "animal_id": [1],
        "color": ["yellow"],
    }

    expected_result: Relation = {
        "animal_id": [1],
        "animal_name": ["duck"],
        "color": ["yellow"],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["animal_id"])


def test_empty_natural_join(natural_join: NaturalJoinFunc) -> None:
    # Test joining of empty relations
    relation1: Relation = {
        "animal_id": [],
        "animal_name": [],
    }

    relation2: Relation = {
        "animal_id": [],
        "color": [],
    }

    expected_result: Relation = {
        "animal_id": [],
        "animal_name": [],
        "color": [],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["animal_id"])


def test_multiple_rows_natural_join(natural_join: NaturalJoinFunc) -> None:
    # Test joining of "duck" with "yellow" over "animal_id" attribute with value 1
    # and "bluewhale" with "blue" over "animal_id" attribute with value 3.
    relation1: Relation = {
        "animal_id": [1, 2, 3],
        "animal_name": ["duck", "fish", "bluewhale"],
    }

    relation2: Relation = {
        "animal_id": [1, 3],
        "color": ["yellow", "blue"],
    }

    expected_result: Relation = {
        "animal_id": [1, 3],
        "animal_name": ["duck", "bluewhale"],
        "color": ["yellow", "blue"],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["animal_id"])


def test_multiple_rows_natural_join_random_ids(natural_join: NaturalJoinFunc) -> None:
    # Test if natural join works with unordered ids
    relation1: Relation = {
        "animal_id": [1337, 42, 666],
        "animal_name": ["duck", "fish", "bluewhale"],
    }

    relation2: Relation = {
        "animal_id": [666, 1337],
        "color": ["blue", "yellow"],
    }

    expected_result: Relation = {
        "animal_id": [666, 1337],
        "animal_name": ["bluewhale", "duck"],
        "color": ["blue", "yellow"],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["animal_id"])


def test_multiple_attributes_natural_join(natural_join: NaturalJoinFunc) -> None:
    # Test whether both attributes are used for joining
    relation1: Relation = {
        "category_id": ["bird", "fish", "mammal", "mammal"],
        "animal_id": [1337, 42, 666, 1234],
        "animal_name": ["duck", "fish", "bluewhale", "platypus"],
    }

    relation2: Relation = {
        "category_id": ["mammal", "bird", "mammal", "mammal"],
        "animal_id": [666, 1337, 4321, 1234],
        "color": ["blue", "yellow", "black", "brown"],
    }

    expected_result: Relation = {
        "animal_id": [666, 1234, 1337],
        "animal_name": ["bluewhale", "platypus", "duck"],
        "category_id": ["mammal", "mammal", "bird"],
        "color": ["blue", "brown", "yellow"],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["animal_id"])


def test_multiple_same_attributes_natural_join(natural_join: NaturalJoinFunc) -> None:
    relation1: Relation = {
        "id1": [5, 3, 2, 1, 4],
        "a": [5, 1, 1, 2, 4],
    }

    relation2: Relation = {
        "id2": [20, 10, 40, 30, 50, 60, 99],
        "a": [1, 1, 2, 2, 1, 3, 999],
    }

    expected_result: Relation = {
        "a": [2, 2, 1, 1, 1, 1, 1, 1],
        "id1": [1, 1, 2, 2, 2, 3, 3, 3],
        "id2": [30, 40, 10, 20, 50, 10, 20, 50],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["id1", "id2"])


def test_random_values_natural_join(natural_join: NaturalJoinFunc) -> None:
    relation1: Relation = {
        "id1": [7, 1, 5, 3, 17, 2, 6, 0, 8, 9, 10, 14, 13, 12, 11, 15, 16, 7, 18, 19],
        "a": [1, 2, 0, 3, 3, 1, 0, 0, 0, 3, 4, 2, 0, 1, 4, 4, 2, 2, 1, 0],
        "b": [2, 1, 0, 2, 2, 1, 1, 2, 2, 2, 0, 4, 2, 3, 4, 1, 1, 1, 3, 2],
        "c": [0, 4, 2, 0, 2, 4, 2, 4, 1, 3, 3, 4, 2, 3, 3, 1, 1, 2, 2, 0],
    }
    relation2: Relation = {
        "id2": [28, 29, 26, 25, 24, 23, 22, 27, 20, 21],
        "a": [0, 0, 3, 2, 4, 4, 3, 2, 1, 1],
        "b": [1, 2, 4, 4, 1, 0, 2, 1, 2, 3],
        "c": [4, 1, 3, 2, 1, 2, 3, 4, 1, 2],
    }

    expected_result: Relation = {
        "a": [2, 0, 3, 4, 1],
        "b": [1, 2, 2, 1, 3],
        "c": [4, 1, 3, 1, 2],
        "id1": [1, 8, 9, 15, 18],
        "id2": [27, 29, 22, 24, 21],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["id1", "id2"])


def test_cross_join(natural_join: NaturalJoinFunc) -> None:
    # Joining without common attributes should become a cross join
    relation1: Relation = {
        "a": [1, 2],
        "b": [3, 4],
    }

    relation2: Relation = {
        "c": [5, 6],
        "d": [7, 8],
    }

    expected_result: Relation = {
        "a": [1, 1, 2, 2],
        "b": [3, 3, 4, 4],
        "c": [5, 6, 5, 6],
        "d": [7, 8, 7, 8],
    }

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["a", "b", "c", "d"])


def test_large(natural_join: NaturalJoinFunc) -> None:
    random.seed(0)
    num_rows = 100_000
    value_range = 100_000_000

    relation1: Relation = {
        "a": [random.randrange(value_range) for _ in range(num_rows)],
        "b": [random.randrange(value_range) for _ in range(num_rows)],
        "id1": shuffled(list(range(num_rows))),
    }

    relation2: Relation = {
        "b": [random.randrange(value_range) for _ in range(num_rows)],
        "c": [random.randrange(value_range) for _ in range(num_rows)],
        "id2": shuffled(list(range(num_rows))),
    }

    # Create in-memory database
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        # Create tables for both relations
        cursor.execute("CREATE TABLE relation1 (a INT, b INT, id1 INT)")
        cursor.execute("CREATE TABLE relation2 (b INT, c INT, id2 INT)")

        # Insert all values into the tables using named attributes
        cursor.executemany(
            "INSERT INTO relation1 (a, b, id1) VALUES (?, ?, ?)",
            zip(relation1["a"], relation1["b"], relation1["id1"]),
        )
        cursor.executemany(
            "INSERT INTO relation2 (b, c, id2) VALUES (?, ?, ?)",
            zip(relation2["b"], relation2["c"], relation2["id2"]),
        )

        # Perform the natural join using SQL
        cursor.execute("SELECT a, b, c, id1, id2 FROM relation1 NATURAL JOIN relation2 ORDER BY id1, id2")

        # Fetch the result
        attribute_names = [description[0] for description in cursor.description]
        expected_result: Relation = {key: [] for key in attribute_names}
        for row in cursor.fetchall():
            for i, key in enumerate(expected_result):
                expected_result[key].append(row[i])

    test_natural_join_relations(natural_join, relation1, relation2, expected_result, ["id1", "id2"])


def test_natural_join(natural_join: NaturalJoinFunc) -> None:
    test_simple_natural_join(natural_join)
    test_empty_natural_join(natural_join)
    test_multiple_rows_natural_join(natural_join)
    test_multiple_rows_natural_join_random_ids(natural_join)
    test_multiple_attributes_natural_join(natural_join)
    test_multiple_same_attributes_natural_join(natural_join)
    test_cross_join(natural_join)
    test_random_values_natural_join(natural_join)
    test_large(natural_join)

    print("Whether your code actually implements the correct join method will be checked manually.")

def shuffled(values: list[Any]) -> list[Any]:
    result = list(values)
    random.shuffle(result)
    return result


if __name__ == "__main__":
    test_natural_join(exercise_1_a.join)
    zipme.finish(__file__, allowed_imports={"typing"})

# 71216444743200000000
