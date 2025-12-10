import re
from csv import reader
from itertools import product
from pathlib import Path

import networkx as nx
import numpy as np


def advanced_read(
    filename,
    blank_rows=False,
    rows_with_spaces=False,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
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


###### START OF ACTUAL CODE ######


def parse_input_str(inputs_str):
    result = []
    for s in inputs_str:
        first_raw = re.search(r"\[(.*?)\]", s).group(1)
        second_raw = re.findall(r"\((.*?)\)", s)  # <-- only inside parens
        third_raw = re.search(r"\{(.*?)\}", s).group(1)

        # Convert blocks
        n = len(first_raw)
        first = tuple(1 if ch == "#" else 0 for ch in first_raw)
        second = []
        for block in second_raw:
            indices = list(map(int, block.split(",")))
            tuple_binary = tuple(1 if i in indices else 0 for i in range(n))
            second.append(tuple_binary)
        third = set(map(int, third_raw.split(",")))
        result.append((n, first, second, third))
    return result


def Cayley_graph(G, generators, operation):
    G.add_edges_from((v, operation(v, s)) for v, s in product(G.nodes, generators))
    return G


def mod_addition_n_dim(x, y):
    return tuple(((np.array(x) + np.array(y)) % 2).tolist())


def get_common_data(inputs):
    result = []
    for n, destination, generators, _ in inputs:
        G = nx.Graph()
        G.add_nodes_from(product({0, 1}, repeat=n))
        G = Cayley_graph(G, generators, mod_addition_n_dim)
        source = (0,) * n
        result.append((G, source, n, destination, generators, _))
    return result


def problem1(common_data):
    result = 0
    for G, source, _, destination, _, _ in common_data:
        distance = nx.dijkstra_path_length(G, source, destination)
        result += distance
    return result


def problem2(common_data):
    for G, source, _, _, _, joltage in common_data:
        pass


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 7,
        (problem1, "input"): 481,
        (problem2, "input_example"): None,
        (problem2, "input"): None,
    }
    for filename in ["input_example", "input"]:
        inputs_str = advanced_read(filename, rows_with_spaces=True)
        inputs = parse_input_str(inputs_str)
        common_data = get_common_data(inputs)
        for problem in (problem1, problem2):
            actual_result = problem(common_data)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {expected_result=}, {actual_result=}"
