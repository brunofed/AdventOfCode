#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
from typing import NamedTuple
# from collections import Counter
# import math
# import pandas as pd

def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f'{filename}.txt'), 'r') as file:
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
    for row in inputs_str:
        pass

def problem1(input):
    pass

def problem2(input):
    pass


if __name__ == '__main__':
    for filename in ['input_example',
                    'input']:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = None if filename == "input_example" else None
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass