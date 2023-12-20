from functools import cache
from typing import TypeAlias

import regex as re

import adventofcode as aoc

ConditionRecord: TypeAlias = tuple[str, tuple[int, ...]]


def parse_condition_records(puzzle_input: aoc.PuzzleInput) -> list[ConditionRecord]:
    return [
        (hot_springs, tuple(map(int, group_sizes.split(','))))
        for hot_springs, group_sizes in re.findall(r'([.?#]+) ((?:\d+,?)+)', puzzle_input.get())
    ]


GROUP_PATTERN = '(?<!#[^#]*)[#?]{{{}}}(?!#)'


@cache
def get_arrangement_count(hot_springs: str, groups: tuple[int, ...]) -> int:
    if len(groups) == 0:
        return 1 if '#' not in hot_springs else 0

    next_group = groups[0]
    pattern = re.compile(GROUP_PATTERN.format(next_group))

    arrangement_count = 0
    for match in pattern.finditer(hot_springs, overlapped=True):
        remaining_hot_springs = hot_springs[match.end() + 1:]
        remaining_groups = groups[1:]
        arrangement_count += get_arrangement_count(remaining_hot_springs, remaining_groups)
    return arrangement_count


def unfold(condition_record: ConditionRecord) -> ConditionRecord:
    damages = '?'.join(condition_record[0] for _ in range(5))
    groups = condition_record[1] * 5
    return damages, groups


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    condition_records = parse_condition_records(puzzle_input)
    return sum(get_arrangement_count(*condition_record) for condition_record in condition_records)


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    condition_records = parse_condition_records(puzzle_input)
    return sum(get_arrangement_count(*unfold(condition_record)) for condition_record in condition_records)
