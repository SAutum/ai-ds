import zipme
import psycopg
import time
from exercise_1_c import create_data


def test() -> None:
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:

            def measure_fastest_time(name: str) -> float:
                min_time = float("inf")

                for _ in range(5):
                    start_time = time.perf_counter()

                    cursor.execute(
                        "SELECT z FROM mytable WHERE x = 0 AND y = 0"
                    ).fetchall()

                    elapsed_time = time.perf_counter() - start_time

                    min_time = min(min_time, elapsed_time)

                print(f"{min_time * 1000:4.1f} milliseconds for {name}")

                return min_time

            cursor.execute("DROP TABLE IF EXISTS mytable")
            cursor.execute("CREATE TABLE mytable (x INT, y INT, z INT)")

            data = create_data()

            assert isinstance(data, list), f"Expected list, but got {type(data)}"
            for i, tup in enumerate(data):
                assert isinstance(
                    tup, tuple
                ), f"Expected tuple, but got {type(tup)} at index {i}"
                assert (
                    len(tup) == 3
                ), f"Expected tuple of length 3, but got {len(tup)} at index {i}"
                for j, value in enumerate(tup):
                    assert isinstance(
                        value, int
                    ), f"Expected int, but got {type(value)} at index {i}, {j} for value {value}"

            cursor.executemany(
                "INSERT INTO mytable (x, y, z) VALUES (%s, %s, %s)", data
            )

            median_time1 = measure_fastest_time("query without index")

            cursor.execute("DROP INDEX IF EXISTS x_index")
            cursor.execute("CREATE INDEX x_index ON mytable (x)")
            median_time2 = measure_fastest_time("query with index on x")
            cursor.execute("DROP INDEX IF EXISTS x_index")

            cursor.execute("DROP INDEX IF EXISTS x_y_index")
            cursor.execute("CREATE INDEX x_y_index ON mytable (x, y)")
            median_time3 = measure_fastest_time("query with index on x and y")
            cursor.execute("DROP INDEX IF EXISTS x_y_index")

            assert (
                median_time1 < median_time2
            ), "Query without index should be faster than query with index on x, but it is not."
            assert (
                median_time1 > median_time3 * 5
            ), "Query with index on x and y should be at least 5 times faster than query without index, but it is not."


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 66501035020200000000
