#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from more_itertools import windowed
# from collections import Counter
# from dataclasses import dataclass
# import math
# import pandas as pd

def read(filename, blank_rows=False, by_rows=False, only_one_line=False, dir_path=None):
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
        if only_one_line:
            lines = file.readlines()
            return lines[0].rstrip()
        if by_rows:
            lines = file.readlines()
            return [line.rstrip() for line in lines]
        return [row[0] for row in reader(file)]
        
def list_of_str_to_numpy_array(inputs_str):
    return np.array(apply(int, inputs_str), dtype=int)

def to_list(numbers):
    return [loads(ls_str) for ls_str in numbers]

def apply(func, data):
    if isinstance(data, list):
        return [apply(func, x) for x in data]
    return func(data)

def problem(inputs_str, window_size):
    for idx, window in enumerate(windowed(inputs_str, window_size)):
        if len(set(window)) == window_size:
            return idx + window_size
    return 'no marker found'

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, only_one_line=True)

    result1 = problem(inputs_str, 4)
    result2 = problem(inputs_str, 14)
    pass