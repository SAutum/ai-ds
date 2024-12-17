import itertools


def group_by_cube_fast(rows: list[list[int]]) -> list[tuple[int | None, ...]]:
    # Your solution goes here.
    # aggregation lattice

    # The first 5 attributes are `a`, `b`, `c`, `d` and `e` for GROUP BY CUBE(a, b, c, d, e).
    # The last attribute is `value`.
    attributes = [0, 1, 2, 3, 4]
    results = []
    groups_done = []

    # get total combination
    combined_rows = compute_result_rows(rows, attributes, attributes)
    results += combined_rows

    # For all attribute combinations
    length = len(attributes) - 1
    aggregation(combined_rows, length, groups_done, attributes, results)

    return results


def aggregation(rows, length, groups_done, attributes, results):
    # compute all the possible combinations based on current combination
    for group_by_attributes in itertools.combinations(attributes, length):
        if group_by_attributes in groups_done:
            continue
        else:
            groups_done.append(group_by_attributes)

        subrows = compute_result_rows(rows, group_by_attributes, attributes)
        results += subrows

        sub_length = len(group_by_attributes)

        if sub_length >= 1:
            aggregation(subrows, sub_length-1, groups_done,
                        group_by_attributes,
                        results)

    return


def compute_result_rows(subrows, group_by_attributes, attributes):
    # Compute GROUP BY of group_by_attributes
    results = []
    groups: dict[tuple[int, ...], int] = {}
    for row in subrows:
        key = tuple(row[attr] for attr in group_by_attributes)
        # Aggregate last attribute of row, which is `value`
        groups[key] = groups.get(key, 0) + row[-1]

    # Append result rows
    for key, value in groups.items():
        # Fill in None for missing attributes
        result_row: list[int | None] = [None] * (len(subrows[0]) - 1)
        for i, k in zip(group_by_attributes, key):
            result_row[i] = k

        results.append(tuple(result_row + [value]))

    return results
