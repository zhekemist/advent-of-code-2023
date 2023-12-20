import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import adventofcode as aoc


def run(config: aoc.Config) -> None:
    print(f'Starting setup for day {config.DAY} ...')

    solution_folder = Path(config.SOLUTION_FOLDER)
    solution_folder.mkdir(parents=True)
    default_solution_file = solution_folder.joinpath(config.SOLUTION_DEFAULT_FILE)
    default_solution_file.write_text(config.SOLUTION_TEMPLATE)

    example_input = Path(config.EXAMPLE_INPUT_PATH)
    example_input.touch()

    print(f'Created basic directories and files.')

    with open('keys.json') as file:
        session_token = json.load(file)['aoc-session-token']

    now = datetime.now()
    then = datetime(now.year, now.month, config.DAY, config.START_HOUR)
    waiting_time = (then - now).total_seconds()

    if waiting_time > 0:
        print(f'Waiting for input to be available ...')
        time.sleep(waiting_time)

    aoc.download_input(config.DAY, session_token, config.INPUT_PATH)
    print(f'Downloaded input.')

    print(f'Setup complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Automatic Setup for AOC')
    parser.add_argument('config', help="path to configuration file")
    parser.add_argument('-d', '--day', type=int)
    args = parser.parse_args()

    run(aoc.Config.load(args.config, args.day))
