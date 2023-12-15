from os.path import dirname, realpath, join
from csv import reader


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
    return [Lens(string) for string in inputs_str[0].split(",")]


class Lens:
    def __init__(self, string):
        self.step = string
        self.symbol = "-" if "-" in self.step else "="
        self.name, focal_length_str = self.step.split(self.symbol)
        self.focal_length = "" if not focal_length_str else int(focal_length_str)
        self.clean_step = None if self.symbol == "-" else self.name + " " + focal_length_str

    def __repr__(self):
        string = self.clean_step if self.clean_step is not None else self.step
        return f"Lens('{string}')"


def hash(string):
    current_value = 0
    for char in string:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value


def problem1(input):
    return sum(hash(lens.step) for lens in input)


def problem2(input):
    boxes = {i: [] for i in range(256)}
    total = 0
    for lens in input:
        key = hash(lens.name)
        old_value = boxes[key]
        if lens.symbol == "-":
            new_value = [old_lens for old_lens in old_value if old_lens.name != lens.name]
        else:
            found = False
            new_value = []
            for old_lens in old_value:
                if old_lens.name == lens.name:
                    found = True
                    new_value.append(lens)
                else:
                    new_value.append(old_lens)
            if found == False:
                new_value.append(lens)

        boxes[key] = new_value

    for id, lenses in boxes.items():
        for slot, lens in enumerate(lenses, start=1):
            total += (id + 1) * slot * lens.focal_length
    return total


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename, rows_with_spaces=True)
        input = parse_input_str(inputs_str)

        expected_result1 = 1320 if filename == "input_example" else 516070
        assert problem1(input) == expected_result1
        expected_result2 = 145 if filename == "input_example" else 244981
        assert problem2(input) == expected_result2
    pass
