#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
# from dataclasses import dataclass
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
        
def list_of_str_to_numpy_array(inputs_str):
    return np.array(apply(int, inputs_str), dtype=int)

def to_list(numbers):
    return [loads(ls_str) for ls_str in numbers]

def apply(func, data, depth=None):
    if isinstance(data, list) or (isinstance(depth, int) and depth > 0):
        return [apply(func, x, depth-1) for x in data]
    return func(data)

def problem1(calories):
    return max(calories)

def problem2(calories):
    calories.sort()
    return sum(calories[-3:])

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, blank_rows=True)
    inputs = apply(int, inputs_str)

    calories = apply(sum, inputs, depth=1)
    result1 = problem1(calories)
    result2 = problem2(calories)
    pass