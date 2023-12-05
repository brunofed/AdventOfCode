import os
from csv import reader
import numpy as np
import matplotlib.pyplot as plt

def str_to_transformation(s):
    #s is assumed to be of the form "x=100" or "y=42", i.e. with the number being a natural number
    s_split = s.split('=')
    x_or_y = s_split[0]
    if x_or_y not in ['x', 'y']:
        raise Exception(f'Expected a string of the form x= or y=, instead received {s}')
    position = int(s_split[1])
    return x_or_y, position

def transform(x_or_y, position, point):
    if point.ndim != 1:
        raise Exception(f'Expected a 2-dimensional numpy array, instead received {point}')
    if x_or_y=='x':
        if 0 <= point[0] <= position:
            return point
        reflection = np.array([[-1,0],[0,1]])
        translation = np.array([position, 0])
    else:
        if 0 <= point[1] <= position:
            return point
        reflection = np.array([[1,0],[0,-1]])
        translation = np.array([0,position])
    return reflection.dot(point - translation) + translation

def str_to_transform(s,point):
    x_or_y, position = str_to_transformation(s)
    return transform(x_or_y, position, point)

def transform_points(points, s):
    new_points_with_multiplicity = [str_to_transform(s,point) for point in points]
    new_points_distinct = {tuple(v) for v in np.array(new_points_with_multiplicity)}
    return np.array(list(new_points_distinct))

def result_problem_1(points, s, expected = None):
    results_set = transform_points(points, s)
    if expected and len(results_set) != expected:
        raise Exception('failed')
    else:
        return len(results_set)

def result_problem_2(points, transformations):
    for s in transformations:
        points = transform_points(points, s)
    x = points[:,0]
    y = points[:,1]
    plt.scatter(x, y)
    plt.show()
    return

dir_path = os.path.dirname(os.path.realpath(__file__))

points = np.genfromtxt(os.path.join(dir_path, 'points.csv'), delimiter=',', dtype=('i','i'))
transformations_file = open(os.path.join(dir_path, 'transformations.txt'), 'r')
transformations = [row[0] for row in reader(transformations_file)]

example_points = [[6,10 ],
                  [0,14 ],
                  [9,10 ],
                  [0,3  ],
                  [10,4 ],
                  [4,11 ],
                  [6,0  ],
                  [6,12 ],
                  [4,1  ],
                  [0,13 ],
                  [10,12],
                  [3,4  ],
                  [3,0  ],
                  [8,4  ],
                  [1,10 ],
                  [2,14 ],
                  [8,10 ],
                  [9,0  ]]
result_problem_1(np.array(example_points), 'y=7', 17)
result_1 = result_problem_1(points, transformations[0])
result_problem_2(points, transformations)