#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
from operator import attrgetter
from dataclasses import dataclass
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

def apply(func, data):
    if isinstance(data, list):
        return [apply(func, x) for x in data]
    return func(data)

def parse_input_str(inputs_str):
    inputs_str = [s for s in inputs_str if s]
    return [eval(x) for x in inputs_str]

def pair_up_input(input):
    paired_input = []
    assert len(input) % 2 == 0
    for i in range(0, len(input), 2):
        paired_input.append([input[i], input[i+1]])
    return paired_input

def comparison(x,y):
    assert type(x) == type(y)
    list_to_int = lambda a: a if type(a)==int else len(a)
    if list_to_int(x) == list_to_int(y):
        return None
    return list_to_int(x) < list_to_int(y)

def are_right_order(x,y):
    if type(x) == type(y):
        if type(x) == int:
            return comparison(x,y)
        if type(x) == list:
            for x1,y1 in zip(x,y):
                order = are_right_order(x1,y1)
                if order is not None:
                    return order
            return comparison(x,y)
    else: # x is int and y is list or viceversa
        int_to_list = lambda a: a if type(a)==list else [a]
        return are_right_order(int_to_list(x), int_to_list(y))

def problem1(input):
    results = 0
    for idx, pair in enumerate(pair_up_input(input), start=1):
        left, right = pair
        if are_right_order(left, right):
            results += idx
    return results

def problem2(input):
    extra_item1 = [[2]]
    extra_item2 = [[6]]
    input += [extra_item1, extra_item2] # ...for reasons

    @dataclass
    class NestedListOfInt():
        item: list

        def __lt__(self, other):
            return are_right_order(self.item, other.item)

    input_class = [NestedListOfInt(x) for x in input]
    input_class.sort()
    return (input_class.index(NestedListOfInt(extra_item1))+1) * (input_class.index(NestedListOfInt(extra_item2))+1)

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, rows_with_spaces=True)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass