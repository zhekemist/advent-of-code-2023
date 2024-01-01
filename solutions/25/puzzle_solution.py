import random
from collections import defaultdict, Counter
from typing import TypeAlias

import adventofcode as aoc

Node: TypeAlias = frozenset[str]
AdjacencyList: TypeAlias = dict[Node, Counter[Node]]


def parse_connections(puzzle_input: aoc.PuzzleInput) -> AdjacencyList:
    connections = defaultdict(Counter)
    for line in puzzle_input.get_lines():
        component, connected_components = line.split(': ')
        component = frozenset([component])

        for connected_component in connected_components.split(' '):
            connected_component = frozenset([connected_component])
            connections[component][connected_component] = 1
            connections[connected_component][component] = 1

    return connections


def contract_edge(edge: tuple[Node, Node], connections: AdjacencyList) -> None:
    contracted_node = edge[0] | edge[1]

    neighbors = connections[edge[0]] + connections[edge[1]]
    for endpoint in edge:
        del neighbors[endpoint]
        del connections[endpoint]

    connections[contracted_node] = neighbors

    for neighbor, edge_count in connections[contracted_node].items():
        updated_neighbor = connections[neighbor].copy()

        updated_neighbor[contracted_node] = edge_count
        for endpoint in edge:
            updated_neighbor.pop(endpoint, None)

        connections[neighbor] = updated_neighbor


def find_random_cut(connections: AdjacencyList) -> tuple[set[str], set[str], int]:
    connections = connections.copy()

    while len(connections) > 2:
        source = random.choice(list(connections))
        target = random.choice(list(connections[source]))

        contract_edge((source, target), connections)

    first_subset, second_subset = list(connections)
    return first_subset, second_subset, connections[first_subset].total()


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    connections = parse_connections(puzzle_input)

    while True:
        first_group, second_group, cut_edges = find_random_cut(connections)
        if cut_edges == 3:
            return len(first_group) * len(second_group)


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    return '\N{GLOWING STAR}'
