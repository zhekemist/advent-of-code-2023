from heapq import heappush, heappop
from typing import NamedTuple, Self

import adventofcode as aoc


def parse_block_costs(puzzle_input: aoc.PuzzleInput) -> list[list[int]]:
    return [[int(field) for field in line]
            for line in puzzle_input.get_lines()]


class CrucibleState(NamedTuple):
    position: tuple[int, int]
    direction: tuple[int, int]
    straight_moves: int

    def get_ensuing_states(self, max_straight_moves, min_straight_moves) -> list[Self]:
        ensuing_states = []
        if self.straight_moves < max_straight_moves:
            ensuing_states.append(self._move_towards(self.direction))
        if self.straight_moves >= min_straight_moves:
            d_row, d_col = self.direction
            ensuing_states.append(self._move_towards((d_col, d_row)))
            ensuing_states.append(self._move_towards((-d_col, -d_row)))
        return ensuing_states

    def _move_towards(self, direction: tuple[int, int]) -> Self:
        position = self.position[0] + direction[0], self.position[1] + direction[1]
        if direction == self.direction:
            straight_moves = self.straight_moves + 1
        else:
            straight_moves = 1
        return CrucibleState(position, direction, straight_moves)


def find_minimal_heat_loss(block_costs: list[list[int]], max_straight_moves: int, min_straight_moves: int = 0) -> int:
    rows, cols = len(block_costs), len(block_costs[0])

    seen_states = set()
    state_queue = []
    for init_row, init_col in [(0, 1), (1, 0)]:
        heappush(state_queue,
                 (block_costs[init_row][init_col], CrucibleState((init_row, init_col), (init_row, init_col), 1)))

    # type hints of `heappop` are somehow useless
    cost: int
    state: CrucibleState

    while True:
        cost, state = heappop(state_queue)

        if state.position == (rows - 1, cols - 1) and state.straight_moves >= min_straight_moves:
            return cost

        if state in seen_states:
            continue
        else:
            seen_states.add(state)

        for ensuing_state in state.get_ensuing_states(max_straight_moves, min_straight_moves):
            row, col = ensuing_state.position
            if 0 <= row < rows and 0 <= col < cols:
                heappush(state_queue, (cost + block_costs[row][col], ensuing_state))


@aoc.solution(part=aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    block_costs = parse_block_costs(puzzle_input)
    return find_minimal_heat_loss(block_costs, 3)


@aoc.solution(part=aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    block_costs = parse_block_costs(puzzle_input)
    return find_minimal_heat_loss(block_costs, 10, 4)
