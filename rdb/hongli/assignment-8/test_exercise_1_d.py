import zipme
import psycopg
from exercise_1_d import get_values


def test() -> None:
    values = get_values()

    assert isinstance(values, list), f"The values should be of type list, not {type(values)}."
    assert len(values) > 0, "The list of values should not be empty."
    for i, value in enumerate(values):
        assert isinstance(value, int), f"The {i}-th value should be of type int, not {type(value)}."

    query1 = "SELECT       RANK() OVER (ORDER BY x) FROM x_values ORDER BY x"
    query2 = "SELECT ROW_NUMBER() OVER (ORDER BY x) FROM x_values ORDER BY x"

    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS x_values")
            cursor.execute("CREATE TABLE x_values (x INT)")
            for value in values:
                cursor.execute("INSERT INTO x_values (x) VALUES (%s)", (value,))

            results1 = cursor.execute(query1).fetchall()
            results2 = cursor.execute(query2).fetchall()

            print("Results from first query:")
            print(results1)
            print()
            print("Results from second query:")
            print(results2)

            assert results1 != results2, "The two queries should produce different results."


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 76176774101200000000
