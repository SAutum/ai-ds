import re
import sys
import time
import zipme
import psycopg
import statistics
from exercise_1_e import create_database, get_query1, get_query2


def test_query() -> None:
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            create_database(cursor)

            query1 = get_query1()
            query2 = get_query2()

            # The word "SELECT" may only be used once in the first query
            select_count = query1.upper().count("SELECT")
            assert (
                select_count == 1
            ), f"The word 'SELECT' may only appear once in the first query, but you used it {select_count} times."

            # The word "SELECT" must appear exactly twice in the second query
            select_count = query2.upper().count("SELECT")
            assert (
                select_count == 2
            ), f"The word 'SELECT' must appear exactly twice in the second query, but you used it {select_count} times."

            # "GROUP BY" must appear exactly twice in the second query
            group_by_count = query2.upper().count("GROUP BY")
            assert (
                group_by_count == 2
            ), f"'GROUP BY' must appear exactly twice in the second query, but you used it {group_by_count} times."

            aggregate_count1 = sum(1 for _ in re.findall(r"\b(?:AVG|COUNT|MAX|MIN|SUM)\b", query1.upper(), re.IGNORECASE))

            # The first query must contain at least one aggregate function
            assert (
                aggregate_count1 >= 1
            ), f"The first query must contain at least one aggregate function (AVG, COUNT, MAX, MIN, SUM), but it only contains {aggregate_count1}."

            aggregate_count2 = sum(1 for _ in re.findall(r"\b(?:AVG|COUNT|MAX|MIN|SUM)\b", query2.upper(), re.IGNORECASE))

            # The second query must contain at least two aggregate functions
            assert (
                aggregate_count2 >= 2
            ), f"The second query must contain at least two aggregate functions (AVG, COUNT, MAX, MIN, SUM), but it only contains {aggregate_count2}."

            # Warmup to avoid cold start effects
            for query in [query1, query2]:
                cursor.execute(query).fetchall()

            # Repeat a few times to get more stable time measurements
            times = [[], []]
            for _ in range(10):
                results = [None, None]

                for i_query, query in enumerate([query1, query2]):
                    start_time = time.perf_counter()

                    results[i_query] = cursor.execute(query).fetchall()

                    elapsed_time = time.perf_counter() - start_time

                    times[i_query].append(elapsed_time)

                if results[0] != results[1]:
                    print_red("The results of the two queries are not the same.\n")

                    n1 = min(10, len(results[0]))

                    print_red(f"Here are the first {n1} rows of the first query:\n")

                    for row in results[0][:n1]:
                        print_red(row)

                    print_red("\n")

                    n2 = min(10, len(results[1]))

                    print_red(f"Here are the first {n2} rows of the second query:\n")

                    for row in results[1][:n2]:
                        print_red(row)

                    sys.exit(1)

            avg_times1 = statistics.mean(times[0])
            avg_times2 = statistics.mean(times[1])
            std_times1 = statistics.stdev(times[0])
            std_times2 = statistics.stdev(times[1])

            print(
                f"First query: {avg_times1 * 1000:.3f} ± {std_times1 * 1000:.3f} milliseconds, second query: {avg_times2 * 1000:.3f} ± {std_times2 * 1000:.3f} milliseconds"
            )

            assert avg_times1 > avg_times2, "The second query should be faster than the first one."
            assert (
                avg_times1 - std_times1 > avg_times2 + std_times2
            ), "The second query is faster than the first query, but the difference is not significant. Choose data or queries such that the difference is more pronounced."


def print_red(msg: str, end: str = "\n") -> None:
    print(f"\033[91m{msg}\033[0m", end=end)


if __name__ == "__main__":
    for _ in range(3):
        test_query()
    zipme.finish(__file__)

# 32127330601000000000
