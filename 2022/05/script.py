#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
from queue import LifoQueue
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
            return [line.rstrip().split() for line in lines]
        return [row[0] for row in reader(file)]
        
def list_of_str_to_numpy_array(inputs_str):
    return np.array(apply(int, inputs_str), dtype=int)

def to_list(numbers):
    return [loads(ls_str) for ls_str in numbers]

def apply(func, data):
    if isinstance(data, list):
        return [apply(func, x) for x in data]
    return func(data)

def transfer1(quantity, from_stack, to_stack):
    for _ in range(quantity):
        to_stack.put(from_stack.get())
    return from_stack, to_stack

def transfer2(quantity, from_stack, to_stack):
    crates_to_add = []
    for _ in range(quantity):
        crates_to_add.append(from_stack.get())
    for crate in crates_to_add[::-1]:
        to_stack.put(crate)
    return from_stack, to_stack

def transfer(num):
    return transfer1 if num==1 else transfer2

def problem(crate_stacks, moves, num):
    stacks = []
    for crate_stack in crate_stacks:
        stack = LifoQueue()
        for crate in crate_stack:
            stack.put(crate)
        stacks.append(stack)
    for move in moves:
        quantity = move[0]
        from_stack_idx = move[1]-1
        to_stack_idx = move[2]-1
        stacks[from_stack_idx], stacks[to_stack_idx] = transfer(num)(quantity, stacks[from_stack_idx], stacks[to_stack_idx])
    top_crates = ''
    for stack in stacks:
        top_crates += stack.get() #this modifies the stack
    return top_crates


crate_stacks_str = read('input_crate_stacks')
crate_stacks = [list(crate_stack) for crate_stack in crate_stacks_str]
moves_str = read('input_moves', rows_with_spaces=True)
moves = apply(int, moves_str)
#result1 = problem(crate_stacks, moves, 1)
result2 = problem(crate_stacks, moves, 2)
pass