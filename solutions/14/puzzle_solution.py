import numpy as np

import adventofcode as aoc


def parse_platform(puzzle_input: aoc.PuzzleInput) -> np.ndarray:
    return np.array([
        list(map('.O#'.index, line))
        for line in puzzle_input.get_lines()
    ])


def tilt_platform(platform: np.ndarray) -> None:
    for col, column in enumerate(platform.T):
        free_row = 0
        for row, field in enumerate(column):
            match field:
                case 1:
                    platform[row, col] = 0
                    platform[free_row, col] = 1
                    free_row += 1
                case 2:
                    free_row = row + 1


def get_load(platform: np.ndarray | tuple[int, ...]) -> int:
    if isinstance(platform, tuple):
        platform = np.array(platform)
    return sum(
        (factor + 1) * np.sum(row == 1)
        for factor, row in enumerate(platform[::-1])
    )


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    platform = parse_platform(puzzle_input)
    tilt_platform(platform)
    return get_load(platform)


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    platform = parse_platform(puzzle_input)
    not_rotated_platform = platform

    tilts = 0
    seen_configurations = {}

    while True:
        for _ in range(4):
            tilt_platform(platform)
            platform = np.rot90(platform, -1)

        platform_tuple = tuple(map(tuple, not_rotated_platform))
        if platform_tuple not in seen_configurations:
            seen_configurations[platform_tuple] = None
        else:
            break

        tilts += 1

    seen_configurations = list(seen_configurations)

    cycle_start = seen_configurations.index(platform_tuple)
    position_in_cycle = (1_000_000_000 - cycle_start - 1) % (tilts - cycle_start)
    absolute_position = cycle_start + position_in_cycle

    return get_load(seen_configurations[absolute_position])
