from test_exercise_2_a import test_query
from exercise_2_b import get_query
import zipme


def test_code() -> None:
    query = get_query()

    with open("exercise_2_b.py", encoding="utf-8") as f:
        code = f.read()

    assert "CUBE" not in code.upper(), "No CUBE allowed. Use GROUPING SETS instead."
    assert "ROLLUP" not in code.upper(), "No ROLLUP allowed. Use GROUPING SETS instead."
    assert "UNION" not in code.upper(), "No UNION allowed. Use GROUPING SETS instead."


if __name__ == "__main__":
    test_code()
    test_query(get_query())
    zipme.finish(__file__)

# 22713436623000000000
