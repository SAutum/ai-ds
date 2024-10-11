import typing
from exercise_1 import add
import zipme

def test_add(a: int, b: int, expected_sum: int) -> None:
    print(f"Testing {a} + {b}, which should be {expected_sum}.")

    result = add(a, b)

    assert result is not None, "The function `add` returned nothing."
    assert isinstance(result, int), "The returned value should be an int."
    assert result == expected_sum, f"Incorrect result {result}."

    print(f"Computed {a} + {b} = {result} as expected.\n")


def test() -> None:
    test_add(1, 1, 2)
    test_add(2, 3, 5)
    test_add(-1, 1, 0)


if __name__ == "__main__":
    test()
    zipme.finish(__file__)

# 42120624101200000000
