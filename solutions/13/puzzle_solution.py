import numpy as np

import adventofcode as aoc


def parse_landscapes(puzzle_input: aoc.PuzzleInput) -> list[np.ndarray]:
    return [
        np.array([[int(char == '#') for char in line]
                  for line in landscape_chunk.splitlines()])
        for landscape_chunk in puzzle_input.get().split('\n\n')
    ]


def count_differences(first_array: np.ndarray, second_array: np.ndarray) -> int:
    return int(np.sum(np.abs(first_array - second_array)))


def get_reflection(landscape: np.ndarray, tolerance: int = 0) -> int:
    rows = landscape.shape[0]
    for row in range(1, rows):
        reflection_size = min(row, rows - row)
        before = landscape[row - reflection_size:row]
        after = landscape[row:row + reflection_size]

        differences = count_differences(before, np.flip(after, axis=0))
        if differences == tolerance:
            return row

    return 0


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    landscapes = parse_landscapes(puzzle_input)
    return sum(
        get_reflection(landscape) * 100 + get_reflection(landscape.T)
        for landscape in landscapes
    )


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    landscapes = parse_landscapes(puzzle_input)
    return sum(
        get_reflection(landscape, 1) * 100 + get_reflection(landscape.T, 1)
        for landscape in landscapes
    )
