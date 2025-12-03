import math
from collections import Counter, defaultdict
from csv import reader
from dataclasses import dataclass
from itertools import pairwise
from json import loads
from os.path import dirname, join, realpath
from pathlib import Path
from typing import NamedTuple

import networkx as nx
import numpy as np
import pandas as pd
from interval import Interval


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return list(reader(file))[0]


def advanced_read(
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


def apply(args, func=int):
    return list(map(func, args))


def str_to_ints(string, start_idx=0, spaces_are_meaningful=True):
    if spaces_are_meaningful:
        return apply(int, string.split()[start_idx:])
    return int(string.replace(" ", "").split(":")[-1])  # only one number


def is_within_bounds(coords, bounds):
    return all(0 <= coords[i] < bounds[i] for i in [0, 1])


def parse_input_str(inputs_str):
    ids = [range.split("-") for range in inputs_str]
    return [(int(a), int(b)) for a, b in ids]


def is_doubled(x):
    digits = list(str(x))
    n = len(digits)
    if n % 2:
        return False
    return digits[: n // 2] == digits[n // 2 :]


def is_repeated(x):
    digits = list(str(x))
    n = len(digits)
    for size in range(1, n // 2 + 1):
        if n % size:
            continue
        if all(digits[i : i + size] == digits[0:size] for i in range(0, n, size)):
            return True
    return False


def problem1(inputs):
    return sum(x for inf, sup in inputs for x in range(inf, sup + 1) if is_doubled(x))


def problem2(inputs):
    return sum(x for inf, sup in inputs for x in range(inf, sup + 1) if is_repeated(x))


if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 1227775554,
        (problem1, "input"): 19574776074,
        (problem2, "input_example"): 4174379265,
        (problem2, "input"): 25912654282,
    }
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        for problem in (problem1, problem2):
            actual_result = problem(inputs)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {actual_result=}, {expected_result=}"
    pass
