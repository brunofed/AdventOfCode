from csv import reader
from itertools import product
from operator import add, mul
from pathlib import Path
from typing import NamedTuple


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


def apply(func, args):
    return list(map(func, args))


class Line(NamedTuple):
    test_num: int
    numbers: list[int]


def parse_input_str(inputs_str):
    lines = []
    for row in inputs_str:
        test_str, numbers_str = row.split(": ")
        line = Line(int(test_str), apply(int, numbers_str.split()))
        lines.append(line)
    return lines


def concatenate(a: int, b: int):
    return int(str(a) + str(b))


def can_be_solved(line, is_problem1):
    operators = [mul, add]
    if not is_problem1:
        operators = [concatenate] + operators

    # put mul before add so that bigger numbers are reached earlier
    sequences_of_operations = product(operators, repeat=len(line.numbers) - 1)
    for operations in sequences_of_operations:
        result = line.numbers[0]
        # apply all operations to result
        for i, number in enumerate(line.numbers[1:]):
            result = operations[i](result, number)
            # optimization: if the result is too big, there's no point in keep adding/multiplying numbers
            if result > line.test_num:
                break
        else:
            if result == line.test_num:
                return True
    return False


def problem(input, is_problem1):
    return sum(line.test_num for line in input if can_be_solved(line, is_problem1))


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 3749 if filename == "input_example" else 5030892084481
        assert problem(input, is_problem1=True) == expected_result1
        expected_result2 = 11387 if filename == "input_example" else 91377448644679
        # takes <2 minutes for "input"
        assert problem(input, is_problem1=False) == expected_result2
    pass
