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
    cards = []
    for row in inputs_str:
        split_row = row.split()
        separator = split_row.index("|")
        my_numbers = split_row[2:separator]
        my_numbers_set = set(my_numbers)
        winning_numbers = split_row[separator + 1 :]
        winning_numbers_set = set(winning_numbers)
        assert len(my_numbers) == len(my_numbers_set) and len(winning_numbers) == len(
            winning_numbers_set
        )  # set didn't delete anything
        cards.append([my_numbers_set, winning_numbers_set])
    return cards


def points(n):
    if n == 0:
        return 0
    return 2 ** (n - 1)


def get_intersection_sizes(cards):
    return [len(my_num & winning_num) for my_num, winning_num in cards]


def problem1(overlaps):
    return sum(points(num) for num in overlaps)


def problem2(overlaps):
    card_multiplicity = [1]*len(overlaps)
    for i, num in enumerate(overlaps):
        for j in range(i + 1, i + num + 1):
            card_multiplicity[j] += card_multiplicity[i]
    return sum(card_multiplicity)


for filename in ["input_example", "input"]:
    inputs_str = read(filename)
    input = parse_input_str(inputs_str)
    overlaps = get_intersection_sizes(input)
    expected_result1 = 13 if filename == "input_example" else 21959
    assert problem1(overlaps) == expected_result1
    expected_result2 = 30 if filename == "input_example" else 5132675
    assert problem2(overlaps) == expected_result2
pass
