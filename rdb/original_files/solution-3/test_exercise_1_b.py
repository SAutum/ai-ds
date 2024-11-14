from exercise_1_b import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        ("Hello, Bill Brown",),
        ("Hello, Bill White",),
        ("Hello, Jane Wilson",),
        ("Hello, Joe Brown",),
        ("Hello, John Williams",),
        ("Hello, Mary Williams",),
        ("Hello, Mary Wilson",),
        ("Hello, Peter Brown",),
        ("Hello, Sue Wilson",),
    ]

    expected_attributes = ["greeting"]

    test_sql_query(get_query(), expected_attributes, expected)
    zipme.finish(__file__)

# 72716104623000000000
