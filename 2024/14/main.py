import math
import re
from typing import ClassVar

from tools import parse_lines, print_ans, print_part
from tools.generic_types import Coordinates


class Map:
    HEIGHT: ClassVar[int]
    WIDTH: ClassVar[int]
    MIDDLE_ROW: ClassVar[int]
    MIDDLE_COL: ClassVar[int]


class Robot:
    def __init__(self, pos: Coordinates, velocity: Coordinates):
        self._pos0 = pos
        self._v = velocity

    def simulate_move(self, t: int) -> Coordinates:
        nr, nc = self._pos0 + t * self._v
        return Coordinates(nr % Map.HEIGHT, nc % Map.WIDTH)

    @staticmethod
    def quadrant(pos: Coordinates) -> int:
        if pos.r == Map.MIDDLE_ROW or pos.c == Map.MIDDLE_COL:
            return 0

        is_top = pos.r < Map.MIDDLE_ROW
        is_left = pos.c < Map.MIDDLE_COL
        if is_top:
            return 1 if is_left else 2
        else:
            return 4 if is_left else 3


XY_PATTERN = r"\w=(-?\d+),(-?\d+)"


def __get_xy_values(line: str) -> tuple[Coordinates, ...]:
    return tuple(Coordinates(*map(int, xy)) for xy in re.findall(XY_PATTERN, line))


@print_part
def solve(filepath: str, part: int = 1):
    if "short" in filepath:
        Map.HEIGHT, Map.WIDTH = 11, 7
    else:
        Map.HEIGHT, Map.WIDTH = (101, 103)
    Map.MIDDLE_ROW = Map.HEIGHT // 2
    Map.MIDDLE_COL = Map.WIDTH // 2

    robots = tuple(Robot(*__get_xy_values(line)) for line in parse_lines(filepath))
    if part == 1:
        from collections import Counter

        positions = (robot.simulate_move(100) for robot in robots)
        quadrants = Counter(map(Robot.quadrant, positions))
        ans = math.prod(v for k, v in quadrants.items() if k > 0)
    else:
        # no image: high noise → high pixel variance
        # image available: low noise → low pixel variance

        #  https://www.reddit.com/r/adventofcode/comments/1hdvhvu/comment/m1zws1g/
        from statistics import variance

        t_min_rvar, min_rvar = 0, 1000 * 10
        t_min_cvar, min_cvar = 0, 1000 * 10

        for t in range(Map.WIDTH):
            rs, cs = zip(*(robot.simulate_move(t) for robot in robots))
            if (rvar := variance(rs)) < min_rvar:
                min_rvar = rvar
                t_min_rvar = t
            if (cvar := variance(cs)) < min_cvar:
                min_cvar = cvar
                t_min_cvar = t

        # t_min = t_min_rvar + n*H = t_min_rvar (mod H)
        # t_min = t_min_cvar + m*W = t_min_cvar (mod W)

        # Chinese Remainder Theorem
        # t_min_rvar + n*H = t_min_cvar (mod W)
        # n*H = t_min_cvar - t_min_rvar (mod W)
        # n = inv.H.W * (t_min_cvar - t_min_rvar) (mod W)

        n = (pow(Map.HEIGHT, -1, Map.WIDTH) * (t_min_cvar - t_min_rvar)) % Map.WIDTH
        ans = t_min_rvar + n * Map.HEIGHT

    print_ans(ans, correct_ans=226548000 if part == 1 else 7753)


if __name__ == "__main__":
    # FILEPATH = "input_short"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
