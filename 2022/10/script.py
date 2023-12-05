#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
import itertools
from collections import Counter
import math
import pandas as pd

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
    pass

def check_cycle_num(cycle, x, d):
    if cycle in [20, 60, 100, 140, 180, 220]:
        try: # we don't want to overwrite an already written-on dictionary
            d[cycle]
        except(KeyError):
            d[cycle] = x*cycle
    return d

def update_cycle(cycle, x, d):
    cycle += 1
    d = check_cycle_num(cycle, x, d)
    return cycle, d

def problem1(input):
    cycle = 0
    x = 1
    d = {}
    x_values = [1]
    for operation in input:
        if operation == 'noop':
            cycle, d = update_cycle(cycle, x, d)
            x_values.append(x_values[-1])
        else:
            func, num = operation.split(' ')
            assert func == 'addx'
            
            cycle, d = update_cycle(cycle, x, d)
            x_values.append(x_values[-1])
            cycle, d = update_cycle(cycle, x, d)
            x += int(num)
            x_values.append(x)
    return sum(d.values()), x_values

def problem2(x_values):
    CRT = list(range(40))*6 # i.e [[0, 1, ..., 39], [0, 1, ..., 39], [0, 1, ..., 39], [0, 1, ..., 39], [0, 1, ..., 39], [0, 1, ..., 39]]
    monitor = np.zeros([6,40])
    for idx, crt_and_x in enumerate(zip(CRT, x_values)):
        crt, x = crt_and_x
        if abs(crt-x) <= 1:
           i = idx // 40
           j = idx % 40
           monitor[i,j] = 1
    for row in monitor:
        print(''.join(['#' if j else ' ' for j in row]))
    pass

for filename in [#'input_example',
                 'input_example2',
                 'input']:
    inputs_str = read(filename)
    
    result1, x_values = problem1(inputs_str)
    result2 = problem2(x_values)
    pass