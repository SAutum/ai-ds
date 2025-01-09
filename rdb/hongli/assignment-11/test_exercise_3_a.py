import zipme
import os
import tracemalloc
import exercise_3_a


def test() -> None:
    filename = "exercise_3_a.png"

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    exercise_3_a.run_experiments_and_save_plot()

    assert os.path.exists(
        filename
    ), f"run_experiments_and_save_plot did not create a file named {filename}"

    with open("exercise_3_a.txt", encoding="utf-8") as f:
        text = f.read()

    assert (
        len(text) >= 47
    ), f"Text in exercise_3_a.txt appears to be too short ({len(text)} characters)"
    assert len(text) < 2000, "Text in exercise_3_a.txt too long"

    print("Whether your experiments made sense will be checked manually after the deadline.")


if __name__ == "__main__":
    # Disable memory measurement for benchmark, but do not abuse this!
    # Memory limit is still 1 GB!
    tracemalloc.stop()
    test()
    zipme.finish(__file__)

# 75724611701000000000
