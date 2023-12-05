#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from collections import Counter
import networkx as nx
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

def char_to_num(x, special_chars: dict):
    if x in special_chars:
        return special_chars[x]
    return ord(x)-ord('a')

def apply(func, data, depth=None):
    if isinstance(data, list):
        return [apply(func, x) for x in data]
    return func(data)

def to_num(input):
    num_input = [[]]
    for idx, string in enumerate(input):
        for jdx, c in enumerate(string):
            num_input[idx].append(char_to_num(c, {'S': 0, 'E': 25}))
            if c == 'S':
                source = (idx,jdx)
            if c == 'E':
                target = (idx,jdx)
        num_input.append([])
    return np.array(num_input[:-1]), source, target

def generate_graph(input):
    m, n = input.shape
    graph = nx.DiGraph()
    for i,j in np.ndindex(input.shape):
        # add edges in the following directions:
        if j+1<n and input[i, j] + 1 >= input[i, j+1]: # >
            graph.add_edge((i,j), (i,j+1))
        if i+1<m and input[i, j] + 1 >= input[i+1, j]: # v
            graph.add_edge((i,j), (i+1,j))
        if j-1>=0 and input[i, j] + 1 >= input[i, j-1]: # <
            graph.add_edge((i,j), (i,j-1))
        if i-1>=0 and input[i, j] + 1 >= input[i-1, j]: # ^
            graph.add_edge((i,j), (i-1,j))
    return graph

def problem1(graph, source, target):
    return nx.shortest_path_length(graph, source, target)

def problem2(input, graph, target):
    sources = np.argwhere(input==0)
    distances = []
    for source in sources:
        try:
            distances.append(nx.shortest_path_length(graph, tuple(source), target))
        except(nx.NetworkXNoPath): # that source cannot reach target
            pass
    return min(distances)
        

for filename in ['input_example',
                 'input']:
    input_str = read(filename)
    input, source, target = to_num(input_str)
    graph = generate_graph(input)
    
    result1 = problem1(graph, source, target)
    result2 = problem2(input, graph, target)
    pass