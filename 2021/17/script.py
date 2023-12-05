import os
from csv import reader
import numpy as np
import networkx as nx

def get_dir():
    return os.path.dirname(os.path.realpath(__file__))

def read(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        return [row[0] for row in reader(file)]

def to_numpy_array(ls):
    return np.array([[int(x) for x in line] for line in ls], dtype=int)

def generate_vertices(n):
    vertices = []
    for i in range(n):
        for j in range(n):
            vertices.append((i,j))
    return vertices

def generate_edges(n, vertices):
    edges = []
    for i,j in vertices:
        if i<n-1:
            edges.append([(i,j),(i+1,j)])
        if i>0:
            edges.append([(i,j),(i-1,j)])
        if j<n-1:
            edges.append([(i,j),(i,j+1)])
        if j>0:
            edges.append([(i,j),(i,j-1)])
    return edges

def add_weights(edges, node_weights):
    for e in edges:
        # e[1] is the target vertex (i,j) of the edge that starts in e[0]
        # and the cost of going from e[0] to e[1] is the weight of (i,j)
        i = e[1][0]
        j = e[1][1]
        e.append(node_weights[i][j])
    return edges

def generate_weighted_edges(n, node_weights):
    vertices = generate_vertices(n)
    edges = generate_edges(n, vertices)
    return add_weights(edges, node_weights)

def print_path(path, n):
    visual_path = np.array([['.']*n]*n)
    for v in path:        
        visual_path[v[0]][v[1]] = 'X'
    print(visual_path)

def path_weight(path, node_weights):
    node_weights_used = [node_weights[v[0]][v[1]] for v in path]
    return sum(node_weights_used[1:]) # first vertex does not contribute to the path weight

def problem1(node_weights, n):
    edge_list = generate_weighted_edges(n, node_weights)
    G = nx.Graph()
    G.add_weighted_edges_from(edge_list)
    path = nx.dijkstra_path(G, (0,0), (n-1,n-1))
    print_path(path, n)
    return path_weight(path, node_weights)

dir_path = get_dir()
for input_file in ['node_weights_example',
                   'node_weights']:
    node_weights_ls = read(input_file, dir_path)

    node_weights = to_numpy_array(node_weights_ls)
    n = node_weights.shape[0] # it's a square, so both dimensions are the same
    result = problem1(node_weights, n)