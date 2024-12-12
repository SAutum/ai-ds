from exercise_2_a import get_query
import traceback
import psycopg
import zipme
import sys


def test_code() -> None:
    with open("exercise_2_a.py", encoding="utf-8") as f:
        code = f.read()

    assert "UNION" not in code.upper(), "No UNION allowed. UNION ALL is part of a later exercise."
    assert "GROUPING" not in code.upper(), "No GROUPING allowed. GROUPING SETS are part of a later exercise."


def test_query(query: str) -> None:
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
            except psycopg.errors.UndefinedTable:
                traceback.print_exc()
                print_red("Did you run populate_database.py from the previous assignment yet?")
                sys.exit(1)

            rows = cursor.fetchall()

            # Check headers
            description = cursor.description
            assert description
            headers = [desc[0] for desc in description]

            expected_headers = ["category", "subcategory", "year", "n"]

            assert headers == expected_headers, f"Expected headers {expected_headers}, but got headers {headers}"

            # Check row count
            num_expected_rows = 2949

            assert len(rows) == num_expected_rows, f"Expected {num_expected_rows}, but got {len(rows)} instead"

            # Check a few random rows
            test_rows = [
                (None, None, None, 1000000),
                ("Home & Kitchen", "Kitchen & Dining", 2019, 863),
                ("Electronics", "Computer Accessories & Peripherals", 2015, 83),
                ("Books", "Humor & Entertainment", None, 899),
                ("Electronics", None, None, 167797),
                (None, None, 2020, 178072),
            ]

            for test_row in test_rows:
                assert test_row in rows, f"Your result does not contain the row {test_row}"


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[0m")


if __name__ == "__main__":
    test_code()
    test_query(get_query())
    zipme.finish(__file__)

# 52543553462000000000
