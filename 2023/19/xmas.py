from typing import NamedTuple

from condition import Condition


class Xmas(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self):
        return sum([self.__getattribute__(x) for x in "xmas"])

    def satisfies(self, condition: Condition) -> bool:
        att_, rng = condition.c_range
        return getattr(self, att_) in rng
