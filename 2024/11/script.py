from collections import Counter
from copy import copy
from csv import reader
from pathlib import Path
from time import time as current_time

import matplotlib.pyplot as plt


def read(
    filename,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


def apply(args, func=int):
    return list(map(func, args))


def parse_input_str(inputs_str):
    return Counter(apply(inputs_str[0].split()))


def problem(inputs, blinks, return_distinct=False):
    print(blinks)
    for _ in range(blinks):
        result = copy(inputs)
        for number, occurrences in inputs.items():
            if number == 0:
                result[1] += occurrences
            elif len(str(number)) % 2 == 0:
                midpoint = len(str(number)) // 2
                number_str = str(number)
                left, right = int(number_str[:midpoint]), int(number_str[midpoint:])
                result[left] += occurrences
                result[right] += occurrences
            else:
                result[number * 2024] += occurrences
            result[number] -= occurrences
        inputs = copy(result)
    if not return_distinct:
        return sum(result.values())
    return len(result)


def plot(input, max_blinks):
    x_s = list(range(1, max_blinks))
    y_s = [problem(input, blinks, return_distinct=True) for blinks in x_s]

    plt.figure(figsize=(10, 6))
    plt.plot(x_s, y_s, marker="o", linestyle="-", color="b", label="f(x)")
    plt.title("Function Plot")
    plt.xlabel("Input (x)")
    plt.ylabel("Output (f(x))")
    plt.grid(True)
    plt.legend()
    plt.show()
    pass


if __name__ == "__main__":
    for filename in ["input_example1", "input_example2", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        expected_result1 = {"input_example1": 7, "input_example2": 55312, "input": 233875}
        blinks = {"input_example1": 1, "input_example2": 25, "input": 25}
        assert problem(inputs, blinks[filename]) == expected_result1[filename]
        if filename == "input":
            assert problem(inputs, blinks=75) == 277444936413293
        # plot(inputs, max_blinks=120)
    pass
