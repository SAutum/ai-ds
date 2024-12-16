from test_exercise_2_a import test_query
from exercise_2_c import get_query
import zipme


def test_code() -> None:
    query = get_query()

    with open("exercise_2_c.py", encoding="utf-8") as f:
        code = f.read()

    assert "CUBE" not in code.upper(), "No CUBE allowed. Use UNION ALL instead."
    assert "ROLLUP" not in code.upper(), "No ROLLUP allowed. Use UNION ALL instead."
    assert "GROUPING" not in code.upper(), "No GROUPING allowed. Use UNION ALL instead."

    for evil in ["%", "+", "format", "f'", 'f"', "join", "{", "}", "$"]:
        assert (
            evil not in code
        ), f'Found a "{evil}" symbol, which might be string formatting. No string formatting allowed!'


if __name__ == "__main__":
    test_code()
    test_query(get_query())
    zipme.finish(__file__, allowed_imports=set())

# 75242652621000000000
