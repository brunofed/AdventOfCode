#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
# from itertools import pairwise
# from collections import Counter
from math import prod
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
    forest = []
    for str in inputs_str:
        tree_row = [int(c) for c in str]
        forest.append(tree_row)        
    return np.array(forest)

def reverse(iterable, boolean):
    return reversed(list(iterable)) if boolean else iterable

def visibility(forest, reverse_rows=False, transpose=False): # default values imply a visibility from left
    visible_trees = {}
    for i, tree_row in enumerate(forest):
        tree_list = []
        for j, tree in reverse(enumerate(tree_row), reverse_rows):
            if not tree_list or tree > tree_list[-1]:
                tree_list.append(tree)
                index = (i,j) if not transpose else (j,i)
                visible_trees[index] = tree
    return visible_trees

def problem1(forest):
    from_left = visibility(forest)
    from_right = visibility(forest, reverse_rows=True)
    from_up = visibility(forest.T, transpose=True)
    from_down = visibility(forest.T, reverse_rows=True, transpose=True)
    
    visible_forest = from_left | from_right | from_up | from_down
    
    return len(visible_forest)

def append_if_small(value, l: list, reversed=False):
    small_values = []
    for x in reverse(l, reversed):
        small_values.append(x)
        if x >= value:
            return small_values
    return small_values

def score(i, j, tree, forest):
    viewed_trees = {}  
    viewed_trees['l'] = append_if_small(tree, forest[i][:j], reversed=True)
    viewed_trees['r'] = append_if_small(tree, forest[i][j+1:])
    viewed_trees['u'] = append_if_small(tree, forest[:, j][:i], reversed=True)
    viewed_trees['d'] = append_if_small(tree, forest[:, j][i+1:])
    
    return prod(len(value) for value in viewed_trees.values())

def problem2(forest):
    scores = set()
    n, m = forest.shape
    # trees on the edge have score=0 and can be ignored
    for i, tree_row in enumerate(forest):
        if i not in {0, n}:
            for j, tree in enumerate(tree_row):
                if j not in {0, m}:
                    scores.add(score(i, j, tree, forest))
    return max(scores)

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass