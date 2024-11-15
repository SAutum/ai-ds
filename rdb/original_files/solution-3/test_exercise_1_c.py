from exercise_1_c import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        (4, 31),
        (5, 28),
    ]

    expected_attributes = ["product_id", "total_amount"]

    test_sql_query(get_query(), expected_attributes, expected)
    zipme.finish(__file__)

# 26025473061200000000
