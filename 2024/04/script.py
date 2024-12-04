from csv import reader
from itertools import product
from os.path import dirname, join, realpath

import numpy as np


def read(filename):
    dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
        return [row[0] for row in reader(file)]


def parse_input_str(inputs_str):
    return np.array([list(row) for row in inputs_str])


def problem1(input):
    count = 0
    n, m = input.shape
    directions = [(x, y) for x, y in product([-1, 0, 1], repeat=2) if (x, y) != (0, 0)]
    for (i, j), value in np.ndenumerate(input):
        if value != "X":
            continue
        # search for ['X', 'M', 'A', 'S'] pattern in the 8 possible directions, without going out of bounds
        for di, dj in directions:
            if not (0 <= i + di * 3 < n and 0 <= j + dj * 3 < m):  # out of bounds
                continue
            # check if the pattern is present in the direction di, dj
            if all(input[i + di * k, j + dj * k] == letter for k, letter in enumerate("XMAS")):
                count += 1
    return count


def problem2(input):
    count = 0
    n, m = input.shape
    directions = list(product([-1, 1], repeat=2))
    patterns = [list(zip(directions, word)) for word in ["MSMS", "MMSS", "SMSM", "SSMM"]]

    for (i, j), value in np.ndenumerate(input):
        if value != "A":
            continue
        # search for the pattern around the 'A' without going out of bounds
        if not (1 <= i < n - 1 and 1 <= j < m - 1):  # out of bounds
            continue
        # check if the pattern is present
        for pattern in patterns:
            if all(input[i + di, j + dj] == letter for (di, dj), letter in pattern):
                count += 1
                break
    return count


for filename in ["input_example", "input"]:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)

    expected_result1 = 18 if filename == "input_example" else 2613
    assert problem1(input) == expected_result1
    expected_result2 = 9 if filename == "input_example" else 1905
    assert problem2(input) == expected_result2
pass
