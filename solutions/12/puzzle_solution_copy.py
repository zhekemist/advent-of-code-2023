import re

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


INDENT = ''


def find_new(line: str, groups, current=0):
    global INDENT
    while current < len(line) and line[current] == '.':
        current += 1

    if len(groups) == 0:
        # print(f'{INDENT}SUCESS.')
        return 1

    if current >= len(line) or line[current] == '.':
        # print(f'{INDENT}FAILURE.')
        return 0

    if '.' in line[current:]:
        next_point = line[current:].find('.')
    else:
        next_point = len(line) - current

    if next_point < groups[0]:
        return find_new(line, groups, current + next_point + 1)

    offset_bound = max(next_point - groups[0] + 1, 0)

    # print(
    #    f'--------\n{INDENT}Line: {line[current:]}\n{INDENT}Groups: {groups}\n{INDENT}NextPoint:{next_point}\n{INDENT}OffsetBound: {offset_bound}')

    sub_sum = 0

    INDENT += '\t'
    for offset in range(offset_bound):
        end = current + offset + groups[0]
        if offset + current >= 1 and line[offset + current - 1] == '#':
            continue
        if end >= len(line) or line[end] != '#':
            sub_sum += find_new(line, groups[1:], end + 1)
    INDENT = INDENT[:-1]

    return sub_sum


def unfold(input):
    damages = '?'.join(input[0] for _ in range(5))
    groups = input[1] * 5
    return damages, groups


# @aoc.solution(aoc.Part.ONE)
def solve_part_one(puzzle_input: aoc.PuzzleInput):
    input = parse(puzzle_input.get_lines())
    return sum(find_combinations(*elem) for elem in input)


# @aoc.solution(aoc.Part.TWO)
def solve_part_two(puzzle_input: aoc.PuzzleInput):
    input = parse(puzzle_input.get_lines())
    for i in input:
        print(i)
        print(find_new(*unfold(i)))
    # return sum(find_new(*unfold(elem)) for elem in input if print(elem) is None)
