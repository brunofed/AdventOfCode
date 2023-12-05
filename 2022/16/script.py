#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
import networkx as nx
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
    graph = nx.DiGraph()
    for row in inputs_str:
        valve_part, tunnels_part = row.split(';')
        valve_name = valve_part[6:8]
        rate = int(valve_part.split('=')[1])
        idx = 24 if tunnels_part[23]==' ' else 23
        tunnels = tunnels_part[idx:].split(', ')
        graph.add_node(valve_name, rate=rate)
        #nx.set_node_attributes(valve_name, rate, "rate")
        graph.add_edges_from([(valve_name, tunnel) for tunnel in tunnels])
    return graph

def neighbours(node, graph):
    return list(graph.adj._atlas[node])

def problem1(graph):
    nodes_to_rate = nx.get_node_attributes(graph, 'rate')

def problem2(input):
    pass

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, rows_with_spaces=True)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass