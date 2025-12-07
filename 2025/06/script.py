from csv import reader
from functools import reduce
from pathlib import Path

import numpy as np


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


###### START OF ACTUAL CODE ######


def apply(args, func=int):
    return list(map(func, args))


def parse_input_str_1(inputs_str):
    data = [row.split() for row in inputs_str]
    data_cleaned = [apply(row) for row in data[:-1]]
    return zip(np.array(data_cleaned).T, data[-1])


STR_TO_OP = {"+": np.sum, "*": np.prod}


def problem1(inputs):
    return sum(int(STR_TO_OP[operator](numbers)) for numbers, operator in inputs)


def parse_input_str_2(inputs_str):
    numbers_str, operators_str = inputs_str[:-1], inputs_str[-1]
    operators = operators_str.split()
    result = 0
    column_numbers = []
    operators_it = iter(operators)
    for column in zip(*numbers_str):
        if all(x == " " for x in column):
            column_numbers_np = np.array(column_numbers)
            operator = next(operators_it)
            addend = int(STR_TO_OP[operator](column_numbers_np))
            result += addend
            column_numbers = []
        else:
            num = int(reduce(lambda a, b: a + b, column))
            column_numbers.append(num)
    return result


def problem2(inputs):  # ops, I did everything in the parsing step
    return inputs


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 4277556,
        (problem1, "input"): 6171290547579,
        (problem2, "input_example"): 3263827,
        (problem2, "input"): 8811937976367,
    }
    inputs = {}
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs[problem1] = parse_input_str_1(inputs_str)
        inputs[problem2] = parse_input_str_2(inputs_str)

        for problem in (problem1, problem2):
            actual_result = problem(inputs[problem])
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {actual_result=}, {expected_result=}"
    pass
