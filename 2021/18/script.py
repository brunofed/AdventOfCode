import os
from csv import reader
import numpy as np
from json import loads

def get_dir():
    return os.path.dirname(os.path.realpath(__file__))

def read(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        return [row[0] for row in reader(file)]

def read2(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        lines = file.readlines()
        return [line.rstrip() for line in lines]

def to_list(snumbers_str):
    return [loads(ls_str) for ls_str in snumbers_str]

def split_regular_num(n):
    div = n//2
    return [div, div + (n%2)] #operator // rounds down, so 5//2 = 2 = floor(n/2). n%2 is either 0 or 1 so n//2 + n%2 = ceil(n/2)

def explode_one_pair(left_num, pair, right_num):
    new_left_num = pair[0] + left_num if left_num else None
    new_right_num = pair[1] + left_num if right_num else None
    return new_left_num, 0, new_right_num

def apply_one_rule(snum):
    pair_to_explode = find_pair_to_explode(snum)
    if pair_to_explode:
        return explode(snum, pair_to_explode)
    num_to_split = find_num_to_split(snum)
    if num_to_split:
        return split(snum, num_to_split)
    return None

def reduce(snum):
    while(True):
        if not apply_one_rule(snum):
            return snum

def add(snum1, snum2):
    joined_snum = [snum1, snum2]
    return reduce(joined_snum)

def magnitude(snum):
    try: #if snum is a regular integer
        mag = int(snum)
    except: #else snum is a list with 2 elements
        mag = 3*magnitude(snum[0]) + 2*magnitude(snum[1])
    return mag

def problem1(snumbers):
    sum = []
    for snum in snumbers:
        sum = add(sum, snum)
    return magnitude(sum)

dir_path = get_dir()
for input_file in ['snumbers_example',
                   'snumbers']:
    snumbers_str = read2(input_file, dir_path)

    snumbers = to_list(snumbers_str)
    result = problem1(snumbers)