from exercise_1_a import create_index
import numpy as np
import matplotlib.pyplot as plt
import psycopg
import zipme
import time
import bz2
import csv
import io


def measure_query_time(cursor: psycopg.Cursor) -> tuple[float, np.ndarray]:
    with open("data/tux_without_hat_and_presents.bin", "rb") as f:
        tux_without_hat_and_presents = bz2.decompress(f.read())

    pixels = np.frombuffer(tux_without_hat_and_presents, dtype=np.uint8)
    pixels = pixels.reshape(400, 348, 3).copy()

    times = []
    for i in range(150, 255):
        for rgb_range in [
            (0, 0, 50, 200, i, i + 1),
            (50, 255, i, i + 1, 0, 0),
        ]:

            start_time = time.perf_counter()

            cursor.execute(
                """
            SELECT r, g, b, x, y FROM pixel WHERE
                %s <= r AND r <= %s AND
                %s <= g AND g <= %s AND
                %s <= b AND b <= %s
            """,
                rgb_range,
            )

            elapsed_time = time.perf_counter() - start_time

            times.append(elapsed_time)

            for r, g, b, x, y in cursor.fetchall():
                pixels[y, x] = (r, g, b)

    return min(times), pixels


def test() -> None:
    connection = psycopg.connect()

    cursor = connection.cursor()

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

    # Measure how long queries takes without index
    time_without_index, expected_pixels = measure_query_time(cursor)

    print(f"Query takes {time_without_index * 1000:.3f} milliseconds without index.")

    # Measure how long queries take with index
    cursor.execute(create_index())
    time_with_index, pixels = measure_query_time(cursor)

    assert np.allclose(
        pixels, expected_pixels
    ), "Query returns different results with index"

    speedup = time_without_index / time_with_index - 1

    print(f"Query takes {time_with_index * 1000:.3f} milliseconds with index.")

    print(f"Your query is {speedup:.3f} times faster")

    plt.imshow(pixels)
    plt.axis("off")
    plt.savefig("tux_with_presents.png")
    print("Image has been written to tux_with_presents.png")

    min_speedup = 20

    assert (
        speedup > min_speedup
    ), f"With an index, the query should be at least {min_speedup} times faster, but your query is only {speedup:.3f} times faster"


if __name__ == "__main__":
    # Run tests twice to ensure reproducibility
    for _ in range(2):
        test()
    zipme.finish(__file__)

# 34077146463000000000
