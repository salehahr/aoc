from __future__ import annotations

import itertools
from typing import Iterable

import numpy as np

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, Direction


def _next_obstacle(
    obstacles: set[Coordinates],
    start: Coordinates,
    end: Coordinates = None,
    direction: Direction = None,
) -> Coordinates | None:
    next_coords = LineSegment(start, end=end, dir_=direction).path
    try:
        obstacle = next(filter(lambda coord: coord in obstacles, next_coords))
        return obstacle
    except StopIteration:
        return None


def _ray_to_obstacle(
    obstacles: set[Coordinates], start: Coordinates, direction: Direction
) -> tuple[LineSegment | None, Coordinates | None]:
    if next_obj := _next_obstacle(obstacles, start=start, direction=direction):
        next_pos = next_obj - direction
        if next_pos == start:
            return None, next_obj
        ls = LineSegment(start, end=next_pos)
    else:
        ls = LineSegment(start, dir_=direction)
    return ls, next_obj


class Guard:
    def __init__(self, pos0: Coordinates, direction0: Direction):
        self.pos = pos0
        self.direction = direction0

    def turn(self):
        self.direction = Direction.rotate_90(self.direction, clockwise=True)

    def travel(
        self,
        obstacles: set[Coordinates],
        jump_table: dict[
            tuple[Coordinates, Direction], tuple[LineSegment, Coordinates]
        ],
        dyn_obs: Coordinates = None,
    ) -> tuple[set[Coordinates], bool]:
        visited_ = {(self.pos, self.direction)}
        next_obj = "#"
        is_loop = False

        if dyn_obs:
            obstacles_ = obstacles | {dyn_obs}
        else:
            obstacles_ = obstacles

        while next_obj:
            if dyn_obs and (self.pos.r == dyn_obs.r or self.pos.c == dyn_obs.c):
                ls, next_obj = _ray_to_obstacle(obstacles_, self.pos, self.direction)
            else:
                ls, next_obj = jump_table[(self.pos, self.direction)]

            if ls:
                path = [(p, self.direction) for p in ls.path]
                if visited_ & set(path[1:]):
                    is_loop = True
                    break
                visited_ |= set(path)
                self.pos = ls.end
            self.turn()

        return visited_, is_loop


class LineSegment:
    """
    Line segment on a 2D map.
    """

    MIN_R: int = 0
    MIN_C: int = 0
    MAX_R: int
    MAX_C: int

    def __init__(
        self,
        start: Coordinates,
        end: Coordinates = None,
        dir_: Direction = None,
        num_steps: int | None = None,
    ):
        dir_ = dir_ if dir_ else Direction.from_coords(end - start)
        if num_steps is None:
            if end:
                num_steps = int((end - start).magnitude)
            else:
                num_steps = self.__get_max_num_steps(start, dir_)
        end = end if end is not None else start + (dir_.value * num_steps)

        self.start = start
        self.end = end
        self.dir = dir_

        self._n = num_steps + 1

    def __get_max_num_steps(self, start: Coordinates, dir_: Direction) -> int:
        if dir_.is_vertical:
            target_r = self.MIN_R if dir_ == Direction.UP else self.MAX_R
            num_steps = abs(target_r - start.r)
        else:
            target_c = self.MIN_C if dir_ == Direction.LEFT else self.MAX_C
            num_steps = abs(target_c - start.c)
        return num_steps

    def __len__(self) -> int:
        return self._n

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end} | {self.dir}"

    @property
    def path(self) -> Iterable[Coordinates]:
        num_steps = len(self) - 1
        return itertools.accumulate(
            (self.dir.value for _ in range(num_steps)),
            initial=self.start,
        )


@print_part
def solve(filepath: str, part: int = 1):
    map_ = get_array(filepath)
    height, width = map_.shape
    LineSegment.MAX_R = height - 1
    LineSegment.MAX_C = width - 1

    obstacles = set(Coordinates(*x) for x in np.argwhere(map_ == "#"))
    pos0 = Coordinates(*np.argwhere(map_ == "^")[0])

    lookup: dict[tuple[Coordinates, Direction], tuple[LineSegment, Coordinates]] = {}
    tiles = set(Coordinates(*x) for x in np.argwhere(map_ != "#"))
    all_coords_dirs = ((s, d) for s in tiles for d in Direction)
    for start, direction in all_coords_dirs:
        ls, next_obstacle = _ray_to_obstacle(obstacles, start, direction)
        lookup[(start, direction)] = (ls, next_obstacle)

    guard = Guard(pos0, direction0=Direction.UP)
    visited, _ = guard.travel(obstacles, lookup)
    seen, _ = zip(*visited)
    seen = set(seen)

    if part == 1:
        print_ans(len(seen), correct_ans=5305)
    else:
        n_obstacles = 0
        for o in seen - {pos0}:
            _, is_loop = Guard(pos0, Direction.UP).travel(obstacles, lookup, dyn_obs=o)
            n_obstacles += is_loop
        print_ans(n_obstacles, correct_ans=2143)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
