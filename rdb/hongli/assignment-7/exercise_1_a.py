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

# Your solution goes here.

sale: Relation = {
    "sale_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "geography_id": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
    "product_id": [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    "time_id": [1, 2, 3, 1, 2, 1, 2, 3, 1, 2],
}

sale_attributes = sale.keys()

# add 5 sale records with Germany, Cosmetics, January 2020
for i in range(5):
    sale["sale_id"].append(i + 11)
    sale["geography_id"].append(1)
    sale["product_id"].append(1)
    sale["time_id"].append(1)

# add 1000 sale records with Germany, Cosmetics, Februrary 2020
# sale join geography will be a huge relation
for i in range(1000):
    sale["sale_id"].append(i + 16)
    sale["geography_id"].append(1)
    sale["product_id"].append(1)
    sale["time_id"].append(2)
