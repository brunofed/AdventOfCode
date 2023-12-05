#import stuff
from os.path import dirname, realpath, join
from csv import reader
from json import loads

#actual math stuff
import numpy as np
from dataclasses import dataclass
from itertools import pairwise
from collections import namedtuple
from operator import add, floordiv, mul, sub, eq
from typing import Self
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

OPERATORS = {'+': add,
             '-': sub,
             '*': mul,
             '/': floordiv, # not truediv because I trust that only divisions without remainder will be necessary
             '=': eq}

OPERATORS_INVERSE = {'+': sub,
                     '-': add,
                     '*': floordiv,
                     '/': mul,
                     '=': eq}

@dataclass
class Node:
    name: str
    value: str|int
    left: Self = None
    right: Self = None
    parent: Self = None
    sibling: Self = None
    
    @property
    def is_leaf(self):
        return type(self.value) == int
    
    @property
    def is_root(self):
        return self.parent is None and self.sibling is None
    
    def compute(self):
        if self.is_leaf:
            return self.value
        return OPERATORS[self.value](self.left.compute(), self.right.compute())

    def nodes_in_subtree(self):
        if self.is_leaf:
            return [self]
        return self.left.nodes_in_subtree() + self.right.nodes_in_subtree() # concatenate the lists
    
    def find_node_in_subtree(self, node_name):
        return find_node_by_name(self.nodes_in_subtree(), node_name)
    
    def path_to_root(self):
        return [self] + ([] if self.is_root else self.parent.path_to_root())
    
    def collapse_subtree(self):
        self.value = self.compute()
        self.left = None
        self.right = None
        
def find(iterable, condition): # it's dumb, but there is no native way in Python to find an element in a list. This returns the first such element
    return next(x for x in iterable if condition(x)) # throws a StopIteration exception if no such element is found

def find_node_by_name(iterable, node_name):
    return find(iterable, lambda x: x.name==node_name)

def parse_input_str(inputs_str):
    nodes = []
    for row in inputs_str:
        name, data = row.split(': ')
        try:
            data = int(data)
            node = Node(name, data)
        except(ValueError):
            left, operation, right = data.split()
            node = Node(name, operation, left, right)
        nodes.append(node)
    for node in nodes:
        if not node.is_leaf:
            # fill the genealogical tree
            node.left = find_node_by_name(nodes, node.left)
            node.right = find_node_by_name(nodes, node.right)
            node.left.parent = node
            node.right.parent = node
            node.left.sibling = node.right
            node.right.sibling = node.left
        if node.name == 'root':
            root = node
    return root            

def problem1(root):
    return root.compute()

def solve_for(x, node):
    # step 1: find a geodesic from root to x
    path_from_root = x.path_to_root()[::-1]
    
    # step 2: collapse all vertices whose subtree does not include x. 
    # Those are exactly the children of siblings of path_from_root, starting after root
    for node in path_from_root[1:]: # exclude root by doing 1:
        node.sibling.collapse_subtree()
    # step 3: swap siblings so that the tree (under root) is
    # a path with 1 extra vertex attached to each vertex distinct from x
    # and all children to x are on the same side, say right children:
    # root
    # |___v1
    # |___v2
    #     |___v2.1
    #     |___v2.2
    #          |___...
    #          |___...
    #                 |___vn.1
    #                 |___x
    
    #CORRECTION: this cannot be done easily due to - and / not being commutative        
    # for current_node, next_node in zip(path_from_root, path_from_root[1:]):
    #     if next_node != current_node.right: # I want all nodes on this path to be the right child
    #         current_node.right, current_node.left = current_node.left, current_node.right # i.e. swap those children
    
    # step 3bis: move everything except x on the other side of root (which represents equality)
    for node in path_from_root[1:-1]: # exclude root and x
        next_on_path = node.left
        to_move = node.right
        operation = node.value
        operation_inv = OPERATORS_INVERSE[operation]
        
        node.parent.left = Node(name=node.name + '_moved',
                                value=)
    
    
    
def problem2(root):
    root.value = '='
    humn = root.find_node_in_subtree('humn')
    return solve_for(humn, root)        

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)

    result1 = problem1(input)
    result2 = problem2(input)
    pass