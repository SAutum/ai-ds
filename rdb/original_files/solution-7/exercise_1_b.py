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

# BEGIN_SOLUTION

# Very few sales, but other tables are larger
sale: Relation = {
    "sale_id": [1, 2, 3, 4, 5],
    "geography_id": [1, 1, 1, 1, 1],
    "product_id": [1, 1, 1, 1, 1],
    "time_id": [1, 1, 1, 1, 1],
}

geography: Relation = {
    "geography_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "country": ["Germany"] * 10,
    "city": [
        "Berlin",
        "Hamburg",
        "Munich",
        "Cologne",
        "Frankfurt",
        "Stuttgart",
        "Düsseldorf",
        "Dortmund",
        "Essen",
        "Leipzig",
    ],
}

product: Relation = {
    "product_id": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    ],
    "product_name": ["Cosmetics"] * 20,
    "price": [
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
    ],
}

time: Relation = {
    "time_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "month": ["January 2020"] * 10,
    "day": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
}

# END_SOLUTION
