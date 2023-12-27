from os.path import dirname, realpath, join
from csv import reader
from attr import dataclass
from matplotlib import pyplot as plt
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

    def get_instruction(self, instruction):
        self.direction = instruction.direction
        self.steps = instruction.steps

    def move(self):
        if self.direction is not None and self.steps is not None:
            self.position += self.steps * self.direction.array


@dataclass
class Sizes:
    max_x: int = 0
    max_y: int = 0
    min_x: int = 0
    min_y: int = 0

    def update_from(self, new_position):
        x, y = new_position
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)


@dataclass
class Ground:
    sizes: Sizes
    visited_positions: set[tuple]

    def update(self, p: Particle):
        new_positions = [tuple(p.position + k * p.direction.array) for k in range(p.steps + 1)]
        self.sizes.update_from(new_positions[-1])
        self.visited_positions.update(new_positions)

    def to_np(self):
        size_y = self.sizes.max_y - self.sizes.min_y + 1
        size_x = self.sizes.max_x - self.sizes.min_x + 1
        dimensions = (size_y, size_x)
        ground_np = np.zeros(dimensions, dtype=int)
        for position in self.visited_positions:
            i, j = position
            ground_np[j - self.sizes.min_y][i - self.sizes.min_x] = 1
        return ground_np

    def fill(self):
        return ndimage.binary_fill_holes(self.to_np()).astype(int)


def plot_binary_matrix(matrix, to_terminal=True, replace_nums_with_chars=True):
    if to_terminal:
        print()  # empty line
        if replace_nums_with_chars:
            matrix = np.where(matrix == 1, "#", ".")
        print(matrix)
    else:
        matrix_with_colors = np.zeros((*matrix.shape, 3))
        matrix_with_colors[matrix < 0.5] = [1, 1, 1]
        matrix_with_colors[matrix > 0.5] = [0, 0, 0]
        plt.imshow(matrix_with_colors)
        plt.show()


def parse_input_str(inputs_str):
    instructions = []
    for row in inputs_str:
        dir, steps, _color = row.split()
        assert _color[0] == "(" and _color[-1] == ")"
        color = _color[2:-1]
        instructions.append(Instruction(Direction(dir), int(steps), color_hex=color))
    return instructions


def problem1(input):
    particle = Particle()
    ground = Ground(Sizes(), set())
    for instruction in input:
        particle.get_instruction(instruction)
        ground.update(particle)
        particle.move()

    # plot_binary_matrix(ground.to_np())
    # plot_binary_matrix(ground.fill())

    return ground.fill().sum()


def problem2(input):
    # it takes up so much memory it crashes. Use Pick's Theorem and the Shoelace Formula
    new_instructions = []
    num_to_dir = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for instruction in input:
        new_direction = num_to_dir[instruction.color_hex[-1]]
        new_steps = int(instruction.color_hex[:-1], 16)
        new_instruction = Instruction(Direction(new_direction), new_steps, "")
        new_instructions.append(new_instruction)
    return problem1(new_instructions)


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 62 if filename == "input_example" else 40714
        assert problem1(input) == expected_result1
        expected_result2 = 952408144115 if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
