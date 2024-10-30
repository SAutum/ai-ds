from exercise_1_e import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        (7, "Sigrid", "Kleinschmidt"),
        (17, "Sabrina", "Scholz"),
        (18, "Ira", "Schnabel"),
        (25, "Abram", "Behrendt"),
        (30, "Sofia", "Springer"),
    ]

    test_sql_query(
        get_query(),
        ["id", "firstname", "lastname"],
        expected,
    )

    zipme.finish(__file__)

# 76704751140000000000
