import glob
import importlib
from typing import Callable, Any, Self

from .common import Part
from .puzzleinput import PuzzleInput


def load_solutions(source_dir: str) -> None:
    for module_file in glob.glob(source_dir + '/*.py'):
        module_name = module_file.split('.')[0].replace('/', '.')
        importlib.import_module(module_name)


class solution:
    solution_registry: dict[Part, Self] = {}

    @classmethod
    def for_part(cls, part: Part) -> Self:
        if part not in cls.solution_registry:
            raise RuntimeError(f'No solution for part {part.value} known.')
        return cls.solution_registry[part]

    @classmethod
    def exists_for_part(cls, part: Part) -> bool:
        return part in cls.solution_registry

    def __init__(self, part: Part):
        self.part = part
        self.function = None

    def __call__(self, function: Callable[[PuzzleInput], Any]) -> Callable[[PuzzleInput], Any]:
        self.function = function
        self.__register()
        return function

    def for_input(self, puzzle_input: PuzzleInput) -> Any:
        return self.function(puzzle_input)

    def __register(self):
        if self.part in solution.solution_registry:
            raise RuntimeWarning(f'Solution for part {self.part.value} already exists, but another one was registered.')
        solution.solution_registry[self.part] = self
