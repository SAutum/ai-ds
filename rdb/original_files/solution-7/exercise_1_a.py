from typing import Any

Relation = dict[str, list[Any]]

# These relations here are just placeholders.
# Your relations should have the same column names though.

sale: Relation = {
    "sale_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "geography_id": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
    "product_id": [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    "time_id": [1, 2, 3, 1, 2, 1, 2, 3, 1, 2],
}

geography: Relation = {
    "geography_id": [1, 2, 3],
    "country": ["Germany", "USA", "Canada"],
    "city": ["Berlin", "New York", "Toronto"],
}

product: Relation = {
    "product_id": [1, 2],
    "product_name": ["Cosmetics", "Tetris"],
    "price": [10.00, 5.00],
}

time: Relation = {
    "time_id": [1, 2, 3],
    "month": ["January 2020", "February 2020", "March 2020"],
    "day": [1, 2, 3],
}

# BEGIN_SOLUTION

# Many sales in germany, but only five sales in the Cosmetics category
sale: Relation = {
    "sale_id": list(range(5000)),
    "geography_id": [1] * 5000,
    "product_id": [1] * 5 + [2] * 4995,
    "time_id": [1] * 5000,
}

geography: Relation = {
    "geography_id": [1, 2, 3],
    "country": ["Germany", "USA", "Canada"],
    "city": ["Berlin", "New York", "Toronto"],
}

product: Relation = {
    "product_id": [1, 2],
    "product_name": ["Cosmetics", "Toys"],
    "price": [10.00, 5.00],
}

time: Relation = {
    "time_id": [1, 2, 3],
    "month": ["January 2020", "February 2020", "March 2020"],
    "day": [1, 2, 3],
}

# END_SOLUTION
