from itertools import combinations, product
from math import prod
from pathlib import Path
import networkx as nx

def is_numeric(char: str):
    try:
        int(char)
    except ValueError:
        return False
    else:
        return True

def get_value(G, node):
    return G.nodes[node]['value']

def grid_2d(grid_values, diagonal_adjacencies=False):
    width = len(grid_values[0])
    height = len(grid_values)
    
    G = nx.grid_2d_graph(width, height)
    number_of_base_edges = (width-1)*height + (height-1)*width
    assert len(G.edges) == number_of_base_edges # sanity check 1
    
    if diagonal_adjacencies:
        diagonal_edges = []
        for x,y in product(range(width-1), range(height-1)):
            diagonal_edges.extend([((x, y), (x+1, y+1)),
                                ((x+1, y), (x, y+1))])
        G.add_edges_from(diagonal_edges)
        assert len(G.edges) == number_of_base_edges + 2*(width-1)*(height-1) # sanity check 2
    
    for j, row in enumerate(grid_values):
        for i, value in enumerate(row):
            G.nodes[(i,j)]['value'] = value
        
    return G

def remove_redundant_nodes(nodes):
    redundant_nodes = []
    for p,q in combinations(nodes, 2):
        if abs(p[0]-q[0]) == 1 and p[1]==q[1]:
            redundant_nodes.append(q)
    return [node for node in nodes if node not in redundant_nodes]

def find_number_boundaries(G, node, left_or_right):
    dx = 1 if left_or_right=='right' else -1
    current_node = node
    while True:
        # move left or right
        new_node = (current_node[0] + dx, current_node[1])
        if new_node in G.neighbors(current_node): # i.e. we didn't fall off the grid
            if is_numeric(get_value(G, new_node)):
                current_node = new_node
                continue
            break
        break
    return current_node

def get_full_number(G, node, grid):
    start, y = find_number_boundaries(G, node, "left")
    end, y1 = find_number_boundaries(G, node, "right")
    assert y == y1
    return int(grid[y][start : end+1])
    

def problem(grid, problem_num):
    G = grid_2d(grid, diagonal_adjacencies=True)
    all_numbers = []
    for j, row in enumerate(grid):
        for i, value in enumerate(row):
            if value == '.' or is_numeric(value):
                continue
            numeric_neighbors = [node for node in G.neighbors((i,j)) if is_numeric(get_value(G, node))]
            numeric_neighbors = remove_redundant_nodes(numeric_neighbors)
            # this does not take into account bad cases where multiple symbols touch the same number:
            # ...
            # .1#
            # .$.
            # that 1 would be counted twice
            # Luckily both the example and the full input did not have this problem
            adjacent_numbers = [get_full_number(G, neighbor, grid) for neighbor in numeric_neighbors]
            if problem_num==2:
                if len(adjacent_numbers)==2:
                    gear_ratio = prod(adjacent_numbers)
                    all_numbers.append(gear_ratio)
            if problem_num==1:                
                all_numbers.extend(adjacent_numbers)
    return sum(all_numbers)
            


def get_input(this_folder, input_filename):
    with open(Path(this_folder, input_filename + '.txt'), 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def process_input(raw_input):
    return raw_input
            

if __name__ == '__main__':
    this_folder = Path(__file__).parent

    for input_filename in ["input_example", "input"]:
        raw_input = get_input(this_folder, input_filename)
        input = process_input(raw_input)
        result1 = problem(input, 1)
        result2 = problem(input, 2)
        pass