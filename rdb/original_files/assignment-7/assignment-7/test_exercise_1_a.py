from exercise_1_a import sale, geography, time, product
from typing import Any
import zipme

Relation = dict[str, list[Any]]
Index = dict[tuple[Any, ...], list[int]]


def queryplan1(
    sale: Relation,
    geography_germany: Relation,
    time_january_2020: Relation,
    product_cosmetics: Relation,
) -> tuple[int, int]:
    print("Joining sale, geography, time and product (slide 15):")
    total = 0
    print(f"sale: {plural_rows(sale)}")
    result = hash_join(sale, geography_germany)
    total += relation_len(result)
    print(
        f"after joining sales with geography where Country is \"Germany\": {plural_rows(result)}, total {total} row{'' if total == 1 else 's'}"
    )
    result = hash_join(result, time_january_2020)
    total += relation_len(result)
    print(
        f"after joining with time where month is \"January 2020\": {plural_rows(result)}, total {total} row{'' if total == 1 else 's'}"
    )
    result = hash_join(result, product_cosmetics)
    total += relation_len(result)
    print(
        f"after joining with product where product_name is \"Cosmetics\": {plural_rows(result)}, total {total} row{'' if total == 1 else 's'}\n"
    )

    return total, relation_len(result)


def queryplan2(
    sale: Relation,
    geography_germany: Relation,
    time_january_2020: Relation,
    product_cosmetics: Relation,
) -> tuple[int, int]:
    print("Joining geography, time, product and sale (slide 16):")
    total = 0
    print(f'geography where Country = "Germany": {plural_rows(geography_germany)}')
    result = hash_join(geography_germany, time_january_2020)
    total += relation_len(result)
    print(
        f"after joining with time where month is \"January 2020\": {plural_rows(result)}, total {total} row{'' if total == 1 else 's'}"
    )
    result = hash_join(result, product_cosmetics)
    total += relation_len(result)
    print(
        f"after joining with product where product_name is \"Cosmetics\": {plural_rows(result)}, total {total} row{'' if total == 1 else 's'}"
    )
    result = hash_join(result, sale)
    total += relation_len(result)
    print(f"after joining with sale: {plural_rows(result)}, total {total} row{'' if total == 1 else 's'}\n")

    return total, relation_len(result)


def print_relation(relation: Relation) -> None:
    length = max((len(column) for column in relation.values()), default=0)
    widths = [len(attribute) for attribute in relation]
    columns = [["NULL"] * length for _ in relation]
    for i, column in enumerate(relation.values()):
        for j, value in enumerate(column):
            columns[i][j] = str(value)
            widths[i] = max(widths[i], len(columns[i][j]))
    rows = list(zip(*columns))

    divider = "+--" + "--+--".join("-" * width for width in widths) + "--+"
    border = "+" + "-" * (len(divider) - 2) + "+"
    headers = "|  " + "  |  ".join(attr.rjust(width) for attr, width in zip(relation, widths)) + "  |"
    print(border)
    print(headers)
    print(divider)
    for row in rows:
        print("|  " + "  |  ".join(value.rjust(width) for value, width in zip(row, widths)) + "  |")
    print(border)
    print()


def check_relation(relation: Relation) -> None:
    assert isinstance(relation, dict), "Relation must be a dictionary"
    for attribute, column in relation.items():
        assert isinstance(attribute, str), "Attribute names must be strings"
        assert isinstance(column, list), "Columns must be lists"
    column_names = list(relation.keys())
    column_lengths = [len(column) for column in relation.values()]
    for column_name, column in relation.items():
        assert (
            len(column) == column_lengths[0]
        ), f"Column {column_name} has length {len(column)}, but column {column_names[0]} has length {column_lengths[0]}. All columns should have the same length."


def relation_len(relation: Relation) -> int:
    # Return number of rows in a relation.

    # Check that the relation is valid
    check_relation(relation)

    for column in relation.values():
        return len(column)
    return 0


def make_index(index: Index, relation: Relation, attribute_names: list[str]) -> None:
    for i in range(relation_len(relation)):
        key = tuple(relation[attribute_name][i] for attribute_name in attribute_names)
        index.setdefault(key, []).append(i)


