import adventofcode as aoc


def parse_histories(puzzle_input: aoc.PuzzleInput) -> list[list[int]]:
    return [[int(i) for i in line.split(' ')]
            for line in puzzle_input.get_lines()]


def extrapolate(sequence: list[int]) -> int:
    result = sequence[-1]
    if any(sequence):
        differences = [i - j for i, j in zip(sequence[1:], sequence)]
        result += extrapolate(differences)
    return result


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    histories = parse_histories(puzzle_input)
    return sum(map(extrapolate, histories))


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    histories = parse_histories(puzzle_input)
    histories = map(lambda x: list(reversed(x)), histories)
    return sum(map(extrapolate, histories))
