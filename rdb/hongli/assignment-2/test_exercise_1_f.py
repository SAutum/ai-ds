from exercise_1_f import get_query
from test_exercise_1_a import test_sql_query
import zipme

if __name__ == "__main__":
    expected = [
        (21, "Lothar", "Wiedmann"),
        (10, "Susanne", "Stern"),
        (4, "Norbert", "Steinhauer"),
        (6, "Emil", "Schmidt"),
        (28, "Anna", "Radtke"),
        (27, "Mark", "Neumann"),
        (15, "Birgit", "Kraft"),
        (13, "Harald", "Kirschbaum"),
        (24, "Ulrike", "Jahn"),
        (9, "Maria", "Holtz"),
        (16, "Ralf", "Hey"),
        (20, "Marie", "Harter"),
        (22, "Rita", "Erdmann"),
        (25, "Abram", "Behrendt"),
    ]

    test_sql_query(get_query(), ["id", "firstname", "lastname"], expected, compare_sets=False)

    zipme.finish(__file__)

# 23222122021000000000
