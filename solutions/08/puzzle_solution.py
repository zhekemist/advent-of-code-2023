import itertools
import re
from typing import Callable, Iterable

import math

import adventofcode as aoc


def parse_adjacency_map(puzzle_input: aoc.PuzzleInput) -> dict[str, tuple[str, str]]:
    return {
        node: (left, right) for node, left, right
        in re.findall(r'(\w+) = \((\w+), (\w+)\)', puzzle_input.get())
    }


def get_shortest_path(start_node: str, directions: Iterable[int], adjacency_map: dict[str, tuple[str, str]],
                      end_condition: Callable[[str], bool]) -> int:
    current_node = start_node
    directions = itertools.cycle(directions)
    steps = 0

    while not end_condition(current_node):
        steps += 1
        current_node = adjacency_map[current_node][next(directions)]

    return steps


def ends_with(char: str) -> Callable[[str], bool]:
    return lambda string: string.endswith(char)


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    directions = map('LR'.index, puzzle_input.get_lines()[0])
    adjacency_map = parse_adjacency_map(puzzle_input)

    return get_shortest_path('AAA', directions, adjacency_map, ends_with('ZZZ'))


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    directions = list(map('LR'.index, puzzle_input.get_lines()[0]))
    adjacency_map = parse_adjacency_map(puzzle_input)

    start_nodes = filter(ends_with('A'), adjacency_map.keys())
    shortest_path_lengths = (get_shortest_path(start_node, directions, adjacency_map, ends_with('Z'))
                             for start_node in start_nodes)

    return math.lcm(*shortest_path_lengths)
