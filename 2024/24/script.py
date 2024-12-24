from csv import reader
from dataclasses import dataclass
from operator import and_, or_, xor
from pathlib import Path


def read(
    filename,
    blank_rows=False,
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
        return [row[0] for row in reader(file)]


def apply(func, args):
    return list(map(func, args))


@dataclass
class Wire:
    name: str
    value: bool | None = None


OPERATOR_DICT = {"AND": and_, "OR": or_, "XOR": xor}


def parse_input_str(inputs_str):
    initial_values, gates_str = inputs_str

    initialised_wires = []
    for initial_value in initial_values:
        string, value = initial_value.split(": ")
        wire = Wire(string, bool(int(value)))
        initialised_wires.append(wire)

    gates = []
    for gate_str in gates_str:
        wire1, op, wire2, _, wire_result = gate_str.split()
        gates.append((wire1, OPERATOR_DICT[op], wire2, wire_result))
    return initialised_wires, gates


def convert_z_values(wires):
    z_wires = [wire for wire in wires if wire.name.startswith("z")]
    z_wires.sort(key=lambda wire: wire.name)
    bool_list = [wire.value for wire in z_wires[::-1]]
    return int("".join(str(int(b)) for b in bool_list), 2)


def find_or_create(name, wires, names):
    try:
        index = names.index(name)
    except ValueError:
        wire = Wire(name, None)
        wires.append(wire)
        names.append(name)
        return wire, wires, names
    else:
        wire = wires[index]
        return wire, wires, names


def problem1(wires, gates):
    names = [wire.name for wire in wires]
    while True:
        for name1, op, name2, name_result in gates:
            wire1, wires, names = find_or_create(name1, wires, names)
            wire2, wires, names = find_or_create(name2, wires, names)
            wire_result, wires, names = find_or_create(name_result, wires, names)
            value1, value2 = wire1.value, wire2.value
            if value1 is None or value2 is None:
                continue
            wire_result.value = op(value1, value2)
        if all(wire.value is not None for wire in wires):
            break
    return convert_z_values(wires)


def problem2(input):
    pass


if __name__ == "__main__":
    expected_result1 = {"input_example1": 4, "input_example2": 2024, "input": 59619940979346}
    for filename in ["input_example1", "input_example2", "input"]:
        inputs_str = read(filename, blank_rows=True)
        input = parse_input_str(inputs_str)

        assert problem1(*input) == expected_result1[filename]
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
