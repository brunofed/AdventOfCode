# import stuff
from os.path import dirname, realpath, join
from csv import reader

# actual math stuff
import numpy as np
from itertools import combinations


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


def parse_input_str(inputs):
    char_to_num = {"#": 1, ".": 0}
    return np.array([[char_to_num[char] for char in row] for row in inputs])


def check_content(array, possible_num):
    # check that array contains only values from possible_num
    return np.all(np.isin(array, possible_num))


def find_empty_lines(input):
    return [i for i, row in enumerate(input) if check_content(row, [0])]


def problem(input, coeff):
    assert check_content(input, [0, 1])
    empty_lines = {"rows": find_empty_lines(input), "cols": find_empty_lines(input.T)}
    # transpose so that the first coordinate is the visually horizontal one.
    # It does not matter to the scope of the problem as we sum over all distances
    coords_of_ones = np.where(input.T == 1)
    galaxies = list(zip(coords_of_ones[0], coords_of_ones[1]))

    distances = []
    for (x1, y1), (x2, y2) in combinations(galaxies, 2):
        # coeff-1 because we already counted the empty lines once in the abs( )

        num_empty_cols = len([col for col in empty_lines["cols"] if x1 < col < x2])
        dx_after_expansion = abs(x1 - x2) + (coeff - 1) * num_empty_cols

        num_empty_rows = len([row for row in empty_lines["rows"] if y1 < row < y2])
        dy_after_expansion = abs(y1 - y2) + (coeff - 1) * num_empty_rows

        l1_after_expansion = dx_after_expansion + dy_after_expansion
        # test case 1:
        point5 = (1, 5)
        point9 = (4, 9)
        if point5 == (x1, y1) and point9 == (x2, y2):
            assert l1_after_expansion == 9
        # test case 2:
        point1 = (3, 0)
        point7 = (7, 8)
        if point1 == (x1, y1) and point7 == (x2, y2):
            assert l1_after_expansion == 15
        # test case 3:
        point3 = (0, 2)
        point6 = (9, 6)
        if point3 == (x1, y1) and point6 == (x2, y2):
            assert l1_after_expansion == 17
        # test case 4:
        point8 = (0, 9)
        point9 = (4, 9)
        if point8 == (x1, y1) and point9 == (x2, y2):
            assert l1_after_expansion == 5
        distances.append(l1_after_expansion)
    return sum(distances)


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 374 if filename == "input_example" else 9521776
        assert problem(input, 2) == expected_result1
        assert problem(input, 10) == 1030
        assert problem(input, 100) == 8410
        assert problem(input, 1_000_000) == None
    pass
