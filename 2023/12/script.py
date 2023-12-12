# import stuff
from itertools import pairwise
from os.path import dirname, realpath, join
from csv import reader
from sympy import binomial


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
        return [row[0] for row in reader(file)]


def apply(func, args):
    return list(map(func, args))


def str_to_ints(string, delimiter=" ", start_idx=0, spaces_are_meaningful=True):
    if spaces_are_meaningful:
        return apply(int, string.split(delimiter)[start_idx:])
    return int(string.replace(" ", "").split(":")[-1])  # only one number


def split_string(input_string):
    # sample input: "abccdddeeeeffff"
    # output: ['a', 'b', 'cc', 'ddd', 'eeee', 'ffff']
    result = [input_string[0]]
    for char, char_next in pairwise(input_string[1:]):
        if char != char_next:
            result.append(char)
        else:
            result[-1] += char
    return result


def parse_input_str(inputs_str):
    springs_and_numbers = []
    for row in inputs_str:
        springs, numbers_str = row.split()
        springs_split = split_string(springs)
        numbers = str_to_ints(numbers_str, delimiter=",")
        springs_and_numbers.append((springs_split, numbers))
    return springs_and_numbers


def base_case(springs, numbers):
    # this works for the simplest case, made only of ?: ???????
    num_springs = len(springs)
    assert springs == "?" * num_springs
    num_numbers = len(numbers)
    # I call 'stars' the spaces between padded springs, as customary in combinatorics
    # by padded springs I mean: ### becomes ###. since every streak of springs needs a . to be separated by the next streak
    num_stars = num_springs - (sum(numbers) + num_numbers - 1)
    assert num_stars >= 0
    # the following in combinatorics is called a Composition, see wikipedia page
    return binomial(num_numbers + num_stars, num_numbers)


def problem1(input):
    sum = 0
    for springs, numbers in input:
        pass
    return sum


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename, rows_with_spaces=True)
        input = parse_input_str(inputs_str)

        expected_result1 = None if filename == "input_example" else None
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
