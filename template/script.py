import math
from collections import Counter
from csv import reader
from dataclasses import dataclass
from itertools import pairwise
from json import loads
from os.path import dirname, join, realpath
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd


def read(
    filename,
    blank_rows=False,
    rows_with_spaces=False,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
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
    for row in inputs_str:
        pass


def problem1(input):
    pass


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = None if filename == "input_example" else None
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
