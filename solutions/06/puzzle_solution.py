import re

from math import sqrt, prod, ceil, floor

import adventofcode as aoc


def parse_races(lines: list[str]) -> list[tuple[int, int]]:
    numbers = [map(int, re.findall(r'(\d+)', line)) for line in lines]
    return list(zip(*numbers))


def get_minimal_button_time(race: tuple[int, int]) -> int:
    total_time, minimal_distance = race
    lower_bound = (-total_time + sqrt(total_time ** 2 - 4 * minimal_distance)) / (-2)
    upper_bound = (-total_time - sqrt(total_time ** 2 - 4 * minimal_distance)) / (-2)

    return ceil(upper_bound) - floor(lower_bound) - 1


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    races = parse_races(puzzle_input.get_lines())
    return prod(map(get_minimal_button_time, races))


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    race = parse_races(puzzle_input.get().replace(' ', '').splitlines())[0]
    return get_minimal_button_time(race)
