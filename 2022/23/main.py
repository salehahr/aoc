import collections
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np

from tools import parse_lines, print_part

SPACE = "-"
ELF = "█"
NUM_PADDING = 5


def input_array(filepath):
    lines = [
        [SPACE if c == "." else ELF for c in line] for line in parse_lines(filepath)
    ]
    return np.array([np.array(line) for line in lines])


class Moves(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


@dataclass
class Elf:
    rc: tuple[int, int]
    proposed: Any = None

    def __repr__(self):
        return f"({self.rc}, {self.proposed})"

    @property
    def r(self):
        return self.rc[0]

    @property
    def c(self):
        return self.rc[-1]


def pad_array(array):
    need_padding = check_need_padding(array)

    if need_padding:
        array = np.pad(array, NUM_PADDING, constant_values=SPACE)

    return array, [Elf(rc) for rc in zip(*np.where(array == ELF))]


def check_need_padding(array):
    height, width = array.shape
    elf_positions = set(zip(*np.where(array == ELF)))
    for r, c in elf_positions:
        if r == 0 or r == (height - 1) or c == 0 or c == (width - 1):
            return True
    return False


def rearrange_moves(moves):
    first_move = moves.pop(0)
    moves.append(first_move)


def neighbour_coords(r, c):
    return [
        (row, col)
        for row in range(r - 1, r + 2)
        for col in range(c - 1, c + 2)
        if (r, c) != (row, col)
    ]


def execute_moves(array, elves, to_ignore):
    for elf in elves:
        if elf.proposed and elf.proposed not in to_ignore:
            array[elf.rc] = SPACE
            array[elf.proposed] = ELF


def unpad(array):
    height, width = array.shape
    for min_row in range(height):
        if ELF in array[min_row, :]:
            break
    for max_row in range(height - 1, min_row, -1):
        if ELF in array[max_row, :]:
            break
    for min_col in range(width):
        if ELF in array[:, min_col]:
            break
    for max_col in range(width - 1, min_col, -1):
        if ELF in array[:, max_col]:
            break
    return array[min_row : max_row + 1, min_col : max_col + 1]


@print_part
def solve(filepath: str, part: int = 1):
    array = input_array(filepath)
    desired_moves = [m for m in Moves]

    rd = 1
    while True:
        array, elves = pad_array(array)

        proposed, duplicates = set(), set()
        for i, elf in enumerate(elves):
            set_proposed_move(elf, array, desired_moves, proposed, duplicates)
        execute_moves(array, elves, to_ignore=duplicates)
        rearrange_moves(desired_moves)

        if part == 1 and rd == 10:
            num_tiles = len(np.argwhere(unpad(array) == SPACE))
            print(num_tiles)
            return
        if part == 2 and sum([1 for elf in elves if elf.proposed]) == 0:
            print(rd)
            return

        rd += 1


def set_proposed_move(elf, array, moves, proposed, duplicates):
    has_elf_neighbour = any([array[rc] == ELF for rc in neighbour_coords(*elf.rc)])
    if not has_elf_neighbour:
        return

    for move in moves:
        delta_r, delta_c = move.value
        row, col = elf.r + delta_r, elf.c + delta_c
        if delta_r and ELF not in array[row, (col - 1) : (col + 2)]:
            break
        elif delta_c and ELF not in array[(row - 1) : (row + 2), col]:
            break
    else:
        return

    if (row, col) in proposed:
        duplicates.add((row, col))
    else:
        proposed.add((row, col))
        elf.proposed = (row, col)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
