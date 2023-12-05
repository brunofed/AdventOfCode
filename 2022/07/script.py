#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from anytree import Node, RenderTree, PostOrderIter, NodeMixin
from abc import ABC, abstractmethod
from dataclasses import dataclass
#from collections import Counter
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

@dataclass
class FolderOrFile(ABC, NodeMixin):
    name: str
    size: int

    @abstractmethod
    def total_size(self):
        pass

    def is_folder(self):
        return type(self) == Folder

@dataclass
class Folder(FolderOrFile):
    size: int = 0 #folders have 0 intrinsic size
    
    def total_size(self):
        return sum([child.total_size() for child in self.children])
    
    def is_root(self):
        return self.parent is None
    
    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        raise Exception(f'missing child {name} in folder {self.name}')
    
@dataclass
class Root(Folder):
    name: str = '/'

    def print_filesystem(self):
        print(RenderTree(self))

    def construct_filesystem(self, terminal_inputs):
        cwd = self # current working directory
        for input in terminal_inputs:
            parts = input.split()
            # it's a command
            if parts[0] == '$':
                if parts[1] == 'cd':
                    if parts[2] == self.name:
                        cwd = self
                    elif parts[2] == '..':
                        cwd = cwd.parent
                    else:
                        cwd = cwd.find_child(parts[2])                    
                else: # an 'ls' command
                    continue
            
            # it's the result of a '$ ls' command
            elif parts[0] == 'dir':
                new_folder = Folder(parts[1])
                new_folder.parent = cwd
            else:
                size = int(parts[0])
                if '.' in parts[1]:
                    name, file_type = parts[1].split('.')
                else:
                    name = parts[1]
                    file_type = ''
                new_file = File(name=name, size=size, file_type=file_type)
                new_file.parent = cwd

@dataclass
class File(FolderOrFile):
    file_type: str

    def total_size(self):
        return self.size

def problem1(terminal_inputs, threshold: int = 100_000):
    root = Root()
    root.construct_filesystem(terminal_inputs)
    small_size_total = 0
    for node in PostOrderIter(root):
        if node.is_folder():
            total_size = node.total_size()
            if total_size < threshold:
                small_size_total += total_size
    return root, small_size_total


def problem2(root):
    total_disk_space = 70_000_000
    update_space = 30_000_000
    used_space = root.total_size()
    unused_space = total_disk_space - used_space
    needed_space = update_space - unused_space

    delenda_folder_size = used_space
    for node in PostOrderIter(root):
        if node.is_folder():
            total_size = node.total_size()
            if total_size > needed_space:
                delenda_folder_size = min(delenda_folder_size, total_size)
    return delenda_folder_size

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename)

    root, result1 = problem1(inputs_str)
    result2 = problem2(root)
    pass