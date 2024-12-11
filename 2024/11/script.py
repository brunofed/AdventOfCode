from collections import Counter
from copy import copy
from csv import reader
from pathlib import Path


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


def problem(inputs, blinks):
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
    return sum(result.values())


if __name__ == "__main__":
    for filename in ["input_example2", "input_example1", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = {"input_example1": 55312, "input_example2": 7, "input": 233875}
        blinks = {"input_example1": 25, "input_example2": 1, "input": 25}
        assert problem(input, blinks[filename]) == expected_result1[filename]
        if filename == "input":
            assert problem(input, blinks=75) == 277444936413293
    pass
