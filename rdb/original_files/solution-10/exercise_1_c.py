def create_data() -> list[tuple[int, int, int]]:
    # BEGIN_SOLUTION
    import random

    data = []
    for i in range(100_000):
        # Same value for all x
        x = 0

        # y = 0 does not exist
        y = random.randint(1, 100)

        # Value of z does not matter
        z = random.randint(1, 100)

        data.append((x, y, z))

    # An index on x will be useless, because all rows have the same value for x.
    # This index can not help us to reduce the number of rows we have to filter.
    # In fact, if the database tries to use the index, it will be slower than
    # using no index at all, because it tries to filter rows, fails, and has to
    # check them all again anyway, which is slower than just checking them all
    # directly.

    # An index on (x, y), on the other hand, will be excellent, because it can
    # remove all rows immediately since we query for (x, y) = (0, 0) and there
    # is not a single row that matches this criteria.

    # Here is an example of how the different queries might look like in Python:
    """
    import time, collections

    # Our query is looking for rows with x = 0 and y = 0.
    query_x = 0
    query_y = 0

    # Building index on x
    index_on_x = collections.defaultdict(list)
    for i, (x, y, z) in enumerate(data):
        index_on_x[x].append(i)

    # Building index on x and y
    index_on_x_and_y = collections.defaultdict(list)
    for i, (x, y, z) in enumerate(data):
        index_on_x_and_y[(x, y)].append(i)

    t0 = time.perf_counter()

    # Sequential scan without index:
    result1 = []
    for x, y, z in data:
        if x == query_x and y == query_y:
            result1.append([z])

    t1 = time.perf_counter()

    # Using index on x, checking y (x is already equal to query_x, no need to check again)
    x = 0
    result2 = []
    for i in index_on_x[query_x]:
        x, y, z = data[i]
        if y == query_y:
            result2.append([z])

    t2 = time.perf_counter()

    # Using index on x and y, not checking x or y again
    x = 0
    result3 = []
    for i in index_on_x_and_y[(query_x, query_y)]:
        x, y, z = data[i]
        result3.append([z])

    t3 = time.perf_counter()

    assert result1 == result2
    assert result1 == result3

    print(f"Time full scan       : {(t1 - t0) * 1e6:.3f} µs")
    print(f"Time index on x      : {(t2 - t1) * 1e6:.3f} µs")
    print(f"Time index on x and y: {(t3 - t2) * 1e6:.3f} µs")
    """

    # END_SOLUTION
    return data
