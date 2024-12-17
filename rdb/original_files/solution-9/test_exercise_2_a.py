import zipme
import time
import random
import itertools
from exercise_2_a import group_by_cube_fast


def group_by_cube_slow(rows: list[list[int]]) -> list[tuple[int | None, ...]]:
    # The first 5 attributes are `a`, `b`, `c`, `d` and `e` for GROUP BY CUBE(a, b, c, d, e).
    # The last attribute is `value`.
    attributes = [0, 1, 2, 3, 4]
    results = []

    # For all attribute combinations
    for length in range(len(attributes) + 1):
        for group_by_attributes in itertools.combinations(attributes, length):

            # Compute GROUP BY of group_by_attributes
            groups: dict[tuple[int, ...], int] = {}
            for row in rows:
                key = tuple(row[attr] for attr in group_by_attributes)

                # Aggregate last attribute of row, which is `value`
                groups[key] = groups.get(key, 0) + row[-1]

            # Append result rows
            for key, value in groups.items():
                # Fill in None for missing attributes
                result_row: list[int | None] = [None] * len(attributes)
                for i, k in zip(group_by_attributes, key):
                    result_row[i] = k

                results.append(tuple(result_row + [value]))

    return results


def test() -> None:
    for attempt in range(1, 6):
        rows = []
        for _ in range(10000):
            row = [random.randrange(2) for _ in range(6)]
            rows.append(row)

        t1 = time.perf_counter()
        results2 = group_by_cube_fast(rows)
        dt2 = time.perf_counter() - t1
        print(f"Your solution took {dt2 * 1000:.3f} millisecond.s")

        t1 = time.perf_counter()
        results1 = group_by_cube_slow(rows)
        dt1 = time.perf_counter() - t1
        print(f"The slow solution took {dt1 * 1000:.3f} milliseconds.")

        set1 = set(results1)
        set2 = set(results2)

        if set1 != set2:
            print_red("ERROR: Results differ.")
            print_red("Expected result:")
            print(results1)
            print_red("Your result:")
            print(results2)
            too_many = set2 - set1
            if too_many:
                print_red(
                    "Your result contains the following rows which are not in the expected result:"
                )
                print(too_many)
            too_few = set1 - set2
            if too_few:
                print_red("Your result is missing the following rows:")
                print(too_few)
            raise ValueError("Results differ.")

        speedup = dt1 / dt2

        print(f"Attempt {attempt}, speedup: {speedup:.2f}.\n")

        if speedup >= 30:
            return

    raise ValueError("Your solution is not fast enough.")


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[00m")


if __name__ == "__main__":
    test()
    zipme.finish(__file__, disallowed_imports={"psycopg", "sqlite"})

# 67307014460200000000
