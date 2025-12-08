from csv import reader
from pathlib import Path


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


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
    for row in inputs_str:
        pass


def problem1(inputs):
    pass


def problem2(inputs):
    pass


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): None,
        (problem1, "input"): None,
        (problem2, "input_example"): None,
        (problem2, "input"): None,
    }
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        for problem in (problem1, problem2):
            actual_result = problem(inputs)
            expected_result = expected_results[(problem, filename)]
            assert (
                actual_result == expected_result
            ), f"{problem.__name__},  {filename=}, {expected_result=}, {actual_result=}"
    pass
