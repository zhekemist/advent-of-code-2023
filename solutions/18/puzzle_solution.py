import re
from typing import TypeAlias

import adventofcode as aoc

DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}

Vector: TypeAlias = tuple[int, int]


def parse_dig_plan(puzzle_input: aoc.PuzzleInput) -> list[tuple[Vector, int]]:
    return [
        (DIRECTIONS[direction], int(step_count))
        for direction, step_count, _ in re.findall(r'(\w) (\d+) \(#(\w+)\)', puzzle_input.get())
    ]


def parse_colors_as_dig_plan(puzzle_input: aoc.PuzzleInput):
    return [
        (DIRECTIONS['RDLU'[int(color[5])]], int(color[:5], 16))
        for _, _, color in re.findall(r'(\w) (\d+) \(#(\w+)\)', puzzle_input.get())
    ]


def get_trench_corners(dig_plan: list[tuple[Vector, int]]) -> list[Vector]:
    corners = []
    current_position = (0, 0)
    last_direction = (0, 0)

    for direction, step_size in dig_plan:
        current_position = current_position[0] + step_size * direction[0], current_position[1] + step_size * direction[
            1]
        if last_direction != direction:
            corners.append(current_position)
        last_direction = direction

    return corners


def get_lagoon_area(trench_corners: list[Vector]) -> int:
    area = 0
    for i in range(len(trench_corners)):
        j = (i + 1) % len(trench_corners)
        area += (trench_corners[i][1] + trench_corners[j][1]) * (trench_corners[i][0] - trench_corners[j][0])
    return abs(area) // 2


def count_outer_points(dig_plan: list[tuple[Vector, int]]) -> int:
    return sum(step for _, step in dig_plan)


def get_lagoon_volume(dig_plan: list[tuple[Vector, int]]) -> int:
    lagoon_area = get_lagoon_area(get_trench_corners(dig_plan))
    outer_points = count_outer_points(dig_plan)
    return lagoon_area + (outer_points // 2) + 1


@aoc.solution(part=aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    dig_plan = parse_dig_plan(puzzle_input)
    return get_lagoon_volume(dig_plan)


@aoc.solution(part=aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    dig_plan = parse_colors_as_dig_plan(puzzle_input)
    return get_lagoon_volume(dig_plan)
