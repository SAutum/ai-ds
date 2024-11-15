from exercise_1_a import get_query
import sqlite3
import typing
import zipme
import sys
import hashlib


def test_sql_query(
    query: str,
    expected_attribute_names: typing.List[str],
    expected_result: typing.Any,
    compare_sets: bool = True,
    ignore_order: bool = False,
) -> None:
    db_filename = "data/database.db"

    assert '"' not in query, "SQL strings must be single-quoted"

    query = query.rstrip("; \r\n\t")

    assert query.count(";") == 0, "Only a single query is allowed. There is no need to use a semicolon."

    with sqlite3.connect(db_filename) as db:
        cursor = db.cursor()

        cursor.execute(query)

        attribute_names = [description[0] for description in cursor.description]

        names_are_equal = True

        if len(attribute_names) != len(expected_attribute_names):
            names_are_equal = False
        else:
            for name1, name2 in zip(attribute_names, expected_attribute_names):
                if name1 != name2 and name2 != "any name":
                    names_are_equal = False

        if not names_are_equal:
            fail(
                f"Expected attributes: {', '.join(expected_attribute_names)}\n"
                f"but got attributes: {', '.join(attribute_names)}."
            )

        result = cursor.fetchall()

        if compare_sets:
            if set(result) != set(expected_result):
                fail(f"Expected {expected_result}\nbut got {result}.")
        else:
            if result != expected_result:
                fail(f"Expected {expected_result}\nbut got {result}.")

    with open(db_filename, "rb") as f:
        data = f.read()

    expected_hash = "93fc3904c95a1605b783a9b5d272af863b0f5c73053f8252ba81cd741872695f"

    assert (
        hashlib.sha256(data).hexdigest() == expected_hash
    ), f"Database {db_filename} may not be modified. Replace it with the original file."


def fail(message: str) -> None:
    print(f"\033[91m{message}\033[0m")
    sys.exit(1)


if __name__ == "__main__":
    expected = [
        ("Lemons",),
        ("Salad",),
        ("Potatoes",),
        ("Pears",),
        ("Apples",),
        ("Bread",),
        ("Lemonade",),
        ("Marmelade",),
        ("Pizza",),
    ]

    test_sql_query(get_query(), ["productname"], expected)

    zipme.finish(__file__)

# 44650722162000000000
