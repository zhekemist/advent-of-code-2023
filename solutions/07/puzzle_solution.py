import re
from collections import Counter
from functools import partial

import adventofcode as aoc


def parse_hands(puzzle_input: aoc.PuzzleInput) -> list[tuple[str, int]]:
    return [
        (hand, int(bid))
        for hand, bid in re.findall(r'(\w+) (\d+)', puzzle_input.get())
    ]


HAND_VALUES = {
    (1, 5): 6,
    (2, 4): 5,
    (2, 3): 4,
    (3, 3): 3,
    (3, 2): 2,
    (4, 2): 1,
    (5, 1): 0
}

STANDARD_ORDER = '23456789TJQKA'
JOKER_ORDER = 'J23456789TQKA'


def apply_jokers(card_counts: Counter) -> Counter:
    if 'J' not in card_counts:
        return card_counts

    joker_count = card_counts['J']
    del card_counts['J']

    if len(card_counts) > 0:
        card_counts[card_counts.most_common(1)[0][0]] += joker_count
    else:
        card_counts['X'] = 5

    return card_counts


def hand_key(hand_and_bid: tuple[str, int], jokers: bool = False) -> tuple:
    hand = hand_and_bid[0]

    card_counts = Counter(hand)
    if jokers:
        card_counts = apply_jokers(card_counts)

    different_cards = len(card_counts)
    most_common_cards = card_counts.most_common(1)[0][1]
    hand_value = HAND_VALUES[(different_cards, most_common_cards)]

    card_order = STANDARD_ORDER if not jokers else JOKER_ORDER
    card_values = tuple(map(card_order.index, hand))

    return hand_value, card_values


@aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    hands = parse_hands(puzzle_input)
    sorted_hands = sorted(hands, key=hand_key)
    return sum((pos + 1) * bid for pos, (_, bid) in enumerate(sorted_hands))


@aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    hands = parse_hands(puzzle_input)
    sorted_hands = sorted(hands, key=partial(hand_key, jokers=True))
    return sum((pos + 1) * bid for pos, (_, bid) in enumerate(sorted_hands))
