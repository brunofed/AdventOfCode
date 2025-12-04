import math
from collections import Counter, defaultdict
from csv import reader
from dataclasses import dataclass
from itertools import combinations, pairwise, product
from json import loads
from os.path import dirname, join, realpath
from pathlib import Path
from typing import NamedTuple

import networkx as nx
import numpy as np
import pandas as pd


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


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


def apply(args, func=int):
    return list(map(func, args))


def str_to_ints(string, start_idx=0, spaces_are_meaningful=True):
    if spaces_are_meaningful:
        return apply(int, string.split()[start_idx:])
    return int(string.replace(" ", "").split(":")[-1])  # only one number


def is_within_bounds(coords, bounds):
    return all(0 <= coords[i] < bounds[i] for i in [0, 1])


def parse_input_str(inputs_str):
    G = nx.Graph()
    for j, row in enumerate(inputs_str):
        for i, char in enumerate(row):
            if char == "@":
                G.add_node((i, j))

    directions = {(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)}
    for v, w in combinations(G.nodes, 2):
        if (v[0] - w[0], v[1] - w[1]) in directions:
            G.add_edge(v, w)
    return G


def small_deg_vertices(G: nx.Graph, max_deg=3):
    return [node for node, degree in G.degree if degree <= max_deg]


def problem1(G):
    return len(small_deg_vertices(G))


def problem2(G: nx.Graph):
    count = 0
    while vertices := small_deg_vertices(G):
        count += len(vertices)
        G.remove_nodes_from(vertices)
    return count


if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 13,
        (problem1, "input"): 1424,
        (problem2, "input_example"): 43,
        (problem2, "input"): 8727,
    }
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        for problem in (problem1, problem2):
            actual_result = problem(inputs)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {actual_result=}, {expected_result=}"
    pass
