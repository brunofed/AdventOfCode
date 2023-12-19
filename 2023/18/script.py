from dataclasses import field
from os.path import dirname, realpath, join
from csv import reader
from typing import ClassVar, List, NamedTuple
from attr import dataclass
import numpy as np
from scipy import ndimage

# from colormap import rgb2hex, hex2rgb


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


@dataclass
class Instruction:
    direction: str
    steps: int
    color_hex: str


@dataclass
class Direction:
    name: str

    @property
    def array(self):
        UP = np.array([0, -1])
        DOWN = np.array([0, 1])
        LEFT = np.array([-1, 0])
        RIGHT = np.array([1, 0])

        return {"R": RIGHT, "D": DOWN, "L": LEFT, "U": UP}[self.name]


@dataclass
class Particle:
    position: np.ndarray = np.array([0, 0])
    direction: Direction = None
    steps: int = None

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def from_instruction(self, instruction):
        self.direction = instruction.direction
        self.steps = instruction.steps

    def move(self):
        if self.direction is not None and self.steps is not None:
            self.position += self.position + self.steps * self.direction.array


@dataclass
class Boundaries:
    max_x: int = 0
    max_y: int = 0

    def update_from(self, new_position):
        x, y = new_position
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)


@dataclass
class Ground:
    boundaries: Boundaries = Boundaries()
    visited_positions: set[tuple] = set()

    def update(self, p):
        new_positions = [tuple(p.position + k * p.direction.array) for k in range(p.steps + 1)]
        self.boundaries.update_from(new_positions[-1])
        self.visited_positions.update(new_positions)

    def to_np(self):
        dimensions = (max(1, self.boundaries.max_y), max(1, self.boundaries.max_x))
        ground = np.zeros(dimensions)
        # basta
        for position in self.visited_positions:
            i, j = position
            ground[i][j] = 1
        return ground

    def plot(self):
        print()  # empty line
        print(self.to_np())


def parse_input_str(inputs_str):
    instructions = []
    for row in inputs_str:
        dir, steps, _color = row.split()
        assert _color[0] == "(" and _color[-1] == ")"
        color = _color[1:-1]
        instructions.append(Instruction(Direction(dir), int(steps), color_hex=color))
    return instructions


def problem1(input):
    particle = Particle()
    ground = Ground()
    for instruction in input:
        particle.from_instruction(instruction)
        ground.update(particle)
        particle.move()
        ground.plot()
        pass


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = None if filename == "input_example" else None
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
