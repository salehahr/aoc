from collections import defaultdict
from enum import StrEnum
from typing import Callable

import numpy as np

from tools import parse_lines, print_ans, print_part
from tools.generic_types import CHAR_TO_DIRECTIONS, Coordinates, Direction


class Symbol(StrEnum):
    BOX = "O"
    WALL = "#"
    FREE = "."
    ROBOT = "@"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    BIG_BOX = "[]"


class Map:
    def __init__(self, lines: list[str], part: int):
        if part == 2:
            lines = map(self.__expand_map_row, lines)
        arr = np.array([[c for c in line] for line in lines])
        pos0 = set(Coordinates(*rc) for rc in np.argwhere(arr == "@")).pop()
        arr[pos0] = Symbol.FREE.value
        self.robot = Robot(self, pos0)

        self.__part = part
        self.__arr = arr
        self.__walls = tuple(
            Coordinates(*rc) for rc in np.argwhere(arr == Symbol.WALL.value)
        )

        self.__is_box: Callable[[Coordinates], bool] = (
            self.__is_p1_box if part == 1 else self.__is_p2_box
        )
        self.__box_symbol = Symbol.BOX.value if part == 1 else Symbol.BIG_BOX.value

    @property
    def boxes(self) -> set[Coordinates]:
        return set(
            Coordinates(*rc) for rc in np.argwhere(self.__arr == Symbol.BOX.value)
        )

    @property
    def boxes_left(self) -> set[Coordinates]:
        return set(
            Coordinates(*rc) for rc in np.argwhere(self.__arr == Symbol.BOX_LEFT.value)
        )

    @property
    def boxes_right(self) -> set[Coordinates]:
        return set(
            Coordinates(*rc) for rc in np.argwhere(self.__arr == Symbol.BOX_RIGHT.value)
        )

    def is_free(self, rc: Coordinates) -> bool:
        return self.__arr[rc] == Symbol.FREE.value

    def is_wall(self, rc: Coordinates) -> bool:
        return rc in self.__walls

    def __is_p1_box(self, rc: Coordinates) -> bool:
        return rc in self.boxes

    def __is_p2_box(self, rc: Coordinates) -> bool:
        return rc in self.boxes_left | self.boxes_right

    def __pictogram(self, n: int) -> list[str]:
        return list(n * str(self.__box_symbol))

    def __move_box_vert(self, direction: Direction, box: Coordinates) -> bool:
        next_rcs = defaultdict(set)
        i = 0
        next_rcs[i] = self.__box_set(box)
        while l_boxes := next_rcs[i]:
            next_boxes = [lb + direction for lb in l_boxes]
            if any(map(self.is_wall, next_boxes)):
                return False
            elif all(map(self.is_free, next_boxes)):
                break

            for next_box in next_boxes:
                next_rcs[i + 1] |= self.__box_set(next_box)

            i += 1

        for boxes in reversed(next_rcs.values()):
            for old_box in boxes:
                new_box = old_box + direction
                if old_box in self.boxes_left:
                    sym = Symbol.BOX_LEFT.value
                elif old_box in self.boxes_right:
                    sym = Symbol.BOX_RIGHT.value
                else:
                    sym = Symbol.BOX.value
                self.__arr[new_box] = sym
                self.__arr[old_box] = Symbol.FREE.value
        return True

    def __move_box_horz(
        self, direction: Direction, box: Coordinates, target: Coordinates
    ) -> bool:
        num_boxes = abs(box.c - target.c)
        c_start = target.c if direction == Direction.LEFT else box.c + 1
        c_end = c_start + num_boxes
        if self.__part == 2:
            num_boxes = num_boxes // 2
        rows, cols = target.r, range(c_start, c_end)

        self.__arr[rows, cols] = self.__pictogram(num_boxes)
        self.__arr[self.robot.pos + direction] = Symbol.FREE.value

        return True

    def __box_set(self, box: Coordinates) -> set[Coordinates]:
        if self.__is_box(box):
            if box in self.boxes_left:
                other = box + Direction.RIGHT
                return {other, box}
            elif box in self.boxes_right:
                other = box + Direction.LEFT
                return {other, box}
            else:
                return {box}
        else:
            return set()

    def print(self, robot_loc: Coordinates = None):
        robot_loc = robot_loc if robot_loc else self.robot.pos
        self.__arr[robot_loc] = Symbol.ROBOT.value
        for line in self.__arr:
            line = "".join(line)
            print(line)
        self.__arr[robot_loc] = Symbol.FREE.value

    @staticmethod
    def __expand_map_row(line: str) -> str:
        line = line.replace(Symbol.WALL.value, 2 * Symbol.WALL.value)
        line = line.replace(Symbol.FREE.value, 2 * Symbol.FREE.value)
        line = line.replace(Symbol.ROBOT.value, Symbol.ROBOT.value + Symbol.FREE.value)
        line = line.replace(Symbol.BOX.value, Symbol.BIG_BOX.value)
        return line

    def move_box(
        self,
        first_box_rc: Coordinates,
        direction: Direction,
    ) -> bool:
        delta = (
            2 * direction.value
            if (self.__part == 2 and direction.is_horizontal)
            else direction.value
        )
        target_rc = first_box_rc + delta
        while True:
            if self.is_wall(target_rc):
                return False

            if self.is_free(target_rc):
                if direction.is_vertical:
                    return self.__move_box_vert(direction, first_box_rc)
                else:
                    return self.__move_box_horz(direction, first_box_rc, target_rc)

            target_rc += delta


class Robot:
    def __init__(self, map_: Map, pos0: Coordinates) -> None:
        self._map = map_
        self.pos = pos0

    def move(self, direction: Direction):
        next_rc = self.pos + direction
        if self._map.is_wall(next_rc):
            return

        if self._map.is_free(next_rc):
            self.pos = next_rc
            return

        if self._map.move_box(next_rc, direction):
            self.pos = next_rc


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    sep_index = lines.index("")
    map_ = Map(lines[:sep_index], part)
    directions = [CHAR_TO_DIRECTIONS[d] for d in "".join(lines[sep_index + 1 :])]

    while directions:
        direction = directions.pop(0)
        map_.robot.move(direction)
    map_.print()

    boxes = map_.boxes if part == 1 else map_.boxes_left
    gpses = sum(r * 100 + c for r, c in boxes)

    if "short" in filepath:
        print_ans(gpses, correct_ans=10092 if part == 1 else 9021)
    else:
        print_ans(gpses, correct_ans=1436690 if part == 1 else 1482350)


if __name__ == "__main__":
    # FILEPATH = "input_short"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
