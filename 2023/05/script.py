#import stuff
from os.path import dirname, realpath, join
from csv import reader
from operator import add
#actual math stuff
from itertools import batched
    
def create_mapping(src_to_dest_mappings):
    def f(n):
        for dest_range_start, src_range_start, range_length in src_to_dest_mappings:
            diff = n - src_range_start
            if 0 <= diff < range_length: # maybe it's <= ???
                return dest_range_start + diff
        return n
    return f    

def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f'{filename}.txt'), 'r') as file:
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

def str_to_ints(string):
    return list(map(int, string.split()))

def parse_input_str(inputs_str):
    mappings = []
    seeds = str_to_ints(inputs_str[0][0].split(': ')[1])
    old_dest_name = None
    for row in inputs_str[1:]:
        src_name, _, dest_name = row[0].split(' ')[0].split('-')
        if old_dest_name is not None:
            assert src_name == old_dest_name # just to check that all transformations can be composed with the following one
        ranges = [str_to_ints(mapping_str) for mapping_str in row[1:]]
        f = create_mapping(ranges)
        mappings.append(f)
        old_dest_name = dest_name
    return seeds, mappings
            
def problem1(input):
    seeds, mappings = input
    transformed_seeds = seeds
    for f in mappings:
        transformed_seeds = list(map(f, transformed_seeds))
    return min(transformed_seeds)

def problem2(input):
    seed_ranges, mappings = input
    assert len(seed_ranges) % 2 == 0 # apparently they come in pairs
    starts_and_ends = batched(seed_ranges, 2)
    seeds = []
    for start, length in starts_and_ends:
        actual_range = list(range(start, start+length))
        seeds += actual_range
    return problem1((seeds, mappings))

for filename in ['input_example',
                 'input']:
    inputs_str = read(filename, blank_rows=True)
    input = parse_input_str(inputs_str)

    expected_result1 = 35 if filename == "input_example" else 600279879
    assert problem1(input) == expected_result1
    expected_result2 = 46 if filename == "input_example" else None
    assert problem2(input) == expected_result2
pass