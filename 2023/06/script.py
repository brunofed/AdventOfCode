#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
from math import inf, prod, sqrt, ceil, floor
import operator
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
def apply(func, args):
    return list(map(func, args))

def str_to_ints(string, start_idx=0, spaces_are_meaningful=True):
    if spaces_are_meaningful:
        return apply(int, string.split()[start_idx:])
    return int(string.replace(' ', '').split(':')[-1]) # only one number

def parse_input_str(inputs_str, spaces_are_meaningful=True):
    times_str, distances_str = inputs_str
    times = str_to_ints(times_str, 1, spaces_are_meaningful)
    distances = str_to_ints(distances_str, 1, spaces_are_meaningful)
    return times, distances

def solve_second_degree_equation(a, b, c):
    # roots of a*x^2 + b*x + c = 0
    d = b**2-4*a*c
    roots = []
    for sign in {1, -1}:
        roots.append((-b+sign*sqrt(d))/(2*a))
    return roots

def strict_ceil(x, integer_result=True):
    if not integer_result:
        return x
    return ceil(x) + 1 if x%1==0 else ceil(x)

def strict_floor(x, integer_result=True):
    if not integer_result:
        return x
    return floor(x) - 1 if x%1==0 else floor(x)

def solve_second_degree_inequality(a, b, c, integer_solutions=True):
    # solve a*x^2 + b*x + c > 0
    assert a != 0
    roots = solve_second_degree_equation(a, b, c)
    roots.sort()
    r1, r2 = roots
    assert r1 < r2
    if a < 0:
        return strict_ceil(r1, integer_solutions), strict_floor(r2, integer_solutions)
    return (-inf, strict_floor(r1, integer_solutions)), (strict_ceil(r2, integer_solutions), inf)

def problem1(input):
    times, distances = input
    ways_to_win = []
    for time, distance in zip(times, distances):
        # we want to solve for x the following inequality:
        # x(t-x) > d
        # where t is time and d is distance
        # and return the number of integer points between the 2 solutions.
        # Now, that inequality becomes
        # -x^2 + t*x -d > 0
        r1, r2 = solve_second_degree_inequality(-1, time, -distance)
        ways_to_win.append(r2-r1+1)
    return prod(ways_to_win)

def problem2(input):
    time, distance = input
    times = [time]
    distances = [distance]
    return problem1((times, distances))


if __name__ == '__main__':
    for filename in ['input_example',
                    'input']:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 288 if filename == "input_example" else 114400
        assert problem1(input) == expected_result1
        expected_result2 = 71503 if filename == "input_example" else 21039729
        assert problem2(parse_input_str(inputs_str, False)) == expected_result2
    pass