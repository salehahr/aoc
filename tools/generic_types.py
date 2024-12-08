from __future__ import annotations

import math
from enum import Enum
from typing import Iterable, NamedTuple


def in_bounds(coords: Coordinates, map_height: int, map_width: int) -> bool:
    in_row = 0 <= coords.r < map_height
    in_col = 0 <= coords.c < map_width
    return in_row and in_col


def get_neighbours(rc: Coordinates, h: int, w: int) -> Iterable[Coordinates]:
    return filter(
        lambda nrc: in_bounds(nrc, h, w), (rc + direction for direction in Direction)
    )


BaseState = NamedTuple


class Coordinates(NamedTuple):
    r: int
    c: int

    def __repr__(self):
        return f"{(self.r, self.c)}"

    def __add__(self, other: Coordinates | Direction | tuple):
        if isinstance(other, Coordinates):
            return Coordinates(self.r + other.r, self.c + other.c)
        elif isinstance(other, Direction):
            return self + Coordinates(*other.value)
        elif isinstance(other, tuple):
            return self + Coordinates(*other)
        else:
            raise NotImplementedError

    def __sub__(self, other: Coordinates | Direction | tuple):
        if isinstance(other, Coordinates):
            return Coordinates(self.r - other.r, self.c - other.c)
        elif isinstance(other, Direction):
            return self - Coordinates(*other.value)
        elif isinstance(other, tuple):
            return self - Coordinates(*other)
        else:
            raise NotImplementedError

    def __mul__(self, other: int):
        return Coordinates(self.r * other, self.c * other)

    def __rmul__(self, other: int):
        return self.__mul__(other)

    @property
    def magnitude(self):
        return math.sqrt(self.r**2 + self.c**2)


class Direction(Enum):
    UP = Coordinates(-1, 0)
    DOWN = Coordinates(1, 0)
    LEFT = Coordinates(0, -1)
    RIGHT = Coordinates(0, 1)

    def __repr__(self):
        return self.name[0]

    @property
    def is_vertical(self) -> bool:
        return self in DirectionCategory.VERTICAL.value

    @staticmethod
    def from_coords(coords: Coordinates) -> Direction:
        magnitude = coords.magnitude
        rc = [int(getattr(coords, val)) // magnitude for val in "rc"]
        return Direction(Coordinates(*rc))


class DirectionCategory(Enum):
    VERTICAL = (Direction.UP, Direction.DOWN)
    HORIZONTAL = (Direction.LEFT, Direction.RIGHT)

    def __lt__(self, other: DirectionCategory) -> bool:
        return True

    @property
    def opposite(self) -> DirectionCategory:
        match self:
            case DirectionCategory.VERTICAL:
                return DirectionCategory.HORIZONTAL
            case DirectionCategory.HORIZONTAL:
                return DirectionCategory.VERTICAL
