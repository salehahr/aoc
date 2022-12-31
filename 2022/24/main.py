from __future__ import annotations

import math
from collections import namedtuple
from collections.abc import MutableSet
from typing import NamedTuple

import numpy as np

from tools import parse_lines, print_part

WALL = "O"
SPACE = " "
BLIZZARD = "█"
BLIZZARD_SYMBOLS = {"right": ">", "left": "<", "up": "^", "down": "v"}


def neighbour_coords(r: int, c: int, height: int, width: int) -> set:
    """
    Returns the coordinates of the four neighbours of a node in a grid,
    barring coordinates that lie outside the grid.
    (Includes wall coordinates)
    """
    neighbours = {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}

    if r == 0:
        neighbours.remove((r - 1, c))

    if r == (height - 1):
        neighbours.remove((r + 1, c))

    if c == 0:
        neighbours.remove((r, c - 1))

    if c == (width - 1):
        neighbours.remove((r, c + 1))

    return neighbours


def wall_coordinates(height: int, width: int, not_wall: list[tuple[int, int]]):
    """Returns the edge coordinates of a grid barring select coordinates given as not_wall."""
    coords = (
        {(0, c) for c in range(width)}
        | {(height - 1, c) for c in range(width)}
        | {(r, 0) for r in range(height)}
        | {(r, width - 1) for r in range(height)}
    )
    for rc in not_wall:
        coords.remove(rc)
    return coords


class Node(namedtuple("Node", ["minute", "rc"])):
    minute: int
    rc: tuple[int, int]

    def mod_node(self, mod_time) -> Node:
        """Returns equivalent node in the time-space grid."""
        return Node(self.minute % mod_time, self.rc)

    def __repr__(self):
        return f"({self.minute}, {self.rc[0]}, {self.rc[1]})"


class Explored(MutableSet):
    def __init__(self, mod_minutes: int, initvalue=()):
        self._theset = set()
        self._mod_minutes = mod_minutes
        for x in initvalue:
            self.add(x)

    def add(self, node: Node):
        mod_node = node.mod_node(self._mod_minutes)
        self._theset.add(mod_node)

    def discard(self, node: Node):
        mod_node = node.mod_node(self._mod_minutes)
        self._theset.remove(mod_node)

    def __iter__(self):
        return iter(self._theset)

    def __len__(self):
        return len(self._theset)

    def __contains__(self, node: Node):
        mod_node = node.mod_node(self._mod_minutes)
        try:
            return mod_node in self._theset
        except AttributeError:
            return False

    def clear(self, init=None):
        self._theset = set()

        init = init if init else set()
        for elem in init:
            self.add(elem)

    def __repr__(self):
        return repr(self._theset)


class Grid:
    def __init__(self, array: np.array, part):
        self._array = array

        HEIGHT, WIDTH = array.shape
        self._height = HEIGHT
        self._width = WIDTH
        self._height_internal = HEIGHT - 2
        self._width_internal = WIDTH - 2

        # minute where blizzard pattern repeats
        self._mod_minutes = math.lcm(self._height_internal, self._width_internal)

        self._start_rc = (0, 1)
        self._end_rc = (HEIGHT - 1, WIDTH - 2)
        self._goals = (
            [self._end_rc]
            if part == 1
            else [self._end_rc, self._start_rc, self._end_rc]
        )

        self._walls = wall_coordinates(
            HEIGHT, WIDTH, not_wall=[self._start_rc, self._end_rc]
        )
        self._blizzards = {
            direction: set(zip(*np.where(array == symbol)))
            for direction, symbol in BLIZZARD_SYMBOLS.items()
        }
        self._explored = Explored(self._mod_minutes)

    def _simulate_blizzards(self, minute: int) -> set:
        """Returns blizzard coordinates at the given minute."""
        right = {(r, self._mod_column(c + minute)) for r, c in self._blizzards["right"]}
        down = {(self._mod_row(r + minute), c) for r, c in self._blizzards["down"]}

        left = {(r, self._mod_column(c - minute)) for r, c in self._blizzards["left"]}
        up = {(self._mod_row(r - minute), c) for r, c in self._blizzards["up"]}

        return set().union(*[rcs for rcs in [right, down, left, up]])

    def _mod_column(self, newc: int) -> int:
        modc = newc % self._width_internal
        return modc if modc else self._width_internal

    def _mod_row(self, newr: int) -> int:
        modr = newr % self._height_internal
        return modr if modr else self._height_internal

    def _draw_array(self, node: Node):
        # clear array
        self._array[1 : self._height_internal + 1, 1 : self._width_internal + 1] = SPACE

        self._draw_walls()
        self._draw_blizzards(node.minute)

        self._array[node.rc] = "E"
        print(self._array)

    def _draw_walls(self):
        self._array[0, :] = WALL
        self._array[-1, :] = WALL
        self._array[:, 0] = WALL
        self._array[:, -1] = WALL

        self._array[self._start_rc] = SPACE
        self._array[self._end_rc] = SPACE

    def _draw_blizzards(self, minute):
        for rc in self._simulate_blizzards(minute):
            self._array[rc] = BLIZZARD

    def _current_goal(self):
        return self._goals.pop()

    def solve(self, debug: bool = False):
        # https://en.wikipedia.org/wiki/Breadth-first_search
        prev_minute = 0
        node = Node(prev_minute, self._start_rc)

        current_goal = self._current_goal()

        self._explored.add(node)
        Q = [node]

        while Q:
            node = Q.pop(0)  # FIFO

            # visualisation for debugging
            if debug and node.minute % self._height == 0:
                print(f"Currently at {node.rc} at minute {node.minute}")
                self._draw_array(node)

            next_minute = node.minute + 1
            if prev_minute != next_minute:  # this really speeds things up
                next_blizzard_rcs = self._simulate_blizzards(next_minute)

            next_nodes = neighbour_coords(*node.rc, self._height, self._width)
            next_nodes = next_nodes - self._walls - next_blizzard_rcs

            if current_goal in next_nodes:
                node = Node(next_minute, current_goal)

                print(f"Arrived at {node.rc} on minute {node.minute}")
                self._draw_array(node)

                if not self._goals:
                    break
                else:
                    current_goal = self._current_goal()

                    self._explored.clear(init=[node])
                    Q = [node]

                    continue

            next_nodes = set([Node(next_minute, rc) for rc in next_nodes])

            # option to stand still for the next move
            if node.rc not in next_blizzard_rcs:
                next_nodes.add(Node(next_minute, node.rc))

            for n_node in next_nodes:
                if n_node not in self._explored:
                    self._explored.add(n_node)
                    Q.append(n_node)

            prev_minute = next_minute


@print_part
def solve(filepath: str, part: int = 1):
    array = np.array([np.array(list(line)) for line in parse_lines(filepath)])
    grid = Grid(array, part)
    grid.solve()


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    # solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
