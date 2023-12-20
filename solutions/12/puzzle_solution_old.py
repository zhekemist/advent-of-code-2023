import regex as re

import adventofcode as aoc


def parse(input_lines):
    return [
        (line.split(' ')[0], tuple(int(i) for i in line.split(' ')[1].split(',')))
        for line in input_lines
    ]


def is_feasible(damages: str, groups: tuple) -> bool:
    pattern = '[.?]*?' + '[.?]+?'.join([f'[#?]{{{group}}}' for group in groups]) + '[.?]*?'
    return re.fullmatch(pattern, damages) is not None


def find_combinations(damages: str, groups: tuple) -> int:
    if not is_feasible(damages, groups):
        return 0
    elif '?' not in damages:
        return 1

    return (find_combinations(damages.replace('?', '#', 1), groups)
            + find_combinations(damages.replace('?', '.', 1), groups))


GROUP_PATTERN = '(?<!#)[#?]{{{}}}(?!#)'

INDENT = 0


def print_indented(string):
    # print(INDENT * '\t', string)
    pass


CACHE = {}


def fast_find(string, groups):
    global INDENT

    if len(groups) == 0:
        return 1 if '#' not in string else 0

    next_group = groups[0]
    pattern = re.compile(GROUP_PATTERN.format(next_group))

    sub_sum = 0
    INDENT += 1
    for match in pattern.finditer(string, overlapped=True):
        if '#' in string[:match.start()]:
            continue
        print_indented(f'{match.group()} at {match.start()}.')
        sub_str = string[match.end() + 1:]
        sub_grp = groups[1:]
        if (sub_str, sub_grp) in CACHE:
            sub_sum += CACHE[(sub_str, sub_grp)]
        else:
            result = fast_find(sub_str, sub_grp)
            CACHE[(sub_str, sub_grp)] = result
            sub_sum += result
    INDENT -= 1
    return sub_sum


def unfold(input, n=5):
    damages = '?'.join(input[0] for _ in range(n))
    groups = input[1] * n
    return damages, groups


# @aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    input = parse(puzzle_input.get_lines())
    return sum(find_combinations(*elem) for elem in input)


# @aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    input = parse(puzzle_input.get_lines())

    return sum(fast_find(*unfold(i)) for i in input)
