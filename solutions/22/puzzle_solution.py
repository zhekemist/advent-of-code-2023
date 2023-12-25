import copy
import itertools
import re
import string
from itertools import product
from typing import NamedTuple, Self

import adventofcode as aoc


class Brick(NamedTuple):
    name: str
    start: tuple[int, int, int]
    end: tuple[int, int, int]

    def move_down_to(self, start_z: int) -> Self:
        difference = self.start[2] - start_z
        start = self.start[0], self.start[1], start_z
        end = self.end[0], self.end[1], self.end[2] - difference
        return Brick(self.name, start, end)

    def area(self) -> list[tuple[int, int]]:
        return [
            (x, y) for x, y in
            product(range(self.start[0], self.end[0] + 1), range(self.start[1], self.end[1] + 1))
        ]


def parse_bricks(puzzle_input: aoc.PuzzleInput) -> list[Brick]:
    digits = itertools.cycle(string.ascii_letters)
    return [
        Brick(next(digits), int_coordinates[:3], int_coordinates[3:])
        for coordinates in re.findall(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', puzzle_input.get())
        if (int_coordinates := tuple(map(int, coordinates)))
    ]


def get_base_dimensions(bricks: list[Brick]) -> tuple[int, int]:
    x_bound = max(bricks, key=lambda brick: brick.end[0]).end[0] + 1
    y_bound = max(bricks, key=lambda brick: brick.end[1]).end[1] + 1
    return x_bound, y_bound


def stack_bricks(bricks: list[Brick]) -> dict[Brick, list[Brick]]:
    sorted_bricks = sorted(bricks, key=lambda brick: brick.start[2], reverse=True)
    x_dim, y_dim = get_base_dimensions(bricks)

    occupied = [[0 for _ in range(y_dim)]
                for _ in range(x_dim)]

    stacked_bricks = []
    supported_by = {}
    while len(sorted_bricks) > 0:
        brick = sorted_bricks.pop()
        area = brick.area()
        z = max(occupied[x][y] for x, y in area) + 1

        moved_brick = brick.move_down_to(z)
        stacked_bricks.append(moved_brick)
        for x, y in area:
            occupied[x][y] = moved_brick.end[2]

        below = filter(lambda brick_below: brick_below.end[2] == (z - 1), stacked_bricks)
        supported_by[moved_brick] = [brick_below for brick_below in below if
                                     len(set(brick_below.area()) & set(area)) > 0]

    return supported_by


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    bricks = parse_bricks(puzzle_input)
    number_of_bricks = len(bricks)

    supported_by = stack_bricks(bricks)
    single_supporters = {
        bricks[0] for bricks in supported_by.values() if len(bricks) == 1
    }

    return number_of_bricks - len(single_supporters)


def get_falling_bricks(first_brick: Brick, supports: dict[Brick, list[Brick]],
                       supported_by: dict[Brick, list[Brick]]) -> int:
    supported_by = copy.deepcopy(supported_by)

    falling_bricks = set()
    next_to_fall = {first_brick}
    while len(next_to_fall) > 0:
        brick = next_to_fall.pop()
        if brick in falling_bricks:
            continue
        falling_bricks.add(brick)

        for supported_brick in supports[brick]:
            supported_by[supported_brick].remove(brick)
            if len(supported_by[supported_brick]) == 0:
                next_to_fall.add(supported_brick)

    return len(falling_bricks) - 1


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    bricks = parse_bricks(puzzle_input)
    supported_by = stack_bricks(bricks)

    single_supporters = {
        bricks[0] for bricks in supported_by.values() if len(bricks) == 1
    }

    supports = {
        brick: [other_brick for other_brick, supporting_bricks in supported_by.items() if brick in supporting_bricks]
        for brick in supported_by
    }

    return sum(get_falling_bricks(s, supports, supported_by) for s in single_supporters)
