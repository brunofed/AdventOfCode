import os
from csv import reader
import numpy as np
#from json import loads
from scipy.signal import convolve2d

def get_dir():
    return os.path.dirname(os.path.realpath(__file__))

def read(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        return [row[0] for row in reader(file)]

def read2(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        lines = file.readlines()
        return [line.rstrip() for line in lines]

def read3(filename, dir_path):
    char_to_bin = {"#":1, ".":0}
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        lines = file.readlines()
        if len(lines) == 1:
            return np.array([char_to_bin[c] for c in lines[0].rstrip()])
        else:
            return np.array([[char_to_bin[c] for c in line.rstrip()] for line in lines])

def newalgo():
    pass

def problem1(image, kernel, enhancement):
    enhanced_image = image
    for i in range(0,2):
        shape_before = np.array(enhanced_image.shape)
        fill_value = 1 - i if (enhancement[0] == 1 and enhancement[-1] == 0) else 0
        enhanced_image = enhancement[convolve2d(enhanced_image, kernel, mode='full', fillvalue=fill_value)]
        #assert np.array_equal(np.array(enhanced_image.shape), shape_before + np.array([2,2]))
    return np.count_nonzero(enhanced_image)

dir_path = get_dir()
kernel = np.array([2**i for i in range(0,9)]).reshape(3,3)

for suffix in ['_example','']:
    image = read3('image' + suffix, dir_path)
    enhancement = read3('enhancement' + suffix, dir_path)
    assert len(enhancement) == 512
    result = problem1(image, kernel, enhancement)
    pass

