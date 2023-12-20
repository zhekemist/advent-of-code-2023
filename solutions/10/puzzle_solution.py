from typing import TypeAlias

import adventofcode as aoc

PIPE_DIRECTIONS = {
    '|': ((-1, 0), (1, 0)),
    '-': ((0, 1), (0, -1)),
    'L': ((-1, 0), (0, 1)),
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)]
}

Position: TypeAlias = tuple[int, int]


def parse_grid(puzzle_input: aoc.PuzzleInput):
    start = None
    pipe_adjacencies = {}
    field_types = {}

    for row, line in enumerate(puzzle_input.get_lines()):
        for col, tile in enumerate(line):
            if tile == 'S':
                start = (row, col)
            elif tile in PIPE_DIRECTIONS:
                adjacent_pipes = [(row + d_row, col + d_col) for d_row, d_col
                                  in PIPE_DIRECTIONS[tile]]
                pipe_adjacencies[(row, col)] = adjacent_pipes
            field_types[(row, col)] = tile

    pipe_adjacencies[start] = [pipe for pipe, adjacent_pipes in pipe_adjacencies.items()
                               if start in adjacent_pipes]

    return start, pipe_adjacencies, field_types


def get_pipe_loop(start: Position, pipe_adjacencies: dict[Position, list[Position]]) -> list[Position]:
    last_pipe = start
    current_pipe = pipe_adjacencies[start][0]

    pipe_loop = [start]

    while current_pipe != start:
        pipe_loop.append(current_pipe)
        next_pipe = next(adj for adj in pipe_adjacencies[current_pipe]
                         if adj != last_pipe)
        last_pipe, current_pipe = current_pipe, next_pipe

    return pipe_loop


def get_polygon_area(corners: list[Position]) -> int:
    area = 0

    for i in range(len(corners)):
        j = (i + 1) % len(corners)
        area += (corners[i][1] + corners[j][1]) * (corners[i][0] - corners[j][0])

    return abs(area) // 2


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    start, pipe_adjacencies, _ = parse_grid(puzzle_input)
    pipe_loop = get_pipe_loop(start, pipe_adjacencies)
    return len(pipe_loop) // 2


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    start, pipe_adjacencies, field_types = parse_grid(puzzle_input)
    pipe_loop = get_pipe_loop(start, pipe_adjacencies)

    loop_corners = [pipe for pipe in pipe_loop if field_types[pipe] in 'SLJF7']
    loop_area = get_polygon_area(loop_corners)

    return loop_area - len(pipe_loop) // 2 + 1
