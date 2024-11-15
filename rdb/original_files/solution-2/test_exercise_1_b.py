from exercise_1_b import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        (6, "Emil", "Schmidt"),
        (11, "Lore", "Schmidt"),
        (17, "Sabrina", "Scholz"),
        (18, "Ira", "Schnabel"),
    ]

    test_sql_query(
        get_query(),
        ["id", "firstname", "lastname"],
        expected,
    )

    zipme.finish(__file__)

# 55752330003200000000
