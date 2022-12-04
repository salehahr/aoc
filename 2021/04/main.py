# https://adventofcode.com/2021/day/4

from __future__ import annotations

from copy import copy

import context
import numpy as np

from tools import parse_lines, print_part


def parse_bingo(filepath) -> Tuple[List[int], List[Board]]:
    raw = parse_lines(filepath)

    numbers_ = [int(n_) for n_ in raw[0].split(",")]

    raw_boards = [b for b in raw[1:] if len(b) > 0]
    num_boards = len(raw_boards) // 5
    boards_ = [Board(raw_boards[i * 5 : i * 5 + 5]) for i in range(num_boards)]

    return numbers_, boards_


def parse_board(list_of_nums):
    return np.array([[int(num) for num in line.split()] for line in list_of_nums])


class Board(object):
    MARKED_NEGATIVE = -3

    def __init__(self, raw_repr):
        self._data = parse_board(raw_repr)

    def _elem_exists(self, elem: int):
        idx = np.argwhere(self._data == elem)
        return len(idx) > 0

    def _elem_index(self, elem: int) -> Tuple[int, int]:
        return np.argwhere(self._data == elem)[0]

    def mark(self, elem: int):
        if not self._elem_exists(elem):
            return

        row, col = self._elem_index(elem)
        self._data[row, col] = Board.MARKED_NEGATIVE

    @property
    def winning_paths(self):
        rows = [(self._data[rc, :], self._data[:, rc]) for rc in range(5)]
        return [r for rc in rows for r in rc]

    @property
    def has_win(self):
        for wp in self.winning_paths:
            if np.all(wp < 0):
                return True
        return False

    @property
    def unmarked_numbers(self):
        return self._data[self._data >= 0]


def get_first_winning_board(numbers_, boards_):
    winner = None

    for n in numbers_:
        for board in boards_:
            board.mark(n)

            if board.has_win:
                winner = board
                break

        if winner is not None:
            break

    return winner, n


def get_last_winning_board(numbers_, boards_):
    winner = None
    boards_list = copy(boards_)

    num_boards = len(boards_)
    num_won = 0

    for n in numbers_:
        for board in boards_list:
            board.mark(n)

            if board.has_win:
                num_won += 1

            if num_boards == num_won:
                winner = board
                break

        if winner is None:
            boards_list = [b for b in boards_list if not b.has_win]
        else:
            break

    return winner, n


@print_part
def solve(filepath: str, part: int = 1):
    numbers, boards = parse_bingo(filepath)

    if part == 1:
        winning_board, n = get_first_winning_board(numbers, boards)
    else:
        winning_board, n = get_last_winning_board(numbers, boards)

    score = sum(winning_board.unmarked_numbers) * n
    print(score)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
