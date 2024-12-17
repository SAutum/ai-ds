import itertools


def group_by_cube_fast(rows: list[list[int]]) -> list[tuple[int | None, ...]]:
    # BEGIN_SOLUTION
    attributes = [0, 1, 2, 3, 4]

    # GROUP BY (a, b, c, d, e), SUM(value)
    aggregates = {}
    for row in rows:
        key = tuple(row[:-1])
        aggregates[key] = aggregates.get(key, 0) + row[-1]

    # We can now compute all the other GROUP BY sums from the previous result,
    # of which there are not that many because there are only few different
    # values for each attribute.

    # This could be split into more aggregation steps if we had a large number
    # of aggragtes, but we don't, so it isn't.
    results = []
    for length in range(len(attributes) + 1):
        for combination in itertools.combinations(attributes, length):
            # Aggregate other combinations from precomputed aggregates,
            # of which there are much fewer than the number of rows.
            groups = {}
            for key, value in aggregates.items():
                key = tuple(
                    key[attr] if attr in combination else None for attr in attributes
                )
                groups[key] = groups.get(key, 0) + value

            # Append result rows
            for key, value in groups.items():
                row = list(key) + [value]
                results.append(tuple(row))

    return results
    # END_SOLUTION
