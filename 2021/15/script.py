import os
from csv import reader
import numpy as np
import pandas as pd

def get_dir():
    return os.path.dirname(os.path.realpath(__file__))

def read(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        return [row[0] for row in reader(file)]

def vec(vx,vy):
    return np.array([vx,vy])

def is_in_target_area(p, x_min, x_max, y_min, y_max):
    return (x_min <= p[0] <= x_max) and (y_min <= p[1] <= y_max)

def can_reach_target_area(p, v, x_min, x_max, y_min):
    return p[0] <= x_max and (p[0] >= x_min or v[0] > 0) and p[1] >= y_min

def drag(x):
    return max(0, abs(x)-1)

def update_position_and_velocity(p,v):
    return p+v, vec(drag(v[0]), v[1]-1)

def adjust_v0(v0, p, v, x_min, x_max, y_min):
    if p[0] > x_max:
        v0 = v0 + vec(-1,0)
    elif p[0] < x_min and v[0] <= 0:
        v0 = v0 + vec(1,0)
    elif p[1] < y_min:
        v0 = vec(v0[0], drag(v0[1]))
    return v0

def max_height_reached(origin, v0, x_min, x_max, y_min, y_max):
    while(1):
        p = origin
        v = v0
        max_height = 0
        enters_loop = False
        while(can_reach_target_area(p, v, x_min, x_max, y_min)):
            enters_loop = True
            print(f'v0 = {v0}, p = {p}, v = {v}')
            if is_in_target_area(p, x_min, x_max, y_min, y_max):
                return v0, max_height
            else:
                p,v = update_position_and_velocity(p,v)
                max_height = max(max_height, p[1])
        if not enters_loop:
            return v0, np.nan
        # it overshot, therefore we adjust the initial velocity
        v0 = adjust_v0(v0, p, v, x_min, x_max, y_min)

def problem1(x_min, x_max, y_min, y_max):
    origin = vec(0,0)
    rows = []
    for v0_x in range(0,10):
        for v0_y in range(0,10):
            v0 = vec(v0_x,v0_y)
            new_v0, max_height = max_height_reached(origin, v0, x_min, x_max, y_min, y_max)
            rows.append([v0, new_v0, max_height])
    velocity_and_heights = pd.DataFrame(rows, columns=['tentative_initial_velocity', 'initial_velocity', 'max_height'])
    return np.nanmax(velocity_and_heights.max_height)

def calculate_p_n(max_v_with_drag, n):
    return n*max_v_with_drag - n*(n-1)/2 * vec(1,1)

# def explicit_solution(origin, v0, x_min, x_max, y_min, y_max):
#     max_v_with_drag = vec(max(1,v0[0],v0[1]))
#     for n in range(0,100):
#         p_n = calculate_p_n(max_v_with_drag, n)
#     return

area_test = (20,30,-10,-5)
area = (240,292,-90,-57)

test1 = problem1(*area_test)
if test1!= 45:
    print('failed')
else:
    print('passed')
result1 = problem1(*area)
pass
