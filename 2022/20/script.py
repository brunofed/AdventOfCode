#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
from collections import namedtuple
from bidict import bidict
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
    return [int(row) for row in inputs_str]

def enumer(l):
    return list(zip(range(n), l)) # this distinguishes possible duplicates in l

def mix(l_enumer, l_enumer_original=None):
    """
    expected permutation at each step of 1 mixing for problem 2:
    d = {0: [811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612],
         1: [1623178306, -2434767459, 2434767459, -1623178306, 0, 811589153, 3246356612],
         2: [-2434767459, 2434767459, -1623178306, 0, 1623178306, 811589153, 3246356612],
         3: [2434767459, -1623178306, 0, -2434767459, 1623178306, 811589153, 3246356612],
         4: [-1623178306, 0, -2434767459, 2434767459, 1623178306, 811589153, 3246356612],
         5: [0, -2434767459, -1623178306, 2434767459, 1623178306, 811589153, 3246356612],
         6: [0, -2434767459, -1623178306, 2434767459, 1623178306, 811589153, 3246356612],
         7: [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153]}
    """
    if l_enumer_original is None:
        l_enumer_original = l_enumer.copy()
    for i, num in l_enumer_original:
        old_i = l_enumer.index((i,num))
        new_i = (old_i + num) % (n-1) # redundant brackets, for clarity
        if new_i == 0: # this is a matter of convention, and apparently the game prefers it this way
            new_i = n-1
        l_enumer.insert(new_i, l_enumer.pop(old_i))
    return l_enumer

def grove_sum(l_mixed_enum):
    l = [num for _, num in l_mixed_enum]
    assert len([x for x in l if x == 0]) == 1 # only one 0 must be present in l
    i_0 = l.index(0)
    return sum(l[(i_0 + i) % n] for i in [1000,2000,3000])

def problem1(l_enumerated):
    return grove_sum(mix(l_enumerated))

def problem2(l_enumerated):
    description_key = 811589153
    new_l_enumerated = [(i, x*description_key) for i, x in l_enumerated]
    new_l_enumerated_original = new_l_enumerated.copy()
    for _ in range(1, 11):
        new_l_enumerated = mix(new_l_enumerated, new_l_enumerated_original)
    return grove_sum(new_l_enumerated)

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename)
    l = parse_input_str(inputs_str)
    
    n = len(l)
    result1 = problem1(enumer(l))
    result2 = problem2(enumer(l))
    pass