# https://adventofcode.com/2021/day/7
from collections import Counter

import context

from tools import parse_lines, print_part


def abs_diff(pos: int, ref_pos: int) -> int:
    return abs(pos - ref_pos)


def sum_int(pos: int, ref_pos: int) -> int:
    n = abs_diff(pos, ref_pos)
    return n * (n + 1) // 2


@print_part
def solve(filepath: str, part: int = 1):
    horz_pos0 = [int(x) for x in parse_lines(filepath)[0].split(",")]
    positions = list(range(min(horz_pos0), max(horz_pos0) + 1))

    best_fuel = 10000000000
    calc_fuel = abs_diff if part == 1 else sum_int

    for ref_pos in positions:
        fuel = sum([calc_fuel(x0, ref_pos) for x0 in horz_pos0])
        if fuel < best_fuel:
            best_fuel = fuel
    print(best_fuel)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
