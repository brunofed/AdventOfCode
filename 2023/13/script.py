# import stuff
from copy import deepcopy
from os.path import dirname, realpath, join
from csv import reader

import numpy as np


def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
        if blank_rows:
            grouped_rows = [[]]
            idx = 0
            for row in reader(file):
                if row:
                    grouped_rows[idx].append(row[0])
                else:
                    grouped_rows.append([])
                    idx += 1
            return grouped_rows
        if rows_with_spaces:
            lines = file.readlines()
            return [line.rstrip() for line in lines]
        return [row[0] for row in reader(file)]


def parse_input_str(inputs_str):
    return [[list(row) for row in _pattern] for _pattern in inputs_str]


def find_horizontal_symmetry(pattern):
    n = len(pattern)
    for i in range(1, n):
        double = 2 * i
        start, end = (0, double) if double <= n else (double - n, n)
        restricted_pattern = pattern[start:end]
        if restricted_pattern == restricted_pattern[::-1]:
            return i
    return 0


def find_symmetry(pattern):
    row = find_horizontal_symmetry(pattern)
    pattern_transposed = np.array(pattern).T.tolist()
    column = find_horizontal_symmetry(pattern_transposed)
    return row, column


def problem1(input):
    sum = 0
    store_results = []
    for pattern in input:
        row, column = find_symmetry(pattern)
        if row + column == 0:
            raise ValueError(f"no symmetry found in pattern:\n{pattern}")
        sum += 100 * row + column
        store_results.append((pattern, row, column))
    return sum, store_results


def problem2(store_results):
    sum = 0
    for pattern, old_row, old_column in store_results:
        # modified_pattern = []
        # for row in pattern:
        #     modified_row = []
        #     for char in row:
        #         new_char = "#" if char == "." else "."
        #         modified_row.append(new_char)
        #     modified_pattern.append(modified_row)
        modified_pattern = deepcopy(pattern)
        for i, row in enumerate(pattern):
            for j, char in enumerate(row):
                new_char = "#" if char == "." else "."
                modified_pattern[i][j] = new_char
                new_row, new_column = find_symmetry(modified_pattern)
                if (new_row, new_column) != (old_row, old_column):  # found a new reflection
                    sum += 100 * new_row + new_column
    return sum


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename, blank_rows=True)
        input = parse_input_str(inputs_str)

        expected_result1 = 405 if filename == "input_example" else 30802
        result1, store_results = problem1(input)
        assert result1 == expected_result1
        expected_result2 = 400 if filename == "input_example" else None
        assert problem2(store_results) == expected_result2
    pass
