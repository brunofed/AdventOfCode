import math
from collections import Counter, defaultdict
from csv import reader
from dataclasses import dataclass
from itertools import pairwise
from json import loads
from os.path import dirname, join, realpath
from pathlib import Path
from typing import NamedTuple
from unittest import result

import numpy as np
import pandas as pd
from seaborn import residplot


def read(
    filename,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


def apply(func, args):
    return list(map(func, args))


def parse_input_str(inputs_str):
    return apply(int, inputs_str[0])


def problem1(inputs):
    blocks_str = []
    # generate the blocks string
    for i, digit in enumerate(inputs):
        string = str(i // 2) if i % 2 == 0 else "."
        blocks_str.append(string * digit)
    split_blocks = list("".join(blocks_str))
    # reorder the blocks
    next_dot = 0
    for i, item in reversed(list(enumerate(split_blocks))):
        if item == ".":
            continue
        try:
            next_dot += split_blocks[next_dot:i].index(".")
            split_blocks[next_dot], split_blocks[i] = split_blocks[i], split_blocks[next_dot]
        except ValueError:  # end of the search
            break
    # calculate checksum
    checksum = 0
    for i, item in enumerate(split_blocks):
        if item == ".":
            break  # all remaining items are not digits
        checksum += int(item) * i
    return checksum


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        expected_result1 = 1928 if filename == "input_example" else None
        assert problem1(inputs) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(inputs) == expected_result2
    pass
