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

    def hash(self, is_problem1):
        if is_problem1:
            return tuple(self.position)
        return tuple(self.position), tuple(self.momentum)


def plot(p, map, visited_positions, is_problem1=False, should_plot=False):
    if not should_plot:
        return
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


def navigate(map, starting_position, is_problem1=False, should_plot=False):
    p = Particle(starting_position, CONSTANTS.UP)
    map[starting_position] = "."  # clean map from '^'
    visited_positions = {starting_position} if is_problem1 else {p.hash(is_problem1)}
    n, m = map.shape
    while True:
        plot(p, map, visited_positions, is_problem1, should_plot)
        new_position = tuple(p.position + p.momentum)
        is_within_bound = 0 <= new_position[0] < n and 0 <= new_position[1] < m
        if not is_within_bound:  # we left the map
            if is_problem1:
                break
            return False  # ...so it's not a loop
        new_tile = map[swap(new_position)]

        if new_tile in ["#", "O"]:
            p.rotate_direction("R")
            continue
        p.position = new_position
        item = p.hash(is_problem1)
        if is_problem1:
            visited_positions.add(item)
            continue
        plot(p, map, visited_positions, is_problem1, should_plot)
        return True  # we found a loop
    plot(p, map, visited_positions, is_problem1, should_plot)
    if is_problem1:
        return visited_positions.copy()


def problem1(map, starting_position):
    visited_positions_problem1 = navigate(map, starting_position, is_problem1=True)
    return len(visited_positions_problem1), visited_positions_problem1


def problem2(map, starting_position, visited_positions_problem1, should_plot):
    loops_found = 0
    for coordinates, tile in tqdm(np.ndenumerate(map)):
        map_copy = map.copy()
        if tile in ["#", "^"]:
            continue
        # only changing a visited position can influence the path
        if coordinates not in visited_positions_problem1:
            continue
        # test if placing a O on the tile would create a loop
        map_copy[swap(coordinates)] = "O"
        loops_found += navigate(
            map_copy, starting_position, is_problem1=False, should_plot=should_plot
        )
    return loops_found


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        starting_position = swap(np.argwhere(inputs == "^")[0])
        expected_result1 = 41 if filename == "input_example" else 5404
        result, visited_positions_problem1 = problem1(inputs, starting_position)
        assert result == expected_result1
        expected_result2 = 6 if filename == "input_example" else None  # obtained 1899 but was wrong
        assert (
            problem2(inputs, starting_position, visited_positions_problem1, should_plot=False)
            == expected_result2
        )
    pass
