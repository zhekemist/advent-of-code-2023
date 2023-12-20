import json
import re
from dataclasses import dataclass, field
from typing import TypeAlias, Self

import math

import adventofcode as aoc

Predicate: TypeAlias = tuple[str, str, int] | None
Workflow: TypeAlias = list[tuple[Predicate, str]]
Part: TypeAlias = dict[str, int]


@dataclass
class PartInterval:
    attr_intervals: dict[str, tuple[int, int]] = field(default_factory=dict)

    def is_empty(self) -> bool:
        return any(interval[1] - interval[0] < 0 for interval in self.attr_intervals.values())

    def possible_combinations(self) -> int:
        return math.prod(interval[1] - interval[0] + 1 for interval in self.attr_intervals.values())

    def split_by_predicate(self, predicate: Predicate) -> tuple[Self, Self]:
        if predicate is None:
            return self, PartInterval()

        attr, operator, bound = predicate
        matching_interval, remaining_interval = self.attr_intervals.copy(), self.attr_intervals.copy()
        lower_bound, upper_bound = self.attr_intervals[attr]

        if operator == '<':
            matching_interval[attr] = (lower_bound, bound - 1)
            remaining_interval[attr] = (bound, upper_bound)
        elif operator == '>':
            matching_interval[attr] = (bound + 1, upper_bound)
            remaining_interval[attr] = (lower_bound, bound)

        return PartInterval(matching_interval), PartInterval(remaining_interval)


def parse_workflow(line: str) -> tuple[str, Workflow]:
    name, rule_specs = line.split('{')
    rules = [
        ((attr, op, int(bound)) if attr else None, target)
        for attr, op, bound, target in re.findall('(?:(\w)([<>])(\d+):)?(\w+)', rule_specs)
    ]
    return name, rules


def parse_workflows(puzzle_input: aoc.PuzzleInput) -> dict[str, Workflow]:
    return dict(
        parse_workflow(line)
        for line in puzzle_input.get().split('\n\n')[0].splitlines()
    )


def parse_parts(puzzle_input: aoc.PuzzleInput) -> list[Part]:
    return [
        json.loads(re.sub(r'(\w)=', r'"\1":', line))
        for line in puzzle_input.get().split('\n\n')[1].splitlines()
    ]


def is_part_accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
    current_workflow = 'in'
    while current_workflow not in 'AR':
        for predicate, target_workflow in workflows[current_workflow]:
            match predicate:
                case attr, '<', bound if part[attr] >= bound:
                    continue
                case attr, '>', bound if part[attr] <= bound:
                    continue
                case _:
                    current_workflow = target_workflow
                    break

    return current_workflow == 'A'


def get_accepted_intervals(part_interval: PartInterval, workflow: str,
                           workflows: dict[str, Workflow]) -> list[PartInterval]:
    if workflow == 'A':
        return [part_interval]
    elif workflow == 'R':
        return []

    result = []
    for predicate, target_workflow in workflows[workflow]:
        matching_interval, part_interval = part_interval.split_by_predicate(predicate)

        if not matching_interval.is_empty():
            result += get_accepted_intervals(matching_interval, target_workflow, workflows)

        if part_interval.is_empty():
            break

    return result


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    workflows = parse_workflows(puzzle_input)
    parts = parse_parts(puzzle_input)

    return sum(sum(part.values()) for part in parts
               if is_part_accepted(part, workflows))


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    workflows = parse_workflows(puzzle_input)

    base_interval = PartInterval({i: (1, 4000) for i in 'xmas'})
    accepted_intervals = get_accepted_intervals(base_interval, 'in', workflows)

    return sum(map(PartInterval.possible_combinations, accepted_intervals))
