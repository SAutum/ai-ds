import time
import random
import matplotlib.pyplot as plt
import numpy as np


def run_experiments_and_save_plot() -> None:
    n = 5000

    fig, ax = plt.subplots(2, 3, figsize=(15, 10))

    # append a value to the list with n elements
    x, append_times = test_append(n)
    plot_subplot(ax[0, 0], x, append_times, 'list append')

    # prepending a value to a list with n elements.
    prepend_times = test_prepend(n)
    plot_subplot(ax[0, 1], x, prepend_times, 'list prepend')

    # append a character to the string with n elements
    append_times = test_append_str(n)
    plot_subplot(ax[0, 2], x, append_times, 'string append')

    # retrieve a value for a random key from a dictionary with n elements
    get_times = test_get_dict(n)
    plot_subplot(ax[1, 0], x, get_times, 'dictionary get')

    # append a (least significant) bit to an integer with n bits
    append_times = test_append_int(n)
    plot_subplot(ax[1, 1], x, append_times, 'append bit')

    # changing a bit in an integer with n bits
    change_times = test_change_int(n)
    plot_subplot(ax[1, 2], x, change_times, 'change bit')

    plt.savefig('exercise_3_a.png', dpi=800)


def eval_time(func, *args) -> float:
    start = time.time()
    func(*args)
    end = time.time()
    return end - start


def plot_subplot(ax, x, y, title, xlabel='length', ylabel='time ($ \mu s$)'):
    ax.scatter(x, y, s=0.05)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()


def test_append(n: int):
    # append a value to the list with n elements
    append_times = []
    x = []
    for i in range(1, n + 1):
        lst = list(np.random.randint(0, 100, i))
        value = random.randint(0, 100)
        append_times.append(eval_time(lst.append, value) * 1_000_000)
        x.append(i)
    return x, append_times


def test_prepend(n: int):
    # Prepending a value to a list with n elements.
    prepend_times = []
    for i in range(1, n + 1):
        lst = list(np.random.randint(0, 100, i))
        value = random.randint(0, 100)
        prepend_times.append(eval_time(lst.insert, 0, value) * 1_000_000)
    return prepend_times


def test_append_str(n: int):
    # append a character to the string with n elements
    append_times = []
    for i in range(1, n + 1):
        s = ''.join([chr(random.randint(0, 100)) for _ in range(i)])
        value = chr(random.randint(0, 100))
        append_times.append(eval_time(s.__add__, value) * 1_000_000)
    return append_times


def test_get_dict(n: int):
    # retrieve a value for a random key from a dictionary with n elements
    get_times = []
    for i in range(1, n + 1):
        d = {j: random.randint(0, 100) for j in range(i)}
        key = random.randint(0, i - 1)
        get_times.append(eval_time(d.get, key) * 1_000_000)
    return get_times


def test_append_int(n: int):
    # append a (least significant) bit to an integer with n bits
    append_times = []
    for i in range(1, n + 1):
        value = random.randint(2**(i - 1), 2**i - 1)
        bit = random.randint(0, 1)
        append_times.append(eval_time(lambda: value << 1 | bit) * 1_000_000)
    return append_times


def test_change_int(n: int):
    # changing a bit in an integer with n bits
    change_times = []
    for i in range(1, n + 1):
        value = random.randint(2**(i - 1), 2**i - 1)
        bit = random.randint(0, i - 1)
        # 1 << bit is the bit mask
        # keep all bits except the bit-th bit
        change_times.append(eval_time(lambda: value ^ (1 << bit)) * 1_000_000)
    return change_times
