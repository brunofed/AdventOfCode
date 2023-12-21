from enum import Enum
from os.path import dirname, realpath, join
from csv import reader
from dataclasses import dataclass
from python_datastructures import queue


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


class Pulse(Enum):
    low = 0
    high = 1


@dataclass
class Module:
    name: str
    destination_modules: list
    pulse_out: Pulse = None
    pulse_in: Pulse = None
    source_module: list = None

    def pulse_in_to_out(self):
        self.pulse_out = self.pulse_in

    def send_pulse(self):
        for module in self.destination_modules:
            module.pulse_in = self.pulse_out
            module.source_module = self

    def process(self):
        self.pulse_in_to_out()
        self.send_pulse()


@dataclass
class FlipFlop(Module):
    on: bool = False

    def pulse_in_to_out(self):
        if self.pulse_in == Pulse.low:
            self.on = not self.on
            self.pulse_out = Pulse.high if self.on else Pulse.low


@dataclass
class Conjunction(Module):
    all_pulses_received: dict[Module, Pulse] = None

    def pulse_in_to_out(self):
        self.all_pulses_received[self.source_module] = self.pulse_in
        if all(self.all_pulses_received.values == Pulse.high):
            self.pulse_out = Pulse.low
        else:
            self.pulse_out = Pulse.high


def parse_input_str(inputs_str):
    modules = {}
    str_to_modules = {"broadcaster": Module, "%": FlipFlop, "&": Conjunction}
    for row in inputs_str:
        source, _targets = row.split(" -> ")
        targets = _targets.split(", ")
        if source == "broadcaster":
            module_name = source
            module_type = source
            pulse_in = Pulse.low
        else:
            module_type = source[0]
            module_name = source[1:]
            pulse_in = None

        modules[module_name] = str_to_modules[module_type](name=source, destination_modules=targets, pulse_in=pulse_in)

    return modules


def problem1(input):
    pass


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example_1", "input_example_2", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = None if filename == "input_example" else None
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
