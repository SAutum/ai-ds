import zipme
import os


if __name__ == "__main__":
    assert os.path.isfile("exercise_1_c.png"), "exercise_1_c.png is missing."
    zipme.finish("exercise_1_c.txt", min_size=100, max_size=1000)

# 40136173661000000000
