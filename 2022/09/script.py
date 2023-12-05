#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
from operator import attrgetter
from dataclasses import dataclass
import matplotlib.pyplot as plt
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
    dir_to_vec = {'U': [0,1],
                 'R': [1,0],
                 'D': [0,-1],
                 'L': [-1,0]}
    input = []
    for s in inputs_str:
        direction, repetition = s.split(' ')
        input += [np.array(dir_to_vec[direction])]*int(repetition)
    return input

def update(T, H):
    diff = H-T
    abs_diff = abs(diff)
    if all(abs_diff <= 1): # H is close enough and T does not move
        return T
    if not any(np.remainder(diff, 2)): # diff only has even entries
        return (T+H)//2
    if set(abs_diff) == {1,2}: # T and H are at "knight-jump"
        shorter_jump = np.vectorize(lambda x: x if abs(x)==1 else x//2)
        return T + shorter_jump(diff)        

def problem1(input):
    H = np.array([0,0])
    T = np.array([0,0])
    visited_by_tail = set((0,0))
    for move in input:
        H += move
        T = update(T, H)
        visited_by_tail.add(tuple(T))
    return len(visited_by_tail)

def plot(rope):
    plt.scatter(*zip(*rope))
    plt.show()

def problem2(input):
    rope = np.zeros((10, 2))
    visited_by_tail = set((0,0))
    for move in input:
        rope[0] += move
        for i in range(1, len(rope)):
            rope[i] = update(rope[i], rope[i-1])
        visited_by_tail.add(tuple(rope[-1]))
        #plot(rope)
    return len(visited_by_tail)

for filename in ['input_example',
                 'input_example2',
                 'input']:
    inputs_str = read(filename, rows_with_spaces=True)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass