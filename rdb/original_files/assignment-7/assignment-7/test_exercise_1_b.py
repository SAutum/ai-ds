from test_exercise_1_a import count_intermediate_relation_size
from exercise_1_b import sale, geography, time, product
import zipme


def test() -> None:
    total1, total2, length1, length2 = count_intermediate_relation_size(sale, geography, time, product)

    assert (
        length1 >= 5
    ), f"The result of the first execution plan should have at least 5 rows instead of just {length1}."
    assert (
        length2 >= 5
    ), f"The result of the second execution plan should have at least 5 rows instead of just {length2}."
    assert length1 == length2, "The result of the first and second execution plan should have the same number of rows."

    assert (
        total1 * 100 <= total2
    ), "The total size of the intermediate relations during the first execution plan should be at most 1% of the total size of the intermediate relations during the second execution plan."

    print("Test passed!")


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 50040566001000000000
