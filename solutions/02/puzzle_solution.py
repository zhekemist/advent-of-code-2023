from input import *

MINIMAL_CONFIGURATION = {
    Color.RED: 12,
    Color.GREEN: 13,
    Color.BLUE: 14,
}


def is_possible(drawings: list[dict[Color, int]], configuration: dict[Color, int]) -> bool:
    for drawing in drawings:
        for color, count in drawing.items():
            if count > configuration[color]:
                return False
    return True


def find_maximal_counts(drawings: list[dict[Color, int]]) -> list[int]:
    maxima = {}
    for drawing in drawings:
        for color, count in drawing.items():
            if not color in maxima or maxima[color] < count:
                maxima[color] = count
    return list(maxima.values())


def get_power_of_set(drawings: list[dict[Color, int]]):
    power = 1
    maximal_counts = find_maximal_counts(drawings)
    for value in maximal_counts:
        power *= value
    return power


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput) -> int:
    games = load_games(puzzle_input)

    sum_of_possible_ids = 0
    for game_id, drawings in games.items():
        if is_possible(drawings, MINIMAL_CONFIGURATION):
            sum_of_possible_ids += game_id

    return sum_of_possible_ids


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput) -> int:
    games = load_games(puzzle_input)

    sum_of_powers = 0
    for drawings in games.values():
        power = get_power_of_set(drawings)
        sum_of_powers += power

    return sum_of_powers
