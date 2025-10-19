from __future__ import annotations

import math
from enum import Enum
from typing import Iterable, NamedTuple


def in_bounds(coords: Coordinates, map_height: int, map_width: int) -> bool:
    in_row = 0 <= coords.r < map_height
    in_col = 0 <= coords.c < map_width
    return in_row and in_col


def get_neighbours(
    rc: Coordinates, h: int = None, w: int = None, incl_diags: bool = False
) -> Iterable[Coordinates]:
    all_dirs = Direction if not incl_diags else CompassDirection
    neighbours = (rc + direction for direction in all_dirs)
    if h is None and w is None:
        return neighbours
    else:
        return filter(lambda nrc: in_bounds(nrc, h, w), neighbours)


BaseState = NamedTuple


class Coordinates(NamedTuple):
    r: int
    c: int

    def __repr__(self):
        return f"{(int(self.r), int(self.c))}"

    def __add__(self, other: Coordinates | Direction | CompassDirection | tuple):
        if isinstance(other, Coordinates):
            return Coordinates(self.r + other.r, self.c + other.c)
        elif isinstance(other, Direction) or isinstance(other, CompassDirection):
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
    def category(self) -> DirectionCategory:
        if self.is_vertical:
            return DirectionCategory.VERTICAL
        else:
            return DirectionCategory.HORIZONTAL

    @property
    def is_vertical(self) -> bool:
        return self in DirectionCategory.VERTICAL.value

    @property
    def is_horizontal(self) -> bool:
        return not self.is_vertical

    @staticmethod
    def from_coords(coords: Coordinates) -> Direction:
        magnitude = coords.magnitude
        rc = [int(getattr(coords, val)) // magnitude for val in "rc"]
        return Direction(Coordinates(*rc))

    @staticmethod
    def rotate_90(direction: Direction, clockwise: bool) -> Direction:
        cval = complex(*direction.value)
        if clockwise:
            cval *= 0 - 1j
        else:
            cval *= 0 + 1j

        for d in Direction:
            if d.value == Coordinates(int(cval.real), int(cval.imag)):
                return d

    def get_orthogonal(self) -> Direction:
        match self:
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case _:
                raise ValueError


class CompassDirection(Enum):
    NORTH = Direction.UP.value
    SOUTH = Direction.DOWN.value
    EAST = Direction.RIGHT.value
    WEST = Direction.LEFT.value
    NORTHWEST = Coordinates(-1, -1)
    NORTHEAST = Coordinates(-1, 1)
    SOUTHWEST = Coordinates(1, -1)
    SOUTHEAST = Coordinates(1, 1)


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


CHAR_TO_DIRECTIONS = {
    ">": Direction.RIGHT,
    "^": Direction.UP,
    "<": Direction.LEFT,
    "v": Direction.DOWN,
}
