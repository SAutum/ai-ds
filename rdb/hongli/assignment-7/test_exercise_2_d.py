import zipme
import re

filename = "exercise_2_d.txt"


def test() -> None:
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    # Remove comments
    text = "\n".join(line for line in lines if "#" not in line).strip()

    numbers = list(re.findall("[0-9]+", text))

    assert (
        len(numbers) == 1
    ), f"Your answer should only contain a single number, but it contained multiple numbers: {numbers}"


if __name__ == "__main__":
    test()
    zipme.finish(filename, min_size=20, max_size=1000)

# 76210642720000000000
