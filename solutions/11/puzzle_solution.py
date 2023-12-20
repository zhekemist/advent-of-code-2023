import itertools
from collections import Counter
from typing import TypeAlias

import adventofcode as aoc

Position: TypeAlias = tuple[int, int]


def parse_galaxies(puzzle_input: aoc.PuzzleInput) -> list[Position]:
    return [
        (row, col)
        for row, line in enumerate(puzzle_input.get_lines())
        for col, sector in enumerate(line)
        if sector == '#'
    ]


def get_total_distance(galaxies: list[Position]) -> int:
    return sum(abs(galaxy_one[0] - galaxy_two[0]) + abs(galaxy_one[1] - galaxy_two[1])
               for galaxy_one, galaxy_two in itertools.combinations(galaxies, 2))


def get_expansion_distance(galaxies: list[Position], universe_dims: tuple[int, int],
                           axis: int, expansion_extent: int = 1) -> int:
    galaxies_per_sector = Counter(galaxy[axis] for galaxy in galaxies)
    before = 0
    after = len(galaxies)

    expansion_distance = 0
    for sector in range(universe_dims[axis]):
        if sector in galaxies_per_sector:
            before += galaxies_per_sector[sector]
            after -= galaxies_per_sector[sector]
        else:
            expansion_distance += before * after * expansion_extent

    return expansion_distance


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    galaxies = parse_galaxies(puzzle_input)
    universe_dims = (len(puzzle_input.get_lines()), len(puzzle_input.get_lines()[0]))

    distance = get_total_distance(galaxies)
    distance += get_expansion_distance(galaxies, universe_dims, 0)
    distance += get_expansion_distance(galaxies, universe_dims, 1)

    return distance


@aoc.solution(aoc.Part.TWO)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    galaxies = parse_galaxies(puzzle_input)
    universe_dims = (len(puzzle_input.get_lines()), len(puzzle_input.get_lines()[0]))

    distance = get_total_distance(galaxies)
    distance += get_expansion_distance(galaxies, universe_dims, 0, 1000000 - 1)
    distance += get_expansion_distance(galaxies, universe_dims, 1, 1000000 - 1)

    return distance
