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


def find_horizontal_symmetry(pattern, old_row=None):
    n = len(pattern)
    for i in range(1, n):
        double = 2 * i
        start, end = (0, double) if double <= n else (double - n, n)
        sliced_pattern = pattern[start:end]
        if sliced_pattern == sliced_pattern[::-1]:
            if old_row is None or i != old_row:  # I want to find a different symmetry, not the old one
                return i
    return 0  # no horizontal symmetry was found


def find_symmetry(pattern, old_row=None, old_column=None):
    row = find_horizontal_symmetry(pattern, old_row)
    pattern_transposed = np.array(pattern).T.tolist()
    column = find_horizontal_symmetry(pattern_transposed, old_column)
    return row, column


def problem1(input):
    sum = 0
    store_results = []
    for pattern in input:
        row, column = find_symmetry(pattern)
        if row == column == 0:
            raise ValueError(f"no symmetry found in pattern:\n{pattern}")
        sum += 100 * row + column
        store_results.append((pattern, row, column))
    return sum, store_results


def find_another_symmetry(pattern, old_row, old_column):
    for i, row in enumerate(pattern):
        for j, char in enumerate(row):
            new_char = "#" if char == "." else "."
            modified_pattern = deepcopy(pattern)
            modified_pattern[i][j] = new_char
            # ensure indeed only 1 symbol was modified:
            assert len([(i, j) for i, row in enumerate(pattern) for j, _ in enumerate(row) if pattern[i][j] != modified_pattern[i][j]]) == 1
            # we pass the old lines so that it starts the search after those lines,
            # to ensure it detects new lines of symmetry
            new_row, new_column = find_symmetry(modified_pattern, old_row, old_column)
            if (0, 0) != (new_row, new_column) != (old_row, old_column):  # found a new reflection
                return new_row, new_column
    raise ValueError(f"no new symmetry found in pattern:\n{pattern}")


def problem2(store_results):
    sum = 0
    for pattern, old_row, old_column in store_results:
        assert len({old_row, old_column} - {0}) == 1  # the old pattern is of the form (0, x) or (x, 0) for x!=0
        new_row, new_column = find_another_symmetry(pattern, old_row, old_column)
        if new_row != old_row:  # the new symmetry is horizontal
            sum += 100 * new_row
        elif new_column != old_column:
            sum += new_column
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

    # analogous to commutator and associator

    # for row1, row2 in zip(sliced_pattern, sliced_pattern[::-1]):
    #     palindromator = len([char1 for char1, char2 in zip(row1, row2) if char1!=char2])
    # #palindromator = len([char1 for char1, char2 in zip(sliced_pattern, sliced_pattern[::-1]) if char1 != char2])
    # if quasi_symmetry and palindromator == 1:  # sliced_patter differs in exactly 1 place with its reverse
    #     return i
    # elif not quasi_symmetry and palindromator == 0:  # sliced_pattern is a palindrome
    #     return i
