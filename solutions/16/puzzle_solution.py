import adventofcode as aoc


def parse_contraption(puzzle_input: aoc.PuzzleInput) -> dict[tuple[int, int], str]:
    return {
        (row, col): field
        for row, line in enumerate(puzzle_input.get_lines())
        for col, field in enumerate(line)
    }


def parse_dimensions(puzzle_input: aoc.PuzzleInput) -> tuple[int, int]:
    return len(puzzle_input.get_lines()), len(puzzle_input.get_lines()[0])


def redirect_beam(reflector: str, beam_direction: tuple[int, int]) -> list[tuple[int, int]]:
    match reflector, beam_direction:
        case '|', (0, _):
            return [(1, 0), (-1, 0)]
        case '-', (_, 0):
            return [(0, 1), (0, -1)]
        case '\\', (x, y):
            return [(y, x)]
        case '/', (x, y):
            return [(-y, -x)]
        case _:
            return [beam_direction]


def count_energized_tiles(start_beam, contraption: dict[tuple[int, int], str], dims: tuple[int, int]) -> int:
    future_beams = {start_beam}
    past_beams = set()

    while len(future_beams) > 0:
        beam = future_beams.pop()
        past_beams.add(beam)
        tile, direction = beam
        for next_direction in redirect_beam(contraption[tile], direction):
            next_tile = tile[0] + next_direction[0], tile[1] + next_direction[1]
            if 0 <= next_tile[0] < dims[0] and 0 <= next_tile[1] < dims[1] \
                    and (next_tile, next_direction) not in past_beams:
                future_beams.add((next_tile, next_direction))

    return len({beam[0] for beam in past_beams})


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    contraption = parse_contraption(puzzle_input)
    dims = parse_dimensions(puzzle_input)
    start_beam = ((0, 0), (0, 1))
    return count_energized_tiles(start_beam, contraption, dims)


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    contraption = parse_contraption(puzzle_input)
    dims = parse_dimensions(puzzle_input)

    start_beams = []
    for row in range(dims[0]):
        start_beams.append(((row, 0), (0, 1)))
        start_beams.append(((row, dims[1] - 1), (0, -1)))
    for col in range(dims[1]):
        start_beams.append(((0, col), (1, 0)))
        start_beams.append(((dims[0] - 1, col), (-1, 0)))

    return max(count_energized_tiles(start_beam, contraption, dims) for start_beam in start_beams)
