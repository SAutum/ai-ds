import zipme
import os


if __name__ == "__main__":
    assert os.path.isfile("exercise_1_a.png"), "exercise_1_a.png is missing."
    zipme.finish("exercise_1_a.txt", min_size=100, max_size=1000)

# 43611117123200000000
