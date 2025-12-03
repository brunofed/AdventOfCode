import math
from collections import Counter, defaultdict
from csv import reader
from dataclasses import dataclass
from itertools import pairwise, product
from json import loads
from os.path import dirname, join, realpath
from pathlib import Path
from typing import NamedTuple

import networkx as nx
import numpy as np
import pandas as pd


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


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
    return [[int(c) for c in row] for row in inputs_str]


def max_sublist(lst, k):
    # given a list of integers and k <= len(lst), find the largest k-elements sublist of non-necessarily contiguous elements where two sublists are compared lexicographically
    n = len(lst)
    assert 0 < k <= n
    result = []
    start_idx = 0
    for end_idx in range(n - k + 1, n + 1):
        moving_window = list(enumerate(lst[start_idx:end_idx], start=start_idx))
        max_idx, max_digit = max(moving_window, key=lambda x: x[1])
        result.append(max_digit)
        start_idx = max_idx + 1
    return int("".join(map(str, result)))


def problem1(inputs):
    total_output = 0
    for bank in inputs:
        pairs_of_batteries = product(tuple(enumerate(bank)), repeat=2)
        joltage = max(
            b1[1] * 10 + b2[1] for b1, b2 in pairs_of_batteries if b1[0] < b2[0]
        )
        total_output += joltage
    return total_output


def problem2(inputs):
    return sum(max_sublist(bank, 12) for bank in inputs)


if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 357,
        (problem1, "input"): 17085,
        (problem2, "input_example"): 3121910778619,
        (problem2, "input"): 169408143086082,
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
