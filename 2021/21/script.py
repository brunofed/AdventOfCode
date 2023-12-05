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

class Player():
    def __init__(self, name, position):
        self.score = 0
        self.universes = 0
        self.name = name
        self.position = position
    
    def __ge__(self, other):
        return self.universes >= other.universes

class Players():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def current_best_player(self):
        return self.p1 if self.p1.universes > self.p2.universes else self.p2
    
    def split_universes(self):
        pass


def mod(x, n):
    return x%n if x%n else n

def problem1(p1, p2, threshold):
    i = 0
    die_rolls = 0
    while(True):
        for p in [p1, p2]:
            die_rolls += 3
            p.position = mod(p.position + mod(i+1,100) + mod(i+2,100) + mod(i+3,100),10)
            p.score += p.position
            if p.score >= threshold:
                losing_score = min(p1.score, p2.score)
                return losing_score * die_rolls
            i += 3

def problem2(p1, p2, universes):
    while(True):
        pass
            

threshold1 = 1000
p1 = Player('p1', 4)
p2 = Player('p2', 9)

result = problem1(p1, p2, threshold1)

threshold2 = 21
p1 = Player('p1', 4)
p2 = Player('p2', 8)
threed3 = {3: 1,
           4: 3,
           5: 6,
           6: 7,
           7: 6,
           8: 3,
           9: 1}
result = problem2(p1, p2, threed3, threshold2)

pass