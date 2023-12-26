from collections import deque, defaultdict
from typing import TypeAlias

import adventofcode as aoc

Intersection: TypeAlias = tuple[int, int]
TrailsMap: TypeAlias = dict[Intersection, dict[Intersection, int]]
AdjacencyMap = dict[Intersection, list[Intersection]]

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ALLOWED_SLOPES = {(0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}


def parse_trails(puzzle_input: aoc.PuzzleInput, directed: bool = True) -> tuple[AdjacencyMap, TrailsMap, int]:
    trails_map = puzzle_input.get_lines()
    size = len(trails_map)

    start = (0, 1)
    end = (size - 1, size - 2)

    adjacency_map = defaultdict(list)
    trails = defaultdict(dict)

    next_nodes = deque([((1, 1), start, 1)])
    visited_nodes = set()
    while len(next_nodes) > 0:
        node, predecessor, distance = next_nodes.popleft()

        if node in visited_nodes:
            continue
        visited_nodes.add(node)

        last_node = predecessor
        while True:
            if node == end:
                neighbors = []
            else:
                neighbors = [
                    (neighbor, (d_row, d_col))
                    for d_row, d_col in DIRECTIONS
                    if trails_map[row := node[0] + d_row][col := node[1] + d_col] != '#'
                       and (neighbor := (row, col)) != last_node
                ]

            if len(neighbors) != 1:
                break

            last_node = node
            node = neighbors[0][0]
            distance += 1

        adjacency_map[predecessor].append(node)
        trails[predecessor][node] = distance

        if not directed:
            adjacency_map[node].append(predecessor)
            trails[node][predecessor] = distance

        for (row, col), direction in neighbors:
            if trails_map[row][col] == ALLOWED_SLOPES[direction]:
                next_nodes.append(((row, col), node, 1))

    return adjacency_map, trails, size


def get_maximal_hike_length(adjacency_map: AdjacencyMap, trails: TrailsMap, size: int) -> int:
    maximal_hike_length = 0
    start = (0, 1)
    end = (size - 1, size - 2)

    next_states = deque([(start, 0, frozenset())])
    while len(next_states) > 0:
        intersection, distance, seen_intersections = next_states.pop()

        if intersection == end:
            maximal_hike_length = max(distance, maximal_hike_length)
            continue

        neighbors = [neighbor for neighbor in adjacency_map[intersection]
                     if neighbor not in seen_intersections]

        seen_intersections |= {intersection}
        for neighbor in neighbors:
            neighbor_distance = distance + trails[intersection][neighbor]
            next_states.append((neighbor, neighbor_distance, seen_intersections))

    return maximal_hike_length


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    adjacency_map, trails, size = parse_trails(puzzle_input)
    return get_maximal_hike_length(adjacency_map, trails, size)


@aoc.solution(aoc.Part.TWO)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    adjacency_map, trails, size = parse_trails(puzzle_input, directed=False)
    return get_maximal_hike_length(adjacency_map, trails, size)
