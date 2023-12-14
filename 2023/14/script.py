# import stuff
from os.path import dirname, realpath, join
from csv import reader
import numpy as np
from tqdm import trange


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


def parse_input_str(inputs_str):
    return np.array([list(row) for row in inputs_str])


def split_list(input_list, delimiter="#"):
    sublists = []
    current_sublist = []

    for char in input_list:
        if char == delimiter:
            if current_sublist:  # Add the current sublist if it's not empty
                sublists.append(current_sublist)
            sublists.append([delimiter])  # Add a list containing delimiter
            current_sublist = []  # Reset the current_sublist
        else:
            current_sublist.append(char)

    # Add the last sublist if it's not empty
    if current_sublist:
        sublists.append(current_sublist)
    return sublists


assert split_list(list("O.#.OO.#.#")) == [["O", "."], ["#"], [".", "O", "O", "."], ["#"], ["."], ["#"]]


def tilt_north(platform):
    # transpose everything because it's easier to work with horizontal rows
    # now rock move horizontally and toward the left
    # the leftmost column has weight 10
    input_t = platform.T

    new_platform = []
    for row in input_t:  # row...that means column in the original data
        split_row = split_list(row, delimiter="#")
        # reorder elements within split_row and copy them into a new row
        new_row = []
        for sublist in split_row:
            if sublist == ["#"]:
                new_row.extend(sublist)
            else:
                sorted_sublist = sorted(sublist, key=lambda x: x == ".")  # all 'O' come before all '.'
                new_row.extend(sorted_sublist)
        new_platform.append(new_row)
    return np.array(new_platform).T  # transpose back to original


def calculate_load_on_north_beam(platform):
    total = 0
    num_rows = platform.shape[0]
    for i, row in enumerate(platform):
        load_per_rock = num_rows - i
        rocks_on_this_row = np.sum(row == "O")
        total += load_per_rock * rocks_on_this_row
    return total


def problem1(input):
    resulting_platform = tilt_north(input)
    load = calculate_load_on_north_beam(resulting_platform)
    return load


def problem2(input):
    num_cycles = 1_000_000_000
    # simpler_input = np.array([[".", "O"], [".", "#"]])
    platform = np.rot90(input)  # start anti-rotated so the first iteration set the platform back in place
    for cycle in trange(num_cycles):
        for direction in ("N", "W", "S", "E"):
            # to tilt to the left of the current direction, rotate clockwise and tilt up
            rotated_platform = np.rot90(platform, -1)
            platform = tilt_north(rotated_platform)
    load = calculate_load_on_north_beam(np.rot90(platform, -1))
    return load


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 136 if filename == "input_example" else 105623
        assert problem1(input) == expected_result1
        expected_result2 = 64 if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
