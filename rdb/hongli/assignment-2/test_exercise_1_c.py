from exercise_1_c import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [(9,)]

    test_sql_query(get_query(), ["any name"], expected)

    zipme.finish(__file__)

# 44705032623200000000
