# import stuff
from collections import Counter
from csv import reader
from dataclasses import dataclass
from itertools import pairwise
from json import loads
from os.path import dirname, join, realpath
from typing import NamedTuple

# actual math stuff
import numpy as np

# import math
# import pandas as pd


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
    list_of_rows = [np.array(apply(int, row.split())) for row in inputs_str]
    return list_of_rows


def condition(arr):
    return np.all((1 <= arr) & (arr <= 3)) or np.all((-3 <= arr) & (arr <= -1))


def problem1(input):
    diff = [np.diff(row) for row in input]
    return sum(condition(arr) for arr in diff)


def problem2(input):
    safe_rows = 0
    for row in input:
        if condition(row):
            safe_rows += 1
            continue
        new_diffs = [np.diff(np.delete(row, i)) for i, _ in enumerate(row)]
        for new_arr in new_diffs:
            if condition(new_arr):
                safe_rows += 1
                break

    return safe_rows


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 2 if filename == "input_example" else 486
        assert problem1(input) == expected_result1
        expected_result2 = 4 if filename == "input_example" else 540
        assert problem2(input) == expected_result2
    pass
