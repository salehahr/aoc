import re

from tools import parse_lines, print_ans, print_part
from tools.generic_types import Coordinates

XY_PATTERN = r"X[+-=](\d+), Y[+-=](\d+)"
COST_A = 3
COST_B = 1
P2_OFFSET = 10000000000000


def __get_xy_values(line: str) -> Coordinates:
    return Coordinates(*[int(x) for x in re.search(XY_PATTERN, line).groups()])


@print_part
def solve(filepath: str, part: int = 1):
    def __constraints_ok(n_pushes: float) -> bool:
        is_int = n_pushes == int(n_pushes)
        within_max = (n_pushes <= 100) if part == 1 else True
        return is_int and within_max

    lines = tuple(line for line in parse_lines(filepath) if line)
    machines = tuple(lines[i : i + 3] for i in range(0, len(lines), 3))

    total_cost = 0
    for machine in machines:
        a, b, prize = map(__get_xy_values, machine)
        if part == 2:
            prize = Coordinates(prize.r + P2_OFFSET, prize.c + P2_OFFSET)

        # 2d equations
        # a.r*na + b.r*nb = prize.r
        # a.c*na + b.c*nb = prize.c
        determinant = a.r * b.c - a.c * b.r
        na = (prize.r * b.c - prize.c * b.r) / determinant
        nb = (prize.c * a.r - prize.r * a.c) / determinant

        if __constraints_ok(na) and __constraints_ok(nb):
            total_cost += int(na * COST_A + nb * COST_B)

    print_ans(total_cost, correct_ans=31897 if part == 1 else 87596249540359)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
