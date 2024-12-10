import re
import ast
import json
import zipme
from exercise_1_b import filter_outliers


def test(filename_outliers: str, filename_expected: str) -> None:
    print("Testing", filename_outliers)
    filtered_rows = filter_outliers(filename_outliers)
    with open(filename_expected, encoding="utf-8") as f:
        expected_rows = json.load(f)

    for i, ((t1, y1), (t2, y2)) in enumerate(zip(filtered_rows, expected_rows), 1):
        assert t1 == t2, f"Time for row {i} differs: {t1} != {t2}"
        assert abs(y1 - y2) < 1e-5, f"Value for t={t1} differs: {y1} != {y2}"


def test_file_content(filename: str) -> None:
    with open(filename, encoding="utf-8") as f:
        code = f.read()

    overs = list(re.findall(r"\bOVER\b", code, re.IGNORECASE))

    assert len(overs) >= 2, "You should use the OVER keyword at least twice in your code."

    tree = ast.parse(code)

    num_ast_nodes = sum(1 for _ in ast.walk(tree))

    print(f"{num_ast_nodes} Python AST nodes")

    assert (
        num_ast_nodes < 150
    ), "Your code is using too many Python statements. You should solve this exercise using as much SQL as possible."


if __name__ == "__main__":
    test("data/waterlevel_outliers1.csv", "data/waterlevel_expected1.json")
    test("data/waterlevel_outliers2.csv", "data/waterlevel_expected2.json")
    test_file_content("exercise_1_b.py")
    zipme.finish(__file__)

# 42162424623200000000
