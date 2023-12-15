from os.path import dirname, realpath, join
from csv import reader
from collections import deque


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
    return inputs_str[0].split(",")


def problem1(input):
    total = 0
    for step in input:
        current_value = 0
        for char in step:
            current_value = ((current_value + ord(char)) * 17) % 256
        total += current_value
    return total


def problem2(input):
    boxes = {i: [] for i in range(256)}
    for step in input:
        name, symbol, number_str = step[:2], step[2], step[3:]
        clean_step = name + " " + number_str
        if symbol == "-":
            assert number_str == ""
            for key, value in boxes.items():
                new_value = [lens for lens in value if not lens.startswith(name)]
                boxes[key] = new_value
        else:
            for key, value in boxes.items():
                found = False
                new_value = []
                for lens in value:
                    if lens.startswith(name):
                        found = True
                        new_value.append(clean_step)
                    else:
                        new_value.append(lens)
                if found == False:
                    new_value.insert(0, clean_step)
                boxes[key] = new_value
    total = 0
    for key, value in boxes.items():
        for slot, lens in enumerate(value, start=1):
            try:
                focal_length = int(lens[3])
            except:
                raise ("something went wrong")
            total += (key + 1) * slot * focal_length
    return total


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename, rows_with_spaces=True)
        input = parse_input_str(inputs_str)

        expected_result1 = 1320 if filename == "input_example" else 516070
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
