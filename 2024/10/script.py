from collections import defaultdict
from csv import reader
from itertools import product
from pathlib import Path

import networkx as nx
import numpy as np


def read(
    filename,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


def apply(args, func=int):
    return list(map(func, args))


def parse_input_str(inputs_str):
    return np.array([apply(row) for row in inputs_str])


def is_within_bounds(coords, bounds):
    return all(0 <= coords[i] < bounds[i] for i in [0, 1])


def problem(input, is_problem1):
    bounds = input.shape
    G = nx.DiGraph()

    # construct the graph
    for coords, value in np.ndenumerate(input):
        G.add_node(coords, value=value)
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            neighbor = direction[0] + coords[0], direction[1] + coords[1]
            if is_within_bounds(neighbor, bounds) and (input[neighbor] - value) == 1:
                G.add_edge(coords, neighbor)  # only add edge if neighbor is exactly 1 above value

    # find all paths from nodes with value 0 to nodes with value 9
    sources = []
    targets = []
    for node in G.nodes:
        value = G.nodes[node]["value"]
        if value == 0:
            sources.append(node)
        elif value == 9:
            targets.append(node)

    if is_problem1:
        path_count = sum(
            nx.has_path(G, source, target) for source, target in product(sources, targets)
        )
    else:
        path_count = len(
            [path for source in sources for path in nx.all_simple_paths(G, source, targets)]
        )
    return path_count


if __name__ == "__main__":
    for filename in [
        "input_example",
        "input",
    ]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 36 if filename == "input_example" else 624
        assert problem(input, is_problem1=True) == expected_result1
        expected_result2 = 81 if filename == "input_example" else 1483
        assert problem(input, is_problem1=False) == expected_result2
    pass
