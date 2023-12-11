# import stuff
from os.path import dirname, realpath, join
from csv import reader

# actual math stuff
import numpy as np
from sympy import binomial


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


def apply(func, args):
    return list(map(func, args))


def str_to_ints(string, start_idx=0, spaces_are_meaningful=True):
    if spaces_are_meaningful:
        return apply(int, string.split()[start_idx:])
    return int(string.replace(" ", "").split(":")[-1])  # only one number


def parse_input_str(inputs_str):
    return [str_to_ints(row) for row in inputs_str]


def problem(input, reverse=False):
    if reverse:
        input = [numbers[::-1] for numbers in input]
    total = 0
    for numbers in input:
        diff_rows = [np.array(numbers)]
        while True:
            new_row = np.diff(diff_rows[-1])
            diff_rows.append(np.array(new_row))
            if np.all(np.isin(new_row, new_row[0])):
                break  # row is constant
        n = len(numbers)  # the index of the place after the last element of numbers
        # for the following formula, google "Mathologer what comes next Newton" and go to 16:03
        total += sum(row[0] * binomial(n, k) for k, row in enumerate(diff_rows))
    return total


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 114 if filename == "input_example" else 1819125966
        assert problem(input) == expected_result1
        expected_result2 = 2 if filename == "input_example" else 1140
        assert problem(input, True) == expected_result2
    pass
