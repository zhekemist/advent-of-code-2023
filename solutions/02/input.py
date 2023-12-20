from enum import Enum

import adventofcode as aoc


class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3


COLOR_MAP = {
    'blue': Color.BLUE,
    'green': Color.GREEN,
    'red': Color.RED
}


def parse_line(line: str) -> tuple[int, list[dict[Color, int]]]:
    game_str, drawings_str = line.split(": ")
    game_id = int(game_str.split(' ')[1])

    drawings = []
    for drawing_str in drawings_str.split('; '):
        drawing = {}
        for per_color_str in drawing_str.split(', '):
            count_str, color_str = per_color_str.split(' ')
            color = COLOR_MAP[color_str]
            count = int(count_str)
            drawing[color] = count
        drawings.append(drawing)

    return game_id, drawings


def load_games(puzzle_input: aoc.PuzzleInput) -> dict[int, list[dict[Color, int]]]:
    result = {}

    for line in puzzle_input.get_lines():
        game_id, drawings = parse_line(line)
        result[game_id] = drawings

    return result
