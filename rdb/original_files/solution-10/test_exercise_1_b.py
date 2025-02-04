from exercise_1_b import create_index_and_stuff, get_query
import numpy as np
import matplotlib.pyplot as plt
import psycopg
import zipme
import time
import bz2
import csv
import io


def test() -> None:
    connection = psycopg.connect()

    cursor = connection.cursor()

    cursor.execute("DROP INDEX IF EXISTS index_1b")

    cursor.execute("DROP TABLE IF EXISTS pixel CASCADE")

    cursor.execute(
        """
    CREATE TABLE pixel (
        r INTEGER,
        g INTEGER,
        b INTEGER,
        x INTEGER,
        y INTEGER
    )
    """
    )

    with open("data/tux_with_hat_and_presents.bin", "rb") as f:
        tux_with_hat_and_presents = bz2.decompress(f.read())

    assert len(tux_with_hat_and_presents) == 400 * 348 * 3

    f = io.StringIO()
    writer = csv.writer(f)
    i = 0
    for y in range(400):
        for x in range(348):
            r = tux_with_hat_and_presents[i]
            g = tux_with_hat_and_presents[i + 1]
            b = tux_with_hat_and_presents[i + 2]
            i += 3

            writer.writerow((r, g, b, x, y))
    f.seek(0)

    with cursor.copy("COPY pixel (r, g, b, x, y) FROM STDIN WITH CSV") as copy:
        copy.write(f.read())

    # Measure how long a query takes without index
    times = []

    for _ in range(11):
        start_time = time.perf_counter()

        cursor.execute(
            """
        SELECT r, g, b, x, y FROM pixel WHERE
            (x - 174)^2 + (y - 50)^2 BETWEEN %s^2 and %s^2
        """,
            (399, 400),
        )

        cursor.fetchall()

        elapsed_time = time.perf_counter() - start_time

        times.append(elapsed_time)

    # Choose min time
    time_without_index = min(times)
    ms = time_without_index * 1000

    print(f"Naive query takes {ms:.3f} milliseconds")

    cursor.execute(create_index_and_stuff())

    with open("data/tux_without_hat_and_presents.bin", "rb") as f:
        tux_without_hat_and_presents = bz2.decompress(f.read())

    pixels = np.frombuffer(tux_without_hat_and_presents, dtype=np.uint8)
    pixels = pixels.reshape(400, 348, 3).copy()

    times = []
    for inner_radius in range(400):
        outer_radius = inner_radius + 1

        start_time = time.perf_counter()

        cursor.execute(get_query(), (inner_radius, outer_radius))

        result = cursor.fetchall()

        elapsed_time = time.perf_counter() - start_time

        times.append(elapsed_time)

        for r, g, b, x, y in result:
            pixels[y, x] = (r, g, b)

            slop = 5

            lb = inner_radius**2 - slop
            ub = outer_radius**2 + slop

            assert (
                lb <= (x - 174) ** 2 + (y - 50) ** 2 <= ub
            ), f"Selected pixel at ({x}, {y}) is not within distance of {inner_radius} and {outer_radius} of point (174, 50)"

    time_with_index = min(times)
    ms = time_with_index * 1000

    speedup = time_without_index / time_with_index - 1

    print(f"Query takes {ms:.3f} milliseconds with additional things.")
    print(f"Your query is {speedup:.3f} times faster")

    plt.imshow(pixels)
    plt.axis("off")
    plt.savefig("tux_with_hat_and_presents.png")
    print("Image has been written to tux_with_hat_and_presents.png")

    assert (
        speedup > 8
    ), f"With an index, the query should be at least 8 times faster, but your query is only {speedup:.3f} times faster"

    expected_pixels = np.frombuffer(tux_with_hat_and_presents, dtype=np.uint8)

    error = np.sum(pixels != expected_pixels.reshape(400, 348, 3))

    assert error == 0, f"{error} pixels are not as expected"


if __name__ == "__main__":
    # Run tests twice to ensure reproducibility
    for _ in range(2):
        test()
    zipme.finish(__file__)

# 43750143660000000000
