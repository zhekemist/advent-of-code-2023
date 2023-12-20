import itertools
import typing
from functools import singledispatchmethod
from typing import NamedTuple, Self

import math

T = typing.TypeVar('T')


class Interval(typing.NamedTuple):
    start: int
    end: int

    def __contains__(self, value: int) -> bool:
        return self.start <= value < self.end

    def __and__(self, other: typing.Self) -> Self:
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        return Interval(start, end)

    def __len__(self) -> int:
        return max(0, self.end - self.start)

    def shift(self, x: int) -> Self:
        return Interval(self.start + x, self.end + x)


class Map(NamedTuple):
    offsets: dict[Interval, int]

    @singledispatchmethod
    def apply(self, image: T) -> T:
        return image

    @apply.register
    def _(self, image: int) -> int:
        for interval, offset in self.offsets.items():
            if image in interval:
                return image + offset
        return image

    @apply.register
    def _(self, image: list) -> list[Interval]:
        return list(itertools.chain(*map(self._apply_to_interval, image)))

    def _apply_to_interval(self, image: Interval) -> list[Interval]:
        return [
            intersection.shift(offset)
            for map_interval, offset in self.offsets.items()
            if len(intersection := image & map_interval) > 0
        ]

    @classmethod
    def from_text(cls, text: str) -> Self:
        offsets = {}
        for line in text.splitlines()[1:]:
            dst_start, src_start, length = map(int, line.split(' '))
            src_interval = Interval(src_start, src_start + length)
            offsets[src_interval] = dst_start - src_start
        sorted_items = sorted(offsets.items())
        ordered_items = [(Interval(0, sorted_items[0][0][0]), 0),
                         *sorted_items,
                         (Interval(sorted_items[-1][0][1], math.inf), 0)]
        return Map(dict(ordered_items))
