from csv import reader
from functools import reduce
from pathlib import Path

import portion as Interval


def advanced_read(
    filename,
    blank_rows=False,
    rows_with_spaces=False,
):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
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


###### START OF ACTUAL CODE ######


def parse_input_str(inputs_str):
    intervals_str, numbers_str = inputs_str
    intervals = []
    for interval in intervals_str:
        a, b = interval.split("-")
        intervals.append(Interval.closed(int(a), int(b)))
    numbers = list(map(int, numbers_str))
    intervals_union = reduce(lambda x, y: x | y, intervals)
    return intervals_union, numbers


def problem1(intervals_union, numbers):
    return sum(1 for n in numbers if n in intervals_union)


def problem2(intervals_union, _):
    return sum(interval.upper - interval.lower + 1 for interval in intervals_union)


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 3,
        (problem1, "input"): 811,
        (problem2, "input_example"): 14,
        (problem2, "input"): 338189277144473,
    }
    for filename in ["input_example", "input"]:
        inputs_str = advanced_read(filename, blank_rows=True)
        inputs = parse_input_str(inputs_str)

        for problem in (problem1, problem2):
            actual_result = problem(*inputs)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {actual_result=}, {expected_result=}"