def hash_join(
    relation1: Relation,
    relation2: Relation,
) -> Relation:
    # Join two relations using their common attributes.

    # Find attributes which are common to both relations
    common_attributes = list(relation1.keys() & relation2.keys())
    # Combine attributes of both relations
    combined_attributes = relation1.keys() | relation2.keys()
    # Create a new relation with the combined attributes
    result: Relation = {attribute: [] for attribute in combined_attributes}
    # Create a hash index for the smaller relation
    index: Index = {}
    if relation_len(relation1) < relation_len(relation2):
        make_index(index, relation1, common_attributes)
        smaller_relation = relation1
        larger_relation = relation2
    else:
        make_index(index, relation2, common_attributes)
        smaller_relation = relation2
        larger_relation = relation1
    # For each row in the larger relation
    for i in range(relation_len(larger_relation)):
        key = tuple(larger_relation[attribute][i] for attribute in common_attributes)
        # For each row in the smaller relation with the same key
        for j in index.get(key, []):
            # Add the combined row to the result
            for attribute in combined_attributes:
                # Decide whether to take attribute from relation1 or relation2
                if attribute in smaller_relation:
                    result[attribute].append(smaller_relation[attribute][j])
                else:
                    result[attribute].append(larger_relation[attribute][i])

    return result


def select_where(relation: Relation, attribute: str, value: Any) -> Relation:
    return {attr: [val for i, val in enumerate(relation[attr]) if relation[attribute][i] == value] for attr in relation}


def plural_rows(relation: Relation) -> str:
    return "1 row" if relation_len(relation) == 1 else f"{relation_len(relation)} rows"


def count_intermediate_relation_size(
    sale: Relation,
    geography: Relation,
    time: Relation,
    product: Relation,
) -> tuple[int, int, int, int]:
    assert sale.keys() == {"sale_id", "geography_id", "product_id", "time_id"}
    assert geography.keys() == {"geography_id", "country", "city"}
    assert time.keys() == {"time_id", "month", "day"}
    assert product.keys() == {"product_id", "product_name", "price"}

    geography_ids = set(geography["geography_id"])
    time_ids = set(time["time_id"])
    product_ids = set(product["product_id"])

    # Check foreign keys
    for sale_id, geography_id, product_id, time_id in zip(
        sale["sale_id"],
        sale["geography_id"],
        sale["product_id"],
        sale["time_id"],
    ):
        assert (
            geography_id in geography_ids
        ), f"Invalid geography_id {geography_id} in sale with sale_id {sale_id} does not exist in geography relation"
        assert (
            time_id in time_ids
        ), f"Invalid time_id {time_id} in sale with sale_id {sale_id} does not exist in time relation"
        assert (
            product_id in product_ids
        ), f"Invalid product_id {product_id} in sale with sale_id {sale_id} does not exist in product relation"

    print(f"geography: {relation_len(geography)} rows")
    geography_germany = select_where(geography, "country", "Germany")
    print(f'after filtering for country "Germany": {plural_rows(geography_germany)}\n')

    print(f"time: {relation_len(time)} rows")
    time_january_2020 = select_where(time, "month", "January 2020")
    print(f'after filtering for month "January 2020": {plural_rows(time_january_2020)}\n')

    print(f"product: {relation_len(product)} rows")
    product_cosmetics = select_where(product, "product_name", "Cosmetics")
    print(f'after filtering for product_name "Cosmetics": {plural_rows(product_cosmetics)}\n')

    total1, length1 = queryplan1(sale, geography_germany, time_january_2020, product_cosmetics)
    total2, length2 = queryplan2(sale, geography_germany, time_january_2020, product_cosmetics)

    print("Total size of intermediate relations after joins is:")
    print(f"Execution plan slide 12: total {total1} rows after joins")
    print(f"Execution plan slide 13: total {total2} rows after joins\n")

    return total1, total2, length1, length2


def test() -> None:
    total1, total2, length1, length2 = count_intermediate_relation_size(sale, geography, time, product)

    assert (
        length1 >= 5
    ), f"The result of the first execution plan should have at least 5 rows instead of just {length1}."
    assert (
        length2 >= 5
    ), f"The result of the second execution plan should have at least 5 rows instead of just {length2}."
    assert length1 == length2, "The result of the first and second execution plan should have the same number of rows."

    assert (
        total2 * 100 <= total1
    ), "The total size of the intermediate relations during the second execution plan should be at most 1% of the total size of the intermediate relations during the first execution plan."

    print("Test passed!")


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 15341610160000000000
