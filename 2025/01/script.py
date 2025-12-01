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
    results = []
    sign_dict = {"L": -1, "R": 1}
    for row in inputs_str:
        sign, num = row[0], row[1:]
        results.append(sign_dict[sign] * int(num))
    return results


def problem1(inputs):
    current = 50
    num_of_zeroes = 0
    for num in inputs:
        current = (current + num) % 100
        if current == 0:
            num_of_zeroes += 1
    return num_of_zeroes


def problem2(inputs):
    current = 50
    num_of_zeroes = 0
    for num in inputs:
        assert 0 <= current < 100
        sum = current + num
        if not (0 <= sum <= 100):
            if sum > 0:
                num_of_zeroes += sum // 100
            else:
                num_of_zeroes += (-sum // 100) + 1 if current != 0 else -sum // 100
        current = sum % 100
        if current % 100 == 0:
            num_of_zeroes += 1
    return num_of_zeroes


if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 3,
        (problem1, "input"): 1066,
        (problem2, "input_example"): 6,
        (problem2, "input"): None,
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
