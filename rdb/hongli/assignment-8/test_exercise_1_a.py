import re
import sys
import zipme
import psycopg
from exercise_1_a import get_query


def test() -> None:
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS mytable")

            cursor.execute("""
            CREATE TABLE mytable (
                A TEXT,
                B TEXT,
                C TEXT,
                D TEXT,
                E TEXT,
                F TEXT,
                G TEXT
            )
            """)

            cursor.execute("INSERT INTO mytable VALUES ('A', 'B', 'C', 'D', 'E', 'F', 'G')")

            query = get_query()

            cursor.execute(query)

            rows = list(cursor.fetchall())

    text_rows = ["(" + ", ".join(value for value in row if value) + ")" for row in rows]

    text_rows.sort()

    required = """
(A, B, C, D, E)
(A, B, C, D, E, F)
(A, B, C, D, F, G)
(A, B, C, D, G)
(A, C, D, E)
(A, C, D, E, F)
(A, C, D, F, G)
(A, C, D, G)
(B, C, D, E)
(B, C, D, E, F)
(B, C, D, F, G)
(B, C, D, G)
(B, D, E)
(B, D, E, F)
(B, D, F, G)
(B, D, G)
(B, E)
(B, E, F)
(B, F, G)
(B, G)
(C, D, E)
(C, D, E, F)
(C, D, F, G)
(C, D, G)
(D, E)
(D, E, F)
(D, F, G)
(D, G)
(E)
(E, F)
(F, G)
(G)
    """.strip().split("\n")

    errors = 0
    print("GROUP BY:")
    for row in text_rows:
        print(row, end="")

        if row in required:
            required.remove(row)
            print()
        else:
            print_red(" <--- ERROR: This combination of attributes should not be here.")
            errors += 1

    if errors:
        sys.exit(1)

    if required:
        print_red("ERROR: The following combinations of attributes are missing:")
        for row in required:
            print(row)
        sys.exit(1)

    assert query.lstrip().startswith(
        "SELECT A, B, C, D, E, F, G FROM mytable GROUP BY"
    ), f"Query must start with\nSELECT A, B, C, D, E, F, G FROM mytable GROUP BY\nYour query is:\n{query.lstrip()}"
    assert "CUBE" in query.upper(), "Query must contain the CUBE keyword"
    assert "ROLLUP" in query.upper(), "Query must contain the ROLLUP keyword"
    assert "GROUPING SETS" in query.upper(), "Query must contain the GROUPING SETS keyword"
    allowed = "A B C D E F G SELECT FROM mytable GROUP BY ROLLUP GROUPING SETS CUBE".split()
    for part in re.findall("[a-zA-Z]+", query):
        assert (
            part.upper() in allowed or part.lower() in allowed
        ), f"Using {part} is not allowed. Allowed identifiers are: {', '.join(allowed)}"

    num_non_whitespace = len("".join(query.split()))
    assert num_non_whitespace < 200, f"Your query consists of {num_non_whitespace} characters. You are probably doing something shady. For comparison, the solution has less than 100."

def print_red(msg: str, end: str = "\n") -> None:
    print(f"\033[91m{msg}\033[0m", end=end)


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 23011373321000000000
