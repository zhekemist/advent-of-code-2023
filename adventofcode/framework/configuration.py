import datetime
import json
from dataclasses import dataclass
from typing import Self


@dataclass(slots=True)
class Config:
    DAY: int
    DAY_STR: str
    START_HOUR: int

    SOLUTION_FOLDER: str
    SOLUTION_DEFAULT_FILE: str
    SOLUTION_TEMPLATE: str

    INPUT_PATH: str
    EXAMPLE_INPUT_PATH: str

    def __init__(self, config_values: dict):
        for key, value in config_values.items():
            self.__setattr__(key, value)

    @classmethod
    def load(cls, config_file: str, day: int = None) -> Self:
        if day is None:
            day = datetime.date.today().day
        day_str = f'{day:0>2}'

        with open(config_file) as file:
            raw_config = json.load(file)

        config = {key: (value.format(DAY=day, DAY_STR=day_str) if isinstance(value, str) else value)
                  for key, value in raw_config.items()}

        config['DAY'] = day
        config['DAY_STR'] = day_str

        return Config(config)
