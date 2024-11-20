from exercise_1_g import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected_customers = [
        (0, "Mary", "Johnson"),
        (1, "John", "Williams"),
        (2, "Bill", "White"),
        (3, "Mary", "Williams"),
        (4, "Sue", "Wilson"),
        (5, "Joe", "Taylor"),
        (6, "Bill", "Brown"),
        (7, "Peter", "Brown"),
        (8, "Jane", "Thompson"),
        (9, "Peter", "Roberts"),
        (10, "Joe", "Brown"),
        (11, "Peter", "Jones"),
        (12, "Jane", "Wilson"),
        (13, "Sue", "Roberts"),
        (14, "Jane", "Wilson"),
        (15, "Mary", "Wilson"),
        (16, "Joe", "Taylor"),
        (17, "Bill", "White"),
        (18, "Sue", "Roberts"),
        (19, "Peter", "Smith"),
        (20, "Bill", None),
    ]

    test_sql_query(
        get_query(),
        [],
        [],
        expected=[
            {
                "query": "SELECT * FROM customer ORDER BY customer_id",
                "result": expected_customers,
            }
        ],
    )
    zipme.finish(__file__)

# 36511056403000000000
