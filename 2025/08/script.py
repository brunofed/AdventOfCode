from csv import reader
from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row for row in reader(file)]


###### START OF ACTUAL CODE ######


def parse_input_str(inputs_str):
    return [tuple(map(int, row)) for row in inputs_str]


def get_common_data(boxes):
    pairs_by_distance = sorted(
        [(p, q) for p, q in combinations(boxes, 2)],
        key=lambda pair: np.linalg.norm(np.array(pair[0]) - np.array(pair[1])),
    )
    G = nx.Graph()
    G.add_nodes_from(boxes)
    return G, pairs_by_distance


def problem1(filename, G, pairs_by_distance):
    num_connections = 10 if filename == "input_example" else 1000
    G.add_edges_from(pairs_by_distance[:num_connections])

    # calculate the result
    components = list(nx.connected_components(G))
    sorted_sizes = [len(c) for c in sorted(components, key=len, reverse=True)]
    return int(np.prod(sorted_sizes[:3]))


def problem2(_, G, pairs_by_distance):
    for edge in pairs_by_distance:
        u, v = edge
        G.add_edge(u, v)
        if nx.is_connected(G):
            return u[0] * v[0]


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 40,
        (problem1, "input"): 129564,
        (problem2, "input_example"): 25272,
        (problem2, "input"): 42047840,
    }
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        common_data = get_common_data(inputs)
        for problem in (problem1, problem2):
            actual_result = problem(filename, *common_data)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {expected_result=}, {actual_result=}"
    pass
