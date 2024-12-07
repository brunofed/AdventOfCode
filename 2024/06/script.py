from csv import reader
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import ClassVar

import numpy as np
from tqdm import tqdm


def read(
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


@dataclass
class CONSTANTS:  # ClassVar means that variable is not provided in __init__, so cannot be initialized
    # due to the origin being at the top, y-coordinates are flipped, for directions and rotations
    UP: ClassVar = np.array([0, -1])
    DOWN: ClassVar = np.array([0, 1])
    LEFT: ClassVar = np.array([-1, 0])
    RIGHT: ClassVar = np.array([1, 0])

    # again, those are apparently swapped
    ROT_CLOCKWISE: ClassVar = np.array([[0, -1], [1, 0]])
    ROT_COUNTERCLOCKWISE: ClassVar = np.array([[0, 1], [-1, 0]])
    ROTATIONS: ClassVar = {"R": ROT_CLOCKWISE, "L": ROT_COUNTERCLOCKWISE}


def plot_momentum(p, int_output=False):
    dir = p.momentum
    # stupid numpy cannot compare easily for equality
    if np.array_equal(dir, CONSTANTS.RIGHT):
        return 0 if int_output else ">"
    if np.array_equal(dir, CONSTANTS.DOWN):
        return 1 if int_output else "v"
    if np.array_equal(dir, CONSTANTS.LEFT):
        return 2 if int_output else "<"
    if np.array_equal(dir, CONSTANTS.UP):
        return 3 if int_output else "^"
    raise ValueError("unknown direction")


@dataclass
class Particle:
    position: np.ndarray
    momentum: np.ndarray

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def rotate_direction(self, left_or_right):
        self.momentum = np.dot(CONSTANTS.ROTATIONS[left_or_right], self.momentum)

    def to_tuple(self):
        return tuple(self.position), tuple(self.momentum)


def plot(p, map, visited_positions, is_problem1=False):
    map_with_p = map.copy()
    for position in visited_positions:
        pos = position if is_problem1 else position[0]
        map_with_p[pos[1], pos[0]] = "X"
    map_with_p[p.y][p.x] = plot_momentum(p)
    print()  # empty line
    for row in map_with_p:
        print("".join(row))


def parse_input_str(inputs_str):
    return np.array([list(row) for row in inputs_str])


def swap(t):
    t = tuple(t)
    assert len(t) == 2
    return t[1], t[0]


def navigate(map, is_problem1=False, should_plot=False):
    starting_position = swap(np.argwhere(map == "^")[0])
    p = Particle(starting_position, CONSTANTS.UP)
    map[starting_position] = "."  # clean map from '^'
    visited_positions = {starting_position} if is_problem1 else {p.to_tuple()}
    n, m = map.shape
    while True:
        if should_plot:
            plot(p, map, visited_positions, is_problem1=is_problem1)
        new_position = tuple(p.position + p.momentum)
        is_within_bound = 0 <= new_position[0] < n and 0 <= new_position[1] < m
        if not is_within_bound:
            if not is_problem1:
                return False  # we left the map, so it's not a loop
            break
        new_tile = map[swap(new_position)]

        if new_tile in ["#", "O"]:
            p.rotate_direction("R")
        else:
            p.position = new_position
            if is_problem1:
                visited_positions.add(new_position)
            else:
                item = p.to_tuple()
                if item in visited_positions:
                    return True  # we found a loop
                visited_positions.add(item)
    if is_problem1:
        return visited_positions


def problem1(map):
    visited_positions = navigate(map, is_problem1=True)
    return len(visited_positions), visited_positions


def problem2(map, visited_positions, input_example=True):
    loops_found = 0

    for coordinates, tile in tqdm(np.ndenumerate(map)):

        if tile in ["#", "^"]:
            continue
        # only changing a visited position can influence the path
        if coordinates not in visited_positions:
            continue
        map_copy = map.copy()
        # test if placing a O on the tile would create a loop
        map_copy[*coordinates] = "O"
        loops_found += navigate(map_copy, is_problem1=False, should_plot=input_example)
    return loops_found


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 41 if filename == "input_example" else 5404
        result, visited_positions = problem1(input)
        assert result == expected_result1
        expected_result2 = 6 if filename == "input_example" else None
        assert problem2(input, visited_positions) == expected_result2
    pass
