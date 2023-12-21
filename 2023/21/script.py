import math
from os.path import dirname, realpath, join
from csv import reader
import networkx as nx
import numpy as np
import scipy.sparse as sp


def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
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


def apply(func, args):
    return list(map(func, args))


def str_to_ints(string, start_idx=0, spaces_are_meaningful=True):
    if spaces_are_meaningful:
        return apply(int, string.split()[start_idx:])
    return int(string.replace(" ", "").split(":")[-1])  # only one number


def parse_input_str(inputs_str):
    G = nx.grid_2d_graph(len(inputs_str), len(inputs_str[0]))
    root = None
    for i, row in enumerate(inputs_str):
        for j, char in enumerate(row):
            if char == "#":
                G.remove_node((i, j))
            elif char == "S":
                root = (i, j)
    return G, root


def power_of_2(x, exponent):
    log_2 = int(math.log2(exponent))
    if log_2 < 0:
        raise ValueError
    if log_2 == 0:
        return 1
    for _ in range(log_2 - 1):
        x = x**2
    return x


def sparse_np_to_sparse_sp(A):
    non_zero_indices = A.nonzero()
    n = len(non_zero_indices[0])
    assert n == len(non_zero_indices[1])
    # all elements are ones
    sparse_matrix = sp.coo_matrix((np.ones(n), non_zero_indices), shape=A.shape, dtype=np.intc)
    return sparse_matrix


def matrix_power_of_2(sparse_matrix, exponent):
    identity_matrix = sp.eye(sparse_matrix.shape[0], format="coo", dtype=np.intc)
    if exponent == 0:
        return identity_matrix
    current_matrix = sparse_matrix
    # Perform matrix power using a loop
    exponent_of_2 = int(math.log2(exponent))
    for _ in range(exponent_of_2):
        current_matrix = current_matrix.dot(current_matrix)

    return current_matrix.toarray()


def problem1(input):
    G, root = input
    exponent = 64
    root_index = list(G.nodes()).index(root)
    adjacency_matrix = nx.adjacency_matrix(G)
    new_adj = sparse_np_to_sparse_sp(adjacency_matrix)
    reachability_matrix = matrix_power_of_2(new_adj, exponent)
    # # this is much slower
    # adj_np = adjacency_matrix.toarray()
    # reachability_matrix = np.linalg.matrix_power(adj_np, exponent)

    reachable_from_root = reachability_matrix[root_index]
    return np.count_nonzero(reachable_from_root)


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 42 if filename == "input_example" else 3585
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
