def create_data() -> list[tuple[int, int, int]]:
    # Your solution goes here.
    import numpy as np
    from numpy.random import randint
    np.random.seed(0)
    n = 100000
    data = []
    for i in range(n):
        data.append((0, i, randint(0, 152)))
    return data
