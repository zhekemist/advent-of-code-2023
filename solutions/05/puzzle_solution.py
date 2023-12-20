import re

import adventofcode as aoc
from .maps import *


def apply_all_maps(image: T, maps: list[Map]) -> T:
    for map in maps:
        image = map.apply(image)
    return image


def parse_input(puzzle_input: aoc.PuzzleInput) -> tuple[list[int], list[Map]]:
    seeds_chunk, *mapping_chunks = puzzle_input.get().split('\n\n')
    seed_ids = list(map(int, re.findall(r'(\d+)', seeds_chunk)))
    maps = list(map(Map.from_text, mapping_chunks))

    return seed_ids, maps


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    seed_ids, maps = parse_input(puzzle_input)

    return min(apply_all_maps(seed_id, maps) for seed_id in seed_ids)


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    seed_ids, maps = parse_input(puzzle_input)

    seed_intervals = [Interval(start, start + length)
                      for start, length in zip(seed_ids[::2], seed_ids[1::2])]

    return min(apply_all_maps(seed_intervals, maps)).start
