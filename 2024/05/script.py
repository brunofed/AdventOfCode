from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        lines = file.readlines()

        result = []
        current_list = []
        found_break = False
        for line in lines:
            stripped_line = line.strip() if not found_break else line.strip().split(",")
            if stripped_line:  # Non-empty line
                current_list.append(stripped_line)
            else:  # Empty line
                found_break = True
                if current_list:  # Save the current list if it has content
                    result.append(current_list)
                    current_list = []

        # Add the last list if there's any content left
        if current_list:
            result.append(current_list)

        return result


def apply(func, args):
    return list(map(func, args))


def parse_input_str(inputs_str):
    page_pairs_str, updates_str = inputs_str
    page_pairs = defaultdict(list)
    for pair in page_pairs_str:
        a, b = apply(int, pair.split("|"))
        page_pairs[a].append(b)
    updates = [apply(int, update) for update in updates_str]
    return page_pairs, updates


def sum_middle_elements(updates):
    return sum(update[len(update) // 2].x for update in updates)


def problem1(updates):
    correct_updates = []
    incorrect_updates = []
    for update in updates:
        for current, next in pairwise(update):
            if not (current < next):
                incorrect_updates.append(update)
                break
        else:
            correct_updates.append(update)
    return sum_middle_elements(correct_updates), incorrect_updates


def problem2(incorrect_updates):
    for update in incorrect_updates:
        update.sort()
    return sum_middle_elements(incorrect_updates)


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        page_pairs, updates = parse_input_str(inputs_str)

        @dataclass
        class UpdateElement:
            x: int

            def __lt__(self, other):
                return other.x in page_pairs[self.x]

        updates_class = [[UpdateElement(x) for x in update] for update in updates]
        expected_result1 = 143 if filename == "input_example" else 4872
        result, incorrect_updates = problem1(updates_class)
        assert result == expected_result1
        expected_result2 = 123 if filename == "input_example" else 5564
        assert problem2(incorrect_updates) == expected_result2
    pass
