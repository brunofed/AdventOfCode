#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
from collections import namedtuple
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
    return list(inputs_str[0])

@dataclass
class Shape():
    shape: set[np.ndarray]
    left_edge: np.ndarray
    bottom_edge: np.ndarray
    can_move: bool = True

minus = Shape(shape=np.array([[1,1,1,1]]), left_edge=np.array([0,0]), bottom_edge=np.array([0,0]))
plus = Shape(shape=np.array([[0,1,0],
                             [1,1,1],
                             [0,1,0]]), left_edge=np.array([1,0]), bottom_edge=np.array([1,2]))
J = Shape(shape=np.array([[0,0,1],
                          [0,0,1],
                          [1,1,1]]), left_edge=np.array([2,0]), bottom_edge=np.array([2,0]))
I = Shape(shape=np.array([[1],
                          [1],
                          [1],
                          [1]]), left_edge=np.array([0,0]), bottom_edge=np.array([3,0]))
O = Shape(shape=np.array([[1,1],
                          [1,1]]), left_edge=np.array([0,0]), bottom_edge=np.array([1,0]))

def problem1(input):
    # constants:
    chamber_width = 7
    # the new piece appears in the unique position such that:
    # - the left edge is 2 units away from the left wall
    # - the bottom edge is 3 units away from the highest piece
    new_piece_left_edge = 3
    max_height = 0 # to be updated with each new piece
    new_piece_bottom_edge = 3 + max_height
    
    piece_order = [minus, plus, J, I, O]
    piece_sequence = piece_order * 404 + piece_order[:1] # so that it's a sequence of 2022 pieces
    max_theoretical_height = 2022 * 4 + 4 # Just an arbitrary high enough number to contain all pieces. Incidentally, it's equal to 2**13 - 100
    chamber = np.zeros((max_theoretical_height, chamber_width))
    for piece in piece_sequence:
        pass

def problem2(input):
    pass

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass