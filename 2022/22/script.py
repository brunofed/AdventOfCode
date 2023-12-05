#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
from typing import NamedTuple, ClassVar
import re
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

def str_to_num(x):
    try:
        return int(x)
    except(ValueError):
        return x

def is_in(v, l): # stupid numpy that does not have a "in" function
    return list(v) in [list(x) for x in l]

def parse_input_str(inputs_str):
    _board, _password = inputs_str[0], inputs_str[1][0]
    
    # split the password in numbers and letters
    password_split = [str_to_num(x) for x in re.findall(r'\d+|\D+', _password)]
    
    # pad the board with spaces
    max_length = max(len(x) for x in _board)
    board_padded = [x + ' '*(max_length-len(x)) for x in _board]
    board_np = np.array([list(x) for x in board_padded])
    return board_np, password_split

@dataclass
class CONSTANTS(): # ClassVar means that variable is not provided in __init__, so cannot be initialized
    #due to the origin being at the top, y-coordinates are flipped, for directions and rotations
    UP: ClassVar = np.array([0,-1])
    DOWN: ClassVar = np.array([0,1])
    LEFT: ClassVar = np.array([-1,0])
    RIGHT: ClassVar = np.array([1,0])
    
    # again, those are apparently swapped
    ROT_CLOCKWISE: ClassVar = np.array([[0, -1],
                                        [1,  0]])
    ROT_COUNTERCLOCKWISE: ClassVar = np.array([[ 0, 1],
                                               [-1, 0]])
    ROTATIONS: ClassVar = {'R': ROT_CLOCKWISE, 'L': ROT_COUNTERCLOCKWISE}

def facing_converter(p, int_output=True): # stupid numpy cannot compare easily for equality
    dir = p.momentum
    if np.array_equal(dir, CONSTANTS.RIGHT):
        return 0 if int_output else '>'
    if np.array_equal(dir, CONSTANTS.DOWN):
        return 1 if int_output else 'v'
    if np.array_equal(dir, CONSTANTS.LEFT):
        return 2 if int_output else '<' 
    if np.array_equal(dir, CONSTANTS.UP):
        return 3 if int_output else '^'
    raise Exception("unknown direction")

@dataclass
class Particle():
    position: np.ndarray
    momentum: np.ndarray
        
    @property
    def x(self):
        return self.position[0]
    
    @property
    def y(self):
        return self.position[1]
    
    def rotate_direction(self, left_or_right):
        self.momentum = np.dot(CONSTANTS.ROTATIONS[left_or_right], self.momentum)
        
    def move_1_step(self, position_at_other_end, need_to_wrap):
        if need_to_wrap:
            self.position = np.array(position_at_other_end)
        else:
            self.position += self.momentum

def index_default(lis, value, default_value):
    try:
        return lis.index(value)
    except(ValueError):
        return default_value

def find_index(lis, possible_values=['.', '#']):
    l = list(lis) # just to make sure    
    n = len(l) # which is larger than any other index in the list
    return min(index_default(l, x, n) for x in possible_values)

def reverse_find_index(lis, possible_values=['.', '#']):
    l = list(lis) # just to make sure
    n = len(l) # which is larger than any other index in the list
    return max(n - index_default(l[::-1], x, n) - 1 for x in possible_values)

def wrap_position(problem_num, filename, p, board):
    if problem_num == 1:
        dir = p.momentum
        if np.array_equal(dir, CONSTANTS.RIGHT):
            return find_index(board[p.y]), p.y
        if np.array_equal(dir, CONSTANTS.DOWN):
            return p.x, find_index(board[:, p.x])
        if np.array_equal(dir, CONSTANTS.LEFT):
            return reverse_find_index(board[p.y]), p.y
        if np.array_equal(dir, CONSTANTS.UP):
            return p.x, reverse_find_index(board[:, p.x])
        raise Exception("unknown direction")
    else:
        if filename == 'input_example':
            """
                    1111
                    1  1
                    1  1
                    1111
            222233334444
            2  23  34  4
            2  23  34  4
            222233334444
                    55556666
                    5  56  6
                    5  56  6
                    55556666
            """
            pass
        else:
            """
                11112222
                1  12  2
                1  12  2
                11112222
                3333
                3  3
                3  3
                3333
            44445555
            4  45  5
            4  45  5
            44445555
            6666
            6  6
            6  6
            6666
            """
            pass

def swap(t: tuple):
    assert len(t) == 2
    return t[1], t[0]

def next_tile_to_move(p, board, position_at_other_end, need_to_wrap):
    try:
        next_tile = board[swap(p.position + p.momentum)]
    except(IndexError):
        next_tile = None
    match next_tile:
        case '.' | '#':
            return next_tile, False
        case ' ' | None:
            return board[swap(position_at_other_end)], True
    
def plot(p, board):
    board_with_p = board.copy()
    board_with_p[p.y][p.x] = facing_converter(p, int_output=False)
    print() # empty line
    for row in board_with_p:
        print(''.join(row))

def problem(problem_num, filename, board, password):
    first_dot = np.argmax(board[0] == '.')
    starting_position = np.array([first_dot, 0])
    starting_direction = CONSTANTS.RIGHT
    p = Particle(starting_position, starting_direction)
    for command in password:
        match command:
            case int():
                for _ in range(command):
                    need_to_wrap = False
                    position_at_other_end = wrap_position(problem_num, filename, p, board)
                    next_tile, need_to_wrap = next_tile_to_move(p, board, position_at_other_end, need_to_wrap)
                    if next_tile == '.':
                        p.move_1_step(position_at_other_end, need_to_wrap)
                    #plot(p, board)
            case str():
                p.rotate_direction(command)
                #plot(p, board)
            case other:
                raise Exception('unknown command')
    
    # we had 0-based indices to insert them into numpy arrays
    return 1000*(p.y + 1) + 4*(p.x + 1) + facing_converter(p)

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, blank_rows=True)
    board_padded, password_split = parse_input_str(inputs_str)

    result1 = problem(1, filename, board_padded, password_split)
    result2 = problem(2, filename, board_padded, password_split)
    pass