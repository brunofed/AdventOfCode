#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
from dataclasses import dataclass, field
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
    pass

def problem(problem_num, input):
    mod = prod(monkey.divisible_by for monkey in input)
    num_rounds = 20 if problem_num == 1 else 10_000
    for round in range(1, num_rounds+1):
        for monkey in input:
            monkey.update_inspections()
            monkey.throw_items(problem_num, modulo=mod)
    input.sort()
    return prod(monkey.inspections for monkey in input[-2:])

@dataclass
class Monkey():
    name: int
    items: list[int]
    operation: None
    divisible_by: int
    throw_true = None
    throw_false = None
    inspections: int = 0

    def throw_to_monkey(self, x):
        return self.throw_true if x % self.divisible_by == 0 else self.throw_false
    
    def throw_items(self, problem_num, modulo):
        for x in self.items:
            operation = self.operation if problem_num==1 else lambda x: self.operation(x) % modulo
            new_x = operation(x)//3 if problem_num==1 else operation(x)
            self.throw_to_monkey(new_x).items.append(new_x)
        # all items have been thrown to other monkeys, so this monkey has no items left
        self.items = []

    def update_inspections(self):
        self.inspections += len(self.items)

    def __lt__(self, other):
        return self.inspections < other.inspections

m0 = Monkey(name=0, items=[79, 98], operation= lambda x: x * 19, divisible_by=23)
m1 = Monkey(name=1, items=[54, 65, 75, 74], operation= lambda x: x + 6, divisible_by=19)
m2 = Monkey(name=2, items=[79, 60, 97], operation= lambda x: x * x, divisible_by=13)
m3 = Monkey(name=3, items=[74], operation= lambda x: x + 3, divisible_by=17)
m0.throw_true = m2
m0.throw_false = m3
m1.throw_true = m2
m1.throw_false = m0
m2.throw_true = m1
m2.throw_false = m3
m3.throw_true = m0
m3.throw_false = m1

input_example = [m0,m1,m2,m3]

M0 = Monkey(name=0, items=[85, 79, 63, 72], operation= lambda x: x * 17, divisible_by=2)
M1 = Monkey(name=1, items=[53, 94, 65, 81, 93, 73, 57, 92], operation= lambda x: x * x, divisible_by=7)
M2 = Monkey(name=2, items=[62, 63], operation= lambda x: x + 7, divisible_by=13)
M3 = Monkey(name=3, items=[57, 92, 56], operation= lambda x: x + 4, divisible_by=5)
M4 = Monkey(name=4, items=[67], operation= lambda x: x + 5, divisible_by=3)
M5 = Monkey(name=5, items=[85, 56, 66, 72, 57, 99], operation= lambda x: x + 6, divisible_by=19)
M6 = Monkey(name=6, items=[86, 65, 98, 97, 69], operation= lambda x: x * 13, divisible_by=11)
M7 = Monkey(name=7, items=[87, 68, 92, 66, 91, 50, 68], operation= lambda x: x + 2, divisible_by=17)
M0.throw_true = M2
M0.throw_false = M6
M1.throw_true = M0
M1.throw_false = M2
M2.throw_true = M7
M2.throw_false = M6
M3.throw_true = M4
M3.throw_false = M5
M4.throw_true = M1
M4.throw_false = M5
M5.throw_true = M1
M5.throw_false = M0
M6.throw_true = M3
M6.throw_false = M7
M7.throw_true = M4
M7.throw_false = M3

input = [M0,M1,M2,M3,M4,M5,M6,M7]

# commented to reset the input
# result1_example = problem(1, input_example)
# result1 = problem(1, input)

result2_example = problem(2, input_example)
result2 = problem(2, input)
pass