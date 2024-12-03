import re
from os.path import dirname, join, realpath


def read(filename):
    dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
        return file.read()


def parse_input_str(inputs_str, problem1):
    pattern1 = r"mul\(\d{1,3},\d{1,3}\)"
    pattern = pattern1 if problem1 else rf"(do\(\)|don't\(\)|{pattern1})"
    return re.findall(pattern, inputs_str)


def mul(a, b):
    return a * b


def problem1(input):
    return sum(eval(command) for command in input)


def problem2(input):
    sum = 0
    enabled = True
    for command in input:
        if command.startswith("do"):
            enabled = command == "do()"
            continue
        sum += enabled * eval(command)
    return sum


if __name__ == "__main__":
    for filename in ["input_example1", "input_example2", "input"]:
        inputs_str = read(filename)

        expected_result1 = 161 if filename == "input_example1" else 181345830
        if filename != "input_example2":
            input = parse_input_str(inputs_str, problem1=True)
            assert problem1(input) == expected_result1
        expected_result2 = 48 if filename == "input_example2" else 98729041
        if filename != "input_example1":
            input = parse_input_str(inputs_str, problem1=False)
            assert problem2(input) == expected_result2
    pass
