from collections import OrderedDict
from dataclasses import astuple
from os.path import dirname, realpath, join
from csv import reader
import re

from attr import dataclass


def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
        if blank_rows:
            grouped_rows = [[]]
            idx = 0
            for row in reader(file, delimiter="\n"):
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


def apply(func, args):
    return list(map(func, args))


def find_all_numbers(string):
    num_as_string = re.findall(r"\d+", string)
    return apply(int, num_as_string)


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    accepted: bool = None

    def rating(self):
        return self.x + self.m + self.a + self.s


@dataclass
class Rule:
    condition: bool
    result: str

    def apply_condition(self, part: Part):
        x, m, a, s = part.x, part.m, part.a, part.s  # astuple(part) would be easier but somehow doesn't work
        if self.condition is True or eval(self.condition):
            return self.result
        return None


@dataclass
class Workflow:
    name: str
    rules: list[Rule]

    def apply_all_rules(self, part):
        for rule in self.rules:
            result = rule.apply_condition(part)
            if result == "A":
                part.accepted = True
            elif result == "R":
                part.accepted = False
            if result is not None:
                return part, result


def parse_input_str(inputs_str):
    workflows_str, _parts = inputs_str

    workflows = {}
    for name_and_conditions in workflows_str:
        name, conditions_str = name_and_conditions.split("{")
        conditions_str = conditions_str.rstrip("}")  # Remove the closing '}'

        conditions = conditions_str.split(",")

        workflow_list = []
        for condition_and_strategy in conditions:
            try:
                cond, target_strategy = condition_and_strategy.split(":")
            except ValueError:
                cond = True
                target_strategy = condition_and_strategy
            workflow_list.append(Rule(cond, target_strategy))

        workflows[name] = Workflow(name, workflow_list)

    parts = []
    for _part in _parts:
        x, m, a, s = find_all_numbers(_part)
        parts.append(Part(x, m, a, s))

    return workflows, parts


def problem1(input):
    workflows, parts = input
    for part in parts:
        current_workflow = "in"
        while part.accepted is None:
            workflow = workflows[current_workflow]
            part, current_workflow = workflow.apply_all_rules(part)
    return sum(part.rating() for part in parts if part.accepted)


def problem2(input):
    workflows, _ = input
    # 1) rewrite the final condition of all workflows so it's still of the form "cond: workflow"
    for workflow in workflows.values():
        final_rule = workflow.rules[-1]
        standard_rules = workflow.rules[:-1]
        conditions = [rule.condition for rule in standard_rules]
        new_final_rule = Rule(f"not any({','.join(conditions)})", final_rule.result)
        workflow.rules[-1] = new_final_rule
        pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename, blank_rows=True)
        input = parse_input_str(inputs_str)

        expected_result1 = 19114 if filename == "input_example" else 397643
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
