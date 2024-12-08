from collections import defaultdict
from csv import reader
from itertools import combinations
from pathlib import Path

import numpy as np


def read(
    filename,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


def parse_input_str(inputs_str):
    map = np.array([list(line) for line in inputs_str])
    antennas = [(np.array(coords), map[*coords]) for coords in np.argwhere(map != ".")]
    antennas_by_value = defaultdict(list)
    for coords, value in antennas:
        antennas_by_value[value].append(coords)
    return antennas_by_value, map.shape


def is_within_bounds(coords, bounds):
    return all(0 <= coords[i] < bounds[i] for i in [0, 1])


def antinodes_to_add(is_problem1, two_points, bounds):
    start, end = two_points
    vector = end - start
    if is_problem1:
        points = start + 2 * vector, start - vector
        return {tuple(point) for point in points if is_within_bounds(point, bounds)}
    points = set()
    for coeff in [1, -1]:
        point = np.copy(start)
        while is_within_bounds(point, bounds):
            points.add(tuple(point))
            point += coeff * vector
    return points


def problem(input, is_problem1):
    antennas_by_value, shape = input
    total_antinodes = set()
    for list_of_coords in antennas_by_value.values():
        pairs_of_coords = combinations(list_of_coords, r=2)
        for two_antennas in pairs_of_coords:
            total_antinodes |= antinodes_to_add(is_problem1, two_antennas, shape)
    return len(total_antinodes)


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 14 if filename == "input_example" else 252
        assert problem(input, is_problem1=True) == expected_result1
        expected_result2 = 34 if filename == "input_example" else 839
        assert problem(input, is_problem1=False) == expected_result2
    pass
