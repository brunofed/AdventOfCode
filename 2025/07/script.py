from collections import defaultdict, deque
from csv import reader
from itertools import product
from pathlib import Path


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


###### START OF ACTUAL CODE ######


def parse_input_str(inputs_str):
    source = (inputs_str[0].index("S"), 0)
    splitters_by_row = defaultdict(set)
    for j, row in enumerate(inputs_str):
        for i, char in enumerate(row):
            if char == "^":
                splitters_by_row[j].add(i)
    return source, splitters_by_row


def problem1(source, splitters_by_row):
    beams_splits = 0
    beams = {source[0]}
    for row, splitters in splitters_by_row.items():
        splitters_hit = splitters & beams
        beams_splits += len(splitters_hit)
        beams -= splitters_hit
        beams |= {beam + dx for dx, beam in product((-1, 1), splitters_hit)}
    return beams_splits


def problem2(source, splitters_by_row):
    beams_splits = 0
    beams = {source[0]}
    for row, splitters in splitters_by_row.items():
        splitters_hit = splitters & beams
        beams_splits += 2 * len(splitters_hit)
        beams -= splitters_hit
        beams |= {beam + dx for dx, beam in product((-1, 1), splitters_hit)}
    return beams_splits


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 21,
        (problem1, "input"): 1504,
        (problem2, "input_example"): 40,
        (problem2, "input"): None,
    }
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        for problem in (problem1, problem2):
            actual_result = problem(*inputs)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {actual_result=}, {expected_result=}"
    pass
