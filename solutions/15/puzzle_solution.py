import re
from collections import defaultdict

import adventofcode as aoc


def parse_init_sequence(puzzle_input: aoc.PuzzleInput) -> list[str]:
    return puzzle_input.get().replace('\n', '').split(',')


def hash_algorithm(string: str) -> int:
    result = 0
    for character in string:
        result = (result + ord(character)) * 17 % 256
    return result


def fill_boxes(init_sequence: list[str]) -> dict[int, dict[str, int]]:
    boxes = defaultdict(dict)
    for instruction in init_sequence:
        match re.search(r'(\w+)([-=])(\d+)?', instruction).groups():
            case label, '=', focal_length:
                box = hash_algorithm(label)
                boxes[box][label] = int(focal_length)
            case label, '-', _:
                box = hash_algorithm(label)
                boxes[box].pop(label, None)
    return boxes


def get_focusing_power(boxes: dict[int, dict[str, int]]) -> int:
    return sum(
        (box + 1) * (slot + 1) * focal_length
        for box, lenses in boxes.items()
        for slot, focal_length in enumerate(lenses.values())
    )


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    init_sequence = parse_init_sequence(puzzle_input)
    return sum(map(hash_algorithm, init_sequence))


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    init_sequence = parse_init_sequence(puzzle_input)
    boxes = fill_boxes(init_sequence)
    return get_focusing_power(boxes)
