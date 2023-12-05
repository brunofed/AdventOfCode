#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise, product
from re import findall
from collections import namedtuple
import portion as P
from collections import defaultdict
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
        
def list_of_str_to_numpy_array(inputs_str):
    return np.array(apply(int, inputs_str), dtype=int)

def to_list(numbers):
    return [loads(ls_str) for ls_str in numbers]

def apply(func, data):
    if isinstance(data, list):
        return [apply(func, x) for x in data]
    return func(data)

Point = namedtuple("Point", "x y")
SensorBeaconDistance= namedtuple("Sensor_and_Beacon_and_distance", "Sensor Beacon Distance")
  
def manhattan_dist(sensor, beacon):
    return abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

def parse_input_str(inputs_str):
    sens_beac_dist = set()
    for row in inputs_str:
        pattern = r'-?\d+'
        numbers = tuple(int(s) for s in findall(pattern, row))
        sensor = Point(*numbers[:2])
        beacon = Point(*numbers[2:])
        sens_beac_dist.add(
            SensorBeaconDistance(sensor, beacon, manhattan_dist(sensor, beacon))
            )
    return sens_beac_dist

def d(i, incr=1):
    """
    shamelessly copied from https://github.com/AlexandreDecan/portion/issues/24
    this function discretize an interval (i.e. only considers integers):
    normally [0,1] with [2,3] will not result in [0,3], but after d() they do
    it even works with empty intervals
    """
    first_step = lambda s: (P.OPEN, (s.lower - incr if s.left is P.CLOSED else s.lower), (s.upper + incr if s.right is P.CLOSED else s.upper), P.OPEN)
    second_step = lambda s: (P.CLOSED, (s.lower + incr if s.left is P.OPEN and s.lower != -P.inf else s.lower), (s.upper - incr if s.right is P.OPEN and s.upper != P.inf else s.upper), P.CLOSED)
    return i.apply(first_step).apply(second_step)

# def interval_covered(sensor, distance, test_y):
#     dy = abs(test_y - sensor.y)
#     if dy > distance: # the row at test_y is too far away from the sensor
#         return P.empty()
#     dx = distance - dy
#     return P.closed(sensor.x - dx, sensor.x + dx)

def length(multi_interval):
    length = 0
    for component in multi_interval:
        length += component.upper - component.lower + 1
    return length

def covered_area(sens_beac_dist, test_y, remove_devices=True):
    empty_area = P.empty()
    for sensor, beacon, distance in sens_beac_dist:
        interval = P.empty()
        dx = distance - abs(test_y - sensor.y)
        if dx >= 0:
            interval = P.closed(sensor.x - dx, sensor.x + dx)
        # remove sensor and beacon from the covered area
        if remove_devices:
            if sensor.y == test_y:
                interval -= P.singleton(sensor.x)
            if beacon.y == test_y:
                interval -= P.singleton(beacon.x)
        empty_area = empty_area | interval
    return empty_area

def problem1(sens_beac_dist, test_y):
    return length(covered_area(sens_beac_dist, test_y))

def log(test_y, period=100_000):
    if test_y % period == 0:
        print(test_y)

def covered_area_new(sens_beac_dist, remove_devices=True):
    y_to_unused_area = defaultdict(lambda: P.empty())
    for sensor, beacon, distance in sens_beac_dist:
        # case dy==0
        y_to_unused_area[sensor.y] |= d(P.closed(sensor.x - distance, sensor.x + distance))
        for dy in range(1, distance+1):
            dx = distance - dy
            interval = d(P.closed(sensor.x - dx, sensor.x + dx))
            y_to_unused_area[sensor.y + dy] |= interval
            y_to_unused_area[sensor.y - dy] |= interval
        # remove sensor and beacon from the covered area
        if remove_devices:
            y_to_unused_area[sensor.y] -= d(P.singleton(sensor.x))
            y_to_unused_area[beacon.y] -= d(P.singleton(beacon.x))
    return y_to_unused_area

def problem2(sens_beac_dist, max_components):
    whole_row = P.closed(0,max_components)
    for test_y in range(max_components+1):
        log(test_y)
        can_contain_beacon = d(whole_row - covered_area(sens_beac_dist, test_y, False))
        if can_contain_beacon:
            assert length(can_contain_beacon) == 1 # i.e it's an interval with coinciding endpoints
            distress_beacon = Point(can_contain_beacon.lower, test_y)
            return distress_beacon.x * 4_000_000 + distress_beacon.y
        
def problem2_new(sens_beac_dist, max_components):
    whole_row = P.closed(0,max_components)
    y_to_unused_area = covered_area_new(sens_beac_dist, False)
    for interv in y_to_unused_area.values():
        can_contain_beacon = d(whole_row - interv)
        if can_contain_beacon:
            assert length(can_contain_beacon) == 1 # i.e it's an interval with coinciding endpoints
            distress_beacon = Point(can_contain_beacon.lower, test_y)
            return distress_beacon.x * 4_000_000 + distress_beacon.y
        
for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, rows_with_spaces=True)
    input = parse_input_str(inputs_str)
    
    test_y = 10 if filename=='input_example' else 2_000_000
    #result1 = problem1(input, test_y)
    
    max_components = 20 if filename=='input_example' else 4_000_000
    result2 = problem2(input, max_components)
    pass