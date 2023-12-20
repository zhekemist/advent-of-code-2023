from string import digits

import adventofcode as aoc

DIGIT_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_first_digit(string: str, reverse: bool = False) -> int:
    positions = range(len(string))
    if reverse:
        positions = reversed(positions)

    for pos in positions:
        if string[pos] in digits:
            return int(string[pos])

        for digit_idx, digit_word in enumerate(DIGIT_WORDS):
            if string.startswith(digit_word, pos):
                return digit_idx + 1


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput) -> int:
    calibration_sum = 0

    for line in puzzle_input.get_lines():
        numbers = [int(c) for c in line if c in digits]
        number = 10 * numbers[0] + numbers[-1]

        calibration_sum += number

    return calibration_sum


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput) -> int:
    calibration_sum = 0

    for line in puzzle_input.get_lines():
        first_digit = get_first_digit(line)
        last_digit = get_first_digit(line, reverse=True)
        number = 10 * first_digit + last_digit
        calibration_sum += number

    return calibration_sum
