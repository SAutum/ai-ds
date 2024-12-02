from exercise_1_a import Relation

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
geography["geography_id"] += list(range(4,10004))
geography["country"] += ["Germany"] * 10000
geography["city"] += [f"city{i}" for i in range(10000)]

product["product_id"] += list(range(3,10003))
product["product_name"] += [f"product{i}" for i in range(10000)]
product["price"] += [10.00] * 10000

sale["sale_id"] += list(range(11,21))
sale["geography_id"] += [1] * 10
sale["product_id"] += [1] * 10
sale["time_id"] += [1] *10

