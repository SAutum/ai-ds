from exercise_1_e import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        (19, 2),
        (5, 2),
        (4, 2),
        (7, 2),
    ]

    expected_attributes = ["customer_id", "total_amount"]

    test_sql_query(get_query(), expected_attributes, expected)
    zipme.finish(__file__)

# 51173661061200000000
