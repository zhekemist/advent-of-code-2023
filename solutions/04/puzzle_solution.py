import re

import adventofcode as aoc


def parse_card(line: str) -> int:
    winning_numbers, received_numbers = line.split(':')[1].split('|')
    return len(set(re.findall(r'(\d+)', winning_numbers))
               & set(re.findall(r'(\d+)', received_numbers)))


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    return sum(0 if (matches := parse_card(line)) == 0 else (1 << matches - 1) for line in puzzle_input.get_lines())


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    number_of_cards = len(puzzle_input.get_lines())
    match_counts = [parse_card(line) for line in puzzle_input.get_lines()]
    copies_per_card = [0] * number_of_cards
    for card, match_count in enumerate(reversed(match_counts)):
        card = number_of_cards - (card + 1)
        copies = 1 + sum(copies_per_card[card + 1:card + match_count + 1])
        copies_per_card[card] = copies

    return sum(copies_per_card)
