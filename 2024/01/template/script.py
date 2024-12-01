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


def parse_input_str(inputs_str):
    matrix = [list(map(int, row.split())) for row in inputs_str]
    np_matrix = np.array(matrix)
    return np_matrix.T


def problem1(first_col, second_col):
    first_col.sort()
    second_col.sort()
    return sum(abs(first_col - second_col))


def problem2(first_col, second_col):
    first_col_cnt, second_col_cnt = Counter(first_col), Counter(second_col)
    return sum(n * first_col_cnt[n] * second_col_cnt[n] for n in first_col_cnt)


for filename in ["input_example", "input"]:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)

    expected_result1 = 11 if filename == "input_example" else 2430334
    assert problem1(*input) == expected_result1
    expected_result2 = 31 if filename == "input_example" else 28786472
    assert problem2(*input) == expected_result2
pass
