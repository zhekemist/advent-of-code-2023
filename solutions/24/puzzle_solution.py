import itertools
import re

import numpy as np

import adventofcode as aoc


def parse_hailstones(puzzle_input: aoc.PuzzleInput) -> list[tuple[np.ndarray, np.ndarray]]:
    return [
        (casted_numbers[:3], casted_numbers[3:])
        for numbers in re.findall(r'(\d+), (\d+), (\d+) @ ([- ]?\d+), ([- ]?\d+), ([- ]?\d+)', puzzle_input.get())
        for casted_numbers in [np.fromiter(map(int, numbers), dtype=int, count=6)]
    ]


def intersect_in_area(hailstone_one: np.ndarray, hailstone_two: np.ndarray, area_start: int, area_end: int) -> bool:
    position_one = hailstone_one[0][:2]
    position_two = hailstone_two[0][:2]

    velocity_one = hailstone_one[1][:2]
    velocity_two = hailstone_two[1][:2]

    velocity_matrix = np.concatenate([velocity_one, -velocity_two]).reshape(2, 2).T
    d_position = position_two - position_one

    if np.linalg.det(velocity_matrix) == 0:
        return False

    intersection_times = np.linalg.solve(velocity_matrix, d_position)
    if (intersection_times < 0).any():
        return False

    intersection = position_one + velocity_one * intersection_times[0]
    return ((intersection >= area_start) & (intersection <= area_end)).all()


def count_intersections(hailstones: list[tuple[np.ndarray, np.ndarray]], area_start: int, area_end: int) -> int:
    return sum(1 for hailstone_pair in itertools.combinations(hailstones, 2)
               if intersect_in_area(*hailstone_pair, area_start, area_end))


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    hailstones = parse_hailstones(puzzle_input)
    return count_intersections(hailstones, 200000000000000, 400000000000000)


def cross_product_matrix(vector):
    rows = []
    for i in range(0, 3):
        unit_vector = np.zeros((1, 3), dtype=int)
        unit_vector[0, i] = 1
        row = np.cross(vector, unit_vector)
        rows.append(row)
    return np.concatenate(rows)


def make_linear_equations(hailstone_one, hailstone_two):
    position_one, velocity_one = hailstone_one
    position_two, velocity_two = hailstone_two

    coefficients = np.concatenate([
        cross_product_matrix(velocity_one - velocity_two), cross_product_matrix(position_two - position_one)
    ], axis=1)
    constants = np.cross(position_one, velocity_one) - np.cross(position_two, velocity_two)
    return coefficients, constants


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    hailstones = parse_hailstones(puzzle_input)

    linear_equations = [
        make_linear_equations(hailstones[0], hailstones[1]),
        make_linear_equations(hailstones[1], hailstones[2])
    ]

    A = np.concatenate([x[0] for x in linear_equations])
    b = np.concatenate([x[1] for x in linear_equations])

    solution = np.linalg.solve(A, b)

    return round(np.sum(solution[:3])[0])
