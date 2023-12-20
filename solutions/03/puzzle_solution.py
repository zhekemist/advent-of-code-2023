from dataclasses import dataclass
from string import digits
from typing import Self, Callable

import math

import adventofcode as aoc


@dataclass
class Position:
    row: int
    col: int

    def adjacent_to(self, other: Self) -> bool:
        return abs(self.row - other.row) <= 1 and abs(self.col - other.col) <= 1

    def adjacent_to_any_of(self, others: list[Self]) -> bool:
        return any(self.adjacent_to(other) for other in others)


@dataclass
class Number:
    value: int
    digit_positions: list[Position]


def parse_schematic(puzzle_input: aoc.PuzzleInput, symbol_filter: Callable[[str], bool]) \
        -> tuple[list[Position], list[Number]]:
    symbol_positions = []
    numbers = []

    for row, line in enumerate(puzzle_input.get().splitlines(keepends=True)):
        number_str = ''
        digit_positions = []
        for col, character in enumerate(line):
            if character in digits:
                number_str += character
                digit_positions.append(Position(row, col))
            else:
                if len(number_str) > 0:
                    numbers.append(Number(int(number_str), digit_positions))
                    number_str = ''
                    digit_positions = []

                if symbol_filter(character):
                    symbol_positions.append(Position(row, col))

    return symbol_positions, numbers


def contain_adjacent_points(positions_one: list[Position], position_two: list[Position]) -> bool:
    return any(position.adjacent_to_any_of(position_two) for position in positions_one)


def find_part_numbers(symbol_positions: list[Position], numbers: list[Number]) -> list[int]:
    return [number.value for number in numbers if contain_adjacent_points(symbol_positions, number.digit_positions)]


def get_gear_ratios(star_positions: list[Position], numbers: list[Number]) -> list[int]:
    return [
        math.prod(adjacent_numbers) for star_position in star_positions
        if 2 == len(adjacent_numbers := [number.value for number in numbers if
                                         star_position.adjacent_to_any_of(number.digit_positions)])
    ]


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput) -> int:
    symbol_positions, numbers = parse_schematic(puzzle_input, lambda char: char not in ['.', '\n'])
    numbers = find_part_numbers(symbol_positions, numbers)
    return sum(numbers)


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput) -> int:
    star_positions, numbers = parse_schematic(puzzle_input, lambda char: char == '*')
    gear_ratios = get_gear_ratios(star_positions, numbers)
    return sum(gear_ratios)
