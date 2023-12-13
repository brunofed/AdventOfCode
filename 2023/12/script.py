# import stuff
from itertools import groupby, chain, combinations
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
    # sample input: "abccdddaaaaffff"
    # output: ['a', 'b', 'cc', 'ddd', 'aaaa', 'ffff']
    return ["".join(group) for _, group in groupby(input_string)]


def parse_input_str(inputs_str):
    strings_and_numbers = []
    for row in inputs_str:
        string, numbers_str = row.split()
        string_split = split_string(string)
        numbers = str_to_ints(numbers_str, delimiter=",")
        strings_and_numbers.append((string, string_split, numbers))
    return strings_and_numbers


# not used, but runs in O(1)
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


def replace_in_all_places(original, num_new_value, old_value, new_value, alternative_value):
    indexes = {i for i, char in enumerate(original) if char == old_value}
    all_combinations = []

    for subset in combinations(indexes, num_new_value):
        _modified_string = list(original)
        for i in subset:
            _modified_string[i] = new_value
        complement = indexes - set(subset)
        for j in complement:
            _modified_string[j] = alternative_value
        modified_string = "".join(_modified_string)
        all_combinations.append(modified_string)
    return all_combinations


def problem1(input):
    total = 0
    for string, _, numbers in input:
        working_alternatives = []
        needed_question_marks = sum(numbers) - string.count("#")
        possible_strings = replace_in_all_places(string, needed_question_marks, "?", "#", ".")
        for possible_string in possible_strings:
            lengths = [len(list(group)) for key, group in groupby(possible_string) if key == "#"]
            if lengths == numbers:
                working_alternatives.append(possible_string)
        total += len(working_alternatives)
    return total


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename, rows_with_spaces=True)
        input = parse_input_str(inputs_str)

        expected_result1 = 21 if filename == "input_example" else 7939
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
