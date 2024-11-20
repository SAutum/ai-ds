from exercise_1_d import get_query
from test_exercise_1_a import test_sql_query
from decimal import Decimal
import zipme

if __name__ == "__main__":
    expected = [
        (2, Decimal("70350.55")),
    ]

    expected_attributes = ["customer_id", "total_money_spent"]

    test_sql_query(get_query(), expected_attributes, expected)
    zipme.finish(__file__)

# 26330634101000000000
