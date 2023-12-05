import os
from csv import reader
import numpy as np
from ast import literal_eval
from itertools import product

def get_dir():
    return os.path.dirname(os.path.realpath(__file__))

def read(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        return [row[0] for row in reader(file)]

def read2(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        lines = file.readlines()
        return [line.rstrip() for line in lines]

def problem1(alu):
    numbers = product(range(1,10))
    for rule in alu:
        l = literal_eval(rule[4])
        try:
            r = literal_eval(rule[6:])
        except:
            pass    
        operator = rule[:2]
        # if operator == 'inp':            
        # elif operator == 'add':            
        # elif operator == 'inp':
        # elif operator == 'inp':
        # elif operator == 'inp':
        
        
    pass

dir_path = get_dir()

for suffix in ['_example', '']:
    alu = read('alu' + suffix, dir_path)
    result = problem1(alu)
    pass