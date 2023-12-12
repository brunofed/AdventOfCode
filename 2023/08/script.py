# import stuff
from itertools import cycle
from os.path import dirname, realpath, join
from csv import reader
import re
from typing import NamedTuple


def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
        if rows_with_spaces:
            lines = file.readlines()
            return [line.rstrip() for line in lines]
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


def get_mapping(string):
    pattern = r"[^a-zA-Z0-9]"
    result = re.split(pattern, string)
    return list(filter(None, result))


def parse_input_str(inputs_str):
    rule = inputs_str[0]
    graph = {}
    for row in inputs_str[2:]:
        source, target_left, target_right = get_mapping(row)
        graph[source] = {"L": target_left, "R": target_right}
    return rule, graph


def problem1(input):
    rules, graph = input
    current_node = "AAA"
    end_node = "ZZZ"
    for step, rule in enumerate(cycle(rules), start=1):  # beware: infinite loop
        new_node = graph[current_node][rule]
        if new_node == end_node:
            break
        current_node = new_node
    return step


def problem2(input):
    rules, graph = input
    current_nodes = {node for node in graph if node.endswith("A")}
    end_nodes = {node for node in graph if node.endswith("Z")}
    for step, rule in enumerate(cycle(rules), start=1):  # beware: infinite loop
        new_nodes = {graph[current_node][rule] for current_node in current_nodes}
        if new_nodes.issubset(end_nodes):
            break
        current_nodes = new_nodes
    # while True:
    #     for step, rule in enumerate(rules, start=1):
    #         new_nodes = {graph[current_node][rule] for current_node in current_nodes}
    #         current_nodes = new_nodes
    #         if new_nodes.issubset(end_nodes):  # Z is supposed to be at the end of the cycle
    #             break
    #     if new_nodes.issubset(end_nodes):  # Z is supposed to be at the end of the cycle
    #         break
    return step


if __name__ == "__main__":
    for filename in ["input_example", "other_input", "input"]:
        inputs_str = read(filename, rows_with_spaces=True)
        input = parse_input_str(inputs_str)
        if filename == "input_example":
            expected_result1 = 2
            assert problem1(input) == expected_result1
        elif filename == "input":
            expected_result1 = 23147
            assert problem1(input) == expected_result1

        if filename == "other_input":
            expected_result2 = 6
            assert problem2(input) == expected_result2
        elif filename == "input":
            expected_result2 = None
            assert problem2(input) == expected_result2
    pass
