from csv import reader
from itertools import combinations, cycle, pairwise
from pathlib import Path

import numpy as np
from tqdm import tqdm


def read(filename):
    file_path = Path(__file__).parent / f"{filename}.txt"
    with open(file_path, "r") as file:
        return [row for row in reader(file)]


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
    return [np.array((int(a), int(b))) for a, b in inputs_str]


def area(p, q):
    dx = abs(p[0] - q[0]) + 1
    dy = abs(p[1] - q[1]) + 1
    if not dx:
        return dy
    if not dy:
        return dx
    return dx * dy


def problem1(inputs):
    return max(area(*pair) for pair in combinations(inputs, 2))


def are_points_in_polygon(points, polygon):
    """
    Vectorized check if multiple points are inside a polygon.

    Parameters:
    - points: (N,2) array of points
    - polygon: (M,2) array of polygon vertices in order

    Returns:
    - mask: boolean array of length N, True if inside, False if outside
    """
    points = np.atleast_2d(points).astype(float)
    polygon = np.array(polygon, dtype=float)

    # Polygon edges
    p1 = polygon
    p2 = np.roll(polygon, -1, axis=0)

    # Expand for broadcasting: points[:, None, :] and edges[None, :, :]
    x, y = points[:, 0, None], points[:, 1, None]
    x1, y1 = p1[None, :, 0], p1[None, :, 1]
    x2, y2 = p2[None, :, 0], p2[None, :, 1]

    # Conditions for upward and downward edge crossings
    cond_up = (y1 <= y) & (y2 > y)
    cond_down = (y1 > y) & (y2 <= y)

    # Compute cross product for each point-edge pair
    cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)

    # Winding number contribution per edge
    wn = np.sum(cond_up & (cross > 0), axis=1) - np.sum(cond_down & (cross < 0), axis=1)

    return wn != 0


def is_point_in_rect_strictly(point, rect):
    return bool(np.all((rect[0] <= point) & (point <= rect[1])))


def is_empty_rect(rect, points):
    return not any(is_point_in_rect_strictly(point, rect) for point in points)


def is_rect_in_polygon(rect, polygon):
    # check if the rectangle rect is within the polygon. The polygon is represented as the list of vertices of its boundary
    (x1, y1), (x2, y2) = rect
    corners = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
    return all(are_points_in_polygon(corners, polygon))


def problem2(points):
    areas = []
    for pair in tqdm(combinations(points, 2)):
        if is_empty_rect(pair, points) and is_rect_in_polygon(pair, points):
            areas.append(area(*pair))
    return max(areas)


###### END OF ACTUAL CODE ######

if __name__ == "__main__":
    expected_results = {
        (problem1, "input_example"): 50,
        (problem1, "input"): 4781546175,
        (problem2, "input_example"): 24,
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
