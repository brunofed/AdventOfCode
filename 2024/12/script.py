from csv import reader
from pathlib import Path

import numpy as np
from scipy.ndimage import label


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row[0] for row in reader(file)]


def parse_input_str(inputs_str):
    return np.array([list(row) for row in inputs_str])


def get_connected_components(boolean_array, connectivity_type=4):
    match connectivity_type:
        # if two areas are considered adjacent if they share a common edge (case 4)
        # or even a common corner (case 8)
        case 4:
            structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)
        case 8:
            structure = np.ones((3, 3), dtype=bool)
        case _:
            raise ValueError("The connectivity type must be 4 or 8")
    labeled_array, num_features = label(boolean_array, structure=structure)
    components = []  # if wanted, we could label each component with its own number
    for label_val in range(1, num_features + 1):  # Exclude 0 (background)
        components.append((labeled_array == label_val))
    return components


def get_perimeter(a):
    # count the edges between 1s and 0s within the 2D boolean array
    n_interior = abs(np.diff(a, axis=0)).sum() + abs(np.diff(a, axis=1)).sum()
    n_boundary = a[0, :].sum() + a[:, 0].sum() + a[-1, :].sum() + a[:, -1].sum()
    return n_interior + n_boundary


def get_sides(component):
    # it's necessary to convert to int because corners in the outer diff will count for 2+ instead of 1
    padded_mask = np.pad(component.astype(np.int32), 1)

    def count_parallel_sides(i):
        return np.abs(np.diff(np.diff(padded_mask, axis=i), axis=1 - i)).sum()

    return (count_parallel_sides(0) + count_parallel_sides(1)) // 2


def problem(garden, is_problem1):
    result = 0
    for value in np.unique(garden):
        boolean_array = garden == value
        for component in get_connected_components(boolean_array):
            multiplier = get_perimeter(component) if is_problem1 else get_sides(component)
            area = np.count_nonzero(component)
            result += multiplier * area
    return result


if __name__ == "__main__":
    expected_result1 = {
        "input_example1": 140,
        "input_example2": 772,
        "input_example3": 1930,
        "input": 1450816,
    }
    expected_result2 = {
        "input_example1": 80,
        "input_example4": 236,
        "input_example5": 368,
        "input": 865662,
    }
    for filename in [f"input_example{i}" for i in range(1, 6)] + ["input"]:
        inputs_str = read(filename)
        inputs = parse_input_str(inputs_str)

        if filename in expected_result1.keys():
            assert problem(inputs, is_problem1=True) == expected_result1[filename]
        if filename in expected_result2.keys():
            assert problem(inputs, is_problem1=False) == expected_result2[filename]
    pass
