import re
from typing import Optional

import requests


class PuzzleInput:
    def __init__(self, path: str):
        self.path: str = path
        self.content: Optional[str] = None
        self.__load()

    def get(self) -> str:
        return self.content

    def get_lines(self) -> list[str]:
        return self.content.splitlines()

    def split(self, pattern: str) -> list[str]:
        return re.split(pattern, self.content)

    def __load(self):
        with open(self.path) as file:
            self.content = file.read()


def download_input(day: int, session_token: str, output_file: str) -> None:
    url = f'https://adventofcode.com/2023/day/{day}/input'
    response = requests.get(url, cookies={'session': session_token})
    response.raise_for_status()

    with open(output_file, 'w') as file:
        file.write(response.text)
