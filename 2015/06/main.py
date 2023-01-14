import re
from dataclasses import dataclass

import numpy as np

from tools import parse_lines, print_ans, print_part

GRID_DIM = 1_000


@dataclass
class Point:
    x: int
    y: int


class Grid:
    def __init__(self, part: int):
        if part == 1:
            self._array = np.full((GRID_DIM, GRID_DIM), False)
        else:
            self._array = np.zeros((GRID_DIM, GRID_DIM))

    def print(self):
        print(self._array)

    def toggle_p1(self, command: str, start: Point, end: Point):
        if command == "on":
            self._array[start.x : end.x + 1, start.y : end.y + 1] = True
        elif command == "off":
            self._array[start.x : end.x + 1, start.y : end.y + 1] = False
        else:
            current = self._array[start.x : end.x + 1, start.y : end.y + 1]
            self._array[start.x : end.x + 1, start.y : end.y + 1] = np.logical_not(
                current
            )

    def toggle_p2(self, command: str, start: Point, end: Point):
        if command == "on":
            self._array[start.x : end.x + 1, start.y : end.y + 1] += 1
        elif command == "off":
            self._array[start.x : end.x + 1, start.y : end.y + 1] -= 1
            self._array = np.where(self._array < 0, 0, self._array)
        else:
            self._array[start.x : end.x + 1, start.y : end.y + 1] += 2

    @property
    def lit(self) -> int:
        return np.count_nonzero(self._array)

    @property
    def sum(self):
        return np.sum(self._array, axis=None)


def _parse_commands(line):
    command, p_start, p_end = re.search(
        r".*(on|off|toggle).* (\d+,\d+) .* (\d+,\d+)", line
    ).groups()
    return command, Point(*eval(p_start)), Point(*eval(p_end))


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    if part == 1:
        grid = Grid(part)
        for command_data in map(_parse_commands, lines):
            grid.toggle_p1(*command_data)
        print_ans(grid.lit, 569999)
    else:
        grid = Grid(part)
        for command_data in map(_parse_commands, lines):
            grid.toggle_p2(*command_data)
        print_ans(grid.sum)


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
