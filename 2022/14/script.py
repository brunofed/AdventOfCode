#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
from dataclasses import dataclass, field
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
    paths_of_rocks = []
    for row in inputs_str:
        pairs_str = row.split(' -> ')
        path_of_rock = []
        for pair_str in pairs_str:
            pair = apply(int, pair_str.split(','))
            path_of_rock.append(pair)
        paths_of_rocks.append(path_of_rock)
    return paths_of_rocks        

# l'asse y è rivoltato, quindi "down" vuol dire aumentare le y
down = (0,1) # fuck me
down_left = (-1,1) # devi morì
down_right = (1,1) # muori male

directions = [down, down_left, down_right]

@dataclass
class Landscape():
    obstacles: set[tuple] = field(default_factory=set)
    sand_amount: int = 0
    largest_height: int = 0
    floor: int = 0
    
    def path_of_rock(self, list_of_endpoints):
        for p, q in zip(list_of_endpoints, list_of_endpoints[1:]):
            assert p[0] == q[0] or p[1] == q[1]
            i = 1 if p[0] == q[0] else 0
            least = min(p[i], q[i])
            largest = max(p[i], q[i])
            for a in range(least, largest+1):
                rock = (p[1-i],a) if i == 1 else (a, p[1-i])
                self.obstacles.add(rock)
    
    def set_heights(self):
        self.largest_height = max([obstacle[1] for obstacle in self.obstacles])
        self.floor = self.largest_height + 2
     
    def sand_fall(self, num=1):
        sand_source = (500,0)
        sand = sand_source
        while True:
            if sand in self.obstacles: #source of sand is blocked
                break # finish the game
            
            for dir in directions:
                sand_plus_dir = (sand[0]+dir[0], sand[1]+dir[1]) # tuple do not have sum implemented
                if sand_plus_dir not in self.obstacles and sand_plus_dir[1] < self.floor:
                    sand = sand_plus_dir
                    break
            else: # all directions are blocked
                self.obstacles.add(sand)
                self.sand_amount += 1
                break
        
            if num==1 and sand[1] > self.largest_height: # sand goes into the endless void of the abyss
                break # forget about this sand
            
def problem(num, input):
    landscape = Landscape()
    for row in input:
        landscape.path_of_rock(row)
    landscape.set_heights()
    while True:
        current_amount = landscape.sand_amount
        landscape.sand_fall(num)
        if current_amount >= landscape.sand_amount: # no sand has been added
            break
    return landscape.sand_amount

def problem2(input):
    pass

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, rows_with_spaces=True)
    input = parse_input_str(inputs_str)

    result1 = problem(1, input)
    result2 = problem(2, input)
    pass