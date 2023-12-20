import argparse

import adventofcode as aoc

HEADER = "=" * 11 + " Day {} " + "=" * 11
TEST_HEADER = "=" * 7 + " Day {} :: TEST " + "=" * 7
SECTION_HEADER = "-" * 10 + " Part {} " + "-" * 10
FOOTER = 30 * "="


def run(config: aoc.Config, test_mode: bool) -> None:
    aoc.load_solutions(config.SOLUTION_FOLDER)

    if test_mode:
        print(TEST_HEADER.format(config.DAY_STR))
        puzzle_input = aoc.PuzzleInput(config.EXAMPLE_INPUT_PATH)
    else:
        print(HEADER.format(config.DAY_STR))
        puzzle_input = aoc.PuzzleInput(config.INPUT_PATH)

    for part in aoc.Part:
        print(SECTION_HEADER.format(part.name))
        if aoc.solution.exists_for_part(part):
            result = aoc.solution.for_part(part).for_input(puzzle_input)
            if result is not None:
                print(f'Solution: {result}')
                continue
        print("No solution exists yet.")

    print(FOOTER)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Runner for AOC')
    parser.add_argument('config', help="path to configuration file")
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-d', '--day', type=int)
    args = parser.parse_args()

    run(aoc.Config.load(args.config, args.day), args.test)
