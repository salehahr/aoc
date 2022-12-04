# https://adventofcode.com/2021/day/5

import re

import context
import numpy as np

from tools import parse_lines, print_part


def coordinates_to_int(coordinates: str) -> list[int]:
    """
    Parses coordinates in the string form of '0,9 -> 5,9'
    to a list in integers [0, 9, 5, 9].
    """
    pattern = r"(\d+),(\d+) .* (\d+),(\d+)"
    element_strings = re.match(pattern, coordinates).group(1, 2, 3, 4)
    return [int(elem) for elem in element_strings]


def parse_line_coordinates(filepath: str) -> np.ndarray:
    """
    Extracts line coordinates from file asa numpy array.
    Array columns: x1, y1, x2, y2
    """
    coordinates = parse_lines(filepath)
    start_end_coords = [coordinates_to_int(coords) for coords in coordinates]
    return np.array(start_end_coords)


def get_max_coords(start_end_coords: np.ndarray) -> tuple[int, int]:
    """
    Obtains maximum values for each coordinate axis.
    """
    max_values = np.max(start_end_coords, 0)
    max_x = max(max_values[0], max_values[2])
    max_y = max(max_values[1], max_values[3])

    return max_x, max_y


class Grid(object):
    """
    Grid object on which straight lines can be drawn.
    """

    def __init__(self, max_x: int, max_y: int):
        self._max_x = max_x
        self._max_y = max_y

        self._data: optional[np.ndarray] = None
        self._draw_diagonals: bool = False

        self.reset()

    def reset(self) -> None:
        self._data = np.zeros((self._max_y + 1, self._max_x + 1))

    def draw(self, lines_: np.ndarray, diagonals: bool = False) -> None:
        self._draw_diagonals = diagonals

        for line in lines_:
            self._draw_line(line)

    def _draw_line(self, start_end_coords: np.ndarray) -> None:
        x1, y1, x2, y2 = start_end_coords

        if x1 == x2:
            minv = min(y1, y2)
            maxv = max(y1, y2)

            for i in range(minv, maxv + 1):
                self._data[i, x1] = self._data[i, x1] + 1

        elif y1 == y2:
            minv = min(x1, x2)
            maxv = max(x1, x2)

            for i in range(minv, maxv + 1):
                self._data[y1, i] = self._data[y1, i] + 1

        elif self._draw_diagonals:
            increment_x = 1 if x2 >= x1 else -1
            x_coords = list(range(x1, x2 + increment_x, increment_x))

            increment_y = 1 if y2 >= y1 else -1
            y_coords = list(range(y1, y2 + increment_y, increment_y))

            for x, y in zip(x_coords, y_coords):
                self._data[y, x] = self._data[y, x] + 1

    @property
    def num_overlaps(self) -> int:
        return len(self._data[self._data >= 2])


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_line_coordinates(filepath)
    max_coords = get_max_coords(lines)

    grid = Grid(*max_coords)
    grid.draw(lines, diagonals=part == 2)
    print(grid.num_overlaps)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
