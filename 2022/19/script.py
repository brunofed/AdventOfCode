#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
from collections import namedtuple, defaultdict
# from collections import Counter
# import math
# import pandas as pd

def read(filename, blank_rows=False, rows_with_spaces=False, colon_and_full_stops=False, dir_path=None):
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

@dataclass
class Resources():
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

@dataclass
class Robot():
    costs: Resources

@dataclass
class Blueprint():
    ID: int
    ore_robot: Robot
    clay_robot: Robot
    obsidian_robot: Robot
    geode_robot: Robot
    
    def quality_level(self, geode_num):
        return self.ID * geode_num

def parse_input_str(inputs_str):
    blueprints = []
    for row in inputs_str:
        before_colon, after_colon = row.split(': ')
        _, ID = before_colon.split()
        sentences = after_colon.split('. ')
        #blueprint = Blueprint(ID=int(ID), robots=[])
        for sentence in sentences:
            words = sentence.split()
            robot_type = words[1]
            costs = words[4:]
            robot = Robot(type=robot_type,costs=[])
            resource1 = Resource(costs[1], int(costs[0]))
            robot.costs.append(resource1)
            if 'and' in costs:
                resource2 = Resource(costs[4], int(costs[3]))
                robot.costs.append(resource2)
            blueprint.robots.append(robot)
        blueprints.append(blueprint)
    return blueprints

def problem1(input):
    minutes = 24
    initial_resources = 
    for blueprint in input:
        

def problem2(input):
    pass

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass