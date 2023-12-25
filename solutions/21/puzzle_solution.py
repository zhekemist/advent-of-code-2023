import itertools
from collections import deque
from typing import TypeAlias

import adventofcode as aoc

Plot: TypeAlias = tuple[int, int]


def parse_garden(puzzle_input: aoc.PuzzleInput) -> tuple[list[str], Plot]:
    garden = puzzle_input.get_lines()
    return garden, next((row, line.index('S')) for row, line in enumerate(garden) if 'S' in line)


def count_reachable_plots(start: Plot, garden: list[str], steps: int) -> int:
    reachable_plots = 0
    seen_plots = set()

    next_plots = deque([(0, start)])
    while len(next_plots) > 0:
        distance, plot = next_plots.pop()

        if (distance, plot) in seen_plots:
            continue
        seen_plots.add((distance, plot))

        if distance == steps:
            reachable_plots += 1
            continue

        for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_row, next_col = next_plot = plot[0] + d_row, plot[1] + d_col
            if 0 <= next_row < len(garden) and 0 <= next_col < len(garden[0]) and garden[next_row][next_col] != '#':
                next_plots.append((distance + 1, next_plot))

    return reachable_plots


@aoc.solution(part=aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    garden, start = parse_garden(puzzle_input)
    return count_reachable_plots(start, garden, 64)


@aoc.solution(part=aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    garden, start = parse_garden(puzzle_input)
    start_row, start_col = start
    size = len(garden)
    steps = 26501365

    diamond_radius = ((2 * steps + 1) - 3 * size) // (2 * size)

    center_even = count_reachable_plots(start, garden, size - 1)
    center_even *= (diamond_radius + 1) ** 2

    center_uneven = count_reachable_plots(start, garden, size)
    center_uneven *= diamond_radius ** 2

    corners = 0
    for corner in [(start_row, 0), (start_row, size - 1), (0, start_col), (size - 1, start_col)]:
        corners += count_reachable_plots(corner, garden, size - 1)

    small_borders = 0
    for small_border in itertools.product([0, size - 1], repeat=2):
        small_borders += count_reachable_plots(small_border, garden, size // 2 - 1)
    small_borders *= (diamond_radius + 1)

    large_borders = 0
    for large_border in itertools.product([0, size - 1], repeat=2):
        large_borders += count_reachable_plots(large_border, garden, size + size // 2 - 1)
    large_borders *= diamond_radius

    return center_even + center_uneven + corners + small_borders + large_borders
