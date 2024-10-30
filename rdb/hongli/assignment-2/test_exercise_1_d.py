from exercise_1_d import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        (4, "Duisburg"),
        (5, "Bielefeld"),
        (7, "Dortmund"),
    ]

    test_sql_query(
        get_query(),
        ["id", "cityname"],
        expected,
    )

    zipme.finish(__file__)

# 70727757403000000000
